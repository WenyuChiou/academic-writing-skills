"""Registration, routing and literal preservation controls; not semantic scoring."""
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "evals/comment_scope_cases.json").read_text(encoding="utf-8"))["cases"]


def test_hypothetical_scope_cases_have_unique_ids_and_all_required_controls():
    assert len(CASES) == 16
    assert {c["id"] for c in CASES} == {f"SC{i:02}" for i in range(1, 17)}
    kinds = {c["anchor_kind"] for c in CASES}
    assert kinds == {"range", "stale", "missing", "deleted_only", "overlap", "reply", "multiple"}
    actions = {c["expected_action"] for c in CASES}
    assert {"retain", "explicit_expansion", "dependency_expansion", "locked_dependency",
            "proposal_only", "surface_only", "uncertain_target", "cross_paragraph"} <= actions


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_case_binds_source_request_selection_facts_and_fixed_criteria(case):
    assert case["source_text"].strip() and case["request"].strip() and case["comment"].strip()
    assert len(case["criteria"]) >= 2 and len(case["facts"]) >= 2
    if case["selected_text"] is not None:
        assert case["source_text"].count(case["selected_text"]) == 1


def test_scope_routes_and_unregistered_reader_are_available():
    core = ROOT / "skills/academic-writing-skills"
    assert "comment-scoped-revision.md" in (core / "SKILL.md").read_text(encoding="utf-8")
    for name in ("execution-and-acceptance", "prose-and-citation-editing", "reviewer-response-workflow"):
        assert "comment-scoped-revision.md" in (core / f"references/{name}.md").read_text(encoding="utf-8")
    assert (core / "scripts/inspect_comment_targets.py").is_file()
    adapter = json.loads((ROOT / "adapter.json").read_text(encoding="utf-8"))
    assert set(adapter["operations"]) == {"state", "consistency", "prose", "candidate", "docx", "regression"}


def test_counterfactual_local_case_can_detect_copying_the_teaching_example():
    case = CASES[0]
    guide = (ROOT / "skills/academic-writing-skills/references/comment-scoped-revision.md").read_text(encoding="utf-8")
    assert "91.2" in case["source_text"] and "84.6" not in case["source_text"]
    assert "84.6" in guide and "91.2" not in guide


def test_literal_boundary_control_rejects_an_unrequested_smooth_rewrite():
    case = CASES[0]
    prefix, suffix = case["source_text"].split(case["selected_text"])
    local = prefix + "A reported greater willingness: 91.2 versus 82.5 for B, a descriptive difference of 8.7 points." + suffix
    overedit = local.replace("Figure 8 compares the two groups.", "We first examine the groups in Figure 8.")
    assert local.startswith(prefix) and local.endswith(suffix)
    assert not (overedit.startswith(prefix) and overedit.endswith(suffix))
    # This control checks exact surroundings, not the scientific quality of either sentence.
