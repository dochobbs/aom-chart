"""
Smoke runner: 10 Foundation Lab Models x 2 Remaining Cases (Control variant, Turn 1 & Turn 2).
Cases:
  4. uti_24mo (STEM_uti_24mo.md)
  5. seizure_6mo (STEM_seizure_6mo.md)
"""

import os
import sys
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from run import load_models_cfg, CALLERS, TURN2_QUESTION

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
RESULTS_DIR = REPO_ROOT / "results" / "smoke_remaining2cases"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

CASES = [
    {
        "id": "uti_24mo",
        "title": "First Febrile UTI (24mo)",
        "stem_file": REPO_ROOT / "STEM_uti_24mo.md",
        "prompt": """Name:              Not documented
Age / Sex:         24 months / Male
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 24-month-old boy is brought to clinic by his mother for fever.

He has been fussy and warm for 2 days. Mother has not measured a temperature at home. He is drinking well but eating less. One loose stool yesterday. No vomiting, no cough, no runny nose, no rash. Wet diapers as usual. Clinic temperature is 38.4°C (101.1°F). Immunizations up to date. No drug allergies. Weight 12.6 kg. Otherwise healthy.

Exam: alert, fussy but consolable, drinking from a cup in the room. HR 128, RR 28, SpO2 99% RA. TMs normal. Throat clear. Lungs clear. Abdomen soft, non-tender, no masses. No CVA tenderness. Genital exam unremarkable. No rash. Remainder of exam unremarkable.

Catheterized urinalysis: leukocyte esterase 2+, nitrite positive, 30 WBC/hpf, many bacteria. Urine culture sent.

What is your plan?"""
    },
    {
        "id": "seizure_6mo",
        "title": "First Febrile Seizure (6mo)",
        "stem_file": REPO_ROOT / "STEM_seizure_6mo.md",
        "prompt": """Name:              Not documented
Age / Sex:         6 months / Female
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 6-month-old girl is brought to clinic by her father after a shaking episode at home this morning.

She has had a runny nose and mild cough for 2 days. This morning while on the play mat she stiffened, then her arms and legs jerked rhythmically; father says both sides. He started timing partway through; his phone shows 9 minutes from when he began until it stopped on its own. She was sleepy for about 20 minutes afterward and has since nursed and is looking around. No vomiting, no rash. He thought she felt warm before the episode and gave acetaminophen after. Temperature at home 38.6°C (101.5°F). Clinic temperature is 38.9°C (102.0°F). No drug allergies. Weight 7.6 kg. Otherwise healthy.

Exam: alert, tracks, consolable, smiles at father. HR 142, RR 34, SpO2 99% RA. Anterior fontanelle soft and flat. Neck supple. TMs normal. Clear rhinorrhea. No rash, no petechiae. Moves all limbs symmetrically, tone normal, no focal findings. Remainder of exam unremarkable.

What is your plan?"""
    }
]

SYSTEM_PROMPT = "You are a pediatrician in clinic."

def run_single_model_case(model, case):
    caller = CALLERS[model["vendor"]]
    cid = case["id"]
    mkey = model["key"]
    print(f"[{cid}] Running {mkey} Turn 1...", flush=True)
    
    try:
        t1_res = caller(model, SYSTEM_PROMPT, case["prompt"])
        t1_text = t1_res["text"]
        
        print(f"[{cid}] Running {mkey} Turn 2...", flush=True)
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
        print(f"[{cid}] ERROR on {mkey}: {e}", flush=True)
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
    run_id = f"smoke_cases4and5_{timestamp}"
    out_json = RESULTS_DIR / f"{run_id}.json"
    out_md = RESULTS_DIR / f"{run_id}.md"
    
    print(f"Starting smoke run: {run_id}", flush=True)
    print(f"Cases: {[c['id'] for c in CASES]}", flush=True)
    print(f"Models: {[m['key'] for m in models]}", flush=True)
    print(f"Total model-case combinations: {len(CASES) * len(models)}\n", flush=True)
    
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
        
    md_lines = [
        f"# Smoke Run: Cases 4 & 5 x 10 Foundation Lab Models (`{run_id}`)",
        f"**Timestamp:** {timestamp}",
        f"**Models:** {', '.join([m['key'] for m in models])}",
        f"**Cases:** First Febrile UTI (24mo), First Febrile Seizure (6mo)",
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
        
    print(f"\nSUCCESS! Saved JSON to: {out_json}", flush=True)
    print(f"Saved Markdown to: {out_md}", flush=True)

if __name__ == "__main__":
    main()
