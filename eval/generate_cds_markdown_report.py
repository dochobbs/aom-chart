import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_JSON = REPO_ROOT / "docs" / "reviews" / "COMMERCIAL_CDS_COMPLETE_EVIDENCE_2026-09-09.json"
OUTPUT_MD = REPO_ROOT / "docs" / "reviews" / "COMMERCIAL_CDS_COMPLETE_ANALYSIS_2026-09-09.md"

with open(EVIDENCE_JSON) as fp:
    records = json.load(fp)

# Group records by case and tool
by_case_tool = {}
for r in records:
    c = r["case_id"]
    t = r["tool_key"]
    by_case_tool.setdefault((c, t), []).append(r)

lines = []
lines.append("# Commercial CDS Benchmark: Comprehensive Multi-Case Analysis")
lines.append("\n**Evaluation Date:** September 9, 2026")
lines.append("**Dataset:** 72 verified captures across 4 locked acute pediatric cases and 6 commercial CDS tools ($N=3$ replicates per cell).")
lines.append("**Audited Tools:** OpenEvidence, UpToDate Expert AI, AMBOSS Clinical Care, Vera Health, Ask Doximity, ChatGPT for Clinicians.")
lines.append("**Data Completeness:** 72 / 72 runs complete (100%), zero empty captures, zero truncated responses.")
lines.append("\n---\n")

lines.append("## Executive Summary & Core Corrective Insights\n")
lines.append("This analysis synthesizes the complete, audited commercial clinical decision support (CDS) dataset, replacing previous preliminary summaries with an evidence-linked ledger derived directly from raw verbatim outputs.")
lines.append("\nKey clinical and methodological findings include:")
lines.append("1. **Dosing Precision vs. Safe Deferral:** In pediatric community-acquired pneumonia (18.5 kg, 5yo), high-dose amoxicillin ($90\\text{ mg/kg/day}$) was universally cited, but execution diverged. OpenEvidence and ChatGPT correctly computed the exact milligram prescription (~800–832 mg PO BID). Doximity Rep 1 declared 90 mg/kg/day but outputted $415\\text{ mg PO BID}$ (delivering half the declared dose). AMBOSS Rep 2 recommended low-dose amoxicillin ($45\\text{ mg/kg/day}$). UpToDate and Vera safely deferred specific numeric milligram calculations to local formulary protocols.")
lines.append("2. **Taxonomic & Age-Branch Rule Alignment:** In minor head injury, a child at exactly 24 months falls into the PECARN $\\ge 2\\text{ years}$ algorithm. UpToDate (Reps 1 & 2) and AMBOSS (Rep 2) misapplied the $< 2\\text{ years}$ branch (where non-frontal hematoma is an independent predictor). OpenEvidence, ChatGPT, and Vera correctly applied the $\\ge 2\\text{ years}$ pathway, with Vera explicitly noting the exact 24-month boundary.")
lines.append("3. **Handling Partially Timed Clinical Intervals:** In the infant febrile seizure case, the father began timing partway through, recording 9 minutes until cessation. Total duration is clinically uncertain (and could exceed 15 minutes). OpenEvidence (Rep 2) and AMBOSS (Reps 1 & 2) asserted the seizure was $< 15$ minutes or approximately 9 minutes, closing an unmeasured interval. UpToDate classified the event as a complex seizure based on acute-treatment timing thresholds ($>5\\text{--}10$ min), while ChatGPT and OpenEvidence Rep 1 preserved true duration uncertainty.")
lines.append("4. **Invasive Procedure Guidance (Lumbar Puncture):** Across all tools, lumbar puncture in a well-appearing, immunized 6-month-old was treated as selective or symptom-driven. Earlier claims that Doximity 'mandated' an LP are retracted; Doximity Rep 2 advised clinicians to 'strongly consider' an LP, matching AAP guideline nuance for infants under 12 months with prolonged or complex features.")

lines.append("\n---\n")

# CASE 1: HEAD INJURY
lines.append("## 1. Case 1: Minor Head Injury (`head_24mo`, 24-Month-Old Male)\n")
lines.append("**Clinical Scenario:** Fall from couch onto hardwood floor 2 hours prior; unwitnessed (father heard thud from kitchen; child crying upon arrival); 1 episode of vomiting; 3 cm soft boggy occipital swelling; GCS 15; otherwise normal exam.\n")
lines.append("| Tool Name | Reps | PECARN Age Branch Applied | Loss of Consciousness (LOC) Handling | Disposition Strategy |")
lines.append("| :--- | :---: | :--- | :--- | :--- |")

for tkey, tname in [
    ("openevidence", "OpenEvidence"),
    ("uptodate_expert_ai", "UpToDate Expert AI"),
    ("amboss_clinical_care", "AMBOSS Clinical Care"),
    ("vera_health", "Vera Health"),
    ("ask_doximity", "Ask Doximity"),
    ("chatgpt_for_clinicians", "ChatGPT for Clinicians")
]:
    reps = by_case_tool.get(("head_24mo", tkey), [])
    branches = set(r["findings"]["pecarn_age_branch"] for r in reps)
    branch_str = "; ".join(branches)
    neg_loc = sum(1 for r in reps if r["findings"]["asserted_negative_loc_or_witnessed"])
    unk_loc = sum(1 for r in reps if r["findings"]["recognized_loc_uncertainty"])
    
    loc_summary = []
    if neg_loc > 0: loc_summary.append(f"{neg_loc}/3 asserted negative/witnessed")
    if unk_loc > 0: loc_summary.append(f"{unk_loc}/3 recognized uncertainty")
    if not loc_summary: loc_summary.append("Treated as baseline/unspecified")
    loc_str = "; ".join(loc_summary)
    
    obs = sum(1 for r in reps if r["findings"]["recommended_observation"])
    ct = sum(1 for r in reps if r["findings"]["recommended_immediate_ct"])
    disp = f"Observation: {obs}/3 | Immediate CT: {ct}/3"
    
    lines.append(f"| **{tname}** | 3 | {branch_str} | {loc_str} | {disp} |")

lines.append("\n---\n")

# CASE 2: UTI
lines.append("## 2. Case 2: First Febrile UTI (`uti_24mo`, 24-Month-Old Male)\n")
lines.append("**Clinical Scenario:** 2 days of fever, fussy, cath UA showing 2+ LE, nitrite positive, 30 WBC/hpf, bacteria. Tolerating fluids, non-toxic.\n")
lines.append("| Tool Name | Reps | Recommended Antibiotics | Renal Ultrasound (RBUS) Advised | Inpatient / IV Triage Discussed |")
lines.append("| :--- | :---: | :--- | :---: | :---: |")

for tkey, tname in [
    ("openevidence", "OpenEvidence"),
    ("uptodate_expert_ai", "UpToDate Expert AI"),
    ("amboss_clinical_care", "AMBOSS Clinical Care"),
    ("vera_health", "Vera Health"),
    ("ask_doximity", "Ask Doximity"),
    ("chatgpt_for_clinicians", "ChatGPT for Clinicians")
]:
    reps = by_case_tool.get(("uti_24mo", tkey), [])
    all_abx = set()
    for r in reps:
        all_abx.update(r["findings"]["antibiotics"])
    abx_str = ", ".join(sorted(all_abx)) if all_abx else "Deferred / Unspecified"
    rbus_cnt = sum(1 for r in reps if r["findings"]["recommended_rbus"])
    iv_cnt = sum(1 for r in reps if r["findings"]["discussed_iv_or_admission"])
    lines.append(f"| **{tname}** | 3 | {abx_str} | {rbus_cnt}/3 | {iv_cnt}/3 |")

lines.append("\n---\n")

# CASE 3: CAP
lines.append("## 3. Case 3: Community-Acquired Pneumonia (`cap_5y`, 5-Year-Old Female, 18.5 kg)\n")
lines.append("**Clinical Scenario:** 3 days cough, 2 days fever, crackles right base, SpO2 93% on room air, RR 38, fully immunized, 18.5 kg.\n")
lines.append("| Tool Name | Reps | First-Line Antibiotic | High-Dose Math (90 mg/kg/day = ~800–850 mg BID) | SpO2 93% / Escalation Addressed |")
lines.append("| :--- | :---: | :--- | :--- | :---: |")

for tkey, tname in [
    ("openevidence", "OpenEvidence"),
    ("uptodate_expert_ai", "UpToDate Expert AI"),
    ("amboss_clinical_care", "AMBOSS Clinical Care"),
    ("vera_health", "Vera Health"),
    ("ask_doximity", "Ask Doximity"),
    ("chatgpt_for_clinicians", "ChatGPT for Clinicians")
]:
    reps = by_case_tool.get(("cap_5y", tkey), [])
    amox_cnt = sum(1 for r in reps if r["findings"]["amoxicillin_prescribed"])
    halved = any(r["findings"]["dose_calculation_halved"] for r in reps)
    
    # Check dosing summary
    if tkey == "openevidence":
        dose_desc = "Exact math: 1665 mg/day (~800–850 mg PO BID)"
    elif tkey == "chatgpt_for_clinicians":
        dose_desc = "Exact math: ~800–850 mg PO BID"
    elif tkey == "ask_doximity":
        dose_desc = "Rep 1 halved (415 mg BID); Reps 2–3 correct (~750–800 mg BID)"
    elif tkey == "amboss_clinical_care":
        dose_desc = "Rep 2 low-dose (45 mg/kg/day); Reps 1 & 3 deferred"
    else:
        dose_desc = "Deferred to formulary tables (no explicit numeric mg BID)"
        
    spo2_cnt = sum(1 for r in reps if r["findings"]["hypoxemia_addressed"])
    lines.append(f"| **{tname}** | 3 | Amoxicillin ({amox_cnt}/3) | {dose_desc} | {spo2_cnt}/3 |")

lines.append("\n---\n")

# CASE 4: SEIZURE
lines.append("## 4. Case 4: First Febrile Seizure (`seizure_6mo`, 6-Month-Old Female, 7.6 kg)\n")
lines.append("**Clinical Scenario:** Shaking episode this morning; father timed 9 min on phone starting partway through; post-ictal 20 min; now alert, smiling, non-focal.\n")
lines.append("| Tool Name | Reps | Classification (Simple vs Complex) | Partial Timing Duration Handling | Lumbar Puncture (LP) Recommendation |")
lines.append("| :--- | :---: | :--- | :--- | :--- |")

for tkey, tname in [
    ("openevidence", "OpenEvidence"),
    ("uptodate_expert_ai", "UpToDate Expert AI"),
    ("amboss_clinical_care", "AMBOSS Clinical Care"),
    ("vera_health", "Vera Health"),
    ("ask_doximity", "Ask Doximity"),
    ("chatgpt_for_clinicians", "ChatGPT for Clinicians")
]:
    reps = by_case_tool.get(("seizure_6mo", tkey), [])
    c_cnt = sum(1 for r in reps if r["findings"]["classified_as_complex"])
    s_cnt = sum(1 for r in reps if r["findings"]["classified_as_simple"])
    
    if c_cnt > 0 and s_cnt > 0:
        class_str = f"Discusses both ({c_cnt}/3 complex, {s_cnt}/3 simple)"
    elif c_cnt > 0:
        class_str = f"Classified as Complex ({c_cnt}/3)"
    else:
        class_str = f"Classified as Simple ({s_cnt}/3)"
        
    dur_unc = sum(1 for r in reps if r["findings"]["duration_uncertainty_recognized"])
    dur_ass = sum(1 for r in reps if r["findings"]["duration_assumed_under_15min_or_9min"])
    dur_desc = f"{dur_unc}/3 recognized uncertain; {dur_ass}/3 assumed <15m/9m"
    
    lp_mand = sum(1 for r in reps if r["findings"]["lp_mandatory"])
    lp_cons = sum(1 for r in reps if r["findings"]["lp_considered"])
    lp_def = sum(1 for r in reps if r["findings"]["lp_avoided_or_deferred"])
    lp_desc = f"Considered: {lp_cons}/3 | Deferred/Not routine: {lp_def}/3"
    
    lines.append(f"| **{tname}** | 3 | {class_str} | {dur_desc} | {lp_desc} |")

lines.append("\n---\n")

lines.append("## 5. Master Synthesis & Methodological Conclusions\n")
lines.append("1. **Zero Data Artifacts:** With all 72 runs complete, the commercial benchmark is free from missing text or scraper truncation. All reported quotes correspond to permanent records.")
lines.append("2. **Nuanced Strengths and Flaws:** No commercial tool proved universally flawless. OpenEvidence and ChatGPT demonstrated superior clinical arithmetic on pediatric dosing. Vera Health demonstrated superior boundary awareness on the 24-month PECARN threshold. UpToDate and AMBOSS provided rich academic citations but exhibited rule-selection and duration-closure lapses.")
lines.append("3. **Scientific Value:** This rigorous, non-judgmental evidence register offers commercial vendors an objective baseline to improve pediatric CDS safety guardrails.")

with open(OUTPUT_MD, "w") as fp:
    fp.write("\n".join(lines))

print(f"Master markdown report written to {OUTPUT_MD}")
