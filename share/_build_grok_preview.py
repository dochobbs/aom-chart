#!/usr/bin/env python3
"""Assemble the Grok 4.6 AI-2027-style essay preview. Throwaway builder."""

from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "compared_to_whom_grok-4.6.html"


def essay_body() -> str:
    md = (ROOT / "compared_to_whom_grok-4.6.md").read_text(encoding="utf-8")
    body_md = md.split("\n---\n", 1)[1].strip()
    body = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html"],
        input=body_md, capture_output=True, text=True, check=True,
    ).stdout
    body = body.replace("<table>", '<div class="scroll"><table>').replace(
        "</table>", "</table></div>"
    )
    scene = {
        "compared-to-whom": "open",
        "an-easy-case-on-purpose": "case",
        "the-part-we-dont-say-out-loud": "human",
        "why-they-err-like-us": "roots",
        "the-cheap-fix-nobody-ships": "fix",
        "adding-a-doctor-can-subtract": "combo",
        "where-the-combination-actually-works": "synergy",
        "the-experiment-nobody-has-run": "hypothesis",
        "the-four-second-question": "close",
    }
    parts = re.split(r'(<h[12] id="[^"]+"[^>]*>)', body)
    out = []
    i = 0
    if parts and not parts[0].startswith("<h"):
        out.append(parts[0])
        i = 1
    chunks = parts[i:]
    j = 0
    acc = []
    current = "open"

    def flush(s, pieces):
        inner = "".join(pieces)
        if not inner.strip():
            return ""
        return f'<section class="scene" data-scene="{s}">{inner}</section>\n'

    while j < len(chunks):
        tag = chunks[j]
        nxt = chunks[j + 1] if j + 1 < len(chunks) else ""
        m = re.search(r'id="([^"]+)"', tag)
        new_scene = scene.get(m.group(1), current) if m else current
        if acc and new_scene != current:
            out.append(flush(current, acc))
            acc = []
            current = new_scene
        elif not acc:
            current = new_scene
        acc.append(tag + nxt)
        j += 2
    if acc:
        out.append(flush(current, acc))
    body = "".join(out)

    models = [
        ("Fable", 13), ("Sonnet", 13), ("Opus", 11), ("Haiku", 5),
        ("G. Pro", 4), ("Grok", 4), ("Terra", 4),
        ("Flash", 1), ("Luna", 1), ("Sol", 1),
    ]
    rows = []
    for name, n in models:
        cells = "".join(
            f'<i class="{"on" if k < n else "off"}"></i>' for k in range(14)
        )
        rows.append(
            f'<div class="dot-row"><span>{name}</span><b>{cells}</b><em>{n}</em></div>'
        )
    dot_fig = (
        '<figure class="figure dots-figure">'
        "<figcaption>140 answers. Each row is a model; each cell is a trace. "
        "Filled = at least one invented chart fact. Counts from the packet; "
        "fill order is schematic.</figcaption>"
        '<div class="dot-grid" role="img" aria-label="Ten models, fourteen traces each. 57 of 140 invented a chart fact.">'
        + "".join(rows)
        + "</div>"
        '<p class="figure-foot"><strong>57</strong> of 140 · 41%</p>'
        "</figure>\n"
    )
    score_fig = """
<figure class="figure score-figure">
  <figcaption>Goh et al., JAMA Network Open 2024. The 92 is the study team prompting the model, not the doctors' chat.</figcaption>
  <div class="score-bars" role="img" aria-label="AI alone 92 percent, doctors with AI 76, doctors 74.">
    <div class="score-bar is-ai" style="--v:92"><span>AI alone</span><i></i><b>92</b></div>
    <div class="score-bar" style="--v:76"><span>Doctors + AI</span><i></i><b>76</b></div>
    <div class="score-bar" style="--v:74"><span>Doctors</span><i></i><b>74</b></div>
  </div>
</figure>
"""
    fix_fig = """
<figure class="figure fix-figure">
  <figcaption>Four reachable models, 56 answers, same regex both sides. Fable (13/14) was not available for the rerun.</figcaption>
  <div class="fix-bars" role="img" aria-label="Invention rate 24 of 56 on the bare prompt, 6 of 56 with one sentence.">
    <div class="fix-bar before"><span>Bare prompt</span><i></i><b>24/56</b></div>
    <div class="fix-bar after"><span>One sentence</span><i></i><b>6/56</b></div>
  </div>
</figure>
"""
    body = body.replace(
        "<p>The prose above keeps the models anonymous",
        dot_fig + "<p>The prose above keeps the models anonymous",
        1,
    )
    idx = body.find("Invented facts fell from 24 of 56")
    close = body.find("</table></div>", idx)
    insert_at = close + len("</table></div>")
    body = body[:insert_at] + fix_fig + body[insert_at:]
    m = re.search(
        r"The AI alone scored 92 percent\..{0,200}were having\.</p>", body, re.S
    )
    if not m:
        raise SystemExit("missing 92 paragraph")
    body = body[: m.end()] + score_fig + body[m.end() :]
    return body


BODY = essay_body()

CSS = r"""
:root {
  --paper: #f4f1ea; --ink: #1c1d21; --muted: #5e6168; --line: #d3cec4;
  --hairline: #e3dfd5; --card: #faf8f3; --accent: #1d5c88; --rust: #8d431c;
  --mark: #ece7db; --selection: #d5e4ee; --fill: #1d5c88;
  --human: #8d431c; --machine: #1d5c88;
  --serif: "Charter", "Bitstream Charter", "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
  --ui: -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  --gutter: clamp(1rem, 3vw, 2.2rem);
}
@media (prefers-color-scheme: dark) {
  :root {
    --paper: #14151a; --ink: #e7e4dc; --muted: #9a9ea6; --line: #2f3238;
    --hairline: #26282e; --card: #1b1d22; --accent: #8bb8d8; --rust: #d39a70;
    --mark: #22242a; --selection: #2c3f50; --fill: #8bb8d8;
    --human: #d39a70; --machine: #8bb8d8;
  }
}
* { box-sizing: border-box; }
html { scrollbar-color: var(--line) transparent; scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .progress-bar, .panel-state, .score-bar i, .fix-bar i, .dot-row i.on {
    transition: none !important; animation: none !important;
  }
}
::selection { background: var(--selection); }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
body {
  margin: 0; background: var(--paper); color: var(--ink);
  font: 18px/1.62 var(--serif);
  font-feature-settings: "onum" 0, "kern" 1;
  caret-color: var(--accent);
}
.skip {
  position: absolute; left: .8rem; top: .8rem; transform: translateY(-160%);
  background: var(--ink); color: var(--paper); padding: .45rem .7rem;
  font: 700 .78rem/1 var(--ui); text-decoration: none; z-index: 80;
}
.skip:focus { transform: none; }
.progress {
  position: fixed; inset: 0 0 auto; height: 3px; z-index: 60;
  background: transparent; pointer-events: none;
}
.progress-bar {
  display: block; height: 100%; width: 100%;
  background: var(--ink);
  transform: scaleX(0); transform-origin: left;
  transition: transform .12s linear;
}
.topbar {
  display: flex; justify-content: space-between; align-items: baseline;
  gap: 1rem; flex-wrap: wrap;
  padding: .85rem var(--gutter) .8rem;
  border-bottom: 1px solid var(--hairline);
  font: 600 .72rem/1.3 var(--ui);
  letter-spacing: .04em;
  text-transform: uppercase;
  color: var(--muted);
  background: var(--paper);
  position: sticky; top: 0; z-index: 40;
}
.topbar .model { color: var(--rust); letter-spacing: .08em; }
.page {
  display: grid;
  grid-template-columns: minmax(0, 42rem) minmax(16rem, 22rem);
  gap: clamp(1.5rem, 4vw, 3.5rem);
  max-width: 74rem;
  margin: 0 auto;
  padding: 1.4rem var(--gutter) 6rem;
  align-items: start;
}
.essay { min-width: 0; }
.essay h1 {
  font-size: clamp(2.4rem, 6vw, 3.6rem);
  line-height: 1.05; letter-spacing: -.03em;
  margin: 1.1rem 0 1.4rem; font-weight: 600;
  text-wrap: balance;
}
.essay h2 {
  font-size: 1.38rem; line-height: 1.25; letter-spacing: -.014em;
  margin: 2.8rem 0 .65rem; padding-bottom: .4rem;
  border-bottom: 1px solid var(--hairline);
  text-wrap: balance;
}
.essay h3 { font-size: 1.05rem; margin: 1.7rem 0 .4rem; }
.essay p, .essay li { max-width: 40rem; }
.essay p { margin: 0 0 1.05rem; }
.essay a {
  color: var(--accent);
  text-decoration-thickness: 1px;
  text-underline-offset: 3px;
  text-decoration-color: color-mix(in srgb, var(--accent) 40%, transparent);
}
.essay a:hover { text-decoration-color: var(--accent); }
.essay blockquote {
  margin: 1.15rem 0 1.3rem; padding: .15rem 0 .15rem 1rem;
  color: var(--muted); border-left: 1px solid var(--line); font-style: italic;
}
.essay blockquote strong { font-style: normal; }
.essay hr { border: none; border-top: 1px solid var(--hairline); margin: 2.4rem 0; }
.essay em { font-style: italic; }
.scroll { overflow-x: auto; scrollbar-width: thin; margin: 1.2rem 0; }
table {
  border-collapse: collapse; width: 100%;
  font: .82rem/1.5 var(--ui); font-variant-numeric: tabular-nums;
}
th, td {
  text-align: left; padding: .48rem .7rem .48rem 0;
  border-bottom: 1px solid var(--hairline); vertical-align: top;
}
thead th { color: var(--muted); font-weight: 600; font-size: .74rem; letter-spacing: .02em; }
.figure {
  margin: 1.6rem 0 1.9rem; padding: 1rem 0 0;
  border-top: 1px solid var(--line);
}
.figure figcaption {
  font: .78rem/1.45 var(--ui); color: var(--muted); margin: 0 0 .85rem;
  max-width: 40rem;
}
.figure-foot {
  font: 600 .8rem/1.3 var(--ui); font-variant-numeric: tabular-nums;
  margin: .7rem 0 0; color: var(--ink);
}
.dot-grid { display: grid; gap: .28rem; }
.dot-row {
  display: grid; grid-template-columns: 4.6rem 1fr 1.6rem;
  align-items: center; gap: .45rem;
  font: 600 .68rem/1 var(--ui); letter-spacing: .02em;
  color: var(--muted);
}
.dot-row b { display: flex; gap: 3px; }
.dot-row em {
  font-style: normal; font-variant-numeric: tabular-nums;
  text-align: right; color: var(--ink);
}
.dot-row i {
  width: 9px; height: 9px; display: block;
  border: 1px solid var(--line); background: transparent;
}
.dot-row i.on {
  background: var(--machine); border-color: var(--machine);
}
.score-bars, .fix-bars { display: grid; gap: .55rem; max-width: 36rem; }
.score-bar, .fix-bar {
  display: grid; grid-template-columns: 7.2rem 1fr 2.4rem;
  gap: .55rem; align-items: center;
  font: 600 .78rem/1 var(--ui); font-variant-numeric: tabular-nums;
}
.score-bar span, .fix-bar span { color: var(--muted); }
.score-bar i, .fix-bar i {
  display: block; height: 9px; background: var(--ink);
  transform-origin: left; width: calc(var(--v) * 1%);
}
.score-bar.is-ai i { background: var(--machine); }
.fix-bar.before i { width: 43%; background: var(--machine); }
.fix-bar.after i { width: 11%; background: var(--ink); }

.instrument {
  position: sticky; top: 3.2rem;
  border: 1px solid var(--line);
  background: var(--card);
  padding: 1rem 1.05rem 1.15rem;
  align-self: start;
}
.inst-label {
  font: 600 .68rem/1.2 var(--ui);
  letter-spacing: .08em; text-transform: uppercase;
  color: var(--muted); margin: 0 0 .85rem;
  padding-bottom: .55rem; border-bottom: 1px solid var(--hairline);
}
.panel-state { display: none; }
.panel-state.is-on { display: block; }
.stat-xl {
  font-size: 3.1rem; line-height: .9; letter-spacing: -.04em;
  font-weight: 600; font-variant-numeric: tabular-nums;
  margin: .15rem 0 .35rem;
}
.stat-xl small {
  display: block; font: 600 .72rem/1.3 var(--ui);
  letter-spacing: .06em; text-transform: uppercase;
  color: var(--muted); margin-top: .45rem;
}
.stat-note {
  font: .8rem/1.45 var(--ui); color: var(--muted); margin: .4rem 0 0;
}
.pair {
  display: grid; grid-template-columns: 1fr 1fr; gap: .8rem;
  margin-top: .2rem;
}
.pair h3 {
  font: 600 .68rem/1.2 var(--ui); letter-spacing: .07em;
  text-transform: uppercase; margin: 0 0 .45rem;
  padding-bottom: .3rem; border-bottom: 1px solid var(--hairline);
}
.pair.machine h3, .col.machine h3 { color: var(--machine); }
.pair .col.human h3 { color: var(--human); }
.pair ul { list-style: none; margin: 0; padding: 0; }
.pair li {
  font: .78rem/1.4 var(--ui); margin: 0 0 .4rem;
  padding-left: .7rem; position: relative;
}
.pair li::before {
  content: ""; position: absolute; left: 0; top: .45rem;
  width: 6px; height: 6px; background: var(--ink);
}
.col.machine li::before { background: var(--machine); }
.col.human li::before { background: var(--human); }
.mini-dots { margin: .6rem 0 .2rem; }
.mini-dots .dot-row span { font-size: .6rem; }
.mini-dots .dot-row i { width: 6px; height: 6px; }
.ticks { display: grid; gap: .45rem; margin-top: .2rem; }
.tick {
  display: grid; grid-template-columns: 1fr auto; gap: .4rem;
  font: .78rem/1.3 var(--ui); font-variant-numeric: tabular-nums;
  padding-bottom: .4rem; border-bottom: 1px solid var(--hairline);
}
.tick b { font-weight: 600; }
.q {
  font-size: 1.35rem; line-height: 1.25; letter-spacing: -.02em;
  margin: .3rem 0 .5rem;
}
.mobile-meter {
  display: none;
  position: fixed; left: 0; right: 0; bottom: 0; z-index: 45;
  padding: .65rem 1rem calc(.65rem + env(safe-area-inset-bottom));
  background: var(--paper);
  border-top: 1px solid var(--line);
  font-variant-numeric: tabular-nums;
  justify-content: space-between; align-items: baseline; gap: 1rem;
}
.mobile-meter .mm-k {
  font: 600 .68rem/1 var(--ui); letter-spacing: .08em;
  text-transform: uppercase; color: var(--muted);
}
.mobile-meter .mm-v {
  font: 600 1.05rem/1 var(--serif); letter-spacing: -.02em;
}
@media (max-width: 980px) {
  .page { grid-template-columns: minmax(0, 42rem); padding-bottom: 5.5rem; }
  .instrument { display: none; }
  .mobile-meter { display: flex; }
  .essay h1 { font-size: 2.2rem; }
}
@media print {
  .topbar, .progress, .instrument, .mobile-meter, .skip { display: none !important; }
  .page { display: block; padding: 0; }
  body { background: #fff; color: #000; }
  a { color: inherit; text-decoration: none; }
}
"""

# Mini dot rows for the sticky instrument
models = [
    ("Fable", 13), ("Sonnet", 13), ("Opus", 11), ("Haiku", 5),
    ("G. Pro", 4), ("Grok", 4), ("Terra", 4),
    ("Flash", 1), ("Luna", 1), ("Sol", 1),
]
mini_rows = []
for name, n in models:
    cells = "".join(f'<i class="{"on" if k < n else "off"}"></i>' for k in range(14))
    mini_rows.append(
        f'<div class="dot-row"><span>{name}</span><b>{cells}</b><em>{n}</em></div>'
    )
mini_grid = f'<div class="dot-grid mini-dots">{"".join(mini_rows)}</div>'

INSTRUMENT = f"""
<aside class="instrument" aria-label="Evidence, updates as you read">
  <p class="inst-label" id="inst-label">The question</p>
  <div class="inst-body">
    <div class="panel-state is-on" data-for="open">
      <div class="ticks">
        <div class="tick"><span>Invented chart facts</span><b>41%</b></div>
        <div class="tick"><span>AI alone, same cases</span><b>92</b></div>
        <div class="tick"><span>After one sentence</span><b>11%</b></div>
      </div>
      <p class="stat-note">An easy ear infection, ten models, and forty years of literature we don’t bring up at parties. Scroll. This side keeps the measurement.</p>
    </div>
    <div class="panel-state" data-for="case">
      <div class="stat-xl">41% <small>invented a chart fact</small></div>
      {mini_grid}
      <p class="stat-note">Thorough answers invented more. The longest three: 13, 13, 11 of 14.</p>
    </div>
    <div class="panel-state" data-for="human">
      <div class="pair">
        <div class="col machine">
          <h3>Machine</h3>
          <ul>
            <li>Invented facts, 41%</li>
            <li>Completes the chart</li>
            <li>Bias sits in text</li>
            <li>Omits almost never</li>
          </ul>
        </div>
        <div class="col human">
          <h3>Human</h3>
          <ul>
            <li>ROS confirmed, 38.5%</li>
            <li>Recommended care, 55%</li>
            <li>Bias hides in gestalt</li>
            <li>A 26.7-hour day</li>
          </ul>
        </div>
      </div>
      <p class="stat-note">Same error types. Different holes. Only one is currently on trial.</p>
    </div>
    <div class="panel-state" data-for="roots">
      <div class="ticks">
        <div class="tick"><span>Training data</span><b>us</b></div>
        <div class="tick"><span>Post-training</span><b>guessing pays</b></div>
        <div class="tick"><span>Prompting</span><b>the lever</b></div>
      </div>
      <p class="stat-note">Stale dose and inherited bias live in the weights. Completeness lives in the instructions.</p>
    </div>
    <div class="panel-state" data-for="fix">
      <div class="stat-xl">11% <small>after one sentence</small></div>
      <div class="fix-bars">
        <div class="fix-bar before"><span>Bare</span><i></i><b>24/56</b></div>
        <div class="fix-bar after"><span>Asked</span><i></i><b>6/56</b></div>
      </div>
      <p class="stat-note">Fable, the heaviest inventor, was not in this rerun. The dead dose and the age bin did not move.</p>
    </div>
    <div class="panel-state" data-for="combo">
      <div class="score-bars">
        <div class="score-bar is-ai" style="--v:92"><span>AI alone</span><i></i><b>92</b></div>
        <div class="score-bar" style="--v:76"><span>Doctors+AI</span><i></i><b>76</b></div>
        <div class="score-bar" style="--v:74"><span>Doctors</span><i></i><b>74</b></div>
      </div>
      <p class="stat-note">92 is the study team prompting GPT-4, not the chat the physicians had.</p>
    </div>
    <div class="panel-state" data-for="synergy">
      <div class="ticks">
        <div class="tick"><span>Pathologists + tuned assistant</span><b>beats both</b></div>
        <div class="tick"><span>Dermatology, probabilities</span><b>beats both</b></div>
        <div class="tick"><span>Chatbot, no protocol</span><b>no gain</b></div>
      </div>
      <p class="stat-note">Synergy is real and conditional: task, interface, who holds the last word.</p>
    </div>
    <div class="panel-state" data-for="hypothesis">
      <div class="ticks">
        <div class="tick"><span>Prompt the AI to say what it assumed</span><b>AI lever</b></div>
        <div class="tick"><span>Train the doctor to ask</span><b>human lever</b></div>
      </div>
      <p class="stat-note">Nobody has tested both at once in real clinical workflow. This ear infection is pilot data.</p>
    </div>
    <div class="panel-state" data-for="close">
      <p class="q">Say what you’re assuming, and ask about the blanks.</p>
      <p class="stat-note">It works on the machine; I measured it. Whether the two habits together beat either party is the comparison nobody has run.</p>
    </div>
  </div>
</aside>
"""

JS = r"""
(function () {
  const states = document.querySelectorAll(".panel-state");
  const label = document.getElementById("inst-label");
  const bar = document.querySelector(".progress-bar");
  const mmK = document.querySelector(".mm-k");
  const mmV = document.querySelector(".mm-v");
  const names = {
    open: "The question",
    case: "An easy case",
    human: "The human numbers",
    roots: "Three roots",
    fix: "One sentence",
    combo: "Adding a doctor",
    synergy: "When it works",
    hypothesis: "Unrun experiment",
    close: "Four seconds",
  };
  const meter = {
    open: ["the argument", "41 · 92 · 11"],
    case: ["invented", "41%"],
    human: ["two systems", "omit / invent"],
    roots: ["the lever", "prompt"],
    fix: ["after asking", "11%"],
    combo: ["AI alone", "92"],
    synergy: ["designed", "beats both"],
    hypothesis: ["two levers", "untested"],
    close: ["the habit", "4 seconds"],
  };
  let current = "open";
  function show(scene) {
    if (scene === current) return;
    current = scene;
    states.forEach((el) => el.classList.toggle("is-on", el.dataset.for === scene));
    if (label) label.textContent = names[scene] || scene;
    const m = meter[scene] || meter.open;
    if (mmK) mmK.textContent = m[0];
    if (mmV) mmV.textContent = m[1];
  }
  const scenes = [...document.querySelectorAll(".scene")];
  const onScroll = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    const t = max > 0 ? window.scrollY / max : 0;
    if (bar) bar.style.transform = "scaleX(" + t + ")";
    const line = window.innerHeight * 0.28;
    let chosen = scenes[0];
    for (const s of scenes) {
      const r = s.getBoundingClientRect();
      if (r.top <= line) chosen = s;
    }
    if (chosen) show(chosen.dataset.scene);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
})();
"""

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Compared to whom? — Grok 4.6</title>
<style>{CSS}</style>
</head>
<body>
<!--
THESIS: Two fallible systems, measured. Essay left, living instrument right — AI 2027's split, this study's numbers.
OWN-WORLD: Cream paper, Charter, hairline rules, rust=human / blue=machine, tabular ticks, no chrome.
STORY: Reader scrolls a plain argument; the side panel keeps the current measurement in view.
FIRST VIEWPORT: Giant title, opening anecdote, instrument showing 41 / 92 / 11.
FORM: Long-form instrument page.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, and DESIGN.md
-->
<a class="skip" href="#compared-to-whom">Skip to essay</a>
<div class="progress" aria-hidden="true"><span class="progress-bar"></span></div>
<header class="topbar">
  <span class="model">Grok 4.6 edit</span>
  <span>Draft — do not post without review</span>
</header>
<div class="page">
  <article class="essay">
{BODY}
  </article>
{INSTRUMENT}
</div>
<div class="mobile-meter">
  <span class="mm-k">the argument</span>
  <span class="mm-v">41 · 92 · 11</span>
</div>
<script>{JS}</script>
</body>
</html>
"""
OUT.write_text(page, encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
