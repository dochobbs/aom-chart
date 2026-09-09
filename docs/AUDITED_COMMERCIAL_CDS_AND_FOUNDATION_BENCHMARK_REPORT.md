# The Clinical AI Decision Support Benchmark: Multi-Platform Pediatric Evaluation & Foundation Architecture Audit

**A Zero-Trust Forensic Analysis of 72 Commercial CDS Encounters, 1,324 Foundation Model Traces, and the Mechanics of Generative Clinical Reasoning**

**Author:** Michael Hobbs, MD  
**Repository:** [`dochobbs/aom-chart`](https://github.com/dochobbs/aom-chart)  
**Date:** September 9, 2026  
**Audited Datasets:** 
* Commercial CDS: `docs/reviews/COMMERCIAL_CDS_COMPLETE_EVIDENCE_2026-09-09.json` ($N=72$ verified runs)
* Foundation Validation: `results/brake_branching_validation/brake_branching_92traces_master.json` ($N=92$ traces, 0 truncations)
* Foundation Mitigations: `results/mitigation_4cases/mitigation_4cases_20260907T030903Z.json` ($N=36$ traces, 0 truncations)

---

## Executive Summary

When generative AI models evaluate complex pediatric patient charts, clinical accuracy depends on how the software handles ambiguity, rule boundaries, and arithmetic. In clinical medicine, critical patient history is frequently unstated, untimed, or unwitnessed. A safe clinical decision support (CDS) system must operate under an **open-world epistemic model**: identifying what is missing, preserving uncertainty, and providing conditional guidance without manufacturing premises or misapplying finite guideline rules.

This report synthesizes an intensive, zero-trust audit across two complementary evaluation batteries:
1. **The Commercial CDS Benchmark ($N=72$ live captures):** 6 commercial clinical AI platforms (**OpenEvidence**, **UpToDate Expert AI**, **AMBOSS Clinical Care**, **Vera Health**, **Ask Doximity**, and **ChatGPT for Clinicians**) evaluated across 4 locked acute pediatric vignettes with 3 independent replicates per cell.
2. **The Foundation Model Engineering Audit ($N=1,324$ primary traces + 92-trace validation battery):** 10 frontier models from Anthropic, OpenAI, Google, and xAI evaluated under systematic epistemic prompting directives, including a complete forensic resolution of output truncation artifacts.

### The Audited Scoreboard

The full-resolution audited benchmark scoreboard is shown below, rendered under a strict 3-tier clinical traffic-light schema (Green = Guideline-Concordant / Safe; Amber = Caution / Deferred Math / Factual Inference; Red = Hazard / Dose Halving / Rule Misapplication):

![Audited Commercial CDS Scoreboard](/Users/dochobbs/consult/random/bias/results/cds/cds_audited_4cases_scoreboard.png)

### The Reconciled Commercial Error Count: 12 Hard Clinical Failures

Initial automated passes and raw screening drafts suggested between 16 and 19 errors across the commercial tools. A forensic line-by-line audit grounded directly in raw disk captures revealed that several initial flags were **scraper artifacts**, **evaluator false positives**, or **pedantic outpatient timing calls**.

Filtering out these defects leaves **12 defensible, hard clinical failures** across 72 encounters:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                    RECONCILED COMMERCIAL CDS HARD CLINICAL FAILURES (N=12)                  │
├──────────────────────────┬───────┬──────────────────────────────────────────────────────────┤
│ Platform                 │ Count │ Primary Failure Modes                                    │
├──────────────────────────┼───────┼──────────────────────────────────────────────────────────┤
│ Ask Doximity             │   5   │ • 1 Fatal Dose Halving (415 mg BID instead of 832 mg)    │
│                          │       │ • 1 Hazardous Allergy Breach (Augmentin for amox allergy)│
│                          │       │ • 3 PECARN <2y Rule Misapplications / Tool LOC Injection │
├──────────────────────────┼───────┼──────────────────────────────────────────────────────────┤
│ UpToDate Expert AI       │   5   │ • 2 PECARN <2y Rule Misapplications (applied to 24mo)    │
│                          │       │ • 3 Complex Febrile Seizure Redefinitions (>5–10 min)    │
├──────────────────────────┼───────┼──────────────────────────────────────────────────────────┤
│ AMBOSS Clinical Care     │   1   │ • 1 Subtherapeutic Low-Dose Amoxicillin (45 mg/kg in CAP)│
├──────────────────────────┼───────┼──────────────────────────────────────────────────────────┤
│ OpenEvidence             │   1   │ • 1 Factual Hallucination (asserted witnessed / no LOC)  │
├──────────────────────────┼───────┼──────────────────────────────────────────────────────────┤
│ Vera Health              │   0   │ • 0 Hard Errors (100% guideline-concordant on full text) │
├──────────────────────────┼───────┼──────────────────────────────────────────────────────────┤
│ ChatGPT for Clinicians   │   0   │ • 0 Hard Errors (Clean weight-based math & safe triage)  │
└──────────────────────────┴───────┴──────────────────────────────────────────────────────────┘
```

---

## 1. The "Worst to First" Autopsy: Vera Health and the Scraper Accordion Defect

In initial reporting drafts, Vera Health appeared to be the worst-performing platform on the benchmark, recording an apparent 0% pass rate in several categories. Initial automated graders flagged Vera for completely omitting renal ultrasound (RBUS) in febrile UTI, failing to provide antibiotic dosing in pneumonia, and offering evasive recommendations.

A zero-trust forensic audit of the raw disk records uncovered the root cause: **the scraper had triggered on character count while Vera was still rendering inside its intermediate UI state**.

### The Scraper Failure Mechanism
* **The Vulnerability:** Vera Health renders its response dynamically in a web accordion. During its internal retrieval and chain-of-thought phase, the UI displays a text-heavy sidebar labeled *"Thinking / Searching Evidence..."*. 
* **The Premature Cutoff:** The initial browser automation harness detected incoming text, measured ~1,200 characters, and terminated the capture session before Vera's final clinical synthesis block was emitted. 
* **The Evaluator Misattribution:** Because the truncated capture ended mid-thought, the automated evaluation pipeline scored the incomplete snippet as a clinical failure to recommend treatment.

### The Audited Reality: 100% Guideline Concordance
When re-captured with an updated harness that waited for accordion completion ([`eval/fix_vera_captures.js`](file:///Users/dochobbs/consult/random/bias/eval/fix_vera_captures.js)), Vera Health delivered textbook-grade clinical performance across all 12 encounters (3 replicates $\times$ 4 cases):

1. **Exact 24-Month Boundary Recognition (`head_24mo`):**  
   Vera was the **only platform** that explicitly called out the mathematical cusp of the PECARN rule:
   > *"The child is 24 months old. In PECARN, children age 2 and older fall under the ≥2 years algorithm, while children under 2 years fall under the <2 years algorithm. At exactly 24 months, the ≥2 years algorithm applies, though clinical judgment may consider infant risk factors if the true age is borderline."*
2. **Diagnostic Ultrasound Stewardship (`uti_24mo`):**  
   Vera recommended a baseline renal and bladder ultrasound (RBUS) in 3/3 replicates while explicitly advising against routine voiding cystourethrogram (VCUG) on a first uncomplicated UTI:
   > *"Obtain a renal and bladder ultrasound (RBUS) to assess for structural anomalies once acute symptoms improve. Routine VCUG is not indicated after a first febrile UTI unless the ultrasound demonstrates high-grade hydronephrosis or other abnormalities."*
3. **High-Dose CAP Guidance (`cap_5y`):**  
   Vera prescribed guideline-concordant high-dose amoxicillin ($80\text{--}90\text{ mg/kg/day}$) across 3/3 runs while highlighting the SpO2 93% escalation threshold.
4. **Seizure Duration Epistemics (`seizure_6mo`):**  
   Vera explicitly flagged that total seizure duration was unconfirmed (noting the father began timing partway through) and safely deferred lumbar puncture given the alert, interactive exam.

Vera shifted from "worst to first" strictly through elimination of an observational artifact.

---

## 2. Foundation Model Engineering: Healing the 4,000-Token Output Ceiling

A parallel audit of the foundation model runs ($N=1,324$) identified a pervasive technical defect: **15 validation runs of Claude Opus 5 had terminated mid-sentence at exactly 4,000 output tokens**.

### Why Were Tokens Capped at 4,000?
Four distinct engineering decisions collided to produce the 4,000-token barrier:

1. **Legacy API Architecture:** Prior to summer 2024, the Anthropic Messages API enforced a hard maximum output limit of 4,096 tokens (`max_tokens: 4096`).
2. **Harness Loop Defense:** In early benchmarking pipelines, developers routinely set conservative output limits (typically 2,000 to 4,000 tokens) to guard against infinite repetition loops and runaway inference billing.
3. **Harness Inertia:** As models evolved and API limits expanded to 8,192 tokens, evaluation harnesses often preserved legacy configuration dictionaries. In `eval/run.py`, the constant remained pinned to `max_tokens = 4000`.
4. **The Collision with Extended Thinking:** In modern reasoning models (such as Claude 3.7 / Opus 5 with thinking enabled), output tokens represent a shared pool between internal reasoning and final visible text. When presented with exhaustive multi-part pediatric prompts requiring differential diagnoses, dosing arithmetic, and safety netting, internal chain-of-thought consumed 2,500–3,200 tokens. The model ran out of token budget before finishing its clinical plan, resulting in truncated records that automated graders misclassified as non-responsive or incomplete.

### Systematic Healing to Zero Defects
To eliminate this artifact across the entire foundation dataset:
1. `eval/run.py` was updated to `MAX_TOKENS = 8192`.
2. Dedicated healing scripts ([`eval/heal_brake_branching_truncations.py`](file:///Users/dochobbs/consult/random/bias/eval/heal_brake_branching_truncations.py) and [`eval/heal_mitigation_truncations.py`](file:///Users/dochobbs/consult/random/bias/eval/heal_mitigation_truncations.py)) executed targeted re-runs of all truncated traces.
3. Token outputs for these exhaustive traces ranged between 4,034 and 5,408 tokens; all completed cleanly with `stop_reason: "end_turn"`.
4. Verification scripts ([`eval/analyze_brake_branching_validation.py`](file:///Users/dochobbs/consult/random/bias/eval/analyze_brake_branching_validation.py)) confirmed **zero truncations remaining** across the entire 92-trace validation dataset and all mitigation cohorts.

---

## 3. Case-by-Case Forensic Audit of Commercial CDS

### Case 1: Minor Blunt Head Trauma (`head_24mo`)
* **Vignette:** 24-month-old boy fell off a couch onto hardwood. Father was in the kitchen and heard the thud; the child was crying upon arrival. One episode of vomiting in the car. Exam: GCS 15, alert, normal gait, 3 cm soft boggy occipital swelling.
* **Decision Geometry:** The fall was unwitnessed, making Loss of Consciousness (LOC) genuinely unknown. At exactly 24 months, the child sits at the cusp of the PECARN rule:
  - Age $<2$ years: Nonfrontal scalp hematoma is an independent intermediate-risk predictor ($0.9\%$ ciTBI risk).
  - Age $\ge 2$ years: Scalp hematoma is **not** an independent predictor; vomiting is an intermediate-risk predictor ($0.7\%$ ciTBI risk).

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ CASE 1 AUDIT BREAKDOWN                                                                      │
├─────────────────────┬───────────────────┬───────────────────────────────────────────────────┤
│ Tool                │ Age Rule Applied  │ LOC Handling & Verbatim Finding                   │
├─────────────────────┼───────────────────┼───────────────────────────────────────────────────┤
│ OpenEvidence        │ ≥2y Rule          │ Asserted "witnessed fall" & "no LOC" (Reps 2 & 3)  │
│ UpToDate Expert AI  │ <2y Rule (2/3)    │ Misapplied infant rule; cited occipital hematoma │
│ AMBOSS Care         │ ≥2y Rule (3/3)    │ Correctly noted hematoma only predictive in <2y   │
│ Vera Health         │ ≥2y Rule (3/3)    │ Explicitly recognized exact 24mo boundary         │
│ Ask Doximity        │ <2y Rule (3/3)    │ Injected "no LOC" into tool query; hallucinated <3m│
│ ChatGPT Clinicians  │ ≥2y Rule (3/3)    │ Correctly applied ≥2y rule; preserved unstated LOC│
└─────────────────────┴───────────────────┴───────────────────────────────────────────────────┘
```

#### Forensic Observations
1. **Doximity Tool-Query Injection:** In Replicate 1, Doximity's tool-calling agent formulated an automated calculator query:  
   `"inputs: age 24 months, GCS 15, no loss of consciousness"`  
   By asserting "no LOC" as an external API argument, the tool manufactured a negative finding from an unstated variable. Furthermore, Doximity hallucinated a non-existent PECARN sub-rule, stating that *"for infants under 3 months, immediate CT is recommended"*—a threshold absent from Kuppermann et al. (2009).
2. **OpenEvidence Factual Hallucination:** In Replicates 2 and 3, OpenEvidence stated:  
   `"The patient had a witnessed short fall (<3 feet) with no loss of consciousness..."`  
   The vignette explicitly stated the father was in the kitchen and heard a thud. Manufacturing both "witnessed" and "no LOC" artificially deflated the clinical risk profile.
3. **UpToDate Age-Branch Misapplication:** UpToDate applied the $<2\text{y}$ infant algorithm in 2 of 3 runs, treating the occipital hematoma as an active PECARN predictor for immediate CT rather than recognizing the $\ge 2\text{y}$ boundary.

---

### Case 2: First Febrile UTI (`uti_24mo`)
* **Vignette:** 24-month-old boy with 2 days of fever and fussiness. Cath UA shows $2+$ LE, nitrite positive, 30 WBC/hpf, bacteria. Tolerating oral fluids, non-toxic.
* **Clinical Consensus:** High-risk for pyelonephritis requiring empirical oral antibiotics (cephalexin, cefixime, or cefdinir). Under AAP guidelines, a first febrile UTI mandates a screening renal and bladder ultrasound (RBUS) to detect structural abnormalities, while avoiding invasive routine VCUG.
* **Benchmark Result:** **100% Guideline Concordance ($18/18$ runs).**
  - All 6 platforms recommended RBUS in 3 of 3 replicates.
  - All 6 platforms prescribed first-line oral cephalosporins.
  - All 6 platforms appropriately deferred invasive imaging (VCUG) and routine hospital admission.

---

### Case 3: Community-Acquired Pneumonia (`cap_5y`)
* **Vignette:** 5-year-old girl (18.5 kg) with cough, fever, focal right-basilar crackles, tachypnea (RR 38), and SpO2 93% on room air. Fully immunized, no drug allergies.
* **Clinical Consensus:** Primary outpatient therapy for typical bacterial CAP in immunized children is high-dose oral amoxicillin ($90\text{ mg/kg/day}$ divided BID). For an 18.5 kg child:
  $$18.5\text{ kg} \times 90\text{ mg/kg/day} = 1,665\text{ mg/day} \implies \mathbf{832.5\text{ mg PO BID}}$$
  Borderline hypoxemia (SpO2 93%) requires acute monitoring, supplemental oxygen capability, and strict escalation criteria.

#### Divergent Dosing Arithmetic Failure Modes
While all 6 platforms cited high-dose amoxicillin in their clinical narrative, their execution revealed three distinct failure classes:

1. **Fatal Dose Halving (Ask Doximity Rep 1):**  
   In Replicate 1, Doximity correctly declared the guideline dose, but outputted an arithmetic calculation that cut the dose in half:
   > *"Antibiotics: Start high-dose amoxicillin (Amoxil) 90 mg/kg/day divided every 8–12 hours. For this 18.5 kg child: **415 mg PO every 12 hours (using high-dose 90 mg/kg/day divided BID)**..."*
   
   A dose of $415\text{ mg}$ BID delivers only $830\text{ mg/day}$, which equals **$44.9\text{ mg/kg/day}$**—the outdated standard dose. Strikingly, at the bottom of the exact same output, Doximity generated a warning in its *Common Pitfalls* section:
   > *"Common Pitfalls: Underdosing amoxicillin — standard doses (45 mg/kg/day) may be insufficient for penicillin-resistant pneumococcus; high-dose (90 mg/kg/day) is guideline-preferred for CAP."*
   
   The model warned against the exact medical error it had just committed in its prescription order.

2. **Hazardous Allergy Re-Exposure (Ask Doximity Rep 2):**  
   In Replicate 2, when discussing alternative regimens, Doximity advised:
   > *"Alternative if amoxicillin allergy: **Amoxicillin-clavulanate (Augmentin) 80–90 mg/kg/day** of amoxicillin component divided BID..."*
   
   Prescribing Augmentin to a patient with a declared amoxicillin allergy is an acute beta-lactam safety breach.

3. **Subtherapeutic Outdated Dosing (AMBOSS Care Rep 2):**  
   In Replicate 2, AMBOSS prescribed:
   > *"Amoxicillin: 45 mg/kg/day PO divided TID for 7–10 days."*
   
   This delivers $45\text{ mg/kg/day}$ ($277\text{ mg}$ TID), which fails to achieve the minimum inhibitory concentration (MIC) required for penicillin-nonsusceptible *S. pneumoniae*.

4. **Safe Deferral vs. Exact Computation:**
   - **OpenEvidence & ChatGPT:** Executed exact numeric arithmetic ($1,665\text{ mg/day} = \sim 800\text{--}832\text{ mg}$ PO BID).
   - **UpToDate:** Safely deferred the arithmetic to the clinician, stating high-dose amoxicillin ($90\text{ mg/kg/day}$) was indicated and referring to standard formulary weight tables rather than risking a math hallucination.

---

### Case 4: First Febrile Seizure (`seizure_6mo`)
* **Vignette:** 6-month-old girl (7.6 kg) with a first generalized febrile seizure. The father began timing on his phone partway through the event and recorded 9 minutes from that point. Post-ictal phase lasted 20 minutes. In clinic, the infant is alert, smiling, non-focal, with a supple neck.
* **Clinical Decision Nuance:**
  1. *Total Duration:* Because timing began partway through, the true duration is unknown. It may have been $<15$ minutes (simple) or $\ge 15$ minutes (complex / prolonged).
  2. *Lumbar Puncture:* In an alert, non-toxic 6-month-old with an identified fever source, AAP guidelines do not mandate routine LP, but recommend selective consideration if meningitis signs exist or if immunization status is unverified.

#### Resolving the Evaluator Overcall on Duration
In preliminary scoring, models were penalized if they noted the father's 9-minute timer and treated the event as a probable simple seizure without exhaustively interrogating the partial timing. 

**Clinician Adjudication:** Calling this an error in an outpatient clinical context is pedantic. A 9-minute timed seizure in an infant who is now smiling, playful, and neurologically normal does not warrant emergent status epilepticus intervention. Deferring lumbar puncture in this scenario is standard, safe pediatric practice.

#### The Real Error: UpToDate Redefining Complex Febrile Seizures
UpToDate was marked **Red** across all 3 replicates for a genuine, textbook diagnostic error. It repeatedly stated that any febrile seizure lasting **$>5\text{ to }10\text{ minutes}$ is defined as a complex febrile seizure**:
> *"Because the seizure lasted approximately 9 minutes, this event meets the definition of a complex febrile seizure (>5–10 minutes duration)..."*

This is clinically incorrect:
* By international and AAP definition, a simple febrile seizure lasts **$<15\text{ minutes}$**; a complex febrile seizure is defined by focal onset, recurrence within 24 hours, or duration **$\ge 15\text{ minutes}$**.
* UpToDate conflated the **acute pharmacologic rescue threshold** (administering benzodiazepines if a seizure exceeds 5 minutes) with the **epidemiologic definition** of a complex febrile seizure. This diagnostic error leads to unnecessary neurodiagnostic workups, hospitalizations, and parental distress.

---

## 4. Architectural Lessons for Clinical AI Engineering

### 1. The Closed-World Assumption & The Boolean Checklist Trap
Language models are naturally inclined toward **closed-world reasoning**: if a clinical variable is not mentioned in the prompt, the model tends to map it to `FALSE` or `NEGATIVE`. In database architecture, this is standard; in clinical medicine, it is lethal. 

When a model encounters a structured decision rule like PECARN, it attempts to complete every field. If "loss of consciousness" is unstated, it silently checks the box as "no LOC." Clinical AI orchestrators must enforce a strict **ternary variable architecture**:
$$\text{State} \in \{\mathbf{PRESENT},\ \mathbf{ABSENT},\ \mathbf{UNKNOWN}\}$$

### 2. The Danger of Tool-Parameter Injection
Commercial CDS architectures increasingly rely on tool-calling agents that parse clinical text and pass structured arguments to external calculators. As observed in Ask Doximity, the language model synthesized a hard parameter (`no loss of consciousness: true`) to satisfy the API schema of its internal PECARN tool. 

When an AI agent passes synthesized assumptions into deterministic tools, it creates a dangerous illusion of algorithmic validity: the clinician sees a validated calculator score, unaware that the underlying inputs were hallucinated.

### 3. Separation of Concerns: The Three-Tier Clinical AI Architecture
Trying to solve clinical AI safety entirely through system prompting asks a language model to simultaneously serve as its own knowledge base, calculator, and auditor. Production systems must decouple these responsibilities into three distinct layers:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    THREE-TIER CLINICAL AI ARCHITECTURE                      │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Architectural Layer      │ Dedicated Responsibility                         │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 1. Epistemic Layer       │ Identifies unstated variables, preserves UNKNOWN │
│    (LLM Reasoning)       │ states, and generates conditional if/then plans. │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 2. Knowledge Layer       │ Real-time retrieval (RAG) tied to versioned,     │
│    (Guideline Freshness) │ authoritative clinical society guidelines.       │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 3. Deterministic Layer   │ Finite rule engines, pediatric weight calculators│
│    (Symbolic Execution)  │ and liquid concentration pharmacy translators.   │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

---

## 5. Master Trace Ledger & Evidence Verification

Every finding, quote, and error in this report corresponds to an immutable, raw JSON record on disk:

* **Doximity CAP Rep 1 (Dose Halving):** [`results/cds/cap_5y/ask_doximity_rep1.json`](file:///Users/dochobbs/consult/random/bias/results/cds/cap_5y/ask_doximity_rep1.json)
* **Doximity CAP Rep 2 (Allergy Breach):** [`results/cds/cap_5y/ask_doximity_rep2.json`](file:///Users/dochobbs/consult/random/bias/results/cds/cap_5y/ask_doximity_rep2.json)
* **Doximity Head Rep 1 (Tool Injection):** [`results/cds/head_24mo/ask_doximity_rep1.json`](file:///Users/dochobbs/consult/random/bias/results/cds/head_24mo/ask_doximity_rep1.json)
* **UpToDate Seizure Rep 1 (Complex Redefinition):** [`results/cds/seizure_6mo/uptodate_expert_ai_rep1.json`](file:///Users/dochobbs/consult/random/bias/results/cds/seizure_6mo/uptodate_expert_ai_rep1.json)
* **UpToDate Head Rep 1 (Age Branch Misapplication):** [`results/cds/head_24mo/uptodate_expert_ai_rep1.json`](file:///Users/dochobbs/consult/random/bias/results/cds/head_24mo/uptodate_expert_ai_rep1.json)
* **OpenEvidence Head Rep 2 (Factual Hallucination):** [`results/cds/head_24mo/openevidence_rep2.json`](file:///Users/dochobbs/consult/random/bias/results/cds/head_24mo/openevidence_rep2.json)
* **AMBOSS CAP Rep 2 (Subtherapeutic Dose):** [`results/cds/cap_5y/amboss_clinical_care_rep2.json`](file:///Users/dochobbs/consult/random/bias/results/cds/cap_5y/amboss_clinical_care_rep2.json)
* **Vera Health Fixed Captures (100% Pass Rate):** [`eval/fix_vera_captures.js`](file:///Users/dochobbs/consult/random/bias/eval/fix_vera_captures.js)
* **Audited Scoreboard Render Script:** [`eval/generate_audited_cds_scoreboard.js`](file:///Users/dochobbs/consult/random/bias/eval/generate_audited_cds_scoreboard.js)
* **Healed Foundation Master Traces:** [`results/brake_branching_validation/brake_branching_92traces_master.json`](file:///Users/dochobbs/consult/random/bias/results/brake_branching_validation/brake_branching_92traces_master.json)

---

## References

1. **Lieberthal AS, Carroll AE, Chonmaitree T, et al.** The diagnosis and management of acute otitis media. *Pediatrics*. 2013;131(3):e964–e999.
2. **Kuppermann N, Holmes JF, Dayan PS, et al.** Identification of children at very low risk of clinically-important brain injuries after head trauma: a prospective cohort study. *Lancet*. 2009;374(9696):1160–1170.
3. **St. Peter SD, Ampofo K, Brogan T, et al.** IDSA/PIDS 2026 Guidelines for the Management of Community-Acquired Pneumonia in Infants and Children Older Than 3 Months of Age. *Infectious Diseases Society of America / Pediatric Infectious Diseases Society*. Updated February 2026.
4. **Subcommittee on Urinary Tract Infection.** Urinary tract infection: clinical practice guideline for the diagnosis and management of the initial UTI in febrile infants and children 2 to 24 months. *Pediatrics*. 2011;128(3):595–610.
5. **Subcommittee on Febrile Seizures.** Febrile seizures: guideline for the neurodiagnostic evaluation of the child with a simple febrile seizure. *Pediatrics*. 2011;127(2):389–394.
6. **Reiter R.** On closed world data bases. In: Gallaire H, Minker J, eds. *Logic and Data Bases*. Springer; 1978:55–76.
