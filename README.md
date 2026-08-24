# They completed the chart

Ten frontier AI models, one synthetic pediatric ear-infection chart with decision-critical facts deliberately left blank. 41% of answers invented the missing facts rather than ask. Identity never changed the prescription — it changed the justifications and defaults. One added prompt sentence cut fact fabrication by three-quarters.

Built by Michael Hobbs, MD; every disputed judgment is anchored to a verbatim quote a human can check. Synthetic case, no PHI.

## Start here

| You want | Resource |
|---|---|
| **Clean Open Datasets (CSV)** | [`data/`](data/) (`main_140_traces.csv`, `identity_contrasts.csv`, `prompt_mitigation.csv`) |
| **Data Dictionary & Error Codebook** | [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md) |
| **Reproduction Notebook** | [`notebooks/reproduce_findings.ipynb`](notebooks/reproduce_findings.ipynb) |
| **Full Technical Findings** | [`FINDINGS.md`](FINDINGS.md) |
| **The Locked Patient Chart** | [`docs/STEM.md`](docs/STEM.md) |
| **Final Adjudication & Tiebreak Log** | [`results/smoke_20260815T160303Z_tiebreak.md`](results/smoke_20260815T160303Z_tiebreak.md) |
| **Plain-Language Summary (Team)** | [`share/team_summary.md`](share/team_summary.md) |
| **What Ran, in Order** | [`docs/RUNS.md`](docs/RUNS.md) |

## Headline numbers (final, tiebroken)

| Measured Finding | Adjudicated Count | Rate / Context |
|---|:---:|---|
| **Answers asserting ≥1 unstated chart fact** | **57 / 140** | **40.7%** (Mode 2) |
| "Reliable follow-up is available," asserted as fact | 11 / 140 | 7 of 10 frontier models |
| Claude Fable 5: "no antibiotics in past 30 days," stated flat | 13 / 14 | 92.9% (load-bearing premise) |
| Claude Haiku: amoxicillin 45 mg/kg (superseded ~2004) | 10 / 14 | 71.4% (Mode 5 stale guidance) |
| Claude Sonnet 5: stated 24-month-old binned as "under 2" | 12 / 14 | 85.7% (Mode 6 left-digit cusp error) |
| Real AAP guideline cited for non-existent mandate | 11 / 140 | 7.9% (Mode 4 citation failure) |
| Prescriptions changed by race, name, insurance, or job | 0 / 228 | 0.0% (pre-registered null held) |
| Identity shifted justifications and default paths | 2 findings | Fable nurse 6/6; Flash private default 5/6 |
| Must-not-miss clinical basics omitted | 3 / 140 | 2.1% (Mode 1 omission) |
| **Ask-don't-assume prompt constraint: invention rate** | **24/56 → 6/56** | **43% → 11%** (Opus & Haiku to 0%) |

*Do not average treat-rates across models — plan choice is a property of the model rather than the chart ([`FINDINGS.md`](FINDINGS.md)).*

## Directory layout

```text
├── data/            Exported, analysis-ready CSVs (140 main traces, identity contrasts, prompt mitigation)
├── docs/            The locked case (STEM.md), DATA_DICTIONARY.md, codebooks, judge protocols, run ledger
├── eval/            Runner (run.py), judge (judge.py), CSV exporter (export_csvs.py), models, tests
├── notebooks/       Jupyter reproduction notebook (reproduce_findings.ipynb)
├── results/         Every raw JSON trace, scored file, and human adjudication log (results/README.md)
├── share/           Team summary, one-pager, slide deck, and presentation materials
├── prototypes/      Interactive HTML/CSS web preview prototypes
├── site/            HTML renders of the documentation set (rebuild: python eval/build_site.py)
└── archive/         Superseded working docs and pre-registration trail
```

Markdown is the source of truth; `site/` is generated from it.

## Reproduce & verify

### 1. Interactive Jupyter Notebook
Run the standalone reproduction notebook to verify all statistics, tables, and figures from scratch:
```bash
jupyter notebook notebooks/reproduce_findings.ipynb
```

### 2. Export & Audit CSV Datasets
Re-generate and audit all analysis CSVs from raw JSON results:
```bash
python3 eval/export_csvs.py
```

### 3. Run Test Suite
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r eval/requirements.txt
python3 -m pytest eval/tests/ -q
```

### 4. Re-run Synthetic Model Generations
```bash
# Dry-run prompt assembly
python3 eval/run.py --dry-run

# Live calls (requires vendor API keys in environment)
python3 eval/run.py --smoke --n 1 --model terra --cells control
```

*Second stem (18 months): [`docs/STEM_18mo.md`](docs/STEM_18mo.md) — do not pool with 24-month rows.*

Michael Hobbs, MD — [michael@hobbs.md](mailto:michael@hobbs.md)
