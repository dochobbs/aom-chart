#!/usr/bin/env python3
"""
Re-run and heal truncated foundation runs in results/mitigation_4cases:
- Index 5: Opus-5 on head_24mo
- Index 34: Sonnet-5 on seizure_6mo (previously empty text due to token starvation)
- Index 35: Opus-5 on seizure_6mo
All run with max_tokens=8192.
"""

import sys
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

from run import load_models_cfg, CALLERS, TURN2_QUESTION
from run_4cases_mitigation import CASES, SYSTEM_PROMPT, run_single_mitigation_task

MITIGATION_DIR = REPO_ROOT / "results" / "mitigation_4cases"
TARGET_JSON = MITIGATION_DIR / "mitigation_4cases_20260907T030903Z.json"
TARGET_MD = MITIGATION_DIR / "mitigation_4cases_20260907T030903Z.md"
BACKUP_JSON = MITIGATION_DIR / "mitigation_4cases_20260907T030903Z.bak.json"

def main():
    if not TARGET_JSON.exists():
        print(f"Error: {TARGET_JSON} not found!")
        sys.exit(1)
        
    if not BACKUP_JSON.exists():
        shutil.copyfile(TARGET_JSON, BACKUP_JSON)
        print(f"Created backup at {BACKUP_JSON}")
        
    with open(TARGET_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    results = data.get("results", [])
    models_by_key = {m["key"]: m for m in load_models_cfg()["models"]}
    cases_by_id = {c["id"]: c for c in CASES}
    
    # Indices to heal: 5, 34, 35
    repair_targets = [5, 34, 35]
    print(f"Starting healing of {len(repair_targets)} truncated/empty traces in mitigation_4cases...\n")
    
    for idx in repair_targets:
        old_row = results[idx]
        mkey = old_row["model_key"]
        cid = old_row["case_id"]
        print(f"--- Re-running Idx {idx}: {mkey} on {cid} (was t1_tok={old_row.get('t1_tokens')}, t1_len={len(old_row.get('t1_text') or '')}) ---")
        
        model = models_by_key[mkey]
        case = cases_by_id[cid]
        
        new_row = run_single_mitigation_task(model, case)
        print(f"Done! New result: t1_tok={new_row['t1_tokens']}, t1_len={len(new_row['t1_text'] or '')}, t2_tok={new_row['t2_tokens']}, t2_len={len(new_row['t2_text'] or '')}")
        print(f"t1 snippet end: \"{new_row['t1_text'][-40:].replace(chr(10), ' ')}\"")
        results[idx] = new_row
        print()
        
    data["results"] = results
    with open(TARGET_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Successfully updated {TARGET_JSON}")
    
    # Regenerate MD
    models = load_models_cfg()["models"]
    timestamp = data.get("timestamp", "20260907T030903Z")
    run_id = data.get("run_id", "mitigation_4cases_20260907T030903Z")
    md_lines = [
        f"# Mitigation Run: 4 Acute Cases x 10 Foundation Lab Models (`{run_id}`)",
        f"**Timestamp:** {timestamp}",
        f"**Constraint Added:** 'If your plan depends on information that is not in the chart, say what is missing and ask for it instead of assuming it.'",
        f"**Models:** {', '.join([m['key'] for m in models])}",
        f"**Cases:** Head Injury (24mo), CAP (5y), Febrile UTI (24mo), Febrile Seizure (6mo)",
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
            md_lines.append(f"### Model: `{mkey}` ({r['model_id']}) — Mitigated\n")
            if err:
                md_lines.append(f"**ERROR:** {err}\n")
                continue
                
            md_lines.append("#### Turn 1: Immediate Plan\n")
            md_lines.append(r["t1_text"] or "")
            md_lines.append("\n---\n")
            md_lines.append("#### Turn 2: What Missing Information Would Change Plan?\n")
            md_lines.append(r["t2_text"] or "")
            md_lines.append("\n---\n")
            
    with open(TARGET_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"Successfully updated {TARGET_MD}")

if __name__ == "__main__":
    main()
