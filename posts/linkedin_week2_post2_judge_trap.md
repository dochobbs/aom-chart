# LinkedIn Post 2 (Week 2): The Evaluator Trap

*Part 2 of the "Compared to Whom?" series.*

---

The grader flunked the same question it was grading.

In our pediatric benchmark, the test case was a 24-month-old with a one-sided ear infection. The AAP age bands are 6 to 23 months and 24-plus. Twenty-four months lands in the second band. That cusp is the trap in the case, and it is there on purpose.

Claude Sonnet fell in: it called the stated 24-month-old "under 2" on 12 of 14 answers, then cited the AAP for a non-existent rule mandating antibiotics.

So I ran a standard LLM-as-judge pipeline to re-grade all 140 answers. A different frontier model from a different lab family, with the full clinical codebook in the prompt.

The judge read answers that said "24 months, <2 years" verbatim and coded the age classification as correct on 11 of 14 traces. It fumbled the exact cusp it was there to catch.

Automated scoring failed in both directions. Simple regex screening flagged 48 answers as asserting reliable follow-up when 37 of them were actually proper conditionals ("requires reliable follow-up, confirm with parent"). The judge also generated 85 false-positive flags for demographic bias by counting generic clinic boilerplate that appeared evenly across control and experimental cells.

What settled it was not a third judge model. It was the quote. Pull the verbatim sentence, place it next to the codebook, and a human can adjudicate twelve rows in ten minutes. Two frontier models disagreed; a grep ended the argument.

LLM-as-a-judge is a useful second opinion, but it is not verification. If your evaluation matters, every disputed judgment has to resolve to a quote a human can read.

Stem, traces, and the full adjudication trail: https://github.com/dochobbs/aom-chart
