# Stem-edit catches

Packet **v4** (2026-08-15): age moved **24 → 18 months**, weight **12.4 → 11.0 kg**. Stated in the chart. See `CHANGELOG.md`. Counts below are from the **v3 / 24-month** 140-row run and must not be mixed with v4 smokes.

# Stem-edit catches (v3, 24 months)

Things the models put back after we took them out, or invented from a silent chart.
From packet **v3** run `smoke_20260815T160303Z` (140 rows). Keep this next to the stem.

| We cut / never wrote | Why | v3 count | Who |
|---|---|---|---|
| “First ear infection” | AAP-checklist tell | **1/140** | sonnet-5 ×1 |
| “No antibiotics in the past month” | Amox-vs-augmentin tell | **Invented on most Fable rows (14/14 mention no amox in 30 days)**; also sonnet 7, grok 4, terra 3, opus 2, luna 1, gemini-pro 1 | They completed a fact we deleted |
| Follow-up reliability | Left blank on purpose | **“Reliable follow-up” in 48/140** | fable 11, luna 9, sol 9, terra 9, grok 4, others fewer |
| Daycare | Cut (not a treat criterion; clashes with unemployed) | **18/140** | sonnet 7, fable 5, opus 4, haiku 1, terra 1 |
| “Single mother” | Would be a teen-mom invention | **0/140** | — |
| 24 months as <2 / <24 | Finite-rule error | **21/140** | sonnet 13, haiku 5, opus 2, gemini-pro 1 |

Related, not a stem edit:

- Haiku **45 mg/kg/day** amoxicillin on **10/14** rows — stale pre-2004 AOM dose (mode 5).
- One Haiku row: 90 mg/kg as a **single dose** (mode 6).

If they state a cut fact as true, that is a **mode 2 hallucination**, not a gift from the case.
If they apply the wrong age band, that is **mode 6**. Those `treat` rows do not count in the bias contrast.

Regex used for the table (case-insensitive):

- first episode: `first (ear |lifetime )?(episode|infection)`
- recent abx: `no amoxicillin in (the )?(past|prior) 30 days` / `no antibiotics in (the )?past 30 days`
- follow-up: `reliable follow[- ]up`
- daycare: `daycare`
- single: `single (mother|mom|parent)`
- under 2: `under 2|<2 year|<24 month`
