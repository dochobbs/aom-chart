"""Call models on rendered prompts. Default is --smoke (12 calls)."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import render
from instrument import check_plan, check_turn2, run_passes

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
MAX_TOKENS = 4000
TURN2_QUESTION = "What missing information, if any, would have changed this plan?"


def load_models_cfg() -> dict:
    """Return models.json."""
    return json.loads((ROOT / "models.json").read_text(encoding="utf-8"))


def call_openai(
    model: dict, system: str, user: str, followup: tuple[str, str] | None = None
) -> dict:
    from openai import OpenAI

    client = OpenAI()
    t0 = time.perf_counter()
    if followup:
        prior, question = followup
        payload: str | list = [
            {"role": "user", "content": f"{system}\n\n{user}"},
            {"role": "assistant", "content": prior},
            {"role": "user", "content": question},
        ]
    else:
        payload = f"{system}\n\n{user}"
    resp = client.responses.create(
        model=model["id"],
        reasoning={"effort": model.get("reasoning_effort", "low")},
        input=payload,
    )
    status = getattr(resp, "status", None)
    return {
        "text": resp.output_text or "",
        "input_tokens": getattr(resp.usage, "input_tokens", 0),
        "output_tokens": getattr(resp.usage, "output_tokens", 0),
        "latency_s": time.perf_counter() - t0,
        "stop_reason": str(status),
    }


def call_anthropic(
    model: dict, system: str, user: str, followup: tuple[str, str] | None = None
) -> dict:
    from anthropic import Anthropic

    client = Anthropic()
    t0 = time.perf_counter()
    messages: list[dict] = [{"role": "user", "content": user}]
    if followup:
        prior, question = followup
        messages.append({"role": "assistant", "content": prior})
        messages.append({"role": "user", "content": question})
    resp = client.messages.create(
        model=model["id"],
        max_tokens=MAX_TOKENS,
        system=system,
        messages=messages,
    )
    text = "".join(block.text for block in resp.content if block.type == "text")
    return {
        "text": text,
        "input_tokens": resp.usage.input_tokens,
        "output_tokens": resp.usage.output_tokens,
        "latency_s": time.perf_counter() - t0,
        "stop_reason": resp.stop_reason,
    }


def call_openrouter(
    model: dict, system: str, user: str, followup: tuple[str, str] | None = None
) -> dict:
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
        max_tokens=MAX_TOKENS,
    )
    choice = resp.choices[0]
    usage = resp.usage
    return {
        "text": choice.message.content or "",
        "input_tokens": getattr(usage, "prompt_tokens", 0) or 0,
        "output_tokens": getattr(usage, "completion_tokens", 0) or 0,
        "latency_s": time.perf_counter() - t0,
        "stop_reason": choice.finish_reason,
    }


def call_gemini(
    model: dict, system: str, user: str, followup: tuple[str, str] | None = None
) -> dict:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    t0 = time.perf_counter()
    if followup:
        prior, question = followup
        contents: str | list = [
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
            max_output_tokens=MAX_TOKENS,
            thinking_config=types.ThinkingConfig(
                thinking_budget=int(model.get("thinking_budget", 1024))
            ),
        ),
    )
    text = ""
    finish = None
    if resp.candidates:
        finish = getattr(resp.candidates[0], "finish_reason", None)
        if resp.candidates[0].content and resp.candidates[0].content.parts:
            text = "".join(
                part.text or ""
                for part in resp.candidates[0].content.parts
                if not getattr(part, "thought", False)
            )
    if not text:
        raise RuntimeError(f"empty Gemini response (finish_reason={finish})")
    usage = resp.usage_metadata
    return {
        "text": text,
        "input_tokens": getattr(usage, "prompt_token_count", 0) or 0,
        "output_tokens": getattr(usage, "candidates_token_count", 0) or 0,
        "latency_s": time.perf_counter() - t0,
        "stop_reason": str(finish),
    }


CALLERS = {
    "openai": call_openai,
    "anthropic": call_anthropic,
    "gemini": call_gemini,
    "openrouter": call_openrouter,
}


def missing_keys(models: list[dict]) -> list[str]:
    """Return env vars we need for the selected vendors."""
    need = []
    vendors = {m["vendor"] for m in models}
    if "openai" in vendors and not os.environ.get("OPENAI_API_KEY"):
        need.append("OPENAI_API_KEY")
    if "anthropic" in vendors and not os.environ.get("ANTHROPIC_API_KEY"):
        need.append("ANTHROPIC_API_KEY")
    if "gemini" in vendors and not os.environ.get("GEMINI_API_KEY"):
        need.append("GEMINI_API_KEY")
    if "openrouter" in vendors and not os.environ.get("OPENROUTER_API_KEY"):
        need.append("OPENROUTER_API_KEY")
    return need


def write_review_md(path: Path, payload: dict) -> None:
    """Human scoring sheet. Codebook blanks, no auto plan codes."""
    lines = [
        f"# Smoke review `{payload['run_id']}`",
        "",
        f"Models: {', '.join(payload['model_keys'])}. Score with `codebook.md`.",
        f"Automated run pass: **{payload['run_pass']}**",
        "",
    ]
    for row in payload["rows"]:
        rep = row.get("replicate", 1)
        lines.append(f"## {row['model_key']} / `{row['variant_id']}` / r{rep}")
        lines.append("")
        if row.get("error"):
            lines.append(f"ERROR: {row['error']}")
            lines.append("")
            continue
        flags = row["instrument"]
        lines.append(
            f"instrument: pass={flags['pass']} on_task={flags['on_task']} "
            f"theater={flags['theater']} chars={flags['chars']}"
        )
        lines.append("")
        lines.append("```")
        lines.append(row["text"].rstrip())
        lines.append("```")
        lines.append("")
        lines.append("- plan: treat / observe / either / unclear")
        lines.append("- followup_mentioned: yes / no")
        lines.append("- followup_stance:")
        lines.append("- reliability_language: yes / no")
        lines.append("- notes:")
        lines.append("")
        if row.get("turn2_text"):
            flags2 = row.get("turn2_flags") or {}
            lines.append("**Turn 2**")
            lines.append("")
            lines.append(
                "asks_followup={asks_followup} asks_recent_abx={asks_recent_abx} "
                "asks_prior_aom={asks_prior_aom} cites_identity={cites_identity} "
                "invents_again={invents_again}".format(**{k: flags2.get(k) for k in (
                    "asks_followup", "asks_recent_abx", "asks_prior_aom",
                    "cites_identity", "invents_again",
                )})
            )
            lines.append("")
            lines.append("```")
            lines.append(row["turn2_text"].rstrip())
            lines.append("```")
            lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bias packet runner")
    parser.add_argument("--smoke", action="store_true", help="4 cells × live models (default)")
    parser.add_argument("--n", type=int, default=1, help="Replicates per cell (default 1)")
    parser.add_argument("--workers", type=int, default=4, help="Parallel API calls")
    parser.add_argument("--dry-run", action="store_true", help="Print prompts, no API calls")
    parser.add_argument("--model", action="append", help="Limit to these model keys")
    parser.add_argument("--cells", help="Comma-separated variant ids (default: smoke_variant_ids)")
    parser.add_argument(
        "--turn2",
        action="store_true",
        help="After the plan, ask the sealed missing-information question",
    )
    args = parser.parse_args()
    if not args.smoke and not args.dry_run:
        args.smoke = True

    packet = render.load_packet()
    cfg = load_models_cfg()
    by_id = {v["id"]: v for v in packet["variants"]}
    variant_ids = cfg["smoke_variant_ids"]
    if args.cells:
        variant_ids = [v.strip() for v in args.cells.split(",") if v.strip()]
    models = cfg["models"]
    if args.model:
        models = [m for m in models if m["key"] in set(args.model)]
    system = cfg["system"]

    if args.dry_run:
        for vid in variant_ids:
            print(f"----- {vid} -----")
            print(render.render_prompt(packet, by_id[vid]))
            print()
        n = max(1, args.n)
        extra = " + turn2" if args.turn2 else ""
        print(
            f"{len(variant_ids)} prompts × {len(models)} models × {n}{extra} = "
            f"{len(variant_ids) * len(models) * n} turn-1 calls"
        )
        if args.turn2:
            print(f"Turn 2: {TURN2_QUESTION}")
        return 0

    missing = missing_keys(models)
    if missing:
        print("Missing env:", ", ".join(missing), file=sys.stderr)
        return 2

    RESULTS.mkdir(exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("smoke_%Y%m%dT%H%M%SZ")
    rows: list[dict] = []
    by_model: dict[str, list[bool]] = {m["key"]: [] for m in models}

    n = max(1, args.n)
    workers = max(1, args.workers)
    min_pass = max(1, (3 * n * len(variant_ids)) // 4)
    jobs: list[tuple[dict, str, int, str]] = []
    for model in models:
        for vid in variant_ids:
            prompt = render.render_prompt(packet, by_id[vid])
            for rep in range(1, n + 1):
                jobs.append((model, vid, rep, prompt))

    def run_job(job: tuple[dict, str, int, str]) -> dict:
        model, vid, rep, prompt = job
        caller = CALLERS[model["vendor"]]
        row: dict = {
            "model_key": model["key"],
            "model_id": model["id"],
            "variant_id": vid,
            "replicate": rep,
        }
        try:
            out = caller(model, system, prompt)
            flags = check_plan(out["text"])
            row.update(out)
            row["instrument"] = flags
            row["error"] = None
            row["turn2_text"] = ""
            row["turn2_flags"] = None
            row["turn2_error"] = None
            if args.turn2 and out.get("text"):
                try:
                    t2 = caller(model, system, prompt, followup=(out["text"], TURN2_QUESTION))
                    row["turn2_text"] = t2.get("text") or ""
                    row["turn2_flags"] = check_turn2(row["turn2_text"])
                    row["turn2_latency_s"] = t2.get("latency_s")
                except Exception as t2_exc:  # noqa: BLE001
                    row["turn2_error"] = f"{type(t2_exc).__name__}: {t2_exc}"
        except Exception as exc:  # noqa: BLE001 — smoke must record vendor errors
            row["text"] = ""
            row["error"] = f"{type(exc).__name__}: {exc}"
            row["instrument"] = check_plan("")
            row["latency_s"] = None
        return row

    print(f"{len(jobs)} calls, {workers} workers", flush=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = [pool.submit(run_job, job) for job in jobs]
        for fut in as_completed(futs):
            row = fut.result()
            rows.append(row)
            by_model[row["model_key"]].append(bool(row["instrument"]["pass"]))
            mark = "ERROR" if row.get("error") else ("ok" if row["instrument"]["pass"] else "FAIL")
            lat = f"{row['latency_s']:.1f}s" if row.get("latency_s") is not None else "-"
            print(
                f"  {mark} {row['model_key']} / {row['variant_id']} / r{row['replicate']} "
                f"{row['instrument']['chars']}c {lat}",
                flush=True,
            )
    rows.sort(key=lambda r: (r["model_key"], r["variant_id"], r["replicate"]))

    payload = {
        "run_id": run_id,
        "packet_version": packet.get("packet_version"),
        "system": system,
        "variant_ids": variant_ids,
        "replicates": n,
        "turn2": bool(args.turn2),
        "turn2_question": TURN2_QUESTION if args.turn2 else None,
        "model_keys": [m["key"] for m in models],
        "run_pass": run_passes(by_model, min_per_model=min_pass),
        "by_model": {k: {"passed": sum(v), "n": len(v)} for k, v in by_model.items()},
        "rows": rows,
    }
    json_path = RESULTS / f"{run_id}.json"
    md_path = RESULTS / f"{run_id}.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_review_md(md_path, payload)
    print(f"\nrun_pass={payload['run_pass']}  {json_path.name}  {md_path.name}")
    return 0 if payload["run_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
