#!/usr/bin/env python3
"""Audit the exact candidate passage against project terminology and prose rules."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from audit_prose_patterns import audit_text as audit_prose_text
from audit_text_consistency import applies_to_role, artifact_role, audit_fragment


MANUAL_CHECKS = [
    "paragraph contract and adjacent-paragraph flow",
    "claim scope and preservation of locked meaning",
    "functional transitions and cumulative information flow",
    "literature-example ordering from broad context to the closest precedent and gap, or another explicit evidentiary logic",
    "function-preserving concision and sentence rhythm",
    "sentence-opening families and repeated clause shapes, including We first/We then/We next; preserve necessary procedural order without cosmetic synonym or voice rotation",
    "natural scholarly subjects, syntax, and disciplinary accessibility",
    "reader accessibility, including nonessential field shorthand, transition templates, and indirect verbs",
    "claim-to-citation support and reference-list changes",
    "observable stock or AI-like prose features without authorship inference",
    "dash and hyphen style, including grammatical role, established open compounds, density, and suspended compounds",
    "necessary technical repetition versus avoidable restatement",
]


def audit_profile(state: dict) -> list[dict]:
    findings: list[dict] = []
    if not (state.get("style_profile") or state.get("terminology") or state.get("semantic_locks")):
        findings.append({"code": "CAND001", "message": "no project terminology or style profile was loaded"})
    for index, lock in enumerate(state.get("semantic_locks", []), start=1):
        missing = [key for key in ("id", "kind", "canonical") if not str(lock.get(key, "")).strip()]
        if missing:
            findings.append({
                "code": "CAND002",
                "message": f"semantic_locks[{index}] is not auditable; missing {', '.join(missing)}",
            })
    for index, term in enumerate(state.get("terminology", []), start=1):
        if not str(term.get("id", term.get("concept", ""))).strip() or not str(term.get("preferred", "")).strip():
            findings.append({
                "code": "CAND003",
                "message": f"terminology[{index}] requires an id or concept and a preferred term",
            })
        if term.get("status") == "PROPOSED":
            findings.append({
                "code": "CAND004",
                "message": f"terminology[{index}] is proposed, not confirmed; keep it in terminology_proposals",
            })
    return findings


def check_context(state: dict, label: str, state_bytes: bytes) -> dict:
    """Bind scan evidence to its inputs without certifying semantic coverage."""
    role = artifact_role(state, label)
    terms = state.get("terminology", [])
    scoped = [term for term in terms if term.get("scope_roles")]
    scoped_rules = bool(scoped) or any(
        entry.get(key) for collection, key in (("semantic_locks", "required_roles"), ("facts", "scope_roles"))
        for entry in state.get(collection, [])
    )
    rule_paths = [
        "SKILL.md", "references/state-and-authority.md",
        "references/universal-integrity.md", "references/prose-and-citation-editing.md",
        "scripts/audit_candidate_text.py", "scripts/audit_text_consistency.py",
        "scripts/audit_prose_patterns.py",
    ]
    root = Path(__file__).resolve().parents[1]
    fingerprints = {
        name: hashlib.sha256((root / name).read_bytes()).hexdigest()
        for name in rule_paths
    }
    project = state.get("project", {})
    return {
        "state_sha256": hashlib.sha256(state_bytes).hexdigest(),
        "project_id": project.get("id") if isinstance(project, dict) else None,
        "artifact_role": role,
        "scope_unresolved": role is None and scoped_rules,
        "rule_sha256": fingerprints,
        "terminology_coverage": {
            "registered_entries": len(terms),
            "applicable_entries": sum(applies_to_role(term, role, "scope_roles") for term in terms)
            if role is not None else sum(not term.get("scope_roles") for term in terms),
            "scope_unresolved": bool(role is None and scoped),
            "inventory_completeness_certified": False,
            "scan_basis": "registered_patterns_only; contextual review remains required",
        },
    }


def audit_candidate(text: str, artifact: str, state: dict) -> list[dict]:
    findings = audit_profile(state)
    findings.extend(audit_fragment(text, artifact, state))
    findings.extend(audit_prose_text(text, artifact, state))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", help="manuscript_state.json")
    parser.add_argument("candidate", help="UTF-8 text file containing the exact candidate passage")
    parser.add_argument("--label", default="candidate")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    try:
        state_bytes = Path(args.state).expanduser().read_bytes()
        state = json.loads(state_bytes.decode("utf-8"))
        raw = Path(args.candidate).expanduser().read_bytes()
        text = raw.decode("utf-8")
        findings = audit_candidate(text, args.label, state)
        result = {
            "status": "FINDINGS" if findings else "PASS",
            "candidate_sha256": hashlib.sha256(raw).hexdigest(),
            "profile_loaded": not any(item["code"].startswith("CAND00") for item in findings),
            "findings": findings,
            "manual_checks_required": MANUAL_CHECKS,
            **check_context(state, args.label, state_bytes),
        }
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        result = {
            "status": "ERROR", "candidate_sha256": None, "profile_loaded": False,
            "findings": [{"code": "CAND000", "message": str(exc)}],
            "manual_checks_required": MANUAL_CHECKS,
        }

    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"{result['status']}: {len(result['findings'])} finding(s)")
        print(f"candidate_sha256: {result['candidate_sha256']}")
        if "terminology_coverage" in result:
            coverage = result["terminology_coverage"]
            print(f"terminology: {coverage['registered_entries']} registered entries; inventory completeness not certified")
            if result["scope_unresolved"]:
                print("artifact role unresolved: scoped matches are conservative diagnostics")
        for item in result["findings"]:
            print(f"{item['code']}: {item['message']} ({item.get('match', args.label)})")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
