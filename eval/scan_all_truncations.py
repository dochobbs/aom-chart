import os
import json
import glob
from collections import defaultdict

def scan_truncations():
    results_dir = "results"
    all_json_files = glob.glob(f"{results_dir}/**/*.json", recursive=True)
    print(f"Total JSON files found in {results_dir}: {len(all_json_files)}")

    truncations = []
    file_summary = defaultdict(int)

    for filepath in sorted(all_json_files):
        # Skip backup files for clean reporting (we can inspect them separately)
        if ".bak." in filepath or "source_snapshots" in filepath:
            continue
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            continue

        records = []
        if isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            if "results" in data and isinstance(data["results"], list):
                records = data["results"]
            elif "traces" in data and isinstance(data["traces"], list):
                records = data["traces"]
            elif "evaluations" in data and isinstance(data["evaluations"], list):
                records = data["evaluations"]
            elif any(k in data for k in ["raw_text", "response", "text", "plan", "turn1_response", "t1_text"]):
                records = [data]

        for idx, rec in enumerate(records):
            if not isinstance(rec, dict):
                continue

            # Identify all text fields (Turn 1, Turn 2, single response)
            text_fields = []
            if "raw_text" in rec: text_fields.append(("raw_text", rec["raw_text"], rec.get("output_tokens")))
            if "response" in rec: text_fields.append(("response", rec["response"], rec.get("output_tokens")))
            if "text" in rec and not text_fields: text_fields.append(("text", rec["text"], rec.get("output_tokens")))
            if "plan" in rec and not text_fields: text_fields.append(("plan", rec["plan"], rec.get("output_tokens")))
            if "turn1_response" in rec: text_fields.append(("turn1_response", rec["turn1_response"], rec.get("turn1_tokens") or rec.get("output_tokens")))
            if "turn2_response" in rec: text_fields.append(("turn2_response", rec["turn2_response"], rec.get("turn2_tokens")))
            if "t1_text" in rec: text_fields.append(("t1_text", rec["t1_text"], rec.get("t1_tokens")))
            if "t2_text" in rec: text_fields.append(("t2_text", rec["t2_text"], rec.get("t2_tokens")))

            if not text_fields:
                continue

            for field_name, text, tokens in text_fields:
                if isinstance(text, dict):
                    text = text.get("text") or str(text)
                if text is None:
                    text = ""

                output_tokens = tokens
                if output_tokens is None and "usage" in rec and isinstance(rec["usage"], dict):
                    output_tokens = rec["usage"].get("output_tokens") or rec["usage"].get("completion_tokens")

                stop_reason = rec.get("stop_reason") or rec.get("finish_reason")

                is_truncated = False
                reasons = []

                if stop_reason in ["max_tokens", "length"]:
                    is_truncated = True
                    reasons.append(f"stop_reason={stop_reason}")

                # If explicit 4000 limit was hit
                if output_tokens is not None and output_tokens in [4000, 4096]:
                    is_truncated = True
                    reasons.append(f"output_tokens={output_tokens}")
                
                # Check for truly empty responses where an error or abort occurred
                if len(text.strip()) == 0 and rec.get("error"):
                    is_truncated = True
                    reasons.append(f"error={rec.get('error')}")
                elif len(text.strip()) == 0 and ("model" in rec or "model_key" in rec):
                    is_truncated = True
                    reasons.append("empty_text")

                # Check if text abruptly cuts off mid-word or without punctuation when long
                if len(text) > 3000:
                    stripped = text.strip()
                    last_char = stripped[-1] if stripped else ""
                    # Check if ending is incomplete word or unclosed sentence
                    if last_char not in ".!?:\"'\n`)]}*" and output_tokens and output_tokens >= 3900:
                        is_truncated = True
                        reasons.append(f"abrupt_ending: ...{stripped[-25:]}")

                if is_truncated:
                    item = {
                        "file": filepath,
                        "record_idx": idx,
                        "field": field_name,
                        "model": rec.get("model") or rec.get("model_key") or rec.get("model_name") or rec.get("model_id"),
                        "case": rec.get("case") or rec.get("case_id"),
                        "output_tokens": output_tokens,
                        "stop_reason": stop_reason,
                        "text_len": len(text),
                        "reasons": reasons,
                        "preview": text.strip()[-60:] if text else ""
                    }
                    truncations.append(item)
                    file_summary[filepath] += 1

    print(f"\nAccurate Scan Complete! Found {len(truncations)} genuinely truncated/incomplete records across {len(file_summary)} files.\n")
    print("Breakdown by file:")
    for fpath, count in sorted(file_summary.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {fpath}: {count} truncated records")

    print("\nDetailed breakdown of all truncated records:")
    for t in truncations:
        print(f"[{t['file']} #idx {t['record_idx']} ({t['field']})] Model: {t['model']} | Case: {t['case']} | Tokens: {t['output_tokens']} | Stop: {t['stop_reason']} | Reasons: {t['reasons']}")
        if t['preview']:
            print(f"    Tail: ...{t['preview']!r}")

    with open("results/accurate_truncation_scan.json", "w", encoding="utf-8") as out:
        json.dump(truncations, out, indent=2)
    print("\nSaved inventory to results/accurate_truncation_scan.json")

if __name__ == "__main__":
    scan_truncations()
