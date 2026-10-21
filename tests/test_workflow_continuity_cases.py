"""Guard source-bound cases and delivered guidance, not reader comprehension."""

import hashlib
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CORE = "skills/academic-writing-skills"
CORPUS = json.loads((ROOT / "evals/workflow_continuity_cases.json").read_text(encoding="utf-8"))
CASES = CORPUS["cases"]


def test_continuity_cases_are_hypothetical_and_semantically_reviewed():
    assert CORPUS["schema_version"] == 1
    assert "Invented" in CORPUS["provenance"]
    assert "not private manuscript text" in CORPUS["provenance"]
    assert "do not establish semantic correctness" in CORPUS["evaluation_boundary"]
    assert len(CASES) == 12
    assert {case["id"] for case in CASES} == {f"RC{i:02}" for i in range(1, 13)}


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_continuity_case_binds_scope_facts_and_prespecified_criteria(case):
    assert case["task"] in {"revise", "review", "proofread"}
    assert case["expected_action"] in {"repair", "qualify", "diagnose_only", "retain", "surface_only"}
    assert case["text"].strip()
    for field in ("facts", "criteria"):
        assert len(case[field]) >= 2
        assert all(isinstance(value, str) and value.strip() for value in case[field])


def test_continuity_controls_preserve_clear_prose_and_authority_boundaries():
    actions = {case["id"]: case["expected_action"] for case in CASES}
    assert {key for key, action in actions.items() if action == "retain"} == {"RC08", "RC11", "RC12"}
    assert actions["RC06"] == "qualify"
    assert actions["RC07"] == "diagnose_only"
    assert actions["RC10"] == "surface_only"


def test_workflow_guidance_is_routed_and_matches_public_manifest():
    entry = (ROOT / CORE / "SKILL.md").read_text(encoding="utf-8")
    guide = (ROOT / CORE / "references/prose-and-citation-editing.md").read_text(encoding="utf-8")
    execution = (ROOT / CORE / "references/execution-and-acceptance.md").read_text(encoding="utf-8")
    assert "references/prose-and-citation-editing.md#workflow-handoff-test" in entry
    assert "### Workflow handoff test" in guide
    assert "prose-and-citation-editing.md#workflow-handoff-test" in execution
    manifest = json.loads((ROOT / "adapter.json").read_text(encoding="utf-8"))
    for relative in ("SKILL.md", "references/prose-and-citation-editing.md", "references/execution-and-acceptance.md"):
        path = f"{CORE}/{relative}"
        assert manifest["files"][path] == hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
