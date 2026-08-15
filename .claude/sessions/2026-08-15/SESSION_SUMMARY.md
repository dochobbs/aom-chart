# Session Summary - 2026-08-15

## Project
AOM chart eval — /Users/dochobbs/consult/random/bias (github.com/dochobbs/aom-chart, private)

## Branch
main

## Accomplishments
- Verified the packet against its own data: caught the 48/140 headline conflating phrase-regex hits with assertions; corrected all seven quoting docs
- Buddy-judged all 140 traces (Terra↔Sonnet cross-family, fallbacks for 12 stubborn rows), then ran the Doc-delegated tiebreak: every disputed call quote-anchored, conventions recorded for codebook v3
- Final numbers: 57/140 rows invented ≥1 chart fact (up from 48), follow-up asserted 11/140 across 7 of 10 models (down from 14), Fable flat-abx 13/14, Sonnet under-2 12/14, Haiku stale dose 10/14
- Three new experiments: job-pair confirmation on terra/opus/haiku (nurse move unique to Fable), Flash×insurance formal ruling (FIRES, 5/6 vs 1/6 WW-preferred — second identity positive), mitigation smoke (one ask-don't-assume sentence: invention rows 24/56 → 6/56, plans intact, modes 4/5/6 untouched)
- Turn-2 tabulation of all 192 responses (97% ask; ≤3 re-invent; Fable confesses its own assumptions)
- Judge findings: Terra-as-judge miscoded the age cusp on 11/14 Sonnet rows; Sonnet-as-judge no-JSON on 25/84
- Repo made private; restructured to docs/ eval/ results/ share/ site/ archive/; pandoc-built HTML site with clinical-offprint design pass; index.html linked landing page
- Publishing set: FINDINGS.md, share/team_summary.md, blog post (~3,400 words, models named, Fisher note, same-family disclosure), 3-post LinkedIn week with schedule
- Retired OpenRouter (Grok out, Fable frozen at existing traces) per Michael

## Work State
- All repo work: committed AND pushed through 618b0cf
- Vault memory (Decision Log ×2, Learned Preferences, User Model, Proactive Triggers): written
- Publishing drafts: awaiting Michael's review — NOT posted, [repo link] placeholders unfilled
- Session archive commit: local only (not pushed, per /done rules)

## Commits Made
- 82c11be DOCS: Tiebroken finals, confirmation + mitigation runs, packaged for sharing
- 6eb74f9 CHORE: Clean root - archive superseded working docs, drop scoring scratch
- 4c0a411 CHORE: Restructure for sharing - docs/, eval/, HTML landing page
- c14cc6f FEATURE: HTML site - pandoc-rendered doc pages, fully linked landing
- 059e4e9 FEATURE: Typeset the site - clinical-offprint design pass
- 7cb5236 DOCS: Publishing set - long-form blog post + three-post LinkedIn week
- 478e241 DOCS: Expand blog post to full-length piece (~3,600 words)
- 618b0cf DOCS: Blog post - name the models, add Fisher note and family disclosure

## Issues Encountered
- Sonnet-as-judge JSON failures (25/84) needed two retry rounds + cross-family fallback judges (Terra for Gemini rows, Opus for OpenAI rows) — all marked in _buddy.json
- google.genai no longer installed (old venv gone) — Gemini unusable as judge; irrelevant for SUT runs already done
- Playwright profile locked by another session; Safari MCP can't open file:// — used a throwaway localhost server (killed after)

## Decisions Made
- No OpenRouter ever again on this project; repo private until posts ship; models named in public writeups but not routers/Grok; "we" kept with provenance line; tiebreak conventions (given/because = assertion; exam-inference OK; strike "access" from reliability_language in codebook v3)

## Next Steps
- Michael: review 4 drafts, fill [repo link], public/private decision (in ~/TODO.md)
- Add mitigation slide to talk.js, rebuild deck
- If fable-5 appears on the Console key: native re-verification of Fable findings
- After any .md edit: python eval/build_site.py
