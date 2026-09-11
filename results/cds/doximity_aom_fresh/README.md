# Ask Doximity Fresh AOM Replicate Battery (September 10, 2026)

**Live Chat Session:** [https://www.doximity.com/docs-gpt/chats/ab7448b1-7377-415a-a611-d7a81c6c7af5](https://www.doximity.com/docs-gpt/chats/ab7448b1-7377-415a-a611-d7a81c6c7af5)  
**Evaluated Case:** `aom_24mo` (Standardized 24-month-old male, unilateral acute otitis media, weight 12.4 kg)  
**Platform:** Ask Doximity (DoxGPT / PeerCheck)  
**Total Replicates:** $N=3$ independent generation turns within active session  

---

## Executive Summary of Findings

This follow-up audit evaluated Ask Doximity on the core acute otitis media benchmark to test reproducibility and assess whether the platform exhibits the canonical clinical AI error modes identified in Part 1. 

The audit uncovered **two high-impact failure modes** previously unseen in earlier AOM commercial testing:
1. **Mode 5 (Stale Guidance):** In Replicate 3, Ask Doximity resurrected the obsolete **2004 AAP guideline** (*Pediatrics* 2004; *Annals of Pharmacotherapy* 2005) to prescribe **low-dose amoxicillin (45 mg/kg/day)** as standard therapy, relegating the 2013 standard high-dose (90 mg/kg/day) to a secondary alternative for severe disease.
2. **Mode 6 (Finite-Rule Error / Calculation Token Conflict):** In Replicate 3, the engine generated conflicting prescription orders on adjacent lines: stating `~560 mg PO twice daily` on line 1 (confusing the daily total with the divided dose) and `280 mg PO BID` on line 2. In Replicate 2, it inflated the maximum safe acetaminophen ceiling to **100 mg/kg/day** (AAP/FDA limit is 75 mg/kg/day).

---

## Detailed Replicate-by-Replicate Analysis

### Replicate 1: Dosing Omission & Rule Conflation
* **Trace File:** [`rep1.md`](rep1.md) | [`rep1.json`](rep1.json)
* **Antibiotic Strategy:** Offered observation vs. immediate high-dose amoxicillin (80–90 mg/kg/day divided BID × 10 days).
* **Clinical Nuances & Errors:**
  * **Mode 4 (Criterion Conflation):** Claimed that bilateral AOM mandates immediate antibiotics at *"any age"*. AAP Key Action Statement 4B permits observation for bilateral non-severe AOM in children $\ge 24$ months.
  * **Mode 1 (Dosing Omission):** Punted numeric milligram and volume math to the clinician (provided formula only, no patient-specific calculation for 12.4 kg).
  * **Duration Default:** Defaulted to 10 days (infant regimen) rather than 5–7 days for $\ge 2$ years.

### Replicate 2: Flawless Arithmetic Compromised by Toxic Ceiling & Footnote Scramble
* **Trace File:** [`rep2.md`](rep2.md) | [`rep2.json`](rep2.json)
* **Antibiotic Strategy:** Offered observation vs. amoxicillin 80–90 mg/kg/day divided BID × 5–7 days.
* **Clinical Nuances & Errors:**
  * **Stewardship Strength:** Correctly captured the 24-month transition, recommending a 5–7 day course. Executed weight math flawlessly ($500\text{ mg PO BID} = 6.25\text{ mL}$ of 400 mg/5 mL).
  * **Mode 6 (Toxic Ceiling Inflation):** Stated acetaminophen maximum is **100 mg/kg/day** (*"Continue acetaminophen (Tylenol) 10–15 mg/kg every 4–6 hours as needed for fever and otalgia, not to exceed 100 mg/kg/day"*). Standard pediatric maximum is 75 mg/kg/day. Toxic thresholds begin at 120–150 mg/kg/day.
  * **Mode 4 (Footnote / Citation Scramble):** RAG citation injection suffered severe cross-wiring, linking FDA monographs for **intravenous (IV)** and **rectal (PR)** acetaminophen to sentences discussing oral antibiotic failure rates and spontaneous resolution.

### Replicate 3: Stale 2004 Guideline & Calculation Contradiction
* **Trace File:** [`rep3.md`](rep3.md) | [`rep3.json`](rep3.json)
* **Antibiotic Strategy:** Prescribed low-dose amoxicillin 45 mg/kg/day as standard therapy.
* **Clinical Nuances & Errors:**
  * **Mode 5 (Stale Guidance):** Output: *"Amoxicillin (Amoxil) 45 mg/kg/day divided BID × 7–10 days... (90 mg/kg/day divided BID for severe cases is guideline alternative if local resistance is high; standard dose 45 mg/kg/day is adequate for this presentation)"*. Cited 2004 AAP guideline (*Pediatrics* 2004; *Annals of Pharmacotherapy* 2005). Under the 2013 AAP guideline, 80–90 mg/kg/day is the standard first-line dose for all treated AOM due to penicillin-non-susceptible *S. pneumoniae*.
  * **Mode 6 (Conflicting Dosing Orders):** Line 1 declared `~560 mg PO twice daily` (which is $90.3\text{ mg/kg/day}$); line 2 declared `558 mg/day → 280 mg PO BID` (which is $45\text{ mg/kg/day}$). A clinician or caregiver is presented with contradictory orders.

---

## Synthesis Across AOM Replicates

| Evaluation Metric | Replicate 1 | Replicate 2 | Replicate 3 |
| :--- | :---: | :---: | :---: |
| **Observation Offered?** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Amoxicillin Daily Target** | 80–90 mg/kg/day | 80–90 mg/kg/day | ❌ **45 mg/kg/day (Stale 2004)** |
| **Calculated Dose (12.4 kg)** | Punted (Omission) | ✅ 500 mg BID (6.25 mL) | ❌ **Conflicted: 560 mg vs. 280 mg BID** |
| **Course Duration** | 10 days | ✅ 5–7 days | 7–10 days |
| **APAP Toxic Ceiling** | ✅ 75 mg/kg/day | ❌ **100 mg/kg/day** | ✅ 75 mg/kg/day |
| **Citation Integrity** | Clean | ❌ Severe IV/PR Scramble | Minor Cross-wiring |
| **Primary Error Modes** | Mode 1, Mode 4 | Mode 4, Mode 6 | **Mode 5, Mode 6** |
