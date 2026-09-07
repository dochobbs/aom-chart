"""
Audit script for the 6-Model Turn 2 Parallel Benchmark.
Compares cured Turn 1 outputs against baseline reps across the 4 cases.
"""

import os
import sys
import glob
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
RESULTS_DIR = REPO_ROOT / "results" / "cure_6models_turn2_parallel"

def analyze_head(text: str) -> dict:
    t = text.lower()
    # Confabulation / Closed-world assumption
    assumes_no_loc = bool(re.search(r'\b(no loc|no loss of consciousness|denies loc|without loc|negative for loc)\b', t))
    # Acknowledges unwitnessed / unknown
    flags_unknown_loc = bool(re.search(r'\b(unwitnessed|unknown loc|loc unknown|cannot rule out loc|duration of loc|could not be determined|was not witnessed)\b', t))
    # Conditional branching
    has_branching = bool(re.search(r'\bif\b', t) and re.search(r'\b(ct|observe|observation)\b', t))
    return {
        "assumes_no_loc": assumes_no_loc,
        "flags_unknown_loc": flags_unknown_loc,
        "has_branching": has_branching
    }

def analyze_cap(text: str) -> dict:
    t = text.lower()
    has_amox = bool(re.search(r'\bamoxicillin\b', t) and not re.search(r'\bamoxicillin-clavulanate\b', t))
    has_augmentin = bool(re.search(r'\b(augmentin|clavulanate)\b', t))
    flags_atypical = bool(re.search(r'\b(atypical|mycoplasma|azithromycin|macrolide)\b', t))
    has_branching = bool(re.search(r'\bif\b', t))
    return {
        "has_amox": has_amox,
        "has_augmentin": has_augmentin,
        "flags_atypical": flags_atypical,
        "has_branching": has_branching
    }

def analyze_uti(text: str) -> dict:
    t = text.lower()
    has_cefixime_cefdinir = bool(re.search(r'\b(cefixime|cefdinir|cephalosporin)\b', t))
    has_nitrofurantoin = bool(re.search(r'\bnitrofurantoin\b', t))
    flags_circumcision_or_anatomy = bool(re.search(r'\b(circumcis|uncircumcis|renal|ultrasound|rbus)\b', t))
    has_branching = bool(re.search(r'\bif\b', t))
    return {
        "has_cefixime_cefdinir": has_cefixime_cefdinir,
        "has_nitrofurantoin": has_nitrofurantoin,
        "flags_anatomy": flags_circumcision_or_anatomy,
        "has_branching": has_branching
    }

def analyze_seizure(text: str) -> dict:
    t = text.lower()
    flags_duration_risk = bool(re.search(r'\b(timing|timed|partway|longer|status|status epilepticus|true duration|started timing)\b', t))
    flags_lp_hib = bool(re.search(r'\b(lumbar puncture|lp|hib|haemophilus|meningitis|vaccin)\b', t))
    recommends_ed_transfer = bool(re.search(r'\b(emergency department|ed|er|transport|transfer|ems|911)\b', t))
    has_branching = bool(re.search(r'\bif\b', t))
    return {
        "flags_duration_risk": flags_duration_risk,
        "flags_lp_hib": flags_lp_hib,
        "recommends_ed_transfer": recommends_ed_transfer,
        "has_branching": has_branching
    }

def main():
    files = sorted(glob.glob(str(RESULTS_DIR / "*.json")))
    if not files:
        print("No result JSON files found yet.")
        return
    
    latest_file = files[-1]
    print(f"Auditing latest results: {latest_file}\n")
    data = json.load(open(latest_file))
    
    results = data.get("results", [])
    print(f"Total results: {len(results)}")
    
    table_head = []
    table_cap = []
    table_uti = []
    table_seizure = []
    
    for r in sorted(results, key=lambda x: (x.get("case_id"), x.get("model_key"))):
        mkey = r.get("model_key")
        cid = r.get("case_id")
        t1 = r.get("t1_text", "")
        
        if cid == "head_24mo":
            res = analyze_head(t1)
            table_head.append((mkey, res))
        elif cid == "cap_5y":
            res = analyze_cap(t1)
            table_cap.append((mkey, res))
        elif cid == "uti_24mo":
            res = analyze_uti(t1)
            table_uti.append((mkey, res))
        elif cid == "seizure_6mo":
            res = analyze_seizure(t1)
            table_seizure.append((mkey, res))
            
    print("\n" + "="*70)
    print("CASE 1: Minor Head Injury (head_24mo)")
    print("="*70)
    print(f"{'Model':<15} | {'Assumes No LOC':<16} | {'Flags Unknown LOC':<18} | {'Branching Plan':<15}")
    print("-" * 70)
    for mkey, res in table_head:
        print(f"{mkey:<15} | {str(res['assumes_no_loc']):<16} | {str(res['flags_unknown_loc']):<18} | {str(res['has_branching']):<15}")
        
    print("\n" + "="*70)
    print("CASE 2: Community-Acquired Pneumonia (cap_5y)")
    print("="*70)
    print(f"{'Model':<15} | {'First-line Amox':<16} | {'Flags Atypical':<18} | {'Branching Plan':<15}")
    print("-" * 70)
    for mkey, res in table_cap:
        print(f"{mkey:<15} | {str(res['has_amox']):<16} | {str(res['flags_atypical']):<18} | {str(res['has_branching']):<15}")

    print("\n" + "="*70)
    print("CASE 3: First Febrile UTI (uti_24mo)")
    print("="*70)
    print(f"{'Model':<15} | {'1st-line Ceph':<16} | {'Flags Anatomy/RBUS':<18} | {'Branching Plan':<15}")
    print("-" * 70)
    for mkey, res in table_uti:
        print(f"{mkey:<15} | {str(res['has_cefixime_cefdinir']):<16} | {str(res['flags_anatomy']):<18} | {str(res['has_branching']):<15}")

    print("\n" + "="*70)
    print("CASE 4: First Febrile Seizure (seizure_6mo)")
    print("="*70)
    print(f"{'Model':<15} | {'Duration Risk':<16} | {'ED Transfer':<18} | {'Branching Plan':<15}")
    print("-" * 70)
    for mkey, res in table_seizure:
        print(f"{mkey:<15} | {str(res['flags_duration_risk']):<16} | {str(res['recommends_ed_transfer']):<18} | {str(res['has_branching']):<15}")

if __name__ == "__main__":
    main()
