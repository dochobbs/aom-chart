# Anchor essay — editorial and citation review

Reviewed 2026-08-29 against v5.4, then v5.5 and a “high-velocity” v6. Numbers in the essay were checked against the packet (`FINDINGS.md`, `STEM.md`) and the cited papers, not only against `human_parallels.md`.

Not a rewrite. Do not relabel 2026 models as 2024 models. Do not keep sanding the long honest draft.

## Version call

| Draft | Verdict |
|---|---|
| **v5.5 lineage** (`posts/compared_to_whom_v5.5.md`, and later `v7` / `final`) | Ship this family. Real model names, caveats on Densen and Morris, Hoffman kept, Goh 2024 reported as a median with CI. |
| **v6 “High-Velocity” (chat A)** | Do not ship. Mapped Fable-5 → “Claude 3.5 Sonnet (early build)” and Terra → GPT-4o. Stated the 73-day doubling and seventeen-year lag as measurements. v5.5 had already labeled both. |
| **Chat B (tight cut)** | Better *shape* for a first reader. Steal contractions back from v5.5; steal Hoffman; check Thornton authors before using B’s reference list. |

Hybrid if an editor demands a cut: B’s hierarchy, v5.5’s mouth and citations. Cut corroboration, not discovery. Keep: invented facts, they knew when asked, one sentence, 92 vs 76, combination has to be designed.

## Packet facts the essay must not invert

Chart (`docs/STEM.md`): no 30-day antibiotic history, no follow-up reliability, **“No drug allergies.”** Conjunctivitis is at most inferred from an unremarkable exam.

v5.4 said “two of those three facts are in the chart. The middle one is invented.” Wrong. One of three is in the chart (allergy). The first fact (no recent amoxicillin) is invented, and that is the premise that picks amoxicillin over amox-clav.

Fable was the heaviest inventor (13/14) and was not in the mitigation rerun. Say **“four worst reachable inventors,”** not “four heaviest.”

Judge error is **11/14 Sonnet rows**, not 11/14 of the 140.

Turn-2 97% is **192 traces**, not the 140.

CDS: **seven named platforms** in the body; Primary AI exists in `results/` as an eighth. If the footer says eight, say the eighth was added later.

Haiku invention **5/14** in the adjudicated 140; **2/14** on the mitigation-baseline rerun (regex, same 14-trace grid). Both can stay if the rerun is named.

Prescription-null lives in the **identity pairs**, not as `0/140`. Current wording: “0 (no prescription shifted in any demographic arm).”

## Citations that were wrong in v5.4 (fixed in v5.5)

| v5.4 cite | Problem | Use |
|---|---|---|
| Wingfield *Am J Hypertens* 2006;19(2):147–152 | That pagination is **Nietert PJ, Wessell AM, Jenkins RG, et al.** Zero recorded 44.6% SBP / 47.5% DBP. Wingfield has earlier TDP papers. | Nietert 2006 |
| Porter J, Choi Y, *JGIM* 2022;37(13):3555–3561 | Wrong title, second author, volume/pages. 26.7 hours is correct. | **Porter J, Boyd C, Skandari MR, Laiteerapong N.** Revisiting the Time Needed to Provide Adult Primary Care. *J Gen Intern Med.* 2023;38(1):147–155 (epub 2022). |
| Cabitza *Front Digit Health* 2021;3:698380 | DOI 404s. Sentence was written for a paper that does not exist. | Cabitza, Rasoini, Gensini, *JAMA* 2017;318(6):517–518 — deskilling / overreliance / black box, **not** “cognitive ergonomics.” Hang it on handing a doctor a chatbot, not on interface design. Jacobs *Transl Psychiatry* 2021;11:108 carries the recommendation-influence claim. |
| Jacobs *Proc ACM Hum-Comput Interact* 2021 | Wrong venue and title. | Jacobs et al. How machine-learning recommendations influence clinician treatment selections. *Transl Psychiatry.* 2021;11:108. |
| Lieberthal “Reaffirmed 2024” | No AAP 2024 reaffirmation paper found. CPS reaffirmed *its* AOM statement 21 Nov 2024. | Lieberthal 2013 without the reaffirmation clause, unless AAP’s CPG list is rechecked. |

**Goldman [essay 1994 *Eval Health Prof*] is the correct paper for κ = 0.31** (21 findings, 13 studies). The internal bank had been pointing at Goldman 1992 *JAMA*, which is the earlier narrative review and does not carry that pooled kappa in the abstract. Keep 1994 in the essay; the bank is corrected in `human_parallels.md`.

**Doherty C, Mc Donnell C.** *Pediatrics* 2012;129(5):916–924 is correct in the essay. The bank’s “Doig” was a bank error.

## Load-bearing numbers that checked

Berdahl 38.5 / 53.2; Dresselhaus 16% undercount; Shenoy ~10% labeled, >9/10 not allergic; Thornton 82%; Prasad 40.2%; Fleming-Dutra ~30%; Borden 43.5 → 44.7; Olenski ~24% relative CABG drop (7.0% vs 5.3%); Alper ~29 h/weekday (epidemiologist review time for a knowledge base); McGlynn 54.9%; Porter 26.7 h; Baethge 16.9%; Goh 2024 medians 76 / 74 / 92 (3 LLM-alone runs); Goh 2025 +6.5 points (43.0 vs 35.7); Vaccaro 106 experiments, 370 effect sizes; Tu AMIE 159 scenarios, *Nature* 2025;642:442–450. OpenEvidence quotes match the raw dump.

Densen 73-day and Morris 17-year: keep the v5.5 warning labels. Morris is a paper *against* a single universal lag.

## Soft citations (not false)

Lingard 2003 / Irby 2004 do not say “if you corner a trainee.” Irby is one-minute preceptor (commit, then probe). Current v5.5 paraphrase — probing reasoning, making uncertainty discussable — is fair.

Croskerry 2003 does not say “curiosity is the antidote to hubris.” That line is the author’s. v5.5 already moved uncertainty to Simpkin.

## What a first reader will remember

Invented follow-up line. 41% → 11% with one sentence. Stanford 76 / 74 / 92. Compared to whom.

Section 2 still testifies after the point is granted. Armor for a hostile reader; fatigue for a first reader. That is a tradeoff, not an unfinished fix. If cutting: keep penicillin-allergy label, 80th-birthday CABG, 26.7-hour day. Drop the memory/citation laundry list first.
