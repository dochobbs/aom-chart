# LinkedIn draft 2 — the judge post. Do not post without review.

Register 6. Companion to the main post; can run a few days after it. Repo is currently private — re-publicize or cut the link line before posting.

---

Follow-up to the ear-infection eval: the grader flunked the same question it was grading.

The case is a 24-month-old with a one-sided ear infection. The AAP age bands are 6–23 months and 24-plus. Twenty-four months lands in the second band. That cusp is the trap in the case, and it's there on purpose.

Sonnet fell in: it called the stated 24-month-old "under 2" on 12 of 14 answers, then cited AAP as if antibiotics were required.

So I did the responsible thing and had a second model re-grade all 140 answers. Different lab, standard LLM-as-judge setup, full codebook in the prompt.

The judge read answers that said "24 months, <2 years" — verbatim — and coded the age band as correct on 11 of 14. It fumbled the exact cusp it was there to catch.

What settled it wasn't a third model. It was the quote. Pull the sentence, put it next to the code, and a human can adjudicate twelve rows in ten minutes. Two frontier models disagreed; a grep ended the argument.

I'll keep using a judge model — it caught real misses the first scorer slept through, including an answer that flatly asserted "reliable follow-up available" out of thin air. But LLM-as-judge is a second opinion, not verification. If your eval matters, every disputed judgment has to resolve to a quote a human can read.

The judge needs the same guardrails as the student.

Stem, traces, and the full adjudication trail: [repo link — private for now]

---

**Numbers cross-checked against `results/smoke_20260815T160303Z_tiebreak.md`:** Sonnet under-2 12/14; judge miscoded 11/14; 140 rows; Haiku "reliable follow-up available" caught by the buddy, upheld in tiebreak.
