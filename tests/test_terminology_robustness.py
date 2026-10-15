"""Desired terminology contract: existing controls plus proposed safeguards.

Failures against the old CLI establish missing safeguards, not failed human
comprehension. All input files are synthetic and isolated by pytest tmp_path.
"""
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys

SCRIPTS = Path(os.environ.get("TERM_SCRIPTS", str(Path(__file__).resolve().parents[1] / "skills" / "academic-writing-skills" / "scripts"))).resolve()
sys.path.insert(0, str(SCRIPTS))
consistency = importlib.import_module("audit_text_consistency")
candidate = importlib.import_module("audit_candidate_text")


def profile():
    return {
        "project": {"id": "survey-alpha"},
        "terminology_revision": "r1",
        "semantic_locks": [],
        "facts": [],
        "style_profile": {"protected_terms": ["willingness to buy flood insurance"]},
        "terminology": [{
            "id": "stated-intention",
            "preferred": "willingness to buy flood insurance",
            "prohibited": ["insurance readiness"],
            "scope_roles": ["main_manuscript"],
        }],
        "artifacts": [],
    }


def codes(findings):
    return {finding["code"] for finding in findings}


def run_cli(tmp_path, state, text="Households reported willingness to buy flood insurance."):
    state_path = tmp_path / "state.json"
    text_path = tmp_path / "candidate.txt"
    state_path.write_text(json.dumps(state), encoding="utf-8")
    text_path.write_text(text, encoding="utf-8")
    before = (state_path.read_bytes(), text_path.read_bytes())
    run = subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPTS / "audit_candidate_text.py"),
         str(state_path), str(text_path), "--label", "main", "--json"],
        text=True, capture_output=True, encoding="utf-8", timeout=20, check=False,
    )
    assert run.returncode in (0, 1), (run.returncode, run.stdout, run.stderr)
    result = json.loads(run.stdout)
    assert before == (state_path.read_bytes(), text_path.read_bytes())
    return result, before


def test_registered_variant_is_detected():
    assert "TERM001" in codes(consistency.audit_fragment("Insurance readiness increased.", "main", profile()))


def test_preferred_term_is_not_flagged():
    assert "TERM001" not in codes(consistency.audit_fragment("Willingness to buy flood insurance increased.", "main", profile()))


def test_distinct_observed_behavior_is_not_replaced():
    assert "TERM001" not in codes(consistency.audit_fragment("Insurance enrollment increased.", "main", profile()))


def test_registered_variant_does_not_match_inside_longer_token():
    assert not consistency.contains_variant("The insurance readinesses label is quoted.", "insurance readiness")


def test_separate_project_does_not_inherit_other_project_rules():
    state = profile()
    state["project"]["id"] = "ecology-beta"
    state["terminology"] = [{"id": "readiness", "preferred": "insurance readiness"}]
    assert "TERM001" not in codes(consistency.audit_fragment("Insurance readiness is the registered construct.", "main", state))


def test_fragment_matches_full_artifact_role_selection(tmp_path):
    state = profile()
    path = tmp_path / "supplement.txt"
    path.write_text("Insurance readiness is the title of a historical scale.", encoding="utf-8")
    state["artifacts"] = [{"id": "sm", "path": path.name, "role": "supplement", "status": "ACTIVE"}]
    full = "TERM001" in codes(consistency.audit(state, tmp_path))
    fragment = "TERM001" in codes(consistency.audit_fragment(path.read_text(encoding="utf-8"), "sm", state))
    assert fragment == full, {"fragment_flagged": fragment, "full_flagged": full}


def test_fragment_still_flags_in_scope_artifact(tmp_path):
    state = profile()
    state["artifacts"] = [{"id": "main", "role": "main_manuscript", "status": "ACTIVE"}]
    assert "TERM001" in codes(consistency.audit_fragment("Insurance readiness increased.", "main", state))


def test_cli_binds_candidate_to_exact_state_bytes(tmp_path):
    result, (state_bytes, text_bytes) = run_cli(tmp_path, profile())
    assert result["candidate_sha256"] == hashlib.sha256(text_bytes).hexdigest()
    assert result.get("state_sha256") == hashlib.sha256(state_bytes).hexdigest()


def test_registry_revision_invalidates_identical_text_receipt(tmp_path):
    state = profile()
    first, _ = run_cli(tmp_path, state)
    state["terminology_revision"] = "r2"
    second, _ = run_cli(tmp_path, state)
    assert first["candidate_sha256"] == second["candidate_sha256"]
    assert first.get("state_sha256") and first["state_sha256"] != second.get("state_sha256")


def test_empty_registry_is_distinguished_from_complete_terminology_check(tmp_path):
    state = profile()
    state["terminology"] = []
    result, _ = run_cli(tmp_path, state)
    assert result["status"] == "PASS"  # Preserve the configured scan's meaning.
    coverage = result.get("terminology_coverage", {})
    assert coverage.get("registered_entries") == 0
    assert coverage.get("inventory_completeness_certified") is False


def test_fresh_process_reads_persisted_registry(tmp_path):
    result, _ = run_cli(tmp_path, profile(), "Insurance readiness increased.")
    assert result["status"] == "FINDINGS" and "TERM001" in codes(result["findings"])


def test_diagnostic_does_not_modify_quoted_source(tmp_path):
    text = 'The historical title was "Insurance readiness"; it is not our variable name.'
    result, _ = run_cli(tmp_path, profile(), text)
    assert "TERM001" in codes(result["findings"])
    assert "manual_checks_required" in result  # A diagnostic is not an automatic edit.


def test_rule_fingerprints_and_project_identity_are_recorded(tmp_path):
    result, _ = run_cli(tmp_path, profile())
    assert result["project_id"] == "survey-alpha"
    assert len(result["rule_sha256"]) == 7
    for name, digest in result["rule_sha256"].items():
        assert digest == hashlib.sha256((SCRIPTS.parent / name).read_bytes()).hexdigest()


def test_unknown_artifact_scope_is_disclosed_not_silently_skipped(tmp_path):
    result, _ = run_cli(tmp_path, profile(), "Insurance readiness increased.")
    assert "TERM001" in codes(result["findings"])
    assert result["artifact_role"] is None
    assert result["terminology_coverage"]["scope_unresolved"] is True


def test_known_out_of_scope_candidate_reports_zero_applicable_entries(tmp_path):
    state = profile()
    state["artifacts"] = [{"id": "main", "role": "supplement", "status": "ACTIVE"}]
    result, _ = run_cli(tmp_path, state, "Insurance readiness is a historical title.")
    assert "TERM001" not in codes(result["findings"])
    assert result["terminology_coverage"]["applicable_entries"] == 0
    assert result["terminology_coverage"]["scope_unresolved"] is False


def test_proposed_entry_cannot_appear_as_confirmed_registry_profile(tmp_path):
    state = profile()
    state["terminology"][0]["status"] = "PROPOSED"
    result, _ = run_cli(tmp_path, state)
    assert "CAND004" in codes(result["findings"])
    assert result["profile_loaded"] is False


def test_separate_proposal_is_not_enforced_as_confirmed_term(tmp_path):
    state = profile()
    state["terminology_proposals"] = [{
        "concept": "unresolved", "preferred": "adaptation pathway",
        "prohibited": ["insurance enrollment"], "status": "PROPOSED",
    }]
    result, _ = run_cli(tmp_path, state, "Insurance enrollment increased.")
    assert "TERM001" not in codes(result["findings"])


def test_fragment_also_honors_lock_and_fact_scope():
    state = profile()
    state["artifacts"] = [{"id": "sm", "role": "supplement", "status": "ACTIVE"}]
    state["semantic_locks"] = [{"id": "label", "kind": "SEMANTIC", "canonical": "new label", "forbidden_variants": ["old label"], "required_roles": ["main_manuscript"]}]
    state["facts"] = [{"id": "n", "forbidden_strings": ["936"], "scope_roles": ["main_manuscript"]}]
    result = consistency.audit_fragment("A historical old label used 936 observations.", "sm", state)
    assert not ({"LOCK002", "FACT101"} & codes(result))


def test_unknown_scope_notice_also_covers_locks_and_facts_without_terms(tmp_path):
    state = profile()
    state["terminology"] = []
    state["semantic_locks"] = [{"id": "label", "kind": "SEMANTIC", "canonical": "new label", "forbidden_variants": ["old label"], "required_roles": ["main_manuscript"]}]
    state["facts"] = [{"id": "n", "forbidden_strings": ["936"], "scope_roles": ["main_manuscript"]}]
    result, _ = run_cli(tmp_path, state, "A historical old label used 936 observations.")
    assert result["scope_unresolved"] is True
    assert {"LOCK002", "FACT101"} <= codes(result["findings"])
    run = subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPTS / "audit_candidate_text.py"), str(tmp_path / "state.json"), str(tmp_path / "candidate.txt")],
        text=True, capture_output=True, encoding="utf-8", timeout=20, check=False,
    )
    assert run.returncode == 1
    assert "artifact role unresolved" in run.stdout
