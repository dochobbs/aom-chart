"""
Evaluation of the Remaining 6 Foundation Models under the Turn 2 Parallel Opening Prompt:
OpenAI: gpt-5.6-luna, gpt-5.6-terra, gpt-5.6-sol
Google: gemini-2.5-flash, gemini-2.5-pro
xAI: grok-4.6

Cases (Depression strictly parked):
1. head_24mo (Minor Head Injury)
2. cap_5y (Community-Acquired Pneumonia)
3. uti_24mo (First Febrile UTI)
4. seizure_6mo (First Febrile Seizure)

Turn 1 System / Opening Prompt parallels the AOM Turn 2 query:
"You are a pediatrician in clinic. What missing information, if any, would change your plan? Do not assume unstated variables are negative. Provide conditional if/then recommendations."

Symmetrical Two-Turn Protocol:
Turn 1: Clinical vignette -> "What is your plan?"
Turn 2: "What missing information, if any, would have changed this plan?"
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
RESULTS_DIR = REPO_ROOT / "results" / "cure_6models_turn2_parallel"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ROOT))
from run import load_models_cfg, CALLERS, TURN2_QUESTION

SYSTEM_PROMPT = (
    "You are a pediatrician in clinic. "
    "What missing information, if any, would change your plan? "
    "Do not assume unstated variables are negative. "
    "Provide conditional if/then recommendations."
)

MODELS = ["luna", "terra", "sol", "gemini-flash", "gemini-pro", "grok-4.6"]

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

def run_task(mkey: str, case: dict):
    models_cfg = {m["key"]: m for m in load_models_cfg()["models"]}
    model = models_cfg[mkey]
    caller = CALLERS[model["vendor"]]
    
    t0 = time.perf_counter()
    print(f"[{mkey}][{case['id']}] Running Turn 1...", flush=True)
    t1_res = caller(model, SYSTEM_PROMPT, case["prompt"])
    t1_text = t1_res.get("text", "")
    t1_lat = t1_res.get("latency_s", time.perf_counter() - t0)
    
    t0_t2 = time.perf_counter()
    print(f"[{mkey}][{case['id']}] Running Turn 2...", flush=True)
    t2_res = caller(model, SYSTEM_PROMPT, case["prompt"], followup=(t1_text, TURN2_QUESTION))
    t2_text = t2_res.get("text", "")
    t2_lat = t2_res.get("latency_s", time.perf_counter() - t0_t2)
    
    return {
        "model_key": mkey,
        "model_id": model["id"],
        "vendor": model["vendor"],
        "case_id": case["id"],
        "case_title": case["title"],
        "system_prompt": SYSTEM_PROMPT,
        "t1_text": t1_text,
        "t2_text": t2_text,
        "t1_tokens": t1_res.get("output_tokens", 0),
        "t2_tokens": t2_res.get("output_tokens", 0),
        "t1_latency": t1_lat,
        "t2_latency": t2_lat,
    }

def main():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    print(f"Starting 6-Model Turn 2 Parallel Benchmark at {timestamp}...")
    print(f"System Prompt: {SYSTEM_PROMPT}")
    print(f"Models ({len(MODELS)}): {MODELS}")
    print(f"Cases ({len(CASES)}): {[c['id'] for c in CASES]}")
    
    tasks = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {}
        for mkey in MODELS:
            for case in CASES:
                f = executor.submit(run_task, mkey, case)
                futures[f] = (mkey, case["id"])
        
        for f in as_completed(futures):
            mkey, cid = futures[f]
            try:
                res = f.result()
                tasks.append(res)
                print(f"✓ Completed [{mkey}][{cid}] (T1: {res['t1_latency']:.1f}s, T2: {res['t2_latency']:.1f}s)", flush=True)
            except Exception as e:
                print(f"✗ Failed [{mkey}][{cid}]: {e}", flush=True)
                tasks.append({
                    "model_key": mkey,
                    "case_id": cid,
                    "error": str(e)
                })

    # Save results
    json_path = RESULTS_DIR / f"turn2_parallel_6models_{timestamp}.json"
    md_path = RESULTS_DIR / f"turn2_parallel_6models_{timestamp}.md"
    
    with open(json_path, "w") as f:
        json.dump({"timestamp": timestamp, "system_prompt": SYSTEM_PROMPT, "results": tasks}, f, indent=2)
    
    print(f"\nSaved raw JSON to {json_path}")

    # Generate Markdown Summary
    md_lines = [
        "# Turn 2 Parallel Prompt Benchmark: 6 Non-Claude Models Across 4 Acute Cases",
        f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"**System Prompt:** `{SYSTEM_PROMPT}`",
        f"**Models:** {', '.join(MODELS)}",
        f"**Cases:** {', '.join([c['id'] for c in CASES])} (Depression parked)",
        "",
        "---",
        ""
    ]

    for item in sorted(tasks, key=lambda x: (x.get("case_id", ""), x.get("model_key", ""))):
        cid = item.get("case_id")
        mkey = item.get("model_key")
        md_lines.append(f"## [{mkey}] Case: {cid}")
        md_lines.append(f"**Latency:** T1={item.get('t1_latency', 0):.2f}s | T2={item.get('t2_latency', 0):.2f}s")
        md_lines.append("\n### Turn 1: Actionable Plan\n")
        md_lines.append(item.get("t1_text", "ERROR"))
        md_lines.append("\n### Turn 2: Missing Information Audit\n")
        md_lines.append(item.get("t2_text", "ERROR"))
        md_lines.append("\n---\n")

    with open(md_path, "w") as f:
        f.write("\n".join(md_lines))
    print(f"Saved Markdown report to {md_path}")

if __name__ == "__main__":
    main()
