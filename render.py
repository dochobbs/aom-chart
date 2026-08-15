"""Render each variant into a full prompt string."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PACKET = ROOT / "variants.json"


def load_packet(path: Path = PACKET) -> dict:
    """Return the bias packet JSON."""
    return json.loads(path.read_text(encoding="utf-8"))


def merge_variant(packet: dict, variant: dict) -> dict:
    """Fill packet defaults for any field the variant does not set."""
    merged = dict(packet["defaults"])
    for key in ("name", "race", "ethnicity", "insurance", "language", "opener"):
        if key in variant:
            merged[key] = variant[key]
    return merged


def render_prompt(packet: dict, variant: dict) -> str:
    """Build the demographics block + opener + frozen body."""
    fields = merge_variant(packet, variant)
    header = (
        f"Name:              {fields['name']}\n"
        f"Age / Sex:         {packet.get('age_months', 18)} months / Male\n"
        f"Race / Ethnicity:  {fields['race']} / {fields['ethnicity']}\n"
        f"Insurance:         {fields['insurance']}\n"
        f"Language:          {fields['language']}"
    )
    return f"{header}\n\n{fields['opener']}\n\n{packet['body']}"


def render_all(packet: dict | None = None) -> list[tuple[str, str]]:
    """Return (variant_id, prompt) for every cell."""
    packet = packet or load_packet()
    return [(v["id"], render_prompt(packet, v)) for v in packet["variants"]]


def main() -> None:
    """Write prompts.md for review."""
    lines = ["# Rendered prompts\n", "Generated from `variants.json`. Review before any model run.\n"]
    for variant_id, prompt in render_all():
        lines.append(f"## `{variant_id}`\n")
        lines.append("```")
        lines.append(prompt)
        lines.append("```\n")
    (ROOT / "prompts.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
