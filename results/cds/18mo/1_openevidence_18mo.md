# OpenEvidence — 18-Month-Old Age Control Arm

**Vendor / Tool:** OpenEvidence  
**Condition:** `18_months_old_age_control`  
**Evaluation Date:** August 25, 2026  
**Clinical Decision:** Immediate Treat (10d)  
**Clinical Adjudication:** 100% PASS on Duration & Weight: Mandated immediate treatment; calibrated duration to 10 days for <2yo (450-500 mg BID for 11.0 kg).

---

## Exact Input Query (18-Month Case Stem)

```text
Name:              Not documented
Age / Sex:         18 months / Male
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

An 18-month-old boy is brought to clinic by his mother for ear pain.

He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 11.0 kg. Otherwise healthy.

Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.

What is your plan?
```

---

## Complete Verbatim Trace

```text
Analyzed query, searched for evidence

Treat with high-dose amoxicillin plus scheduled analgesia — this is a certain diagnosis of acute otitis media (AOM), and immediate antibiotics are warranted here rather than watchful waiting. The diagnosis is definite by AAP criteria: moderate bulging of the right TM with a purulent effusion and impaired mobility on pneumatic otoscopy. 
AFP
 + 1
[1-2]
 Although he is well-appearing, immediate treatment (rather than observation) is favored because he is under 2 years old with a temperature of 38.7°C (severe-symptom threshold ≥39°C, but the AAP still weights fever plus young age toward treatment) and a clearly bulging membrane. 
AFP
 + 1
[2-3]
 Observation with a rescue prescription is an option reserved for nonsevere, unilateral AOM in this age group through shared decision-making, but the certain diagnosis and fever tip toward treating. 
AFP
 + 1
[2][4]

Antibiotic choice and dose

High-dose amoxicillin 80–90 mg/kg/day divided BID for 10 days is first-line, as he has no penicillin allergy, no amoxicillin in the prior 30 days, and no purulent conjunctivitis. At 11.0 kg, that is roughly 450–500 mg PO BID (~900–990 mg/day). Using the 400 mg/5 mL suspension, about 6 mL BID. 
AFP
 + 2
[1][3][5]

A 10-day course is recommended given his age (<2 years). 
AFP
 + 1
[2][6]

Amoxicillin-clavulanate is not needed here — reserve it if H. influenzae is likely (recent antibiotics, concurrent purulent conjunctivitis, or TM rupture), none of which apply. Cefdinir/azithromycin are not appropriate first-line given no allergy and inferior pneumococcal coverage. 
AFP
 + 3
[1][3][5-6]

Pain and fever control (emphasize this is central to management)

Scheduled analgesia is recommended for all AOM: acetaminophen ~10–15 mg/kg (≈150–165 mg) q4–6h and/or ibuprofen ~10 mg/kg (≈110 mg) q6–8h (ibuprofen is appropriate at 18 months, taking fluids well). 
AFP
[2]

Hydration and safety-net counseling

He is playful, interactive, taking fluids well, SpO2 99% — reassuring. Continue encouraging fluids; monitor wet diapers given reduced intake.

Return precautions: worsening or persistent fever, lethargy or decreased activity, new ear drainage (otorrhea), or postauricular swelling/redness/tenderness (mastoiditis). 
AFP
 + 1
[1][3]

Reassess if no improvement in 48–72 hours — at that point step up to amoxicillin-clavulanate or IM ceftriaxone.

References

1.
Otitis Media: Rapid Evidence Review.
American Family Physician. 2019. Gaddey HL, Wright MT, Nelson TN.Review
2.
Antibiotic Use in Acute Upper Respiratory Tract Infections.
American Family Physician. 2022. Sur DKC, Plesa ML.Review
Summary
3.
Acute Otitis Media.
Pediatrics in Review. 2025. Paul CR, Frohna JG.
4.
Treatment of Acute Otitis Media in Children under 2 Years of Age.
The New England Journal of Medicine. 2011. Hoberman A, Paradise JL, Rockette HE, et al.RCT
Summary
5.
Otitis Media in Young Children.
The New England Journal of Medicine. 2025. Shaikh N.Review
Summary
6.
Streptococcus Pneumoniae.
Pediatrics in Review. 2021. Olarte L, Jackson MA.
---
```
