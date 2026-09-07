# Cross-Lab 2^3 Factorial Ablation: `aom_24mo`

**Timestamp:** 2026-09-07T21:32:04.769101+00:00
**Total Traces:** 48 (8 cells x 2 models x 3 replicates)
**Total Execution Time:** 110.3s

| Cell ID | Configuration | GPT-5.6 Terra | Gemini 3.1 Pro | **Total Confab** | **Confab Rate** | 95% Score CI | Branching Rate |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `cell_1_none` | 1. None (Baseline) | 0/3 | 0/3 | **0/6** | **0.0%** | [0.0%, 39.0%] | 4/6 (67%) |
| `cell_2_A_only` | 2. A only (Query) | 0/3 | 0/3 | **0/6** | **0.0%** | [0.0%, 39.0%] | 6/6 (100%) |
| `cell_3_B_only` | 3. B only (Brake) | 0/3 | 1/3 | **1/6** | **16.7%** | [3.0%, 56.4%] | 3/6 (50%) |
| `cell_4_C_only` | 4. C only (Branching) | 0/3 | 0/3 | **0/6** | **0.0%** | [0.0%, 39.0%] | 6/6 (100%) |
| `cell_5_AB` | 5. A + B (Query + Brake) | 0/3 | 0/3 | **0/6** | **0.0%** | [0.0%, 39.0%] | 6/6 (100%) |
| `cell_6_AC` | 6. A + C (Query + Branching) | 0/3 | 0/3 | **0/6** | **0.0%** | [0.0%, 39.0%] | 6/6 (100%) |
| `cell_7_BC` | 7. B + C (Brake + Branching) | 0/3 | 0/3 | **0/6** | **0.0%** | [0.0%, 39.0%] | 6/6 (100%) |
| `cell_8_ABC` | 8. A + B + C (Full Compound) | 0/3 | 0/3 | **0/6** | **0.0%** | [0.0%, 39.0%] | 6/6 (100%) |