"""
Resume / Backfill Script for Credential vs. Gender Experiment:
Loads the existing run, identifies failed traces due to transient network drop,
and completes them with retries.
"""

import os
import sys
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
RESULTS_DIR = REPO_ROOT / "results" / "credential_vs_gender"

from run import load_models_cfg
from run_credential_vs_gender import CELLS, render_prompt, run_single, MODELS_TO_RUN

def main():
    files = sorted(RESULTS_DIR.glob("credential_vs_gender_*.json"))
    if not files:
        print("No files found!")
        sys.exit(1)
        
    target_file = files[-1]
    print(f"Loading existing file: {target_file}")
    with open(target_file) as fp:
        data = json.load(fp)
        
    results = data["results"]
    cfg = load_models_cfg()["models"]
    models_map = {m["key"]: m for m in cfg if m["key"] in MODELS_TO_RUN}
    cells_map = {c["id"]: c for c in CELLS}
    
    # Identify items needing rerun
    need_rerun = []
    for idx, r in enumerate(results):
        if r.get("error") or not r.get("t1_text"):
            need_rerun.append((idx, r["case_id"], r["cell_id"], r["model_key"], r["replicate"]))
            
    print(f"Found {len(need_rerun)} traces needing backfill / rerun.")
    if not need_rerun:
        print("All 288 traces are complete!")
        return
        
    tasks = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        for idx, cid, cell_id, mkey, rep in need_rerun:
            m = models_map[mkey]
            cell = cells_map[cell_id]
            tasks.append((idx, executor.submit(run_single, m, cid, cell, rep)))
            
        for idx, fut in tasks:
            new_r = fut.result()
            results[idx] = new_r
            
    # Save updated json
    data["results"] = results
    with open(target_file, "w") as fp:
        json.dump(data, fp, indent=2)
        
    # Re-generate markdown report
    out_md = target_file.with_suffix(".md")
    cases = ["aom", "head_24mo"]
    md_lines = [
        f"# Credential vs. Gender Benchmark",
        f"**File:** `{target_file.name}`",
        f"**Timestamp:** {data.get('timestamp')}",
        f"**Total Traces:** {len(results)}",
        "",
        "---"
    ]
    for cid in cases:
        md_lines.append(f"\n## Case: `{cid}`\n")
        for cell in CELLS:
            cell_id = cell["id"]
            md_lines.append(f"\n### Cell: {cell['label']} (`{cell_id}`)\n")
            c_res = [r for r in results if r["case_id"] == cid and r["cell_id"] == cell_id]
            for r in sorted(c_res, key=lambda x: (x["model_key"], x["replicate"])):
                mkey = r["model_key"]
                rep = r["replicate"]
                err = r.get("error")
                md_lines.append(f"#### `{mkey}` (Replicate {rep})\n")
                if err:
                    md_lines.append(f"**ERROR:** {err}\n")
                    continue
                md_lines.append("**Turn 1: Plan**\n")
                md_lines.append(r["t1_text"] or "")
                md_lines.append("\n**Turn 2: What Missing Information Would Change Plan?**\n")
                md_lines.append(r["t2_text"] or "")
                md_lines.append("\n---\n")
                
    with open(out_md, "w") as fp:
        fp.write("\n".join(md_lines))
        
    print(f"\n[SUCCESS] Backfill complete! Updated {target_file} and {out_md}")

if __name__ == "__main__":
    main()
