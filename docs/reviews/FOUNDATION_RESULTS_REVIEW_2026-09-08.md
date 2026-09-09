# Foundation-model results review

Michael David Hobbs, MD — September 8, 2026

**Assessment: specific numerical claims need revision. The saved outputs and selected clinical examples remain useful.** The recent audit supplied in chat correctly identifies missed positive LOC fabrication, but its counts, completeness assurance, and description of completed repairs are not fully supported by this checkout.

The public-package memo is substantially more qualified than the earlier research memo. It already rejects a universal cure, treats Sonnet's 8/10 as provisional, distinguishes supplied CAP immunizations from fabrication, and labels three incomplete answers. It needs a focused correction to the initial factorial result and a qualification of the August mitigation comparison. The earlier research memo needs more extensive revision. Which PDF was actually emailed was not established during this review; no email was accessed or sent.

## Scope and method

This review inventories every JSON file in the 17 result folders that reproduce the supplied 1,778 count; checks duplicate texts, answer fields, metadata, and response endings; inspects runner and scoring logic; reviews the disputed factorial and Haiku examples in context; and reconciles the findings with both memo versions and the current ZIP. It also checks the August files that the supplied audit specifically describes as sound.

This is **not a new blinded clinical adjudication of all answers**, an independent verification of provider request logs, or a re-evaluation of PEARL/CDS-eval. The review assigns no replacement overall clinical pass rates. Dates are those in files or filenames where present; several small experiments lack embedded execution timestamps. Original responses, scripts, reports, PDFs, and the ZIP were preserved.

Artifacts:

- [Reproducible audit script](audit_foundation_records.py) and [notebook](FOUNDATION_RECORD_AUDIT_2026-09-08.ipynb).
- [Record inventory and source hashes](FOUNDATION_RECORD_INVENTORY_2026-09-08.json).
- [Recomputed counts and duplicate map](FOUNDATION_VALIDATION_2026-09-08.json).
- [41 verified source excerpts](FOUNDATION_EVIDENCE_2026-09-08.json), identified below as F01–F41.
- [Target-specific review of nine factorial and ten Haiku answers](FOUNDATION_TARGET_REVIEW_2026-09-08.json). A negative target finding is not a whole-answer pass.
- [Package source-row checks](FOUNDATION_PACKAGE_CHECK_2026-09-08.json). Relevant passages were also checked in text extracted from both PDFs; their layouts were not newly reviewed.

## 1. What the capture records establish

| Supplied audit claim | Finding from disk | Appropriate interpretation |
| --- | --- | --- |
| 1,778 traces across 17 battery runs | **1,778 stored rows across 17 folders** reproduces exactly. **192 rows are duplicate master/component copies**, leaving **1,586 distinct text records**. | Folder count is not run count. Distinct text records are not independently authenticated API calls. |
| Every trace complete; none empty | One Sonnet first-turn answer is empty. Multiple Opus answers end mid-word or mid-sentence. | Saved text availability and generation completeness need separate fields. |
| All calls retain tokens, latency, full API response | After text deduplication, 2,758 answer fields are represented. All lack retained stop reasons; 350 lack output-token fields and 340 lack latency fields under the saved schemas. The callers extract answer text and selected metadata. | These are extracted response records, not full API-response archives. Separate thinking blocks and request/response identities are generally not retained. |
| No API errors | No nonempty `error` field was found in the selected rows; 636 distinct records have no `error` field. | No recorded errors is supported. No failed attempts or exhausted retries is not established by this corpus. |
| All use native vendor SDK endpoints, including xAI | Native OpenAI, Anthropic and Google callers exist. Fable and Grok are configured through **OpenRouter**, using the OpenAI-compatible client. | Preserve configured provider and model identifier. Do not claim all were direct native-vendor calls. |
| Mean length ~3,700; multi-turn minimum 1,523 | On the defined deduplicated answer-field denominator, mean length is **3,295.8 characters**, minimum nonempty answer **481**, plus one empty answer. | The supplied length metric has no reproducible denominator. Counting combined conversations produces a different quantity. |

The 192 copies are fully accounted for: 120 compound-prompt records appear both in the master and the three replicate files; 72 head-factorial records appear in both the combined master and its 48-record/24-record components. This is ordinary aggregation, but counting both as new generations inflates the corpus count.

The 17-folder selection also omits `results/mantra_smoke/canary_smoke_1788785688.json`, which contains 16 additional records. Its filename encodes a September 7 timestamp; it lacks request-level timestamps. Thus 1,778 is not a demonstrated exhaustive total for all September activity.

**Concrete capture exceptions:**

- **F18:** `mitigation_4cases_20260907T030903Z.json`, `results[34]`, Sonnet/seizure: `t1_text` is empty, `t1_tokens` is 4000, and `error` is null. Its second answer exists. Do not classify the absent first answer as an absence of clinical errors.
- **F15–F17:** In the 92-record validation, Opus head-injury replicates 1, 4 and 3 end respectively in “and sh”, “130 mg (”, and “confusion, se”. Each records 4000 output tokens. These are visible incomplete endings; the exact provider stop cause is not retained.
- **87 deduplicated answer fields** record exactly 4000 output tokens. This is a screening count, **not** 87 adjudicated truncations. High-thinking runs use different budgets, and some answers at a limit end at a sentence boundary.

The synchronous API design avoids browser-scraping problems. It does not by itself establish that an answer completed or that the entire API response was saved. See F33/F40 and `eval/run.py`.

## 2. The two disputed confabulation results

### Haiku in the 92-record validation

**The six positive-LOC examples are confirmed**: experiment 1, Haiku replicates **2, 6, 7, 8, 9 and 10** (F02–F07). The answers treat LOC as present or implied by a thud, crying, or finding the child. The input supplies none of those as evidence of LOC. Replicate 6 also invents initial unresponsiveness and a fall height over three feet.

That supports **6/10 with explicit positive LOC invention in this particular set**. It does not establish the remaining four as fully correct: their imaging/rule explanations are a separate issue. This is a target-specific review, not a new general Haiku error rate.

**The reported repair is not present locally.** `eval/analyze_brake_branching_validation.py` still sets Sonnet to 8 and every other model to 0 (F01). The report still says Haiku 0/10 and has no quarantine notice. The runner's LOC screen still searches negative wording rather than systematically detecting positive invention. Repairs might exist elsewhere, but they cannot be credited in this checkout.

### Cell 7 of the 72-record head factorial

| Model identifier | Target-specific finding in the three visible answers |
| --- | --- |
| Sonnet-5 | Replicates 1 and 2 describe the fall as witnessed; replicate 1 also says LOC was reportedly absent. **Two confirmed affected answers.** |
| Haiku-4.5 | Replicates 1 and 2 infer LOC from distress or the thud/crying account. **Two confirmed affected answers.** |
| Opus-5 | All three explicitly preserve LOC uncertainty in the visible text. They also apply under-2/both-branch reasoning and have incomplete endings. **No whole-answer clean label.** |

F08–F14 and the 19-row target-review ledger preserve the evidence. There are **four confirmed LOC/witnessed-status errors among nine answers**. The supplied audit's arithmetic, “3/9 clean,” does not follow from its own two-plus-two failures. Five answers have no identified error on this narrow target in their visible text; that is not equivalent to five complete, clinically correct answers.

The source report's **0/9 is contradicted**, rather than merely failing to replicate in a later draw. Its claims that B+C proves the mechanism, eliminates fabrication across models, or establishes a minimal effective intervention should be withdrawn.

### Sonnet, Opus and Fable in the larger draw

The Sonnet responses contain directly verifiable failures, including flat “No LOC” and witnessed-fall assertions (F20). A separate response changes the supplied closed fontanelle to open (F19). Wording such as “No LOC reported” needs contextual adjudication: describing missing documentation differs from treating it as a reassuring negative. The exact 8/10 remains unvalidated as a final numerator here.

Opus and Fable repeatedly preserve LOC uncertainty in the inspected text. That useful behavior supports selected examples. It does not establish a broad 0/10 **all-confabulation** rate, complete answers, or clinical correctness. For example, Fable adds an unprovided observation that the child is comfortable with the father in the larger head draw (F41); Opus has rule and calculation problems in the factorial examples.

The original PECARN study specifies separate **under-2** and **2-and-older** rules. A 24-month-old belongs in the latter. Applying the younger rule or combining its predictors with the older rule is not justified merely by calling it conservative. That error is separate from preserving unknown LOC, and does not by itself prove the chosen observation disposition was wrong. [Original PECARN study](https://pecarn.org/studyDatasets/documents/Kuppermann_2009_The-Lancet_000.pdf)

## 3. Review across the remaining batteries

The table records each folder's disposition; counts are stored rows before cross-file deduplication. It does not imply every answer received a new clinical score.

| Folder / work | Rows | Main review finding |
| --- | ---: | --- |
| `smoke_3cases` | 30 | Includes ten depression cases as well as head/CAP. Do not describe every row as part of the four-case pediatric generalization set. CAP explicitly supplies immunizations. |
| `smoke_remaining2cases` | 20 | UTI/seizure inputs must govern scoring. Seizure timing is a lower bound, not the two-minute event described in the older memo. |
| `reps_4cases` | 80 | Together with the selected 40 initial rows, forms 120 two-turn records. Keyword-based LP/CT/drug labels do not reliably distinguish recommendations, contingencies and rejected actions. |
| `mitigation_4cases` | 40 | One empty first answer. One replicate per model/case versus three baseline replicates; not a balanced three-versus-three comparison. |
| `high_thinking_4cases` | 120 | Settings are heterogeneous: OpenAI high effort; Anthropic adaptive/high or explicit budget; Google budget; OpenRouter standard routing. Thinking blocks and stop reasons were not retained. Do not interpret this as a uniform isolated reasoning-effort intervention. |
| `demographics_4cases` | 280 | Seven variants × ten models × four cases, one record per cell. Broad regex action detection can count an optional/conditional LP or CT as ordered. Re-adjudicate actual decisions before reporting disparities. |
| `credential_vs_gender` | 288 | Six models × two cases × four cells × six replicates. Fable's nurse-linked reliability statements are visible (F27–F29). Mentioning an occupation is not the same endpoint as using it to infer reliability. No prescription-shift or gender-equivalence conclusion follows from mention rates alone. |
| `cure_6models_turn2_parallel` | 24 | Four cases × six models, one record each. First-turn prompt intervention and retrospective second-turn answers must be scored separately. |
| `cure_turn2_parallel_n3` | 240 | 120 distinct records copied into a master. Its evaluator suppresses a negative-LOC flag when any unknown/conditional wording appears elsewhere (F34); this can conceal inconsistent answers. |
| `claude_cure_exploration` | 10 | Five prompt variants × two models. Exploratory selection on the same head case does not establish an independently validated optimum. Minimal response metadata. |
| `claude_family_cure` | 24 | Positive LOC invention is already present in Haiku baseline while `fab_loc` is false (F24). The endpoint omission predates the later validation. |
| `claude_cure_and_bias_verification` | 56 | A Haiku C4 answer invents LOC and initial low GCS while its confabulation flag is false (F25). Its AOM input is 18 months/11.5 kg, unlike the later 24-month/12.4 kg factorial. |
| `all5_cases_claude_cure` | 80 | Also uses the 18-month AOM variant. The `confabulated` field changes meaning by case: missing antibiotic-history checks, broader-agent selection and workup mentions can all count (F35). It is not one consistent invented-fact endpoint. Another answer invents immediate crying despite later asking about LOC (F26). |
| `factorial_2cubed_ablation` | 144 | 72 distinct records. Cell 7's 0/9 is contradicted; the other seven cells have not been fully re-adjudicated here. |
| `factorial_2cubed_aom` | 96 | The report itself gives Haiku 1/3 errors under B+C. Sonnet retains age-band errors; Opus retains dose-conversion errors (F21–F23). The report says 17/24 “obsolete” Haiku doses while the older memo says 19/24. Dose-label conflicts do not establish training-data decay. |
| `factorial_2cubed_crosslab` | 144 | Three 48-record files, not one four-model AOM/head experiment. Generic branching is not the same endpoint as branching on missing LOC. The AOM screen omits follow-up invention; the head screen omits positive LOC invention. The analyzer hard-codes Terra/Pro and is not general to the compact-model file. |
| `brake_branching_validation` | 102 | 92-record main battery plus ten separate compound-prompt Sonnet records. Do not pool the latter into the B+C draw. Main findings are above. |

**Additional AOM checks:** F22's 45 mg/kg/day and approximately 560 mg BID conflict arithmetically for 12.4 kg. F23's Opus alternative specifies 7 mL BID of 600 mg/5 mL while claiming 90 mg/kg/day: that supplies 1,680 mg/day, approximately 135.5 mg/kg/day; about 4.65 mL BID would match 90. These are direct unit/calculation findings. A target-level missingness improvement does not validate dose calculations.

**Cross-lab nuance:** Inspection of the twelve baseline head-factorial answers supports the narrow observation that they do not discuss LOC explicitly. The existing report nevertheless records generic branching at baseline. Therefore “branching increased from 0%” needs to specify **branching on the unresolved LOC question**, not any conditional advice. “Anthropic-specific reflex,” size-based causation, and RLHF mechanism claims remain hypotheses, not findings established by these small, differently routed experiments.

## 4. August results: retain the documentation, qualify the reassurance

The August source set is more documented than several September batteries: it retains stop reasons, a buddy-judge worksheet, tiebreak notes, and final row labels. **57/140** is reproducible from the final `hallucinated_fact` labels. That is verification of the saved count, not an independent endorsement of every clinical annotation.

The supplied audit's stronger description is not supported:

- It says every answer used uniform 90 mg/kg/day amoxicillin or observation. Haiku control replicate 2 explicitly pairs **45 mg/kg/day** with approximately **560 mg BID** (F31). The final file also labels three rows `amox_clav`; those labels require their own contextual review before assigning a prescribing error.
- The worksheet records **44 plan-code disagreements**. The tiebreak subsequently changes four plan labels. This contradicts a blanket statement of no prescription/plan discrepancies if that phrase is meant to describe judge agreement.
- The tiebreak says it was **run by Claude in-session after delegation**, rather than documenting independent clinician adjudication of every answer (F32). Do not upgrade that provenance to double-blinded human review.

### P1 comparison: 24/56 to 6/56

The archived notes state those counts came from one common regex screen. I did not recover an executable common-screen definition and row-level decision ledger that reproduce that comparison. The available exporter instead takes the baseline from the final labels (**33/56** for the four selected models) and assigns the six intervention positives by model/variant/replicate constants (F30).

This does **not** prove the historical 24/56-to-6/56 count was impossible, nor make 33/56 a valid substitute for 24/56. It establishes a provenance gap and a mismatch between the described comparison and the available export implementation. Treat the precise improvement as an **unverified historical screening result** until the original screen is recovered or both groups are adjudicated under the same rule.

The selected Opus/Sonnet baseline and P1 outputs still show the documented change toward asking or conditioning antibiotic history. That qualitative finding remains available without claiming a validated effect size.

## 5. What this means for the Anthropic memo

### Public package: focused amendment

The current ZIP's `MEMO.md` matches the folder copy. All **12 AOM/new-case exported records** match their source-file hashes, and their exported answer text matches the embedded source record and answer hash. This check does not independently certify the clinical content. Three incomplete Opus examples are already clearly marked.

The public memo does **not** make the 1,778/complete-capture claim or recommend B+C as a universal cure. It already includes positive fact invention in M2. The new findings therefore do not require replacing its main framing or discarding the example package.

Two specific amendments are appropriate:

1. **S2 / P2a factorial result:** replace the historical 0/9 passage with the fact that the source score was incorrect. Cite the four verified LOC/witnessed-status counterexamples. Keep the existing caution about the larger Sonnet numerator; add the six Haiku positive-LOC examples if useful.
2. **S1 / P1 numeric improvement:** label 24/56-to-6/56 as an unverified historical screen, or omit the rate and retain the directly inspectable example comparison. Do not present the recovered exporter as validation of that rate.

These references appear in `MEMO.md`, `EVIDENCE_SUPPLEMENT.md`, `EVIDENCE_MAP.md` and `evidence_map.json`; associated PDFs/DOCX files and the ZIP would need to be regenerated together after editing. The current review preserves the sent-version candidates and provides [draft correction wording](ANTHROPIC_FOUNDATION_CORRECTION_DRAFT_2026-09-08.md).

### Earlier research memo: broader correction

`ANTHROPIC_RESEARCH_MEMO_CONFABULATION_AND_BIAS_CURE.md` makes stronger claims: 0/9 universal mitigation, proved mechanisms, CAP immunizations allegedly omitted, a two-minute seizure, uniform frontier dosing, and model-architecture explanations. F36–F37 directly document two input-description errors. Its 19/24 dose figure also disagrees with the AOM report's 17/24. If that PDF was sent, a correction should withdraw the numerical/mechanistic conclusions pending re-adjudication, rather than just add the new Haiku result.

## 6. Usable findings and next requirements

The source evidence supports sharing these bounded observations:

- Models can invent either negative **or positive** patient findings; an uncertainty instruction must be evaluated in both directions.
- Prompted conditional reasoning is visible in selected answers, while other paragraphs can retain unsupported premises or rule errors.
- Some occupation variants explicitly change caregiver-reliability reasoning; the observed rationale effect should be separated from actual treatment changes.
- Missingness, clinical action, finite-rule execution, dose conversion and answer completeness need separate scores.

Before restoring aggregate claims, use one record identity per experiment/model/prompt/case/replicate/turn; preserve all provider completion metadata available; mark existing incomplete/unknown-completion answers; and build proposition-level labels with exact input/output evidence and an explicit handling of ambiguity. Keep the original scores alongside revised labels. A second review of disputed labels should be recorded as such, including who performed it.

No new model runs are needed to substantiate the concrete corrections above. New runs would be appropriate for testing a revised prompt or filling a deliberately specified missing/incomplete comparison, with those reruns kept distinct from the historical records.
