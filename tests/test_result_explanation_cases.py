"""Offline fixture/route integrity only; independent reading grades prose separately."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDES = ROOT / "skills/academic-writing-skills/references"


def test_result_explanation_inputs_remain_eight_fictional_requests():
    document = json.loads((ROOT / "evals/result_explanation_cases.json").read_text(encoding="utf-8"))
    assert "Fictional" in document["provenance"]
    assert "not manuscript excerpts" in document["provenance"]
    cases = document["cases"]
    assert len(cases) == 8
    assert {case["id"] for case in cases} == {f"RC{i:02}" for i in range(1, 9)}
    for case in cases:
        assert set(case) == {"id", "task", "source_facts", "passage"}
        assert case["task"].strip() and case["passage"].strip()
        assert len(case["source_facts"]) >= 2
        assert all(isinstance(fact, str) and fact.strip() for fact in case["source_facts"])


def test_scope_controls_and_source_distinctions_survive_fixture_packaging():
    cases = {
        case["id"]: case
        for case in json.loads((ROOT / "evals/result_explanation_cases.json").read_text(encoding="utf-8"))["cases"]
    }
    # These are input-integrity checks, not a semantic oracle for generated prose.
    assert "Keep clear wording unchanged" in cases["RC03"]["task"]
    assert "conceptual" in cases["RC07"]["task"]
    assert "Correct only the grammar" in cases["RC08"]["task"]
    assert "4°C" in cases["RC08"]["passage"]
    assert any("not before/after" in fact for fact in cases["RC06"]["source_facts"])
    assert any("No decomposition" in fact for fact in cases["RC05"]["source_facts"])


def test_result_explanation_check_is_reachable_from_existing_reader_routes():
    result = (GUIDES / "results-and-explanation.md").read_text(encoding="utf-8")
    target = "results-and-explanation.md#resultexplanation-continuity"
    assert "### Result–explanation continuity" in result
    for name in ("execution-and-acceptance.md", "independent-reader-review.md"):
        assert target in (GUIDES / name).read_text(encoding="utf-8")
    entry = (ROOT / "skills/academic-writing-skills/SKILL.md").read_text(encoding="utf-8")
    assert "references/results-and-explanation.md" in entry
    assert "references/independent-reader-review.md" in entry
