# The combination literature — AI alone vs doctor alone vs doctor+AI

Evidence bank for the synergy thesis. All citations source-verified 2026-08-22. Companion to `human_parallels.md`.

**The thesis these support:** untrained doctors + unprompted AI is additive at best. Designed collaboration — trained humans, AI prompted to expose its assumptions, the right division of labor — is where synergy has actually been demonstrated. Nobody has tested both levers at once.

## The uncomfortable baseline: adding the doctor can subtract

| Finding | Numbers | Citation |
|---|---|---|
| **LLM alone beat physicians who were using the LLM.** Diagnostic-reasoning RCT, 50 physicians, clinical vignettes. | LLM alone median **92%**; physicians + LLM **76%**; physicians + conventional resources **74%**. LLM-alone advantage over control: 16 points (P=.03); the assist added 2 n.s. points | Goh et al., *JAMA Network Open* 2024 |
| **On average, human–AI combos perform worse than the best of either alone.** Pre-registered meta-analysis: 106 studies, 370 effect sizes. | Significant net loss vs best-alone; losses concentrate in **decision** tasks, gains in **creation** tasks. Direction is conditional: when human > AI alone, combos gain; when AI > human alone, combos lose | Vaccaro, Almaatouq & Malone, *Nature Human Behaviour* 2024 |

The Vaccaro conditional is the whole story in one line: in domains where the AI now outperforms the unaided human — which Goh suggests includes vignette diagnosis — naive combination *degrades* the AI. The human overrides the better answer.

## The proof synergy exists when the collaboration is designed

| Finding | Numbers | Citation |
|---|---|---|
| **Algorithm-assisted pathologists beat both the algorithm alone and pathologists alone.** Lymph-node mets, 6 pathologists, assisted vs unassisted crossover. | Higher accuracy than either alone; significantly higher sensitivity for micrometastases; assisted review also easier/faster | Steiner et al., *Am J Surg Pathol* 2018 |
| **AI support improved skin-cancer diagnosis beyond either alone — and HOW the support was represented mattered.** 302 physicians, dermatoscopy. | Good-quality support improved accuracy (multiclass probabilities: >10-point gain; better than image-retrieval representations); least-experienced clinicians gained most | Tschandl et al., *Nature Medicine* 2020 |
| **The same LLM that didn't help diagnosis DID help management.** Follow-up RCT, 92 physicians, open-ended management vignettes. | LLM-assisted physicians scored higher than conventional-resources physicians on management reasoning; more patient-centered responses | Goh et al., *Nature Medicine* 2025 |

Read together: synergy is real but *conditional* — on task type (management vs diagnosis), on interface/representation (Tschandl), on workflow design (Steiner), and on who holds the last word (Vaccaro). None of these trials trained the physicians in collaboration or prompted the AI to expose its assumptions. Both levers are still on the table.

## How this connects to our AOM data

- Our mitigation experiment is the **AI-side lever**: one sentence cut invented premises 24/56 → 6/56 with plans intact. Nobody prompted Goh's GPT-4 to say what it was assuming.
- Our turn-2 finding is the **human-side lever**: one question ("what missing information would change this plan?") surfaces the assumptions 97% of the time. A doctor trained to ask it interrogates the AI instead of rubber-stamping or overriding it.
- The judge finding is the warning label: unaided verification-by-expert is itself unreliable (Terra miscoding the cusp; Goldman's kappa 0.31). "The doctor will catch the AI's errors" assumes a catcher the data doesn't show.

**The testable hypothesis:** ask-don't-assume prompting (AI side) + interrogation training (human side) → doctor+AI > AI alone. Neither Goh trial tested either lever; the pathology/derm results say designed collaboration clears the bar. This is the study someone should run.

## References

1. Goh E, et al. Large Language Model Influence on Diagnostic Reasoning: A Randomized Clinical Trial. *JAMA Netw Open* 2024;7(10):e2440969. [jamanetwork/pmc](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11519755/)
2. Vaccaro M, Almaatouq A, Malone T. When combinations of humans and AI are useful: A systematic review and meta-analysis. *Nat Hum Behav* 2024;8:2293–2303. [nature.com](https://www.nature.com/articles/s41562-024-02024-1)
3. Steiner DF, et al. Impact of Deep Learning Assistance on the Histopathologic Review of Lymph Nodes for Metastatic Breast Cancer. *Am J Surg Pathol* 2018;42(12):1636–46. [pubmed](https://pubmed.ncbi.nlm.nih.gov/30312179/)
4. Tschandl P, et al. Human–computer collaboration for skin cancer recognition. *Nat Med* 2020;26:1229–34. [nature.com](https://www.nature.com/articles/s41591-020-0942-0)
5. Goh E, et al. GPT-4 assistance for improvement of physician performance on patient care tasks: a randomized controlled trial. *Nat Med* 2025. [nature.com](https://www.nature.com/articles/s41591-024-03456-y)

## Refutability notes

Goh 2024/2025: RCTs, but vignettes not live patients — quote as reasoning-task results, not patient outcomes. Vaccaro: pre-registered meta, the strongest single frame-setter. Steiner: small reader panel (6), crossover design, widely replicated direction in pathology CAD lit. Tschandl: 302 raters, but web-based experiment. All Tier 1–2 by the human_parallels audit standard; none excluded.
