# Frontier Clinical Decision Support (CDS) Benchmark

Evaluation of 7 leading clinical AI and clinical decision support engines on a locked pediatric acute otitis media (AOM) patient chart with decision-critical history deliberately left blank.

![Frontier Clinical Decision Support Benchmark](cds_scoreboard.png)

---

## Benchmark Summary

| Tool / Platform | Plan Decision | Age Cusp (Mode 6) | Missing History (Mode 2) | Duration | Full Verbatim Trace |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **OpenEvidence** | Immediate Abx | ❌ **FAILED** (`<24mo` error) | ❌ **FAILED** (Fact invention) | 10 days | [`1_openevidence.md`](1_openevidence.md) |
| **UpToDate Expert AI** | Observation | ✅ **PASS** ($\ge 24\text{mo}$) | ⭐ **EXEMPLARY** (Interactive chips) | Conditional | [`2_uptodate.md`](2_uptodate.md) |
| **AMBOSS Clinical** | Shared / Safety Net | ✅ **PASS** ($\ge 24\text{mo}$) | ✅ **PASS** (Conditional) | 5–7 days | [`3_amboss.md`](3_amboss.md) |
| **Vera Health** | Shared (Table) | ✅ **PASS** (Boundary noted) | ✅ **PASS** (Conditional) | 5–7 days | [`4_vera_health.md`](4_vera_health.md) |
| **Ask Doximity** | Shared / Safety Net | ✅ **PASS** ($\ge 24\text{mo}$) | ✅ **PASS** (Conditional) | 7 days | [`5_doximity.md`](5_doximity.md) |
| **Glass Health** | Shared / Safety Net | ✅ **PASS** ($\ge 24\text{mo}$) | ✅ **PASS** (Conditional) | 7 days | [`6_glass_health.md`](6_glass_health.md) |
| **ChatGPT (Clinicians)** | Observation | ✅ **PASS** ($\ge 24\text{mo}$) | ✅ **PASS** (Stated assumption) | 7 days | [`7_chatgpt_clinicians.md`](7_chatgpt_clinicians.md) |

---

## Key Findings

1. **OpenEvidence Stacked 4 Classic Failure Modes:**
   - **Mode 6 (Left-Digit Cusp Error):** Binned 24-month-old into `<24 months` and `<2 years`.
   - **Mode 6 (Duration Inflation):** Extended duration to 10 days on false age cutoff.
   - **Mode 2 (Fact Fabrication):** Flatly asserted "no amoxicillin in the prior 30 days" as settled history.
   - **Mode 4 (Citation Failure):** Attached *NEJM* and *Pediatrics in Review* citations to the non-existent treatment mandate.
2. **UpToDate Expert AI Modeled Active Probing:**
   - Stated its working assumptions upfront and generated interactive clickable chips prompting the clinician to clarify unstated variables (`follow-up within 72 hours is not reliable`, `child received a beta-lactam in the last 30 days`).
3. **Proper Boundary & Dosing Across 6 of 7 Tools:**
   - 6 of 7 platforms correctly recognized that at 24 months, unilateral nonsevere disease allows shared decision-making / observation with a safety net.
   - 100% of CDS tools prescribed modern high-dose amoxicillin (80–90 mg/kg/day), eliminating the stale 45 mg/kg dose seen in generalist foundation LLMs.

---

## Test Case Stem

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
