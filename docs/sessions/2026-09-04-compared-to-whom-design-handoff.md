# Compared to whom? article and visual-design handoff

- **Theme:** compared-to-whom
- **Resume aliases:** compared to whom, compared to whom article, article design, AI-2027 article, bias article prototype
- **Status:** Complete and archived at a safe decision boundary
- **Canonical handoff:** `/Users/dochobbs/consult/random/bias/docs/sessions/2026-09-04-compared-to-whom-design-handoff.md`
- **Best next move:** If this work resumes, choose one of the three AI-2027-inspired directions and rebase it on the current local `posts/compared_to_whom_final.md`; first decide whether that final Markdown source should remain local-only or be restored to tracked source control.

## Outcome and decision boundary

The original long-form essay preview was reviewed, then preserved while a separate interactive design study was built. The gallery exposes six reading models: Restrained, Distinctive, Publication, Evidence Engine, Living Case File, and Cinematic Scroll. The last three respond to the request for something closer to `ai-2027.com` without becoming dramatically different from the existing editorial identity.

The visual exploration is complete. No direction was selected for production, no deployment was requested, and no current publication draft was rewritten during closeout.

The standalone Markdown edit created during the original session at `share/compared_to_whom_codex_edit.md` is no longer present after later repository packaging. It was not restored because the article subsequently advanced through multiple local drafts to `posts/compared_to_whom_final.md`; recreating the older edit would introduce a stale competing source. Its editorial changes were limited to framing: a subtitle and metadata, a 20-second read, an argument map, evidence links, table captions, a stronger final refrain, and a cleaner methods/disclosure section. The main essay body was not substantively rewritten.

## Repository and Git state

- **Repository/worktree:** `/Users/dochobbs/consult/random/bias`
- **Branch:** `main`
- **HEAD:** `077c15b4cf8cb0a250cd6303b3ab915d9d2ce62f`
- **Remote relationship:** `main...origin/main` with no reported ahead/behind count at closeout
- **Task-owned commits from this session:** none
- **Existing prototype commits:**
  - `dde7ef75255dd996d5e50ca3ca1d5bdeb388d7f2` — added the initial article/design study
  - `8b996eae6c5dad641472bab0620417a6bb3851cf` — packaged and refined the public benchmark and prototype
- **Prototype state:** tracked and clean at closeout
- **Handoff state:** newly created and intentionally uncommitted

The worktree already contained unrelated or concurrent work. It was preserved without staging, committing, or editing:

```text
 M FINDINGS.md
 M README.md
 M docs/CHANGELOG.md
 M docs/human_parallels.md
 M share/README.md
?? docs/essay_editorial_review.md
?? docs/public_release_review.md
?? eval/analyze_chatgpt_36.py
?? eval/backfill_2_traces.js
?? eval/calc_model_aggregates.py
?? eval/chatgpt_36_master_runner.js
?? eval/chatgpt_suite_runner.js
?? eval/check_luna_text.py
?? eval/extract_history_logic.py
?? eval/generate_chatgpt_report.py
?? eval/generate_oe_tiers_report.py
?? eval/inspect_chatgpt_models.js
?? eval/inspect_model_controls.js
?? eval/oe_models_runner.js
?? eval/oe_multi_runner.js
?? eval/plot_chatgpt_36_matrix.py
?? eval/plot_master_comparison.py
?? eval/plot_oe_tiers.py
?? eval/plot_oe_vs_chatgpt_comparison.py
?? eval/rerun_terra_high_rep3.js
?? eval/run_chatgpt_36_matrix.js
?? eval/run_chatgpt_thinking_spectrum.js
?? eval/run_final_trace.js
?? eval/run_luna_fresh.js
?? eval/save_luna.js
?? eval/score_oe_tiers.py
?? eval/test_chatgpt_single.js
?? eval/test_config.js
?? eval/test_robust_runner.js
?? results/cds/chatgpt_tiers/
?? results/cds/comparison_oe_vs_chatgpt_tiers.png
?? results/cds/oe_tiers/
?? results/cds/oe_vs_chatgpt_master_comparison.png
```

The local `posts/` directory and `.impeccable/` review artifacts are ignored by `.gitignore`. This includes the later article drafts and the critique report.

## Durable artifacts

- Gallery: `prototypes/compared-to-whom/index.html`
- Article shell: `prototypes/compared-to-whom/article.html`
- Concept behavior: `prototypes/compared-to-whom/concepts.js`
- Concept styling: `prototypes/compared-to-whom/concepts.css`
- Gallery behavior and styling: `prototypes/compared-to-whom/gallery.js`, `prototypes/compared-to-whom/gallery.css`
- Local critique: `.impeccable/critique/2026-08-22T12-58-57Z__compared-to-whom-preview-html.md` (ignored, present locally)
- Original essay used by the prototype: `posts/compared_to_whom.md` (ignored, present locally)
- Newer local article source: `posts/compared_to_whom_final.md` (ignored, present locally; last modified 2026-08-31)

## Verification

Closeout verification on 2026-09-04 CDT:

- `node --check prototypes/compared-to-whom/concepts.js` — passed
- `node --check prototypes/compared-to-whom/gallery.js` — passed
- Temporary `python3 -m http.server 8128 --bind 127.0.0.1` — started for verification, then stopped
- Gallery, Evidence Engine, Living Case File, and Cinematic Scroll endpoints — HTTP 200
- `git diff --check` — passed
- Impeccable detector — one non-blocking `single-font` warning against the generated article HTML; no closeout change made

The earlier design pass also checked desktop and mobile containment for all three AI-2027-inspired directions and corrected mobile overflow in the Cinematic Scroll article and gallery controls.

## Publication and external state

- **Committed:** existing prototype commits only; no commit created during closeout
- **Pushed:** current `main` matches `origin/main`; the new handoff is not pushed
- **PR:** none opened or merged by this workstream
- **Deployed:** no
- **Verified live:** local HTTP verification only
- **Retained process:** none; the temporary preview server was stopped

## Unfinished or intentionally parked

- No production direction has been selected.
- The prototype still renders the August 22 article baseline, not the later `posts/compared_to_whom_final.md` draft.
- The older standalone Codex Markdown edit is absent and intentionally not recreated.
- The ignored `posts/` publication drafts are not portable through Git unless the repository's source-control policy changes.
- The one detector typography warning remains accepted and non-blocking.

## Resume

```bash
cd /Users/dochobbs/consult/random/bias
python3 -m http.server 8128 --bind 127.0.0.1
open http://127.0.0.1:8128/prototypes/compared-to-whom/index.html
```

Then compare the selected concept against `posts/compared_to_whom_final.md` before modifying either source.
