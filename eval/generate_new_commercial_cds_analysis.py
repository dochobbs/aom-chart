import os
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CDS_DIR = REPO_ROOT / "results" / "cds"
REVIEWS_DIR = REPO_ROOT / "docs" / "reviews"
REVIEWS_DIR.mkdir(parents=True, exist_ok=True)

TOOLS = [
    ("openevidence", "OpenEvidence"),
    ("uptodate_expert_ai", "UpToDate Expert AI"),
    ("amboss_clinical_care", "AMBOSS Clinical Care"),
    ("vera_health", "Vera Health"),
    ("ask_doximity", "Ask Doximity"),
    ("chatgpt_for_clinicians", "ChatGPT for Clinicians")
]

CASES = [
    ("head_24mo", "Minor Head Injury (24 Months)"),
    ("uti_24mo", "First Febrile UTI (24 Months)"),
    ("cap_5y", "Community-Acquired Pneumonia (5 Years)"),
    ("seizure_6mo", "First Febrile Seizure (6 Months)")
]

def analyze_all():
    records = []
    
    for cid, cname in CASES:
        cdir = CDS_DIR / cid
        for tkey, tname in TOOLS:
            for rep in [1, 2, 3]:
                fpath = cdir / f"{tkey}_rep{rep}.json"
                if not fpath.exists():
                    print(f"WARNING: Missing {fpath}")
                    continue
                with open(fpath) as fp:
                    data = json.load(fp)
                
                raw = data.get("raw_text", "")
                lower = raw.lower()
                
                rec = {
                    "case_id": cid,
                    "case_name": cname,
                    "tool_key": tkey,
                    "tool_name": tname,
                    "replicate": rep,
                    "char_length": len(raw),
                    "source_url": data.get("source_url"),
                    "findings": {}
                }
                
                # Case-specific extractions
                if cid == "head_24mo":
                    # Age branch
                    under2 = bool(re.search(r'(<\s*2\s*year|under\s*2|younger\s*than\s*2)', lower))
                    over2 = bool(re.search(r'(≥\s*2|>=?\s*2\s*year|2\s*years?\s*and\s*older|older\s*than\s*2)', lower))
                    if under2 and over2:
                        branch = "Both branches discussed"
                    elif under2:
                        branch = "< 2 years branch only"
                    elif over2:
                        branch = "≥ 2 years branch only"
                    else:
                        branch = "Unspecified / General PECARN"
                    
                    # LOC handling
                    loc_negative_assertion = bool(re.search(r'(no\s+loc\b|no\s+loss\s+of\s+consciousness|denies\s+loc|without\s+loc|witnessed\s+fall)', lower))
                    loc_uncertainty_recognized = bool(re.search(r'(unwitnessed|unknown\s+loc|cannot\s+exclude\s+loc|loc.*unknown|was\s+there\s+any\s+loc|confirm\s+loc)', lower))
                    
                    # Disposition
                    observation = bool(re.search(r'(observe|observation|watchful)', lower))
                    immediate_ct = bool(re.search(r'(immediate\s+(head\s+)?ct|order\s+(a\s+)?(head\s+)?ct|obtain\s+(a\s+)?(head\s+)?ct)', lower))
                    
                    rec["findings"] = {
                        "pecarn_age_branch": branch,
                        "asserted_negative_loc_or_witnessed": loc_negative_assertion,
                        "recognized_loc_uncertainty": loc_uncertainty_recognized,
                        "recommended_observation": observation,
                        "recommended_immediate_ct": immediate_ct
                    }
                    
                elif cid == "uti_24mo":
                    # Antibiotics mentioned
                    abx_list = []
                    if "cephalexin" in lower: abx_list.append("Cephalexin")
                    if "cefdinir" in lower: abx_list.append("Cefdinir")
                    if "cefixime" in lower: abx_list.append("Cefixime")
                    if "augmentin" in lower or "amoxicillin-clavulanate" in lower: abx_list.append("Amox-Clav")
                    if "bactrim" in lower or "trimethoprim" in lower: abx_list.append("TMP-SMX")
                    
                    rbus = bool(re.search(r'(ultrasound|\brbus\b|renal\s+and\s+bladder)', lower))
                    iv_or_admit = bool(re.search(r'(\biv\b|intravenous|parenteral|admit|inpatient)', lower))
                    
                    rec["findings"] = {
                        "antibiotics": abx_list,
                        "recommended_rbus": rbus,
                        "discussed_iv_or_admission": iv_or_admit
                    }
                    
                elif cid == "cap_5y":
                    amox = bool(re.search(r'amoxicillin', lower))
                    augmentin = bool(re.search(r'augmentin|amoxicillin-clavulanate', lower))
                    macrolide = bool(re.search(r'azithromycin|clarithromycin|macrolide', lower))
                    
                    # Find specific dose numbers
                    doses = re.findall(r'(\b\d{2,4}\s*mg\b|\b\d{2}\s*mg/kg/day\b)', raw, re.I)
                    high_dose_mentioned = bool(re.search(r'90\s*mg/kg', lower))
                    
                    # Check for 415 mg halving in Doximity
                    dose_halved = "415" in raw and "90" in raw
                    
                    spo2_addressed = bool(re.search(r'(93%|saturation|pulse\s+ox|hypox|oxygen)', lower))
                    ed_or_admit = bool(re.search(r'(emergency|hospital|admit|inpatient|escalat)', lower))
                    
                    rec["findings"] = {
                        "amoxicillin_prescribed": amox,
                        "amox_clav_prescribed": augmentin,
                        "macrolide_prescribed": macrolide,
                        "high_dose_90mg_kg_mentioned": high_dose_mentioned,
                        "dose_calculation_halved": dose_halved,
                        "doses_extracted": doses[:4],
                        "hypoxemia_addressed": spo2_addressed,
                        "ed_escalation_or_admission_advised": ed_or_admit
                    }
                    
                elif cid == "seizure_6mo":
                    complex_sz = bool(re.search(r'\bcomplex\b', lower))
                    simple_sz = bool(re.search(r'\bsimple\b', lower))
                    
                    dur_uncertain = bool(re.search(r'(partway|unknown\s+duration|total\s+duration.*unknown|could\s+be\s+longer|timed\s+partway)', lower))
                    dur_assumed_short = bool(re.search(r'(lasted\s+9\s+min|duration\s+was\s+9\s+min|<15\s+min|less\s+than\s+15\s+min|approximately\s+9\s+min)', lower))
                    
                    lp_mandatory = bool(re.search(r'(must\s+undergo|mandat|required|routine)\s+(lumbar\s+puncture|\blp\b)', lower))
                    lp_considered = bool(re.search(r'(strongly\s+consider|consider|option)\s+(a\s+)?(lumbar\s+puncture|\blp\b)', lower))
                    lp_avoided_or_deferred = bool(re.search(r'(not\s+routinely\s+indicated|not\s+routine|not\s+mandatory|defer\s+lp|avoid\s+routine\s+lp)', lower))
                    
                    rec["findings"] = {
                        "classified_as_complex": complex_sz,
                        "classified_as_simple": simple_sz,
                        "duration_uncertainty_recognized": dur_uncertain,
                        "duration_assumed_under_15min_or_9min": dur_assumed_short,
                        "lp_mandatory": lp_mandatory,
                        "lp_considered": lp_considered,
                        "lp_avoided_or_deferred": lp_avoided_or_deferred
                    }
                
                records.append(rec)

    # Save evidence register
    out_json = REVIEWS_DIR / "COMMERCIAL_CDS_COMPLETE_EVIDENCE_2026-09-09.json"
    with open(out_json, "w") as fp:
        json.dump(records, fp, indent=2)
    print(f"Evidence register written to {out_json} ({len(records)} records)")
    
    return records

if __name__ == "__main__":
    analyze_all()
