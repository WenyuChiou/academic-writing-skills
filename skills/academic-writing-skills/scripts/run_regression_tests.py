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
from audit_candidate_text import MANUAL_CHECKS, audit_candidate
from audit_prose_patterns import audit as audit_prose, sentences
from audit_text_consistency import audit as audit_text


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14 = "http://schemas.microsoft.com/office/word/2010/wordml"
W15 = "http://schemas.microsoft.com/office/word/2012/wordml"


def make_docx(path: Path, inner_xml: str) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", f'<w:document xmlns:w="{W}"><w:body>{inner_xml}</w:body></w:document>')


def make_comment_docx(path: Path, parent_id: str = "A0000001") -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(
            "word/document.xml",
            f'<w:document xmlns:w="{W}"><w:body><w:p><w:ins w:author="Wenyu Chiou"><w:r><w:t>new</w:t></w:r></w:ins></w:p></w:body></w:document>',
        )
        archive.writestr(
            "word/comments.xml",
            f'<w:comments xmlns:w="{W}" xmlns:w14="{W14}">'
            '<w:comment w:id="0" w:author="Ethan Yang"><w:p w14:paraId="A0000001"><w:r><w:t>Revise.</w:t></w:r></w:p></w:comment>'
            '<w:comment w:id="1" w:author="Wenyu Chiou"><w:p w14:paraId="B0000001"><w:r><w:t>Revised.</w:t></w:r></w:p></w:comment>'
            '</w:comments>',
        )
        archive.writestr(
            "word/commentsExtended.xml",
            f'<w15:commentsEx xmlns:w15="{W15}">'
            '<w15:commentEx w15:paraId="A0000001" w15:done="0"/>'
            f'<w15:commentEx w15:paraId="B0000001" w15:paraIdParent="{parent_id}" w15:done="0"/>'
            '</w15:commentsEx>',
        )


def make_review_docx(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(
            "word/document.xml",
            f'<w:document xmlns:w="{W}"><w:body><w:p>'
            '<w:r><w:t>Accepted wording.</w:t></w:r>'
            '<w:del><w:r><w:delText>LLM households and nominal significance.</w:delText></w:r></w:del>'
            '</w:p></w:body></w:document>',
        )
        archive.writestr(
            "word/comments.xml",
            f'<w:comments xmlns:w="{W}"><w:comment w:id="0" w:author="Reviewer">'
            '<w:p><w:r><w:t>LLM households and nominal significance.</w:t></w:r></w:p>'
            '</w:comment></w:comments>',
        )


def base_state(root: Path) -> dict:
    artifact = root / "manuscript.md"
    artifact.write_text("Locked SQ text. Funding TEST-GRANT-ALPHA. LLM-generated respondents.\n", encoding="utf-8")
    return {
        "project": {"id": "fixture"},
        "artifacts": [{"id": "main", "path": artifact.name, "role": "main_manuscript", "status": "ACTIVE", "required_for_release": True}],
        "authority_sources": [{"id": "src", "status": "VERIFIED"}],
        "contract": {"questions": [{"id": "Q1"}]},
        "semantic_locks": [{"id": "sq", "kind": "EXACT", "canonical": "Locked SQ text.", "required_roles": ["main_manuscript"], "forbidden_variants": ["What similarities and differences"]}],
        "terminology": [{"id": "llm-artifact", "preferred": "LLM-generated respondents", "prohibited": ["LLM households"], "scope_roles": ["main_manuscript"]}],
        "facts": [{"id": "funding", "value": "TEST-GRANT-ALPHA", "source_id": "src", "scope_roles": ["main_manuscript"], "expected_strings": ["TEST-GRANT-ALPHA"], "forbidden_strings": ["TEST-GRANT-BETA"]}],
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
        (root / "manuscript.md").write_text("What similarities and differences. Funding TEST-GRANT-BETA. LLM households.\n", encoding="utf-8")
        codes = {item["code"] for item in audit_text(state, root)}
        require({"LOCK001", "LOCK002", "TERM001", "FACT101", "FACT102"}.issubset(codes), "semantic/fact drift set incomplete")
        tests.append("semantic and fact drift")

        alias_state = copy.deepcopy(state)
        alias_state["terminology"] = [{
            "concept": "flood experience", "preferred": "flood experience", "avoid": ["FE"],
            "scope_roles": ["main_manuscript"],
        }]
        (root / "manuscript.md").write_text("FE was used as a shorthand.\n", encoding="utf-8")
        require(any(item["code"] == "TERM001" for item in audit_text(alias_state, root)), "legacy avoid alias was ignored")
        tests.append("terminology avoid alias")

        candidate_state = copy.deepcopy(alias_state)
        candidate_state["style_profile"] = {"discouraged_phrases": ["together"]}
        candidate_findings = audit_candidate("Together, FE summarizes the result.", "candidate", candidate_state)
        require({"PROSE003", "TERM001"}.issubset({item["code"] for item in candidate_findings}), "candidate gate missed introduced prose or terminology")
        require(not audit_candidate("Flood experience summarizes the result.", "candidate", candidate_state), "clean candidate unexpectedly flagged")
        require(not audit_candidate("Sufficient evidence summarizes the result.", "candidate", candidate_state), "short prohibited term matched inside a longer word")
        tests.append("exact candidate prose and terminology gate")

        malformed = copy.deepcopy(state)
        malformed["semantic_locks"] = [{"term": "decision variables", "rule": "Use consistently."}]
        require(any(item["code"] == "STATE101" and item["blocker"] for item in audit(malformed, root)), "nonauditable semantic lock silently passed")
        require(any(item["code"] == "CAND002" for item in audit_candidate("Decision variables were compared.", "candidate", malformed)), "candidate gate accepted a malformed project profile")
        tests.append("state schema rejects nonauditable locks")

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

        functional = copy.deepcopy(state)
        functional["style_profile"] = {
            "preferred_open_compounds": ["disaster management"],
        }
        (root / "manuscript.md").write_text(
            "This result identifies one limitation. These findings require another check. "
            "Overall, results are mixed. The subgroup- and topic-specific pattern is unclear. "
            "Evidence—rather than fluency—sets the boundary. "
            "A profile-conditioned, model-specific, group-sensitive, response-level comparison follows. "
            "The review covers disaster-management phases.\n",
            encoding="utf-8",
        )
        functional_codes = {item["code"] for item in audit_prose(functional, root)}
        require(
            {"PROSE006", "PROSE007", "PROSE008", "PROSE009", "PROSE010", "PROSE011"}.issubset(functional_codes),
            "functional prose and dash diagnostics incomplete",
        )
        tests.append("functional prose and dash diagnostics")

        require(
            len(sentences("Hullman et al. (2026) provide one boundary. Another sentence follows.")) == 2,
            "sentence splitter treated et al. as a sentence boundary",
        )
        tests.append("scholarly abbreviation sentence splitting")

        open_compound = copy.deepcopy(state)
        open_compound["style_profile"] = {"preferred_open_compounds": ["disaster management"]}
        require(
            any(
                item["code"] == "PROSE011"
                for item in audit_candidate(
                    "The review covers disaster-management phases.",
                    "candidate",
                    open_compound,
                )
            ),
            "registered open compound was not detected in the exact candidate",
        )
        require(
            not audit_candidate(
                "The review covers phases of disaster management and disaster-related tasks.",
                "candidate",
                open_compound,
            ),
            "preferred open compound or valid related compound was incorrectly flagged",
        )
        tests.append("registered open-compound hyphenation")

        require(
            any(
                "literature-example ordering" in check
                and "closest precedent" in check
                for check in MANUAL_CHECKS
            ),
            "exact-candidate gate omitted cumulative literature-example ordering",
        )
        tests.append("cumulative literature-example ordering gate")

        accessibility = copy.deepcopy(state)
        flagged_accessibility = audit_candidate(
            "Beyond simulation, survey studies draw on post-event data.",
            "candidate",
            accessibility,
        )
        require(
            any(item["code"] == "PROSE012" for item in flagged_accessibility),
            "context-sensitive connective and indirect verb were not reported",
        )
        require(
            not audit_candidate(
                "Survey studies use post-event data to predict evacuation decisions.",
                "candidate",
                accessibility,
            ),
            "direct reader-accessible wording was incorrectly flagged",
        )
        tests.append("context-sensitive connective and indirect-verb review")

        require(
            any(
                "reader accessibility" in check
                and "field shorthand" in check
                for check in MANUAL_CHECKS
            ),
            "exact-candidate gate omitted reader-accessibility review",
        )
        tests.append("reader-accessibility exact-candidate gate")

        review_docx = root / "review.docx"
        make_review_docx(review_docx)
        review_state = copy.deepcopy(state)
        review_state["artifacts"][0]["path"] = review_docx.name
        review_state["semantic_locks"] = []
        review_state["facts"] = []
        review_state["terminology"] = [{
            "id": "llm-artifact", "preferred": "LLM-generated respondents",
            "prohibited": ["LLM households"], "scope_roles": ["main_manuscript"],
        }]
        review_state["style_profile"] = {"discouraged_phrases": ["nominal significance"]}
        require(not audit_text(review_state, root), "deleted text or comments polluted terminology audit")
        require(not audit_prose(review_state, root), "deleted text or comments polluted prose audit")
        tests.append("accepted-view DOCX extraction")

        field_docx = root / "field.docx"
        make_docx(field_docx, '<w:p><w:r><w:instrText>REF _Ref1</w:instrText></w:r><w:r><w:t>Text</w:t></w:r></w:p>')
        report = inspect(field_docx)
        require(report["tracked_changes"] == 0 and report["counts"]["field_instructions"] == 1, "field instruction misclassified as tracked change")
        tests.append("OOXML field false positive")

        edit_docx = root / "edit.docx"
        make_docx(edit_docx, '<w:p><w:ins><w:r><w:t>new</w:t></w:r></w:ins></w:p>')
        require(inspect(edit_docx)["tracked_changes"] == 1, "exact insertion tag not detected")
        tests.append("OOXML insertion")

        comment_docx = root / "comments.docx"
        make_comment_docx(comment_docx)
        comment_report = inspect(comment_docx)
        require(comment_report["revision_authors"] == {"Wenyu Chiou": 1}, "revision author not detected")
        require(comment_report["comment_authors"] == {"Ethan Yang": 1, "Wenyu Chiou": 1}, "comment authors not detected")
        require(comment_report["reply_authors"] == {"Wenyu Chiou": 1}, "reply author not detected")
        require(not comment_report["orphan_parent_para_ids"], "valid parent link marked orphan")
        tests.append("OOXML author and reply linkage")

        orphan_docx = root / "orphan-comment.docx"
        make_comment_docx(orphan_docx, parent_id="DEADBEEF")
        require(inspect(orphan_docx)["orphan_parent_para_ids"] == ["DEADBEEF"], "orphan reply parent not detected")
        tests.append("OOXML orphan reply parent")

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
