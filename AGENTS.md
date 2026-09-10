# Repository Rules & Boundaries

## 1. Confidentiality & External Partner Materials
- **Company Memos are NEVER Public:** Any memos, feedback briefs, advisory documents, and correspondence prepared for external companies or partners (including Anthropic, Doximity, Google, OpenAI, OpenEvidence, UpToDate, AMBOSS, Glass Health, or ANY other commercial company/partner) are non-public and must **NEVER** be committed to public repositories or placed in public-facing directories.
- **Public Repo Scope:** Public repositories must only host basic, general, shareable documentation, open reproducible benchmark reports, case stems, reproduction scripts, and immutable evaluation datasets.
- **Storage Location:** All partner-specific materials belong exclusively inside `docs/internal_review/` (which is gitignored) or under explicit `.gitignore` rules.
- **Preprint Manuscripts & Supplementary Files:** Working manuscripts and supplementary appendices under revision belong in `docs/internal_review/manuscript/` and must remain local and untracked until formal publication.

## 2. Scientific Tone & Rigor
- **Objective & Forensic Framing:** Maintain an objective, scientific, and matter-of-fact tone. Frame technical updates, token expansions, and classifier refinements as transparent sensitivity analyses and forensic audits—never as apologies, concessions, or personal errors.
- **Data Ground Truth:** All numbers in documentation must trace directly to raw, immutable JSON records in `results/`.
