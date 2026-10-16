"""Stage coverage is auditable; prose quality and chronology are not certified."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = Path(os.environ.get("HANDOFF_SCRIPT", str(
    ROOT / "skills/academic-writing-skills/scripts/audit_handoff.py"
)))
SPEC = importlib.util.spec_from_file_location("staged_handoff", SCRIPT)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)

LOCAL = {"meaning_and_evidence", "language_scan", "reader_walkthrough",
         "functional_completeness"}
PASSES = {"argument_structure", "evidence_scope", "scholarly_writing",
          "delivery_integrity"}


def evidence(name, ids=("candidate",)):
    # Toy findings test record shape only; their truth is not certified.
    return {"status": "checked", "outcome": "resolved", "artifact_ids": list(ids),
            "locator": "Paragraph 1 / " + name,
            "finding": "Located review observation; remaining scope is explicit."}


@pytest.fixture
def record(tmp_path):
    files = {"candidate": "The interviews were recorded with consent.",
             "state": '{"project":{"id":"delta"},"terminology":[]}',
             "plan": "Function: report recording; preserve consent and tense."}
    artifacts = []
    for name, content in files.items():
        path = tmp_path / (name + ".txt")
        path.write_text(content, encoding="utf-8")
        artifacts.append({"id": name, "path": path.name,
                          "role": "candidate" if name == "candidate" else "context",
                          "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    checks = {name: evidence(name) for name in LOCAL}
    checks["language_scan"]["artifact_ids"].append("state")
    return {"schema_version": 2, "scope": "sentence", "change": "surface",
            "action": "proofread", "checkpoint": "handoff",
            "features": {"displays": False, "formatted_file": False,
                         "venue_formatting": False, "metadata_changes": False},
            "artifacts": artifacts, "checks": checks}


def add_checks(record, names):
    record["checks"].update({name: evidence(name) for name in names})


def test_v2_grammar_has_no_planning_or_chapter_obligation(record, tmp_path):
    result = audit.audit_record(record, tmp_path)
    assert result["status"] == "COVERAGE_COMPLETE"
    assert set(result["required_checks"]) == LOCAL
    assert result["coverage_basis"] == "workflow_v2"
    assert result["editorial_quality_certified"] is False
    assert result["execution_order_certified"] is False


def test_v1_remains_readable_without_claiming_stage_coverage(record, tmp_path):
    record.update(schema_version=1)
    record.pop("action")
    record.pop("checkpoint")
    record["checks"].pop("functional_completeness")
    result = audit.audit_record(record, tmp_path)
    assert result["status"] == "COVERAGE_COMPLETE"
    assert result["coverage_basis"] == "legacy_v1"
    assert result["workflow"] is None


def test_legacy_metadata_cannot_silently_claim_new_workflow(record, tmp_path):
    record["schema_version"] = 1
    assert audit.audit_record(record, tmp_path)["status"] == "INVALID"


@pytest.mark.parametrize("action", ["plan", "draft", "revise"])
def test_substantive_paragraph_requires_a_real_plan_record(record, tmp_path, action):
    record.update(scope="paragraph", change="substantive", action=action)
    add_checks(record, {"progression_and_framing"})
    result = audit.audit_record(record, tmp_path)
    assert result["status"] == "INCOMPLETE"
    assert "writing_plan" in result["required_checks"]
    record["checks"]["writing_plan"] = evidence("writing_plan", ["plan"])
    assert audit.audit_record(record, tmp_path)["status"] == "COVERAGE_COMPLETE"


def test_review_does_not_fabricate_a_pre_draft_plan(record, tmp_path):
    record.update(scope="paragraph", change="substantive", action="review")
    add_checks(record, {"progression_and_framing"})
    result = audit.audit_record(record, tmp_path)
    assert result["status"] == "COVERAGE_COMPLETE"
    assert "writing_plan" not in result["required_checks"]


def test_conceptual_outline_does_not_require_empirical_sections(record, tmp_path):
    record.update(scope="section", change="substantive", action="plan",
                  checkpoint="outline")
    add_checks(record, {"writing_plan", "progression_and_framing"})
    result = audit.audit_record(record, tmp_path)
    assert result["status"] == "COVERAGE_COMPLETE"
    assert not PASSES.intersection(result["required_checks"])
    assert "chapter_closure" not in result["required_checks"]


def test_chapter_closure_requires_blind_spots_terms_and_four_passes(record, tmp_path):
    record.update(scope="section", change="substantive", action="review",
                  checkpoint="chapter_closure")
    add_checks(record, {"progression_and_framing"})
    result = audit.audit_record(record, tmp_path)
    assert result["status"] == "INCOMPLETE"
    expected = LOCAL | PASSES | {"progression_and_framing", "chapter_closure",
                                 "terminology_reconciliation"}
    assert set(result["required_checks"]) == expected
    add_checks(record, expected)
    assert audit.audit_record(record, tmp_path)["status"] == "COVERAGE_COMPLETE"


@pytest.mark.parametrize("missing", sorted(PASSES))
def test_whole_review_cannot_collapse_four_passes_to_one(record, tmp_path, missing):
    record.update(scope="package", change="substantive", action="review",
                  checkpoint="full_review")
    add_checks(record, PASSES | {"progression_and_framing", "terminology_reconciliation"})
    del record["checks"][missing]
    result = audit.audit_record(record, tmp_path)
    assert result["status"] == "INCOMPLETE"
    assert any(missing in item for item in result["findings"])


def test_substantive_section_handoff_still_requires_four_passes(record, tmp_path):
    record.update(scope="section", change="substantive", action="revise")
    add_checks(record, {"writing_plan", "progression_and_framing"})
    result = audit.audit_record(record, tmp_path)
    assert PASSES <= set(result["required_checks"])
    assert result["status"] == "INCOMPLETE"


def test_whole_file_punctuation_is_not_a_scientific_review(record, tmp_path):
    record.update(scope="package")
    add_checks(record, {"progression_and_framing"})
    result = audit.audit_record(record, tmp_path)
    assert result["status"] == "COVERAGE_COMPLETE"
    assert not PASSES.intersection(result["required_checks"])


@pytest.mark.parametrize("mutation", [
    lambda r: r.pop("action"),
    lambda r: r.pop("checkpoint"),
    lambda r: r.update(action=[]),
    lambda r: r.update(checkpoint={}),
    lambda r: r.update(action="anything"),
    lambda r: r.update(checkpoint="anything"),
    lambda r: r.update(checkpoint="full_review"),
    lambda r: r.update(checkpoint="chapter_closure"),
    lambda r: r.update(action="proofread", change="substantive"),
    lambda r: r.update(checkpoint="outline"),
])
def test_invalid_workflow_cannot_pass(record, tmp_path, mutation):
    mutation(record)
    assert audit.audit_record(record, tmp_path)["status"] == "INVALID"


def test_changed_glossary_targets_declared_dependencies_not_all_checks(record, tmp_path):
    (tmp_path / "state.txt").write_text("Author-approved definition changed", encoding="utf-8")
    result = audit.audit_record(record, tmp_path)
    assert result["status"] == "INVALID"
    assert result["stale_artifact_ids"] == ["state"]
    assert result["invalidated_checks"] == ["language_scan"]
    assert "reader_walkthrough" not in result["invalidated_checks"]
    # This reports declared dependency coverage, not semantic completeness.


@pytest.mark.parametrize("status", ["unavailable", "not_run"])
def test_missing_evidence_is_not_a_completed_stage(record, tmp_path, status):
    record.update(action="draft", change="substantive", scope="paragraph")
    add_checks(record, {"progression_and_framing"})
    record["checks"]["writing_plan"] = {"status": status,
                                            "reason": "Source/contract is not available."}
    assert audit.audit_record(record, tmp_path)["status"] == "INCOMPLETE"


def test_boolean_stage_check_does_not_count_as_evidence(record, tmp_path):
    record.update(action="draft")
    record["checks"]["writing_plan"] = True
    assert audit.audit_record(record, tmp_path)["status"] == "INVALID"


def test_v2_cli_is_read_only_and_returns_current_result(record, tmp_path):
    path = tmp_path / "handoff.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    run = subprocess.run([sys.executable, "-X", "utf8", "-B", str(SCRIPT), str(path), "--json"],
                         capture_output=True, text=True, encoding="utf-8", timeout=10)
    assert run.returncode == 0, run.stderr + run.stdout
    assert json.loads(run.stdout)["coverage_basis"] == "workflow_v2"
    assert before == {p.name: p.read_bytes() for p in tmp_path.iterdir()}


def test_shared_template_has_separate_empty_proposals_not_a_new_glossary():
    template = json.loads((ROOT / "skills/academic-writing-skills/assets/manuscript_state_template.json").read_text(encoding="utf-8"))
    assert template["terminology"] == []
    assert template["terminology_proposals"] == []


def test_eight_forward_probes_remain_registered_and_source_grounded():
    data = json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))
    probes = [entry for entry in data["evals"] if entry["id"].startswith("staged_workflow_")]
    assert [entry["id"] for entry in probes] == [f"staged_workflow_{i:02d}" for i in range(1, 9)]
    for entry in probes:
        assert entry["prompt"] and entry["expected_output"] and entry["acceptance_criteria"]
        assert all((ROOT / path).is_file() for path in entry["files"])
