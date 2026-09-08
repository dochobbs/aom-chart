# Traces

Every live run. Start with the findings file, then open the matching `.md` for full text.

| Run | Packet | What | n | Where to start |
|---|---|---|---:|---|
| `smoke_20260815T160303Z` | v3, 24 mo | 7 cells × 10 models. Main catalog. | 2 | [`_findings.md`](smoke_20260815T160303Z_findings.md) · [`_scored.json`](smoke_20260815T160303Z_scored.json) · [`_adjudication.md`](smoke_20260815T160303Z_adjudication.md) · [`_tiebreak.md`](smoke_20260815T160303Z_tiebreak.md) · [raw](smoke_20260815T160303Z.md) |
| `smoke_20260815T170727Z` | v4, 18 mo | Second stem. Do not pool with 24 mo. | 1 | [`_notes.md`](smoke_20260815T170727Z_notes.md) |
| `smoke_20260815T181825Z` | v5 | Turn 2 smoke | 1 | [`_notes.md`](smoke_20260815T181825Z_notes.md) |
| `smoke_20260815T184406Z` | v5 | Washington vs Whitaker | 6 | [`_notes.md`](smoke_20260815T184406Z_notes.md) |
| `smoke_20260815T185357Z` | v5 | Medicaid vs private | 6 | [`_notes.md`](smoke_20260815T185357Z_notes.md) |
| `smoke_20260815T190148Z` | v5 | Black vs White | 6 | [`_notes.md`](smoke_20260815T190148Z_notes.md) |
| `smoke_20260815T192236Z` | v5 | Unemployed vs nurse | 6 | [`_notes.md`](smoke_20260815T192236Z_notes.md) |
| `smoke_20260815T214424Z` | v5 | Job pair, second model set (terra/opus/haiku) | 6 | [`_notes.md`](smoke_20260815T214424Z_notes.md) |
| `smoke_20260815T214553Z` | v5 | Mitigation smoke (ask-don't-assume sentence) | 2 | [`_notes.md`](smoke_20260815T214553Z_notes.md) |

Turn-2 tabulation across the four identity runs: [`turn2_summary.md`](turn2_summary.md).

Early instrument smokes (`135828Z`, `141420Z`) used a stem that still said “no antibiotics in the past month.” Do not count those as inventions.

Each run has `.json` (machine) and `.md` (full model text). Control-only collage: [`worst_answer_collage.md`](worst_answer_collage.md).

## September 2026 Replication & Validation Batteries

The baseline run above established the August 15 foundational dataset (`FINDINGS.md`). The September batteries evaluate replication depth, cross-condition transfer, prompt component ablations, and commercial CDS tools:

| Battery | Directory | What | n | Key Files |
|---|---|---|---:|---|
| **Brake + Branching Validation** | [`brake_branching_validation/`](brake_branching_validation/) | 4-experiment battery: head trauma depth (N=40), AOM transfer (N=20), specificity/witnessed fall (N=12), cross-lab OpenAI/Google (N=20). Contains the Sonnet 5 8/10 relapse traces. | 92 | [`REPORT.md`](brake_branching_validation/BRAKE_BRANCHING_VALIDATION_REPORT.md) · [`92traces_master.json`](brake_branching_validation/brake_branching_92traces_master.json) · [`sonnet5_10reps.json`](brake_branching_validation/sonnet5_compound_10reps.json) |
| **2³ Factorial Prompt Ablation** | [`factorial_2cubed_ablation/`](factorial_2cubed_ablation/) | Systematic 8-cell factorial ablation of the three prompt components (Brake, Branching, Anchor) across models. Formed Table 1 of Part 2. | 72 | [`REPORT.md`](factorial_2cubed_ablation/FACTORIAL_2CUBED_AUDIT_REPORT.md) · [`72traces_master.json`](factorial_2cubed_ablation/factorial_2cubed_72traces_master.json) |
| **All-5 Clinical Cases Cure** | [`all5_cases_claude_cure/`](all5_cases_claude_cure/) | Cross-condition transfer across all five locked clinical stems (AOM, Head Trauma, Bronchiolitis, CAP, Febrile Infant). | 20 | [`all5_cases_results.json`](all5_cases_claude_cure/all5_cases_results.json) |
| **Commercial CDS Evaluations** | [`cds/`](cds/) | Baseline performance of specialized clinical tools (OpenEvidence, UpToDate, AMBOSS, Vera Health, Doximity, Glass Health) on empty-box clinical charts. | 16+ | [`cds/README.md`](cds/README.md) · [`cds/18mo/`](cds/18mo/README.md) |
