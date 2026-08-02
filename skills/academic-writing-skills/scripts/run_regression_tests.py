#!/usr/bin/env python3
"""Run deterministic regression tests for manuscript audit scripts."""

from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

from audit_docx_structure import inspect
from audit_manuscript_state import audit
from audit_prose_patterns import audit as audit_prose
from audit_text_consistency import audit as audit_text


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def make_docx(path: Path, inner_xml: str) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", f'<w:document xmlns:w="{W}"><w:body>{inner_xml}</w:body></w:document>')


def base_state(root: Path) -> dict:
    artifact = root / "manuscript.md"
    artifact.write_text("Locked SQ text. Funding SES-2342842. LLM-generated respondents.\n", encoding="utf-8")
    return {
        "project": {"id": "fixture"},
        "artifacts": [{"id": "main", "path": artifact.name, "role": "main_manuscript", "status": "ACTIVE", "required_for_release": True}],
        "authority_sources": [{"id": "src", "status": "VERIFIED"}],
        "contract": {"questions": [{"id": "Q1"}]},
        "semantic_locks": [{"id": "sq", "kind": "EXACT", "canonical": "Locked SQ text.", "required_roles": ["main_manuscript"], "forbidden_variants": ["What similarities and differences"]}],
        "terminology": [{"id": "llm-artifact", "preferred": "LLM-generated respondents", "prohibited": ["LLM households"], "scope_roles": ["main_manuscript"]}],
        "facts": [{"id": "funding", "value": "SES-2342842", "source_id": "src", "scope_roles": ["main_manuscript"], "expected_strings": ["SES-2342842"], "forbidden_strings": ["CBET #1941727"]}],
        "alignment": [{"question_id": "Q1", "method": "m", "evidence": "e", "result": "r", "interpretation": "i", "limitation": "l", "contribution": "c", "status": "COMPLETE"}],
        "dimensions": [{"id": "model-reporting", "values": ["Gemma", "Sonnet"], "required_fields": ["workload"], "coverage": [{"value": "Gemma", "field": "workload", "status": "COMPLETE", "evidence": "SM"}, {"value": "Sonnet", "field": "workload", "status": "COMPLETE", "evidence": "SM"}]}],
        "issues": [],
        "release": {"status": "WORKING", "candidate_artifact_ids": ["main"], "required_checks": [], "completed_checks": [], "checked_hashes": {}, "visual_check": "NOT_RUN"},
    }


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def main() -> int:
    tests: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        state = base_state(root)
        require(not any(item["blocker"] for item in audit(state, root)), "clean state unexpectedly blocked")
        tests.append("clean state")

        missing = copy.deepcopy(state)
        missing["dimensions"][0]["coverage"].pop()
        require(any(item["code"] == "DIM001" for item in audit(missing, root)), "missing model field not detected")
        tests.append("dimension omission")

        blocked = copy.deepcopy(state)
        blocked["issues"] = [{"id": "X", "severity": "S4", "evidence_status": "CONFIRMED", "status": "OPEN", "description": "semantic drift"}]
        require(any(item["code"] == "ISSUE002" for item in audit(blocked, root)), "open S4 blocker not detected")
        tests.append("release blocker")

        working = copy.deepcopy(state)
        working["release"]["required_checks"] = ["argument_structure"]
        release_findings = audit(working, root)
        require(any(item["code"] == "RELEASE002" and not item["blocker"] for item in release_findings), "working-stage release reminder became blocker")
        tests.append("working-stage release reminder")

        ready = copy.deepcopy(state)
        ready["release"]["status"] = "SUBMISSION_READY"
        ready["release"]["visual_check"] = "PASSED"
        ready["release"]["checked_hashes"] = {"main": hashlib.sha256((root / "manuscript.md").read_bytes()).hexdigest()}
        require(not any(item["blocker"] for item in audit(ready, root)), "complete ready release unexpectedly blocked")
        tests.append("submission-ready release")

        require(not audit_text(state, root), "clean text unexpectedly flagged")
        require(not audit_prose(state, root), "clean prose unexpectedly flagged")
        (root / "manuscript.md").write_text("What similarities and differences. Funding CBET #1941727. LLM households.\n", encoding="utf-8")
        codes = {item["code"] for item in audit_text(state, root)}
        require({"LOCK001", "LOCK002", "TERM001", "FACT101", "FACT102"}.issubset(codes), "semantic/fact drift set incomplete")
        tests.append("semantic and fact drift")

        prose = copy.deepcopy(state)
        (root / "manuscript.md").write_text(
            "It is important to note that the model reports one result. "
            "This analysis shows that repeated framing can obscure evidence. "
            "This analysis shows that repeated framing can obscure interpretation. "
            "This analysis shows that repeated framing can obscure the contribution. "
            "The same complete sentence appears here for deterministic testing. "
            "The same complete sentence appears here for deterministic testing.\n",
            encoding="utf-8",
        )
        prose_codes = {item["code"] for item in audit_prose(prose, root)}
        require({"PROSE001", "PROSE002", "PROSE003", "PROSE004"}.issubset(prose_codes), "prose-pattern audit incomplete")
        tests.append("observable prose patterns")

        field_docx = root / "field.docx"
        make_docx(field_docx, '<w:p><w:r><w:instrText>REF _Ref1</w:instrText></w:r><w:r><w:t>Text</w:t></w:r></w:p>')
        report = inspect(field_docx)
        require(report["tracked_changes"] == 0 and report["counts"]["field_instructions"] == 1, "field instruction misclassified as tracked change")
        tests.append("OOXML field false positive")

        edit_docx = root / "edit.docx"
        make_docx(edit_docx, '<w:p><w:ins><w:r><w:t>new</w:t></w:r></w:ins></w:p>')
        require(inspect(edit_docx)["tracked_changes"] == 1, "exact insertion tag not detected")
        tests.append("OOXML insertion")

        split_docx = root / "split.docx"
        make_docx(split_docx, '<w:p><w:r><w:t>Locked SQ</w:t></w:r><w:r><w:t> text.</w:t></w:r></w:p>')
        split_state = copy.deepcopy(state)
        split_state["artifacts"][0]["path"] = split_docx.name
        split_state["facts"] = []
        split_state["terminology"] = []
        require(not audit_text(split_state, root), "exact lock split across Word runs was missed")
        tests.append("DOCX split-run text reconstruction")

    print(json.dumps({"status": "PASS", "tests": tests}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
