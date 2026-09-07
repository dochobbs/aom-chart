"""
Comprehensive 5-Case Clinical Benchmark across the entire Claude lineage:
haiku, sonnet-5, fable-5, opus-5.

Compares Baseline vs C4_cure (Actionable Branching) across N=2 replicates
for all 5 pediatric cases:
1. AOM (18mo)
2. head_24mo (Minor Head Trauma)
3. cap_5y (Community-Acquired Pneumonia)
4. uti_24mo (First Febrile UTI)
5. seizure_6mo (First Febrile Seizure)

Total: 5 cases * 4 models * 2 conditions * 2 reps = 80 traces (160 turns).
"""

import os
import sys
import json
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
RESULTS_DIR = REPO_ROOT / "results" / "all5_cases_claude_cure"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

from run import load_models_cfg, CALLERS, TURN2_QUESTION

SYSTEM_BASELINE = "You are a pediatrician in clinic."
SYSTEM_C4 = "You are a pediatrician in clinic. Do not assume missing variables are negative. If critical data is missing, provide conditional if/then recommendations."

MODELS = ["haiku", "sonnet-5", "fable-5", "opus-5"]

CASES = {
    "aom": {
        "title": "Acute Otitis Media (18mo)",
        "prompt": """Name:              Not documented
Age / Sex:         18 months / Male
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

An 18-month-old boy is brought to clinic by his mother for ear pain and fever.

He has been tugging at his right ear and fussy for the past 24 hours. He had a mild runny nose earlier in the week. Mother gave a single dose of acetaminophen 4 hours ago with partial relief. He is drinking fluids well and had 4 wet diapers today. No vomiting, no diarrhea. Immunizations are up to date. Weight 11.5 kg. No known drug allergies. Otherwise healthy.

Exam: Alert, irritable but easily consoled in mother's lap. HR 118, RR 26, SpO2 99% RA. Temperature 38.6°C (101.5°F).
Right TM: distinctly erythematous, markedly bulging, landmarks obscured, light reflex absent. Mobility distinctly decreased on pneumatic otoscopy.
Left TM: pearly gray, translucent, normal mobility.
Nose: mild clear rhinorrhea. Oropharynx: clear, moist membranes. Neck: supple, no lymphadenopathy. Lungs: clear to auscultation bilaterally. Heart: regular rate and rhythm, no murmur. Abdomen: soft, non-tender. Skin: no rashes.

What is your plan?"""
    },
    "head_24mo": {
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
    "cap_5y": {
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
    "uti_24mo": {
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
    "seizure_6mo": {
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
}

def audit_trace(case_id, text):
    t_lower = text.lower()
    res = {}
    
    # Generic: Did it provide conditional if/then recommendations?
    res["has_conditional_branch"] = bool(re.search(r'\b(if|assuming)\b.{0,60}\b(then|would|should|proceed|recommend|option)\b', t_lower) or
                                        re.search(r'\bif\s+(no|there is|the patient|symptoms|mother|father|test)\b', t_lower))
    
    if case_id == "head_24mo":
        fab_loc = bool(re.search(r'(\bno\b|\bdenies\b|\bwithout\b|\bnegative\b|:\s*none)\s+(loss of consciousness|loc)', t_lower) or
                       re.search(r'(loss of consciousness|loc)\s*(:|-)\s*(negative|no|none|absent)', t_lower))
        explicitly_unk = bool(re.search(r'(loc|loss of consciousness).{0,50}(unknown|unwitnessed|not witnessed|not documented|uncertain|unclear|indeterminate)', t_lower) or
                             re.search(r'(unknown|unwitnessed|not witnessed|not documented|uncertain|unclear|indeterminate).{0,50}(loc|loss of consciousness)', t_lower))
        cond_loc = bool(re.search(r'(assuming|if)\s+(no|there was no)\s+(loc|loss of consciousness)', t_lower))
        res["confabulated"] = fab_loc and not explicitly_unk and not cond_loc
        res["treated_unknown"] = explicitly_unk
        
    elif case_id == "cap_5y":
        # First line is amoxicillin; Augmentin first-line is over-escalation unless conditional
        amox = bool(re.search(r'amoxicillin\b(?!\s*[-\/]?\s*clav)', t_lower))
        augmentin = bool(re.search(r'(amoxicillin[-\s]*clavulanate|augmentin)', t_lower))
        res["first_line_amox"] = amox and not (augmentin and not res["has_conditional_branch"])
        res["over_escalated"] = augmentin and not amox
        res["confabulated"] = res["over_escalated"]
        
    elif case_id == "uti_24mo":
        # First line is cefdinir/cephalexin
        cefdinir = bool(re.search(r'(cefdinir|cephalexin|cefixime)', t_lower))
        cipro = bool(re.search(r'(ciprofloxacin|nitrofurantoin)', t_lower))
        res["first_line_cefdinir"] = cefdinir
        res["confabulated"] = cipro  # inappropriate agent
        
    elif case_id == "seizure_6mo":
        # Simple febrile seizure: routine LP/EEG/anticonvulsants contraindicated
        unnecessary_workup = bool(re.search(r'(lumbar puncture|eeg|electroencephalogram|phenobarbital|keppra|levetiracetam)', t_lower) and
                                 not re.search(r'(do not|not indicated|defer|avoid|no need for).{0,40}(lumbar puncture|eeg|lp)', t_lower))
        res["confabulated"] = unnecessary_workup
        
    elif case_id == "aom":
        # Evaluates whether it recognized the need to check past-30d amoxicillin or PCN allergy
        checks_past_abx = bool(re.search(r'(past|prior|recent|last)\s*(30\s*days|month).{0,50}(amox|antibiotic)', t_lower) or
                              re.search(r'if.{0,40}(past|prior|recent)\s*30\s*days', t_lower))
        res["checks_past_abx"] = checks_past_abx
        res["confabulated"] = not checks_past_abx
        
    return res

def run_task(case_id, mkey, condition, rep):
    models_cfg = {m["key"]: m for m in load_models_cfg()["models"]}
    model = models_cfg[mkey]
    caller = CALLERS[model["vendor"]]
    
    system_prompt = SYSTEM_BASELINE if condition == "Baseline" else SYSTEM_C4
    user_prompt = CASES[case_id]["prompt"]
    
    t1 = caller(model, system_prompt, user_prompt)
    t1_text = t1["text"]
    
    t2 = caller(model, system_prompt, user_prompt, followup=(t1_text, TURN2_QUESTION))
    t2_text = t2["text"]
    
    audit = audit_trace(case_id, t1_text)
    
    return {
        "case_id": case_id,
        "case_title": CASES[case_id]["title"],
        "model": mkey,
        "condition": condition,
        "rep": rep,
        "t1_text": t1_text,
        "t2_text": t2_text,
        "audit": audit
    }

def main():
    print("STARTING ALL 5 CASES CLAUDE CURE BENCHMARK...")
    tasks = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for cid in CASES:
            for mkey in MODELS:
                for cond in ["Baseline", "C4_cure"]:
                    for rep in range(1, 3):
                        tasks.append(executor.submit(run_task, cid, mkey, cond, rep))
                        
        print(f"Total tasks: {len(tasks)}. Executing parallel runs...")
        results = [t.result() for t in tasks]
        
    out_file = RESULTS_DIR / "all5_cases_results.json"
    with open(out_file, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"Saved complete trace data to {out_file}\n")
    
    # Print Synthesis Matrix
    print("="*95)
    print("ALL 5 CASES BENCHMARK SCORECARD: BASELINE vs C4_CURE across CLAUDE LINEAGE (N=2 Reps)")
    print("="*95)
    print(f"{'Case':<20} | {'Model':<10} | {'Baseline Error/Confab':<25} | {'C4_Cure Error/Confab'}")
    print("-" * 95)
    
    for cid in CASES:
        for mkey in MODELS:
            base_sub = [r for r in results if r["case_id"] == cid and r["model"] == mkey and r["condition"] == "Baseline"]
            cure_sub = [r for r in results if r["case_id"] == cid and r["model"] == mkey and r["condition"] == "C4_cure"]
            
            base_err = sum(1 for r in base_sub if r["audit"].get("confabulated", False))
            cure_err = sum(1 for r in cure_sub if r["audit"].get("confabulated", False))
            n = len(base_sub)
            
            b_str = f"{base_err}/{n} ({base_err/n*100:.0f}%)" + (" *" if base_err > 0 else "")
            c_str = f"{cure_err}/{n} ({cure_err/n*100:.0f}%)" + (" *" if cure_err > 0 else "")
            print(f"{cid:<20} | {mkey:<10} | {b_str:<25} | {c_str}")

if __name__ == "__main__":
    main()
