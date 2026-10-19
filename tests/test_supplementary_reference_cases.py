"""Guard evidence-safe fixture coverage and packaging, not model comprehension."""

import hashlib
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GUIDE = "skills/academic-writing-skills/references/figures-tables-and-supplements.md"
CORPUS = json.loads((ROOT / "evals/supplementary_reference_cases.json").read_text(encoding="utf-8"))
CASES = CORPUS["cases"]


def test_sm_reference_cases_are_hypothetical_and_require_semantic_review():
    assert CORPUS["schema_version"] == 1
    assert "Invented" in CORPUS["provenance"]
    assert "not private manuscript text" in CORPUS["provenance"]
    assert "do not establish semantic correctness" in CORPUS["evaluation_boundary"]
    assert len(CASES) == 10
    assert {case["id"] for case in CASES} == {f"SM{i:02}" for i in range(1, 11)}


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_sm_reference_case_has_evidence_scope_and_fixed_criteria(case):
    assert case["action"] in {"revise", "retain", "qualify", "proofread"}
    assert case["function"].strip() and case["text"].strip()
    for field in ("facts", "criteria"):
        assert len(case[field]) >= 2
        assert all(isinstance(item, str) and item.strip() for item in case[field])


def test_sm_reference_cases_include_no_change_and_missing_evidence_controls():
    by_id = {case["id"]: case for case in CASES}
    assert {case["id"] for case in CASES if case["action"] == "retain"} == {"SM02", "SM08", "SM10"}
    assert by_id["SM03"]["action"] == "qualify"
    assert by_id["SM06"]["action"] == "proofread"


def test_sm_reference_guidance_remains_in_the_routed_public_guide():
    entrypoint = (ROOT / "skills/academic-writing-skills/SKILL.md").read_text(encoding="utf-8")
    assert "](references/figures-tables-and-supplements.md)" in entrypoint
    text = (ROOT / GUIDE).read_text(encoding="utf-8")
    assert "### Purposeful supplementary references" in text
    manifest = json.loads((ROOT / "adapter.json").read_text(encoding="utf-8"))
    assert manifest["files"][GUIDE] == hashlib.sha256((ROOT / GUIDE).read_bytes()).hexdigest()
