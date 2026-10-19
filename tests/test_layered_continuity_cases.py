"""Fixture/routing integrity only; semantic judgments need independent reading."""

import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CORPUS = json.loads((ROOT / "evals/layered_continuity_cases.json").read_text(encoding="utf-8"))
CASES = CORPUS["cases"]
REFS = ROOT / "skills/academic-writing-skills/references"


def test_layered_cases_have_source_facts_reader_functions_and_fixed_criteria():
    assert CORPUS["schema_version"] == 1
    assert "not verbatim" in CORPUS["provenance"]
    assert "do not certify" in CORPUS["evaluation_boundary"]
    assert {case["id"] for case in CASES} == {f"LC{i:02}" for i in range(1, 17)}
    assert len(CASES) == 16
    for case in CASES:
        assert case["action"] in {"revise", "review", "proofread"}
        assert case["function"].strip() and case["text"].strip()
        assert len(case["facts"]) == 3 and len(case["criteria"]) == 4
        assert all(isinstance(s, str) and s.strip() for s in case["facts"] + case["criteria"])


@pytest.mark.parametrize("case_id", ["LC03", "LC04", "LC05", "LC06"])
def test_non_results_bridges_are_not_replaced_by_results_only_coverage(case_id):
    case = next(c for c in CASES if c["id"] == case_id)
    assert case["action"] == "revise"
    assert any(word in case["function"] for word in ["Literature", "Background", "Discussion", "Limitation"])


def test_controls_include_retention_negative_findings_and_local_scope():
    controls = {c["id"]: c for c in CASES if c["action"] != "revise"}
    assert set(controls) == {"LC11", "LC12", "LC13", "LC14"}
    assert "equivalence" in controls["LC12"]["text"]
    assert "not their relative influence" in controls["LC13"]["text"]
    assert "provide" in controls["LC14"]["text"]


def test_new_guidance_uses_existing_routes_without_new_certification_schema():
    results = (REFS / "results-and-explanation.md").read_text(encoding="utf-8")
    prose = (REFS / "prose-and-citation-editing.md").read_text(encoding="utf-8")
    acceptance = (REFS / "execution-and-acceptance.md").read_text(encoding="utf-8")
    cases = (REFS / "evidence-context-cases.md").read_text(encoding="utf-8")
    assert "coherent result units" in results and "after every number" in results
    assert "shared scale" in results and "whole-model equality" in results
    assert "Apply the same relation test outside Results" in prose
    assert "reader's load" in prose
    assert "where each coherent evidence" in acceptance
    assert "Layered explanation without extra prose rituals" in cases
    assert "evals/layered_continuity_cases.json" in cases
