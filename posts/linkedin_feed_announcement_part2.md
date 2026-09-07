# LinkedIn Feed Announcement Post (The Article Trailer)

*Character count: ~1,950 characters (fits comfortably within LinkedIn's 3,000-character feed limit).*

---

```text
Two weeks ago, I published "The Anatomy of an AI Clinical Error" after testing 10 frontier models on an ear infection.

In 41% of runs, models silently fabricated missing chart history (like prior antibiotic use) so their decision algorithm could finish. Yet on Turn 2, 97% immediately named the exact assumptions they made.

In the comments, Graham Walker, MD (MDCalc founder) and Gabe Wilson, MD asked the load-bearing questions:
Is post-training helpfulness overriding clinical restraint? Does this happen in other acute emergencies? And can we prompt Turn 1 so clinicians don't have to interrogate the AI in Turn 2?

To answer them, we expanded the study from 140 traces to 1,084 clinical traces across 5 cohorts and 10 frontier models (Anthropic, OpenAI, Google, xAI).

Today, I published Part 2: "The Boolean Checklist Trap, the Epistemic Split, and the Prompt Scale Paradox."

Here are the four key discoveries:

1️⃣ The Additive vs. Boolean Trap:
In pneumonia and UTI, frontier models had 0% confabulation. Why? Because those guidelines are ADDITIVE (positive findings justify treatment). But in unwitnessed head trauma (PECARN), models fabricated "- No LOC — negative" on 83% of runs! When an algorithm requires an unstated negative to clear a gate, the model assumes it's negative to stay "helpful."

2️⃣ The Solution ("Brake + Branching"):
Telling models "it's okay to say you don't know" failed. Banning assumptions caused clinical paralysis. 
The breakthrough was pairing a negative constraint with contingency authorization:
"Do not assume unstated variables are negative. Provide conditional if/then recommendations."

3️⃣ The Cross-Lab Divide:
Claude fabricates facts to complete its structured checklists. OpenAI and Google glide past missing data with smooth narrative prose. In medicine, silently ignoring an unwitnessed fall's unknown LOC is just as dangerous as hallucinating that it didn't happen! Brake + Branching cures both: it stops Claude from inventing checklist items, and forces OpenAI and Google to stop ignoring missing data and branch explicitly.

4️⃣ The Model-Scale Paradox & Literature Decay:
Brake + Branching cured AOM and Head Trauma across labs. But prompt constraints cannot overwrite parametric literature decay (e.g. Haiku's 20-year-old 45 mg/kg dosing persisting from pre-2004 training data). Prompts shape epistemic reasoning; deterministic guardrails must catch obsolete medical training weights.

Read the full deep-dive article, trace autopsies, and clinical deployment principles here:
[LINK TO ARTICLE]

All 1,084 raw traces, codebooks, and Python notebooks are open: https://lnkd.in/gKHBTh99

#HealthcareAI #ClinicalAI #MedicalInformatics #LLMs #AIAlignment #PatientSafety #Pediatrics
```
