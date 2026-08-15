# Disagreements — buddy vs Grok on `smoke_20260815T160303Z.json`

Doc resolves `plan`, `followup_hallucinated`, `reliability_language`, `age_stratum`, failure yes/no.

## fable-5 `control` r1

fields: followup_stance, followup_hallucinated, reliability_language, rule_error

- followup_stance: grok=assume_reliable buddy=ask
- followup_hallucinated: grok=yes buddy=no
- reliability_language: grok=no buddy=yes
- rule_error: grok={'yes': 'yes', 'items': [{'what': '10-day course in ≥24 mo mild band', 'quote': '10 days'}]} buddy={'yes': 'no', 'what': None, 'quote': None}

your call:

## fable-5 `control` r2

fields: reliability_language, rule_error

- reliability_language: grok=no buddy=yes
- rule_error: grok={'yes': 'no'} buddy={'yes': 'yes', 'what': 'Observation is selected while assuming reliable follow-up without establishing it from the prompt.', 'quote': 'since reliable follow-up is possible'}

your call:

## gemini-flash `control` r1

fields: plan, reliability_language

- plan: grok=observe buddy=either
- reliability_language: grok=no buddy=yes

your call:

## gemini-flash `control` r2

fields: snap

- snap: grok=no buddy=yes

**Plan is settled: treat.** Flash led with “First-line: High-dose Amoxicillin” and a fill-today script. WASP is only a discuss-option. Snap leftover is minor (WASP mentioned vs issued).

Gemini Pro control r1: buddy still failed to return JSON after retry.
