"""
High-Thinking Spectrum Auditor:
Compares Baseline (Low/Standard Thinking, N=3, 120 traces) vs High-Thinking (N=1, 40 traces)
across the 4 acute pediatric cases.
"""

import sys
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def load_baseline():
    from audit_n3_matrix import load_all_traces, evaluate_trace
    traces = load_all_traces()
    return [evaluate_trace(t) for t in traces]

def load_high_thinking():
    from audit_n3_matrix import evaluate_trace
    p = REPO_ROOT / "results" / "high_thinking_4cases"
    files = sorted(p.glob("high_thinking_4cases_*.json"))
    if not files:
        return []
    
    seen = set()
    all_evaluated = []
    # Process files; later files overwrite earlier if duplicate (model, case, rep)
    for f in files:
        with open(f) as fp:
            d = json.load(fp)
            rep = d.get("replicate", 1)
            for t in d.get("results", []):
                t_rep = t.get("replicate", rep)
                t["replicate"] = t_rep
                key = (t["model_key"], t["case_id"], t_rep)
                if key not in seen:
                    seen.add(key)
                    all_evaluated.append(evaluate_trace(t))
    return all_evaluated

def main():
    base = load_baseline()
    high = load_high_thinking()
    
    high_reps = len(set(h.get("rep", 1) for h in high))
    print("\n" + "="*95)
    print(f"THINKING SPECTRUM AUDIT: BASELINE (N=3, {len(base)} traces) vs HIGH-THINKING (N={high_reps}, {len(high)} traces)")
    print("="*95)
    
    # 1. Head Injury: LOC fabrication & 24mo cusp
    base_head = [b for b in base if b["case"] == "head_24mo"]
    high_head = [h for h in high if h["case"] == "head_24mo"]
    
    print("\n1. MINOR HEAD INJURY (24mo):")
    print(f"{'Model':<14} | {'Base Fab No-LOC':<18} | {'High Fab No-LOC':<18} | {'Base Cusp <2y':<16} | {'High Cusp <2y':<16}")
    print("-" * 88)
    for m in sorted(list(set(b["model"] for b in base_head))):
        b_m = [b for b in base_head if b["model"] == m]
        h_m = [hi for hi in high_head if hi["model"] == m]
        b_len = len(b_m) or 1
        h_len = len(h_m) or 1
        b_fab = sum(1 for b in b_m if b.get("fab_no_loc"))
        h_fab = sum(1 for hi in h_m if hi.get("fab_no_loc"))
        b_cusp = sum(1 for b in b_m if b.get("cusp_under2"))
        h_cusp = sum(1 for hi in h_m if hi.get("cusp_under2"))
        print(f"{m:<14} | {b_fab}/{b_len} ({b_fab/b_len*100:3.0f}%)           | {h_fab}/{h_len} ({h_fab/h_len*100:3.0f}%)           | {b_cusp}/{b_len} ({b_cusp/b_len*100:3.0f}%)        | {h_cusp}/{h_len} ({h_cusp/h_len*100:3.0f}%)")

    # 2. CAP: Augmentin reflex & math blunder
    base_cap = [b for b in base if b["case"] == "cap_5y"]
    high_cap = [h for h in high if h["case"] == "cap_5y"]
    print("\n2. PNEUMONIA (5yo) — Stewardship & Dosing:")
    print(f"{'Model':<14} | {'Base Augmentin':<18} | {'High Augmentin':<18} | {'Base Math Err':<16} | {'High Math Err':<16}")
    print("-" * 88)
    for m in sorted(list(set(b["model"] for b in base_cap))):
        b_m = [b for b in base_cap if b["model"] == m]
        h_m = [hi for hi in high_cap if hi["model"] == m]
        b_len = len(b_m) or 1
        h_len = len(h_m) or 1
        b_aug = sum(1 for b in b_m if b.get("augmentin_reflex"))
        h_aug = sum(1 for hi in h_m if hi.get("augmentin_reflex"))
        b_math = sum(1 for b in b_m if b.get("dosing_math_blunder"))
        h_math = sum(1 for hi in h_m if hi.get("dosing_math_blunder"))
        print(f"{m:<14} | {b_aug}/{b_len} ({b_aug/b_len*100:3.0f}%)           | {h_aug}/{h_len} ({h_aug/h_len*100:3.0f}%)           | {b_math}/{b_len} ({b_math/b_len*100:3.0f}%)        | {h_math}/{h_len} ({h_math/h_len*100:3.0f}%)")

    # 3. Febrile UTI: RBUS omission & IV admission
    base_uti = [b for b in base if b["case"] == "uti_24mo"]
    high_uti = [h for h in high if h["case"] == "uti_24mo"]
    print("\n3. FEBRILE UTI (24mo) — RBUS Omission & IV Admission:")
    print(f"{'Model':<14} | {'Base RBUS Omit':<18} | {'High RBUS Omit':<18} | {'Base IV Admit':<16} | {'High IV Admit':<16}")
    print("-" * 88)
    for m in sorted(list(set(b["model"] for b in base_uti))):
        b_m = [b for b in base_uti if b["model"] == m]
        h_m = [hi for hi in high_uti if hi["model"] == m]
        b_len = len(b_m) or 1
        h_len = len(h_m) or 1
        b_r_om = sum(1 for b in b_m if not b.get("rbus_ordered"))
        h_r_om = sum(1 for hi in h_m if not hi.get("rbus_ordered"))
        b_iv = sum(1 for b in b_m if b.get("iv_admission"))
        h_iv = sum(1 for hi in h_m if hi.get("iv_admission"))
        print(f"{m:<14} | {b_r_om}/{b_len} ({b_r_om/b_len*100:3.0f}%)           | {h_r_om}/{h_len} ({h_r_om/h_len*100:3.0f}%)           | {b_iv}/{b_len} ({b_iv/b_len*100:3.0f}%)        | {h_iv}/{h_len} ({h_iv/h_len*100:3.0f}%)")

    # 4. Febrile Seizures: Hallucinated '<6mo' & Routine LP
    base_seiz = [b for b in base if b["case"] == "seizure_6mo"]
    high_seiz = [h for h in high if h["case"] == "seizure_6mo"]
    print("\n4. FEBRILE SEIZURES (6mo) — Hallucinated '<6mo' & Routine LP:")
    print(f"{'Model':<14} | {'Base Under 6mo':<18} | {'High Under 6mo':<18} | {'Base Routine LP':<16} | {'High Routine LP':<16}")
    print("-" * 88)
    for m in sorted(list(set(b["model"] for b in base_seiz))):
        b_m = [b for b in base_seiz if b["model"] == m]
        h_m = [hi for hi in high_seiz if hi["model"] == m]
        b_len = len(b_m) or 1
        h_len = len(h_m) or 1
        b_u6 = sum(1 for b in b_m if b.get("boundary_under6mo"))
        h_u6 = sum(1 for hi in h_m if hi.get("boundary_under6mo"))
        b_lp = sum(1 for b in b_m if b.get("routine_lp"))
        h_lp = sum(1 for hi in h_m if hi.get("routine_lp"))
        print(f"{m:<14} | {b_u6}/{b_len} ({b_u6/b_len*100:3.0f}%)           | {h_u6}/{h_len} ({h_u6/h_len*100:3.0f}%)           | {b_lp}/{b_len} ({b_lp/b_len*100:3.0f}%)        | {h_lp}/{h_len} ({h_lp/h_len*100:3.0f}%)")

if __name__ == "__main__":
    main()
