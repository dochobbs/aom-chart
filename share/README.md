# Share artifacts

Do not post or present without his review.

| File | What |
|---|---|
| `team_summary.md` | Plain-language summary for the team. Start here. |
| `compared_to_whom.md` | **The anchor essay** (~5,400 words) — the unfair-benchmark thesis: AI errors vs the human-error literature vs the combination trials, ending on the synergy hypothesis. |
| `blog_post.md` | Technical companion (~4,100 words) — the full AOM experiment writeup. |
| `linkedin_1_completed_chart.md` | Post 1 — the case, the inventions, the one-line fix. |
| `linkedin_2_judge.md` | Post 2 — the judge that flunked its own exam. |
| `linkedin_3_identity.md` | Post 3 — identity moved the reasoning, not the prescription. |
| `talk.pptx` | Five slides. Speaker notes are in the file. |
| `talk.pdf` | Same deck, leave-behind / preview. |
| `talk_notes.md` | What to say on each slide, plus pushback. |
| `one_pager.md` | One-page written version. |

**Publishing week:** blog post first (or with post 1). Post 1 Monday, post 2 Wednesday or Thursday, post 3 end of week. Each post copies from its `---` block. Every draft links the repo — it is currently **private**; flip it public first or cut the link lines.

Thesis: **They completed the chart.** Practical payoff: **one ask-don't-assume sentence cut inventions ~75%.**
Detailed technical writeup: `../FINDINGS.md`. Note: the deck and one-pager predate the evening runs — numbers were corrected in place, but the mitigation result and second identity positive appear only in `team_summary.md`, `../FINDINGS.md`, and the post drafts. Refresh `talk.js` before presenting.

Rebuild: `node talk.js` then export PDF from PowerPoint if you change `talk.js`.
