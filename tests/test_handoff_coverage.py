"""First-handoff evidence coverage, not automated editorial judgment."""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/academic-writing-skills/scripts/audit_handoff.py"
SPEC = importlib.util.spec_from_file_location("audit_handoff", SCRIPT)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def artifact(tmp_path, name, role, content):
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return {"id": name, "path": name, "role": role,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


@pytest.fixture
def record(tmp_path):
    data = {
        "schema_version": 1, "scope": "section", "change": "substantive",
        "features": {"displays": True, "formatted_file": True,
                     "venue_formatting": True, "metadata_changes": True},
        "artifacts": [artifact(tmp_path, "candidate.txt", "candidate", "Exact revised section"),
                      artifact(tmp_path, "review.txt", "evidence", "Located editorial findings"),
                      artifact(tmp_path, "render.txt", "render", "Final-file render evidence")],
        "checks": {},
    }
    # The fixture records coverage; it does not assert these toy notes prove quality.
    for name in audit.required_checks(data):
        data["checks"][name] = {
            "status": "checked", "outcome": "resolved", "artifact_ids": ["review.txt"],
            "locator": "Review entry: " + name,
            "finding": "Scope-specific review finding with its remaining limits.",
        }
    data["checks"]["final_layout"]["artifact_ids"].append("render.txt")
    data["checks"]["venue_basis"].update(basis="project_preference", source="Author instruction: preserve the accepted caption spacing.")
    data["checks"]["editor_identity"].update(expected_author="Author", new_edit_authors=["Author"])
    return data


def test_complete_coverage_never_claims_editorial_pass(record, tmp_path):
    result = audit.audit_record(record, tmp_path)
    assert result["status"] == "COVERAGE_COMPLETE"
    assert result["editorial_quality_certified"] is False
    assert not result["findings"]


@pytest.mark.parametrize("name", ["progression_and_framing", "caption_allocation", "final_layout", "editor_identity", "venue_basis"])
def test_grammar_scan_cannot_replace_missing_handoff_checks(record, tmp_path, name):
    del record["checks"][name]
    result = audit.audit_record(record, tmp_path)
    assert result["status"] == "INCOMPLETE"
    assert any(name in finding for finding in result["findings"])


@pytest.mark.parametrize("status", ["not_run", "unavailable"])
def test_pending_checks_allow_provisional_work_but_not_complete_coverage(record, tmp_path, status):
    record["checks"]["venue_basis"] = {"status": status, "reason": "Official instructions could not be inspected."}
    result = audit.audit_record(record, tmp_path)
    assert result["status"] == "INCOMPLETE"
    assert any(status in finding for finding in result["findings"])


def test_required_check_cannot_be_waived_with_not_applicable(record, tmp_path):
    record["checks"]["caption_allocation"] = {"status": "not_applicable", "reason": "Prose scan was clean."}
    assert audit.audit_record(record, tmp_path)["status"] == "INVALID"


@pytest.mark.parametrize("name", ["candidate.txt", "review.txt", "render.txt"])
def test_changed_candidate_context_or_evidence_invalidates_coverage(record, tmp_path, name):
    (tmp_path / name).write_text("Changed after review", encoding="utf-8")
    result = audit.audit_record(record, tmp_path)
    assert result["status"] == "INVALID"
    assert any("SHA256 mismatch" in finding for finding in result["findings"])


def test_checked_is_not_a_boolean_or_empty_tick(record, tmp_path):
    record["checks"]["reader_walkthrough"] = {"status": "checked"}
    assert audit.audit_record(record, tmp_path)["status"] == "INVALID"


def test_xml_only_is_not_final_render_coverage(record, tmp_path):
    record["checks"]["final_layout"]["artifact_ids"] = ["review.txt"]
    result = audit.audit_record(record, tmp_path)
    assert result["status"] == "INVALID"
    assert any("render" in finding for finding in result["findings"])


@pytest.fixture
def package(record, tmp_path):
    record.update(schema_version=2, scope="package", action="review", checkpoint="full_review")
    main = artifact(tmp_path, "body.docx", "candidate", "Main manuscript bytes")
    sm = artifact(tmp_path, "supplement.DOCX", "candidate", "Supplement bytes")
    renders = [
        dict(artifact(tmp_path, f"{source['id']}.png", "render", f"Rendered {source['id']}"),
             source_id=source["id"], source_sha256=source["sha256"])
        for source in (main, sm)
    ]
    record["artifacts"] = [main, sm, *record["artifacts"][1:2], *renders]
    for check in audit.required_checks(record):
        record["checks"].setdefault(check, {
            "status": "checked", "outcome": "resolved", "artifact_ids": ["review.txt"],
            "locator": check, "finding": "Synthetic coverage evidence",
        })
    record["checks"]["final_layout"]["artifact_ids"] = [item["id"] for item in [main, sm, *renders]]
    return record


def test_v2_formatted_package_accepts_matching_evidence_per_document(package, tmp_path):
    result = audit.audit_record(package, tmp_path)
    assert result["status"] == "COVERAGE_COMPLETE"
    assert result["editorial_quality_certified"] is False


def test_v2_layout_requires_receipts_for_both_formatted_files(package, tmp_path):
    package["checks"]["final_layout"]["artifact_ids"].remove("supplement.DOCX.png")
    result = audit.audit_record(package, tmp_path)
    assert result["status"] == "INCOMPLETE"
    assert any("supplement.DOCX" in finding for finding in result["findings"])


def test_v2_layout_rejects_old_render_even_after_source_hash_is_refreshed(package, tmp_path):
    main = package["artifacts"][0]
    path = tmp_path / main["path"]
    path.write_text("Resaved manuscript", encoding="utf-8")
    main["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    result = audit.audit_record(package, tmp_path)
    assert result["status"] == "INVALID"
    assert any("source_sha256" in finding and "body.docx" in finding for finding in result["findings"])


def test_v2_unbound_layout_record_remains_readable_but_incomplete(package, tmp_path):
    for entry in package["artifacts"]:
        if entry["role"] == "render":
            entry.pop("source_id")
            entry.pop("source_sha256")
    assert audit.audit_record(package, tmp_path)["status"] == "INCOMPLETE"


def test_v2_render_cannot_be_bound_to_context(package, tmp_path):
    render = package["artifacts"][-1]
    context = artifact(tmp_path, "other.docx", "context", "Historical manuscript")
    package["artifacts"].append(context)
    render.update(source_id=context["id"], source_sha256=context["sha256"])
    assert audit.audit_record(package, tmp_path)["status"] == "INVALID"


def test_paginated_candidates_cannot_disable_format_checks(package, tmp_path):
    package["features"]["formatted_file"] = False
    package["features"]["metadata_changes"] = False
    package["checks"].pop("final_layout")
    package["checks"].pop("editor_identity")
    result = audit.audit_record(package, tmp_path)
    assert result["status"] == "INVALID"
    assert any("formatted_file" in finding for finding in result["findings"])


def test_v1_preserves_legacy_scope_but_plain_output_identifies_its_limits(record, tmp_path):
    record.update(scope="sentence", change="surface", checks={})
    record["features"] = dict.fromkeys(record["features"], False)
    record["artifacts"] = [artifact(tmp_path, "old.docx", "candidate", "Legacy candidate")]
    for name in audit.required_checks(record):
        record["checks"][name] = {"status": "checked", "outcome": "resolved", "artifact_ids": ["old.docx"],
                                  "locator": "Historical receipt", "finding": "Legacy scope only."}
    result = audit.audit_record(record, tmp_path)
    assert result["status"] == "COVERAGE_COMPLETE"
    assert result["coverage_basis"] == "legacy_v1"
    path = tmp_path / "legacy.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    run = subprocess.run([sys.executable, str(SCRIPT), str(path)],
                         text=True, capture_output=True, timeout=20, check=False)
    assert run.returncode == 0
    assert "legacy coverage does not validate workflow stages or per-file render bindings" in run.stdout


def test_small_surface_edit_needs_no_package_or_new_project_state(record, tmp_path):
    record.update(scope="sentence", change="surface", checks={})
    record["features"] = dict.fromkeys(record["features"], False)
    record["artifacts"] = record["artifacts"][:1]
    record["artifacts"].append(artifact(tmp_path, "source.docx", "context", "Prose source"))
    assert audit.required_checks(record) == {"meaning_and_evidence", "language_scan", "reader_walkthrough"}
    for name in audit.required_checks(record):
        record["checks"][name] = {"status": "checked", "outcome": "resolved", "artifact_ids": ["candidate.txt"],
                                  "locator": "Sentence 1", "finding": "Meaning preserved; no broader audit claimed."}
    assert audit.audit_record(record, tmp_path)["status"] == "COVERAGE_COMPLETE"


def test_reviewed_but_unresolved_is_not_complete(record, tmp_path):
    record["checks"]["reader_walkthrough"]["outcome"] = "open"
    assert audit.audit_record(record, tmp_path)["status"] == "INCOMPLETE"


def test_wrong_new_edit_author_is_not_complete(record, tmp_path):
    record["checks"]["editor_identity"]["new_edit_authors"] = ["Assistant"]
    assert audit.audit_record(record, tmp_path)["status"] == "INCOMPLETE"


def test_verified_absence_of_new_authors_does_not_require_fictional_metadata(record, tmp_path):
    record["checks"]["editor_identity"].update(
        new_edit_authors=[],
        absence_reason="Inspected saved artifact: no new revisions, comments, replies, or identity-bearing file properties.",
    )
    assert audit.audit_record(record, tmp_path)["status"] == "COVERAGE_COMPLETE"


def test_empty_author_list_without_inspection_reason_is_invalid(record, tmp_path):
    record["checks"]["editor_identity"]["new_edit_authors"] = []
    assert audit.audit_record(record, tmp_path)["status"] == "INVALID"


def test_unclassified_format_cannot_be_claimed_as_venue_compliance(record, tmp_path):
    record["checks"]["venue_basis"].pop("basis")
    assert audit.audit_record(record, tmp_path)["status"] == "INVALID"


@pytest.mark.parametrize("mutation", [
    lambda data: data.update(schema_version=True),
    lambda data: data.update(scope="anything"),
    lambda data: data.update(scope=[]),
    lambda data: data.update(change={}),
    lambda data: data["features"].update(displays="false"),
    lambda data: data["artifacts"].append(data["artifacts"][0]),
    lambda data: data.update(checks=[]),
    lambda data: data["checks"].update(typo_check={"status": "checked"}),
    lambda data: data["checks"]["language_scan"].update(status=[]),
    lambda data: data["checks"]["language_scan"].update(outcome=[]),
    lambda data: data["checks"]["venue_basis"].update(basis=[]),
])
def test_malformed_record_cannot_report_completion(record, tmp_path, mutation):
    mutation(record)
    assert audit.audit_record(record, tmp_path)["status"] == "INVALID"


def test_cli_reports_incomplete_nonzero_and_does_not_mutate_inputs(record, tmp_path):
    record["checks"].pop("progression_and_framing")
    path = tmp_path / "handoff.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    result = subprocess.run([sys.executable, "-B", str(SCRIPT), str(path), "--json"],
                            capture_output=True, text=True, check=False, timeout=10)
    assert result.returncode == 1
    assert json.loads(result.stdout)["status"] == "INCOMPLETE"
    assert before == {p.name: p.read_bytes() for p in tmp_path.iterdir()}


def test_duplicate_json_keys_fail_closed(tmp_path):
    path = tmp_path / "duplicate.json"
    path.write_text('{"schema_version": 1, "schema_version": 1}', encoding="utf-8")
    result = subprocess.run([sys.executable, "-B", str(SCRIPT), str(path), "--json"],
                            capture_output=True, text=True, check=False, timeout=10)
    assert result.returncode == 2
    assert json.loads(result.stdout)["status"] == "ERROR"
