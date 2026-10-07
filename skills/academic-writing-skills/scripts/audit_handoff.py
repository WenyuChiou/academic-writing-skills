#!/usr/bin/env python3
"""Validate scoped handoff coverage and exact-file hashes, not editorial quality.

Read-only, standard library only. No manuscript mutation, commands, or network
requests. A complete record is evidence coverage, never scientific certification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat


FEATURES = {"displays", "formatted_file", "venue_formatting", "metadata_changes"}
BASE_CHECKS = {"meaning_and_evidence", "language_scan", "reader_walkthrough"}
ALL_CHECKS = BASE_CHECKS | {
    "progression_and_framing", "caption_allocation", "final_layout",
    "editor_identity", "venue_basis",
}
ROLES = {"candidate", "context", "evidence", "render"}
HASH = re.compile(r"[0-9a-f]{64}")


def required_checks(record: dict) -> set[str]:
    """Derive checks from declared scope/effects; callers must validate first."""
    checks = set(BASE_CHECKS)
    features = record["features"]
    if record["scope"] in {"section", "package"} or record["change"] == "substantive":
        checks.add("progression_and_framing")
    if features["displays"]:
        checks.add("caption_allocation")
    if features["formatted_file"]:
        checks.update({"final_layout", "editor_identity"})
    if features["metadata_changes"]:
        checks.add("editor_identity")
    if features["venue_formatting"]:
        checks.add("venue_basis")
    return checks


def nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def sha256_file(path: Path) -> str:
    """Hash only a regular file, streaming large documents and render evidence."""
    if not stat.S_ISREG(path.stat().st_mode):
        raise ValueError("artifact is not a regular file")
    digest = hashlib.sha256()
    with path.open("rb") as source:
        if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
            raise ValueError("artifact is not a regular file")
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_record(record, root: Path) -> dict:
    """Check record shape, current bytes, applicable coverage, and open findings."""
    invalid, pending = [], []
    required = set()
    artifacts = {}
    if not isinstance(record, dict):
        invalid.append("record must be a JSON object")
        record = {}
    if type(record.get("schema_version")) is not int or record.get("schema_version") != 1:
        invalid.append("schema_version must be integer 1")
    if not isinstance(record.get("scope"), str) or record["scope"] not in {"sentence", "paragraph", "section", "package"}:
        invalid.append("scope must be sentence, paragraph, section, or package")
    if not isinstance(record.get("change"), str) or record["change"] not in {"surface", "substantive"}:
        invalid.append("change must be surface or substantive")
    features = record.get("features")
    if not isinstance(features, dict) or set(features) != FEATURES or any(
        type(value) is not bool for value in features.values()
    ):
        invalid.append("features must declare all four boolean applicability flags")
    if not invalid:
        required = required_checks(record)
    entries = record.get("artifacts")
    if not isinstance(entries, list) or not entries:
        invalid.append("artifacts must be a nonempty list")
        entries = []
    for entry in entries:
        if not isinstance(entry, dict) or not all(nonempty(entry.get(key)) for key in ("id", "path", "role", "sha256")):
            invalid.append("each artifact needs id, path, role, and sha256")
            continue
        name = entry["id"]
        if name in artifacts:
            invalid.append(f"duplicate artifact id: {name}")
            continue
        artifacts[name] = entry
        if entry["role"] not in ROLES or not HASH.fullmatch(entry["sha256"]):
            invalid.append(f"invalid artifact role or SHA256: {name}")
            continue
        path = root / entry["path"]  # absolute paths supported; relative to record
        try:
            if sha256_file(path) != entry["sha256"]:
                invalid.append(f"SHA256 mismatch: {name}; recheck affected candidate/dependencies")
        except (OSError, ValueError) as exc:
            invalid.append(f"unreadable artifact {name}: {exc}")
    if not any(entry["role"] == "candidate" for entry in artifacts.values()):
        invalid.append("at least one exact candidate artifact is required")
    checks = record.get("checks")
    if not isinstance(checks, dict):
        invalid.append("checks must be an object")
        checks = {}
    unknown = set(checks) - ALL_CHECKS
    if unknown:
        invalid.append(f"unknown checks: {sorted(unknown)}")
    for name in sorted(required | (set(checks) & ALL_CHECKS)):
        check = checks.get(name)
        if check is None:
            pending.append(f"{name}: not_run (missing record)")
            continue
        if not isinstance(check, dict):
            invalid.append(f"{name}: check must be an object")
            continue
        status = check.get("status")
        if isinstance(status, str) and status in {"not_run", "unavailable", "not_applicable"}:
            if not nonempty(check.get("reason")):
                invalid.append(f"{name}: {status} requires a reason")
            if status == "not_applicable" and name in required:
                invalid.append(f"{name}: required check cannot be not_applicable")
            elif name in required:
                pending.append(f"{name}: {status}: {check.get('reason', '')}")
            continue
        if status != "checked":
            invalid.append(f"{name}: unsupported status")
            continue
        ids = check.get("artifact_ids")
        if not isinstance(ids, list) or not ids or any(not nonempty(value) or value not in artifacts for value in ids):
            invalid.append(f"{name}: checked needs known artifact_ids")
            ids = []
        if not nonempty(check.get("locator")) or not nonempty(check.get("finding")):
            invalid.append(f"{name}: checked needs a concrete locator and finding")
        if not isinstance(check.get("outcome"), str) or check["outcome"] not in {"resolved", "open"}:
            invalid.append(f"{name}: checked outcome must be resolved or open")
        elif check["outcome"] == "open":
            pending.append(f"{name}: reviewed but unresolved")
        if name == "final_layout" and not any(artifacts[value]["role"] == "render" for value in ids):
            invalid.append("final_layout: checked requires final-file render evidence, not XML alone")
        if name == "venue_basis":
            if not isinstance(check.get("basis"), str) or check["basis"] not in {"verified_requirement", "project_preference", "example"} or not nonempty(check.get("source")):
                invalid.append("venue_basis: classify requirement/preference/example and identify its source")
        if name == "editor_identity":
            expected, observed = check.get("expected_author"), check.get("new_edit_authors")
            if not nonempty(expected) or not isinstance(observed, list) or any(not nonempty(value) for value in observed):
                invalid.append("editor_identity: expected_author and observed new_edit_authors required")
            elif not observed and not nonempty(check.get("absence_reason")):
                invalid.append("editor_identity: empty new_edit_authors requires a verified absence_reason covering applicable file properties")
            elif any(value != expected for value in observed):
                pending.append("editor_identity: new edit/reply authors differ from the explicit author contract")
    return {
        "status": "INVALID" if invalid else "INCOMPLETE" if pending else "COVERAGE_COMPLETE",
        "required_checks": sorted(required), "findings": invalid + pending,
        "editorial_quality_certified": False,
        "limit": "Validates declared coverage and file hashes only; human/agent judgment and truthful evidence remain necessary.",
    }


def load_record(path: Path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = audit_record(load_record(args.record), args.record.absolute().parent)
    except (OSError, UnicodeError, ValueError) as exc:
        result = {"status": "ERROR", "findings": [str(exc)], "editorial_quality_certified": False}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=True))
    else:
        print(result["status"] + " (coverage only; not editorial certification)")
        for finding in result["findings"]:
            print("- " + finding)
    return {"COVERAGE_COMPLETE": 0, "INCOMPLETE": 1, "INVALID": 2, "ERROR": 2}[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
