# LinkedIn Feed Announcement Post (The Article Trailer)

*Character count: 2771 characters (comfortably within LinkedIn's 3,000-character feed limit).*

---

```text
Two weeks ago, I published "The Anatomy of an AI Clinical Error" after testing 10 frontier models on an ambiguous pediatric ear infection.

In 41% of baseline runs, models silently fabricated unstated chart history to reach an unhedged plan. Yet on Turn 2, 97% immediately recognized the exact assumptions they had made.

In the comments, clinical AI leaders like Graham Walker, MD (MDCalc founder) and Gabe Wilson, MD asked the key questions: Does this happen in acute emergencies? What is the mechanism? And can we prompt Turn 1 so clinicians don't have to interrogate the AI in Turn 2?

To find out, we expanded the study from 140 traces to 1,324 clinical generation traces across 8 cohorts and 10 foundation models (Anthropic, OpenAI, Google, xAI).

Today, I published Part 2: "The Boolean Checklist Trap, the Epistemic Split, and the Prompt Scale Paradox."

Here is the core story:

1️⃣ We reproduced the failure in a high-stakes setting:
In unwitnessed pediatric head trauma (PECARN), frontier Claude models (Sonnet 5, Opus 5) fabricated "- No loss of consciousness — negative" on 66.7% of baseline runs to justify observation over CT imaging—even though the fall was unwitnessed.

2️⃣ We identified the trigger: The Boolean Checklist Trap.
In pneumonia and UTI, baseline confabulation was rare. Why? Those guidelines are additive: positive findings justify treatment. But when a clinical rule requires an unrecorded variable to be negative before clearing an exclusionary gate, models cast the unknown to negative to stay decisive.

3️⃣ We found a prompt intervention that changed the behavior: Brake + Branching.
Telling models "it's okay to say you don't know" was ignored. An epistemic brake alone still left models guessing. The solution was pairing the brake with authorization for contingency branches:

"Do not assume unstated variables are negative. Provide conditional if/then recommendations."

This eliminated observed confabulation in our head trauma factorial across all three Claude tiers (0/9, 0.0%).

In the full article, we also examine:
• The Cross-Lab Divide: Why OpenAI and Google models didn't hallucinate checkboxes, but silently omitted missing data entirely (0/12 LOC mentions)—and how Brake + Branching prompted 91.7% active conditional branching.
• The Model-Scale Paradox: Why asking "what missing data would change your plan?" provoked hallucinations in Haiku 4.5, but helped Sonnet 5.
• Parametric Literature Decay: Why prompt engineering cannot fix 20-year-old drug dosing weights.

Read the full article and trace autopsies here:
[LINK TO ARTICLE]

All 1,324 raw traces, codebooks, and replication scripts are open: https://lnkd.in/gKHBTh99

#HealthcareAI #ClinicalAI #MedicalInformatics #LLMs #AIAlignment #PatientSafety #Pediatrics
```
