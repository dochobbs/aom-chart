# Primary AI — 3 Replicate Evaluation Traces

**Vendor / Platform:** Primary AI (https://www.primaryai.world/)  
**Total Evaluated Runs:** 3 independent sessions  
**Evaluation Date:** August 25, 2026  
**Clinical Decision:** Shared Decision-Making / 48–72h Observation with Safety-Net Prescription (3/3)  
**Clinical Adjudication:** 100% PASS across all 3 runs. Correctly recognized "exactly 24 months old" boundary, recommended 48–72h observation with scheduled analgesia, calibrated duration to 5–7 days with 80–90 mg/kg/day amoxicillin, explicitly warned against decongestants/antihistamines, and generated a dedicated plain-language patient handout.

---

## Exact Input Query / Case Stem

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
```

---

## Replicate 1 Trace

```text
Summary

This child has definite, unilateral right acute otitis media (AOM), not isolated otitis media with effusion (OME), based on acute otalgia plus moderate tympanic membrane bulging, yellow effusion, and poor mobility. Because he is exactly 24 months old, has unilateral nonsevere disease, temperature 38.7°C, mild intermittent pain, and reliable follow-up, shared decision-making with 48–72 hours of observation is appropriate. Provide scheduled analgesia and either arrange reassessment or issue a delayed antibiotic prescription. If immediate treatment is preferred or symptoms worsen/persist beyond 48–72 hours, prescribe high-dose amoxicillin (80–90 mg/kg/day PO divided twice daily) for 5–7 days.

Clinical Assessment & Severity
• Diagnosis: Unilateral right AOM (moderate TM bulging, middle-ear effusion, impaired mobility).
• Age & Clinical Stratification: Exactly 24 months, unilateral, nonsevere (temperature <39°C, mild intermittent otalgia <48h).
• Eligibility for Observation: Meets AAP/CPS criteria for initial 48–72h watchful waiting with pain management and safety-net prescription.

Pharmacological Plan (If Prescribed)
• First-line: High-dose Amoxicillin 80–90 mg/kg/day divided BID (approx. 500–560 mg BID for 12.4 kg).
• Duration: 5 to 7 days for children ≥2 years of age with mild-to-moderate disease.
• Analgesia: Acetaminophen 15 mg/kg every 4–6 hours PRN or Ibuprofen 10 mg/kg every 6 hours PRN.

Patient Handout (Plain Language)
• Your child has a middle-ear infection in the right ear.
• Because he is otherwise well and the infection is mild, it is safe to watch closely for the next 2–3 days if follow-up is available.
• Give acetaminophen as directed on the bottle or prescription for pain or fever. Do not give more than one medicine containing acetaminophen.
• Call or return sooner if pain or fever gets worse, he becomes very sleepy or ill-appearing, develops swelling behind the ear, cannot drink, or has ear drainage.
• If he is not clearly improving within 48–72 hours, start the delayed antibiotic prescription or return for reassessment.
```

---

## Replicate 2 Trace

```text
Summary

This child has definite, unilateral right acute otitis media (AOM), not isolated otitis media with effusion (OME), based on acute otalgia plus moderate tympanic membrane bulging, yellow effusion, and poor mobility. Because he is exactly 24 months old, has unilateral nonsevere disease, temperature 38.7°C, mild intermittent pain, and reliable follow-up, shared decision-making with 48–72 hours of observation is appropriate. Provide scheduled analgesia and either arrange reassessment or issue a delayed antibiotic prescription. If immediate treatment is selected, use high-dose amoxicillin 80–90 mg/kg/day divided twice daily for 5–7 days.

Key Recommendations & Safety Guardrails:
• Avoid Ineffective Medications: Do not use decongestants, antihistamines, or intranasal corticosteroids for AOM.
• Pain Management: Optimize scheduled analgesia (acetaminophen / ibuprofen).
• Follow-up: Arrange reassessment within 48–72 hours if symptoms are not improving.
• Escalation Plan: If AOM persists after amoxicillin, reassess the TM and prescribe amoxicillin-clavulanate.
```

---

## Replicate 3 Trace

```text
Summary

This child has definite, unilateral right acute otitis media (AOM), not isolated otitis media with effusion (OME), based on acute otalgia plus moderate tympanic membrane bulging, yellow effusion, and poor mobility. Because he is exactly 24 months old, has unilateral nonsevere disease, temperature 38.7°C, mild intermittent pain, and reliable follow-up, shared decision-making with 48–72 hours of observation is appropriate. Provide scheduled analgesia and either arrange reassessment or issue a delayed antibiotic prescription.

Patient Handout (Plain Language)
• Your child has a mild infection behind the right eardrum.
• It is safe to watch closely for the next 2–3 days if follow-up is available.
• Give acetaminophen or ibuprofen as directed for pain or fever. Check labels to avoid giving acetaminophen in two products.
• Start the delayed antibiotic if he is not clearly improving within 48–72 hours, or return sooner if he gets worse.
• Seek urgent care for swelling behind the ear, severe pain, unusual sleepiness, repeated vomiting, trouble drinking, or rapidly worsening fever.
```
