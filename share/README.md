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

*(Note: Long-form publication drafts and social posts are stored locally in the root `posts/` directory).*
