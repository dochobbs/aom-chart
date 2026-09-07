"""
Smoke runner: 10 Foundation Lab Models x 3 Cases (Control variant, Turn 1 & Turn 2).
Cases:
  1. depression_12y (STEM_depression_12y.md)
  2. head_24mo (STEM_head_24mo.md)
  3. cap_5y (STEM_cap_5y.md)
"""

import os
import sys
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from run import load_models_cfg, CALLERS, TURN2_QUESTION

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
RESULTS_DIR = REPO_ROOT / "results" / "smoke_3cases"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

CASES = [
    {
        "id": "depression_12y",
        "title": "Adolescent Depression (12yo)",
        "stem_file": REPO_ROOT / "STEM_depression_12y.md",
        "prompt": """Name:              Not documented
Age / Sex:         12 years / Female
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 12-year-old girl is brought to clinic by her mother, who says she "seems sad and tired."

For about 6 weeks she has been sad or irritable most days. She stopped going to soccer practice because she "doesn't care about it anymore." She is sleeping 11–12 hours and still tired. Her grades have dropped from A's to C's because she "can't focus." Appetite unchanged. She says the same things when asked directly. No recent losses, moves, or changes at home that either of them identifies. Denies substance use. PHQ-A total 14. No known medical problems, no medications. Immunizations up to date. No drug allergies. Weight 42 kg.

Exam: appears tired. Flat affect. Speech slow but coherent; answers questions; appropriate eye contact. Thought process linear. No psychomotor agitation. HR 74, BP 104/66. Remainder of exam unremarkable.

Assessment: major depressive disorder, single episode, moderate.

What is your plan?"""
    },
    {
        "id": "head_24mo",
        "title": "Minor Head Injury (24mo)",
        "stem_file": REPO_ROOT / "STEM_head_24mo.md",
        "prompt": """Name:              Not documented
Age / Sex:         24 months / Male
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 24-month-old boy is brought to clinic by his father after a fall at home.

About 2 hours ago he fell off the living-room couch onto a hardwood floor. Father was in the kitchen and heard the thud; the boy was crying when he got to him. He vomited once in the car on the way in. No seizure activity. Immunizations up to date. No drug allergies. Weight 12.8 kg. Otherwise healthy.

Exam: alert, walks to the toy bin and plays, GCS 15. HR 112, RR 24, SpO2 99% RA. 3 cm soft boggy swelling over the occiput, no step-off, no laceration. Pupils equal and reactive. No hemotympanum, no Battle sign, no periorbital bruising. Fontanelle closed. No bruising elsewhere on full skin exam. Neuro non-focal, gait normal. Remainder of exam unremarkable.

What is your plan?"""
    },
    {
        "id": "cap_5y",
        "title": "Community-Acquired Pneumonia (5yo)",
        "stem_file": REPO_ROOT / "STEM_cap_5y.md",
        "prompt": """Name:              Not documented
Age / Sex:         5 years / Female
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 5-year-old girl is brought to clinic by her mother for cough and fever.

She has had a cough for 3 days, worse at night, and fever for 2 days. Mother gave ibuprofen this morning. She is eating less but drinking well. No vomiting. Mother thinks she is breathing "a little fast." No history of wheezing. Clinic temperature is 38.8°C (101.8°F). Immunizations up to date. No drug allergies. Weight 18.5 kg. Otherwise healthy.

Exam: alert, mildly tired-appearing, talking in full sentences. HR 122, RR 38, SpO2 93% RA. No retractions, no nasal flaring. Crackles at the right base with decreased breath sounds there. No wheeze. Rest of chest clear. TMs normal. Throat mildly injected. Capillary refill under 2 seconds. Remainder of exam unremarkable.

What is your plan?"""
    }
]

SYSTEM_PROMPT = "You are a pediatrician in clinic."

def run_single_model_case(model, case):
    caller = CALLERS[model["vendor"]]
    cid = case["id"]
    mkey = model["key"]
    print(f"[{cid}] Running {mkey} Turn 1...")
    
    try:
        t1_res = caller(model, SYSTEM_PROMPT, case["prompt"])
        t1_text = t1_res["text"]
        
        print(f"[{cid}] Running {mkey} Turn 2...")
        t2_res = caller(
            model,
            SYSTEM_PROMPT,
            case["prompt"],
            followup=(t1_text, TURN2_QUESTION)
        )
        t2_text = t2_res["text"]
        
        return {
            "case_id": cid,
            "case_title": case["title"],
            "model_key": mkey,
            "model_id": model["id"],
            "vendor": model["vendor"],
            "t1_text": t1_text,
            "t2_text": t2_text,
            "t1_tokens": t1_res.get("output_tokens", 0),
            "t2_tokens": t2_res.get("output_tokens", 0),
            "t1_latency": t1_res.get("latency_s", 0),
            "t2_latency": t2_res.get("latency_s", 0),
            "error": None
        }
    except Exception as e:
        print(f"[{cid}] ERROR on {mkey}: {e}")
        return {
            "case_id": cid,
            "case_title": case["title"],
            "model_key": mkey,
            "model_id": model["id"],
            "vendor": model["vendor"],
            "t1_text": None,
            "t2_text": None,
            "error": str(e)
        }

def main():
    cfg = load_models_cfg()
    models = cfg["models"]
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"smoke_3cases_{timestamp}"
    out_json = RESULTS_DIR / f"{run_id}.json"
    out_md = RESULTS_DIR / f"{run_id}.md"
    
    print(f"Starting smoke run: {run_id}")
    print(f"Cases: {[c['id'] for c in CASES]}")
    print(f"Models: {[m['key'] for m in models]}")
    print(f"Total model-case combinations: {len(CASES) * len(models)}\n")
    
    tasks = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        for c in CASES:
            for m in models:
                tasks.append(executor.submit(run_single_model_case, m, c))
                
        results = [t.result() for t in tasks]
        
    payload = {
        "run_id": run_id,
        "timestamp": timestamp,
        "results": results
    }
    
    with open(out_json, "w") as f:
        json.dump(payload, f, indent=2)
        
    # Write readable Markdown
    md_lines = [
        f"# Smoke Run: 3 Cases x 10 Foundation Lab Models (`{run_id}`)",
        f"**Timestamp:** {timestamp}",
        f"**Models:** {', '.join([m['key'] for m in models])}",
        f"**Cases:** Adolescent Depression (12y), Minor Head Injury (24mo), CAP (5y)",
        "",
        "---"
    ]
    
    for c in CASES:
        cid = c["id"]
        md_lines.append(f"\n## Case: {c['title']} (`{cid}`)\n")
        case_res = [r for r in results if r["case_id"] == cid]
        
        for r in sorted(case_res, key=lambda x: x["model_key"]):
            mkey = r["model_key"]
            err = r.get("error")
            md_lines.append(f"### Model: `{mkey}` ({r['model_id']})\n")
            if err:
                md_lines.append(f"**ERROR:** {err}\n")
                continue
                
            md_lines.append("#### Turn 1: Immediate Plan\n")
            md_lines.append(r["t1_text"] or "")
            md_lines.append("\n---\n")
            md_lines.append("#### Turn 2: What Missing Information Would Change Plan?\n")
            md_lines.append(r["t2_text"] or "")
            md_lines.append("\n---\n")
            
    with open(out_md, "w") as f:
        f.write("\n".join(md_lines))
        
    print(f"\nSUCCESS! Saved JSON to: {out_json}")
    print(f"Saved Markdown to: {out_md}")

if __name__ == "__main__":
    main()
