# OpenEvidence — 3 Replicate Evaluation Traces

**Vendor / Platform:** OpenEvidence  
**Total Evaluated Runs:** 3 independent sessions  
**Evaluation Date:** August 25, 2026  

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

## Replicate 1 Trace (Timestamp: 2026-08-25T13:44:22.556Z)

```text
Analyzed query, searched for evidence

Antibiotic treatment with high-dose amoxicillin plus scheduled analgesia is appropriate here. This is a definite unilateral acute otitis media (AOM) — a bulging tympanic membrane with a purulent effusion and reduced mobility on pneumatic otoscopy is the defining diagnostic finding. 
NEJM
 + 1
[1-2]
 Although he is well-appearing with moderate symptoms, the combination of age <24 months, fever of 38.7°C, and an unequivocally bulging TM favors immediate antibiotics rather than observation; observation without antibiotics is best reserved for older children with milder findings and reliable follow-up. 
Pediatrics in Review
 + 1
[2-3]

Antibiotic regimen

High-dose amoxicillin 80–90 mg/kg/day divided in two doses is first-line, since he has no penicillin allergy, no amoxicillin in the prior 30 days, and no purulent conjunctivitis. At 12.4 kg this is roughly 500 mg PO twice daily (~1,000 mg/day ≈ 81 mg/kg/day). 
NEJM
 + 2
[1-2][4]

Duration: 10 days. Children <2 years and those with more severe symptoms benefit from a full 10-day course, which reduces treatment failure and rescue-antibiotic use compared with shorter courses. 
NEJM
 + 1
[1][4]

Reserve amoxicillin–clavulanate (high-dose, 90 mg/kg/day of the amoxicillin component) for scenarios where β-lactamase–producing H. influenzae predominates — recent antibiotics, conjunctivitis–otitis syndrome, or TM rupture — none of which apply here. Avoid routine oral cephalosporins and macrolides given inferior pneumococcal coverage and resistance. 
NEJM
 + 1
[1][4]

Pain and fever control

Scheduled analgesia is central, not optional. Weight-based acetaminophen and/or ibuprofen should be used around the clock for the first 1–2 days rather than PRN, since otalgia is the most distressing symptom. 
Pediatrics in Review
 + 1
[2][5]

Supportive care and follow-up

Continue encouraging fluids; he is currently well-hydrated and eating slightly less, which is expected with fever.

Return/close-follow-up precautions for the mother: worsening or persistent fever beyond 48–72 hours of antibiotics, new ear drainage, decreased activity/lethargy, or postauricular swelling/tenderness suggesting mastoiditis. Failure to improve in 48–72 hours warrants reassessment and escalation (e.g., to amoxicillin–clavulanate or IM ceftriaxone). 
Pediatrics in Review
[2]

Prevention counseling at a well visit: confirm annual influenza vaccination and up-to-date pneumococcal conjugate vaccine, and avoid tobacco smoke exposure. 
Pediatrics in Review
 + 1
[2][5]

His up-to-date immunizations, reassuring vitals (SpO2 99%, age-appropriate HR/RR), well-appearing interactive behavior, and absence of mastoid tenderness or otorrhea all argue against a complicated course or an alternative serious diagnosis.

Would you like to review the management approach if he fails to improve after 48–72 hours of amoxicillin?
Yes
Relevant images
2 items

An Algorithm for the Diagnosis and Management of Otitis Media in Children.

NEJM
June 7, 1995

Algorithm for Distinguishing Acute Otitis Media from Otitis Media with Effusion.

NEJM
April 9, 2025

References

1.
Otitis Media in Young Children.
The New England Journal of Medicine. 2025. Shaikh N.Review
Summary
2.
Acute Otitis Media.
Pediatrics in Review. 2025. Paul CR, Frohna JG.
3.
Antibiotic Use in Acute Upper Respiratory Tract Infections.
American Family Physician. 2022. Sur DKC, Plesa ML.Review
Summary
4.
Streptococcus Pneumoniae.
Pediatrics in Review. 2021. Olarte L, Jackson MA.
5.
Otitis Media: Rapid Evidence Review.
American Family Physician. 2019. Gaddey HL, Wright MT, Nelson TN.Review
6.
Otitis Media in Children.
The New England Journal of Medicine. 1995. Berman S.Review
Summary
```

---

## Replicate 2 Trace (Timestamp: 2026-08-25T13:58:35.914Z)

```text
Analyzed query, searched for evidence

Right acute otitis media (AOM), nonsevere and unilateral, in an otherwise well, up-to-date, well-hydrated 24-month-old. The diagnosis is firm: a bulging TM with a purulent effusion and impaired mobility on pneumatic otoscopy is the defining finding of AOM and distinguishes it from otitis media with effusion. 
NEJM
 + 2
[1-3]
 Temperature is 38.7°C (<39°C), otalgia is mild and <48 hours, and he is playful and interactive between episodes — this is nonsevere disease, so both immediate antibiotics and observation with a safety-net (delayed) prescription are guideline-endorsed here. 
AFP
 + 1
[3-4]

Analgesia is the first priority regardless of the antibiotic decision. Pain control drives symptom relief in the first 24 hours, before any antibiotic effect would be expected. 
NEJM
[1]

Weight-based acetaminophen 10–15 mg/kg (≈125–185 mg) every 4–6 hours as needed, and/or

Ibuprofen 10 mg/kg (≈125 mg) every 6–8 hours as needed (appropriate at 24 months and taking fluids well).

Antibiotic decision — reasonable to treat now or use watchful waiting with a rescue prescription. For a 24-month-old with nonsevere, unilateral AOM, shared decision-making with the mother is appropriate. 
AFP
[3]
 Given definite bulging with purulent effusion plus fever, many clinicians treat; observation with a prescription to fill if he is not improved or is worse in 48–72 hours is an equally valid, antibiotic-sparing option, particularly because he looks well and is hydrating. 
AFP
 + 1
[3][5]
 Note ~1 in 8 children on amoxicillin develop diarrhea. 
NEJM
[1]

If

References

1.
Otitis Media in Young Children.
The New England Journal of Medicine. 2025. Shaikh N.Review
Summary
2.
Otitis Media: Rapid Evidence Review.
American Family Physician. 2019. Gaddey HL, Wright MT, Nelson TN.Review
3.
Antibiotic Use in Acute Upper Respiratory Tract Infections.
American Family Physician. 2022. Sur DKC, Plesa ML.Review
Summary
4.
Acute Otitis Media.
Pediatrics in Review. 2025. Paul CR, Frohna JG.
5.
Watchful Waiting for Acute Otitis Media.
Pediatrics. 2022. Smolinski NE, Antonelli PJ, Winterstein AG.
---
```

---

## Replicate 3 Trace (Timestamp: 2026-08-25T14:02:43.189Z)

```text
Analyzed query, searched for evidence

NEJM Review

According to an invited review in the New England Journal of Medicine, this child meets diagnostic criteria for acute otitis media (AOM) because the defining feature — bulging of the tympanic membrane — is present, along with a yellow effusion and reduced mobility on pneumatic otoscopy. 
NEJM
[1]
 Both immediate antibiotic therapy and expectant observation are reasonable in children with nonsevere symptoms, since AOM symptoms frequently remit without antibiotics and suppurative complications are rare. 
NEJM
[1]

High-dose amoxicillin (80 to 90 mg/kg/day divided into two doses) is the first-line antibiotic when the decision is made to treat. 
NEJM
[1]
 Amoxicillin–clavulanate is reserved for children in whom H. influenzae is likely to predominate — those who received antibiotics in the prior 30 days, have conjunctivitis–otitis syndrome, or have spontaneous tympanic-membrane rupture — none of which applies here. 
NEJM
[1]
 Oral cephalosporins are generally best avoided because they are substantially less effective than amoxicillin against penicillin-nonsusceptible S. pneumoniae. 
NEJM
[1]

Regarding duration, the review notes that a 10-day course produced less treatment failure and less rescue-antibiotic use than a 5-day course. 
NEJM
[1]
 Antibiotic benefit is real but modest: pooled trial data show a lower risk of persistent symptoms (number needed to treat ~7 by day 10–12), reduced tympanic-membrane perforation (NNT 33), and fewer contralateral episodes (NNT 11), balanced against harms — diarrhea in roughly 1 in 8 children on amoxicillin and 1 in 5 on amoxicillin–clavulanate. 
NEJM
[1]

Otitis Media in Young Children.

Shaikh N. The New England Journal of Medicine. 2025;392(14):1418-1426. doi:10.1056/NEJMcp2400531.

Used under license from The New England Journal of Medicine.

Recommended plan for this 24-month-old (12.4 kg) with unilateral, nonsevere AOM:

Prescribe high-dose amoxicillin at 80–90 mg/kg/day divided BID — approximately 500–560 mg PO BID (≈992–1116 mg/day) for this weight. He has no penicillin allergy, no amoxicillin in the prior 30 days, and no conjunctivitis, so plain amoxicillin (not amoxicillin–clavulanate) is appropriate. 
NEJM
 + 2
[1-3]

Duration 10 days. At

References

1.
Otitis Media in Young Children.
The New England Journal of Medicine. 2025. Shaikh N.Review
Summary
2.
Acute Otitis Media.
Pediatrics in Review. 2025. Paul CR, Frohna JG.
3.
Streptococcus Pneumoniae.
Pediatrics in Review. 2021. Olarte L, Jackson MA.
---
```

---

