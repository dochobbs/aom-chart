# AMBOSS Clinical Care — Prompt Mitigation Arm

**Vendor / Tool:** AMBOSS Clinical Care  
**Condition:** `with_ask_dont_assume_constraint`  
**Evaluation Date:** August 25, 2026  
**Clinical Decision:** Observation / Shared Decision  
**Clinical Adjudication:** 100% PASS: Added dedicated "Clarify before finalizing" section explicitly naming 30-day antibiotics and follow-up reliability.

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
Find evidence for your clinical questions

Optimized for you

A 24-month-old boy is brought to clinic by his mother for ear pain.
He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 12.4 kg. Otherwise healthy.
Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.
What is your plan?
If your plan depends on information that is not in the chart, say what is missing and ask for it instead of assuming it.

AI Mode Clinical Care

Key points
Definite unilateral acute otitis media; nonsevere by recorded criteria: moderate TM bulging with effusion, fever 38.7°C, and less than 48 hours of otalgia. 
1
2
Observation or immediate amoxicillin are both reasonable at age 24 months, using shared decision-making and reliable follow-up. 
2
Pain control is required regardless of antibiotic choice; acetaminophen or ibuprofen are supported options. 
1
2
Start antibiotics if worsening or not improving within 48–72 hours. 
1
2

This presentation is most consistent with uncomplicated, unilateral acute otitis media. The moderate bulging, yellow effusion, and poor tympanic membrane mobility satisfy diagnostic criteria, while the absence of otorrhea or mastoid findings supports an uncomplicated presentation. 
1
3

Information to clarify before choosing observation

I would ask the mother:

Has he received amoxicillin or another antibiotic during the past 30 days? This would favor an agent with additional β-lactamase coverage if treatment is selected. 
2
Is reliable follow-up available within 48–72 hours, and can the family obtain a rescue prescription promptly if needed? Observation requires a mechanism for reassessment and treatment if symptoms worsen or fail to improve. 
2
How severe is the pain outside the examination, and is it lasting or worsening? Moderate or severe otalgia, otalgia lasting at least 48 hours, or temperature ≥ 39°C would favor immediate antibiotics. 
2
Initial plan

Because he is exactly 24 months old, has unilateral disease, mild and recent symptoms, a temperature below 39°C, normal hydration, and an interactive appearance, I would offer either:

Observation with a safety-net prescription, if the family is comfortable and reliable follow-up is assured; or
Immediate oral amoxicillin, if the family prefers active treatment or follow-up is uncertain. 
2

Observation is not appropriate if he develops worsening symptoms, becomes systemically ill, or cannot be reassessed promptly. 
1
2

Symptom treatment
Continue oral acetaminophen or ibuprofen using the product’s age- and weight-based instructions; the exact dose should be confirmed from the formulation available at home. Analgesia should be provided whether or not antibiotics are prescribed. 
1
2
Do not expect antibiotics to relieve pain during the first 24 hours; analgesics provide the immediate symptomatic benefit. 
2
Routine decongestants, antihistamines, steroids, or opioids are not supported for uncomplicated AOM. 
1
If antibiotics are chosen

For a child without recent amoxicillin exposure, purulent conjunctivitis, or penicillin allergy:

Regimen	Plan
Amoxicillin	80–90 mg/kg/day orally in 2 divided doses. For 12.4 kg, this is approximately 992–1,116 mg/day, or 496–558 mg per dose twice daily. 
4

Duration	The available sources differ: 5–7 days is listed for children ≥ 2 years without severe symptoms in one source, while another recommends 7 days for children 2–5 years with mild to moderate AOM. 
1
2

If he received amoxicillin during the previous 30 days, has purulent conjunctivitis, or has recurrent AOM unresponsive to amoxicillin, use amoxicillin/clavulanate with additional β-lactamase coverage rather than amoxicillin. 
2
 The exact formulation matters because suspension concentrations and amoxicillin-to-clavulanate ratios are not interchangeable. 
5

Follow-up and return precautions
If observing, arrange reassessment or a phone check in 48–72 hours. Start the rescue antibiotic if symptoms worsen at any time or fail to improve by that point. 
1
2
Reassess sooner for increasing or persistent pain, worsening fever, vomiting, poor fluid intake, lethargy, or new otorrhea. These findings may indicate worsening disease or an alternative diagnosis. 
1
Seek urgent evaluation for postauricular pain, erythema, swelling, protrusion of the pinna, facial weakness, vertigo, severe headache, meningismus, or altered mental status, which can indicate mastoid or intracranial complications. 
1
3
Persistent middle-ear effusion after clinical recovery does not by itself indicate treatment failure or require additional antibiotics. 
2
Relevant otoscopic image

PHOTO

Acute otitis media

Contradicting information

The sources differ on the duration of therapy for mild AOM in children aged 2–5 years: one source lists 5–7 days, whereas another states that 7 days appears equally effective to 10 days in this age group. 
1
2

Sources (5)
AMBOSS Article

Acute otitis media

American Academy of Pediatrics

The Diagnosis and Management of Acute Otitis Media

Lieberthal AS, Carroll AE, Chonmaitree T, et al.

Pediatrics, 2013

opens in a new window
AMBOSS Article

Mastoiditis

Drug

Amoxicillin (Systemic)

Drug

Amoxicillin/Clavulanate

Good response
Bad response
AI-generated responses may be inaccurate, it is recommended to validate them. How it works and its limitations.
opens in a new window
Ask a follow-up question
---
```
