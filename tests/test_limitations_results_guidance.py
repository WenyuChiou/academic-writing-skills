"""Registration guards, not tests of scientific/editorial performance."""

import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CORE = "skills/academic-writing-skills/"


@pytest.mark.parametrize(
    "case_id,reference",
    [
        ("limitation_identify_explain_only_without_self_indictment", "discussion-and-limitations.md"),
        ("limitation_coherent_boundary_no_forced_remedy", "discussion-and-limitations.md"),
        ("limitation_absent_test_not_automatic_failure", "discussion-and-limitations.md"),
        ("limitation_required_evidence_gap_not_concealed", "discussion-and-limitations.md"),
        ("limitations_overview_grouped_categories_impact_only", "discussion-and-limitations.md"),
        ("limitations_future_work_explicit_author_override", "discussion-and-limitations.md"),
        ("results_first_distribution_orientation_before_values", "results-and-explanation.md"),
        ("results_repeated_display_inherits_context", "results-and-explanation.md"),
        ("results_repeated_plot_changed_denominator_reorients", "results-and-explanation.md"),
        ("results_oriented_finding_led_opening_no_change", "results-and-explanation.md"),
    ],
)
def test_behavior_case_has_scope_and_source_route(case_id, reference):
    cases = json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))["evals"]
    matches = [case for case in cases if case["id"] == case_id]
    assert len(matches) == 1
    case = matches[0]
    assert case["files"] == [CORE + "SKILL.md", CORE + "references/" + reference]
    assert all((ROOT / path).is_file() for path in case["files"])
    assert case["prompt"].strip() and case["expected_output"].strip()
    assert len(case["acceptance_criteria"]) >= 3
    assert all(criterion.strip() for criterion in case["acceptance_criteria"])
