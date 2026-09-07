"""
High-Thinking / Extended Reasoning Spectrum Runner:
Tests the 4 acute pediatric cases across models at their MAXIMUM / HIGH thinking configurations:
- OpenAI (luna, terra, sol): reasoning_effort = "high"
- Anthropic (opus-5, sonnet-5): thinking = {"type": "adaptive"}, output_config = {"effort": "high"}
- Anthropic (haiku): thinking = {"type": "enabled", "budget_tokens": 4096}, max_tokens = 8000
- Google (gemini-flash, gemini-pro): thinking_budget = 16384
- OpenRouter (grok-4.6, fable-5): standard provider routing
"""

import os
import sys
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from run import load_models_cfg, TURN2_QUESTION

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
RESULTS_DIR = REPO_ROOT / "results" / "high_thinking_4cases"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

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

SYSTEM_PROMPT = "You are a pediatrician in clinic."

def call_openai_high(model, system, user, followup=None):
    from openai import OpenAI
    client = OpenAI()
    t0 = time.perf_counter()
    if followup:
        prior, question = followup
        payload = [
            {"role": "user", "content": f"{system}\n\n{user}"},
            {"role": "assistant", "content": prior},
            {"role": "user", "content": question},
        ]
    else:
        payload = f"{system}\n\n{user}"
    resp = client.responses.create(
        model=model["id"],
        reasoning={"effort": "high"},
        input=payload,
    )
    return {
        "text": resp.output_text or "",
        "input_tokens": getattr(resp.usage, "input_tokens", 0),
        "output_tokens": getattr(resp.usage, "output_tokens", 0),
        "latency_s": time.perf_counter() - t0,
    }

def call_anthropic_high(model, system, user, followup=None):
    from anthropic import Anthropic
    client = Anthropic()
    t0 = time.perf_counter()
    messages = [{"role": "user", "content": user}]
    if followup:
        prior, question = followup
        messages.append({"role": "assistant", "content": prior})
        messages.append({"role": "user", "content": question})
        
    m_id = model["id"]
    kwargs = {
        "model": m_id,
        "system": system,
        "messages": messages,
    }
    
    if m_id in ["claude-opus-5", "claude-sonnet-5"]:
        kwargs["max_tokens"] = 6000
        kwargs["thinking"] = {"type": "adaptive"}
        kwargs["output_config"] = {"effort": "high"}
    elif m_id == "claude-haiku-4-5":
        kwargs["max_tokens"] = 8000
        kwargs["thinking"] = {"type": "enabled", "budget_tokens": 4096}
    else:
        kwargs["max_tokens"] = 4000
        
    resp = client.messages.create(**kwargs)
    text = "".join(block.text for block in resp.content if block.type == "text")
    return {
        "text": text,
        "input_tokens": resp.usage.input_tokens,
        "output_tokens": resp.usage.output_tokens,
        "latency_s": time.perf_counter() - t0,
    }

def call_gemini_high(model, system, user, followup=None):
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    t0 = time.perf_counter()
    if followup:
        prior, question = followup
        contents = [
            {"role": "user", "parts": [{"text": user}]},
            {"role": "model", "parts": [{"text": prior}]},
            {"role": "user", "parts": [{"text": question}]},
        ]
    else:
        contents = user
    resp = client.models.generate_content(
        model=model["id"],
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system,
            max_output_tokens=6000,
            thinking_config=types.ThinkingConfig(thinking_budget=16384),
        ),
    )
    return {
        "text": resp.text or "",
        "input_tokens": getattr(resp.usage_metadata, "prompt_token_count", 0) if hasattr(resp, "usage_metadata") else 0,
        "output_tokens": getattr(resp.usage_metadata, "candidates_token_count", 0) if hasattr(resp, "usage_metadata") else 0,
        "latency_s": time.perf_counter() - t0,
    }

def call_openrouter_std(model, system, user, followup=None):
    from openai import OpenAI
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY"),
    )
    t0 = time.perf_counter()
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    if followup:
        prior, question = followup
        messages.append({"role": "assistant", "content": prior})
        messages.append({"role": "user", "content": question})
    resp = client.chat.completions.create(
        model=model["id"],
        messages=messages,
        max_tokens=4000,
    )
    choice = resp.choices[0]
    usage = resp.usage
    return {
        "text": choice.message.content or "",
        "input_tokens": getattr(usage, "prompt_tokens", 0) or 0,
        "output_tokens": getattr(usage, "completion_tokens", 0) or 0,
        "latency_s": time.perf_counter() - t0,
    }

HIGH_CALLERS = {
    "openai": call_openai_high,
    "anthropic": call_anthropic_high,
    "gemini": call_gemini_high,
    "openrouter": call_openrouter_std,
}

def run_single_high_task(model, case):
    caller = HIGH_CALLERS[model["vendor"]]
    cid = case["id"]
    mkey = model["key"]
    print(f"[High-Thinking] [{cid}] Running {mkey} Turn 1...", flush=True)
    
    try:
        t1_res = caller(model, SYSTEM_PROMPT, case["prompt"])
        t1_text = t1_res["text"]
        
        print(f"[High-Thinking] [{cid}] Running {mkey} Turn 2...", flush=True)
        t2_res = caller(
            model,
            SYSTEM_PROMPT,
            case["prompt"],
            followup=(t1_text, TURN2_QUESTION)
        )
        t2_text = t2_res["text"]
        
        return {
            "condition": "high_thinking",
            "case_id": cid,
            "case_title": case["title"],
            "model_key": mkey,
            "model_id": model["id"],
            "vendor": model["vendor"],
            "t1_text": t1_text,
            "t2_text": t2_text,
            "t1_tokens": t1_res.get("output_tokens", 0),
            "t2_tokens": t2_res.get("output_tokens", 0),
            "t1_latency": t1_res.get("latency_s", 0),
            "t2_latency": t2_res.get("latency_s", 0),
            "error": None
        }
    except Exception as e:
        print(f"[High-Thinking] [{cid}] ERROR on {mkey}: {e}", flush=True)
        return {
            "condition": "high_thinking",
            "case_id": cid,
            "case_title": case["title"],
            "model_key": mkey,
            "model_id": model["id"],
            "vendor": model["vendor"],
            "t1_text": None,
            "t2_text": None,
            "error": str(e)
        }

def main():
    import argparse
    parser = argparse.ArgumentParser(description="High-Thinking Runner for 4 Acute Cases")
    parser.add_argument("--rep", type=int, default=1, help="Replicate number (1, 2, or 3)")
    parser.add_argument("--workers", type=int, default=5, help="Concurrent workers")
    args = parser.parse_args()
    rep = args.rep
    workers = args.workers

    cfg = load_models_cfg()
    models = cfg["models"]
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"high_thinking_4cases_rep{rep}_{timestamp}"
    out_json = RESULTS_DIR / f"{run_id}.json"
    out_md = RESULTS_DIR / f"{run_id}.md"
    
    print(f"\nSTARTING HIGH-THINKING RUN (Rep {rep}): {run_id} with {workers} workers\n", flush=True)
    
    tasks = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        for c in CASES:
            for m in models:
                tasks.append(executor.submit(run_single_high_task, m, c))
                
        results = [t.result() for t in tasks]

    for r in results:
        r["replicate"] = rep
        
    payload = {
        "run_id": run_id,
        "condition": "high_thinking",
        "replicate": rep,
        "timestamp": timestamp,
        "results": results
    }
    
    with open(out_json, "w") as f:
        json.dump(payload, f, indent=2)
        
    md_lines = [
        f"# High-Thinking Run: 4 Acute Cases x 10 Foundation Lab Models (`{run_id}`)",
        f"**Timestamp:** {timestamp}",
        f"**Replicate:** {rep}",
        f"**Thinking Mode:** Maximum / High Reasoning Effort across all models",
        f"**Models:** {', '.join([m['key'] for m in models])}",
        f"**Cases:** Head Injury (24mo), CAP (5y), Febrile UTI (24mo), Febrile Seizure (6mo)",
        "",
        "---"
    ]
    
    for c in CASES:
        cid = c["id"]
        md_lines.append(f"\n## Case: {c['title']} (`{cid}`)\n")
        case_res = [r for r in results if r["case_id"] == cid]
        
        for r in sorted(case_res, key=lambda x: x["model_key"]):
            mkey = r["model_key"]
            err = r.get("error")
            md_lines.append(f"### Model: `{mkey}` ({r['model_id']}) — High Thinking (Rep {rep})\n")
            if err:
                md_lines.append(f"**ERROR:** {err}\n")
                continue
                
            md_lines.append("#### Turn 1: Immediate Plan\n")
            md_lines.append(r["t1_text"] or "")
            md_lines.append("\n---\n")
            md_lines.append("#### Turn 2: What Missing Information Would Change Plan?\n")
            md_lines.append(r["t2_text"] or "")
            md_lines.append("\n---\n")
            
    with open(out_md, "w") as f:
        f.write("\n".join(md_lines))
        
    print(f"\nSUCCESS! Saved high-thinking results to: {out_json}", flush=True)

if __name__ == "__main__":
    main()

