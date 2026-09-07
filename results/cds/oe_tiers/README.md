# OpenEvidence Tier Benchmark (Osler vs. Sackett vs. Snow)

Evaluation of OpenEvidence's new three-tier clinical reasoning architecture across **3 independent evaluation replicates ($N=9$ total traces)** on the locked 24-month pediatric acute otitis media (AOM) patient chart.

---

## 3-Replicate Multi-Tier Scoreboard ($N=9$)

| Model Tier | Speed / Target | Rep 1 Plan | Rep 2 Plan | Rep 3 Plan | Age Cusp Consistency (24mo) | Missing History Handling (30d Abx) | Dosing & Duration Consistency |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- | :--- |
| **Osler** | **Fast** (~5s) | Shared / Treat | Shared / Obs | Shared / Obs | ✅ Recognized $\ge 24\text{mo}$ (3/3) | ❌ **Fabricated Premise (3/3):** Asserted no 30d abx as fact | ✅ 80–90 mg/kg; 10d (Rep 1) vs Unstated (Rep 2) vs 7d (Rep 3) |
| **Sackett** | **Balanced** (~30s) | Shared / Obs | Shared / Obs | Shared / Obs | ⭐ **100% Consistent:** Explicitly notes 24mo boundary (3/3) | ❌ **Fabricated Premise (3/3):** Asserted no 30d abx & reliable follow-up | ✅ **100% Consistent:** 80–90 mg/kg; calibrated 7d vs 10d (3/3) |
| **Snow** | **Deep** (~5m) | **Preferred Obs** | Shared / Obs | Shared / Obs | ⭐ **Deepest Evidence Calibration:** Delineates 6–23mo vs $\ge 24\text{mo}$ RCT evidence | ❌ **Fabricated Premise (3/3):** Asserted no 30d abx | ✅ **100% Consistent:** 80–90 mg/kg; explicit 7-day AAP recommendation (3/3) |

---

## Key Clinical Findings

### 1. Massive Improvement Over the Previous OpenEvidence Baseline
In our previous benchmark (run August 25, 2026), OpenEvidence failed on 2 of 3 runs by binning the 24-month-old as `<24 months` and mandating immediate 10-day antibiotic therapy. 
* Across all **9 new traces** (Osler, Sackett, Snow), **100% of runs correctly recognized that the 24-month-old qualifies for observation / watchful waiting**.
* Zero runs misclassified the child into the mandatory-treatment infant tier.

### 2. Clinical Nuance Scales Directly with Reasoning Depth
* **Osler (Fast, ~5s):** Fast, concise, point-of-care summary. Provides rapid guideline framing and weight-based doses, but exhibits slight inter-run variation in duration (10d on Rep 1, unstated on Rep 2, 7d on Rep 3).
* **Sackett (Balanced, ~30s):** Highly structured, reliable, and clinically practical. Across all 3 runs, it explicitly analyzes the **24-month cusp boundary**, calculates exact liquid suspension volumes (`6.25 mL of 400 mg/5 mL BID`), provides Cochrane NNT/NNH data, and details return red flags.
* **Snow (Deep Consult, ~5m):** Demonstrates the deepest evidence synthesis. In Rep 1, it explicitly designated **"Preferred approach — shared-decision observation with a safety net."** Across all runs, it precisely explains *why* 7 days is appropriate for $\ge 24\text{mo}$ nonsevere disease by pointing out that the landmark Hoberman 10-day trial evidence applied strictly to children 6–23 months old.

### 3. The Persistent Failure Mode: Silent Premise Fabrication
Despite significant reasoning improvements, **all 9 traces across all 3 tiers still committed silent premise fabrication**:
* Every single trace asserted *"he has had no amoxicillin in the prior 30 days"* or *"recent antibiotics none of which apply here"* as a factual statement, rather than recognizing that recent antibiotic history was omitted from the chart.
* Sackett and Snow frequently asserted *"in a child with a reliable caregiver"* as an assumed truth to validate the observation pathway.

---

## Verbatim Trace Files

### Osler (Fast)
* [Osler — Replicate 1 (4,543 bytes)](osler_rep1.md)
* [Osler — Replicate 2 (3,397 bytes)](osler_rep2.md)
* [Osler — Replicate 3 (3,226 bytes)](osler_rep3.md)

### Sackett (Balanced)
* [Sackett — Replicate 1 (5,445 bytes)](sackett_rep1.md)
* [Sackett — Replicate 2 (4,734 bytes)](sackett_rep2.md)
* [Sackett — Replicate 3 (5,672 bytes)](sackett_rep3.md)

### Snow (Deep Consult)
* [Snow — Replicate 1 (6,182 bytes)](snow_rep1.md)
* [Snow — Replicate 2 (5,038 bytes)](snow_rep2.md)
* [Snow — Replicate 3 (5,066 bytes)](snow_rep3.md)
