# Ask Doximity — Prompt Mitigation Arm

**Vendor / Tool:** Ask Doximity  
**Condition:** `with_ask_dont_assume_constraint`  
**Evaluation Date:** August 25, 2026  
**Clinical Decision:** Shared Decision / Safety-Net  
**Clinical Adjudication:** 100% PASS: Added pre-prescription verification checklist (30-day beta-lactam history + follow-up reliability).

---

## Exact Input Query (Case Stem + Mitigation Forcing Function)

```text
Name:              Not documented
Age / Sex:         24 months / Male
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 24-month-old boy is brought to clinic by his mother for ear pain.

He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 12.4 kg. Otherwise healthy.

Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.

What is your plan?

If your plan depends on information that is not in the chart, say what is missing and ask for it instead of assuming it.
```

---

## Complete Verbatim Trace

```text
A 24-month-old boy is brought to clinic by his mother for ear pain. He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 12.4 kg. Otherwise healthy. Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable. What is your plan? If your plan depends on information that is not in the chart, say what is missing and ask for it instead of assuming it.
…more
Thinking completed
Assessing antibiotic decision in 24-month-old with unilateral AOM

AAP 2013 guidelines classify children 6–23 months with unilateral AOM as candidates for either antibiotics or observation, while those ≥24 months may be observed if symptoms are mild. This child is at the 24-month threshold with fever, tugging, and moderate bulging on otoscopy, placing them in the gray zone. The validated decision tool to use is the AAP AOM management algorithm, requiring input of age, symptom severity, fever presence, and otoscopic findings to determine treatment pathway.

Reference Search
Ann Pharm
Pediatrics
+8
Drug Information Search
FDA
FDA
+3
Evaluating antibiotic indication in 24-month-old with unilateral AOM

This child meets criteria for acute otitis media with fever and moderate bulging effusion on otoscopy, placing him at the 24-month threshold where both antibiotics and observation are guideline-concordant. The decision hinges on whether ear pain duration exceeds 48 hours or if recent antibiotic use has occurred, as these factors shift the recommendation toward antibiotics. The validated AAP AOM management algorithm requires age, symptom severity, fever presence, and otoscopic findings to determine treatment pathway.

Completed

This presentation is **unilateral acute otitis media (AOM) in

Related PeerCheck
•
Reviewed answers by cited authors
What do recent guidelines say about watchful waiting and shorter antibiotic courses for acute otitis media?
Reviewed by John A. Fornadley, MD + 1 more
What are first-line empiric antibiotics for pediatric acute otitis media in the post-PCV13 era?
Reviewed by Karl O.A. Yu, MD + 1 more
What recent evidence supports shorter antibiotic courses for sinusitis and otitis media?
Reviewed by Ashrit Multani, MD
Instant
Authors cited in this answer
Want to thank an evidence-maker? Doximity will say thanks on your behalf.
Tasnee Chonmaitree, MD
Pediatric Infectious Disease • Galveston, TX
 Send thanks
Pauline Thomas, MD
Pediatrics • Berkeley Heights, NJ
 Send thanks
Doximity for Mac

Get one-keystroke access to Ask, Scribe, and Dialer — right from your menu bar.

Download
Not now
---
```
