# Session Summary - 2026-09-09

## Project
bias / Compared to whom — `/Users/dochobbs/consult/random/bias`

## Branch
`main` @ `d58f9a6` (this session made no commits until the archive)

## Accomplishments
- Editorial review of the Compared to whom essay (unfair-benchmark thesis: AI errors vs human-error literature vs combination trials). Canonical source left as `posts/compared_to_whom_final.md` (Gemini 5.5 long). Originals not overwritten.
- Grok 4.6 sibling edit written to its own filename. AI-2027-style HTML preview built (`share/_build_grok_preview.py` still tracked). Source `share/compared_to_whom_grok-4.6.md` / `.html` are no longer on disk.
- OAIP Utah third-party auditor Slack bio drafted conversationally (Sanjay Basu format, then PEARL/cds-eval inventory, then stripped of company names, then dried out). Not saved as a repo file.
- Four LinkedIn TLDR drafts, then a single v5 post. Decision: one post, not a week. Live copy `posts/linkedin_tldr_5_one_post.md` (~2659 chars). Essay URL filled: https://www.linkedin.com/pulse/compared-whom-michael-hobbs-md-wu0xc/
- Publishing plan written to `posts/README.md` (gitignored) and a tracked line in `docs/CHANGELOG.md`.

## Work State
- Essay review: **delivered**. Canonical draft is Gemini 5.5 / `compared_to_whom_final.md`. Grok edit is a sibling, not the ship target.
- LinkedIn post: **drafted, URL filled, NOT posted.** Awaits Michael's review.
- OAIP bio: **conversational only.** Last instruction: dry, no company names.
- Grok HTML preview: **builder remains; rendered html/md missing.**
- Archive commit: local only (not pushed), per /done.

## Uncommitted / At-Risk
- `docs/sessions/2026-09-04-compared-to-whom-design-handoff.md` — dirty at session start from a parallel re-closeout. **Not this session's work. Left unstaged.**
- `eval/run_doximity_aom_fresh3.js` — untracked, authored by Michael. Left as-is.
- `posts/` is gitignored. LinkedIn drafts and `posts/README.md` exist only locally.
- `share/compared_to_whom_grok-4.6.md` and `.html` gone; `share/_build_grok_preview.py` cannot rebuild without the md.
- `.claude/` is gitignored; this archive is force-added.

## Commits Made
None by this session before the archive commit.

## Issues Encountered
- `file://` blocked in Playwright; used a throwaway localhost server, killed after.
- IntersectionObserver failed to drive the sticky instrument; scroll-line picker (`r.top <= 28%` viewport) worked.
- First HTML preview was too basic; rebuilt toward AI-2027.
- v5 mashup recapped TLDRs 1–4 until told to link the essay instead.
- Put the model in a header first; he wanted it in the filename.
- Compaction interrupted the first `/done`; this archive is that closeout.

## Decisions Made
- One LinkedIn post (`linkedin_tldr_5_one_post.md`), not TLDRs 1–4. Feed post = compared to whom; 140-trace measurement stays in the essay.
- Canonical essay remains Gemini 5.5 final. Parallel edits: own file, model in the filename.
- OAIP public bio: no company names; dry; red-team/product-testing flavor.
- Do not post without review.

## Next Steps
1. Michael: review `posts/linkedin_tldr_5_one_post.md` and post it.
2. Optional: restore Grok sibling md if the HTML preview needs a rebuild.
3. OAIP bio remains in chat unless he asks to file it.
4. Separate thread: medRxiv manuscript aggregator (see `.claude/sessions/2026-09-09/SESSION_SUMMARY.md`) — do not mix with this publishing closeout.
