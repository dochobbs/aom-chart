# Presentation & Team Artifacts

Slide deck, speaker notes, and team summaries for presenting the benchmark.

| File | What |
|---|---|
| **`team_summary.md`** | Plain-language summary for the clinical and engineering team. Start here. |
| **`one_pager.md`** | One-page written executive brief. |
| **`talk.pptx`** | Five-slide presentation deck. Speaker notes are embedded in the slides. |
| **`talk.pdf`** | PDF leave-behind / deck preview. |
| **`talk_notes.md`** | Slide-by-slide speaker script, clinical context, and pushback handling. |
| **`talk.js`** | NodeJS slide builder script (builds `talk.pptx` via `pptxgenjs`). |

## Rebuilding the deck

To modify the slide deck:
```bash
cd share
npm install
node talk.js
```
Then export `talk.pdf` from PowerPoint.

Long-form drafts and social posts live in `posts/`. See **`posts/README.md`**. LinkedIn for the anchor essay is a single post (`posts/linkedin_tldr_5_one_post.md`) that links the full article plus the GitHub packet; do not recap the 140-trace scoreboard in the post.
