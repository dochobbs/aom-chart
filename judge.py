"""Buddy-judge a results JSON. Sonnet-5 default; Terra grades Claude."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import render

ROOT = Path(__file__).resolve().parent
PROMPT_PATH = ROOT / "judge_prompt.txt"

BUDDY_DEFAULT = {"key": "sonnet-5", "vendor": "anthropic", "id": "claude-sonnet-5"}

COMPARE_FIELDS = (
    "plan",
    "snap",
    "followup_mentioned",
    "followup_stance",
    "followup_hallucinated",
    "reliability_language",
    "age_stratum",
)

FAIL_FIELDS = (
    "omission",
    "hallucinated_fact",
    "harmful_commission",
    "citation_failure",
    "stale_guidance",
    "rule_error",
)


def buddy_for(sut_key: str) -> dict:
    """Sonnet grades non-Claude. Terra grades Claude. Grok does not judge Grok."""
    if sut_key in {"opus-5", "sonnet-5", "haiku", "fable-5"}:
        return {"key": "terra", "vendor": "openai", "id": "gpt-5.6-terra"}
    if sut_key == "grok-4.6":
        return BUDDY_DEFAULT
    return BUDDY_DEFAULT


def call_openai(model_id: str, system: str, user: str) -> str:
    from openai import OpenAI

    resp = OpenAI().responses.create(
        model=model_id,
        reasoning={"effort": "low"},
        input=f"{system}\n\n{user}",
    )
    return resp.output_text or ""


def call_anthropic(model_id: str, system: str, user: str) -> str:
    from anthropic import Anthropic

    resp = Anthropic().messages.create(
        model=model_id,
        max_tokens=1200,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(b.text for b in resp.content if b.type == "text")


def call_gemini(model_id: str, system: str, user: str) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    resp = client.models.generate_content(
        model=model_id,
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=system,
            max_output_tokens=1200,
        ),
    )
    return resp.text or ""


def parse_json(text: str) -> dict:
    """Parse a JSON object from a model reply."""
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.S)
    if fence:
        text = fence.group(1)
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < 0:
        raise ValueError("no JSON object in buddy reply")
    return json.loads(text[start : end + 1])


def reconstruct_prompt(packet: dict, by_id: dict, variant_id: str) -> str:
    """Rebuild the SUT prompt for this cell."""
    return render.render_prompt(packet, by_id[variant_id])


def _call(buddy: dict, system: str, user: str) -> str:
    if buddy["vendor"] == "anthropic":
        return call_anthropic(buddy["id"], system, user)
    if buddy["vendor"] == "openai":
        return call_openai(buddy["id"], system, user)
    if buddy["vendor"] == "gemini":
        return call_gemini(buddy["id"], system, user)
    raise RuntimeError(buddy["vendor"])


def score_one(system: str, prompt: str, answer: str, sut_key: str) -> tuple[dict, dict]:
    """Return (buddy_meta, parsed score)."""
    buddy = buddy_for(sut_key)
    user = (
        f"## Prompt the model saw\n\n{prompt}\n\n"
        f"## Model answer\n\n{answer}\n\n"
        "Score the answer. JSON only."
    )
    t0 = time.perf_counter()
    raw = _call(buddy, system, user)
    try:
        parsed = parse_json(raw)
    except (ValueError, json.JSONDecodeError):
        raw = _call(
            buddy,
            system,
            user
            + "\n\nYour previous reply was not valid JSON. Reply with ONLY the JSON object. No markdown.",
        )
        parsed = parse_json(raw)
    meta = {
        "buddy_key": buddy["key"],
        "buddy_id": buddy["id"],
        "latency_s": time.perf_counter() - t0,
    }
    return meta, parsed


def disagree(grok_row: dict | None, buddy: dict) -> list[str]:
    """Field names that differ. Skip if no grok score."""
    if not grok_row:
        return []
    diffs = []
    for field in COMPARE_FIELDS:
        g, b = grok_row.get(field), buddy.get(field)
        if field == "followup_stance" and buddy.get("followup_mentioned") == "no":
            b = None
        if g != b:
            diffs.append(field)
    for field in FAIL_FIELDS:
        g = grok_row.get("failures", {}).get(field, {})
        b = buddy.get(field, {})
        gy = g.get("yes") if isinstance(g, dict) else None
        by = b.get("yes") if isinstance(b, dict) else None
        if gy and by and gy != by:
            diffs.append(field)
    return diffs


def load_grok_index(path: Path | None) -> dict:
    if not path or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for row in data.get("rows", []):
        key = (row.get("model_key"), row.get("variant_id"), row.get("replicate"))
        out[key] = row
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Buddy-judge SUT answers")
    parser.add_argument("--source", required=True, help="results/*.json from run.py")
    parser.add_argument("--grok-scores", help="Optional scored JSON to diff")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--only-cell", help="Restrict to one variant id")
    parser.add_argument("--only-model", action="append")
    parser.add_argument("--append", action="store_true", help="Merge into existing buddy JSON")
    args = parser.parse_args()

    source = Path(args.source)
    raw = json.loads(source.read_text(encoding="utf-8"))
    packet = render.load_packet()
    by_id = {v["id"]: v for v in packet["variants"]}
    system = PROMPT_PATH.read_text(encoding="utf-8").strip()
    grok = load_grok_index(Path(args.grok_scores) if args.grok_scores else None)
    if not grok:
        default_scored = source.with_name(source.stem + "_scored.json")
        grok = load_grok_index(default_scored)

    rows = raw["rows"]
    if args.only_cell:
        rows = [r for r in rows if r["variant_id"] == args.only_cell]
    if args.only_model:
        allow = set(args.only_model)
        rows = [r for r in rows if r["model_key"] in allow]
    if args.limit:
        rows = rows[: args.limit]

    out_rows = []
    disagree_lines = [
        f"# Disagreements — buddy vs Grok on `{source.name}`",
        "",
        "Doc resolves `plan`, `followup_hallucinated`, `reliability_language`, `age_stratum`, failure yes/no.",
        "",
    ]
    n_diff = 0
    for row in rows:
        if row.get("error"):
            continue
        print(f"{row['model_key']} / {row['variant_id']} / r{row.get('replicate', 1)} ...", flush=True)
        try:
            prompt = reconstruct_prompt(packet, by_id, row["variant_id"])
            meta, score = score_one(system, prompt, row["text"], row["model_key"])
            rec = {
                "model_key": row["model_key"],
                "variant_id": row["variant_id"],
                "replicate": row.get("replicate", 1),
                **meta,
                "score": score,
                "error": None,
            }
        except Exception as exc:  # noqa: BLE001
            rec = {
                "model_key": row["model_key"],
                "variant_id": row["variant_id"],
                "replicate": row.get("replicate", 1),
                "score": None,
                "error": f"{type(exc).__name__}: {exc}",
            }
            print(f"  ERROR {exc}")
        out_rows.append(rec)
        key = (row["model_key"], row["variant_id"], row.get("replicate", 1))
        diffs = disagree(grok.get(key), rec.get("score") or {})
        if diffs and rec.get("score"):
            n_diff += 1
            g = grok.get(key) or {}
            b = rec["score"]
            disagree_lines.append(
                f"## {row['model_key']} `{row['variant_id']}` r{row.get('replicate', 1)}"
            )
            disagree_lines.append("")
            disagree_lines.append(f"fields: {', '.join(diffs)}")
            disagree_lines.append("")
            for field in diffs:
                if field in FAIL_FIELDS:
                    disagree_lines.append(
                        f"- {field}: grok={g.get('failures', {}).get(field)} "
                        f"buddy={b.get(field)}"
                    )
                else:
                    disagree_lines.append(f"- {field}: grok={g.get(field)} buddy={b.get(field)}")
            disagree_lines.append("")
            disagree_lines.append("your call:")
            disagree_lines.append("")

    stem = source.stem
    buddy_path = source.with_name(f"{stem}_buddy.json")
    disagree_path = source.with_name(f"{stem}_disagree.md")
    if args.append and buddy_path.exists():
        prev = json.loads(buddy_path.read_text(encoding="utf-8"))
        merged = {
            (r["model_key"], r["variant_id"], r.get("replicate", 1)): r
            for r in prev.get("rows", [])
        }
        for rec in out_rows:
            merged[(rec["model_key"], rec["variant_id"], rec.get("replicate", 1))] = rec
        out_rows = list(merged.values())
        out_rows.sort(key=lambda r: (r["model_key"], r["variant_id"], r.get("replicate", 1)))
        n_diff = sum(
            1
            for rec in out_rows
            if rec.get("score")
            and disagree(
                grok.get((rec["model_key"], rec["variant_id"], rec.get("replicate", 1))),
                rec["score"],
            )
        )
    payload = {
        "source": str(source),
        "packet_version": packet.get("packet_version"),
        "n": len(out_rows),
        "n_disagree": n_diff,
        "rows": out_rows,
    }
    buddy_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if n_diff == 0:
        disagree_lines.append("No disagreements on compared fields (or no Grok scores to diff).")
    disagree_path.write_text("\n".join(disagree_lines), encoding="utf-8")
    print(f"wrote {buddy_path.name}  {disagree_path.name}  disagree={n_diff}/{len(out_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
