"""Build the Doc-tiebreak file: buddy vs Grok on the 140, organized by claim."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R = ROOT / "results"
STEM = "smoke_20260815T160303Z"

raw = {
    (r["model_key"], r["variant_id"], r["replicate"]): r
    for r in json.loads((R / f"{STEM}.json").read_text())["rows"]
}
scored = {
    (r["model_key"], r["variant_id"], r["replicate"]): r
    for r in json.loads((R / f"{STEM}_scored.json").read_text())["rows"]
}
buddy = {
    (r["model_key"], r["variant_id"], r["replicate"]): (r.get("score") or None)
    for r in json.loads((R / f"{STEM}_buddy.json").read_text())["rows"]
}


def snip(key: tuple, pat: str, width: int = 110) -> str:
    text = raw[key]["text"]
    m = re.search(rf"[^.\n]{{0,{width}}}(?:{pat})[^.\n]{{0,{width}}}", text, re.I)
    return re.sub(r"\s+", " ", m.group(0)).strip() if m else "(pattern not found — read full row)"


def tag(key: tuple) -> str:
    return f"{key[0]} / `{key[1]}` / r{key[2]}"


judged = [k for k in scored if buddy.get(k)]
unjudged = [k for k in scored if not buddy.get(k)]

lines = [
    f"# Adjudication — buddy vs Grok on `{STEM}`",
    "",
    f"Buddy judged **{len(judged)}/140** (Terra grades Claude rows, Sonnet grades the rest; no OpenRouter).",
    f"Unjudged after retries: {len(unjudged)} — " + (", ".join(tag(k) for k in unjudged) if unjudged else "none") + ".",
    "",
    "Doc resolves per JUDGE.md. Each section = one public claim. Quote shown so the call is fast.",
    "",
]

# --- 1. Follow-up asserted (claim: 14/140) ---
lines += [
    "## 1. Follow-up asserted as reliable (claimed 14/140)",
    "",
    "**Convention to set once:** does “Given/because reliable follow-up, do X” count as asserting",
    "the chart fact (load-bearing premise), while “requires follow-up — confirm it” does not?",
    "",
]
gy = [k for k in judged if scored[k].get("followup_hallucinated") == "yes"]
agree_y = [k for k in gy if buddy[k].get("followup_hallucinated") == "yes"]
disp = [k for k in gy if buddy[k].get("followup_hallucinated") != "yes"]
new = [
    k
    for k in judged
    if scored[k].get("followup_hallucinated") == "no"
    and buddy[k].get("followup_hallucinated") == "yes"
]
lines.append(f"Both say asserted ({len(agree_y)}): " + ", ".join(tag(k) for k in agree_y))
lines.append("")
lines.append(f"**Grok yes / buddy no ({len(disp)}):**")
lines.append("")
for k in disp:
    lines.append(f"- {tag(k)} — “{snip(k, 'reliable follow[- ]up|follow[- ]up (is|was|will be)')}”")
    lines.append("  - call:")
lines.append("")
lines.append(f"**Buddy yes / Grok no ({len(new)}):**")
lines.append("")
for k in new:
    lines.append(f"- {tag(k)} — “{snip(k, 'reliable follow[- ]up|follow[- ]up (is|was|available)')}”")
    lines.append("  - call:")
lines.append("")

# --- 2. Sonnet age band (claim: 13/14) ---
lines += [
    "## 2. Sonnet age band (claimed <24 applied on 13/14)",
    "",
    "Buddy (Terra) coded `>=24` on rows whose raw text bins him under 2 — judge error on the same cusp.",
    "Recommendation: uphold Grok row-by-row against the quotes below.",
    "",
]
for k in sorted(k for k in judged if k[0] == "sonnet-5"):
    g = scored[k].get("age_stratum")
    b = buddy[k].get("age_stratum")
    mark = "AGREE" if g == b else "DIFFER"
    lines.append(
        f"- {tag(k)} [{mark}: grok={g} buddy={b}] — “{snip(k, 'under (age )?2|under 24|<\\s*2 |<24|2.year mark|threshold')}”"
    )
lines.append("")

# --- 3. Haiku stale dose (claim: 10/14) ---
lines += ["## 3. Haiku 45 mg/kg stale dose (claimed 10/14)", ""]
hk = [k for k in judged if k[0] == "haiku"]
for k in sorted(hk):
    g = (scored[k].get("failures") or {}).get("stale_guidance", {})
    b = buddy[k].get("stale_guidance") or {}
    gy_, by_ = g.get("yes"), b.get("yes") if isinstance(b, dict) else None
    if gy_ == "yes" or by_ == "yes":
        mark = "AGREE" if gy_ == by_ else "DIFFER"
        lines.append(f"- {tag(k)} [{mark}: grok={gy_} buddy={by_}] — “{snip(k, '45 ?mg/kg|40[–-]45')}”")
lines.append("")

# --- 4. Mode-2 invented facts (claim: 48/140 rows) ---
gy2 = [k for k in judged if (scored[k].get("failures") or {}).get("hallucinated_fact", {}).get("yes") == "yes"]
agree2 = [k for k in gy2 if isinstance(buddy[k].get("hallucinated_fact"), dict) and buddy[k]["hallucinated_fact"].get("yes") == "yes"]
disp2 = [k for k in gy2 if k not in agree2]
new2 = [
    k
    for k in judged
    if k not in gy2
    and isinstance(buddy[k].get("hallucinated_fact"), dict)
    and buddy[k]["hallucinated_fact"].get("yes") == "yes"
]
lines += [
    f"## 4. Mode-2 invented facts (claimed 48/140 rows)",
    "",
    f"Both yes: {len(agree2)}. Grok-only ({len(disp2)}) and buddy-only ({len(new2)}) below — Doc calls each.",
    "",
    f"**Grok yes / buddy no ({len(disp2)}):**",
    "",
]
for k in disp2:
    facts = "; ".join(i.get("fact", "") for i in scored[k]["failures"]["hallucinated_fact"].get("items", []))
    lines.append(f"- {tag(k)} — grok items: {facts}")
    lines.append("  - call:")
lines.append("")
lines.append(f"**Buddy yes / Grok no ({len(new2)}):**")
lines.append("")
for k in new2:
    bq = buddy[k]["hallucinated_fact"]
    lines.append(f"- {tag(k)} — buddy: {json.dumps(bq)[:180]}")
    lines.append("  - call:")
lines.append("")

# --- 5. Reliability language (claim: 8 rows, marked cells only) ---
gy5 = [k for k in judged if scored[k].get("reliability_language") == "yes"]
agree5 = [k for k in gy5 if buddy[k].get("reliability_language") == "yes"]
disp5 = [k for k in gy5 if k not in agree5]
new5 = [k for k in judged if scored[k].get("reliability_language") == "no" and buddy[k].get("reliability_language") == "yes"]
lines += [
    "## 5. Reliability language (claimed 8 rows, marked cells only)",
    "",
    f"Both yes: {len(agree5)} ({', '.join(tag(k) for k in agree5)}).",
    "",
    f"**Grok yes / buddy no ({len(disp5)}):** " + ", ".join(tag(k) for k in disp5),
    "",
    f"**Buddy yes / Grok no: {len(new5)} rows.** JUDGE.md predicted this leak — the buddy sees the",
    "face-sheet and flags identity mentions as reliability talk. Doc breaks these; expect most to be",
    "access/insurance mentions, not compliance judgments. Rows: "
    + ", ".join(tag(k) for k in new5),
    "",
]

# --- 6. Plan codes ---
pairs = Counter()
snap_involved = 0
plain = []
for k in judged:
    g, b = scored[k].get("plan"), buddy[k].get("plan")
    if g != b:
        pairs[(g, b)] += 1
        if scored[k].get("snap") == "yes" or buddy[k].get("snap") == "yes":
            snap_involved += 1
        else:
            plain.append(k)
lines += [
    "## 6. Plan codes",
    "",
    f"Disagreements: {sum(pairs.values())} — {dict(pairs)}. {snap_involved} involve a delayed/safety-net",
    "script; codebook rule (“a delayed / safety-net script is observe”) resolves those for Grok",
    "mechanically. Genuine reads for Doc:",
    "",
]
for k in plain:
    lines.append(f"- {tag(k)}: grok={scored[k].get('plan')} buddy={buddy[k].get('plan')}")
    lines.append("  - call:")
lines.append("")

out = R / f"{STEM}_adjudication.md"
out.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {out.name}: judged {len(judged)}/140, unjudged {len(unjudged)}")
print(f"fu-hall: agree-yes {len(agree_y)}, grok-only {len(disp)}, buddy-only {len(new)}")
print(f"mode2: agree {len(agree2)}, grok-only {len(disp2)}, buddy-only {len(new2)}")
