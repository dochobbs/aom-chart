# They completed the chart

Ten frontier AI models, one synthetic pediatric ear-infection chart with the decision-critical facts deliberately left blank. 41% of answers invented the missing facts rather than ask. Identity never changed the prescription — it changed the justifications and defaults. One added prompt sentence cut the inventing by three-quarters.

Built by Michael Hobbs, MD directing Claude; every disputed judgment is anchored to a quote a human can check. Synthetic case, no PHI.

## Start here

| You want | Read |
|---|---|
| Plain-language summary (team) | [`share/team_summary.md`](share/team_summary.md) |
| Full technical writeup | [`FINDINGS.md`](FINDINGS.md) |
| The exact chart models saw | [`docs/STEM.md`](docs/STEM.md) |
| Final adjudicated numbers | [`results/smoke_20260815T160303Z_tiebreak.md`](results/smoke_20260815T160303Z_tiebreak.md) |
| What ran, in order | [`docs/RUNS.md`](docs/RUNS.md) |

## Headline numbers (final, tiebroken)

| Finding | Count |
|---|---|
| Answers with ≥1 invented chart fact | **57/140 (41%)** |
| "Reliable follow-up is available," asserted | 11/140, 7 of 10 models |
| Fable: "no amox in past 30 days," stated flat | 13/14 |
| Haiku: dead 45 mg/kg amoxicillin dose | 10/14 |
| Sonnet: stated 24-month-old binned "under 2" | 12/14 |
| Identity changed the prescription | Never (2 pre-registered nulls) |
| Identity changed the justification/default | Fable×nurse 6/6; Flash×insurance 5/6 vs 1/6 |
| Ask-don't-assume sentence: invention rows | 24/56 → **6/56**, plans intact |

Do not average treat-rates across models — plan choice is a property of the model, not the chart (`FINDINGS.md`).

## Layout

```
FINDINGS.md      full writeup + data map
docs/            the chart (STEM.md), codebook, judge/turn-2 protocols, run ledger, changelog
eval/            run.py, judge.py, scorers, models.json, variants.json, tests
results/         every trace, score file, notes, adjudication + tiebreak   → results/README.md
share/           team summary, LinkedIn drafts, one-pager, talk
archive/         superseded working docs (pre-registration trail)
```

## Reproduce

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r eval/requirements.txt
python -m pytest eval/tests/ -q
python eval/run.py --dry-run
# live calls need vendor keys in the environment
python eval/run.py --smoke --n 1 --model terra --cells control
```

Second stem (18 months): `docs/STEM_18mo.md` — do not pool with 24-month rows.

Michael Hobbs, MD — [michael@hobbs.md](mailto:michael@hobbs.md)
