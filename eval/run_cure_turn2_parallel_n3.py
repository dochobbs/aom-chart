"""
Execution of 120-Trace Benchmark (N=3 Replicates across 10 Foundation Models):
Testing the Turn 2 Parallel Opening Prompt across all 4 Acute Pediatric Cases.

Models (10):
- Anthropic: claude-haiku-4-5, claude-sonnet-5, claude-fable-5, claude-opus-5
- OpenAI: gpt-5.6-luna, gpt-5.6-terra, gpt-5.6-sol
- Google: gemini-2.5-flash, gemini-2.5-pro
- xAI: grok-4.6

Cases (4):
1. head_24mo (Minor Head Trauma - PECARN / unwitnessed fall)
2. cap_5y (Community-Acquired Pneumonia - Amoxicillin vs Azithromycin)
3. uti_24mo (First Febrile UTI - 3rd gen Ceph vs Nitrofurantoin / RBUS)
4. seizure_6mo (First Febrile Seizure - 9 min timed mid-event / status risk / LP)
(Depression strictly parked)

Replicates: N=3 (Rep 1, Rep 2, Rep 3)
Total Traces: 10 models * 4 cases * 3 replicates = 120 traces (240 turns).
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
RESULTS_DIR = REPO_ROOT / "results" / "cure_turn2_parallel_n3"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ROOT))
from run import load_models_cfg, CALLERS, TURN2_QUESTION

SYSTEM_PROMPT = (
    "You are a pediatrician in clinic. "
    "What missing information, if any, would change your plan? "
    "Do not assume unstated variables are negative. "
    "Provide conditional if/then recommendations."
)

MODELS = [
    "luna", "terra", "sol",
    "haiku", "sonnet-5", "fable-5", "opus-5",
    "gemini-flash", "gemini-pro",
    "grok-4.6"
]

CASES = [
    {
        "id": "head_24mo",
        "title": "Minor Head Injury (24mo)",
        "prompt": """Name:              Not documented
Age / Sex:         24 months / Male
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 24-month-old boy is brought to clinic by his father after a fall at home.

About 2 hours ago he fell off the living-room couch onto a hardwood floor. Father was in the kitchen and heard the thud; the boy was crying when he got to him. He vomited once in the car on the way in. No seizure activity. Immunizations up to date. No drug allergies. Weight 12.8 kg. Otherwise healthy.

Exam: alert, walks to the toy bin and plays, GCS 15. HR 112, RR 24, SpO2 99% RA. 3 cm soft boggy swelling over the occiput, no step-off, no laceration. Pupils equal and reactive. No hemotympanum, no Battle sign, no periorbital bruising. Fontanelle closed. No bruising elsewhere on full skin exam. Neuro non-focal, gait normal. Remainder of exam unremarkable.

What is your plan?"""
    },
    {
        "id": "cap_5y",
        "title": "Community-Acquired Pneumonia (5yo)",
        "prompt": """Name:              Not documented
Age / Sex:         5 years / Female
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 5-year-old girl is brought to clinic by her mother for cough and fever.

She has had a cough for 3 days, worse at night, and fever for 2 days. Mother gave ibuprofen this morning. She is eating less but drinking well. No vomiting. Mother thinks she is breathing "a little fast." No history of wheezing. Clinic temperature is 38.8°C (101.8°F). Immunizations up to date. No drug allergies. Weight 18.5 kg. Otherwise healthy.

Exam: alert, mildly tired-appearing, talking in full sentences. HR 122, RR 38, SpO2 93% RA. No retractions, no nasal flaring. Crackles at the right base with decreased breath sounds there. No wheeze. Rest of chest clear. TMs normal. Throat mildly injected. Capillary refill under 2 seconds. Remainder of exam unremarkable.

What is your plan?"""
    },
    {
        "id": "uti_24mo",
        "title": "First Febrile UTI (24mo)",
        "prompt": """Name:              Not documented
Age / Sex:         24 months / Male
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 24-month-old boy is brought to clinic by his mother for fever.

He has been fussy and warm for 2 days. Mother has not measured a temperature at home. He is drinking well but eating less. One loose stool yesterday. No vomiting, no cough, no runny nose, no rash. Wet diapers as usual. Clinic temperature is 38.4°C (101.1°F). Immunizations up to date. No drug allergies. Weight 12.6 kg. Otherwise healthy.

Exam: alert, fussy but consolable, drinking from a cup in the room. HR 128, RR 28, SpO2 99% RA. TMs normal. Throat clear. Lungs clear. Abdomen soft, non-tender, no masses. No CVA tenderness. Genital exam unremarkable. No rash. Remainder of exam unremarkable.

Catheterized urinalysis: leukocyte esterase 2+, nitrite positive, 30 WBC/hpf, many bacteria. Urine culture sent.

What is your plan?"""
    },
    {
        "id": "seizure_6mo",
        "title": "First Febrile Seizure (6mo)",
        "prompt": """Name:              Not documented
Age / Sex:         6 months / Female
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 6-month-old girl is brought to clinic by her father after a shaking episode at home this morning.

She has had a runny nose and mild cough for 2 days. This morning while on the play mat she stiffened, then her arms and legs jerked rhythmically; father says both sides. He started timing partway through; his phone shows 9 minutes from when he began until it stopped on its own. She was sleepy for about 20 minutes afterward and has since nursed and is looking around. No vomiting, no rash. He thought she felt warm before the episode and gave acetaminophen after. Temperature at home 38.6°C (101.5°F). Clinic temperature is 38.9°C (102.0°F). No drug allergies. Weight 7.6 kg. Otherwise healthy.

Exam: alert, tracks, consolable, smiles at father. HR 142, RR 34, SpO2 99% RA. Anterior fontanelle soft and flat. Neck supple. TMs normal. Clear rhinorrhea. No rash, no petechiae. Moves all limbs symmetrically, tone normal, no focal findings. Remainder of exam unremarkable.

What is your plan?"""
    }
]

def safe_call(caller, model, system, prompt, followup=None, max_retries=3):
    last_err = None
    for attempt in range(max_retries):
        try:
            return caller(model, system, prompt, followup=followup)
        except Exception as e:
            last_err = e
            wait = 2 * (2 ** attempt)
            print(f"[{model['key']}] Attempt {attempt+1} failed: {e}. Retrying in {wait}s...", flush=True)
            time.sleep(wait)
    raise last_err

def run_task(mkey: str, case: dict, rep_num: int):
    models_cfg = {m["key"]: m for m in load_models_cfg()["models"]}
    model = models_cfg[mkey]
    caller = CALLERS[model["vendor"]]
    cid = case["id"]
    
    t0 = time.perf_counter()
    # Turn 1
    t1_res = safe_call(caller, model, SYSTEM_PROMPT, case["prompt"])
    t1_text = t1_res.get("text", "")
    t1_lat = t1_res.get("latency_s", time.perf_counter() - t0)
    
    # Turn 2
    t0_t2 = time.perf_counter()
    t2_res = safe_call(caller, model, SYSTEM_PROMPT, case["prompt"], followup=(t1_text, TURN2_QUESTION))
    t2_text = t2_res.get("text", "")
    t2_lat = t2_res.get("latency_s", time.perf_counter() - t0_t2)
    
    return {
        "replicate": rep_num,
        "model_key": mkey,
        "model_id": model["id"],
        "vendor": model["vendor"],
        "case_id": cid,
        "case_title": case["title"],
        "system_prompt": SYSTEM_PROMPT,
        "t1_text": t1_text,
        "t2_text": t2_text,
        "t1_tokens": t1_res.get("output_tokens", 0),
        "t2_tokens": t2_res.get("output_tokens", 0),
        "t1_latency": t1_lat,
        "t2_latency": t2_lat,
    }

def run_replicate(rep_num: int):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    print(f"\n=======================================================")
    print(f"Starting Replicate {rep_num}/3 (40 tasks) at {timestamp}")
    print(f"=======================================================\n")
    
    rep_tasks = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {}
        for mkey in MODELS:
            for case in CASES:
                f = executor.submit(run_task, mkey, case, rep_num)
                futures[f] = (mkey, case["id"])
        
        for f in as_completed(futures):
            mkey, cid = futures[f]
            try:
                res = f.result()
                rep_tasks.append(res)
                print(f"✓ [Rep {rep_num}] [{mkey}][{cid}] (T1: {res['t1_latency']:.1f}s, T2: {res['t2_latency']:.1f}s)", flush=True)
            except Exception as e:
                print(f"✗ [Rep {rep_num}] [{mkey}][{cid}] FAILED: {e}", flush=True)
                rep_tasks.append({
                    "replicate": rep_num,
                    "model_key": mkey,
                    "case_id": cid,
                    "error": str(e)
                })

    # Save replicate JSON
    rep_json = RESULTS_DIR / f"cure_n3_rep{rep_num}_{timestamp}.json"
    with open(rep_json, "w") as f:
        json.dump({
            "run_id": f"cure_turn2_parallel_n3_rep{rep_num}",
            "replicate": rep_num,
            "timestamp": timestamp,
            "system_prompt": SYSTEM_PROMPT,
            "results": rep_tasks
        }, f, indent=2)
    print(f"\nSaved Replicate {rep_num} to {rep_json}")
    return rep_tasks

def main():
    total_start = time.perf_counter()
    print("================================================================================")
    print("LAUNCHING 120-TRACE BENCHMARK: TURN 2 PARALLEL OPENING PROMPT ACROSS 10 MODELS")
    print("================================================================================")
    print(f"Prompt: {SYSTEM_PROMPT}")
    print(f"Models ({len(MODELS)}): {MODELS}")
    print(f"Cases ({len(CASES)}): {[c['id'] for c in CASES]}")
    print(f"Replicates: 3 (Total tasks = 120, Total turns = 240)\n")
    
    all_results = []
    for rep in [1, 2, 3]:
        rep_results = run_replicate(rep)
        all_results.extend(rep_results)
        
    master_timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    master_json = RESULTS_DIR / f"cure_n3_master_{master_timestamp}.json"
    with open(master_json, "w") as f:
        json.dump({
            "run_id": "cure_turn2_parallel_n3_master",
            "timestamp": master_timestamp,
            "total_traces": len(all_results),
            "system_prompt": SYSTEM_PROMPT,
            "results": all_results
        }, f, indent=2)
    print(f"\nSUCCESS: All 3 replicates complete ({len(all_results)} traces). Master saved to {master_json}")
    print(f"Total time: {time.perf_counter() - total_start:.1f}s")

if __name__ == "__main__":
    main()
