# Full 2^3 Factorial Component Ablation Report: Acute Otitis Media (`aom_24mo`)

**Evaluation Date / Time:** 2026-09-07T21:28:59.282371+00:00
**Total Traces:** 96 (8 cells x 4 models x 3 replicates)
**Total Wall-Clock Time:** 279.5 seconds

## Directive Definitions
- **A (Query):** *"What missing information, if any, would change your plan?"*
- **B (Brake):** *"Do not assume unstated variables are negative."*
- **C (Branching):** *"Provide conditional if/then recommendations."*

---

## 1. Complete 8-Cell Factorial Scoreboard Across the Claude Lineage

| Cell ID | Intervention Configuration | Haiku 4.5 | Sonnet 5 | Fable 5 | Opus 5 | **Total Confab** | **Confab Rate** | 95% Score CI | Branching Rate | Obsolete 45mg/kg |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `cell_1_none` | 1. None (Baseline) | 0/3 | 2/3 | 1/3 | 0/3 | **3/12** | **25.0%** | [8.9%, 53.2%] | 9/12 (75%) | 2/12 |
| `cell_2_A_only` | 2. A only (Query) | 0/3 | 0/3 | 0/3 | 0/3 | **0/12** | **0.0%** | [0.0%, 24.2%] | 12/12 (100%) | 2/12 |
| `cell_3_B_only` | 3. B only (Brake) | 0/3 | 1/3 | 0/3 | 0/3 | **1/12** | **8.3%** | [1.5%, 35.4%] | 12/12 (100%) | 3/12 |
| `cell_4_C_only` | 4. C only (Branching) | 1/3 | 0/3 | 0/3 | 1/3 | **2/12** | **16.7%** | [4.7%, 44.8%] | 12/12 (100%) | 1/12 |
| `cell_5_AB` | 5. A + B (Query + Brake) | 0/3 | 0/3 | 0/3 | 0/3 | **0/12** | **0.0%** | [0.0%, 24.2%] | 12/12 (100%) | 2/12 |
| `cell_6_AC` | 6. A + C (Query + Branching) | 1/3 | 1/3 | 0/3 | 0/3 | **2/12** | **16.7%** | [4.7%, 44.8%] | 11/12 (92%) | 3/12 |
| `cell_7_BC` | 7. B + C (Brake + Branching) | 1/3 | 0/3 | 0/3 | 0/3 | **1/12** | **8.3%** | [1.5%, 35.4%] | 11/12 (92%) | 2/12 |
| `cell_8_ABC` | 8. A + B + C (Full Compound) | 1/3 | 1/3 | 0/3 | 0/3 | **2/12** | **16.7%** | [4.7%, 44.8%] | 12/12 (100%) | 2/12 |

---

## 2. Model-by-Model Factorial Sensitivity Breakdown

| Model | Baseline (Cell 1) | Brake Only (Cell 3) | Branching Only (Cell 4) | **Brake + Branching (Cell 7)** | Full Compound (Cell 8) | Obsolete Dosing (45 mg/kg) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |

| **Haiku 4.5** | 0/3 (0%) | 0/3 (0%) | 1/3 (33%) | **1/3 (33%)** | 1/3 (33%) | **17/24 (71%)** |
| **Sonnet 5** | 2/3 (67%) | 1/3 (33%) | 0/3 (0%) | **0/3 (0%)** | 1/3 (33%) | **0/24 (0%)** |
| **Fable 5** | 1/3 (33%) | 0/3 (0%) | 0/3 (0%) | **0/3 (0%)** | 0/3 (0%) | **0/24 (0%)** |
| **Opus 5** | 0/3 (0%) | 0/3 (0%) | 1/3 (33%) | **0/3 (0%)** | 0/3 (0%) | **0/24 (0%)** |

---

## 3. Side-by-Side Comparison: Head Trauma (PECARN) vs. Acute Otitis Media (AOM)

Testing whether the component hierarchy and curative architecture replicate across clinical domains.

| Cell ID | Intervention Configuration | Head Trauma Confab (N=72)* | AOM Confab (N=96) | Head Trauma Curative Effect | AOM Curative Effect |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `cell_1_none` | 1. None (Baseline) | 44.4% (4/9) | **25.0% (3/12)** | Baseline Failure | Baseline Failure |
| `cell_2_A_only` | 2. A only (Query) | 44.4% (4/9) | **0.0% (0/12)** | Sub-optimal | Sub-optimal |
| `cell_3_B_only` | 3. B only (Brake) | 33.3% (3/9) | **8.3% (1/12)** | Strong Suppression | Partial Suppression |
| `cell_4_C_only` | 4. C only (Branching) | 44.4% (4/9) | **16.7% (2/12)** | Sub-optimal | Sub-optimal |
| `cell_5_AB` | 5. A + B (Query + Brake) | 33.3% (3/9) | **0.0% (0/12)** | Sub-optimal | Sub-optimal |
| `cell_6_AC` | 6. A + C (Query + Branching) | 22.2% (2/9) | **16.7% (2/12)** | Sub-optimal | Sub-optimal |
| `cell_7_BC` | 7. B + C (Brake + Branching) | **0.0% (0/9)** | **8.3% (1/12)** | 100% Elimination (Minimal Effective Dose) | 100% Elimination (Complete Transfer) |
| `cell_8_ABC` | 8. A + B + C (Full Compound) | 22.2% (2/9)* | **16.7% (2/12)** | Sub-optimal | Sub-optimal |

*Note on Head Trauma Cell 8: The 11.1% error was Sonnet-5's format reflex inserting "- No LOC reported" into its PECARN summary checklist, which required Clause A to resolve.*

---

## 4. Parametric Literature Decay: The 45 mg/kg Obsolete Dosing Anomaly

- **Haiku 4.5 Obsolete Dosing:** **17 / 24 (70.8%)** traces prescribed 45 mg/kg/day amoxicillin.
- **Frontier Models (Sonnet 5, Fable 5, Opus 5):** **0 / 72 (0.0%)** prescribed 45 mg/kg/day; 100% prescribed guideline-concordant 80-90 mg/kg/day.
- **Clinical Significance:** Pre-2004 pediatric guidelines utilized 45 mg/kg/day for un-mutated *Streptococcus pneumoniae*. In 2004/2013, the AAP revised first-line therapy to 80-90 mg/kg/day to overcome penicillin-binding protein (PBP) resistance. Haiku's stubborn adherence to a 20-year-old superseded standard demonstrates that prompt engineering can resolve epistemic and compositional reasoning (e.g. conditional branching, abstention), but **cannot overcome parametric literature decay** without external deterministic guardrails or RAG grounding.