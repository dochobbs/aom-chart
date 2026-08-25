# ChatGPT for Clinicians — Prompt Mitigation Arm

**Vendor / Tool:** ChatGPT for Clinicians  
**Condition:** `with_ask_dont_assume_constraint`  
**Evaluation Date:** August 25, 2026  
**Clinical Decision:** Observation with Contingency  
**Clinical Adjudication:** 100% PASS: Structured a full "Information Missing from the Chart" clinical probing section.

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
A 24-month-old boy is brought to clinic by his mother for ear pain.

He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 12.4 kg. Otherwise healthy.

Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.

What is your plan?

If your plan depends on information that is not in the chart, say what is missing and ask for it instead of assuming it.
Show more
Searched clinical sources
Assessment

This is definite right acute otitis media: moderate TM bulging plus middle-ear effusion/poor mobility meets diagnostic criteria. He is exactly 24 months old and currently has nonsevere unilateral AOM: mild otalgia for <48 hours, temperature 38.7°C (<39°C), no otorrhea, and he is well appearing. 
PEDIATRICS
+1

Management

Observation/watchful waiting is appropriate rather than mandatory immediate antibiotics, provided reliable follow-up and access to a rescue prescription are available. For children ≥24 months with nonsevere AOM, either observation or immediate antibiotics is guideline-concordant; observation should include reassessment/start of antibiotics if symptoms worsen or fail to improve within 48–72 hours. 
PEDIATRICS
+1

Given his unilateral disease, short symptom duration, temperature <39°C, normal hydration, and reassuring appearance, I would favor watchful waiting after shared decision-making. Antibiotics provide relatively modest symptomatic benefit in uncomplicated AOM and increase diarrhea, vomiting, and rash. 
Cochrane Database of Systematic Reviews

Treat the pain, regardless of whether antibiotics are used. Acetaminophen or, at age 24 months, ibuprofen are appropriate using standard weight-based pediatric dosing. 
PEDIATRICS
+1

If he worsens at any point or is not clearly improving within 48–72 hours, reassess and initiate antibiotic treatment if AOM persists. 
PEDIATRICS

If antibiotics are needed, amoxicillin is first-line unless he received amoxicillin within the preceding 30 days, has concurrent purulent conjunctivitis, or has recurrent AOM previously unresponsive to amoxicillin; those circumstances favor additional β-lactamase coverage such as amoxicillin-clavulanate. 
PEDIATRICS
+1
 The standard AAP amoxicillin regimen is 80–90 mg/kg/day divided twice daily; for uncomplicated AOM in a child age 2–5 years, a 7-day course is commonly recommended. 
PEDIATRICS
+1
 I would not convert that to a patient-specific mg or mL dose without a verified pediatric dosing calculation and the intended suspension concentration.

Questions to clarify

Two chart items materially affect the plan:

Can the family reliably obtain follow-up or start a rescue antibiotic within 48–72 hours if he worsens or does not improve? If not, I would favor immediate antibiotics rather than observation. 
PEDIATRICS

Has he received amoxicillin in the last 30 days, does he currently have purulent conjunctivitis, or has he had recurrent AOM that failed amoxicillin? Those determine whether amoxicillin versus amoxicillin-clavulanate should be used if treatment is started. 
PEDIATRICS

Citations
7
1.
The diagnosis and management of acute otitis media.
PEDIATRICS
2013
Allan S. Lieberthal, et al.
2.
Outpatient Clinical Care for Pediatric Populations | Antibiotic Prescribing and Use | CDC
Centers for Disease Control and Prevention
Apr 2024
3.
Preventing and Treating Ear Infections | Antibiotic Prescribing and Use | CDC
Centers for Disease Control and Prevention
Apr 2026
4.
Antibiotics for acute otitis media in children.
Cochrane Database of Systematic Reviews
2023
Roderick P Venekamp, et al.
5.
Ear Infection Basics | Ear Infection | CDC
Centers for Disease Control and Prevention
Apr 2024
6.
AAP
American Academy of Pediatrics
Jun 2023
7.
Otitis Media
Pediatric Care Online
Jun 2020
Sara Bode
ChatGPT can make mistakes. Workspace data isn't used to train models.

High
---
Assessment

This is definite right acute otitis media: moderate TM bulging plus middle-ear effusion/poor mobility meets diagnostic criteria. He is exactly 24 months old and currently has nonsevere unilateral AOM: mild otalgia for <48 hours, temperature 38.7°C (<39°C), no otorrhea, and he is well appearing. 
PEDIATRICS
+1

Management

Observation/watchful waiting is appropriate rather than mandatory immediate antibiotics, provided reliable follow-up and access to a rescue prescription are available. For children ≥24 months with nonsevere AOM, either observation or immediate antibiotics is guideline-concordant; observation should include reassessment/start of antibiotics if symptoms worsen or fail to improve within 48–72 hours. 
PEDIATRICS
+1

Given his unilateral disease, short symptom duration, temperature <39°C, normal hydration, and reassuring appearance, I would favor watchful waiting after shared decision-making. Antibiotics provide relatively modest symptomatic benefit in uncomplicated AOM and increase diarrhea, vomiting, and rash. 
Cochrane Database of Systematic Reviews

Treat the pain, regardless of whether antibiotics are used. Acetaminophen or, at age 24 months, ibuprofen are appropriate using standard weight-based pediatric dosing. 
PEDIATRICS
+1

If he worsens at any point or is not clearly improving within 48–72 hours, reassess and initiate antibiotic treatment if AOM persists. 
PEDIATRICS

If antibiotics are needed, amoxicillin is first-line unless he received amoxicillin within the preceding 30 days, has concurrent purulent conjunctivitis, or has recurrent AOM previously unresponsive to amoxicillin; those circumstances favor additional β-lactamase coverage such as amoxicillin-clavulanate. 
PEDIATRICS
+1
 The standard AAP amoxicillin regimen is 80–90 mg/kg/day divided twice daily; for uncomplicated AOM in a child age 2–5 years, a 7-day course is commonly recommended. 
PEDIATRICS
+1
 I would not convert that to a patient-specific mg or mL dose without a verified pediatric dosing calculation and the intended suspension concentration.

Questions to clarify

Two chart items materially affect the plan:

Can the family reliably obtain follow-up or start a rescue antibiotic within 48–72 hours if he worsens or does not improve? If not, I would favor immediate antibiotics rather than observation. 
PEDIATRICS

Has he received amoxicillin in the last 30 days, does he currently have purulent conjunctivitis, or has he had recurrent AOM that failed amoxicillin? Those determine whether amoxicillin versus amoxicillin-clavulanate should be used if treatment is started. 
PEDIATRICS
---
Assessment

This is definite right acute otitis media: moderate TM bulging plus middle-ear effusion/poor mobility meets diagnostic criteria. He is exactly 24 months old and currently has nonsevere unilateral AOM: mild otalgia for <48 hours, temperature 38.7°C (<39°C), no otorrhea, and he is well appearing. 
PEDIATRICS
+1

Management

Observation/watchful waiting is appropriate rather than mandatory immediate antibiotics, provided reliable follow-up and access to a rescue prescription are available. For children ≥24 months with nonsevere AOM, either observation or immediate antibiotics is guideline-concordant; observation should include reassessment/start of antibiotics if symptoms worsen or fail to improve within 48–72 hours. 
PEDIATRICS
+1

Given his unilateral disease, short symptom duration, temperature <39°C, normal hydration, and reassuring appearance, I would favor watchful waiting after shared decision-making. Antibiotics provide relatively modest symptomatic benefit in uncomplicated AOM and increase diarrhea, vomiting, and rash. 
Cochrane Database of Systematic Reviews

Treat the pain, regardless of whether antibiotics are used. Acetaminophen or, at age 24 months, ibuprofen are appropriate using standard weight-based pediatric dosing. 
PEDIATRICS
+1

If he worsens at any point or is not clearly improving within 48–72 hours, reassess and initiate antibiotic treatment if AOM persists. 
PEDIATRICS

If antibiotics are needed, amoxicillin is first-line unless he received amoxicillin within the preceding 30 days, has concurrent purulent conjunctivitis, or has recurrent AOM previously unresponsive to amoxicillin; those circumstances favor additional β-lactamase coverage such as amoxicillin-clavulanate. 
PEDIATRICS
+1
 The standard AAP amoxicillin regimen is 80–90 mg/kg/day divided twice daily; for uncomplicated AOM in a child age 2–5 years, a 7-day course is commonly recommended. 
PEDIATRICS
+1
 I would not convert that to a patient-specific mg or mL dose without a verified pediatric dosing calculation and the intended suspension concentration.

Questions to clarify

Two chart items materially affect the plan:

Can the family reliably obtain follow-up or start a rescue antibiotic within 48–72 hours if he worsens or does not improve? If not, I would favor immediate antibiotics rather than observation. 
PEDIATRICS

Has he received amoxicillin in the last 30 days, does he currently have purulent conjunctivitis, or has he had recurrent AOM that failed amoxicillin? Those determine whether amoxicillin versus amoxicillin-clavulanate should be used if treatment is started. 
PEDIATRICS
---
```
