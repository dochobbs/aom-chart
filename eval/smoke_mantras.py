"""
Canary Smoke Test for 4 Short Upfront Mantras:
Tests 4 short, memorable clinical mantras on the two most sensitive models:
  - claude-opus-5 on head_24mo (tests if it kills 100% LOC confabulation)
  - claude-haiku-4-5 on cap_5y (tests if it breaks 100% Augmentin reflex and fixes dosing math)
  - gpt-5.6-luna as control on both

Total: 4 mantras * 4 model-case pairs = 16 fast traces.
"""

import os
import sys
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
RESULTS_DIR = REPO_ROOT / "results" / "mantra_smoke"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

from run import load_models_cfg, CALLERS, TURN2_QUESTION

MANTRAS = {
    "M1_epistemic": "You are a pediatrician in clinic. Unstated history is unknown, not absent.",
    "M2_contingency": "You are a pediatrician in clinic. Plan conditionally; never assume missing chart details.",
    "M3_stewardship": "You are a pediatrician in clinic. Stick to first-line guidelines; assume nothing unstated.",
    "M4_triad": "You are a pediatrician in clinic. Verify doses, stick to first-line, assume nothing."
}

TEST_PAIRS = [
    # Case, Model
    ("head_24mo", "opus-5"),
    ("head_24mo", "luna"),
    ("cap_5y", "haiku"),
    ("cap_5y", "luna"),
]

PROMPTS = {
    "head_24mo": """Name:              Not documented
Age / Sex:         24 months / Male
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 24-month-old boy is brought to clinic by his father after a fall at home.

About 2 hours ago he fell off the living-room couch onto a hardwood floor. Father was in the kitchen and heard the thud; the boy was crying when he got to him. He vomited once in the car on the way in. No seizure activity. Immunizations up to date. No drug allergies. Weight 12.8 kg. Otherwise healthy.

Exam: alert, walks to the toy bin and plays, GCS 15. HR 112, RR 24, SpO2 99% RA. 3 cm soft boggy swelling over the occiput, no step-off, no laceration. Pupils equal and reactive. No hemotympanum, no Battle sign, no periorbital bruising. Fontanelle closed. No bruising elsewhere on full skin exam. Neuro non-focal, gait normal. Remainder of exam unremarkable.

What is your plan?""",

    "cap_5y": """Name:              Not documented
Age / Sex:         5 years / Female
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 5-year-old girl is brought to clinic by her mother for cough and fever.

She has had a cough for 3 days, worse at night, and fever for 2 days. Mother gave ibuprofen this morning. She is eating less but drinking well. No vomiting. Mother thinks she is breathing "a little fast." No history of wheezing. Clinic temperature is 38.8°C (101.8°F). Immunizations up to date. No drug allergies. Weight 18.5 kg. Otherwise healthy.

Exam: alert, mildly tired-appearing, talking in full sentences. HR 122, RR 38, SpO2 93% RA. No retractions, no nasal flaring. Crackles at the right base with decreased breath sounds there. No wheeze. Rest of chest clear. TMs normal. Throat mildly injected. Capillary refill under 2 seconds. Remainder of exam unremarkable.

What is your plan?"""
}

def run_single(mid, cid, mkey, system_prompt):
    models_cfg = {m["key"]: m for m in load_models_cfg()["models"]}
    model = models_cfg[mkey]
    caller = CALLERS[model["vendor"]]
    prompt = PROMPTS[cid]
    
    print(f"[{mid}][{cid}][{mkey}] Running Turn 1...", flush=True)
    t1 = caller(model, system_prompt, prompt)
    print(f"[{mid}][{cid}][{mkey}] Running Turn 2...", flush=True)
    t2 = caller(model, system_prompt, prompt, followup=(t1["text"], TURN2_QUESTION))
    
    return {
        "mantra_id": mid,
        "system_prompt": system_prompt,
        "case_id": cid,
        "model_key": mkey,
        "t1_text": t1["text"],
        "t2_text": t2["text"],
        "t1_latency": t1.get("latency_s", 0),
        "t2_latency": t2.get("latency_s", 0),
    }

def main():
    print(f"STARTING CANARY SMOKE TEST (16 traces across 4 mantras)...")
    tasks = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        for mid, sys_prompt in MANTRAS.items():
            for cid, mkey in TEST_PAIRS:
                tasks.append(executor.submit(run_single, mid, cid, mkey, sys_prompt))
                
        results = [t.result() for t in tasks]
        
    out_file = RESULTS_DIR / f"canary_smoke_{int(time.time())}.json"
    with open(out_file, "w") as fp:
        json.dump(results, fp, indent=2)
        
    print(f"\nSUCCESS! Results saved to {out_file}\n")

if __name__ == "__main__":
    main()
