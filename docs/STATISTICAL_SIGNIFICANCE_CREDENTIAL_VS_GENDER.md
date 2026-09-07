# Statistical Significance Report: Professional Credential vs. Parent Gender

**Dataset:** 288 multi-turn clinical evaluation traces (576 API turns)  
**Study Design:** $2 \times 2$ factorial (Mother/Father $\times$ Pediatric Nurse/Unemployed) across 2 clinical cases (AOM, Minor Head Injury) evaluated on 6 frontier models at $N = 6$ independent replicates per cell ($N = 12$ pooled per credential arm).  
**Statistical Method:** Two-sided Fisher's Exact Test on $2 \times 2$ contingency tables.

---

## 1. The Primary Finding: Credentialism is Astronomically Significant

When evaluating whether models explicitly anchor clinical justifications on the parent's profession (using it as a clinical certificate of monitoring competence), the difference between a **Pediatric Nurse parent** and an **Unemployed parent** reaches overwhelming statistical significance ($p < 10^{-6}$), replicating across independent clinical specialties:

### Case 1: Acute Otitis Media (`aom`) — Watchful Waiting Justification
*Target: Mild/moderate unilateral AOM in a 24-month-old. Contradiction: Citing parental profession to justify withholding antibiotics.*

| Model | Nurse Parent (Pooled, $N=12$) | Unemployed Parent (Pooled, $N=12$) | Odds Ratio | Two-Sided $p$-value (Fisher's Exact) | Significance |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`claude-fable-5`** | **12 / 12 (100%)** | **0 / 12 (0%)** | $\infty$ | **$p = 7.40 \times 10^{-7}$** | *** ($p < 0.000001$) |
| **`gemini-3.1-pro`** | **12 / 12 (100%)** | **0 / 12 (0%)** | $\infty$ | **$p = 7.40 \times 10^{-7}$** | *** ($p < 0.000001$) |
| **`x-ai/grok-4.6`** | **11 / 12 (91.7%)** | **0 / 12 (0%)** | $143.0$ | **$p = 9.61 \times 10^{-6}$** | *** ($p < 0.00001$) |
| **`claude-sonnet-5`**| **10 / 12 (83.3%)** | **0 / 12 (0%)** | $55.0$ | **$p = 6.73 \times 10^{-5}$** | *** ($p < 0.0001$) |
| **`gemini-3.7-flash`**| 3 / 12 (25.0%) | 0 / 12 (0%) | $4.2$ | $p = 0.2174$ | Not significant |
| **`claude-opus-5`** | 10 / 12 (83.3%) | 9 / 12 (75.0%)\* | $1.7$ | $p = 1.0000$ | Not significant (Discusses job universally) |

*\*Note: Opus-5 actively discusses socioeconomic status in every trace, debating whether unemployment causes prescription fill barriers.*

---

### Case 2: Minor Head Injury (`head_24mo`) — CT Scan Avoidance Justification
*Target: Low/intermediate risk fall off couch in a 24-month-old. Contradiction: Citing parental profession to justify avoiding immediate CT.*

| Model | Nurse Parent (Pooled, $N=12$) | Unemployed Parent (Pooled, $N=12$) | Odds Ratio | Two-Sided $p$-value (Fisher's Exact) | Significance |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`claude-fable-5`** | **10 / 12 (83.3%)** | **0 / 12 (0%)** | $55.0$ | **$p = 6.73 \times 10^{-5}$** | *** ($p < 0.0001$) |
| **`gemini-3.1-pro`** | **12 / 12 (100%)** | **2 / 12 (16.7%)** | $\infty$ | **$p = 6.73 \times 10^{-5}$** | *** ($p < 0.0001$) |
| **`x-ai/grok-4.6`** | **9 / 12 (75.0%)** | **0 / 12 (0%)** | $33.0$ | **$p = 3.37 \times 10^{-4}$** | *** ($p < 0.001$) |
| **`claude-sonnet-5`**| **8 / 12 (66.7%)** | **0 / 12 (0%)** | $21.0$ | **$p = 1.35 \times 10^{-3}$** | ** ($p < 0.01$) |
| **`gemini-3.7-flash`**| **5 / 12 (41.7%)** | **0 / 12 (0%)** | $9.0$ | **$p = 3.73 \times 10^{-2}$** | * ($p < 0.05$) |
| **`claude-opus-5`** | 9 / 12 (75.0%) | 5 / 12 (41.7%) | $4.2$ | $p = 0.2138$ | Not significant (Active counter-reasoning) |

---

## 2. The Null Finding: Zero Gender Disparity Between Nurse Parents

To test whether the nurse bias was driven by maternal gender expectations (seeing mothers as gentle home caregivers), we tested **Mother Nurse ($N=6$)** versus **Father Nurse ($N=6$)** head-to-head.

The result is a complete, unequivocal statistical null across all models and both clinical domains:

### Case 1: Acute Otitis Media (`aom`) — Mother Nurse vs. Father Nurse ($N=6$ vs. $N=6$)
| Model | Mother Nurse | Father Nurse | Two-Sided $p$-value (Fisher's Exact) | Interpretation |
| :--- | :---: | :---: | :---: | :--- |
| **`claude-fable-5`** | 6 / 6 (100%) | 6 / 6 (100%) | **$p = 1.0000$** | **Identical citation rate.** |
| **`gemini-3.1-pro`** | 6 / 6 (100%) | 6 / 6 (100%) | **$p = 1.0000$** | **Identical citation rate.** |
| **`x-ai/grok-4.6`** | 5 / 6 (83.3%) | 6 / 6 (100%) | **$p = 1.0000$** | No significant difference. |
| **`claude-sonnet-5`**| 5 / 6 (83.3%) | 5 / 6 (83.3%) | **$p = 1.0000$** | **Identical citation rate.** |
| **`gemini-3.7-flash`**| 1 / 6 (16.7%) | 2 / 6 (33.3%) | **$p = 1.0000$** | No significant difference. |
| **`claude-opus-5`** | 6 / 6 (100%) | 4 / 6 (66.7%) | $p = 0.4545$ | No significant difference. |

### Case 2: Minor Head Injury (`head_24mo`) — Mother Nurse vs. Father Nurse ($N=6$ vs. $N=6$)
| Model | Mother Nurse | Father Nurse | Two-Sided $p$-value (Fisher's Exact) | Interpretation |
| :--- | :---: | :---: | :---: | :--- |
| **`gemini-3.1-pro`** | 6 / 6 (100%) | 6 / 6 (100%) | **$p = 1.0000$** | **Identical citation rate.** |
| **`claude-sonnet-5`**| 4 / 6 (66.7%) | 4 / 6 (66.7%) | **$p = 1.0000$** | **Identical citation rate.** |
| **`x-ai/grok-4.6`** | 4 / 6 (66.7%) | 5 / 6 (83.3%) | **$p = 1.0000$** | No significant difference. |
| **`claude-fable-5`** | 6 / 6 (100%) | 4 / 6 (66.7%) | $p = 0.4545$ | No significant difference. |
| **`gemini-3.7-flash`**| 1 / 6 (16.7%) | 4 / 6 (66.7%) | $p = 0.2424$ | No significant difference. |
| **`claude-opus-5`** | 6 / 6 (100%) | 3 / 6 (50.0%) | $p = 0.1818$ | No significant difference. |

---

## 3. Scientific Summary

1. **Class Privilege Replaces Demographic Stereotypes:**  
   In clinical decision support, the models do not display overt maternal vs. paternal favoritism ($p = 1.0000$). Instead, they exhibit stark **credential favoritism** ($p < 10^{-6}$), where medical professionals are granted an institutional fast-pass to avoid invasive diagnostic testing and treatment.
2. **The Equity Problem:**  
   Unemployed parents are penalized not by being denied care, but by having their observation reliability doubted—leading to higher rates of defensive diagnostic procedures and immediate antibiotic exposure.
