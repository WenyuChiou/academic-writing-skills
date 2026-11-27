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
from audit_prose_patterns import audit as audit_prose, audit_text as audit_prose_text, sentences
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

        sequence = (
            "We first fit the income distributions. "
            "We then sample incomes from these distributions. "
            "We next calculate losses relative to income."
        )
        frames = [item for item in audit_prose_text(sequence, "candidate", {}) if item["code"] == "PROSE013"]
        require(len(frames) == 1 and frames[0]["count"] == 3, "varying procedural sentence frames were missed")
        require(frames[0]["paragraph"] == 1 and frames[0]["sentence_start"] == 1, "frame finding lacks a local anchor")
        require(frames[0]["sentence_end"] == 3, "frame finding has an incorrect end anchor")
        anchored = [item for item in audit_prose_text("The inputs are fixed. " + sequence, "anchored", {}) if item["code"] == "PROSE013"]
        require(len(anchored) == 1 and anchored[0]["sentence_start"] == 2 and anchored[0]["sentence_end"] == 4, "noninitial frame anchors are incorrect")
        separated = [item for item in audit_prose_text(sequence + " The inputs are fixed. " + sequence, "separated", {}) if item["code"] == "PROSE013"]
        require([(item["sentence_start"], item["sentence_end"]) for item in separated] == [(1, 3), (5, 7)], "multiple disjoint frame runs were merged or misanchored")
        require("preserve" in frames[0]["message"], "procedural ordering was treated as an automatic error")
        require(
            any(item["code"] == "PROSE013" for item in audit_candidate(sequence, "candidate", state)),
            "exact-candidate gate missed procedural frame repetition",
        )
        tests.append("varying sentence-frame family and exact-candidate coverage")

        for label, passage in {
            "two necessary steps": "We first fit the distributions. We then sample incomes.",
            "separate paragraphs": "We first fit distributions.\n\nWe then sample incomes.\n\nWe next calculate losses.",
            "wrapped paragraph": "We first fit\nthe distributions. We then sample\nincomes. We next calculate losses.",
            "intervening finding": "We first fit distributions. The fit meets the stated criterion. We then sample incomes. We next calculate losses.",
            "content-led repair": "We fit the income distributions and sample incomes from them. The sampled incomes are then used to calculate losses relative to income.",
        }.items():
            expected = label == "wrapped paragraph"
            actual = any(item["code"] == "PROSE013" for item in audit_prose_text(passage, label, {}))
            require(actual == expected, f"sentence-frame boundary failed: {label}")
        tests.append("procedural-frame scope and necessary-order boundaries")

        frames_docx = root / "frames.docx"
        make_docx(frames_docx, "".join(
            f"<w:p><w:r><w:t>{sentence}</w:t></w:r></w:p>"
            for sentence in (
                "We first fit distributions.", "We then sample incomes.", "We next calculate losses.",
            )
        ))
        frames_state = copy.deepcopy(state)
        frames_state["artifacts"][0]["path"] = frames_docx.name
        require(
            not any(item["code"] == "PROSE013" for item in audit_prose(frames_state, root)),
            "DOCX paragraph boundaries were flattened into one procedural run",
        )
        tests.append("DOCX procedural-frame paragraph boundaries")

        for passage in (
            "Taken together, the findings distinguish losses before and after payouts.",
            "Taken together the findings distinguish the two loss measures.",
            "Beyond insurance, relocation changes exposure.",
        ):
            require(
                any(item["code"] == "PROSE012" for item in audit_prose_text(passage, "connective", {})),
                f"contextual transition was missed: {passage}",
            )
        require(
            not any(item["code"] == "PROSE012" for item in audit_prose_text(
                "Floodwater extended beyond the study boundary. Samples were taken together for analysis.",
                "literal uses", {},
            )),
            "literal beyond or nonconnective taken together was treated as a stock opening",
        )
        tests.append("Taken together review and literal beyond boundary")

        require(
            any("sentence-opening families" in check and "necessary procedural order" in check for check in MANUAL_CHECKS),
            "manual candidate gate omitted structural variety and procedural-order preservation",
        )
        tests.append("sentence-family manual acceptance gate")

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
        require(
            not audit_text(split_state, root),
            "exact lock split across Word runs was missed",
        )
        tests.append("DOCX split-run text reconstruction")

        require(
            any("host-journal register" in check for check in MANUAL_CHECKS)
            and any("bundled condition caveats" in check for check in MANUAL_CHECKS)
            and any("guided 5-step Results arc" in check for check in MANUAL_CHECKS)
            and any("polysemous modifiers" in check for check in MANUAL_CHECKS),
            "manual candidate gate omitted host-register, bundled-condition, guided-results, or polysemous checks",
        )
        tests.append("host-register onboarding, guided results, and bundled-condition manual checks")

        second_wave = (
            "It is not merely a prompt trick; it is a watershed shift. "
            "Model A achieved 0.04 on Figure 2, thereby highlighting the urgent need for management. "
            "Two models reached 0.04 on the Wave 2 metric (p < 0.01)."
        )
        second_codes = {item["code"] for item in audit_prose_text(second_wave, "second-wave", {})}
        require(
            {"PROSE014", "PROSE015", "PROSE016", "PROSE017"}.issubset(second_codes),
            f"second-wave / guided-results codes incomplete: {sorted(second_codes)}",
        )
        require(
            any(item["code"] == "PROSE003" for item in audit_prose_text("綜上所述，本研究賦能防洪調適。", "cjk-stock", {})),
            "CJK stock phrase audit missed boilerplate",
        )
        require(
            not any(
                item["code"] in {"PROSE014", "PROSE015", "PROSE016", "PROSE017"}
                for item in audit_prose_text(
                    "To evaluate household transitions, Figure 2 compares errors. "
                    "Both models reached 0.04 each at Wave 2, limiting inference to exploratory trends.",
                    "guided-clean", {},
                )
            ),
            "clean guided Results passage triggered false-positive PROSE014-017",
        )
        tests.append("second-wave AI tells, CJK stock phrases, and guided Results cues")

        from audit_companion_limits import (
            _extract_captions, check_abstract, check_caption_sync, check_csv_table, check_discrete_band,
            check_docx_tables, check_highlights, check_latex_citations, check_latex_tables,
            check_text_formatting,
        )
        from audit_figure_style import lint_png_file, lint_python_script
        import struct

        hl = root / "highlights.txt"
        hl.write_text("Highlights\n- " + ("x" * 90) + "\n- Concise highlight line.\n", encoding="utf-8")
        require(any(item["code"] == "COMP001" for item in check_highlights(hl)), "long highlight missed")
        abs_file = root / "abstract.txt"
        abs_file.write_text(("word " * 260).strip(), encoding="utf-8")
        require(any(item["code"] == "COMP002" for item in check_abstract(abs_file)), "long abstract missed")
        cap_file = root / "captions.txt"
        cap_file.write_text("Figure 1. Accuracy by group.\nShaded bands show 95% CIs.\n", encoding="utf-8")
        ms_cap = root / "ms_cap.txt"
        ms_cap.write_text("Figure 1. Accuracy by group.\nShaded bands show standard deviations.\n$-40K and 0.208[0.189, 0.229].\n", encoding="utf-8")
        require(any(item["code"] == "COMP003" for item in check_caption_sync(ms_cap, cap_file)), "multiline caption continuation mismatch missed")
        require(len(check_text_formatting(ms_cap)) == 2, "numeric currency/CI spacing check missed")
        esc_md = root / "escaped_currency.md"
        esc_md.write_text(r"Estimated bias was \$-40K in Markdown.", encoding="utf-8")
        require(any(item["code"] == "COMP004" for item in check_text_formatting(esc_md)), "escaped \\$-40K in Markdown missed")

        word_cap_docx = root / "word_caps.docx"
        make_docx(
            word_cap_docx,
            '<w:p><w:r><w:t>first</w:t><w:br/><w:t>second</w:t></w:r>'
            '<w:moveFrom w:author="A"><w:r><w:t> oldmoved</w:t></w:r></w:moveFrom></w:p>'
            '<w:moveFrom w:author="A"><w:p><w:r><w:t>three hidden words</w:t></w:r></w:p></w:moveFrom>',
        )
        require(check_abstract(word_cap_docx, max_words=2) == [], "w:moveFrom paragraph or run was counted or w:br merged words")
        two_words = root / "word_breaks.docx"
        make_docx(two_words, '<w:p><w:r><w:t>alpha</w:t><w:br/><w:t>beta</w:t></w:r></w:p>')
        require(any(item["code"] == "COMP002" for item in check_abstract(two_words, max_words=1)), "w:br word split not counted cleanly")
        csv_file = root / "table.csv"
        csv_file.write_text("model,status,val\nA,available,NA\n", encoding="utf-8")
        require(any(item["code"] == "COMP005" for item in check_csv_table(csv_file)), "CSV available/NA missed")
        require(any(item["code"] == "COMP006" for item in check_discrete_band(3, 0.114)), "discrete step band missed")
        tests.append("companion limits, caption sync, currency/CI formatting, and discrete-band checks")

        bad_plot = root / "bad_plot.py"
        bad_plot.write_text(
            "import matplotlib.pyplot as plt\n"
            "plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']\n"
            "f, (ax1, ax2) = plt.subplots(1, 2)\n"
            "f.suptitle('Baked')\n"
            "ax1.legend()\n"
            "ax1.set_ylabel('RMSEA ≤ 0.08')\n"
            "ax1.set_yticks([0.00, 0.04, 0.08, 0.10, 0.12])\n"
            "ax1.set_ylim(0, 38)\n"
            "ax2.set_ylim(0, 45)\n"
            "f.savefig('x.png')\n",
            encoding="utf-8",
        )
        fig_codes = {item["code"] for item in lint_python_script(bad_plot)}
        require({"FIG001", "FIG002", "FIG003", "FIG004", "FIG005"}.issubset(fig_codes), f"figure linter missed codes: {sorted(fig_codes)}")
        add_sub_plot = root / "add_sub.py"
        add_sub_plot.write_text(
            "import matplotlib.pyplot as plt\n"
            "plt.rcParams.update({'axes.unicode_minus': False})\n"
            "canvas = plt.figure()\n"
            "p1 = canvas.add_subplot(1, 2, 1)\n"
            "p2 = canvas.add_subplot(1, 2, 2)\n"
            "p1.set_ylim(0, 10)\n"
            "p2.set_ylim(0, 20)\n",
            encoding="utf-8",
        )
        require(any(item["code"] == "FIG005" for item in lint_python_script(add_sub_plot)), "add_subplot Fig005 missed")
        clean_separate_figs = root / "separate_figs.py"
        clean_separate_figs.write_text(
            "import matplotlib.pyplot as plt\n"
            "plt.rcParams.update({'axes.unicode_minus': False})\n"
            "if True:\n"
            "    fig, (ax1, ax2) = plt.subplots(1, 2)\n"
            "    ax1.set_xlabel(r'$-0.25$')\n"
            "    ax1.set_ylim(0, 10)\n"
            "    ax2.set_ylim(0, 10)\n"
            "    def unused_helper():\n"
            "        ax2.set_ylim(0, 99)\n"
            "def f1():\n    f, ax = plt.subplots()\n    ax.set_ylim(0, 10)\n    ax.set_ylim(0, 12)\n"
            "figure_custom, ax_c = plt.subplots()\n"
            "figure_custom.legend(loc='upper center')\n"
            "def f2():\n    f, ax2 = plt.subplots()\n    ax2.set_ylim(0, 99)\n"
            "fig_a, (ax1, ax2) = plt.subplots(1, 2)\n"
            "ax1.set_ylim(0, 10)\n"
            "ax2.set_ylim(0, 10)\n"
            "fig_b, ax1 = plt.subplots()\n"
            "ax1.set_ylim(0, 100)\n",
            encoding="utf-8",
        )
        require(lint_python_script(clean_separate_figs) == [], f"false positive on mathtext / nested def / separate figs: {lint_python_script(clean_separate_figs)}")
        small_png = root / "small.png"
        ihdr_data = struct.pack(">IIBBBBB", 640, 400, 8, 2, 0, 0, 0)
        small_png.write_bytes(b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + ihdr_data + b"\x00\x00\x00\x00")
        require(any(item["code"] == "FIG006" for item in lint_png_file(small_png)), "narrow PNG width missed")
        tests.append("static figure style AST and PNG width linter")

        tex_doc = root / "manuscript.tex"
        tex_doc.write_text(
            "\\documentclass{article}\n"
            "% \\cite{ghost_comment_key}\n"
            "\\begin{document}\n"
            "\\begin{abstract}Short abstract.\\end{abstract}\n"
            "\\citestyle{authoryear}\n"
            "\\newcites{supp}{Supplementary references}\n"
            "\\section{Results}\n"
            "It is not merely an LLM; it is a watershed shift \\parencite{smith2024,missing2025}.\n"
            "See \\citeurl{url2024}, \\citeyearpar{yr2024}, and \\parencites[see][]{multiA}[cf.]{multiB}.\n"
            "The change was $-0.25$ units overall.\n"
            "\\begin{figure}\\caption{Accuracy by group. Shaded bands show standard deviations.}\\end{figure}\n"
            "\\begin{table}\\begin{tabular}[t]{p{3cm}|c}\\hline\\hline A & \\$-40K \\\\\\hline\\end{tabular}\\end{table}\n"
            "\\begin{longtable}{lc}\\caption{Long table summary.}\\label{tab:lt}\\\\ \\endfirsthead "
            "\\caption[]{Long table summary (continued).}\\\\ \\endhead A & B \\\\ \\end{longtable}\n"
            "\\end{document}\n",
            encoding="utf-8",
        )
        bib_doc = root / "refs.bib"
        bib_doc.write_text(
            "@article{\n  smith2024,\n  title={Flood}\n}\n"
            "@misc{url2024,\n  title={URL}\n}\n"
            "@article{yr2024,\n  title={YearPar}\n}\n"
            "@article{multiA,\n  title={A}\n}\n"
            "@article{multiB,\n  title={B}\n}\n"
            "@article{uncited2023,\n  title={Extra}\n}\n",
            encoding="utf-8",
        )
        clean_math_tex = root / "clean_math.tex"
        clean_math_tex.write_text("The change was $-0.25$ units and the bias was -$40\\text{K}.\n", encoding="utf-8")
        require(check_text_formatting(clean_math_tex) == [], f"false positive COMP004 on inline math: {check_text_formatting(clean_math_tex)}")
        tex_state = {"artifacts": [{"id": "tex", "path": "manuscript.tex", "role": "manuscript", "status": "ACTIVE"}]}
        tex_prose_codes = {item["code"] for item in audit_prose(tex_state, root)}
        require("PROSE014" in tex_prose_codes, f"LaTeX prose unwrap missed PROSE014: {sorted(tex_prose_codes)}")
        require(check_abstract(tex_doc, max_words=5) == [], "LaTeX abstract environment word count included body")
        tex_caps = _extract_captions(tex_doc)
        require(tex_caps.get("Table 1") == "Long table summary.", f"longtable caption unexpected: {tex_caps}")
        require(any(item["code"] == "COMP003" for item in check_caption_sync(tex_doc, cap_file)), "LaTeX caption sync mismatch missed")
        require(len(check_text_formatting(tex_doc)) == 1, f"expected only escaped \\$-40K COMP004: {check_text_formatting(tex_doc)}")
        require(len(check_latex_tables(tex_doc)) >= 2, "LaTeX COMP007 vertical-rule/double-hline check missed")
        cite_keys = {item["key"] for item in check_latex_citations([tex_doc], [bib_doc])}
        require(cite_keys == {"missing2025", "uncited2023"}, f"BibTeX reconciliation unexpected keys: {cite_keys}")
        tests.append("LaTeX prose unwrapping, abstract/caption sync, booktabs COMP007, and BibTeX COMP008")

        bad_tbl_docx = root / "bad_table.docx"
        make_docx(
            bad_tbl_docx,
            '<w:tbl><w:tblPr><w:tblBorders><w:insideV w:val="single" w:sz="4"/></w:tblBorders></w:tblPr>'
            '<w:tr><w:tc><w:p><w:r><w:t>H1</w:t></w:r></w:p></w:tc></w:tr>'
            '<w:tr><w:tc><w:p><w:r><w:t>V1</w:t></w:r></w:p></w:tc></w:tr></w:tbl>',
        )
        docx_tbl_msgs = [item["message"] for item in check_docx_tables(bad_tbl_docx)]
        require(
            any("vertical borders" in msg for msg in docx_tbl_msgs) and any("w:tblHeader" in msg for msg in docx_tbl_msgs),
            f"Word table COMP009 missed border/header findings: {docx_tbl_msgs}",
        )
        styled_grid_docx = root / "styled_grid.docx"
        with zipfile.ZipFile(styled_grid_docx, "w") as archive:
            archive.writestr(
                "word/document.xml",
                f'<w:document xmlns:w="{W}"><w:body>'
                '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/></w:tblPr>'
                '<w:tr><w:trPr><w:tblHeader/></w:trPr><w:tc><w:p><w:r><w:t>H1</w:t></w:r></w:p></w:tc></w:tr>'
                '<w:tr><w:tc><w:p><w:r><w:t>V1</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
                '</w:body></w:document>',
            )
            archive.writestr(
                "word/styles.xml",
                f'<w:styles xmlns:w="{W}"><w:style w:type="table" w:styleId="TableGrid">'
                '<w:tblPr><w:tblBorders><w:insideV w:val="single" w:sz="4"/></w:tblBorders></w:tblPr>'
                '</w:style></w:styles>',
            )
        require(
            any("vertical borders" in item["message"] for item in check_docx_tables(styled_grid_docx)),
            "Word TableGrid inherited vertical border missed",
        )
        clean_tbl_docx = root / "clean_table.docx"
        with zipfile.ZipFile(clean_tbl_docx, "w") as archive:
            archive.writestr(
                "word/document.xml",
                f'<w:document xmlns:w="{W}"><w:body>'
                '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
                '<w:tblBorders><w:left w:val="none"/><w:right w:val="none"/><w:insideV w:val="none"/></w:tblBorders></w:tblPr>'
                '<w:tr><w:trPr><w:tblHeader/></w:trPr><w:tc><w:p><w:r><w:t>H1</w:t></w:r></w:p></w:tc></w:tr>'
                '<w:tr><w:tc><w:p><w:r><w:t>V1</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
                '</w:body></w:document>',
            )
            archive.writestr(
                "word/styles.xml",
                f'<w:styles xmlns:w="{W}"><w:style w:type="table" w:styleId="TableGrid">'
                '<w:tblPr><w:tblBorders><w:insideV w:val="single" w:sz="4"/></w:tblBorders></w:tblPr>'
                '</w:style></w:styles>',
            )
        require(check_docx_tables(clean_tbl_docx) == [], f"false positive on overridden Word three-line table: {check_docx_tables(clean_tbl_docx)}")
        tests.append("Word .docx three-line table borders and w:tblHeader COMP009 check")

    print(json.dumps({"status": "PASS", "tests": tests}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
