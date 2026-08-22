# Error origins — Doc's three roots, verified

Where LLM misbehavior comes from: (1) training data, (2) RLHF/post-training, (3) prompting. All citations source-verified 2026-08-22. Companion to `human_parallels.md` (what the errors look like) and `combination_lit.md` (what happens when you pair them with us).

## Root 1 — the training data (mostly us)

| Finding | Citation |
|---|---|
| Four commercial LLMs propagated debunked race-based medicine: endorsed race-corrected eGFR with discredited muscle-mass claims; **all models repeated the skin-thickness myth**. The question set was derived from misconceptions documented in medical trainees — i.e., the same false-belief items as Hoffman 2016. The models repeat what half the trainees believed. | Omiye et al., *npj Digital Medicine* 2023 |
| Our own demonstration: Haiku's 45 mg/kg is the pre-2004 literature speaking; the copy-forward chart style (Thornton 82%) is the corpus the models learned documentation from. | This packet |

## Root 2 — post-training (we rewarded confident completeness)

| Finding | Citation |
|---|---|
| Sycophancy is a general behavior of state-of-the-art assistants, and preference data drives it: matching the user's views is among the most predictive features of human preference judgments. Humans reward agreeable and convincing over correct. | Sharma et al. (Anthropic/Oxford), arXiv 2310.13548, 2023 |
| Formal argument that hallucination is incentivized by evaluation itself: virtually all major benchmarks use binary scoring that gives zero credit for "I don't know," making guessing strictly dominant over abstaining. Models are optimized to be good test-takers. | Kalai, Nachum, Vempala, Zhang (OpenAI), "Why Language Models Hallucinate," arXiv 2509.04664, 2025 |
| The pretrained GPT-4 model was well calibrated (confidence tracked probability of correctness); post-training/RLHF **reduced** calibration. Confident wrongness is partly an alignment artifact, not a base-model property. | GPT-4 Technical Report (OpenAI), 2023 |

## Root 3 — prompting (the untested deployment layer)

| Finding | Citation |
|---|---|
| Trivial, meaning-preserving prompt-format changes swing task accuracy by **up to 76 points**; sensitivity persists with model scale and instruction tuning. Single-prompt evaluation is methodologically shaky, and single-prompt deployment inherits the same fragility. | Sclar, Choi, Tsvetkov, Suhr, ICLR 2024 (arXiv 2310.11324) |
| The positive direction of the same lever: one ask-don't-assume sentence cut invented-premise answers 24/56 → 6/56 with plans intact. | This packet (`results/smoke_20260815T214553Z_notes.md`) |

## How the roots map to our findings

- **Root 1** explains the stale dose, the copy-forward habit, and the bias-in-justifications (Omiye closes the loop: trainee misconceptions → training text → model output).
- **Root 2** explains the completeness aesthetic (thorough models invented most), the flat confidence, and why "I don't know" almost never appears unprompted: we graded it out of them.
- **Root 3** explains both the disease severity in deployment (nobody tests the prompt) and the cheapness of the fix (the same sensitivity that makes formatting swing 76 points makes one honest sentence swing fabrication fourfold).

## Refutability notes

Omiye: peer-reviewed, small scenario set (8), direction heavily replicated since. Sharma: arXiv but Anthropic-authored with released data; widely cited. Kalai 2025: formal argument + benchmark audit, arXiv; treat the theorem as argument, the benchmark audit as data. GPT-4 calibration: single figure in a vendor technical report; quote as the vendor's own finding. Sclar: ICLR peer-reviewed; note the 76-point figure is open-weights models in few-shot settings, not frontier chat models — quote as sensitivity evidence, not a frontier-model rate.

## References

1. [Omiye — npj Digital Medicine 2023](https://www.nature.com/articles/s41746-023-00939-z)
2. [Sharma — arXiv 2310.13548](https://arxiv.org/abs/2310.13548)
3. [Kalai — arXiv 2509.04664](https://arxiv.org/abs/2509.04664)
4. [GPT-4 Technical Report](https://arxiv.org/pdf/2303.08774)
5. [Sclar — arXiv 2310.11324](https://arxiv.org/abs/2310.11324)
