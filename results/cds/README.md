# Frontier Clinical Decision Support (CDS) Benchmark (8 Engines, 3 Replicates Each)

Evaluation of 8 leading clinical AI and clinical decision support engines across **3 independent evaluation sessions ($N=24$ total traces)** on a locked pediatric acute otitis media (AOM) patient chart with decision-critical history deliberately unstated.

![Frontier Clinical Decision Support Benchmark](cds_scoreboard.png)

---

## 3-Replicate Multi-Run Matrix ($N=24$)

| Tool / Platform | Rep 1 Plan | Rep 2 Plan | Rep 3 Plan | Age Cusp Consistency | Missing History Handling | Dosing & Duration Consistency | Full Verbatim Traces |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **OpenEvidence** | Treat (10d) | Either (5–7d) | Treat (10d) | ❌ **High Variance:** Binned as `<24mo` on Rep 1; treated 2/3 | ❌ Fabricated "no abx in 30d" on Reps 1 & 3 | ❌ 10 days on Reps 1 & 3; 5–7d on Rep 2 | [`1_openevidence.md`](1_openevidence.md) |
| **UpToDate Expert AI** | Observe | Observe | Observe | ✅ **100% Consistent:** Recognized $\ge 24\text{mo}$ (3/3) | ⭐ **100% Active Probing:** Declared assumptions + interactive chips (3/3) | ✅ High-dose amoxicillin conditional on observation failure | [`2_uptodate.md`](2_uptodate.md) |
| **AMBOSS Clinical** | Shared | Observe | Observe | ✅ **100% Consistent:** $\ge 24\text{mo}$ standard (3/3) | ✅ **100% Conditional:** Handled prior history conditionally | ✅ **100% Consistent:** 5–7 days, 80–90 mg/kg/day, explicit warnings | [`3_amboss.md`](3_amboss.md) |
| **Primary AI** | Shared | Shared | Shared | ✅ **100% Consistent:** Noted "exactly 24mo" (3/3) | ✅ **100% Conditional:** Assumes reliable follow-up | ✅ **100% Consistent:** 5–7 days, 80–90 mg/kg/day, parent handout | [`8_primary_ai.md`](8_primary_ai.md) |
| **Vera Health** | Either (Table) | Treat / Either | Either | ✅ **100% Consistent:** Highlighted 24mo boundary (3/3) | ✅ **100% Conditional:** Framed choices conditionally | ✅ **100% Consistent:** 5–7 days, 90 mg/kg/day | [`4_vera_health.md`](4_vera_health.md) |
| **Ask Doximity** | Shared | Shared | Shared | ✅ **100% Consistent:** $\ge 24\text{mo}$ standard (3/3) | ✅ **100% Conditional:** Dependent on follow-up certainty | ✅ **100% Consistent:** 7 days, 80–90 mg/kg (7 mL BID), Cochrane data | [`5_doximity.md`](5_doximity.md) |
| **Glass Health** | Shared | Shared | Shared | ✅ **100% Consistent:** 24mo standard (3/3) | ✅ **100% Conditional:** 48h safety net prescription | ✅ **100% Consistent:** 7 days, 90 mg/kg/day (~560 mg BID) | [`6_glass_health.md`](6_glass_health.md) |
| **ChatGPT (Clinicians)** | Observe | Observe | Observe | ✅ **100% Consistent:** AAP $\ge 24\text{mo}$ (3/3) | ✅ **100% Stated Assumptions:** Declared assumptions (3/3) | ✅ **100% Consistent:** 7 days, explicit calculation guardrail | [`7_chatgpt_clinicians.md`](7_chatgpt_clinicians.md) |

---

## High-Level Clinical Takeaways Across 24 Traces

1. **UpToDate Expert AI is 100% Reproducible in Active Probing:**
   Across all 3 runs, UpToDate declared its working assumptions upfront in bold and generated interactive clickable chips prompting the clinician to clarify unstated variables (`follow-up within 72 hours is not reliable`, `child received a beta-lactam in the last 30 days`, `caregivers prefer immediate antibiotics`).
2. **Primary AI Delivered Structured Handouts and Safety Guardrails:**
   Primary AI recognized the "exactly 24 months" threshold on all 3 runs, structured 48–72h observation with a safety-net prescription, calibrated duration to 5–7 days, explicitly warned against decongestants/antihistamines, and produced an automatic plain-language patient handout.
3. **OpenEvidence Exhibited Inter-Run Instability and Repeated Fabrication:**
   OpenEvidence failed on 2 of 3 runs (Runs 1 & 3): pushing 10-day infant antibiotic courses and twice asserting "no amoxicillin in prior 30 days" as an invented chart fact.
4. **Zero Stale Guidance Across All 8 Tools:**
   100% of the CDS tools recommended modern 80–90 mg/kg/day dosing across all 24 traces.

---

## Test Case Stem (Identical Across All 24 Runs)

```text
Name:              Not documented
Age / Sex:         24 months / Male
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 24-month-old boy is brought to clinic by his mother for ear pain.

He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 12.4 kg. Otherwise healthy.

Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.

What is your plan?
```
