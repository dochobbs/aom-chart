# Public-release review — aom-chart

Reviewed 2026-08-31 against the working copy at `/Users/dochobbs/consult/random/bias` (`github.com/dochobbs/aom-chart`, already public). Three passes: secrets, names/companies, leftover flags.

Not a legal opinion. Not a rewrite. Nothing in this file is itself a secret.

## Pass 1 — secrets

Scanned the tree and git history (all commits then on `main`).

| Check | Result |
|---|---|
| API keys, `.env`, PEM, tokens (`sk-ant`, `sk-or-`, `sk-proj-`, `ghp_`, `AKIA`) | **None** in files or history |
| Keys in code | Env **names** only (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY`, `XAI_API_KEY`). Values read from the environment |
| PHI / real patients | Synthetic chart. Stated as such |
| Phone / street address / Lakes / Elation / Spruce | **Not present** |

`.gitignore` now covers `.env*`, `*.pem`, `*.key`, `.claude/`, `.playwright/`, `.playwright-mcp/`, `.impeccable/`, `.remember/`, `share/node_modules/`, `share/slides/`. Those agent/browser dirs are **not** in `git ls-files` on current `main`.

## Pass 2 — names and companies

**Keep (author / science):** Michael Hobbs, MD; `michael@hobbs.md`; synthetic audit names (Jamal/Shanice Washington, Liam/Emily Whitaker — `docs/NAMES.md`); literature authors (Goh, Berdahl, van Ryn, etc.); Medicaid as an experimental cell.

**Named on purpose (already the public writeup policy):** OpenAI, Anthropic, Google, xAI; Luna, Terra, Sol, Haiku, Sonnet, Opus, Fable, Gemini Flash/Pro, Grok; Claude as study operator (“Michael directing Claude”).

**Optional plumbing redact** (not a key leak; says this Anthropic org lacks Fable):

- OpenRouter as the Fable/Grok hop
- “Console key lacks fable-5” / “this machine”

Present in `FINDINGS.md` limitations, `docs/GOAL.md`, `docs/RUNS.md`, `eval/models.json`, some `results/*_notes.md`, talk speaker notes.

**Colleague** in the essays is unnamed. Could still be recognizable from the quote. Not a name leak.

Blue Cross Blue Shield is the fictional private-insurance cell in `eval/variants.json`. Trademark, not a real family. Optional: “Private (commercial).”

## Pass 3 — leftover flags

Not secrets. Would I want them on a public scientific repo?

| Flag | Where | Why |
|---|---|---|
| Publishing calendar | `share/README.md` | Two-wave plan, “Goh hook not yet drafted,” await review |
| “Do not post” + `[repo link]` / `[repo link — private for now]` | `share/blog_post.md`, `share/linkedin_*.md`, `share/compared_to_whom.md`, Gemini/Grok/Codex edit passes | Drafts look live once the repo is the packet |
| Landing page points at drafts | `index.html` toc: “LinkedIn drafts and the five-slide talk live beside it” | |
| AI 2027 layout homage | `prototypes/compared-to-whom/`, `share/compared_to_whom_grok-4.6.html` | Style copy, not a data leak |
| Fisher p ≈ 0.001 on n=6 | `FINDINGS.md`, site HTML | Bar was “not a fluke,” not p < 0.05 |
| No LICENSE | repo root | Reuse terms unclear |
| No “not for clinical use” | `index.html` | Prompt is “You are a pediatrician in clinic”; traces are published plans |
| Local absolute path | `share/talk.js` write path | Mild |

Fine as-is: WIC/CHIP/food-pantry language in unemployed *model* traces; `ai2027-hero.png` (generated); GitHub Pages is off (`has_pages: false`); `data/` CSVs are traces, no keys.

## If doing one cleanup

1. Leave author + model names + synthetic chart names.
2. Gitignore or drop `share/` except `team_summary.md` and `one_pager.md` (or keep `share/` and accept drafts + calendar as public).
3. One FINDINGS/docs pass to drop OpenRouter / Console-key / “this machine” if plumbing stays offstage.
4. Add LICENSE + a one-line “synthetic eval, not clinical advice” on `index.html`.

History rewrite is unnecessary: no keys in old commits.

## Not done in this review

No commit from this pass. No redaction applied. Decision still open on `share/` and OpenRouter lines.
