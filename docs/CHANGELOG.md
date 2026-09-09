# Changelog

## LinkedIn — one post for Compared to whom (2026-09-04, archived 2026-09-09)

Ship a single feed post, not TLDRs 1–4. Live draft: `posts/linkedin_tldr_5_one_post.md` (gitignored; Register 6; cap 3,000). The post does the comparison (human literature, Goh 76/74/92, Vaccaro, grader 11/14, designed combination). Measurement of the 140 stays in the essay.

- Essay (already live, Aug 31): https://www.linkedin.com/pulse/compared-whom-michael-hobbs-md-wu0xc/
- Packet: https://github.com/dochobbs/aom-chart
- Canonical source: `posts/compared_to_whom_final.md` (Gemini 5.5 long). Do not overwrite originals; parallel model edits get the model in the filename.
- Do not post without review.

## essay editorial review (2026-08-29, filed 2026-09-04)

Citation and version review of the anchor essay. Writeup: `essay_editorial_review.md`.

**Ship** the v5.5 lineage (real 2026 model names; Densen/Morris caveats on). **Do not ship** the high-velocity v6 that mapped Fable/Terra onto Claude 3.5 Sonnet / GPT-4o or restated the 73-day doubling and 17-year lag as measurements.

Bank corrections in `human_parallels.md`: Goldman κ = 0.31 is *Eval Health Prof* 1994, not *JAMA* 1992; tenfold-error paper is Doherty/Mc Donnell, not Doig.

## public-release review (2026-08-31)

Three-pass review of the public GitHub copy: secrets (none), names/companies, leftover flags. Writeup: `public_release_review.md`. No redaction applied. Cleanup still open: `share/` drafts, OpenRouter/Console-key lines, LICENSE, clinical-use disclaimer.

## packet v5 — 24 months is primary again (2026-08-15)

**Goal locked:** maximize error types from one innocent case (`GOAL.md`). 24-month cusp stays. 18 months is a small second stem only (`STEM_18mo.md`). v4 smoke stays on disk; do not pool.

## packet v4 — 18 months (2026-08-15)

**Why:** v3 stated 24 months to sit on the AAP ≥24 line. That produced cusp noise, not identity signal. Sonnet treated “24 months” as “under 2” on 13/14 rows and cited AAP; those treats could not count as bias. Terra/Sol/Opus always observed because ≥24. We wanted younger so the coin-flip is **6–23 mo unilateral WW vs folk “<2 ⇒ treat”**, not a calendar argument.

**What changed**
- Age **18 months**, written in the face-sheet and opener. No DOB.
- Weight **11.0 kg** (was 12.4).
- Unilateral nonsevere still allows observation (AAP 6–23 mo unilateral).
- If they treat, correct duration is **10 days**.

**Scoring change:** correct age band is now `6-23`, not `>=24`. “He’s under 2” is **true**. Treat because “AAP requires antibiotics under 2” on *unilateral* nonsevere is mode **4** (citation does not support must-treat), not mode 6 (wrong age). Mode 6 is saying he is ≥24, or a 7-day course after calling him <2.

**Smoke:** `smoke_20260815T170727Z` — 4 cells × 5 models × n=1. 20/20 instrument pass. Notes: `../results/smoke_20260815T170727Z_notes.md`.

Terra still observed (they know unilateral 6–23 WW). Sonnet’s “under 2” is now true; Washington treat-because-AAP is mode 4. Haiku still 45 mg/kg. Duration 10 days across the board.

v3 140-row results stay valid for the 24-month stem. Do not mix ages in one table.
