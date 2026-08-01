#!/usr/bin/env python3
"""Validate manuscript project state and compute release blockers."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SEVERITIES = {"S0", "S1", "S2", "S3", "S4"}
ISSUE_STATUSES = {"OPEN", "RESOLVED", "WAIVED"}
EVIDENCE_STATUSES = {"CONFIRMED", "PROBABLE", "UNVERIFIED"}
RELEASE_READY = {"SUBMISSION_READY", "FINAL", "VERIFIED"}


def finding(code: str, severity: str, message: str, blocker: bool = False) -> dict[str, Any]:
    return {"code": code, "severity": severity, "blocker": blocker, "message": message}


def load_state(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("state root must be a JSON object")
    return data


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit(state: dict[str, Any], project_root: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    required = ["project", "artifacts", "authority_sources", "contract", "alignment", "issues", "release"]
    for key in required:
        if key not in state:
            out.append(finding("STATE001", "S4", f"missing top-level field: {key}", True))
    if out:
        return out

    artifacts = state.get("artifacts", [])
    artifact_ids = [item.get("id") for item in artifacts]
    if len(artifact_ids) != len(set(artifact_ids)):
        out.append(finding("STATE002", "S3", "artifact ids are not unique", True))

    active_by_role: dict[str, int] = {}
    for item in artifacts:
        if item.get("status") == "ACTIVE":
            role = item.get("role", "")
            active_by_role[role] = active_by_role.get(role, 0) + 1
        path_text = item.get("path", "")
        if item.get("required_for_release") and not path_text:
            out.append(finding("FILE001", "S3", f"required artifact {item.get('id')} has no path", True))
    for role, count in active_by_role.items():
        if role in {"main_manuscript", "supplement", "title_page", "cover_letter"} and count > 1:
            out.append(finding("VERSION001", "S3", f"multiple ACTIVE artifacts for singular role {role}", True))

    sources = {item.get("id"): item for item in state.get("authority_sources", [])}
    for fact in state.get("facts", []):
        source_id = fact.get("source_id")
        if not source_id or source_id not in sources:
            out.append(finding("FACT001", "S4", f"fact {fact.get('id')} lacks a valid authority source", True))
        elif sources[source_id].get("status") != "VERIFIED":
            out.append(finding("FACT002", "S3", f"fact {fact.get('id')} depends on unverified source {source_id}", True))

    questions = state.get("contract", {}).get("questions", [])
    question_ids = [item.get("id") for item in questions]
    if len(question_ids) != len(set(question_ids)):
        out.append(finding("ALIGN001", "S4", "question ids are not unique", True))
    alignments = {item.get("question_id"): item for item in state.get("alignment", [])}
    for question_id in question_ids:
        row = alignments.get(question_id)
        if not row:
            out.append(finding("ALIGN002", "S4", f"question {question_id} has no alignment row", True))
            continue
        for field in ("method", "evidence", "result", "interpretation", "limitation", "contribution"):
            if not str(row.get(field, "")).strip():
                severity = "S2" if row.get("status") == "PLANNED" else "S3"
                out.append(finding("ALIGN003", severity, f"question {question_id} lacks {field}", severity == "S3"))

    for dimension in state.get("dimensions", []):
        required_pairs = {
            (str(value), str(field))
            for value in dimension.get("values", [])
            for field in dimension.get("required_fields", [])
        }
        coverage = {
            (str(item.get("value")), str(item.get("field"))): item
            for item in dimension.get("coverage", [])
        }
        for pair in sorted(required_pairs):
            row = coverage.get(pair)
            if not row or row.get("status") not in {"COMPLETE", "NOT_APPLICABLE", "WAIVED"}:
                out.append(finding("DIM001", "S3", f"dimension {dimension.get('id')} missing coverage for {pair[0]} × {pair[1]}", True))
            elif row.get("status") in {"NOT_APPLICABLE", "WAIVED"} and not str(row.get("reason", "")).strip():
                out.append(finding("DIM002", "S2", f"dimension {dimension.get('id')} has unexplained {row.get('status')} for {pair[0]} × {pair[1]}"))

    for issue in state.get("issues", []):
        severity = issue.get("severity")
        status = issue.get("status")
        evidence_status = issue.get("evidence_status")
        if severity not in SEVERITIES or status not in ISSUE_STATUSES or evidence_status not in EVIDENCE_STATUSES:
            out.append(finding("ISSUE001", "S3", f"issue {issue.get('id')} has invalid classification", True))
            continue
        if status == "OPEN" and severity in {"S3", "S4"}:
            out.append(finding("ISSUE002", severity, f"open blocker {issue.get('id')}: {issue.get('description', '')}", True))
        if status == "WAIVED" and (
            not issue.get("waiver")
            or not issue.get("waiver", {}).get("reason")
            or not issue.get("waiver", {}).get("authority")
        ):
            out.append(finding("ISSUE003", "S3", f"waived issue {issue.get('id')} lacks waiver authority or reason", True))

    release = state.get("release", {})
    candidates = release.get("candidate_artifact_ids", [])
    known_ids = set(artifact_ids)
    for candidate in candidates:
        if candidate not in known_ids:
            out.append(finding("RELEASE001", "S4", f"release candidate references unknown artifact {candidate}", True))
    required_checks = set(release.get("required_checks", []))
    completed_checks = set(release.get("completed_checks", []))
    missing_checks = sorted(required_checks - completed_checks)
    if missing_checks:
        ready = release.get("status") in RELEASE_READY
        out.append(finding("RELEASE002", "S3" if ready else "S1", f"required checks not completed: {', '.join(missing_checks)}", ready))

    by_id = {item.get("id"): item for item in artifacts}
    checked_hashes = release.get("checked_hashes", {})
    for candidate in candidates:
        item = by_id.get(candidate)
        if not item or not item.get("path"):
            continue
        artifact_path = (project_root / item["path"]).resolve()
        if not artifact_path.exists():
            out.append(finding("FILE002", "S3", f"release artifact is missing: {item['path']}", True))
            continue
        expected_hash = checked_hashes.get(candidate)
        if expected_hash and sha256(artifact_path) != expected_hash:
            out.append(finding("RELEASE003", "S3", f"checked hash is stale for artifact {candidate}", True))
        elif release.get("status") in RELEASE_READY and not expected_hash:
            out.append(finding("RELEASE004", "S3", f"ready release lacks checked hash for artifact {candidate}", True))

    if release.get("status") in RELEASE_READY and release.get("visual_check") != "PASSED":
        out.append(finding("RELEASE005", "S3", "ready release lacks a passed visual check", True))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    state_path = Path(args.state).expanduser().resolve()
    root = Path(args.project_root).expanduser().resolve() if args.project_root else state_path.parent
    try:
        findings = audit(load_state(state_path), root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        findings = [finding("STATE000", "S4", str(exc), True)]

    summary = {
        "status": "BLOCKED" if any(item["blocker"] for item in findings) else "PASS",
        "blockers": sum(1 for item in findings if item["blocker"]),
        "findings": findings,
    }
    if args.as_json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(f"{summary['status']}: {summary['blockers']} blocker(s), {len(findings)} finding(s)")
        for item in findings:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 2 if summary["status"] == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
