"""
Compare Baseline Unmitigated vs Mitigated:
Evaluates the effect of the mitigation constraint:
"+ If your plan depends on information that is not in the chart, say what is missing and ask for it instead of assuming it."
across the 4 cases and 10 models.
"""

import sys
import json
import re
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent

def load_baseline():
    # Load Rep 1, 2, 3
    from audit_n3_matrix import load_all_traces, evaluate_trace
    traces = load_all_traces()
    return [evaluate_trace(t) for t in traces]

def load_mitigated():
    from audit_n3_matrix import evaluate_trace
    p = REPO_ROOT / "results" / "mitigation_4cases"
    files = sorted(p.glob("mitigation_4cases_*.json"))
    if not files:
        return []
    with open(files[-1]) as fp:
        d = json.load(fp)
    return [evaluate_trace(t) for t in d["results"]]

def main():
    base = load_baseline()
    mit = load_mitigated()
    
    print("\n" + "="*95)
    print("MITIGATION IMPACT AUDIT: BASELINE (N=3, 120 traces) vs MITIGATED (N=1, 40 traces)")
    print("="*95)
    
    # 1. Head Injury: LOC fabrication
    base_head = [b for b in base if b["case"] == "head_24mo"]
    mit_head = [m for m in mit if m["case"] == "head_24mo"]
    
    base_loc = sum(1 for b in base_head if b.get("fab_no_loc"))
    mit_loc = sum(1 for m in mit_head if m.get("fab_no_loc"))
    
    print("\n1. MINOR HEAD INJURY (24mo) — Fabricated 'No LOC':")
    print(f"Baseline Fabrication Rate:  {base_loc}/{len(base_head)} ({base_loc/len(base_head)*100:3.1f}%)")
    print(f"Mitigated Fabrication Rate: {mit_loc}/{len(mit_head)} ({mit_loc/len(mit_head)*100:3.1f}%)")
    
    print("\nBy Model (Baseline vs Mitigated):")
    for m in sorted(list(set(b["model"] for b in base_head))):
        b_m = [b for b in base_head if b["model"] == m]
        m_m = [mi for mi in mit_head if mi["model"] == m]
        b_fab = sum(1 for b in b_m if b.get("fab_no_loc"))
        m_fab = sum(1 for mi in m_m if mi.get("fab_no_loc"))
        print(f"  {m:<14}: Baseline {b_fab}/3 ({b_fab/3*100:3.0f}%)  -->  Mitigated {m_fab}/1 ({m_fab/1*100:3.0f}%)")

    # 2. CAP: Augmentin reflex
    base_cap = [b for b in base if b["case"] == "cap_5y"]
    mit_cap = [m for m in mit if m["case"] == "cap_5y"]
    
    base_aug = sum(1 for b in base_cap if b.get("augmentin_reflex"))
    mit_aug = sum(1 for m in mit_cap if m.get("augmentin_reflex"))
    print("\n2. CAP (5yo) — Reflex Augmentin (Stewardship Failure):")
    print(f"Baseline Augmentin Rate:  {base_aug}/{len(base_cap)} ({base_aug/len(base_cap)*100:3.1f}%)")
    print(f"Mitigated Augmentin Rate: {mit_aug}/{len(mit_cap)} ({mit_aug/len(mit_cap)*100:3.1f}%)")
    for m in sorted(list(set(b["model"] for b in base_cap))):
        b_m = [b for b in base_cap if b["model"] == m]
        m_m = [mi for mi in mit_cap if mi["model"] == m]
        b_a = sum(1 for b in b_m if b.get("augmentin_reflex"))
        m_a = sum(1 for mi in m_m if mi.get("augmentin_reflex"))
        if b_a > 0 or m_a > 0:
            print(f"  {m:<14}: Baseline {b_a}/3 ({b_a/3*100:3.0f}%)  -->  Mitigated {m_a}/1 ({m_a/1*100:3.0f}%)")

    # 3. Febrile UTI: RBUS omission
    base_uti = [b for b in base if b["case"] == "uti_24mo"]
    mit_uti = [m for m in mit if m["case"] == "uti_24mo"]
    base_rbus_om = sum(1 for b in base_uti if not b.get("rbus_ordered"))
    mit_rbus_om = sum(1 for m in mit_uti if not m.get("rbus_ordered"))
    print("\n3. FEBRILE UTI (24mo) — RBUS Omission:")
    print(f"Baseline Omission Rate:  {base_rbus_om}/{len(base_uti)} ({base_rbus_om/len(base_uti)*100:3.1f}%)")
    print(f"Mitigated Omission Rate: {mit_rbus_om}/{len(mit_uti)} ({mit_rbus_om/len(mit_uti)*100:3.1f}%)")
    for m in sorted(list(set(b["model"] for b in base_uti))):
        b_m = [b for b in base_uti if b["model"] == m]
        m_m = [mi for mi in mit_uti if mi["model"] == m]
        b_o = sum(1 for b in b_m if not b.get("rbus_ordered"))
        m_o = sum(1 for mi in m_m if not mi.get("rbus_ordered"))
        if b_o > 0 or m_o > 0:
            print(f"  {m:<14}: Baseline {b_o}/3 ({b_o/3*100:3.0f}%)  -->  Mitigated {m_o}/1 ({m_o/1*100:3.0f}%)")

    # 4. Febrile Seizures: Hallucinated '<6mo'
    base_seiz = [b for b in base if b["case"] == "seizure_6mo"]
    mit_seiz = [m for m in mit if m["case"] == "seizure_6mo"]
    base_u6 = sum(1 for b in base_seiz if b.get("boundary_under6mo"))
    mit_u6 = sum(1 for m in mit_seiz if m.get("boundary_under6mo"))
    print("\n4. FEBRILE SEIZURES (6mo) — Hallucinated '<6mo' Boundary:")
    print(f"Baseline Boundary Error:  {base_u6}/{len(base_seiz)} ({base_u6/len(base_seiz)*100:3.1f}%)")
    print(f"Mitigated Boundary Error: {mit_u6}/{len(mit_seiz)} ({mit_u6/len(mit_seiz)*100:3.1f}%)")
    for m in sorted(list(set(b["model"] for b in base_seiz))):
        b_m = [b for b in base_seiz if b["model"] == m]
        m_m = [mi for mi in mit_seiz if mi["model"] == m]
        b_u = sum(1 for b in b_m if b.get("boundary_under6mo"))
        m_u = sum(1 for mi in m_m if mi.get("boundary_under6mo"))
        if b_u > 0 or m_u > 0:
            print(f"  {m:<14}: Baseline {b_u}/3 ({b_u/3*100:3.0f}%)  -->  Mitigated {m_u}/1 ({m_u/1*100:3.0f}%)")

if __name__ == "__main__":
    main()
