"""Input integrity only. Semantic performance requires actual editorial outputs."""
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PACKET = json.loads((ROOT / "evals/interpretation_addition_cases.json").read_text(encoding="utf-8"))
CASES = PACKET["cases"]


def test_cases_are_unique_and_explicitly_fictional():
    assert len(CASES) == 14
    assert len({case["id"] for case in CASES}) == len(CASES)
    assert PACKET["purpose"].startswith("Fictional editorial tasks.")


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_complete_reading_units_and_prespecified_criteria(case):
    for field in ("id", "request", "source"):
        assert isinstance(case[field], str) and case[field].strip()
    for field in ("facts", "criteria"):
        assert isinstance(case[field], list) and case[field]
        assert all(isinstance(value, str) and value.strip() for value in case[field])


def test_control_requests_retain_their_scope_markers():
    controls = {case["id"]: case for case in CASES}
    assert set(controls) == {f"IA{n:02}" for n in range(1, 15)}
    assert "preserve" in controls["IA02"]["request"]
    assert "retain" in controls["IA06"]["request"]
    assert "return only the corrected sentence" in controls["IA14"]["request"]
