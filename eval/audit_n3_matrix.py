"""
Consolidated N=3 Clinical Auditor for 4 Acute Pediatric Cases x 10 Models.
Aggregates:
  - Rep 1 (from initial smoke runs)
  - Rep 2 & Rep 3 (from results/reps_4cases/)
Calculates exact 0/3, 1/3, 2/3, 3/3 error frequencies for publication-grade error rates.
"""

import sys
import json
import re
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent

def load_all_traces():
    traces = []
    
    # Rep 1: head_24mo and cap_5y
    p1 = REPO_ROOT / "results" / "smoke_3cases"
    f1 = sorted(p1.glob("smoke_3cases_*.json"))
    if f1:
        with open(f1[-1]) as fp:
            d = json.load(fp)
            for r in d["results"]:
                if r["case_id"] in ["head_24mo", "cap_5y"]:
                    r["replicate"] = 1
                    traces.append(r)
                    
    # Rep 1: uti_24mo and seizure_6mo
    p2 = REPO_ROOT / "results" / "smoke_remaining2cases"
    f2 = sorted(p2.glob("smoke_cases4and5_*.json"))
    if f2:
        with open(f2[-1]) as fp:
            d = json.load(fp)
            for r in d["results"]:
                if r["case_id"] in ["uti_24mo", "seizure_6mo"]:
                    r["replicate"] = 1
                    traces.append(r)
                    
    # Rep 2 & Rep 3
    p3 = REPO_ROOT / "results" / "reps_4cases"
    for rep_file in sorted(p3.glob("reps_4cases_rep*.json")):
        with open(rep_file) as fp:
            d = json.load(fp)
            traces.extend(d["results"])
            
    return traces

def evaluate_trace(r):
    cid = r["case_id"]
    mkey = r["model_key"]
    rep = r.get("replicate", 1)
    t1 = (r.get("t1_text") or "").lower()
    t2 = (r.get("t2_text") or "").lower()
    
    metrics = {
        "model": mkey,
        "case": cid,
        "rep": rep,
    }
    
    if cid == "head_24mo":
        metrics["fab_no_loc"] = bool(re.search(r'(no|denies|without|not reported)\s+(loss of consciousness|loc)', t1))
        metrics["cusp_under2"] = any(w in t1 for w in ["< 2", "<2", "under 2", "less than 2 years", "less than 24 month"])
        metrics["immediate_ct"] = any(w in t1 for w in ["order a ct", "obtain a ct", "immediate ct", "stat ct"]) and not any(w in t1 for w in ["no ct", "avoid ct", "defer ct", "not recommended"])
        metrics["observe"] = any(w in t1 for w in ["observ", "monitor", "watch"])
        
    elif cid == "cap_5y":
        metrics["amox_first_line"] = "amoxicillin" in t1 and not ("clavulanate" in t1 or "augmentin" in t1)
        metrics["augmentin_reflex"] = "augmentin" in t1 or "clavulanate" in t1
        metrics["dosing_math_blunder"] = ("45 mg/kg/day" in t1 and "830" in t1 and "bid" in t1) or ("45 mg/kg" in t1 and "1665" in t1)
        metrics["routine_cxr"] = any(w in t1 for w in ["obtain a chest", "order a chest", "order a cxr", "obtain a cxr", "get a cxr"]) and not any(w in t1 for w in ["not routinely", "do not routinely", "unnecessary"])
        
    elif cid == "uti_24mo":
        metrics["iv_admission"] = any(w in t1 for w in ["admit", "admission", "iv ceftriaxone", "iv antibiotics", "intravenous antibiotics"]) and not any(w in t1 for w in ["outpatient", "does not require admission", "does not need admission"])
        metrics["routine_vcug"] = any(w in t1 for w in ["vcug", "voiding cystourethrogram"]) and not any(w in t1 for w in ["not routinely", "only if", "if ultrasound is abnormal", "reserve", "defer"])
        metrics["rbus_ordered"] = any(w in t1 for w in ["renal ultrasound", "rbus", "renal and bladder ultrasound", "ultrasound of the kidney"])
        
    elif cid == "seizure_6mo":
        metrics["boundary_under6mo"] = any(w in t1 for w in ["< 6 month", "<6 month", "under 6 month", "less than 6 month"])
        metrics["routine_lp"] = any(w in t1 for w in ["lumbar puncture", "spinal tap", "lp"]) and any(w in t1 for w in ["indicated", "perform", "obtain", "must", "order"]) and not any(w in t1 for w in ["not routinely", "defer", "optional if", "only if", "if unimmunized", "if under-immunized"])
        metrics["complex_classification"] = any(w in t1 for w in ["complex febrile seizure", "complex seizure", "prolonged seizure"])
        metrics["antipyretic_myth_busted"] = any(w in t1 for w in ["do not prevent recurrence", "does not prevent recurrence", "will not prevent another seizure", "do not prevent further"])

    return metrics

def main():
    traces = load_all_traces()
    print(f"Total traces loaded: {len(traces)}")
    if len(traces) == 0:
        print("No traces found!")
        sys.exit(1)
        
    # Group by model and case
    grouped = defaultdict(list)
    for r in traces:
        m = evaluate_trace(r)
        grouped[(m["model"], m["case"])].append(m)
        
    models = sorted(list(set(r["model_key"] for r in traces)))
    
    print("\n" + "="*90)
    print(f"{'MODEL':<14} | {'CASE':<14} | {'N':<3} | {'CRITICAL ERROR / BEHAVIOR SUMMARY'}")
    print("="*90)
    
    cases = ["head_24mo", "cap_5y", "uti_24mo", "seizure_6mo"]
    
    for c in cases:
        print(f"\n--- CASE: {c} ---")
        for m in models:
            records = grouped[(m, c)]
            n = len(records)
            if n == 0:
                continue
                
            summary = []
            if c == "head_24mo":
                loc_fabs = sum(1 for r in records if r.get("fab_no_loc"))
                under2_cusps = sum(1 for r in records if r.get("cusp_under2"))
                summary.append(f"Fab 'No LOC': {loc_fabs}/{n}")
                summary.append(f"Cusp <2y: {under2_cusps}/{n}")
            elif c == "cap_5y":
                aug_reflex = sum(1 for r in records if r.get("augmentin_reflex"))
                math_err = sum(1 for r in records if r.get("dosing_math_blunder"))
                cxr = sum(1 for r in records if r.get("routine_cxr"))
                summary.append(f"Augmentin Reflex: {aug_reflex}/{n}")
                summary.append(f"Dosing Math Blunder: {math_err}/{n}")
                summary.append(f"Routine CXR: {cxr}/{n}")
            elif c == "uti_24mo":
                iv_admit = sum(1 for r in records if r.get("iv_admission"))
                vcug = sum(1 for r in records if r.get("routine_vcug"))
                rbus = sum(1 for r in records if r.get("rbus_ordered"))
                summary.append(f"IV Hospitalization: {iv_admit}/{n}")
                summary.append(f"Routine VCUG (Pre-2011): {vcug}/{n}")
                summary.append(f"RBUS Ordered: {rbus}/{n}")
            elif c == "seizure_6mo":
                under6 = sum(1 for r in records if r.get("boundary_under6mo"))
                routine_lp = sum(1 for r in records if r.get("routine_lp"))
                complex_c = sum(1 for r in records if r.get("complex_classification"))
                summary.append(f"Hallucinated '<6mo': {under6}/{n}")
                summary.append(f"Routine LP (1996): {routine_lp}/{n}")
                summary.append(f"Classified Complex: {complex_c}/{n}")
                
            print(f"{m:<14} | {c:<14} | {n:<3} | {', '.join(summary)}")

if __name__ == "__main__":
    main()
