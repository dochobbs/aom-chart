#!/usr/bin/env python3
"""
Heal truncated traces in results/brake_branching_validation/brake_branching_92traces_master.json:
Re-runs the 15 Opus-5 traces that hit the 4000 token limit with max_tokens=8192.
Then updates the master file and regenerates the validation report.
"""

import sys
import json
import shutil
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

from run_brake_and_branching_validation_battery import (
    PROMPT_HEAD_UNWITNESSED,
    PROMPT_AOM,
    PROMPT_HEAD_WITNESSED,
    audit_head_unwitnessed,
    audit_aom,
    audit_head_witnessed,
    run_single,
)

RESULTS_DIR = REPO_ROOT / "results" / "brake_branching_validation"
MASTER_JSON = RESULTS_DIR / "brake_branching_92traces_master.json"
BACKUP_JSON = RESULTS_DIR / "brake_branching_92traces_master.bak.json"

EXP_PROMPT_AUDIT = {
    "exp1_depth_head_trauma": (PROMPT_HEAD_UNWITNESSED, audit_head_unwitnessed),
    "exp2_transfer_aom": (PROMPT_AOM, audit_aom),
    "exp3_specificity_witnessed": (PROMPT_HEAD_WITNESSED, audit_head_witnessed),
}

def main():
    if not MASTER_JSON.exists():
        print(f"Error: {MASTER_JSON} not found!")
        sys.exit(1)

    if not BACKUP_JSON.exists():
        shutil.copyfile(MASTER_JSON, BACKUP_JSON)
        print(f"Created backup at {BACKUP_JSON}")

    with open(MASTER_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    traces = data["traces"]
    targets = []
    for idx, t in enumerate(traces):
        if t.get("output_tokens") == 4000:
            targets.append((idx, t))

    print(f"Found {len(targets)} truncated traces to heal.\n")

    def heal_task(item):
        idx, old_trace = item
        exp_id = old_trace["exp_id"]
        model_key = old_trace["model_key"]
        rep = old_trace["rep"]
        prompt, audit_fn = EXP_PROMPT_AUDIT[exp_id]
        
        print(f"[Start] Idx {idx}: {exp_id} / {model_key} / rep {rep}...", flush=True)
        t0 = time.time()
        new_trace = run_single(exp_id, prompt, model_key, rep, audit_fn)
        dur = time.time() - t0
        toks = new_trace.get("output_tokens", 0)
        end_snippet = (new_trace.get("text", "")[-40:]).replace("\n", " ")
        print(f"[Done]  Idx {idx}: {exp_id} / rep {rep} -> {toks} tokens in {dur:.1f}s. End: \"{end_snippet}\"", flush=True)
        return idx, new_trace

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(heal_task, item) for item in targets]
        for f in as_completed(futures):
            idx, new_trace = f.result()
            traces[idx] = new_trace

    data["traces"] = traces
    with open(MASTER_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"\nSuccessfully updated {MASTER_JSON}")
    print("\nRunning analyze_brake_branching_validation.py...")
    import subprocess
    subprocess.run([sys.executable, str(ROOT / "analyze_brake_branching_validation.py")], check=True)

if __name__ == "__main__":
    main()
