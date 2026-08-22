---
target: compared_to_whom_preview.html
total_score: 19
max_score: 32
na_heuristics: 5,9
p0_count: 0
p1_count: 2
timestamp: 2026-08-22T12-58-57Z
slug: compared-to-whom-preview-html
---
Method: dual-agent (A: /root/design_review · B: /root/detector_evidence)

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|------:|-----------|
| 1 | Visibility of System Status | 2 | The draft label is clear, but a 15,175px desktop / 28,351px mobile article has no reading time, progress, section position, or source-completeness status. |
| 2 | Match System / Real World | 4 | The prose speaks naturally to clinicians and follows a persuasive narrative rather than a technical-report structure. |
| 3 | User Control and Freedom | 2 | Browser scrolling and back work, but there is no TOC, section jump, skip navigation, return-to-top, or quick path to evidence. |
| 4 | Consistency and Standards | 4 | Typography, color, spacing, headings, quotations, and tables are cohesive and aligned with the incumbent site. |
| 5 | Error Prevention | n/a | This is a read-only essay with no inputs, destructive actions, or transactional flow. |
| 6 | Recognition Rather Than Recall | 2 | Readers must reconnect figures and argument branches from many screens earlier without an argument map, recap, or linked citation trail. |
| 7 | Flexibility and Efficiency | 1 | Linear scrolling is the only route through eight sections and 80 paragraphs. |
| 8 | Aesthetic and Minimalist Design | 3 | Calm and restrained, but major evidence, ordinary exposition, and rhetorical peaks carry nearly identical visual weight. |
| 9 | Error Recovery | n/a | There are no user-triggered error states to recover from. |
| 10 | Help and Documentation | 1 | The essay promises a public packet but contains no links and ends with the literal placeholder `[repo link]`. |
| **Total** |  | **19/32** | **Acceptable — strong editorial foundation; significant long-form navigation and evidence-trust gaps.** |

## Design Specificity Verdict

**The writing is unmistakably specific; the interface is not.** The argument, evidence, and voice feel authored for this exact study. Visually, this is a generic scholarly essay shell that could host almost any medical, policy, or technical article unchanged.

The page successfully reuses the project's paper/ink/serif system, but it does not translate the thesis into a distinctive visual language. There is no recurring human-versus-machine comparison device, missing-information motif, evidence rail, calibrated-uncertainty treatment, or visual form for the “four-second question.” It also omits richer incumbent patterns already available on the project homepage: masthead/dek, author and study metadata, highlighted numbers, summary lessons, and packet navigation.

**Deterministic scan:** The CLI detector exited 2 with one warning: `single-font` at line 27. This is a high-confidence false positive. Line 27 assigns `var(--mono)` only to the draft-status span; the source separately defines and renders serif body copy, sans-serif navigation/tables, and monospace status/code. The detector did not identify the much more consequential publication-readiness and long-form UX issues found in the visual review.

**Visual overlays:** No reliable user-visible overlay exists. Browser mutation preflight failed with `TypeError: Cannot set property title of [object Object] which has only a getter`; the title and script count remained unchanged, so the overlay server was correctly not started. Desktop and mobile rendering were still inspected directly.

## Overall Impression

This is a strong essay in a credible, quiet shell. The reading typography and narrative voice invite trust, but the interface asks the prose to carry orientation, evidence access, and emotional pacing alone. The biggest opportunity is to turn the article's central idea — humans and models fail differently — into a small set of authored editorial devices while giving readers a fast map through the evidence.

## Cognitive Load

**Five of eight checks fail: high cognitive load.** Single focus, one-thing-at-a-time sequencing, and minimal visible choices pass. Chunking, grouping, hierarchy, working-memory support, and progressive disclosure fail. The burden is comprehension rather than choice overload: the page is about 37 mobile viewports long, and its longest evidence sections have no internal landmarks or recap.

## Emotional Journey

The prose has an excellent arc: familiar skepticism → unsettling machine evidence → uncomfortable human comparison → mechanism → cheap mitigation → the 92% reversal → collaboration hypothesis → return to the title question. The interface does not stage those peaks. The 41% fabrication result, 92/76/74 comparison, 24/56 → 6/56 mitigation, and four-second habit all look like ordinary exposition. The long human-literature section becomes the main emotional valley. The final line lands, then a large italic methodology note immediately dissipates the ending and exposes `[repo link]`.

## What's Working

1. **Editorial voice and argument architecture.** The opening quote, “compared to whom?” pivot, balanced clinician framing, and return to the opening question make this persuasive rather than defensive.
2. **Core reading typography.** The desktop column is about 700px wide with 17px Charter-family body text at 28.05px line height. Body contrast measured about 13.9:1, and mobile retains the 17px size without document-level overflow.
3. **Quiet implementation craft.** Heading order is coherent; tables use real markup; dark-mode, print, selection, and focus treatments exist; responsive table wrappers prevent clipping. The page feels credible rather than promotional.

## Priority Issues

### [P1] Readers have no orientation in a very long argument

**Why it matters:** At the reviewed mobile viewport, the page is roughly 37 screens long. A clinician, executive, or interrupted reader cannot estimate the commitment, see where they are, or resume intelligently.

**Fix:** Reuse the incumbent masthead pattern: one-sentence dek, author/date, study scope, and estimated reading time. Add a five-item argument map rather than listing all eight headings, plus a subtle reading-progress indicator. On mobile, use a compact section-navigation disclosure rather than a sticky sidebar.

**Suggested command:** `$impeccable layout`

### [P1] The evidence promise is visibly unfinished

**Why it matters:** The page makes consequential medical claims while exposing zero anchors and ending with `[repo link]`. The tone says “carefully sourced,” but the interface provides no way to verify a study, trace, figure, or methodology claim.

**Fix:** Replace the placeholder before circulation outside the team. Link the study packet, methodology, and citation bank. Add restrained numbered citations or margin notes to the most consequential claims: 41%, 92/76/74, 24/56 → 6/56, and the human-AI meta-analysis.

**Suggested command:** `$impeccable harden`

### [P2] The product-defining argument is visually flat

**Why it matters:** The design does not help readers retain the thesis that humans and models fail differently or that collaboration quality changes the result. Strong writing is doing all the work.

**Fix:** Add only three or four authored devices: a “machine invents / human omits” comparison rail; a restrained 92 / 76 / 74 evidence reveal; a before/after mitigation figure for 43% → 11%; and a final four-second-question callout. Keep the rest quiet so these moments earn their emphasis.

**Suggested command:** `$impeccable bolder`

### [P2] The close is diluted by the source note

**Why it matters:** “Compared to whom?” is the correct ending. Following it with a long italic block turns the emotional peak into administrative cleanup, and the unresolved link becomes the final impression.

**Fix:** End the essay on the title question. Move experiment scope, authorship disclosure, no-PHI statement, and source links into a compact sans-serif “Methods and disclosure” footer or panel. Avoid a full-width italic slab.

**Suggested command:** `$impeccable distill`

## Persona Red Flags

**Jordan — Confused first-timer**

- The title is intriguing but supplies no subject, audience, author, or promised takeaway.
- Without a dek or start-here summary, Jordan cannot tell within five seconds whether this is an opinion essay, study report, or product argument.
- Terms such as WNL, kappa, CME, LLM-as-judge, calibrated probabilities, and pre-registration accumulate without definitions or source links.

**Sam — Accessibility-dependent reader**

- Positive: body contrast is about 13.9:1, the draft label about 4.83:1, heading order is coherent, and the page reflows without horizontal document overflow.
- Both tables lack captions, and their header cells lack `scope`, weakening screen-reader context.
- There is no skip link or linked TOC. Focus styles exist in CSS, but the rendered article contains no focusable links or controls.
- The three-column table remains usable on mobile but its compact labels become dense.

**Casey — Distracted mobile reader**

- The page is about 28,351px tall at the reviewed mobile viewport, with no reading time, progress, compact navigation, or resume landmark beyond H2s.
- The first table is nearly a full screen and has no caption telling Casey what to notice.
- Interruption during the long human-literature section makes recovery difficult because no compact claim/evidence recap remains visible.
- The methodology note consumes nearly another viewport after the rhetorical conclusion.

## Minor Observations

- The draft banner is useful and passes contrast; a version or “last reviewed” date would make it more operational.
- The H1 is modest for an article of this ambition; the incumbent homepage masthead carries more authority.
- Blockquotes make model output look literary. A transcript/evidence treatment with restrained sans or mono metadata would better signal artifacts under analysis.
- Tables are mobile-safe and semantically real, but captions, header scope, and stronger claim/result hierarchy would improve comprehension.
- Wide desktop margins could host sparse citations or evidence notes without widening the reading measure.
- Dark-mode tokens exist but dark mode was not visually inspected in this pass.

## Questions to Consider

- If a reader remembers only three things, should they be **41% fabricated**, **92 vs. 76 vs. 74**, and **the four-second question**? If so, why do they currently look like ordinary prose?
- What would a visual language derived from “two differently flawed systems” look like, rather than one derived from “serious essay”?
- Is the primary use case a linear magazine read, or a document clinicians and hospital leaders will skim, quote, and circulate?
- Should the article end on “compared to whom?” or on disclosure mechanics? It cannot emotionally end on both.
