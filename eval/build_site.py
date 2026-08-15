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
  --bg: #faf9f6; --ink: #1e2126; --muted: #6b7280; --line: #e4e1da;
  --card: #ffffff; --accent: #145a8a; --accent2: #8a4514; --mark: #f3efe6;
}
@media (prefers-color-scheme: dark) {
  :root { --bg: #16181d; --ink: #e8e6e1; --muted: #9aa0aa; --line: #2c2f36;
          --card: #1d2026; --accent: #6db3e8; --accent2: #e8a36d; --mark: #262a31; }
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink);
       font: 16px/1.65 -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }
main { max-width: 800px; margin: 0 auto; padding: 1.5rem 1.25rem 4rem; }
nav { max-width: 800px; margin: 0 auto; padding: 1rem 1.25rem 0;
      font-size: .9rem; color: var(--muted); }
nav a { color: var(--accent); text-decoration: none; }
nav a:hover { text-decoration: underline; }
h1 { font-size: 1.7rem; line-height: 1.25; margin: 1rem 0 .75rem; }
h2 { font-size: 1.2rem; margin: 2rem 0 .6rem; border-bottom: 1px solid var(--line); padding-bottom: .3rem; }
h3 { font-size: 1.05rem; margin: 1.5rem 0 .4rem; }
a { color: var(--accent); }
code { font: .875em ui-monospace, "SF Mono", Menlo, Consolas, monospace;
       background: var(--mark); padding: .1em .35em; border-radius: 4px; }
pre { background: var(--mark); border: 1px solid var(--line); border-radius: 8px;
      padding: .9rem 1rem; overflow-x: auto; }
pre code { background: none; padding: 0; }
blockquote { margin: 1rem 0; padding: .2rem 0 .2rem 1rem; color: var(--muted);
             border-left: 2px solid var(--line); }
.scroll { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: .93rem; }
th, td { text-align: left; padding: .45rem .6rem; border-bottom: 1px solid var(--line); vertical-align: top; }
th { color: var(--muted); font-weight: 600; }
hr { border: none; border-top: 1px solid var(--line); margin: 2rem 0; }
img { max-width: 100%; }
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
