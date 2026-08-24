# LinkedIn Post 3 (Week 2): Compared to Whom?

*Part 3 of the "Compared to Whom?" series.*

---

A colleague told me recently that she would never trust AI in medicine. "It hallucinates," she said. "It just makes things up."

She is right. It does. In our pediatric benchmark, frontier models fabricated chart facts 41% of the time, applied a dosing standard that died in 2004, and misread an age cutoff.

If you stop there, you would never let these systems near a clinic. But that benchmark assumes a comparison to an imaginary doctor who never makes a mistake.

The human side has forty years of literature we rarely talk about.

In real outpatient clinics, pediatricians prescribe antibiotics for acute ear infections 80% to 86% of the time (CDC and RAND data), even though guidelines say roughly half can be safely observed. Across US medicine, adult patients receive only 55% of recommended care. And in diagnostic studies, physician confidence stays pegged at 7 out of 10 even when diagnostic accuracy drops from 55% down to 6%.

Humans fail under time pressure by forgetting, skipping steps, and not knowing when they are wrong. Language models fail by over-completing the chart, dragging forward old pre-training data, and guessing when unconstrained.

On the exact same case where models fabricated missing history, their omission rate for safety essentials was 2.1% (3 of 140 traces). They offered watchful waiting and shared decision-making far more readily than busy clinics. And when given a single sentence to flag missing chart data, unprompted fabrication dropped by three-quarters.

The goal is not an imaginary flawless doctor. It is pairing human judgment with software constraints designed around the failure modes of both.

The full anchor essay, raw data, and code: https://github.com/dochobbs/aom-chart
