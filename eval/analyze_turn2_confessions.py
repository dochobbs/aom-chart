"""
Forensic Turn 2 Confession and Assumption Auditor across all 120 traces.
Analyzes whether models explicitly recognized their own unstated premises in Turn 2:
1. Head Injury: Did it admit LOC was unwitnessed / unknown?
2. CAP: Did it identify prior 30-day antibiotics or atypical exposures as missing?
3. UTI: Did it identify prior UTI history or circumcision as missing?
4. Seizure: Did it identify immunization status (Hib/PCV) or untimed onset as missing?
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

def audit_turn2(r):
    cid = r["case_id"]
    mkey = r["model_key"]
    rep = r.get("replicate", 1)
    t1 = (r.get("t1_text") or "").lower()
    t2 = (r.get("t2_text") or "").lower()
    
    res = {
        "model": mkey,
        "case": cid,
        "rep": rep,
    }
    
    if cid == "head_24mo":
        # Check if T1 fabricated no-LOC
        t1_fab_loc = bool(re.search(r'(no|denies|without|not reported)\s+(loss of consciousness|loc)', t1))
        # Check if T2 confessed or identified LOC as missing
        t2_flags_loc = any(w in t2 for w in ["loc", "loss of consciousness", "unwitnessed", "kitchen", "heard the thud", "did he cry immediately"])
        # Direct confession of assumption
        t2_confesses_assumption = any(w in t2 for w in ["assumed", "without a basis", "not documented", "unconfirmed", "extrapolated", "unstated"])
        res["t1_fab_loc"] = t1_fab_loc
        res["t2_flags_loc"] = t2_flags_loc
        res["t2_confessed"] = t1_fab_loc and t2_flags_loc
        
    elif cid == "cap_5y":
        # Check if T2 identified prior antibiotics in past 30 days
        t2_flags_prior_abx = any(w in t2 for w in ["recent antibiotic", "prior antibiotic", "amoxicillin in the past", "last 30 days", "past 30 days", "prior 30"])
        # Check if T2 identified atypical / Mycoplasma contacts
        t2_flags_atypical = any(w in t2 for w in ["mycoplasma", "walking pneumonia", "atypical", "school contact", "daycare"])
        res["t2_flags_prior_abx"] = t2_flags_prior_abx
        res["t2_flags_atypical"] = t2_flags_atypical
        
    elif cid == "uti_24mo":
        # Check if T1 asserted first UTI
        t1_asserts_first = any(w in t1 for w in ["first uti", "first febrile uti", "no prior uti", "no history of uti"])
        # Check if T2 identified prior UTI as missing fork
        t2_flags_prior_uti = any(w in t2 for w in ["prior uti", "previous uti", "first uti", "history of uti", "recurrent uti"])
        # Check if T2 identified circumcision
        t2_flags_circ = any(w in t2 for w in ["circumcis", "foreskin"])
        res["t1_asserts_first"] = t1_asserts_first
        res["t2_flags_prior_uti"] = t2_flags_prior_uti
        res["t2_flags_circ"] = t2_flags_circ
        
    elif cid == "seizure_6mo":
        # Check if T1 asserted vaccines were UTD
        t1_asserts_vax = any(w in t1 for w in ["immunizations are up to date", "fully vaccinated", "utd", "vaccinated for age"])
        # Check if T2 flags missing immunizations (Hib/PCV)
        t2_flags_vax = any(w in t2 for w in ["immuniz", "vaccin", "hib", "pcv", "pneumococc"])
        # Check if T2 flags untimed onset / total duration
        t2_flags_duration = any(w in t2 for w in ["exact duration", "total duration", "untimed", "onset", "how long"])
        res["t1_asserts_vax"] = t1_asserts_vax
        res["t2_flags_vax"] = t2_flags_vax
        res["t2_flags_duration"] = t2_flags_duration

    return res

def main():
    traces = load_all_traces()
    audits = [audit_turn2(r) for r in traces]
    
    print("\n" + "="*90)
    print("FORENSIC AUDIT: HOW MODELS RESPOND TO UNSTATED LOAD-BEARING VARIABLES IN TURN 2")
    print("="*90)
    
    models = sorted(list(set(r["model_key"] for r in traces)))
    
    print("\n1. MINOR HEAD INJURY (24mo) — Unwitnessed Fall & LOC:")
    print(f"{'Model':<14} | {'T1 Fabricated No-LOC':<22} | {'T2 Flagged Missing LOC':<24} | {'Confession Rate':<16}")
    print("-" * 80)
    head_a = [a for a in audits if a["case"] == "head_24mo"]
    for m in models:
        m_rows = [a for a in head_a if a["model"] == m]
        fab = sum(1 for r in m_rows if r["t1_fab_loc"])
        flag = sum(1 for r in m_rows if r["t2_flags_loc"])
        conf = sum(1 for r in m_rows if r.get("t2_confessed"))
        print(f"{m:<14} | {fab}/3 ({fab/3*100:3.0f}%)               | {flag}/3 ({flag/3*100:3.0f}%)                | {conf}/{fab if fab>0 else 1} ({conf/(fab if fab>0 else 1)*100:3.0f}%)")

    print("\n2. FIRST FEBRILE UTI (24mo) — Prior UTI History & Circumcision:")
    print(f"{'Model':<14} | {'T1 Asserted First UTI':<22} | {'T2 Flagged Prior UTI':<24} | {'T2 Flagged Circumcision':<22}")
    print("-" * 88)
    uti_a = [a for a in audits if a["case"] == "uti_24mo"]
    for m in models:
        m_rows = [a for a in uti_a if a["model"] == m]
        first = sum(1 for r in m_rows if r["t1_asserts_first"])
        p_uti = sum(1 for r in m_rows if r["t2_flags_prior_uti"])
        circ = sum(1 for r in m_rows if r["t2_flags_circ"])
        print(f"{m:<14} | {first}/3 ({first/3*100:3.0f}%)               | {p_uti}/3 ({p_uti/3*100:3.0f}%)                | {circ}/3 ({circ/3*100:3.0f}%)")

    print("\n3. FEBRILE SEIZURES (6mo) — Unstated Vaccines & Untimed Duration:")
    print(f"{'Model':<14} | {'T1 Asserted Vaccines':<22} | {'T2 Flagged Missing Vax':<24} | {'T2 Flagged Duration':<22}")
    print("-" * 88)
    seiz_a = [a for a in audits if a["case"] == "seizure_6mo"]
    for m in models:
        m_rows = [a for a in seiz_a if a["model"] == m]
        vax_t1 = sum(1 for r in m_rows if r["t1_asserts_vax"])
        vax_t2 = sum(1 for r in m_rows if r["t2_flags_vax"])
        dur_t2 = sum(1 for r in m_rows if r["t2_flags_duration"])
        print(f"{m:<14} | {vax_t1}/3 ({vax_t1/3*100:3.0f}%)               | {vax_t2}/3 ({vax_t2/3*100:3.0f}%)                | {dur_t2}/3 ({dur_t2/3*100:3.0f}%)")

    print("\n4. PNEUMONIA (5yo) — 30-Day Antibiotics & Atypical Contacts:")
    print(f"{'Model':<14} | {'T2 Flagged 30d Abx':<22} | {'T2 Flagged Atypical Contacts':<26}")
    print("-" * 68)
    cap_a = [a for a in audits if a["case"] == "cap_5y"]
    for m in models:
        m_rows = [a for a in cap_a if a["model"] == m]
        abx = sum(1 for r in m_rows if r["t2_flags_prior_abx"])
        atyp = sum(1 for r in m_rows if r["t2_flags_atypical"])
        print(f"{m:<14} | {abx}/3 ({abx/3*100:3.0f}%)          | {atyp}/3 ({atyp/3*100:3.0f}%)")

if __name__ == "__main__":
    main()
