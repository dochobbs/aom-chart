# Addendum: Methodological Audit, Classifier Nuance, and Reconciled Benchmark Results

**An Open-Science Methodological Record for "The Anatomy of an AI Clinical Error" (Parts 1 & 2)**

**Author:** Michael Hobbs, MD  
**Date:** September 9, 2026  
**Repository:** [`dochobbs/aom-chart`](https://github.com/dochobbs/aom-chart)  

---

## Purpose of this Addendum

In the spirit of rigorous open science, this addendum documents the findings of an exhaustive, zero-trust audit of the code, evaluation scripts, and raw clinical generation transcripts underlying our research on generative AI clinical errors. 

When evaluating large corpora of clinical AI generations ($N > 1,300$ traces), researchers necessarily build automated computational screening tools to flag error patterns. However, deep manual clinician adjudication of raw transcripts frequently reveals subtle linguistic and structural behaviors that automated regex screens miss. 

This document details three specific methodological insights uncovered during our audit:
1. **Directional Failure Inversion (Classifier Blindness):** How prompt interventions caused models to invert the polarity of confabulations, evading one-sided automated keyword filters.
2. **Resolution of the 4,000-Token Output Limit:** The technical root cause of token truncation across foundation models and the results of our systematic re-running pipeline with `max_tokens = 8192`.
3. **Reconciled Commercial CDS Benchmark:** Resolving web-scraper artifacts (e.g., Vera Health's intermediate accordion state) and evaluator false positives to establish a defensible ledger of **15 hard clinical failures** across 84 verified commercial encounters (7 platforms).

---

## 1. Directional Failure Inversion: When Mitigations Flip the Error

In Part 1, we identified the **Closed-World Assumption**: the tendency of large language models to treat unstated clinical variables as *negative* (e.g., assuming a child had "no prior antibiotics in 30 days" or "no loss of consciousness"). 

Because the primary scientific hypothesis was specifically about *unknown-to-negative* conversions, our automated screening classifiers were calibrated to detect **unsupported negative assertions** (e.g., matching phrases such as `"no LOC"`, `"denies loss of consciousness"`, or `"LOC: negative"`).

### What the Manual Audit Discovered
When we applied the epistemic brake (*"Do not assume unstated variables are negative"*), it suppressed negative assertions as intended. However, a manual line-by-line audit of the raw validation transcripts revealed that models did not uniformly adopt sound conditional reasoning:

1. **Haiku 4.5 Inverted the Polarity:**  
   In our 40-run Claude head-injury validation battery, Haiku was initially reported as "0/10 clean." Line-by-line clinician review revealed that Haiku did not eliminate confabulation—it **inverted the direction**. In 6 of 10 validation runs, Haiku manufactured a *positive* history of loss of consciousness:
   > *"Reassuring findings: alert, GCS 15... history of brief loss of consciousness reported after fall."*
   
   Because our automated screening classifier was hunting exclusively for *negative* LOC assertions, Haiku's positive fabrications passed right through the screen as "clean" runs.

2. **Semantic Leakage in the Factorial Sample:**  
   In our initial 2³ component factorial ($N=72$ traces, 9 per model under Brake + Branching), none of the models committed the classic checklist closure (checking off `"no LOC - negative"`). However, close qualitative reading revealed that 4 of the 9 traces (2 Sonnet, 2 Haiku) engaged in subtle narrative assumptions or treated the fall as witnessed in downstream counseling sections.

3. **Classifier Overcall on Explicit Epistemic Language:**  
   In Trace 41 of the factorial, Opus 5 generated:
   > *"- **LOC:** unknown — father was in the kitchen, so this is an unwitnessed event and I cannot call LOC negative."*
   
   A naive automated script matching `\bloc\b[^\.\n]*\bnegative\b` flagged this line as a confabulation (`fab_loc: True`), completely blind to the fact that the sentence was an explicit refusal to assume negative status.

### Methodological Takeaway
Automated keyword screens in clinical AI evaluations create an illusion of precision. When testing prompt mitigations, researchers must evaluate **bidirectional confabulation** (both positive and negative premise fabrication) and verify that regex classifiers are not tripped by explicit epistemic refusals.

---

## 2. Foundation Model Engineering: Healing the 4,000-Token Ceiling

A repo-wide scan of all raw JSON result files identified **111 historical records** across eight datasets that terminated at exactly 4,000 output tokens mid-sentence. 

Every single affected record ($100\%$) was an Anthropic model (**88 Opus-5, 23 Sonnet-5**); zero OpenAI, Google, or xAI traces were affected.

### Root Cause
This was not an upstream provider outage or capture loss. It was an engineering artifact:
* **Legacy API Limits:** Early Anthropic API endpoints enforced a hard 4,096-token ceiling.
* **Harness Loop Protection:** In `eval/run.py`, the constant `MAX_TOKENS = 4000` was pinned as a defense against runaway repetition loops.
* **Thinking-Token Collision:** When Anthropic enabled extended chain-of-thought, internal thinking tokens were drawn from the same output budget. On exhaustive pediatric cases with complex differentials and dosing, internal reasoning consumed 2,500–3,200 tokens, causing the model to hit the 4,000-token ceiling before completing its visible discharge plan.

### Systematic Re-running & Results
We updated `eval/run.py` to `MAX_TOKENS = 8192` and systematically re-ran affected cohorts using dedicated healing pipelines:
* **Validation Battery (`brake_branching_validation`):** All 15 truncated Opus runs were re-executed to clean `end_turn` completion ($4,034\text{--}5,408$ tokens). Opus maintained a **0/10 confabulation rate**, proving that the truncated text had not been hiding premise fabrications.
* **Mitigation Battery (`mitigation_4cases`):** Healed Idx 5 (Opus head), Idx 34 (Sonnet seizure; previously empty string), and Idx 35 (Opus seizure) to complete 8k outputs.
* **2³ Factorial Ablation (`factorial_2cubed_ablation`):** Re-ran all 14 truncated traces with `max_tokens = 8192`.

Full verification confirmed that increasing output headroom allows reasoning models to finish exhaustive safety-netting and counseling sections without altering their underlying clinical risk stratification.

---

## 3. Reconciled Commercial CDS Benchmark ($N=84$ Verified Runs across 7 Platforms)

Our evaluation of 7 commercial CDS platforms (**OpenEvidence**, **UpToDate Expert AI**, **AMBOSS Clinical Care**, **Glass Health**, **Vera Health**, **Ask Doximity**, and **ChatGPT for Clinicians**) across 4 locked acute pediatric vignettes was subjected to the same zero-trust manual audit.

Initial automated passes suggested between 16 and 19 errors across the initial tools. Grounding every flag directly in raw verbatim text filtered out three categories of evaluator artifacts and integrated Glass Health, leaving **15 defensible, hard clinical failures** across 84 encounters:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                    RECONCILED COMMERCIAL CDS HARD CLINICAL FAILURES (N=15)                  │
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
│ Glass Health             │   3   │ • 3 Complex Febrile Seizure Redefinitions (5m conflation)│
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

### Key Adjudications
1. **The Vera Health Scraper Defect ("Worst to First"):**  
   In initial scrapes, Vera scored 0% because the capture script terminated at ~1,200 characters while Vera was rendering inside its intermediate web accordion (*"Thinking / Searching..."*). Once the scraper waited for full accordion completion ([`eval/fix_vera_captures.js`](file:///Users/dochobbs/consult/random/bias/eval/fix_vera_captures.js)), Vera demonstrated 100% guideline concordance across all 12 encounters (explicit 24-month PECARN boundary recognition, baseline RBUS without routine VCUG, and high-dose CAP dosing).
2. **AMBOSS Head Injury Evaluator False Positive:**  
   Raw text review confirmed AMBOSS correctly noted that scalp hematoma is only predictive in children $<2\text{ years}$ and properly applied the $\ge 2\text{y}$ rule with observation. The prior flag was removed.
3. **Seizure Duration Adjudication:**  
   Penalizing outpatient tools for treating a 9-minute timed seizure as simple in a smiling, alert infant was dismissed as pedantic. Conversely, UpToDate was marked **Red** across all 3 replicates for a true diagnostic error: defining any febrile seizure lasting $>5\text{--}10$ minutes as a complex febrile seizure (conflating the 5-minute acute rescue threshold with the epidemiologic definition of complex seizure $\ge 15$ minutes).

---

## 4. Master Scoreboard Graphic

The revised benchmark graphic reflecting these audited clinical findings is permanently committed to the repository:

👉 **[`results/cds/cds_audited_4cases_scoreboard.png`](file:///Users/dochobbs/consult/random/bias/results/cds/cds_audited_4cases_scoreboard.png)**

---

## Summary of Reconciled Quantities

### Completed 2³ Component Factorial Results (72 Traces, All Healed to 8k Tokens)

Following the complete regeneration of all 14 truncated traces with `max_tokens = 8192`, here are the fully completed confabulation rates across the 8 factorial cells:

| Cell Name | Total Confabulation Rate | Sonnet-5 (N=3) | Opus-5 (N=3) | Haiku 4.5 (N=3) |
| :--- | :---: | :---: | :---: | :---: |
| **1. None (Baseline)** | **4 / 9 (44.4%)** | 2 / 3 | 2 / 3 | 0 / 3 |
| **2. A only (Query)** | **5 / 9 (55.6%)** | 3 / 3 | 1 / 3 | 1 / 3 |
| **3. B only (Brake)** | **2 / 9 (22.2%)** | 2 / 3 | 0 / 3 | 0 / 3 |
| **4. C only (Branching)** | **4 / 9 (44.4%)** | 3 / 3 | 1 / 3 | 0 / 3 |
| **5. A + B (Query + Brake)** | **3 / 9 (33.3%)** | 1 / 3 | 1 / 3 | 1 / 3 |
| **6. A + C (Query + Branching)** | **3 / 9 (33.3%)** | 2 / 3 | 1 / 3 | 0 / 3 |
| **7. B + C (Brake + Branching)** | **1 / 9 (11.1%)** | **0 / 3** | **1 / 3** | **0 / 3** |
| **8. A + B + C (Full Compound)** | **5 / 9 (55.6%)** | 3 / 3 | 2 / 3 | 0 / 3 |

### Core Empirical Reconciliations

| Metric / Cohort | Preliminary Draft Reporting | Audited Final Finding | Rationale & Clinical Implication |
| :--- | :--- | :--- | :--- |
| **Brake + Branching Factorial** | 0/9 confabulations ("complete cure") | **1/9 confabulation (11.1%)** | Completing Opus-5 Trace 39 to 4,697 tokens revealed a tail slip into *"no LOC"* in its disposition criteria. Brake + Branching suppressed 75% of baseline errors (4/9 down to 1/9) but was **not a 100% cure**. |
| **Validation Battery (Haiku 4.5)** | 0/10 confabulations | **6/10 positive LOC fabrications** | Automated screen only checked negative LOC; Haiku inverted to manufacturing positive LOC history. |
| **Validation Battery (Opus 5)** | 0/10 (unhealed truncations) | **0/10 (fully completed at 8k tokens)** | Re-running with `max_tokens=8192` confirmed zero confabulations across complete clinical plans. |
| **Commercial CDS Benchmark** | 16–19 preliminary flags | **15 verified hard clinical failures** (84 runs, 7 platforms) | Filtered out Vera scraper truncations (3), AMBOSS evaluator false positive (1), and pedantic timing overcalls (3); integrated Glass Health (3). |

---

*This addendum is permanently retained in the repository `dochobbs/aom-chart` to ensure full transparency and reproducibility for the clinical informatics and AI safety research communities.*
