"""Fixture/routing integrity only; these tests do not certify writing quality."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "evals/comparison_layer_cases.json").read_text(encoding="utf-8"))["cases"]
GUIDES = ROOT / "skills/academic-writing-skills/references"


def test_fixed_case_inventory_and_unique_ids():
    assert len(CASES) == 10
    assert len({case["id"] for case in CASES}) == len(CASES)


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_case_has_source_facts_request_and_prespecified_editorial_criteria(case):
    assert case["source"].strip()
    assert case["request"].strip()
    assert case["facts"] and all(fact.strip() for fact in case["facts"])
    assert case["criteria"] and all(criterion.strip() for criterion in case["criteria"])
    if "selection" in case:
        assert case["source"].count(case["selection"]) == 1


def test_controls_cover_failure_and_no_change_not_only_positive_rewrites():
    assert {case["kind"] for case in CASES} >= {
        "layer_contribution", "smooth_label_only", "inventory_with_omnibus_ending",
        "interrupted_evidence_meaning", "false_analysis_gate", "false_instrument_change",
        "functioning_no_label", "cross_domain", "scoped_advisor_edit", "missing_item_meaning",
    }


def test_case_guide_is_reachable_from_results_and_execution():
    cases = (GUIDES / "evidence-context-cases.md").read_text(encoding="utf-8")
    results = (GUIDES / "results-and-explanation.md").read_text(encoding="utf-8")
    execution = (GUIDES / "execution-and-acceptance.md").read_text(encoding="utf-8")
    assert "## 11. Comparison contribution is not a sequence label" in cases
    assert "evals/comparison_layer_cases.json" in cases
    assert "evidence-context-cases.md#11-comparison-contribution-is-not-a-sequence-label" in results
    assert "evidence-context case 11" in execution


def test_scoped_control_has_two_protected_neighbors():
    case = next(case for case in CASES if case["kind"] == "scoped_advisor_edit")
    prefix, suffix = case["source"].split(case["selection"])
    assert prefix.strip() and suffix.strip()


def test_corpus_does_not_ship_private_application_packet():
    # Private application inputs and proposed text remain outside the repository.
    assert not (ROOT / "evals/comparison-inputs-private.json").exists()
    assert all(not case["id"].startswith("PP") for case in CASES)
