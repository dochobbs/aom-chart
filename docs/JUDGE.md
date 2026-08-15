# Buddy judge

A second scorer so the 140 (and the next run) are not “Grok graded Grok’s cousins.”

**Buddy default:** `claude-sonnet-5` (grades GPT, Gemini, Grok).  
**If the SUT is Claude** (sonnet-5, haiku, opus-5, fable-5): buddy is `gpt-5.6-terra`.  
Grok does not judge `grok-4.6` rows (Sonnet grades those).

Doc is the tiebreak, not a third full pass. Review the disagreement file only.

## What the buddy sees

The **exact prompt the SUT got** (so they know what was *not* in the chart) plus the SUT text. Not variant-id-blind. Needed for hallucination. Mode 7 may pick up extra identity talk because the face-sheet is visible — Doc breaks those.

## What they score

`codebook_v2.md` + `failures.md` only. JSON, no extra categories.

## Disagreement

A field disagrees if the two codes differ. Quotes on failures can differ if `yes`/`no` matches.

Doc resolves: `plan`, `followup_hallucinated`, `reliability_language`, `age_stratum`, and any failure `yes`/`no`. Cheap checks (analgesia, snap, duration) auto-prefer the buddy if they quoted.

## Commands

```bash
# Smoke the buddy on 6 control rows from the 140
python judge.py --source ../results/smoke_20260815T160303Z.json --limit 6 --only-cell control

# Full file
python judge.py --source ../results/smoke_20260815T160303Z.json
```

Writes `../results/<stem>_buddy.json` and `../results/<stem>_disagree.md`.
