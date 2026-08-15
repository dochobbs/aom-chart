"""Offline checks: packet renders, smoke cells stay one-swap."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import render

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def packet() -> dict:
    return render.load_packet(ROOT / "variants.json")


@pytest.fixture(scope="module")
def models_cfg() -> dict:
    return json.loads((ROOT / "models.json").read_text(encoding="utf-8"))


def test_fifteen_variants(packet: dict) -> None:
    assert len(packet["variants"]) == 15


def test_control_uses_defaults(packet: dict) -> None:
    control = next(v for v in packet["variants"] if v["id"] == "control")
    prompt = render.render_prompt(packet, control)
    assert "Insurance:         Not documented" in prompt
    assert "Race / Ethnicity:  Not documented / Not documented" in prompt
    assert "Language:          English" in prompt
    assert prompt.startswith("Name:")
    assert prompt.endswith("What is your plan?")
    assert "daycare" not in prompt.lower()
    assert "40 hours" not in prompt
    assert "needs antibiotics" not in prompt
    assert "cold symptoms for 5 days" in prompt
    assert "24 months" in prompt
    assert "24-month-old" in prompt
    assert "18-month-old" not in prompt
    assert "12.4 kg" in prompt
    assert "11.0 kg" not in prompt
    assert "once overnight" in prompt
    assert "twice overnight" not in prompt
    assert "first ear infection" not in prompt.lower()
    assert "no antibiotics" not in prompt.lower()


def test_insurance_only_changes_insurance(packet: dict) -> None:
    control = render.render_prompt(packet, next(v for v in packet["variants"] if v["id"] == "control"))
    medicaid = render.render_prompt(
        packet, next(v for v in packet["variants"] if v["id"] == "insurance_medicaid")
    )
    assert "Insurance:         Medicaid" in medicaid
    assert "Insurance:         Not documented" in control
    body = packet["body"]
    assert body in control and body in medicaid


def test_teen_mom_only_changes_opener(packet: dict) -> None:
    control = next(v for v in packet["variants"] if v["id"] == "control")
    teen = next(v for v in packet["variants"] if v["id"] == "teen_mom")
    c_fields = render.merge_variant(packet, control)
    t_fields = render.merge_variant(packet, teen)
    assert c_fields["name"] == t_fields["name"]
    assert c_fields["race"] == t_fields["race"]
    assert c_fields["insurance"] == t_fields["insurance"]
    assert "19-year-old mother" in t_fields["opener"]
    assert "19-year-old" not in c_fields["opener"]


def test_race_black_only_changes_race_line(packet: dict) -> None:
    fields = render.merge_variant(
        packet, next(v for v in packet["variants"] if v["id"] == "race_black")
    )
    assert fields["race"] == "Black or African American"
    assert fields["ethnicity"] == "Not Hispanic or Latino"
    assert fields["insurance"] == "Not documented"
    assert fields["name"] == "Not documented"


def test_smoke_cells_exist_and_are_single_swap(packet: dict, models_cfg: dict) -> None:
    by_id = {v["id"]: v for v in packet["variants"]}
    for vid in models_cfg["smoke_variant_ids"]:
        assert vid in by_id, vid
        variant = by_id[vid]
        if vid == "control":
            assert variant["active_cell"] is None
        else:
            assert variant["active_cell"] in {"insurance", "race", "opener", "language", "name"}


def test_no_stacking_in_any_variant(packet: dict) -> None:
    defaults = packet["defaults"]
    for variant in packet["variants"]:
        changed = [
            key
            for key in ("name", "race", "ethnicity", "insurance", "language", "opener")
            if key in variant and variant[key] != defaults[key]
        ]
        if variant["id"] == "control":
            assert changed == []
            continue
        # race_white_hispanic changes race + ethnicity together by design (one construct)
        if variant["id"] == "race_white_hispanic":
            assert set(changed) <= {"race", "ethnicity"}
            continue
        if variant["id"].startswith("race_"):
            assert set(changed) <= {"race", "ethnicity"}
            continue
        assert len(changed) == 1, (variant["id"], changed)
