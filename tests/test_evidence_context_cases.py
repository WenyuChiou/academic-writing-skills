"""Fixture integrity and real coverage invalidation, not semantic grading.

The independent behavior exercise scores prose against these contextual
principles separately. These tests must never claim to detect editorial errors.
"""

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "evals/evidence_context_cases.json"
CORPUS = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
CASES = CORPUS["cases"]
SPEC = importlib.util.spec_from_file_location(
    "evidence_case_handoff",
    ROOT / "skills/academic-writing-skills/scripts/audit_handoff.py",
)
handoff = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(handoff)


def coverage_record(tmp_path, case):
    record = {
        "schema_version": 1, "scope": "paragraph", "change": "substantive",
        "features": dict.fromkeys(
            ["displays", "formatted_file", "venue_formatting", "metadata_changes"], False
        ),
        "artifacts": [], "checks": {},
    }
    for name, role, text in [
        ("candidate.txt", "candidate", case["acceptable_revision"]),
        ("context.json", "context", json.dumps(case["source_facts"])),
        ("assessment.txt", "evidence", case["judgment"]),
    ]:
        path = tmp_path / name
        path.write_text(text, encoding="utf-8")
        record["artifacts"].append({
            "id": name, "path": name, "role": role,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    for name in handoff.required_checks(record):
        record["checks"][name] = {
            "status": "checked", "outcome": "resolved",
            "artifact_ids": ["candidate.txt", "context.json", "assessment.txt"],
            "locator": case["id"],
            "finding": "Illustrative coverage record, not an independently verified editorial verdict.",
        }
    return record


def test_corpus_has_context_controls_and_no_claim_of_verbatim_research_data():
    assert CORPUS["schema_version"] == 1
    assert len({case["id"] for case in CASES}) == len(CASES) == 9
    assert {case["category"] for case in CASES} == set(range(1, 10))
    assert "not verbatim" in CORPUS["provenance"]
    for case in CASES:
        assert len(case["source_facts"]) >= 2
        assert len(case["must_preserve"]) >= 2
        assert all(isinstance(v, str) and v.strip() for v in case["source_facts"])
        assert all(case[field].strip() for field in
                   ["task", "original", "acceptable_revision", "unsafe_revision",
                    "retain_control", "judgment"])
        assert len({case[k] for k in
                    ["original", "acceptable_revision", "unsafe_revision",
                     "retain_control"]}) == 4


def test_registered_context_evals_stay_aligned_with_current_source_facts():
    entries = json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))["evals"]
    registered = {entry["id"]: entry for entry in entries}
    for case in CASES:
        entry = registered["context_evidence_" + case["id"].lower()]
        for fact in case["source_facts"]:
            assert fact in entry["prompt"]
        assert case["original"] in entry["prompt"]
        assert case["unsafe_revision"] in entry["prompt"]
        assert case["retain_control"] in entry["prompt"]
        assert case["judgment"] in entry["expected_output"]
        assert case["acceptable_revision"] in entry["expected_output"]
        assert entry["acceptance_criteria"] == case["must_preserve"]
        assert all((ROOT / path).is_file() for path in entry["files"])


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_context_and_candidate_can_be_bound_without_claiming_semantic_certification(tmp_path, case):
    record = coverage_record(tmp_path, case)
    result = handoff.audit_record(record, tmp_path)
    assert result["status"] == "COVERAGE_COMPLETE"
    assert result["editorial_quality_certified"] is False


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_changed_source_context_invalidates_each_case_even_if_prose_is_unchanged(tmp_path, case):
    record = coverage_record(tmp_path, case)
    (tmp_path / "context.json").write_text("Source facts changed after review", encoding="utf-8")
    result = handoff.audit_record(record, tmp_path)
    assert result["status"] == "INVALID"
    assert any("SHA256 mismatch" in finding for finding in result["findings"])


@pytest.mark.parametrize("status", ["not_run", "unavailable"])
def test_missing_claim_support_is_not_cleared_by_an_existing_reply_or_doi(tmp_path, status):
    record = coverage_record(tmp_path, CASES[-1])
    record["checks"]["meaning_and_evidence"] = {
        "status": status,
        "reason": "Reply/DOI identity exists, but the supporting source has not been inspected.",
    }
    assert handoff.audit_record(record, tmp_path)["status"] == "INCOMPLETE"


def test_one_open_subquestion_prevents_whole_comment_completion(tmp_path):
    record = coverage_record(tmp_path, CASES[-1])
    record["checks"]["meaning_and_evidence"].update(
        outcome="open",
        finding="Explanation revised; the requested analysis is still planned.",
    )
    assert handoff.audit_record(record, tmp_path)["status"] == "INCOMPLETE"


def test_a_plausible_unsafe_rewrite_does_not_become_automatically_semantic_checked(tmp_path):
    case = dict(CASES[2], acceptable_revision=CASES[2]["unsafe_revision"])
    # The coverage checker can validate a dishonest record structurally.
    # This adversarial control documents its boundary rather than hiding it.
    result = handoff.audit_record(coverage_record(tmp_path, case), tmp_path)
    assert result["status"] == "COVERAGE_COMPLETE"
    assert result["editorial_quality_certified"] is False
