"""Render the curated doc set to styled HTML under site/. Rerun after editing any .md."""

from __future__ import annotations

import posixpath
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

# Repo-relative sources; each renders to site/<same path>.html (lowercased name).
RENDER = [
    "FINDINGS.md",
    "share/team_summary.md",
    "share/one_pager.md",
    "docs/STEM.md",
    "docs/STEM_18mo.md",
    "docs/codebook_v2.md",
    "docs/failures.md",
    "docs/JUDGE.md",
    "docs/TURN2.md",
    "docs/NAMES.md",
    "docs/GOAL.md",
    "docs/RUNS.md",
    "docs/CHANGELOG.md",
    "docs/instrument_catches.md",
    "docs/human_parallels.md",
    "docs/combination_lit.md",
    "docs/error_origins.md",
    "results/README.md",
    "results/smoke_20260815T160303Z_tiebreak.md",
    "results/smoke_20260815T160303Z_adjudication.md",
    "results/smoke_20260815T160303Z_findings.md",
    "results/turn2_summary.md",
    "results/worst_answer_collage.md",
    "results/smoke_20260815T170727Z_notes.md",
    "results/smoke_20260815T181825Z_notes.md",
    "results/smoke_20260815T184406Z_notes.md",
    "results/smoke_20260815T185357Z_notes.md",
    "results/smoke_20260815T190148Z_notes.md",
    "results/smoke_20260815T192236Z_notes.md",
    "results/smoke_20260815T214424Z_notes.md",
    "results/smoke_20260815T214553Z_notes.md",
]


def out_rel(src: str) -> str:
    p = posixpath.dirname(src)
    stem = posixpath.basename(src)[:-3].lower()
    return f"{p}/{stem}.html" if p else f"{stem}.html"


OUT_FOR = {src: out_rel(src) for src in RENDER}

CSS = """\
:root {
  --paper: #f7f5ef; --ink: #23262b; --muted: #686c74; --line: #d8d4ca;
  --hairline: #e6e2d8; --card: #fcfbf8; --accent: #1d5c88; --rust: #96471c;
  --mark: #eeeade; --selection: #d9e5ee;
  --serif: "Charter", "Bitstream Charter", "Sitka Text", Cambria, Georgia, serif;
  --sans: -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :root { --paper: #17181c; --ink: #e5e3dd; --muted: #9b9fa7; --line: #34363d;
          --hairline: #26282e; --card: #1d1f24; --accent: #82b4dc; --rust: #d69a6e;
          --mark: #24262c; --selection: #2c3f50; }
}
* { box-sizing: border-box; }
::selection { background: var(--selection); }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 2px; }
html { scrollbar-color: var(--line) transparent; }
body { margin: 0; background: var(--paper); color: var(--ink);
       font: 17px/1.65 var(--serif);
       font-feature-settings: "onum" 0; caret-color: var(--accent); }
main { max-width: 74ch; margin: 0 auto; padding: 1.25rem 1.25rem 5rem; }
nav { max-width: 74ch; margin: 0 auto; padding: 1.1rem 1.25rem 0;
      font: .82rem/1.4 var(--sans); color: var(--muted);
      display: flex; gap: .6rem; align-items: baseline; flex-wrap: wrap; }
nav a { color: var(--accent); text-decoration: none; letter-spacing: .01em; }
nav a:hover { text-decoration: underline; text-underline-offset: 3px; }
nav span { font-family: var(--mono); font-size: .78rem; color: var(--muted); opacity: .8; }
h1 { font-size: 1.85rem; line-height: 1.2; margin: 1.4rem 0 .9rem;
     letter-spacing: -.012em; text-wrap: balance; }
h2 { font-size: 1.28rem; margin: 2.4rem 0 .7rem; letter-spacing: -.008em;
     padding-bottom: .35rem; border-bottom: 1px solid var(--hairline); text-wrap: balance; }
h3 { font-size: 1.05rem; margin: 1.7rem 0 .45rem; }
p, li { max-width: 70ch; }
a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 3px;
    text-decoration-color: color-mix(in srgb, var(--accent) 45%, transparent); }
a:hover { text-decoration-color: var(--accent); }
strong { letter-spacing: .002em; }
code { font: .82em var(--mono); background: var(--mark);
       padding: .12em .38em; border-radius: 4px; }
pre { background: var(--mark); border: 1px solid var(--hairline); border-radius: 6px;
      padding: .9rem 1.05rem; overflow-x: auto; font-size: .82rem; line-height: 1.55; }
pre code { background: none; padding: 0; font-size: 1em; }
blockquote { margin: 1.2rem 0; padding: .1rem 0 .1rem 1.1rem; color: var(--muted);
             border-left: 1px solid var(--line); font-style: italic; }
blockquote strong { font-style: normal; }
.scroll { overflow-x: auto; scrollbar-width: thin; margin: 1.1rem 0; }
table { border-collapse: collapse; width: 100%;
        font: .855rem/1.5 var(--sans); font-variant-numeric: tabular-nums; }
th, td { text-align: left; padding: .5rem .65rem .5rem 0; padding-right: 1.1rem;
         border-bottom: 1px solid var(--hairline); vertical-align: top; }
tr:last-child td { border-bottom-color: var(--line); }
thead th, tr:first-child th { color: var(--muted); font-weight: 600; font-size: .78rem;
     letter-spacing: .015em; border-bottom: 1px solid var(--line); }
hr { border: none; border-top: 1px solid var(--hairline); margin: 2.4rem 0; }
img { max-width: 100%; }
@media print {
  nav { display: none; }
  body { background: #fff; color: #000; font-size: 11pt; }
  a { color: inherit; text-decoration: none; }
}
"""

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{root}site/style.css">
</head>
<body>
<nav><a href="{root}index.html">&larr; They completed the chart</a> &middot; <span>{crumb}</span></nav>
<main>
{body}
</main>
</body>
</html>
"""


def rewrite_links(html: str, src: str) -> str:
    """Point .md links at rendered pages; other relative links back into the repo tree."""
    src_dir = posixpath.dirname(src)
    page_dir = posixpath.dirname(OUT_FOR[src])  # relative to site/

    def fix(match: re.Match) -> str:
        href = match.group(1)
        if href.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        target = posixpath.normpath(posixpath.join(src_dir, href))
        if target in OUT_FOR:
            new = posixpath.relpath(OUT_FOR[target], page_dir or ".")
        else:
            depth = (page_dir.count("/") + 1) if page_dir else 0
            new = "../" * (depth + 1) + target
        return f'href="{new}"'

    return re.sub(r'href="([^"]+)"', fix, html)


def render(src: str) -> None:
    md = (ROOT / src).read_text(encoding="utf-8")
    title_match = re.search(r"^# (.+)$", md, re.M)
    title = title_match.group(1).strip() if title_match else src
    title = re.sub(r"[`*]", "", title)
    body = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html"],
        input=md, capture_output=True, text=True, check=True,
    ).stdout
    body = rewrite_links(body, src)
    body = body.replace("<table>", '<div class="scroll"><table>').replace("</table>", "</table></div>")
    out = SITE / OUT_FOR[src]
    depth = OUT_FOR[src].count("/")
    root = "../" * (depth + 1)
    crumb = src
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(TEMPLATE.format(title=title, root=root, crumb=crumb, body=body), encoding="utf-8")


def main() -> None:
    SITE.mkdir(exist_ok=True)
    (SITE / "style.css").write_text(CSS, encoding="utf-8")
    for src in RENDER:
        render(src)
    print(f"rendered {len(RENDER)} pages -> site/")


if __name__ == "__main__":
    main()
