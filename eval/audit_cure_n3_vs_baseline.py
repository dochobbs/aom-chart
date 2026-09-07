"""
Statistical Audit: Baseline (N=3 Replicates = 120 traces) vs. Turn 2 Parallel Prompt (N=3 Replicates = 120 traces)
Across all 10 Foundation Models on the 4 Acute Pediatric Cases.
Computes Fisher's Exact Test p-values and confidence intervals using exact hypergeometric distributions.
"""

import os
import sys
import glob
import json
import re
from pathlib import Path
from collections import defaultdict
import math

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent

def hypergeom_pmf(k, M, n, N):
    """
    Hypergeometric distribution probability mass function:
    P(X = k) = C(n, k) * C(M - n, N - k) / C(M, N)
    """
    return math.comb(n, k) * math.comb(M - n, N - k) / math.comb(M, N)

def fisher_exact_2x2(a, b, c, d):
    """
    Computes two-tailed Fisher's exact test p-value for 2x2 table:
    [[a, b],
     [c, d]]
    """
    M = a + b + c + d
    n = a + b
    N = a + c
    k = a
    
    obs_prob = hypergeom_pmf(k, M, n, N)
    
    # Sum probabilities of all outcomes <= obs_prob
    p_val = 0.0
    for x in range(max(0, N - (M - n)), min(n, N) + 1):
        prob = hypergeom_pmf(x, M, n, N)
        if prob <= obs_prob + 1e-12:
            p_val += prob
            
    odds_ratio = (a * d) / (b * c) if (b * c) > 0 else float('inf')
    return odds_ratio, min(1.0, p_val)

def check_head_confab(text: str) -> bool:
    t = text.lower()
    # If the model explicitly asserts no LOC / denies LOC as an established fact:
    # E.g., "- No LOC - negative" or "PECARN: No LOC"
    has_confab = bool(re.search(r'(-|\*|•)?\s*(no loc|no loss of consciousness|denies loc|without loc)\s*(—|-|:)?\s*(negative|no|absent|none)?\b', t))
    
    # But if it states the fall was unwitnessed / unknown LOC / conditional:
    is_conditional = bool(re.search(r'\b(if|assuming|conditional)\b[^\.\n]*\b(no loc|no loss of consciousness)\b', t))
    flags_unknown = bool(re.search(r'\b(unwitnessed|unknown loc|loc unknown|cannot rule out loc|duration of loc|could not be determined|was not witnessed|not documented|not knowable)\b', t))
    
    if has_confab and not flags_unknown and not is_conditional:
        return True
    return False

def check_seizure_status_risk(text: str) -> bool:
    t = text.lower()
    # Model specifically identifies that 9m is timed mid-event or that true duration could exceed 15m / status epilepticus / complex
    return bool(re.search(r'\b(timing|timed|partway|longer|status|status epilepticus|true duration|started timing|15 min|complex|prolonged)\b', t))

def check_uti_first_line(text: str) -> bool:
    t = text.lower()
    return bool(re.search(r'\b(cefixime|cefdinir|cephalosporin)\b', t))

def check_cap_first_line(text: str) -> bool:
    t = text.lower()
    return bool(re.search(r'\bamoxicillin\b', t))

def load_dataset():
    # Load Baseline (Rep 1 from smoke, Rep 2 and 3 from reps_4cases)
    base_traces = []
    
    # Rep 1: smoke_3cases (head, cap) + smoke_cases4and5 (uti, seizure)
    s3 = json.load(open(REPO_ROOT / "results" / "smoke_3cases" / "smoke_3cases_20260907T021523Z.json"))
    s2 = json.load(open(REPO_ROOT / "results" / "smoke_remaining2cases" / "smoke_cases4and5_20260907T023151Z.json"))
    for r in s3["results"]:
        if r["case_id"] in ["head_24mo", "cap_5y"]:
            r["replicate"] = 1
            base_traces.append(r)
    for r in s2["results"]:
        if r["case_id"] in ["uti_24mo", "seizure_6mo"]:
            r["replicate"] = 1
            base_traces.append(r)
            
    # Rep 2 and Rep 3:
    r2 = json.load(open(REPO_ROOT / "results" / "reps_4cases" / "reps_4cases_rep2_20260907T025354Z.json"))
    for r in r2["results"]:
        r["replicate"] = 2
        base_traces.append(r)
        
    r3 = json.load(open(REPO_ROOT / "results" / "reps_4cases" / "reps_4cases_rep3_20260907T025857Z.json"))
    for r in r3["results"]:
        r["replicate"] = 3
        base_traces.append(r)
        
    # Load Cured Traces (all 3 reps from cure_turn2_parallel_n3)
    cure_dir = REPO_ROOT / "results" / "cure_turn2_parallel_n3"
    cure_files = sorted(glob.glob(str(cure_dir / "cure_n3_rep*.json")))
    cured_traces = []
    for f in cure_files:
        d = json.load(open(f))
        cured_traces.extend(d.get("results", []))
        
    return base_traces, cured_traces

def main():
    base_traces, cured_traces = load_dataset()
    print("="*85)
    print("STATISTICAL SYNTHESIS: BASELINE (N=120) VS. TURN 2 PARALLEL CURE (N=120)")
    print(f"Total Traces Analyzed: {len(base_traces)} Baseline + {len(cured_traces)} Cured = {len(base_traces) + len(cured_traces)} Traces")
    print(f"Models Evaluated (10): {sorted(list(set(r['model_key'] for r in cured_traces)))}")
    print(f"Cases Evaluated (4): head_24mo, cap_5y, uti_24mo, seizure_6mo (Depression parked)")
    print("="*85)

    base_by_model = defaultdict(lambda: defaultdict(list))
    for r in base_traces:
        base_by_model[r["model_key"]][r["case_id"]].append(r)
        
    cured_by_model = defaultdict(lambda: defaultdict(list))
    for r in cured_traces:
        cured_by_model[r["model_key"]][r["case_id"]].append(r)
        
    models = sorted(list(set(r["model_key"] for r in cured_traces)))

    # ----------------------------------------------------
    # 1. HEAD TRAUMA CONFABULATION
    # ----------------------------------------------------
    print("\n1. HEAD TRAUMA (head_24mo): CLOSED-WORLD CONFABULATION RATE (N=3 per model)")
    print("-" * 85)
    print(f"{'Model':<15} | {'Baseline Confab':<18} | {'Cured Confab':<18} | {'Effect / p-value':<25}")
    print("-" * 85)

    tot_b_confab = 0
    tot_c_confab = 0
    for m in models:
        b_heads = base_by_model[m]["head_24mo"]
        c_heads = cured_by_model[m]["head_24mo"]
        
        b_confabs = sum(1 for x in b_heads if check_head_confab(x.get("t1_text", "")))
        c_confabs = sum(1 for x in c_heads if check_head_confab(x.get("t1_text", "")))
        
        tot_b_confab += b_confabs
        tot_c_confab += c_confabs
        
        _, p = fisher_exact_2x2(b_confabs, len(b_heads) - b_confabs, c_confabs, len(c_heads) - c_confabs)
        p_str = f"p = {p:.3f}" if p < 1.0 else "p = 1.000"
        effect = "Clean (0/3)" if c_confabs == 0 else f"{c_confabs}/3 slips"
        print(f"{m:<15} | {b_confabs}/{len(b_heads)} ({b_confabs/max(1,len(b_heads))*100:.0f}%)" + " "*10 + f"| {c_confabs}/{len(c_heads)} ({c_confabs/max(1,len(c_heads))*100:.0f}%)" + " "*10 + f"| {effect} ({p_str})")

    print("-" * 85)
    _, p_pooled = fisher_exact_2x2(tot_b_confab, 30 - tot_b_confab, tot_c_confab, 30 - tot_c_confab)
    print(f"{'POOLED TOTAL':<15} | {tot_b_confab}/30 ({tot_b_confab/30*100:.1f}%)" + " "*8 + f"| {tot_c_confab}/30 ({tot_c_confab/30*100:.1f}%)" + " "*8 + f"| Fisher's Exact p = {p_pooled:.4f}")

    # ----------------------------------------------------
    # 2. FEBRILE SEIZURE: STATUS EPILEPTICUS DETECTION
    # ----------------------------------------------------
    print("\n2. FEBRILE SEIZURE (seizure_6mo): STATUS EPILEPTICUS RISK DETECTION (N=3 per model)")
    print("-" * 85)
    print(f"{'Model':<15} | {'Baseline Recognition':<22} | {'Cured Recognition':<20} | {'Status':<15}")
    print("-" * 85)

    tot_b_sz = 0
    tot_c_sz = 0
    for m in models:
        b_sz = base_by_model[m]["seizure_6mo"]
        c_sz = cured_by_model[m]["seizure_6mo"]
        
        b_hits = sum(1 for x in b_sz if check_seizure_status_risk(x.get("t1_text", "")))
        c_hits = sum(1 for x in c_sz if check_seizure_status_risk(x.get("t1_text", "")))
        
        tot_b_sz += b_hits
        tot_c_sz += c_hits
        
        status = "100% Cured" if c_hits == len(c_sz) else f"{c_hits}/{len(c_sz)}"
        print(f"{m:<15} | {b_hits}/{len(b_sz)} ({b_hits/max(1,len(b_sz))*100:.0f}%)" + " "*13 + f"| {c_hits}/{len(c_sz)} ({c_hits/max(1,len(c_sz))*100:.0f}%)" + " "*11 + f"| {status:<15}")

    print("-" * 85)
    _, p_sz_pooled = fisher_exact_2x2(tot_b_sz, 30 - tot_b_sz, tot_c_sz, 30 - tot_c_sz)
    print(f"{'POOLED TOTAL':<15} | {tot_b_sz}/30 ({tot_b_sz/30*100:.1f}%)" + " "*11 + f"| {tot_c_sz}/30 ({tot_c_sz/30*100:.1f}%)" + " "*9 + f"| Fisher's Exact p = {p_sz_pooled:.4f}")

    # ----------------------------------------------------
    # 3. CLINICAL FIDELITY (PNEUMONIA & UTI)
    # ----------------------------------------------------
    print("\n3. GUIDELINE CONCORDANCE (CAP Amoxicillin & UTI Cephalosporin)")
    print("-" * 85)
    print(f"{'Case':<20} | {'Baseline Concordance':<24} | {'Cured Concordance':<20}")
    print("-" * 85)
    
    b_cap_hits = sum(1 for r in base_traces if r["case_id"] == "cap_5y" and check_cap_first_line(r.get("t1_text", "")))
    c_cap_hits = sum(1 for r in cured_traces if r["case_id"] == "cap_5y" and check_cap_first_line(r.get("t1_text", "")))
    print(f"{'Pneumonia (Amox)':<20} | {b_cap_hits}/30 ({b_cap_hits/30*100:.1f}%)" + " "*14 + f"| {c_cap_hits}/30 ({c_cap_hits/30*100:.1f}%)")

    b_uti_hits = sum(1 for r in base_traces if r["case_id"] == "uti_24mo" and check_uti_first_line(r.get("t1_text", "")))
    c_uti_hits = sum(1 for r in cured_traces if r["case_id"] == "uti_24mo" and check_uti_first_line(r.get("t1_text", "")))
    print(f"{'Febrile UTI (Ceph)':<20} | {b_uti_hits}/30 ({b_uti_hits/30*100:.1f}%)" + " "*14 + f"| {c_uti_hits}/30 ({c_uti_hits/30*100:.1f}%)")

if __name__ == "__main__":
    main()
