# Repository Rules & Boundaries

## 1. Confidentiality & External Partner Materials
- **Company Memos are NEVER Public:** Any memos, feedback briefs, advisory documents, and correspondence prepared for external companies or partners (including Anthropic, Doximity, Google, OpenAI, OpenEvidence, UpToDate, AMBOSS, Glass Health, or ANY other commercial company/partner) are non-public and must **NEVER** be committed to public repositories or placed in public-facing directories.
- **Public Repo Scope:** Public repositories must only host basic, general, shareable documentation, open reproducible benchmark reports, case stems, reproduction scripts, and immutable evaluation datasets.
- **Storage Location:** All partner-specific materials belong exclusively inside `docs/internal_review/` (which is gitignored) or under explicit `.gitignore` rules.
- **Preprint Manuscripts & Supplementary Files:** Working manuscripts and supplementary appendices under revision belong in `docs/internal_review/manuscript/` and must remain local and untracked until formal publication.

## 2. Commercial Entity Evaluation Gate (Strict Opt-In Public Policy)
- **Named Company Evaluations are Internal by Default:** All benchmark runs, evaluations, test traces, performance scores, and rankings of ANY named commercial company, platform, vendor, or commercial CDS tool (including AvoMD, Epic, Cerner, UpToDate, OpenEvidence, Glass Health, Doximity, Anthropic, OpenAI, Google, etc.) are STRICTLY INTERNAL by default.
- **NEVER Add New Named Entities to Public Repos:** You must NEVER commit, stage, or add newly evaluated commercial platforms, tools, or vendors to public markdown tables (e.g., `CLINICAL_RECOMMENDATIONS_AND_RANKINGS.md`, `README.md`), public findings, or public directories (`results/cds/`, `docs/`) UNLESS the user explicitly gives affirmative, written instruction specifying that tool (e.g., "publish AvoMD results to public repo").
- **Default Storage Location:** All raw runs, evaluation logs, screenshots, and writeups for named commercial tools belong exclusively in `docs/internal_review/<company_name>/` or gitignored scratch paths.
- **Automatic Gitignore Enforcement:** Any directory, file, or pattern associated with a newly evaluated named commercial platform must be added to `.gitignore` and verified as untracked before saving or committing.

## 3. Scientific Tone & Rigor
- **Objective & Forensic Framing:** Maintain an objective, scientific, and matter-of-fact tone. Frame technical updates, token expansions, and classifier refinements as transparent sensitivity analyses and forensic audits—never as apologies, concessions, or personal errors.
- **Data Ground Truth:** All numbers in documentation must trace directly to raw, immutable JSON records in `results/`.
