"""
Resume / Backfill Script for Demographic Benchmark:
Loads the existing demographics run, finds any traces that failed due to temporary network blip,
and completes them with automatic retries.
"""

import os
import sys
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
RESULTS_DIR = REPO_ROOT / "results" / "demographics_4cases"

from run import load_models_cfg, CALLERS, TURN2_QUESTION
from run_4cases_demographics import CASES, VARIANTS, render_demographic_prompt, SYSTEM_PROMPT

def run_task_with_retries(model, case_id, variant, max_retries=3):
    caller = CALLERS[model["vendor"]]
    mkey = model["key"]
    vid = variant["id"]
    prompt = render_demographic_prompt(case_id, vid)
    
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            print(f"[{case_id}][{vid}] Running {mkey} Turn 1 (Attempt {attempt})...", flush=True)
            t1_res = caller(model, SYSTEM_PROMPT, prompt)
            t1_text = t1_res["text"]
            
            print(f"[{case_id}][{vid}] Running {mkey} Turn 2...", flush=True)
            t2_res = caller(
                model,
                SYSTEM_PROMPT,
                prompt,
                followup=(t1_text, TURN2_QUESTION)
            )
            t2_text = t2_res["text"]
            
            return {
                "case_id": case_id,
                "case_title": CASES[case_id]["title"],
                "variant_id": vid,
                "variant_arm": variant["arm"],
                "variant_label": variant["label"],
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
            last_err = e
            print(f"[{case_id}][{vid}] Error on {mkey} attempt {attempt}: {e}", flush=True)
            time.sleep(2 * attempt)
            
    return {
        "case_id": case_id,
        "case_title": CASES[case_id]["title"],
        "variant_id": vid,
        "variant_arm": variant["arm"],
        "variant_label": variant["label"],
        "model_key": mkey,
        "model_id": model["id"],
        "vendor": model["vendor"],
        "t1_text": None,
        "t2_text": None,
        "error": str(last_err)
    }

def main():
    files = sorted(RESULTS_DIR.glob("demographics_4cases_*.json"))
    if not files:
        print("No demographic files found!")
        sys.exit(1)
        
    target_file = files[-1]
    print(f"Loading existing file: {target_file}")
    with open(target_file) as fp:
        data = json.load(fp)
        
    results = data["results"]
    models_cfg = load_models_cfg()["models"]
    models_map = {m["key"]: m for m in models_cfg}
    variants_map = {v["id"]: v for v in VARIANTS}
    
    # Identify items needing rerun
    need_rerun = []
    for idx, r in enumerate(results):
        if r.get("error") or not r.get("t1_text"):
            need_rerun.append((idx, r["case_id"], r["variant_id"], r["model_key"]))
            
    print(f"Found {len(need_rerun)} traces needing backfill / rerun.")
    if not need_rerun:
        print("All 280 traces are complete and error-free!")
        return
        
    tasks = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        for idx, cid, vid, mkey in need_rerun:
            m = models_map[mkey]
            v = variants_map[vid]
            tasks.append((idx, executor.submit(run_task_with_retries, m, cid, v)))
            
        for idx, fut in tasks:
            new_r = fut.result()
            results[idx] = new_r
            
    # Save updated json
    data["results"] = results
    with open(target_file, "w") as fp:
        json.dump(data, fp, indent=2)
        
    # Re-generate markdown report
    out_md = target_file.with_suffix(".md")
    md_lines = [
        f"# Demographic Matrix Benchmark: 4 Acute Cases x 10 Models",
        f"**File:** `{target_file.name}`",
        f"**Timestamp:** {data.get('timestamp')}",
        f"**Total Traces:** {len(results)}",
        "",
        "---"
    ]
    for cid in CASES:
        md_lines.append(f"\n## Case: {CASES[cid]['title']} (`{cid}`)\n")
        for v in VARIANTS:
            vid = v["id"]
            md_lines.append(f"\n### Variant: {v['label']} (`{vid}`)\n")
            c_v_results = [r for r in results if r["case_id"] == cid and r["variant_id"] == vid]
            for r in sorted(c_v_results, key=lambda x: x["model_key"]):
                mkey = r["model_key"]
                err = r.get("error")
                md_lines.append(f"#### Model: `{mkey}` ({r['model_id']})\n")
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
