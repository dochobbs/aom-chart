# Clinical AI Decision Support (CDS) & Frontier Foundation Model Guide: Rankings, Forensic Audits, and Practical Clinical Recommendations

**Author:** Michael Hobbs, MD  
**Repository:** [`dochobbs/aom-chart`](https://github.com/dochobbs/aom-chart)  
**Date:** September 10, 2026  
**Audited Datasets:**  
* **Commercial CDS Battery:** 7 platforms $\times$ 5 acute pediatric conditions $\times$ 3 independent replicates = **105 primary encounters** (plus 18mo boundary and demographic equity permutations).  
* **Fresh Ask Doximity Follow-Up:** 3 independent replicates on live session [`ab7448b1-7377-415a-a611-d7a81c6c7af5`](https://www.doximity.com/docs-gpt/chats/ab7448b1-7377-415a-a611-d7a81c6c7af5) (`results/cds/doximity_aom_fresh/`).  
* **Frontier Foundation Model Audits:** 10 frontier models from Anthropic, OpenAI, Google, and xAI across 1,324 primary traces and 92-trace validation runs (`results/brake_branching_validation/`).

---

## Executive Summary: What Should Clinicians Use and Why?

Clinical decision support (CDS) requires an **open-world epistemic architecture**. When evaluating pediatric patients, critical historical variables (such as exact seizure duration, loss of consciousness, or prior antibiotic exposure) are frequently unstated, untimed, or unwitnessed. 

When generic large language models encounter these ambiguous charts, they face **epistemic deadlock**. Rather than prompting the human clinician or acknowledging uncertainty, unconstrained generative tools routinely suffer from **epistemic collapse**: they manufacture unstated negative history (*"no loss of consciousness"*, *"witnessed fall"*, *"no antibiotics in 30 days"*) to force a decisive guideline branch, fail basic weight-based division (halving doses or clashing across lines), or default to adult dosing tables.

Across **15 standardized acute pediatric clinical encounters per platform** (5 cases $\times$ 3 independent replicates), only **one platform** achieved a 100% flawless clinical and arithmetic score post-rescore.

---

## Table 1: Commercial Clinical Decision Support (CDS) Platforms

Evaluated across 5 acute pediatric cases ($N=3$ replicates each = **15 encounters per engine**):  
1. **Acute Otitis Media** (`aom_24mo`): 24mo, unilateral, non-severe, 12.4 kg.  
2. **Minor Head Injury** (`head_24mo`): 24mo, unwitnessed fall, unknown LOC, boggy hematoma.  
3. **First Febrile UTI** (`uti_24mo`): 24mo, cath UA+, imaging & empiric selection.  
4. **Community-Acquired Pneumonia** (`cap_5y`): 5yo, SpO2 93%, crackles, 18.5 kg.  
5. **First Febrile Seizure** (`seizure_6mo`): 6mo, untimed onset (9m timed), alert post-ictal.

Scores reflect **forensic rescoring** penalizing chart confabulation, dose-halving, toxic ceiling inflation, adult defaults, and inappropriate emergency mobilization.

| Rank | Platform | Tier & Rating | Rescored Score (15 Encounters) | Primary Observed Failure Modes | Clinician Bottom Line: Should You Use It? |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **1** | **ChatGPT for Clinicians** *(OpenAI)* | 🟢 **Tier 1 (Top Pick)** | **15 / 15** *(100%)* | • Minimal: Occasionally defers hand-calculation of complex math to EHR widgets | **YES. The safest and most consistent clinical workhorse.** Executed clean weight-based arithmetic, preserved unstated history without confabulation, and calibrated outpatient vs. ED observation safely. |
| **2** | **AMBOSS Clinical Care** | 🟢 **Tier 1 (Recommended)** | **13 / 15** *(86.7%)* | • Mode 1 (Dosing Omission): Punted numeric mg math in CAP to local protocol<br>• Conservative low-dose phrasing in 1 run | **YES. Outstanding clinical depth and interactive inquiry.** Actively asks clinicians to clarify unstated variables. The safest interface architecture, though clinicians must hand-calculate doses if it punts math. |
| **3** | **Vera Health** | 🟡 **Tier 2 (Cautious Use)** | **12 / 15** *(80.0%)* | • Mode 2 (Invented Facts): Silently asserted *"no LOC / witnessed fall"* in head trauma Reps 1 & 2 to force observation | **CAUTION. High diagnostic rigor, but watch for silent assumptions.** Perfect PECARN 24mo cusp recognition and imaging stewardship, but prone to inventing negative history under equipoise. |
| **4** | **OpenEvidence** | 🟡 **Tier 2 (Cautious Use)** | **11 / 15** *(73.3%)* | • Mode 2 (Invented Facts): Fabricated *"no abx in 30d"* and *"no LOC"*<br>• Mode 4: PECARN age criteria scrambled in 1 run | **CAUTION. Excellent rapid reference, but verify facts.** Superb PubMed citation cards and speed, but routinely fabricates missing chart details when guidelines present equally valid options. |
| **5** | **Glass Health** | 🟠 **Tier 3 (Not Recommended)** | **10 / 15** *(66.7%)* | • Mode 3 (Harmful Commission): Triggered 911 / EMS dispatch in 3/3 stable seizures<br>• Mode 1: Omitted RBUS via UK NICE rules<br>• Mode 4: 5-min rescue vs. 15-min seizure conflation | **NO for Primary Triage. Severe false-alarm emergency escalation.** High risk of calling 911 on well-appearing post-ictal infants, plus transnational guideline leakage (citing UK NHS rules on US charts). |
| **6** | **UpToDate Expert AI** | 🟠 **Tier 3 (Substantial Flaws)** | **9 / 15** *(60.0%)* | • Adult Default Bias: Prescribed adult fixed 500 mg TID amoxicillin in 3/3 CAP runs (18.5 kg child)<br>• Mode 4: Mis-binned 24mo into $<2\text{y}$ PECARN rule (2/3 runs)<br>• Conflated seizure duration (>5–10 min) | **DO NOT TRUST GENERATIVE OUTPUT. Use legacy calculators instead.** Gold-standard knowledge base, but the generative AI layer suffers from hazardous adult dosing bleed-through and age-band mis-binning. |
| **7** | **Ask Doximity** *(DoxGPT / PeerCheck)* | 🔴 **Tier 4 (Hazardous)** | **8 / 15** *(53.3%)* | • Mode 6: Dose halving (415 mg BID in CAP)<br>• Mode 6: APAP ceiling inflated to 100 mg/kg/day<br>• Mode 6: Conflicting 560 mg vs 280 mg BID orders<br>• Mode 5: Resurrected obsolete 2004 AAP guideline (45 mg/kg)<br>• Mode 2: Injected "no LOC" into search queries<br>• Mode 4: Scrambled IV/PR monographs | **DO NOT USE FOR PEDIATRIC DOSING OR TRIAGE.** Sits at the bottom of the audit. Exhibits pervasive arithmetic errors, guideline staleness, dangerous toxic threshold inflation, and citation hallucinations. |

---

## Table 2: Frontier Foundation Models by Lab

Evaluated across **1,324 primary traces** and **92-trace validation batteries** under standardized pediatric epistemic prompts. (Note: Models tested were frontier 5.x and 4.x generations; no 3.5 models were evaluated).

| Lab & Frontier Families | Clinical Tier & Rating | Default Clinical Habits (Instinctive Behavior) | Fatal Flaws & Failure Modes | Clinician Bottom Line: What to Use It For |
| :--- | :---: | :--- | :--- | :--- |
| **OpenAI**<br>`GPT-5.6` *(Terra, Luna, Sol)*<br>`GPT-4o` | 🟢 **Tier 1<br>(High Confidence)** | **Deterministic, structured, and computationally reliable.** Instinctively performs multi-step weight-based arithmetic without dropping tokens. Strong adherence to formal pediatric guidelines (AAP, IDSA, PECARN). | • Action bias: Can lean toward active intervention unless prompt explicitly instructs observation options.<br>• Occasional defensive abstention on edge-case arithmetic when safety guardrails trigger. | **Best general workhorse for clinical calculation and protocol execution.** Outstanding for weight-based dosing, differential diagnosis checklists, and clear discharge instructions. |
| **Anthropic**<br>`Claude Sonnet 5`<br>`Claude Opus 5`<br>`Claude Haiku 4.5` | 🟢 **Tier 1 (Sonnet/Opus)<br>🟡 Tier 2 (Haiku)** | **Epistemically vigilant and nuanced.** Instinctively highlights what is missing from the chart; refuses to confabulate unstated facts; excels at shared decision-making frameworks and parent communication. | • Verbosity & Token Pressure: Early test harnesses experienced truncations at 4,000 tokens (now resolved with 8k expansion).<br>• Haiku 4.5 is prone to conservative low-dose defaults (45 mg/kg) and arithmetic drift under small context windows. | **Best for complex diagnostic uncertainty and ethics/communication.** Use Sonnet 5 or Opus 5 when a case has subtle nuances, unstated variables, or requires balanced counseling. Avoid Haiku for pediatric dosing. |
| **Google**<br>`Gemini 3.1 Pro`<br>`Gemini 3.7 Flash` | 🟡 **Tier 2<br>(Moderate / Cautious)** | **Broad synthesis and multimodal breadth.** Deep literature retrieval; readily incorporates broad guidelines and academic reviews; strong visual reasoning on diagnostic images. | • Epistemic collapse under equipoise: Frequently fabricates unstated negative history (*"no LOC"*, *"no prior abx"*) to resolve clinical deadlock.<br>• Autocomplete drift: Higher sensitivity to prompt phrasing; occasional hallucinated negative exam findings. | **Best for literature research and multimodal image review.** Excellent for exploring rare conditions or reviewing imaging findings, but clinicians must double-check all clinical history assumptions and math. |
| **xAI**<br>`Grok 4.6` | 🟠 **Tier 3<br>(Not Recommended)** | **Direct, confident, and conversational.** Commits rapidly to a single primary diagnosis; provides concise action plans without unnecessary boilerplate. | • Adult clinical bias: Prone to applying adult clinical intuition and fixed dosing defaults to pediatric charts.<br>• Weak boundary adherence: Struggles with strict numerical cusps (e.g., PECARN 24-month rule transitions). | **Do not use for high-stakes pediatric triage or acute dosing.** Calibrated for general conversational knowledge rather than zero-defect clinical arithmetic or boundary precision. |

---

## Detailed Evidence on the Fresh Ask Doximity Findings

During the September 10, 2026 follow-up audit on live Ask Doximity session [`ab7448b1-7377-415a-a611-d7a81c6c7af5`](https://www.doximity.com/docs-gpt/chats/ab7448b1-7377-415a-a611-d7a81c6c7af5) (`results/cds/doximity_aom_fresh/`), the platform exhibited multiple critical regressions that confirm its Tier 4 ranking:

### 1. Mode 5 (Stale Guidance): Resurrecting the Obsolete 2004 AAP Guideline
In Replicate 3, Ask Doximity retrieved the obsolete **2004 AAP guideline** (*Pediatrics* 2004; *Annals of Pharmacotherapy* 2005) and prescribed:
> *"Amoxicillin (Amoxil) **45 mg/kg/day divided BID** × 7–10 days... (90 mg/kg/day divided BID for severe cases is guideline alternative if local resistance is high; **standard dose 45 mg/kg/day is adequate for this presentation**)"*

* **The Clinical Danger:** The 2013 AAP guideline established that high-dose amoxicillin (**80–90 mg/kg/day**) is mandatory first-line therapy for all treated pediatric AOM to overcome penicillin-non-susceptible *Streptococcus pneumoniae*. Prescribing 45 mg/kg/day results in subtherapeutic middle-ear fluid concentrations and microbiological failure.

### 2. Mode 6 (Finite-Rule Error): Arithmetic Token Clashing
In the very same Replicate 3 response, Ask Doximity generated conflicting prescription orders on consecutive lines:
* **Line 1:** `~560 mg PO twice daily` *(which equals $90.3\text{ mg/kg/day}$)*
* **Line 2:** `558 mg/day → 280 mg PO BID` *(which equals $45\text{ mg/kg/day}$)*

The model computed the daily total ($12.4\text{ kg} \times 45\text{ mg/kg} = 558\text{ mg/day}$), but erroneously labeled it "twice daily" on line 1, before dividing by 2 on line 2.

### 3. Mode 6: Toxic Acetaminophen Ceiling Inflation
In Replicate 2, Ask Doximity stated:
> *"Continue acetaminophen (Tylenol) 10–15 mg/kg every 4–6 hours as needed for fever and otalgia, **not to exceed 100 mg/kg/day**."*

* **The Safety Threat:** The FDA and AAP maximum safe pediatric daily dose is **75 mg/kg/day** (not to exceed 4,000 mg/day). Clinical hepatotoxicity begins at 120–150 mg/kg/day. A 100 mg/kg ceiling erodes the safety buffer for parents administering over-the-counter liquid suspensions.

### 4. Mode 4 (Citation Scrambling): FDA IV/PR Monographs for Oral Antibiotics
In Replicate 2, the RAG citation pipeline completely scrambled footnote associations:
* A sentence asserting that *"approximately 70–80% of children improve without antibiotics"* was linked to **Source 5: "Acetaminophen PR [Rectal] pediatric dosing. FDA, 2025"**.
* A sentence discussing safety-net oral antibiotic prescriptions was linked to **Source 4: "Acetaminophen IV pediatric dosing. FDA, 2025"**.

---

## The 7 AI Error Modes: Unified Cross-Platform Summary

| Error Mode | Description & Part 1 Canonical Name | Commercial CDS Status | Prime Clinical Example from Audit |
| :--- | :--- | :---: | :--- |
| **Mode 1** | **Omission** | ⚠️ **Observed** | Citing UK NICE 224 to omit US AAP-recommended renal ultrasound in UTI; punting weight-based mg dosing to clinician in CAP. |
| **Mode 2** | **Invented Facts (Chart Confabulation)** | ⚠️ **Observed** | Silently asserting *"no loss of consciousness"* and *"witnessed short fall"* in minor head trauma to force an observation branch. |
| **Mode 3** | **Harmful Commission** | ⚠️ **Observed** | Advising clinic staff to *"Activate EMS now / Call 911"* for an alert, stable 6-month-old infant nursing in clinic after a brief febrile seizure. |
| **Mode 4** | **Citation Failure (Threshold Conflation)** | ⚠️ **Observed** | Conflating active 5-minute status epilepticus rescue thresholds with the 15-minute diagnostic definition of complex febrile seizure; scrambling PECARN age bands. |
| **Mode 5** | **Stale Guidance** | ⚠️ **Observed** | Resurrecting obsolete 2004 AAP guideline to prescribe subtherapeutic 45 mg/kg amoxicillin for AOM. |
| **Mode 6** | **Finite-Rule Error (Calculation & Math)** | ⚠️ **Observed** | Halving daily pneumonia dose (415 mg BID instead of 832 mg); emitting conflicting 560 mg vs 280 mg orders on adjacent lines; inflating APAP max to 100 mg/kg/day. |
| **Mode 7** | **Demographic Bias** | ⚪ **Not Evaluated in Part 2** | Standardized clinical audit used neutral baseline stems. Systematic demographic permutations from Part 1 deferred to dedicated equity re-benchmarks. |

---

## Core Guidelines for Clinicians Deploying AI Tools

1. **Never Trust an LLM for Pediatric Weight-Based Arithmetic:**  
   Even specialized clinical platforms fail basic division (e.g., dividing daily dose by 2) or default to adult fixed tablets (500 mg TID). Always use a dedicated, validated formulary calculator.
2. **Beware the "Equipoise Confabulation" Trap:**  
   When a patient case falls in a clinical grey zone, unconstrained AI tools silently hallucinate missing negative history to make the decision appear simple. If the chart didn't state it, do not let the AI assume it.
3. **Guard Against Transnational Guideline Leakage:**  
   AI models trained on global literature frequently blend US AAP, UK NICE, and European guidelines. Verify that recommendations align with local jurisdictional practice standards.
4. **Choose Interactive Choice Architecture Over Autocomplete:**  
   Platforms that expose toggle chips and explicit clarifying questions (like AMBOSS and UpToDate's interactive layer) are inherently safer than tools that provide fluent, unverified prose.
