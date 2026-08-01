#!/usr/bin/env python3
"""Scan active manuscript artifacts for registered semantic and factual conflicts."""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
TEXT_SUFFIXES = {".txt", ".md", ".csv", ".tsv", ".json", ".yaml", ".yml", ".tex"}


def docx_text(path: Path) -> str:
    parts: list[str] = []
    with zipfile.ZipFile(path) as archive:
        names = [
            name for name in archive.namelist()
            if re.fullmatch(r"word/(document|footnotes|endnotes|comments|header\d+|footer\d+)\.xml", name)
        ]
        for name in sorted(names):
            root = ET.fromstring(archive.read(name))
            for paragraph in root.iter(f"{{{WORD_NS}}}p"):
                runs = [
                    node.text or ""
                    for node in paragraph.iter()
                    if node.tag in {f"{{{WORD_NS}}}t", f"{{{WORD_NS}}}delText"}
                ]
                if runs:
                    parts.append("".join(runs))
    return "\n".join(parts)


def extract_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        return docx_text(path)
    if path.suffix.lower() in TEXT_SUFFIXES:
        return path.read_text(encoding="utf-8", errors="replace")
    raise ValueError(f"unsupported file type: {path.suffix}")


def contains(text: str, needle: str, case_sensitive: bool = False) -> bool:
    if not case_sensitive:
        text, needle = text.casefold(), needle.casefold()
    return needle in text


def audit(state: dict[str, Any], project_root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    artifacts: dict[str, dict[str, Any]] = {}
    for item in state.get("artifacts", []):
        if item.get("status") != "ACTIVE" or not item.get("path"):
            continue
        path = (project_root / item["path"]).resolve()
        try:
            artifacts[item.get("id", item["path"])] = {**item, "text": extract_text(path)}
        except (OSError, ValueError, zipfile.BadZipFile, ET.ParseError) as exc:
            findings.append({"code": "TEXT000", "artifact": item.get("id"), "message": str(exc)})

    def selected(required_roles: list[str] | None) -> list[dict[str, Any]]:
        if not required_roles:
            return list(artifacts.values())
        return [item for item in artifacts.values() if item.get("role") in required_roles]

    for lock in state.get("semantic_locks", []):
        canonical = str(lock.get("canonical", ""))
        target_items = selected(lock.get("required_roles"))
        if lock.get("kind") == "EXACT" and canonical and not any(contains(item["text"], canonical, True) for item in target_items):
            findings.append({"code": "LOCK001", "lock": lock.get("id"), "message": "required exact lock not found"})
        for variant in lock.get("forbidden_variants", []):
            for item in target_items:
                if contains(item["text"], str(variant)):
                    findings.append({"code": "LOCK002", "lock": lock.get("id"), "artifact": item.get("id"), "match": variant, "message": "forbidden semantic variant found"})

    for term in state.get("terminology", []):
        for variant in term.get("prohibited", []):
            for item in selected(term.get("scope_roles")):
                if contains(item["text"], str(variant)):
                    findings.append({"code": "TERM001", "term": term.get("id"), "artifact": item.get("id"), "match": variant, "message": "prohibited term variant found"})

    for fact in state.get("facts", []):
        for variant in fact.get("forbidden_strings", []):
            for item in selected(fact.get("scope_roles")):
                if contains(item["text"], str(variant), True):
                    findings.append({"code": "FACT101", "fact": fact.get("id"), "artifact": item.get("id"), "match": variant, "message": "conflicting fact string found"})
        expected = fact.get("expected_strings", [])
        if expected:
            for item in selected(fact.get("scope_roles")):
                if not any(contains(item["text"], str(value), True) for value in expected):
                    findings.append({"code": "FACT102", "fact": fact.get("id"), "artifact": item.get("id"), "message": "expected fact string not found"})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    state_path = Path(args.state).expanduser().resolve()
    root = Path(args.project_root).expanduser().resolve() if args.project_root else state_path.parent
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
        findings = audit(state, root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        findings = [{"code": "TEXT000", "message": str(exc)}]
    result = {"status": "FINDINGS" if findings else "PASS", "findings": findings}
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"{result['status']}: {len(findings)} finding(s)")
        for item in findings:
            print(f"{item['code']}: {item['message']} ({item.get('artifact', 'project')})")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
