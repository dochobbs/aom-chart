# CDS Benchmark — Suite 2: 18-Month-Old Age Control

Evaluation of 7 leading clinical AI platforms on the 18-month-old pediatric AOM case ([`docs/STEM_18mo.md`](../../../docs/STEM_18mo.md): 18 months, 11.0 kg, unilateral AOM, $T=38.7^\circ\text{C}$).

---

## Comparative Scoreboard: 24 Months vs. 18 Months

| CDS Tool / Engine | 24-Month Duration | 18-Month Duration | 18-Month Preferred Plan | 18-Month Dosing Math (11.0 kg) | Verbatim Trace |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **OpenEvidence** | 10d / 5–7d | **10 days** | **Immediate Treat** | 450–500 mg PO BID (~82–91 mg/kg/day) | [`1_openevidence_18mo.md`](1_openevidence_18mo.md) |
| **UpToDate Expert AI** | Conditional | **10 days** | Shared / 10d delayed | High-dose amoxicillin conditional | [`2_uptodate_18mo.md`](2_uptodate_18mo.md) |
| **AMBOSS Clinical** | 5–7 days | **10 days** | **Immediate Treat** | 80–90 mg/kg/day for 10 days | [`3_amboss_18mo.md`](3_amboss_18mo.md) |
| **Vera Health** | 5–7 days | **10 days** | Either (Table) | 80–90 mg/kg/day | [`4_vera_health_18mo.md`](4_vera_health_18mo.md) |
| **Ask Doximity** | 7 days | **10 days** | Shared / 10d delayed | **Exact:** 6 mL BID of 400 mg/5 mL (87 mg/kg/day) | [`5_doximity_18mo.md`](5_doximity_18mo.md) |
| **Glass Health** | 7 days | **10 days** | Shared / 10d delayed | 80–90 mg/kg/day | [`6_glass_health_18mo.md`](6_glass_health_18mo.md) |
| **ChatGPT (Clinicians)** | 7 days | **10 days** | Shared / 10d delayed | Qualitative 80–90 mg/kg/day (volume refusal) | [`7_chatgpt_clinicians_18mo.md`](7_chatgpt_clinicians_18mo.md) |

---

## Detailed Clinical Findings

1. **100% Duration Shift to 10 Days:**
   Every single CDS platform correctly recognized that dropping age from 24 months to 18 months shifts guideline antibiotic duration to a full **10-day course** (AAP standard for children $<2	ext{ years}$).
2. **Weight Recalibration to 11.0 kg:**
   Tools that calculate specific suspension volumes cleanly updated their math from 12.4 kg (7 mL BID) to 11.0 kg (6 mL BID of 400 mg/5 mL, delivering 480 mg/dose = 87.3 mg/kg/day).
3. **Shift Toward Immediate Treatment in OpenEvidence & AMBOSS:**
   Both OpenEvidence and AMBOSS shifted their primary recommendation to **immediate antibiotic treatment**, citing that age $<2$ years combined with documented fever ($38.7^\circ	ext{C}$) tips the clinical risk-benefit ratio toward treatment.
