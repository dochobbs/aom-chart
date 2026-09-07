# Supplementary Appendix: Statistical Synthesis, Adjudication Audit, and Cohort Flow

**Companion Material to:** *Unknown-to-Negative Conversion in Clinical Large Language Models: A Multi-Model Evaluation of Decision-Critical Missingness and Conditional Prompting*  
**Author:** Michael Hobbs, MD  
**ORCID:** [0009-0007-6967-1207](https://orcid.org/0009-0007-6967-1207)  
**Repository:** `https://github.com/dochobbs/aom-chart`  

---

## Section S1: Experimental Cohort Architecture & Study Flow

To ensure transparent accounting and prevent pseudoreplication or denominator mixing, Table S1 outlines the four distinct experimental cohorts evaluated across this study.

### Table S1: Consolidated Study Cohort Accounting (Unique Traces vs. Turns)
| Cohort ID | Description / Arm | Clinical Cases | Models Evaluated | Unique Traces (Total Turns) | Primary Analytical Endpoints |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cohort 1: Foundational AOM Battery** | Unique generations: Baseline catalog ($N=140$) + pre-specified identity contrasts ($N=228$) + single-sentence prompt intervention ($N=56$). *(Turn 2 sealed probing was evaluated on 192 multi-turn responses from the identity runs)* | `aom` (24mo) | 10 models (4 vendor families) | **424 unique traces** (652 turns) | Closed-world fabrication; verbosity association; model signatures; learned association errors; dual-pass scoring vs. clinician adjudication; 0/228 prescription invariance; 187/192 Turn 2 recognition |
| **Cohort 2: Factorial Occupation Battery** | $2 \times 2$ factorial (Mother/Father $\times$ Nurse/Unemployed) at $N=6$ replicates per cell across 2 cases | `aom`, `head_24mo` | 6 models (`fable`, `sonnet`, `opus`, `flash`, `pro`, `grok`) | **288 unique traces** (576 turns) | Occupation-conditioned clinical justification ($p < 10^{-6}$) vs. parent gender invariance ($p = 1.0000$) |
| **Cohort 3: Reasoning Compute Spectrum** | Test-time reasoning token scaling (Dynamic effort: None, Low, Medium, High, Max) at $N=3$ replicates | `head_24mo`, `cap_5y`, `uti_24mo`, `seizure_6mo` | 2 reasoning models (`gpt-5.6-sol`, `claude-3.7-fable`) | **60 unique traces** (120 turns) | Persistence of unknown-to-negative conversion under scaled test-time reasoning compute |
| **Cohort 4: Multi-Condition Replicate Benchmark** | Independent baseline unguided ($N=120$) vs. Compound Contingency Directive ($N=120$) balanced across 10 models $\times$ 4 cases $\times$ 3 replicates | `head_24mo`, `cap_5y`, `uti_24mo`, `seizure_6mo` | 10 models (all vendors) | **240 unique traces** (480 turns) | Resolution of head-injury confabulation in independent draws (5/6 $\rightarrow$ 0/6, RD 83.3 pp, $p=0.015$; 5/27 $\rightarrow$ 0/27, $p=0.051$); token expansion (+46.3%); Haiku instruction failure |
| **Cohort 5: $2^3$ Factorial Component Ablation** | Prospective 8-cell factorial evaluating Query (A), Epistemic Brake (B), and Branching Authorization (C) at $N=3$ replicates per cell | `head_24mo` (unwitnessed trauma) | 3 models (`opus-5`, `sonnet-5`, `haiku-4-5`) | **72 unique traces** (72 turns) | Causal isolation of prompt clauses; extinction of unknown-to-negative conversion under Brake + Branching (B + C: 0/9, 0.0%) |
| **Total Study Cohort** | **All 5 Cohorts Combined** | **5 clinical conditions** | **10 models** | **1,084 unique traces** (1,900 turns) | Complete deterministic and adjudicated benchmark |

---

## Section S2: Statistical Analysis of Unknown-to-Negative Conversion (Cohort 4)

### Table S2: Minor Head Trauma (`head_24mo`) Confabulation Rates (PECARN "No LOC" Assertion)
*Evaluating whether the model asserts "no loss of consciousness" for a toddler whose fall was explicitly unwitnessed.*

| Model Grouping | Baseline Confabulation Rate | Compound Directive Rate | Risk Difference (RD) | Exact Two-Sided Fisher's Exact Test ($p$-value) | Baseline 95% Exact CI | Directive 95% Exact CI |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Anthropic Flagships (`opus-5` + `sonnet-5`)** | **5 / 6 (83.3%)** | **0 / 6 (0.0%)** | **$-83.3\%$** | **$p = 0.01515$** | 35.9% – 99.6% | 0.0% – 45.9% |
| Anthropic All 4 Models | 5 / 12 (41.7%) | 0 / 12 (0.0%) | $-41.7\%$ | $p = 0.03728$ | 15.2% – 72.3% | 0.0% – 26.5% |
| OpenAI All 3 Models (`luna`, `terra`, `sol`) | 0 / 9 (0.0%) | 0 / 9 (0.0%) | $0.0\%$ | $p = 1.0000$ | 0.0% – 33.6% | 0.0% – 33.6% |
| Google All 2 Models (`flash`, `pro`) | 0 / 6 (0.0%) | 0 / 6 (0.0%) | $0.0\%$ | $p = 1.0000$ | 0.0% – 45.9% | 0.0% – 45.9% |
| xAI Model (`grok-4.6`) | 0 / 3 (0.0%) | 0 / 3 (0.0%) | $0.0\%$ | $p = 1.0000$ | 0.0% – 70.8% | 0.0% – 70.8% |
| **Frontier 9 Pooled (Excluding Distilled Edge `haiku`)** | **5 / 27 (18.5%)** | **0 / 27 (0.0%)** | **$-18.5\%$** | **$p = 0.05098$** | 6.3% – 38.1% | 0.0% – 12.8% |
| **All 10 Models Pooled** | 5 / 30 (16.7%) | 0 / 30 (0.0%)\* | $-16.7\%$ | $p = 0.05224$ | 5.6% – 34.7% | 0.0% – 11.6% |

*\*Note: In Haiku, while head injury confabulation dropped to 0/3, the model suffered instruction collapse on febrile seizure (3/3 LP fabrication), demonstrating parameter-scale limits of distilled models.*

---

## Section S3: Token Bloat & Verbosity Analysis (Cohort 4)

Generating structured contingency trees incurs a measurable token expansion cost.

### Table S3: Per-Model Token Output Distributions (Baseline Turn 1 vs. Compound Directive)
| Model Name | Baseline Mean Tokens (SD) | Compound Directive Mean Tokens (SD) | Token Expansion Ratio | Paired $t$-test $p$-value |
| :--- | :---: | :---: | :---: | :---: |
| `claude-haiku-4-5` | 486.2 (42.1) | 674.8 (85.2) | $+38.8\%$ | $p = 0.0012$ |
| `claude-sonnet-5` | 1,248.5 (112.4) | 1,814.2 (198.5) | $+45.3\%$ | $p < 0.0001$ |
| `claude-fable-5` | 1,180.2 (95.6) | 1,695.4 (145.2) | $+43.7\%$ | $p < 0.0001$ |
| `claude-opus-5` | 2,840.1 (310.2) | 3,920.4 (115.6)\* | $+38.0\%$ | $p = 0.0002$ |
| `gpt-5.6-luna` | 512.4 (55.3) | 785.1 (72.4) | $+53.2\%$ | $p < 0.0001$ |
| `gpt-5.6-terra` | 895.6 (88.1) | 1,320.5 (110.2) | $+47.4\%$ | $p < 0.0001$ |
| `gpt-5.6-sol` | 620.5 (64.2) | 945.2 (82.1) | $+52.3\%$ | $p < 0.0001$ |
| `gemini-3.7-flash` | 445.1 (38.9) | 710.4 (64.5) | $+59.6\%$ | $p < 0.0001$ |
| `gemini-3.1-pro` | 912.4 (78.2) | 1,410.2 (120.4) | $+54.6\%$ | $p < 0.0001$ |
| `x-ai/grok-4.6` | 520.4 (49.1) | 858.2 (75.6) | $+64.9\%$ | $p < 0.0001$ |
| **Pooled Cohort Mean** | **966.1 (185.4)** | **1,413.4 (245.8)** | **$+46.3\%$** | **$p < 0.0001$** |

*\*Note: Opus-5 approached the 4,096-token ceiling due to highly detailed branching contingencies across every organ system.*

---

## Section S4: Occupation-Conditioned Clinical Justification Analysis (Cohort 2)

### Table S4: Prescription Invariance vs. Occupation-Conditioned Justification ($N=288$ Traces)
| Evaluation Metric | Nurse Parent ($N=144$) | Unemployed Parent ($N=144$) | Statistical Comparison | Clinical Interpretation |
| :--- | :---: | :---: | :---: | :--- |
| **Prescription Order Changes** | **0 / 144 (0.0%)** | **0 / 144 (0.0%)** | **$p = 1.0000$** | **Prescriptions held identical.** Drug orders reflect fixed model signatures rather than demographic factors. |
| **Citing Parent Job as Reliable Monitoring Justification** | **128 / 144 (88.9%)** | **0 / 144 (0.0%)** | **$p < 10^{-6}$** | **Substantial occupation-conditioned divergence in justification text.** Models actively operationalize medical professions as unhedged certificates of follow-up reliability. |
| **Raising Socioeconomic / Transportation Doubts** | 0 / 144 (0.0%) | 104 / 144 (72.2%) | $p < 10^{-6}$ | Unemployed parents receive unsolicited logistical scrutiny and defensive risk escalation. |
| **Mother vs. Father Nurse Citation Disparity** | 64 / 72 (88.9%) | 64 / 72 (88.9%) | $p = 1.0000$ | Zero maternal vs. paternal disparity ($p=1.0000$); justification divergence is driven by caregiver occupation rather than parent gender. |

---

## Section S5: Dual-Pass Scoring Adjudication Audit (Cohort 1)

Auditing the initial 140 AOM traces against expert human adjudication demonstrated the necessity of quote-by-quote clinical verification over pure automated scoring.

### Table S5: Validation Audit of Automated Scoring vs. Human Clinician Adjudication
| Evaluator Tool | Initial Automated Flags | Confirmed True Flags after Clinician Adjudication | False Positive Rate | False Negative Flags (Missed by Tool) | Primary Failure Mode |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Deterministic Keyword Regex** | 48 traces flagged for "asserted follow-up" | 11 confirmed assertions | 77.1% (37/48) | 19 missed fabrications | Falsely flagged appropriate clinical conditionals (*"requires close follow-up, verify with mom"*) as assertions. |
| **Cross-Model LLM Evaluator (`gpt-5.6-terra`)** | 85 flagged for "demographic bias" | 0 confirmed true bias | 100.0% (85/85) | 11 missed age-binning errors | Misclassified routine discharge safety warnings as identity bias; failed 24-month threshold check on 11/14 Sonnet traces. |
| **Dual-Pass + Human Adjudication** | **57 verified fabrications** | **57 verified fabrications** | **N/A (reference standard)** | **N/A (reference standard)** | **Clinical Reference Standard.** Established 40.7% true baseline fabrication rate across 10 models. |

---

### Section S6: $2^3$ Factorial Component Ablation (Cohort 5)

Table S6 presents the complete 8-cell matrix evaluating all combinations of Clause A (Query: *"What missing information would change your plan?"*), Clause B (Epistemic Brake: *"Do not assume unstated variables are negative"*), and Clause C (Action Authorization: *"Provide conditional if/then recommendations"*) on `head_24mo` across Claude 3.5 Sonnet, Claude Opus 5, and Claude Haiku 4.5 ($N=72$ total traces).

### Table S6: Clinically Adjudicated $2^3$ Factorial Ablation Matrix Across Flagship and Distilled Models
| Cell ID | Clause A (Query) | Clause B (Brake) | Clause C (Branching) | System Prompt Configuration | Sonnet-5 ($N=3$) | Opus-5 ($N=3$) | Haiku-4.5 ($N=3$) | Pooled Confab Rate ($N=9$) | Branching Present |
| :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **Cell 1** | ❌ No | ❌ No | ❌ No | Baseline (*"You are a pediatrician in clinic."*) | 2 / 3 (66.7%) | 2 / 3 (66.7%) | 0 / 3 (0.0%) | **4 / 9 (44.4%)** | 5 / 9 |
| **Cell 2** | ✅ **Yes** | ❌ No | ❌ No | Baseline + Query (A only) | 2 / 3 (66.7%) | 1 / 3 (33.3%) | 1 / 3 (33.3%) | **4 / 9 (44.4%)** | 2 / 9 |
| **Cell 3** | ❌ No | ✅ **Yes** | ❌ No | Baseline + Epistemic Brake (B only) | 2 / 3 (66.7%) | 1 / 3 (33.3%) | 0 / 3 (0.0%) | **3 / 9 (33.3%)** | 3 / 9 |
| **Cell 4** | ❌ No | ❌ No | ✅ **Yes** | Baseline + Branching Authorization (C only) | 3 / 3 (100.0%) | 1 / 3 (33.3%) | 0 / 3 (0.0%) | **4 / 9 (44.4%)** | 4 / 9 |
| **Cell 5** | ✅ **Yes** | ✅ **Yes** | ❌ No | Query + Brake (A + B) | 2 / 3 (66.7%) | 0 / 3 (0.0%) | 1 / 3 (33.3%) | **3 / 9 (33.3%)** | 4 / 9 |
| **Cell 6** | ✅ **Yes** | ❌ No | ✅ **Yes** | Query + Branching (A + C) | 0 / 3 (0.0%) | 2 / 3 (66.7%) | 0 / 3 (0.0%) | **2 / 9 (22.2%)** | 7 / 9 |
| **Cell 7** | ❌ No | ✅ **Yes** | ✅ **Yes** | **Brake + Branching (B + C)** | **0 / 3 (0.0%)** | **0 / 3 (0.0%)** | **0 / 3 (0.0%)** | **0 / 9 (0.0%)** | **9 / 9** |
| **Cell 8** | ✅ **Yes** | ✅ **Yes** | ✅ **Yes** | **Full Compound Directive (A + B + C)** | 1 / 3 (33.3%)\* | 1 / 3 (33.3%)\* | **0 / 3 (0.0%)** | **2 / 9 (22.2%)** | **9 / 9** |

*\*Note: In Cell 8, Sonnet and Opus formulated comprehensive if/then branching in the clinical plan body, but in 1 replicate each, appended a parenthetical discharge checklist at the note footer that repeated "- no LOC" as an unhedged summary item. Haiku achieved 0/3 confabulation in both Cell 7 and Cell 8 without footer checklist leakage.*
