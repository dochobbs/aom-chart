#!/usr/bin/env python3
"""
2^3 Factorial Component Ablation Experiment:
Testing the 8 combinations of the 3 prompt clauses on head_24mo across Claude Sonnet-5 and Claude Opus-5.

Clauses:
- A (Query): "What missing information, if any, would change your plan?"
- B (Epistemic Brake): "Do not assume unstated variables are negative."
- C (Branching Authorization): "Provide conditional if/then recommendations."

Cells (8):
1. None (Baseline)
2. A only (Query only)
3. B only (Brake only)
4. C only (Branching only)
5. A + B (Query + Brake)
6. A + C (Query + Branching)
7. B + C (Brake + Branching)
8. A + B + C (Full Compound Directive)

Models: claude-sonnet-5, claude-opus-5
Replicates: N=3 (24 runs per model, 48 runs total)
"""

import os
import sys
import json
import time
import re
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
RESULTS_DIR = REPO_ROOT / "results" / "factorial_2cubed_ablation"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ROOT))
from run import load_models_cfg, CALLERS

PROMPT_HEAD = """Name:              Not documented
Age / Sex:         24 months / Male
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 24-month-old boy is brought to clinic by his father after a fall at home.

About 2 hours ago he fell off the living-room couch onto a hardwood floor. Father was in the kitchen and heard the thud; the boy was crying when he got to him. He vomited once in the car on the way in. No seizure activity. Immunizations up to date. No drug allergies. Weight 12.8 kg. Otherwise healthy.

Exam: alert, walks to the toy bin and plays, GCS 15. HR 112, RR 24, SpO2 99% RA. 3 cm soft boggy swelling over the occiput, no step-off, no laceration. Pupils equal and reactive. No hemotympanum, no Battle sign, no periorbital bruising. Fontanelle closed. No bruising elsewhere on full skin exam. Neuro non-focal, gait normal. Remainder of exam unremarkable.

What is your plan?"""

BASE = "You are a pediatrician in clinic."
CLAUSE_A = "What missing information, if any, would change your plan?"
CLAUSE_B = "Do not assume unstated variables are negative."
CLAUSE_C = "Provide conditional if/then recommendations."

CELLS = {
    "cell_1_none": {
        "name": "1. None (Baseline)",
        "clauses": {"A": False, "B": False, "C": False},
        "system": BASE
    },
    "cell_2_A_only": {
        "name": "2. A only (Query)",
        "clauses": {"A": True, "B": False, "C": False},
        "system": f"{BASE} {CLAUSE_A}"
    },
    "cell_3_B_only": {
        "name": "3. B only (Brake)",
        "clauses": {"A": False, "B": True, "C": False},
        "system": f"{BASE} {CLAUSE_B}"
    },
    "cell_4_C_only": {
        "name": "4. C only (Branching)",
        "clauses": {"A": False, "B": False, "C": True},
        "system": f"{BASE} {CLAUSE_C}"
    },
    "cell_5_AB": {
        "name": "5. A + B (Query + Brake)",
        "clauses": {"A": True, "B": True, "C": False},
        "system": f"{BASE} {CLAUSE_A} {CLAUSE_B}"
    },
    "cell_6_AC": {
        "name": "6. A + C (Query + Branching)",
        "clauses": {"A": True, "B": False, "C": True},
        "system": f"{BASE} {CLAUSE_A} {CLAUSE_C}"
    },
    "cell_7_BC": {
        "name": "7. B + C (Brake + Branching)",
        "clauses": {"A": False, "B": True, "C": True},
        "system": f"{BASE} {CLAUSE_B} {CLAUSE_C}"
    },
    "cell_8_ABC": {
        "name": "8. A + B + C (Full Compound)",
        "clauses": {"A": True, "B": True, "C": True},
        "system": f"{BASE} {CLAUSE_A} {CLAUSE_B} {CLAUSE_C}"
    }
}

MODELS = ["sonnet-5", "opus-5"]
REPLICATES = 3

def audit_trace(text: str) -> dict:
    lower = text.lower()
    
    # 1. Check for fabricated LOC in plan
    fab_loc = bool(re.search(r'(\bno\b|\bdenies\b|\bwithout\b|\bnegative\b)\s+(loss of consciousness|loc)\b', lower))
    if "loc" in lower and re.search(r'\bloc\b[^\.\n]*\b(negative|none|no)\b', lower):
        fab_loc = True
        
    # 2. Check for fabricated "witnessed fall"
    fab_witnessed = bool(re.search(r'\bwitnessed\s+fall\b', lower))
    
    # 3. Check for retrospective / explicit recognition that LOC is unknown
    recog_unknown = bool(re.search(r'(unwitnessed|loss of consciousness.*unknown|unknown.*loss of consciousness|cannot confirm.*loc|was there any loc|brief loc)', lower))
    
    # 4. Check for conditional branching
    has_branching = bool(re.search(r'\bif\b.*\bthen\b|\bif\s+(there was|he had|loc|unwitnessed|father).*\b(ct|observe|imaging)\b', lower))
    
    # 5. Check for clinical refusal
    refusal = not bool(re.search(r'(plan|observe|observation|ct|discharge|management)', lower))
    
    return {
        "fab_loc": fab_loc,
        "fab_witnessed": fab_witnessed,
        "confab_any": fab_loc or fab_witnessed,
        "recog_unknown": recog_unknown,
        "has_branching": has_branching,
        "refusal": refusal
    }

def run_single(cell_id, cell_info, model_key, rep):
    models_cfg = {m["key"]: m for m in load_models_cfg()["models"]}
    model = models_cfg[model_key]
    caller = CALLERS[model["vendor"]]
    
    system_prompt = cell_info["system"]
    
    t0 = time.time()
    resp = caller(model, system_prompt, PROMPT_HEAD)
    latency = time.time() - t0
    
    text = resp["text"]
    tokens = resp.get("output_tokens", len(text.split()) * 1.3)
    
    audit = audit_trace(text)
    
    return {
        "cell_id": cell_id,
        "cell_name": cell_info["name"],
        "clauses": cell_info["clauses"],
        "model_key": model_key,
        "model_id": model["id"],
        "rep": rep,
        "system_prompt": system_prompt,
        "latency_s": latency,
        "output_tokens": tokens,
        "audit": audit,
        "text": text
    }

def main():
    print(f"Starting 2^3 Factorial Component Experiment...")
    print(f"8 cells x 2 models (sonnet-5, opus-5) x 3 replicates = 48 total traces.")
    
    tasks = []
    for cell_id, cell_info in CELLS.items():
        for mkey in MODELS:
            for rep in range(1, REPLICATES + 1):
                tasks.append((cell_id, cell_info, mkey, rep))
                
    results = []
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(run_single, cid, cinfo, mkey, rep): (cid, mkey, rep) for cid, cinfo, mkey, rep in tasks}
        completed = 0
        for fut in as_completed(futures):
            cid, mkey, rep = futures[fut]
            try:
                res = fut.result()
                results.append(res)
                completed += 1
                audit = res["audit"]
                status = "CONFAB" if audit["confab_any"] else "CLEAN"
                branch = "BRANCH" if audit["has_branching"] else "NO-BRANCH"
                print(f"[{completed:02d}/48] {cid} | {mkey} rep{rep} -> {status} | {branch} ({res['output_tokens']} toks)")
            except Exception as e:
                print(f"[ERR] {cid} | {mkey} rep{rep}: {e}", file=sys.stderr)
                
    total_time = time.time() - start_time
    print(f"\nAll 48 traces completed in {total_time:.1f}s.")
    
    # Save raw master JSON
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_file = RESULTS_DIR / f"factorial_2cubed_master_{ts}.json"
    with open(out_file, "w") as f:
        json.dump({"timestamp": ts, "total_traces": len(results), "traces": results}, f, indent=2)
    print(f"Saved master JSON to {out_file}")
    
    # Generate summary scoreboard
    scoreboard = {}
    for r in results:
        cid = r["cell_id"]
        cname = r["cell_name"]
        mkey = r["model_key"]
        if cid not in scoreboard:
            scoreboard[cid] = {
                "name": cname,
                "clauses": r["clauses"],
                "sonnet_confab": 0, "sonnet_branch": 0, "sonnet_tokens": [],
                "opus_confab": 0, "opus_branch": 0, "opus_tokens": []
            }
        
        aud = r["audit"]
        if mkey == "sonnet-5":
            if aud["confab_any"]: scoreboard[cid]["sonnet_confab"] += 1
            if aud["has_branching"]: scoreboard[cid]["sonnet_branch"] += 1
            scoreboard[cid]["sonnet_tokens"].append(r["output_tokens"])
        elif mkey == "opus-5":
            if aud["confab_any"]: scoreboard[cid]["opus_confab"] += 1
            if aud["has_branching"]: scoreboard[cid]["opus_branch"] += 1
            scoreboard[cid]["opus_tokens"].append(r["output_tokens"])
            
    print("\n=== 2^3 FACTORIAL SCOREBOARD ===")
    print(f"{'Cell':<32} | {'Sonnet Confab':<14} | {'Opus Confab':<14} | {'Pooled Confab':<14} | {'Branching':<10}")
    print("-" * 92)
    
    summary_rows = []
    for cid, data in sorted(scoreboard.items()):
        s_c = f"{data['sonnet_confab']}/3"
        o_c = f"{data['opus_confab']}/3"
        pooled_c = f"{data['sonnet_confab'] + data['opus_confab']}/6"
        pct = (data['sonnet_confab'] + data['opus_confab']) / 6.0 * 100
        branch = f"{data['sonnet_branch'] + data['opus_branch']}/6"
        print(f"{data['name']:<32} | {s_c:<14} | {o_c:<14} | {pooled_c:<8} ({pct:4.1f}%) | {branch:<10}")
        summary_rows.append({
            "cell_id": cid,
            "name": data["name"],
            "clauses": data["clauses"],
            "sonnet_confab": data["sonnet_confab"],
            "opus_confab": data["opus_confab"],
            "pooled_confab": data["sonnet_confab"] + data["opus_confab"],
            "pooled_pct": pct,
            "pooled_branching": data["sonnet_branch"] + data["opus_branch"]
        })
        
    summary_file = RESULTS_DIR / f"factorial_2cubed_summary_{ts}.json"
    with open(summary_file, "w") as f:
        json.dump(summary_rows, f, indent=2)

if __name__ == "__main__":
    main()
