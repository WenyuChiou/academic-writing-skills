#!/usr/bin/env python3
"""Run deterministic regression tests for manuscript audit scripts."""

from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import tempfile
import zipfile
from pathlib import Path

from audit_docx_structure import inspect
from audit_manuscript_state import audit
from audit_candidate_text import MANUAL_CHECKS, audit_candidate
from audit_prose_patterns import audit as audit_prose, audit_text as audit_prose_text, sentences
from audit_text_consistency import audit as audit_text
from build_context_envelope import (
    M_NS,
    build_scoped_context_envelope,
    extract_from_markdown,
    load_or_build_spine,
    locate_target_blocks,
    main as build_env_main,
)
from run_scoped_manuscript_pass import (
    BackendExecutionError,
    _extract_json_object,
    _prepare_windows_safe_exec_cmd,
    assemble_backend_command,
    evaluate_delegate_reply,
    main as run_scoped_pass_main,
    parse_backend_output,
    validate_delegate_reply_schema,
)
from verify_delegate_numbers import (
    extract_numeric_tokens,
    main as verify_numbers_main,
    verify_curated_salience,
    verify_strict_preservation,
)


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
        md_cap_a = root / "md_cap_a.md"
        md_cap_b = root / "md_cap_b.md"
        md_cap_a.write_text("> **Figure 1.** Accuracy across basins.\n", encoding="utf-8")
        md_cap_b.write_text("**Figure 1.** Accuracy across states.\n", encoding="utf-8")
        require(any(item["code"] == "COMP003" for item in check_caption_sync(md_cap_a, md_cap_b)), "Markdown bold/blockquote caption mismatch missed")
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
        plt_title_script = root / "plt_title_only.py"
        plt_title_script.write_text(
            "import matplotlib.pyplot as plt\n"
            "plt.rcParams.update({'axes.unicode_minus': False})\n"
            "fig, ax = plt.subplots()\n"
            "plt.title('Accuracy by condition')\n"
            "def draw():\n    title('Deferred title')\n"
            "from matplotlib.pyplot import title\n"
            "draw()\n"
            "fig.savefig('t.png')\n",
            encoding="utf-8",
        )
        plt_title_findings = lint_python_script(plt_title_script)
        require(
            [item["line"] for item in plt_title_findings if item["code"] == "FIG001"] == [4, 6],
            f"plt.title / deferred import FIG001 mismatch: {plt_title_findings}",
        )
        rebound_leg = root / "rebound_legend.py"
        rebound_leg.write_text(
            "import matplotlib.pyplot as plt\n"
            "plt.rcParams.update({'axes.unicode_minus': False})\n"
            "plot = plt.figure()\n"
            "plot = plot.add_subplot(111)\n"
            "plot.legend()\n"
            "fig_mc, ax_mc = plt.subplots()\n"
            "match 1:\n"
            "    case 1:\n"
            "        ax_mc.legend()\n",
            encoding="utf-8",
        )
        require(
            sum(1 for item in lint_python_script(rebound_leg) if item["code"] == "FIG002") == 2,
            "reassigned or match-case axis legend missed FIG002",
        )
        add_sub_plot = root / "add_sub.py"
        add_sub_plot.write_text(
            "import matplotlib.pyplot as plt\n"
            "plt.rcParams.update({'axes.unicode_minus': False})\n"
            "canvas = plt.figure()\n"
            "p1 = canvas.add_subplot(1, 2, 1)\n"
            "p2 = canvas.add_subplot(1, 2, 2)\n"
            "p1.set_ylim(0, 10)\n"
            "match 1:\n"
            "    case 1:\n"
            "        p2.set_ylim(0, 20)\n",
            encoding="utf-8",
        )
        require(any(item["code"] == "FIG005" for item in lint_python_script(add_sub_plot)), "add_subplot Fig005 missed")
        scale_isolation = root / "scale_isolation.py"
        scale_isolation.write_text(
            "import matplotlib.pyplot as plt\n"
            "plt.rcParams.update({'axes.unicode_minus': False})\n"
            "fig1, ax = plt.subplots()\n"
            "ax.set_yscale('log')\n"
            "plt.yscale('log')\n"
            "fig2, ax = plt.subplots()\n"
            "ax.set_yticks([1, 2, 3, 4])\n"
            "fig3, ax_bad = plt.subplots()\n"
            "ax_bad.set_yscale('log')\n"
            "ax_bad.set_yticks([1, 10, 12, 100])\n"
            "fig_mp, (ax_mp1, ax_mp2) = plt.subplots(1, 2)\n"
            "plt.yscale('log')\n"
            "ax_mp1.set_yticks([0.00, 0.04, 0.08, 0.10, 0.12])\n"
            "ax_mp2.set_yticks([1, 10, 100, 1000])\n"
            "plt.yscale('log')\n"
            "plt.figure()\n"
            "ax_g = plt.gca()\n"
            "ax_g.set_yticks([1, 2, 3, 4])\n"
            "ax_sub = plt.subplot(111)\n"
            "ax_sub.set_yscale('log')\n"
            "ax_sub = plt.subplot(1, 1, 1)\n"
            "ax_sub.set_yticks([1, 10, 100, 1000])\n"
            "plt.figure()\n"
            "ax_sub_new = plt.subplot(111)\n"
            "ax_sub_new.set_yticks([1, 2, 3, 4])\n"
            "fig_clf = plt.figure()\n"
            "ax_clf = fig_clf.add_subplot(111)\n"
            "ax_clf.set_yscale('log')\n"
            "ax_clf_sub = plt.subplot(111)\n"
            "ax_clf_sub.set_yticks([1, 10, 100, 1000])\n"
            "fig_clf.clf()\n"
            "ax_clf = fig_clf.add_subplot(111)\n"
            "ax_clf.set_yticks([1, 2, 3, 4])\n"
            "fig_sup = plt.figure()\n"
            "ax_sup = fig_sup.add_subplot(111)\n"
            "ax_sup.set_xticks([0.00, 0.04, 0.08, 0.10, 0.12])\n"
            "ax_sup.set_xticks([0.00, 0.04, 0.08, 0.12])\n"
            "fig_exp = plt.figure()\n"
            "ax_exp = fig_exp.add_subplot(111)\n"
            "ax_exp.set_xticks([0.00, 0.04, 0.08, 0.10, 0.12])\n"
            "fig_exp.savefig('before.png')\n"
            "ax_exp.set_xticks([0.00, 0.04, 0.08, 0.12])\n"
            "fig_exp.savefig('after.png')\n"
            "class PlotBox:\n"
            "    fig_cls, ax_cls = plt.subplots()\n"
            "    ax_cls.set_yticks([0.00, 0.04, 0.08, 0.10, 0.12])\n",
            encoding="utf-8",
        )
        require(
            [item["line"] for item in lint_python_script(scale_isolation) if item["code"] == "FIG004"] == [10, 13, 40, 46],
            f"scale isolation / log / ClassDef FIG004 mismatch: {lint_python_script(scale_isolation)}",
        )
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
            "if __name__ == '__main__':\n"
            "    canvas, ax_m = plt.subplots()\n"
            "    canvas.legend(loc='upper center')\n"
            "def f2():\n    f, ax2 = plt.subplots()\n    ax2.set_ylim(0, 99)\n"
            "fig_a, (ax1, ax2) = plt.subplots(1, 2)\n"
            "ax1.set_ylim(0, 10)\n"
            "ax2.set_ylim(0, 10)\n"
            "fig_b, ax1 = plt.subplots()\n"
            "ax1.set_ylim(0, 100)\n"
            "fig_log, ax_log = plt.subplots()\n"
            "ax_log.set_xscale('log')\n"
            "ax_log.set_xticks([1, 10, 100, 1000])\n"
            "ax_log.set_yscale('symlog')\n"
            "ax_log.set_yticks([0, 1, 10, 100])\n"
            "def title(s):\n    return s\n"
            "def local_import_scope():\n    from matplotlib.pyplot import title\n    _ = title\n"
            "_ = title('not a plot title')\n",
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
            "See \\citeurl{url2024}, \\citeyearpar{yr2024}, \\footfullcite{ff2024}, \\citetext{see also \\citealp{paren2024}}, "
            "\\volcite{2}[14]{smith2024}, and \\parencites[see][]{multiA}[cf.]{multiB}.\n"
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
            "@article{ff2024,\n  title={FootFull}\n}\n"
            "@article{multiA,\n  title={A}\n}\n"
            "@article{multiB,\n  title={B}\n}\n"
            "@comment{ @article{disabled2021, title={Disabled}} }\n"
            "@comment{Reviewer called this \"unfinished.}\n"
            "@article(paren2024,\n  title={Effect of treatment (pilot study},\n  note=\"Quoted ) paren\",\n  year={2024}\n)\n"
            "@article{uncited2023,\n  title={Extra}\n}\n",
            encoding="utf-8",
        )
        cited_disabled_tex = root / "disabled_cite.tex"
        cited_disabled_tex.write_text("\\cite{disabled2021}\n", encoding="utf-8")
        require(
            any(item["code"] == "COMP008" and item["key"] == "disabled2021" for item in check_latex_citations([cited_disabled_tex], [bib_doc])),
            "disabled key inside @comment{...} block satisfied missing-entry check",
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
        clean_currency_cap_tex = root / "currency_cap.tex"
        clean_currency_cap_tex.write_text(
            "\\begin{figure}\\caption{Costs were \\$40 and \\$50.}\\end{figure}\n",
            encoding="utf-8",
        )
        clean_currency_cap_md = root / "currency_cap.md"
        clean_currency_cap_md.write_text(
            "**Figure 1.** Costs were $40 and $50.\n",
            encoding="utf-8",
        )
        require(
            check_caption_sync(clean_currency_cap_tex, clean_currency_cap_md) == [],
            f"false positive COMP003 on two escaped currency tokens: {check_caption_sync(clean_currency_cap_tex, clean_currency_cap_md)}",
        )
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

        # 34. PROSE018 inline-numeric-overload-candidate boundary and citation non-false-positive checks
        cite_heavy_para = (
            "Figure 2 compares adaptation pathways across prior studies [1, 2], regional flood benchmarks [3, 4], "
            "household surveys [5–8], longitudinal panels [9, 12], and policy syntheses [14, 15]. "
            "Mean adoption rose from 0.24 to 0.38 across the two basins, indicating bounded uptake."
        )
        require(
            not any(f["code"] == "PROSE018" for f in audit_prose_text(cite_heavy_para, "cite_ok", {})),
            "PROSE018 falsely triggered on integer literature citations [1, 2]",
        )
        overloaded_ci_para = (
            "Table 2 reports change MAE differences of +0.015 ([+0.006, +0.024]) and +0.019 ([+0.009, +0.029]) "
            "on the index, +0.014 ([+0.005, +0.023]) on Tension, +0.016 ([+0.007, +0.025]) on Fatigue, "
            "and +0.013 ([+0.004, +0.022]) on Irritability, answering RQ1."
        )
        require(
            any(f["code"] == "PROSE018" for f in audit_prose_text(overloaded_ci_para, "ci_wall", {})),
            "PROSE018 missed 5-bracket decimal CI wall in display-linked paragraph",
        )
        apa_currency_ci_para = (
            "Figure 3a plots damage relief of +$9.42M ([+$6.85M, +$11.98M]), -$0.18M ([-$0.61M, +$0.24M]), "
            "and APA standardized shifts of .14 ([.10, .18]) and -.09 ([-.15, -.03]), bounding adaptation."
        )
        require(
            any(f["code"] == "PROSE018" for f in audit_prose_text(apa_currency_ci_para, "apa_curr_ci", {})),
            "PROSE018 missed currency/APA leading-dot 4-bracket CI wall",
        )
        overloaded_dec_para = (
            "Figure 4 shows cell values of 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.21, "
            "0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.31, and 0.32 across routine cells, "
            "confirming uniform behavior."
        )
        require(
            any(f["code"] == "PROSE018" for f in audit_prose_text(overloaded_dec_para, "dec_dump", {})),
            "PROSE018 missed >=18 high-density decimal dump",
        )
        require(any("selective numeric reporting" in item for item in MANUAL_CHECKS), "MANUAL_CHECKS missing selective numeric reporting check")
        tests.append("PROSE018 inline-numeric-overload-candidate and citation-bracket immunity")

        # 35. OOXML custom heading styles, <m:oMath>, <w:tbl>, w:del exclusion, and References truncation
        spine_docx = root / "custom_spine.docx"
        with zipfile.ZipFile(spine_docx, "w") as archive:
            archive.writestr(
                "word/styles.xml",
                f'<w:styles xmlns:w="{W}">'
                '<w:style w:type="paragraph" w:styleId="1"><w:name w:val="heading 1"/><w:pPr><w:outlineLvl w:val="0"/></w:pPr></w:style>'
                '<w:style w:type="paragraph" w:styleId="21"><w:name w:val="heading 2"/><w:pPr><w:outlineLvl w:val="1"/></w:pPr></w:style>'
                '<w:style w:type="paragraph" w:styleId="a4"><w:name w:val="List Paragraph"/></w:style>'
                '<w:style w:type="paragraph" w:styleId="ad"><w:name w:val="Bibliography"/></w:style>'
                '</w:styles>',
            )
            archive.writestr(
                "word/document.xml",
                f'<w:document xmlns:w="{W}" xmlns:m="{M_NS}"><w:body>'
                '<w:p><w:r><w:t>Synthetic Coupled Survey and Flood Model Manuscript</w:t></w:r></w:p>'
                '<w:p><w:pPr><w:pStyle w:val="1"/></w:pPr><w:r><w:t>Key Points:</w:t></w:r></w:p>'
                '<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr></w:pPr>'
                '<w:r><w:t>Bundled Memory lowers error on Rumination by 0.052 but drops direction accuracy by 3.8%.</w:t></w:r></w:p>'
                '<w:p><w:pPr><w:outlineLvl w:val="0"/></w:pPr><w:r><w:t>Abstract</w:t></w:r></w:p>'
                '<w:p><w:r><w:t>We evaluate 1,400 respondents across three waves. On Rumination, direction accuracy fell by 3.8%.</w:t></w:r></w:p>'
                '<w:p><w:pPr><w:pStyle w:val="a4"/><w:outlineLvl w:val="0"/><w:numPr><w:numId w:val="2"/></w:numPr></w:pPr><w:r><w:t>Introduction</w:t></w:r></w:p>'
                '<w:p><w:r><w:t>However, prior studies leave untested whether bundled histories improve individual updating. RQ1: Does the bundled Memory condition improve change accuracy on self-reported distress scores?</w:t></w:r></w:p>'
                '<w:p><w:pPr><w:pStyle w:val="1"/></w:pPr><w:r><w:t>3. Methodology</w:t></w:r></w:p>'
                '<w:p><w:r><w:t>Confidence intervals use 2,000 respondent-level paired bootstrap resamples conditional on 3 fixed saved repetitions. </w:t></w:r>'
                '<m:oMath><m:r><m:t>Delta_MAE = MAE_Base - MAE_Memory</m:t></m:r></m:oMath>'
                '<w:del><w:r><w:delText> deleted 9999 old text</w:delText></w:r></w:del></w:p>'
                '<w:tbl><w:tr><w:tc><w:p><w:r><w:t>Outcome</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Delta_Dir</w:t></w:r></w:p></w:tc></w:tr>'
                '<w:tr><w:tc><w:p><w:r><w:t>Tension</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>-1.9%</w:t></w:r></w:p></w:tc></w:tr>'
                '<w:tr><w:tc><w:p><w:r><w:t>Rumination</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>-3.8%</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
                '<w:p><w:pPr><w:pStyle w:val="1"/></w:pPr><w:r><w:t>4. Results</w:t></w:r></w:p>'
                '<w:p><w:pPr><w:pStyle w:val="21"/></w:pPr><w:r><w:t>4.2 Within-Respondent Contrasts</w:t></w:r></w:p>'
                '<w:p><w:r><w:t>Table 1 shows Tension shifted by -1.9% and Rumination shifted by -3.8% (0.052 MAE gain).</w:t></w:r></w:p>'
                '<w:p><w:pPr><w:pStyle w:val="1"/></w:pPr><w:r><w:t>5. Discussion</w:t></w:r></w:p>'
                '<w:p><w:r><w:t>The -3.8% Rumination reversal in Section 4.2 bounds longitudinal deployment.</w:t></w:r></w:p>'
                '<w:p><w:pPr><w:pStyle w:val="1"/></w:pPr><w:r><w:t>References</w:t></w:r></w:p>'
                '<w:p><w:pPr><w:pStyle w:val="ad"/></w:pPr><w:r><w:t>Smith (2024). Journal of Testing, 12, 100-120.</w:t></w:r></w:p>'
                '<w:p><w:pPr><w:outlineLvl w:val="0"/></w:pPr><w:r><w:t>Figures</w:t></w:r></w:p>'
                '<w:p><w:r><w:t>Figure 1. Paired change differences across subscales.</w:t></w:r></w:p>'
                '</w:body></w:document>',
            )
        paper_mem = root / ".paper"
        paper_mem.mkdir(exist_ok=True)
        (paper_mem / "claims.yml").write_text("- id: C1\n  statement: Bundled Memory diverges across Rumination\n  status: supported\n", encoding="utf-8")
        s_blocks, spine_obj = load_or_build_spine(spine_docx, paper_dir=paper_mem)
        require(spine_obj["extraction_stats"]["omath_count"] == 1, f"expected 1 oMath, got {spine_obj['extraction_stats']}")
        require(spine_obj["extraction_stats"]["table_count"] == 1, f"expected 1 table, got {spine_obj['extraction_stats']}")
        require(spine_obj["extraction_stats"]["skipped_reference_blocks"] >= 2, "References truncation did not skip bibliography")
        require(not any("9999" in b["text"] or "Smith (2024)" in b["text"] for b in s_blocks), "w:del or References leaked into spine blocks")
        require("Figure 1" in spine_obj["display_inventory"], "post-References Figures section was lost")
        require(bool(spine_obj["external_memory"]["paper_claims"]), ".paper/claims.yml not fused into spine")
        env_txt, env_meta = build_scoped_context_envelope(s_blocks, spine_obj, target_locator="4.2")
        require(env_meta["within_budget"] and env_meta["est_tokens"] <= 4500, f"envelope exceeded budget: {env_meta}")
        require("Delta_MAE = MAE_Base - MAE_Memory" in env_txt, "oMath formula missing from context envelope")
        # Verify range locator retains embedded Txx table blocks, CommonMark single-newline headings/tables parse cleanly, and cache invalidates on .paper edits
        md_with_tbl, _ = extract_from_markdown("# 1. Intro\n\nLead.\n\n# 2. Results\n\nBefore.\n\n| A | B |\n|---|---|\n| X | 0.5 |\n\nAfter.\n")
        rng_ids = [md_with_tbl[idx]["id"] for idx in locate_target_blocks(md_with_tbl, "P002..P005")]
        require("T01" in rng_ids, f"block range locator dropped embedded table T01: {rng_ids}")
        md_compact, _ = extract_from_markdown(
            "# Compact Title\n## Abstract\nRumination dropped by 3.8% (p = 1.2e-4).\n"
            "## 4. Results\n### 4.2 Subscales\nRumination shifted by −3.8% (p = 1.2E-04).\n"
            "| Subscale | Delta |\n|---|---|\n| Rumination | -3.8% |\n"
            "## 5. Discussion\nDirection accuracy fell by 3.8% (p = 1.2e-4).\n"
        )
        sp_compact = load_or_build_spine.__globals__["build_architecture_spine"](md_compact, "sha")
        deps_compact = load_or_build_spine.__globals__["compute_downstream_dependencies"](
            md_compact, locate_target_blocks(md_compact, "4.2")
        )
        dep_items = {d["item"] for d in deps_compact}
        require(
            ("-3.8%" in dep_items or "3.8%" in dep_items)
            and bool(dep_items & {"1.2e-4", "1.2E-04"})
            and "-4" not in dep_items,
            f"downstream dependencies failed on single-newline Markdown / unsigned-vs-signed % / sci notation: {deps_compact}",
        )
        env_compact, meta_compact = build_scoped_context_envelope(md_compact, sp_compact, target_locator="4.2")
        require(
            env_compact.count("Rumination | -3.8%") == 1 and meta_compact["within_budget"],
            "embedded table in target subsection was duplicated across Section 5 and Section 9",
        )
        cache_p = root / "spine_cache_test.json"
        _, cached_s1 = load_or_build_spine(spine_docx, paper_dir=paper_mem, cache_file=cache_p)
        (paper_mem / "claims.yml").write_text("- id: C2\n  statement: Updated claim text\n  status: supported\n", encoding="utf-8")
        _, cached_s2 = load_or_build_spine(spine_docx, paper_dir=paper_mem, cache_file=cache_p)
        require(any("C2" in c for c in cached_s2["external_memory"]["paper_claims"]), "spine cache did not invalidate on .paper/claims.yml update")
        tests.append("build_context_envelope OOXML custom headings, oMath, w:tbl, References cut, and .paper fusion")

        # 36. LaTeX \input{} recursive root-relative expansion and bibliography truncation
        tex_subdir = root / "tex_sections"
        tex_subdir.mkdir(exist_ok=True)
        (tex_subdir / "nested_sub.tex").write_text("Equation (1) holds $N = 500$ fixed.\n", encoding="utf-8")
        sub_tex = tex_subdir / "methods_sub.tex"
        sub_tex.write_text("Bootstrap uses 2,000 resamples across $N = 500$ households.\n\\input{tex_sections/nested_sub}\n", encoding="utf-8")
        main_tex_env = root / "env_main.tex"
        main_tex_env.write_text(
            "\\documentclass{article}\\begin{document}\n"
            "\\title{LaTeX Spine Test}\n"
            "\\section{Introduction}\nRQ1: How do policies shift losses?\n"
            "\\section{Methods}\n\\input{tex_sections/methods_sub}\n"
            "\\section{Results}\nLosses dropped by 12.4\\%.\n"
            "\\begin{thebibliography}{9}\n\\bibitem{k} Ignored reference 88.8\\%.\n\\end{thebibliography}\n"
            "\\end{document}\n",
            encoding="utf-8",
        )
        t_blocks, t_spine = load_or_build_spine(main_tex_env)
        require(any("2,000 resamples" in m for m in t_spine["methods_and_identification_locks"]), "LaTeX \\input expansion missed methods lock")
        require(any("Equation (1)" in m for m in t_spine["methods_and_identification_locks"]), "LaTeX root-relative nested \\input missed")
        require(not any("88.8" in b["text"] for b in t_blocks), "LaTeX thebibliography leaked into blocks")
        tests.append("build_context_envelope LaTeX \\input expansion and bibliography truncation")

        # 37. verify_delegate_numbers strict_preservation and curated_salience (provenance, sign, Mode R partition, downstream orphan)
        strict_ok = verify_strict_preservation(
            "Direction accuracy changed by -2.4% across N = 1,400 respondents (r = 0.42, p = 1.2e-4).",
            "Across N = 1,400 respondents (r = .42, p = 1.2E-04), direction accuracy showed a 2.4% decrease.",
        )
        require(strict_ok["status"] == "PASS", f"strict_preservation rejected valid sign-verb/APA/scientific equivalence: {strict_ok}")
        strict_parenthetical_dec = verify_strict_preservation(
            "Gap was -0.14 (baseline 0.50, SD 0.05).",
            "Compared with 0.50, gap was 0.14 (a 0.05 reduction).",
        )
        require(strict_parenthetical_dec["status"] == "PASS", f"decimal inside parenthetical prematurely cut polarity window: {strict_parenthetical_dec}")
        for bad_before, bad_after, label in [
            ("Direction accuracy changed by -2.4%.", "Direction accuracy showed a 2.4% increase.", "sign flip"),
            ("Mean was 10.18 (N = 100).", "Mean was 90.18 (N = 900).", "leading-digit mutation"),
            ("Effect was p = 1.2e-4.", "Effect was p = 9.9e-4.", "scientific notation mantissa mutation"),
            ("Sample was N = 42.", "Correlation was r = .42.", "integer vs APA leading-dot decimal"),
            ("Wave 1 was 0.61 and Delta was -1.9% (Rumination -3.8%).", "Rumination fell by -3.8%.", "mixed unsigned+signed missing sort"),
        ]:
            res_bad = verify_strict_preservation(bad_before, bad_after)
            require(res_bad["status"] == "FAIL", f"strict_preservation failed to reject {label}: {res_bad}")

        # Unsigned-positive standard tables: truthful opposite-sign subscales pass; 0.25 -> -0.25 and swapped signs fail; quoted CSV parses intact
        unsigned_opp_src = "| Subscale | Delta |\n| Rumination | 0.14 |\n| Worry | -0.14 |"
        require(
            verify_curated_salience(
                after_text="Rumination increased by 0.14, whereas Worry decreased by 0.14.",
                source_texts=[unsigned_opp_src],
            )["status"] == "PASS",
            "curated_salience falsely flagged truthful unsigned-positive + signed-negative same-magnitude subscales",
        )
        require(
            verify_curated_salience(
                after_text="Rumination decreased by -0.25.",
                source_texts=["| Subscale | Beta |\n| Rumination | 0.25 |"],
            )["status"] == "FAIL",
            "curated_salience missed unsigned-positive 0.25 -> -0.25 sign flip",
        )
        swapped_opp = verify_curated_salience(
            after_text="Rumination decreased by -0.14, whereas Worry increased by 0.14.",
            source_texts=[unsigned_opp_src],
        )
        require(
            len([f for f in swapped_opp["findings"] if f["code"] == "ENTITY_SIGN_REVERSAL"]) == 2,
            f"curated_salience missed one side of swapped unsigned 0.14 / -0.14 subscales: {swapped_opp}",
        )
        quoted_csv_res = verify_curated_salience(
            after_text="Worry, anxious decreased by -14 (p = 1.2e-4).",
            source_texts=['"Rumination, brooding",-14,1.2e-4\n"Worry, anxious",14,-3.5e-4'],
        )
        require(
            quoted_csv_res["status"] == "FAIL" and any(f["code"] == "ENTITY_SIGN_REVERSAL" for f in quoted_csv_res["findings"]),
            f"curated_salience missed sign reversal on quoted-comma CSV integer row: {quoted_csv_res}",
        )

        salience_bad = verify_curated_salience(
            after_text="Across 2,000 generative runs, Rumination direction agreement rose by +3.8% and 0.999.",
            source_texts=[env_txt],
            before_text="Table 1 shows Tension shifted by -1.9% and Rumination shifted by -3.8% (0.052 MAE gain).",
            declared_omitted_to_display=[],
            downstream_dependencies=env_meta["downstream_dependencies"],
            cross_section_sync_alerts=[],
        )
        bad_codes = {f["code"] for f in salience_bad["findings"]}
        require(
            {"UNVERIFIED_NUMBER_IN_PROSE", "POPULATION_INTEGER_DRIFT", "ENTITY_SIGN_REVERSAL", "UNDECLARED_OMITTED_NUMBER"} <= bad_codes,
            f"curated_salience missed expected failure codes: {bad_codes}",
        )
        contrast_flip = verify_curated_salience(
            after_text="Whereas Tension decreased by 12%, Rumination increased by 0.18.",
            source_texts=["| Subscale | Delta |\n| Tension | -12% |\n| Rumination | -0.18 |"],
            before_text="Rumination increased by +0.18.",
        )
        require(
            contrast_flip["status"] == "FAIL" and any(f["code"] == "ENTITY_SIGN_REVERSAL" for f in contrast_flip["findings"]),
            f"curated_salience missed multi-clause contrast sign reversal / before_text sign pollution: {contrast_flip}",
        )

        # Orphan check: pruning Rumination / -3.8% without item-specific cross_section_sync_alerts fails (blanket 'Discussion' alert is insufficient)
        orphan_unack = verify_curated_salience(
            after_text="Table 1 shows Tension shifted by -1.9% while overall error improved by 0.052.",
            source_texts=[env_txt],
            before_text="Table 1 shows Tension shifted by -1.9% and Rumination shifted by -3.8% (0.052 MAE gain).",
            declared_omitted_to_display=[{"value_or_entity": "Rumination -3.8%", "display_ref": "Table 1", "rationale_tier": "routine_conforming_subscale"}],
            downstream_dependencies=env_meta["downstream_dependencies"],
            cross_section_sync_alerts=[{"affected_section": "Discussion", "severity_class": "Class B", "issue": "Update unrelated 0.052 wording"}],
        )
        require(
            any(f["code"] == "UNACKNOWLEDGED_DOWNSTREAM_ORPHAN" for f in orphan_unack["findings"]),
            f"missed unacknowledged downstream orphan under blanket section alert: {orphan_unack}",
        )
        orphan_ack = verify_curated_salience(
            after_text="Table 1 shows Rumination error improved by 0.052 but direction accuracy fell by -3.8%, while routine subscales matched the index (Table 1).",
            source_texts=[env_txt],
            before_text="Table 1 shows Tension shifted by -1.9% and Rumination shifted by -3.8% (0.052 MAE gain).",
            declared_omitted_to_display=[{"value_or_entity": "Tension -1.9%", "display_ref": "Table 1", "rationale_tier": "routine_conforming_subscale"}],
            downstream_dependencies=env_meta["downstream_dependencies"],
            cross_section_sync_alerts=[],
        )
        require(orphan_ack["status"] == "PASS", f"curated_salience rejected valid Mode R selective prune: {orphan_ack}")
        tests.append("verify_delegate_numbers strict_preservation, entity-sign provenance, Mode R partition, and downstream orphan gate")

        # 38. run_scoped_manuscript_pass multi-backend assembly, silent print_timeout trap, proofread CI exemption, and <=200-word receipt
        spaced_dir = root / "dir with spaces"
        spaced_dir.mkdir(exist_ok=True)
        for backend_name, extra_kw, expected_tok in [
            ("agy", {"resume_id": "conv-123", "model": "gemini-2.5-pro"}, "--resume"),
            ("codex", {"resume_id": "sess-456"}, 'sandbox_mode="read-only"'),
            ("claude", {"resume_id": "cl-789"}, "--json-schema"),
            ("command", {"cmd_template": 'custom-cli --in "{prompt_file}" --out "{output_file}"'}, str(spaced_dir / "p.txt")),
        ]:
            built_cmd, _ = assemble_backend_command(
                backend=backend_name,
                prompt_file=spaced_dir / "p.txt",
                schema_file=spaced_dir / "s.json",
                raw_output_file=spaced_dir / "o.json",
                spine_file=spaced_dir / "sp.json",
                **extra_kw,
            )
            require(expected_tok in built_cmd, f"backend {backend_name} command missing {expected_tok}: {built_cmd}")

        proofread_4ci = (
            "Figure 4a reports shifts of +0.015 (95% CI [+0.006, +0.024]), +0.019 (95% CI [+0.009, +0.029]), "
            "+0.009 (95% CI [+0.002, +0.016]), and +0.004 (95% CI [-0.002, +0.010]), bounding RQ3."
        )
        proofread_eval = evaluate_delegate_reply(
            reply_obj={
                "revised_target_prose": proofread_4ci,
                "declared_omitted_to_display": [],
                "cross_section_sync_alerts": [],
                "unverified_context_locks": [],
            },
            before_text=proofread_4ci,
            spine={},
            envelope_meta={},
            envelope_text=proofread_4ci,
            companion_paths=[],
            state_path=None,
            verification_mode="strict_preservation",
            mode="proofread",
        )
        require(proofread_eval["status"] == "PASS", f"proofread strict_preservation deadlocked on PROSE018: {proofread_eval}")

        caught_silent_timeout = False
        try:
            parse_backend_output(
                backend="agy",
                returncode=0,
                stdout_text='{"status":"SUCCESS","response":"","finished_reason":"print_timeout"}\n',
                stderr_text="",
            )
        except BackendExecutionError as exc:
            caught_silent_timeout = exc.exit_code == 124 and exc.code == "SILENT_TIMEOUT_OR_TRUNCATION"
        require(caught_silent_timeout, "agy silent print_timeout with exit 0 was not intercepted as exit 124")

        caught_multiline_timeout = False
        try:
            parse_backend_output(
                backend="agy",
                returncode=0,
                stdout_text='{\n  "status": "SUCCESS",\n  "response": "",\n  "finished_reason": "print_timeout"\n}',
                stderr_text="",
            )
        except BackendExecutionError as exc:
            caught_multiline_timeout = exc.exit_code == 124 and exc.code == "SILENT_TIMEOUT_OR_TRUNCATION"
        require(caught_multiline_timeout, "agy multi-line --agy-format json print_timeout bypassed guard")

        pretty_unwrapped = parse_backend_output(
            backend="agy",
            returncode=0,
            stdout_text=json.dumps(
                {
                    "status": "SUCCESS",
                    "structured_output": {
                        "revised_target_prose": "Clean unwrapped prose.",
                        "declared_omitted_to_display": [],
                        "cross_section_sync_alerts": [],
                        "unverified_context_locks": [],
                    },
                    "finished_reason": "stop",
                },
                indent=2,
            ),
            stderr_text="",
        )
        require(pretty_unwrapped.get("revised_target_prose") == "Clean unwrapped prose.", f"agy multi-line JSON failed to unwrap structured_output: {pretty_unwrapped}")

        emb_md = root / "embedded_table_sec.md"
        emb_md.write_text(
            "# Study\n\n## 4. Results\n\n### 4.2 Subscales\n\n"
            "Table 1 shows Rumination fell by -3.8% while Tension matched the index.\n\n"
            "| Subscale | Wave1 | Wave2 | Delta |\n|---|---|---|---|\n"
            "| Rumination | 0.61 | 0.57 | -3.8% |\n| Tension | 0.44 | 0.43 | -1.9% |\n",
            encoding="utf-8",
        )
        emb_reply = root / "emb_reply.json"
        emb_reply.write_text(
            json.dumps({
                "revised_target_prose": "Table 1 shows Rumination fell by -3.8% while Tension matched the index.",
                "declared_omitted_to_display": [],
                "cross_section_sync_alerts": [],
                "unverified_context_locks": [],
            }),
            encoding="utf-8",
        )
        with contextlib.redirect_stdout(io.StringIO()):
            rc_emb = run_scoped_pass_main([
                "--manuscript", str(emb_md),
                "--target", "4.2",
                "--mode", "proofread",
                "--backend", "envelope-only",
                "--verify-reply", str(emb_reply),
                "--workdir", str(root / "emb_work"),
                "--json",
            ])
        require(rc_emb == 0, "embedded table inside target subsection polluted proofread before_text")

        pass_workdir = root / "pass_work"
        with contextlib.redirect_stdout(io.StringIO()):
            rc_prep = run_scoped_pass_main([
                "--manuscript", str(spine_docx),
                "--target", "4.2",
                "--backend", "envelope-only",
                "--workdir", str(pass_workdir),
                "--json",
            ])
        require(rc_prep == 0 and (pass_workdir / "context_envelope.txt").is_file(), "envelope-only preparation failed")
        valid_reply_file = root / "valid_delegate_reply.json"
        valid_reply_file.write_text(
            json.dumps({
                "revised_target_prose": "To test RQ1 on self-reported distress scores, Table 1 shows Rumination MAE improved by 0.052 under the bundled Memory condition whereas direction accuracy fell by -3.8%, while Tension followed the index pattern (Table 1).",
                "declared_omitted_to_display": [
                    {"value_or_entity": "Tension -1.9%", "display_ref": "Table 1", "rationale_tier": "routine_conforming_subscale"}
                ],
                "cross_section_sync_alerts": [],
                "unverified_context_locks": [],
            }),
            encoding="utf-8",
        )
        with contextlib.redirect_stdout(io.StringIO()):
            rc_ver = run_scoped_pass_main([
                "--manuscript", str(spine_docx),
                "--target", "4.2",
                "--backend", "envelope-only",
                "--verify-reply", str(valid_reply_file),
                "--workdir", str(pass_workdir),
                "--json",
            ])
        receipt_data = json.loads((pass_workdir / "pass_receipt.json").read_text(encoding="utf-8"))
        require(
            rc_ver == 0 and receipt_data["status"] == "PASS" and receipt_data["summary_words"] <= 200 and receipt_data["task_packet_tokens"] <= 4500,
            f"envelope-only verify-reply receipt failed constraints: rc={rc_ver}, receipt={receipt_data}",
        )
        tests.append("run_scoped_manuscript_pass 5-backend assembly, silent print_timeout trap, and <=200-word receipt")

        # 39. Round-3 security, provenance, negation, OOXML/LaTeX/Markdown, and fail-closed edge cases (C1-C6)
        # C1.1: unary en-dash vs range hyphen/en-dash + PROSE018 en-dash interval sign detection
        range_toks = extract_numeric_tokens("Rates spanned 5%-8% and 5%\u20138%, whereas Tension shifted by \u20133.8% ([\u20135.2%, \u20132.4%], \u2013$40K, \u2013.09).")
        range_pairs = [(t["sign"], t["magnitude"]) for t in range_toks]
        require(
            range_pairs.count((None, "5%")) == 2
            and range_pairs.count((None, "8%")) == 2
            and ("-", "8%") not in range_pairs
            and ("-", "3.8%") in range_pairs
            and ("-", "5.2%") in range_pairs
            and ("-", "$40K") in range_pairs
            and ("-", "0.09") in range_pairs,
            f"C1.1 unary en-dash / range parsing mismatch: {range_pairs}",
        )
        endash_ci_wall = (
            "Figure 5 compares integer intervals of [\u20135%, +2%], [\u20133%, +1%], [\u20134%, +2%], and [\u20136%, \u20131%], "
            "summarizing subgroup uncertainty."
        )
        require(
            any(f["code"] == "PROSE018" for f in audit_prose_text(endash_ci_wall, "endash_ci", {})),
            "C1.1 PROSE018 missed 4-bracket unary en-dash interval wall",
        )

        # C1.2 & C3: neutral sign-drop reversal, magnitude exemption, non-negative/non-positive, and negated polarity cues
        neutral_drop = verify_curated_salience(
            after_text="Rumination had a mean change of 3.8%.",
            source_texts=["| Subscale | Delta |\n| Rumination | -3.8% |"],
        )
        require(
            neutral_drop["status"] == "FAIL" and any(f["code"] == "ENTITY_SIGN_REVERSAL" for f in neutral_drop["findings"]),
            f"C1.2 missed neutral unsigned drop on negative source value: {neutral_drop}",
        )
        abs_ok = verify_curated_salience(
            after_text="Rumination had an absolute change of 3.8%.",
            source_texts=["| Subscale | Delta |\n| Rumination | -3.8% |"],
        )
        require(abs_ok["status"] == "PASS", f"C1.2 falsely flagged absolute-magnitude phrasing: {abs_ok}")

        non_neg_toks = extract_numeric_tokens("Weights remained non-negative at 0.25 and non-positive at -0.10.")
        require(non_neg_toks[0]["polarity"] == "neutral", f"C3 misclassified 'non-negative' as negative: {non_neg_toks}")
        negated_decrease = verify_curated_salience(
            after_text="Rumination did not decrease by 3.8% and failed to reduce error by 0.12.",
            source_texts=["| Subscale | Delta | Err |\n| Rumination | -3.8% | -0.12 |"],
        )
        require(
            negated_decrease["status"] == "FAIL" and any(f["code"] == "ENTITY_SIGN_REVERSAL" for f in negated_decrease["findings"]),
            f"C3 negated 'did not decrease' falsely satisfied negative polarity: {negated_decrease}",
        )
        rather_than_ok = verify_curated_salience(
            after_text="Rumination decreased by 3.8% rather than increasing.",
            source_texts=["| Subscale | Delta |\n| Rumination | -3.8% |"],
        )
        require(rather_than_ok["status"] == "PASS", f"C3 'decreased rather than increasing' failed polarity check: {rather_than_ok}")

        # C1.3: EMPTY_CANDIDATE_PROSE and verify_delegate_numbers CLI validation
        empty_strict = verify_strict_preservation("Qualitative sentence without numbers.", "   ")
        empty_salience = verify_curated_salience("", source_texts=["| A | 0.5 |"])
        require(
            empty_strict["status"] == "FAIL"
            and any(f["code"] == "EMPTY_CANDIDATE_PROSE" for f in empty_strict["findings"])
            and empty_salience["status"] == "FAIL"
            and any(f["code"] == "EMPTY_CANDIDATE_PROSE" for f in empty_salience["findings"]),
            "C1.3 failed to reject empty candidate prose",
        )
        bad_reply_list = root / "bad_reply_list.json"
        bad_reply_list.write_text("[]", encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()):
            rc_list_reply = verify_numbers_main(["--reply-json", str(bad_reply_list)])
        require(rc_list_reply == 2, f"C1.3 non-dict --reply-json should exit 2, got {rc_list_reply}")
        null_lists_reply = root / "null_lists_reply.json"
        null_lists_reply.write_text(
            json.dumps({
                "revised_target_prose": "Outcome held at 0.50.",
                "declared_omitted_to_display": None,
                "cross_section_sync_alerts": None,
            }),
            encoding="utf-8",
        )
        src_half = root / "src_half.md"
        src_half.write_text("| Metric | Val |\n| Outcome | 0.50 |\n", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            rc_null_lists = verify_numbers_main(["--reply-json", str(null_lists_reply), "--source", str(src_half), "--json"])
        require(rc_null_lists == 0, f"C1.3 nullable list fields crashed verify_delegate_numbers: {rc_null_lists}")

        # C2a: >12-row cited table outside target_indices + [Txx] label cell prefix stripping
        rows_16 = "\n".join(f"| SubgroupR{idx:02d} | -0.{idx + 10:02d} |" for idx in range(1, 17))
        long_tbl_md = root / "long_table_outside.md"
        long_tbl_md.write_text(
            "# Study Title\n\n## 4. Results\n\n### 4.2 Focal Contrasts\n\n"
            "Table 1 shows SubgroupR15 fell by -0.25.\n\n"
            "## Tables\n\nTable 1. Full 16-row subgroup matrix.\n\n"
            f"| Subgroup | Shift |\n|---|---|\n{rows_16}\n",
            encoding="utf-8",
        )
        long_work = root / "long_tbl_work"
        long_ok_reply = root / "long_ok_reply.json"
        long_ok_reply.write_text(
            json.dumps({
                "revised_target_prose": "Table 1 shows SubgroupR15 decreased by 0.25 across the cohort, bounding subgroup drift.",
                "declared_omitted_to_display": [],
                "cross_section_sync_alerts": [],
                "unverified_context_locks": [],
            }),
            encoding="utf-8",
        )
        with contextlib.redirect_stdout(io.StringIO()):
            rc_long_ok = run_scoped_pass_main([
                "--manuscript", str(long_tbl_md),
                "--target", "4.2",
                "--backend", "envelope-only",
                "--verify-reply", str(long_ok_reply),
                "--workdir", str(long_work),
                "--json",
            ])
            rc_long_cli = verify_numbers_main([
                "--reply-json", str(long_ok_reply),
                "--spine", str(long_work / "spine.json"),
                "--json",
            ])
        require(rc_long_ok == 0 and rc_long_cli == 0, f"C2a >12-row external cited table failed provenance: {rc_long_ok}, {rc_long_cli}")
        prefix_row_flip = verify_curated_salience(
            after_text="SubgroupR01 increased by 0.11.",
            source_texts=["[T01] SubgroupR01 | -0.11"],
        )
        require(
            prefix_row_flip["status"] == "FAIL" and any(f["code"] == "ENTITY_SIGN_REVERSAL" for f in prefix_row_flip["findings"]),
            f"C2a [T01] block prefix broke entity label matching: {prefix_row_flip}",
        )

        # C2b: fail closed (exit 2) on missing --source, --spine, --state, --companion, explicit paper_dir, or malformed state JSON
        bad_state = root / "malformed_state.json"
        bad_state.write_text("{broken json", encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()):
            require(verify_numbers_main(["--after", str(src_half), "--source", str(root / "nope.csv")]) == 2, "C2b missing --source did not exit 2")
            require(verify_numbers_main(["--after", str(src_half), "--spine", str(root / "nope_spine.json")]) == 2, "C2b missing --spine did not exit 2")
            require(build_env_main([str(long_tbl_md), "--companion", str(root / "nope.csv")]) == 2, "C2b missing --companion did not exit 2")
            require(build_env_main([str(long_tbl_md), "--state", str(root / "nope_state.json")]) == 2, "C2b missing --state did not exit 2")
            require(build_env_main([str(long_tbl_md), "--state", str(bad_state)]) == 2, "C2b malformed --state JSON did not exit 2")
            require(build_env_main([str(long_tbl_md), "--paper-dir", str(root / "nope_paper_dir")]) == 2, "C2b missing explicit --paper-dir did not exit 2")

        # C4: CLI identifier validation, Windows --flag="..." quote stripping, and Windows .cmd/.bat injection guard + codex.js resolution
        for bad_kw in (
            {"model": "--inject-flag"},
            {"model": "bad model space"},
            {"resume_id": "-o/tmp/pwn"},
            {"timeout_seconds": 0},
        ):
            caught_c4 = False
            try:
                assemble_backend_command(
                    backend="agy",
                    prompt_file=spaced_dir / "p.txt",
                    schema_file=spaced_dir / "s.json",
                    raw_output_file=spaced_dir / "o.json",
                    spine_file=spaced_dir / "sp.json",
                    **bad_kw,
                )
            except ValueError:
                caught_c4 = True
            require(caught_c4, f"C4 failed to reject invalid CLI parameter {bad_kw}")

        win_flag_cmd, win_stdin = assemble_backend_command(
            backend="command",
            prompt_file=spaced_dir / "p.txt",
            schema_file=spaced_dir / "s.json",
            raw_output_file=spaced_dir / "o.json",
            spine_file=spaced_dir / "sp.json",
            cmd_template='runner.exe --prompt="{prompt_file}" --out="{output_file}"',
            use_posix=False,
        )
        require(
            not win_stdin and win_flag_cmd[1] == f"--prompt={spaced_dir / 'p.txt'}" and '"' not in win_flag_cmd[1],
            f"C4.3 Windows --flag=\"...\" quote strip failed: {win_flag_cmd}",
        )
        fake_bat = root / "wrapper.cmd"
        fake_bat.write_text("@echo off\r\n", encoding="utf-8")
        caught_batch_meta = False
        try:
            _prepare_windows_safe_exec_cmd([str(fake_bat), "safe", "bad&whoami"], resolved_exe=str(fake_bat), is_windows=True)
        except BackendExecutionError as exc:
            caught_batch_meta = exc.code == "UNSAFE_WINDOWS_BATCH_ARG" and exc.exit_code == 2
        require(caught_batch_meta, "C4.4 Windows .cmd metacharacter injection was not blocked")

        npm_dir = root / "fake_npm"
        codex_bin_dir = npm_dir / "node_modules" / "@openai" / "codex" / "bin"
        codex_bin_dir.mkdir(parents=True, exist_ok=True)
        fake_codex_cmd = npm_dir / "codex.CMD"
        fake_node_exe = npm_dir / "node.exe"
        fake_codex_js = codex_bin_dir / "codex.js"
        fake_codex_cmd.write_text("@echo off\r\n", encoding="utf-8")
        fake_node_exe.write_text("", encoding="utf-8")
        fake_codex_js.write_text("// stub\n", encoding="utf-8")
        resolved_codex_argv = _prepare_windows_safe_exec_cmd(
            ["codex", "exec", "resume", "-c", 'sandbox_mode="read-only"'],
            resolved_exe=str(fake_codex_cmd),
            is_windows=True,
        )
        require(
            resolved_codex_argv[:2] == [str(fake_node_exe), str(fake_codex_js)],
            f"C4.4 codex.CMD did not unwrap to node.exe + codex.js: {resolved_codex_argv}",
        )

        # C5: <w:del> inside <m:oMath>, <w:sdt> unwrapping, LaTeX preamble \title + abstract, fenced Markdown # References, corrupt .docx exit 2, and ultra_compact row cap
        sdt_math_docx = root / "sdt_math.docx"
        make_docx(
            sdt_math_docx,
            f'<w:sdt><w:sdtContent><w:p><w:r><w:t>Abstract inside SDT control.</w:t></w:r></w:p></w:sdtContent></w:sdt>'
            f'<w:p xmlns:m="{M_NS}"><m:oMath><m:r><m:t>Y = X</m:t></m:r>'
            f'<w:del><m:r><m:t> - 7777</m:t></m:r></w:del></m:oMath></w:p>',
        )
        sdt_blocks, _ = load_or_build_spine(sdt_math_docx)
        sdt_joined = " ".join(b["text"] for b in sdt_blocks)
        require(
            "Abstract inside SDT control." in sdt_joined and "Y = X" in sdt_joined and "7777" not in sdt_joined,
            f"C5.1 OOXML SDT unwrap or oMath <w:del> exclusion failed: {sdt_joined}",
        )

        preamble_tex = root / "preamble_title.tex"
        preamble_tex.write_text(
            "\\documentclass{elsarticle}\n"
            "\\title[Short]{Preamble Flood Adaptation Title}\n"
            "\\begin{abstract}Preamble abstract locks 42.5\\% uptake.\\end{abstract}\n"
            "\\begin{document}\n\\maketitle\n"
            "\\section{Results}\nUptake reached 42.5\\%.\n\\end{document}\n",
            encoding="utf-8",
        )
        _, pre_spine = load_or_build_spine(preamble_tex)
        require(
            pre_spine["title"] == "Preamble Flood Adaptation Title"
            and any("42.5%" in a for a in pre_spine["summary_claims_digest"]["abstract"]),
            f"C5.2 LaTeX preamble title/abstract extraction failed: {pre_spine}",
        )

        fenced_md, _ = extract_from_markdown(
            "# Study\n\n## 2. Methods\n\n```markdown\n# References\nPrompt template line\n```\n\n"
            "~~~\nReferences\n~~~\n\n## 3. Results\n\nRetained result 0.48.\n"
        )
        require(
            any("Retained result 0.48." in b["text"] for b in fenced_md),
            f"C5.3 fenced # References prematurely truncated Markdown manuscript: {fenced_md}",
        )

        bad_zip_docx = root / "corrupt.docx"
        bad_zip_docx.write_bytes(b"not a valid zip archive")
        missing_xml_docx = root / "missing_doc_xml.docx"
        with zipfile.ZipFile(missing_xml_docx, "w") as zf_bad:
            zf_bad.writestr("word/other.xml", "<root/>")
        with contextlib.redirect_stderr(io.StringIO()):
            require(build_env_main([str(bad_zip_docx)]) == 2, "C5.4 BadZipFile did not exit 2 in build_context_envelope")
            require(build_env_main([str(missing_xml_docx)]) == 2, "C5.4 missing word/document.xml KeyError did not exit 2")
            require(
                run_scoped_pass_main(["--manuscript", str(bad_zip_docx), "--target", "1", "--workdir", str(root / "bad_wd")]) == 2,
                "C5.4 BadZipFile did not exit 2 in run_scoped_manuscript_pass",
            )

        huge_rows = "\n".join(f"| ItemGroup_{idx:03d} | -0.{idx:03d} | +0.{idx + 1:03d} | [-0.99, +0.99] |" for idx in range(1, 121))
        huge_md, _ = extract_from_markdown(
            "# Huge Table Paper\n\n## 4. Results\n\n### 4.1 Overview\n\nTable 1 summarizes ItemGroup_115 (-0.115).\n\n"
            f"## Tables\n\nTable 1. Huge matrix.\n\n| Group | A | B | CI |\n|---|---|---|---|\n{huge_rows}\n"
        )
        huge_spine = load_or_build_spine.__globals__["build_architecture_spine"](huge_md, "sha_huge")
        huge_env, huge_meta = build_scoped_context_envelope(huge_md, huge_spine, target_locator="4.1", max_tokens=900)
        require(
            huge_meta["within_budget"]
            and huge_meta["est_tokens"] <= 900
            and "ItemGroup_115" in huge_meta["relevant_display_slices"]["Table 1"]
            and "more rows omitted for packet budget" in huge_env,
            f"C5.5 budget-trim fallback failed to cap Section 5 while preserving relevant_display_slices: {huge_meta}",
        )

        # C6: cross_section_sync_alerts non-empty string validation & _extract_json_object malformed brace fallback
        sync_schema_errs = validate_delegate_reply_schema({
            "revised_target_prose": "Valid prose.",
            "declared_omitted_to_display": [],
            "cross_section_sync_alerts": [{"affected_section": "   ", "severity_class": "Class B", "issue": 123}],
            "unverified_context_locks": [],
        })
        require(bool(sync_schema_errs), "C6 validate_delegate_reply_schema accepted blank/non-string cross_section_sync_alerts fields")
        caught_bad_braces = False
        try:
            _extract_json_object("Error wrapper: {not: valid json}")
        except BackendExecutionError as exc:
            caught_bad_braces = exc.code == "INVALID_BACKEND_JSON" and exc.exit_code == 2
        require(caught_bad_braces, "C6 _extract_json_object leaked JSONDecodeError instead of BackendExecutionError")

        # Additional adversarial edge-case regressions (scoped subtraction-flip, [Pxxx|Heading] pipe tags,
        # curly-apostrophe/numeric/double negations, back-matter caption preserve, nested LaTeX title, wide-cell cap, agy stream delta)
        scoped_subflip_bad = verify_curated_salience(
            after_text="Table 1 shows Insurance fell by -8.1% and Rumination had a mean direction change of 3.8%.",
            source_texts=[
                "Methods: Model skill is evaluated via RMSE error reduction.",
                "| Subscale | Delta |\n| Insurance | +8.1% |\n| Rumination | -3.8% |",
            ],
        )
        require(
            len([f for f in scoped_subflip_bad["findings"] if f["code"] == "ENTITY_SIGN_REVERSAL"]) == 2,
            f"Methods 'error reduction' globally bypassed unrelated ENTITY_SIGN_REVERSAL checks: {scoped_subflip_bad}",
        )
        scoped_subflip_ok = verify_curated_salience(
            after_text="Under MAE_Base - MAE_Memory, Rumination MAE improved by 0.052.",
            source_texts=[
                "Methods: Delta_MAE = MAE_Base - MAE_Memory defines error reduction.",
                "| Subscale | RawDiff |\n| Rumination | -0.052 |",
            ],
        )
        require(scoped_subflip_ok["status"] == "PASS", f"Legitimate local MAE subtraction flip failed: {scoped_subflip_ok}")

        pipe_prefix_ok = verify_curated_salience(
            after_text="Across N = 500 households and 3 saved repetitions, Rumination fell by -3.8%.",
            source_texts=[
                "- [P006|Model Setup] Baseline sample size is N = 500 households across 3 saved repetitions.",
                "[P043|Finance Module] Pk = minmaxGk - δk, 0, Lk (3)",
                "| Subscale | Delta |\n| Rumination | -3.8% |\n| Tension | -1.9% |",
            ],
        )
        require(pipe_prefix_ok["status"] == "PASS", f"[P006|Heading] pipe prefix or equation line caused false CROSS_ENTITY_NUMBER_SWAP: {pipe_prefix_ok}")
        real_swap_bad = verify_curated_salience(
            after_text="Tension fell by -3.8%.",
            source_texts=["| Subscale | Delta |\n| Rumination | -3.8% |\n| Tension | -1.9% |"],
        )
        require(
            real_swap_bad["status"] == "FAIL" and any(f["code"] == "CROSS_ENTITY_NUMBER_SWAP" for f in real_swap_bad["findings"]),
            f"Genuine cross-entity number swap (-3.8% attributed to Tension) was missed: {real_swap_bad}",
        )

        for neg_sentence in (
            "Rumination didn\u2019t decrease by 3.8%.",
            "Rumination cannot decrease by 3.8%.",
            "Rumination showed no 3.8% decrease.",
            "Rumination operated without a 3.8% drop.",
            "Rumination remained non-decreasing at 3.8%.",
        ):
            neg_res = verify_curated_salience(
                after_text=neg_sentence,
                source_texts=["| Subscale | Delta |\n| Rumination | -3.8% |"],
            )
            require(
                neg_res["status"] == "FAIL" and any(f["code"] == "ENTITY_SIGN_REVERSAL" for f in neg_res["findings"]),
                f"Negated cue bypassed polarity check for {neg_sentence!r}: {neg_res}",
            )
        for dbl_neg_sentence in (
            "Rumination was not without a 3.8% decrease.",
            "Rumination did not fail to decrease by 3.8%.",
        ):
            dbl_res = verify_curated_salience(
                after_text=dbl_neg_sentence,
                source_texts=["| Subscale | Delta |\n| Rumination | -3.8% |"],
            )
            require(dbl_res["status"] == "PASS", f"Double-negation cancellation failed for {dbl_neg_sentence!r}: {dbl_res}")

        late_cap_md, _ = extract_from_markdown(
            "# Title\n\n## 2. Methods\n\nTable 1. Parameter matrix.\n\n| Param | Val |\n|---|---|\n| Alpha | 0.500 |\n\n"
            "## Tables\n\nTable 1. Parameter matrix.\n"
        )
        late_cap_spine = load_or_build_spine.__globals__["build_architecture_spine"](late_cap_md, "sha_late")
        require(
            "0.500" in late_cap_spine["display_inventory"]["Table 1"],
            f"Back-matter caption overwrote [T01] table rows in display_inventory: {late_cap_spine['display_inventory']}",
        )

        deep_tex = root / "deep_title.tex"
        deep_tex.write_text(
            "\\documentclass{article}\n"
            "\\title{Coupled \\textbf{Human \\emph{Flood}} Modeling\\\\ Across Basins\\thanks{Grant 99999}}\n"
            "\\begin{document}\n\\section{Results}\nUptake rose by 4.2\\%.\n\\end{document}\n",
            encoding="utf-8",
        )
        _, deep_spine = load_or_build_spine(deep_tex)
        require(
            deep_spine["title"] == "Coupled Human Flood Modeling Across Basins" and "99999" not in deep_spine["title"],
            f"Nested LaTeX \\title / \\thanks cleanup failed: {deep_spine['title']!r}",
        )

        inline_bt_md, _ = extract_from_markdown(
            "# Study\n\n```inline_code``` starts this paragraph.\n\n## References\n\nSmith (2024) 99.9%.\n"
        )
        require(
            not any("99.9%" in b["text"] for b in inline_bt_md),
            f"Single-line triple-backtick span swallowed References heading: {inline_bt_md}",
        )

        wide_cell = "Prompt text " * 350
        wide_md, _ = extract_from_markdown(
            "# Wide Prompt Table\n\n## 3. Methods\n\nTable 1 lists the persona prompt (N = 400).\n\n"
            f"Table 1. Prompt template.\n\n| Kind | Template |\n|---|---|\n| Persona | {wide_cell} |\n"
        )
        wide_spine = load_or_build_spine.__globals__["build_architecture_spine"](wide_md, "sha_wide")
        _, wide_meta = build_scoped_context_envelope(wide_md, wide_spine, target_locator="3. Methods", max_tokens=900)
        require(
            wide_meta["within_budget"] and wide_meta["est_tokens"] <= 900,
            f"Wide 2-row prompt table exceeded max_tokens despite char-cap fallback: {wide_meta}",
        )

        with contextlib.redirect_stderr(io.StringIO()):
            require(
                build_env_main([str(long_tbl_md), "--max-tokens", "0"]) == 2,
                "build_context_envelope --max-tokens 0 without --target did not exit 2",
            )

        stream_delta_out = parse_backend_output(
            backend="agy",
            returncode=0,
            stdout_text=(
                '{"delta":"{\\"revised_target_prose\\":\\"Streamed prose.\\",\\"declared_omitted_to_display\\":[],'
                '\\"cross_section_sync_alerts\\":[],\\"unverified_context_locks\\":[]}"}\n'
                '{"status":"SUCCESS","response":"","finished_reason":"stop"}\n'
            ),
            stderr_text="",
        )
        require(
            stream_delta_out.get("revised_target_prose") == "Streamed prose.",
            f"Trailing empty response field wiped agy stream-json delta payload: {stream_delta_out}",
        )

        claude_cli_dir = npm_dir / "node_modules" / "@anthropic-ai" / "claude-code"
        claude_cli_dir.mkdir(parents=True, exist_ok=True)
        fake_claude_cmd = npm_dir / "claude.CMD"
        fake_claude_js = claude_cli_dir / "cli.js"
        fake_claude_cmd.write_text("@echo off\r\n", encoding="utf-8")
        fake_claude_js.write_text("// stub\n", encoding="utf-8")
        resolved_claude_argv = _prepare_windows_safe_exec_cmd(
            ["claude", "-p", "--output-format", "json"],
            resolved_exe=str(fake_claude_cmd),
            is_windows=True,
        )
        require(
            resolved_claude_argv[:2] == [str(fake_node_exe), str(fake_claude_js)],
            f"claude.CMD did not unwrap to node.exe + cli.js: {resolved_claude_argv}",
        )
        tests.append("Round-3 security, provenance, negation, OOXML/LaTeX/Markdown, and fail-closed regressions")

        # 40. Round-4 regressions (R3-D1..R3-D4)
        # R3-D1(1): verify_strict_preservation 1-for-1 (sign, magnitude, polarity) pool consumption + 4 reproducers
        r3_d1_c1 = verify_strict_preservation("Tension decreased by 3.8%.", "Tension increased by 3.8%.")
        require(
            r3_d1_c1["status"] == "FAIL" and any(f["code"] == "NUM_SIGN_FLIP" for f in r3_d1_c1["findings"]),
            f"R3-D1 Case 1 unsigned decreased->increased 3.8% failed to trigger NUM_SIGN_FLIP: {r3_d1_c1}",
        )
        r3_d1_c2 = verify_strict_preservation(
            "Baseline was 3.8%, and Rumination changed by -3.8%.",
            "Baseline was 3.8%, and Rumination decreased by 3.8%.",
        )
        require(r3_d1_c2["status"] == "PASS", f"R3-D1 Case 2 valid mixed neutral + sign-verb 3.8% failed: {r3_d1_c2}")
        r3_d1_c2_rev = verify_strict_preservation(
            "Across N = 1,400 respondents (r = .42, p = 1.2E-04), direction accuracy showed a 2.4% decrease.",
            "Direction accuracy changed by -2.4% across N = 1,400 respondents (r = 0.42, p = 1.2e-4).",
        )
        require(r3_d1_c2_rev["status"] == "PASS", f"R3-D1 reverse sign-verb with clause bystanders failed: {r3_d1_c2_rev}")
        r3_d1_c3 = verify_strict_preservation(
            "Tension decreased by 3.8%, and Rumination changed by -3.8%.",
            "Tension decreased by 3.8%, and Rumination increased by 3.8%.",
        )
        require(
            r3_d1_c3["status"] == "FAIL" and any(f["code"] == "NUM_SIGN_FLIP" for f in r3_d1_c3["findings"]),
            f"R3-D1 Case 3 double-counted common token and missed -3.8% -> increased 3.8%: {r3_d1_c3}",
        )
        r3_d1_c4 = verify_strict_preservation(
            "Tension decreased by 3.8%, and Rumination changed by -3.8%.",
            "Tension decreased by 3.8%, and Rumination had a mean change of 3.8%.",
        )
        require(
            r3_d1_c4["status"] == "FAIL"
            and any(f["code"] in {"NUM_SIGN_FLIP", "NUM_MISSING_IN_STRICT_MODE"} for f in r3_d1_c4["findings"]),
            f"R3-D1 Case 4 double-counted common token and missed -3.8% -> neutral 3.8% drop: {r3_d1_c4}",
        )
        r3_d1_mag_ok = verify_strict_preservation(
            "Baseline was 3.8%, and Rumination changed by -3.8%.",
            "Baseline was 3.8%, and Rumination had an absolute change of 3.8%.",
        )
        require(r3_d1_mag_ok["status"] == "PASS", f"R3-D1 valid MAGNITUDE_QUALIFIER_RE equivalence failed: {r3_d1_mag_ok}")
        r3_d1_mag_neg_bad = verify_strict_preservation(
            "Rumination changed by -3.8%.",
            "Rumination did not decrease in absolute terms by 3.8%.",
        )
        require(r3_d1_mag_neg_bad["status"] == "FAIL", f"R3-D1 negated absolute clause bypassed strict check: {r3_d1_mag_neg_bad}")
        r3_d1_sneak_verb = verify_strict_preservation(
            "Rumination changed by -2.4% and the other subscale averaged 3.8%.",
            "Rumination decreased by 2.4% and the other subscale decreased by 3.8%.",
        )
        require(r3_d1_sneak_verb["status"] == "FAIL", f"R3-D1 sneaky second directional verb in single clause bypassed strict check: {r3_d1_sneak_verb}")

        # R3-D1(2): verify_curated_salience catches unsigned positive_verb -> unsigned negative_verb reversal
        r3_d1_pos_to_neg_src = verify_curated_salience(
            after_text="Insurance uptake decreased by 8.1%.",
            source_texts=["Baseline Insurance uptake increased by 8.1%."],
        )
        r3_d1_pos_to_neg_before = verify_curated_salience(
            after_text="Insurance uptake decreased by 8.1%.",
            source_texts=[],
            before_text="Baseline Insurance uptake increased by 8.1%.",
        )
        require(
            r3_d1_pos_to_neg_src["status"] == "FAIL"
            and any(f["code"] == "ENTITY_SIGN_REVERSAL" and f.get("expected_sign") == "+" for f in r3_d1_pos_to_neg_src["findings"])
            and r3_d1_pos_to_neg_before["status"] == "FAIL"
            and any(f["code"] == "ENTITY_SIGN_REVERSAL" for f in r3_d1_pos_to_neg_before["findings"]),
            f"R3-D1(2) missed unsigned positive->negative verb reversal: {r3_d1_pos_to_neg_src}, {r3_d1_pos_to_neg_before}",
        )
        r3_d1_pos_mag_ok = verify_curated_salience(
            after_text="Across N = 500 households, Insurance uptake had an absolute change of 8.1% while Elevations decreased by 4.2%.",
            source_texts=["Across N = 500 households, Baseline Insurance uptake increased by 8.1% and Elevations fell by -4.2%."],
        )
        require(r3_d1_pos_mag_ok["status"] == "PASS", f"R3-D1(2) falsely flagged N = 500 or magnitude-qualified 8.1%: {r3_d1_pos_mag_ok}")

        # R3-D2: run_scoped_manuscript_pass main() guards non-list/null/non-str schema-invalid fields without TypeError
        for idx_bad, invalid_payload in enumerate([
            {
                "revised_target_prose": "Valid prose text.",
                "declared_omitted_to_display": None,
                "cross_section_sync_alerts": None,
                "unverified_context_locks": [],
            },
            {
                "revised_target_prose": None,
                "declared_omitted_to_display": 123,
                "cross_section_sync_alerts": True,
                "unverified_context_locks": 456,
            },
            [],
        ]):
            bad_rep_path = root / f"r3_d2_invalid_{idx_bad}.json"
            bad_rep_path.write_text(json.dumps(invalid_payload), encoding="utf-8")
            bad_wd = root / f"r3_d2_wd_{idx_bad}"
            bad_wd.mkdir(parents=True, exist_ok=True)
            (bad_wd / "revised_target_preview.md").write_text("stale preview\n", encoding="utf-8")
            buf_out = io.StringIO()
            with contextlib.redirect_stdout(buf_out):
                rc_d2 = run_scoped_pass_main([
                    "--manuscript", str(emb_md),
                    "--target", "4.2",
                    "--backend", "envelope-only",
                    "--verify-reply", str(bad_rep_path),
                    "--workdir", str(bad_wd),
                    "--json",
                ])
            d2_json = json.loads(buf_out.getvalue())
            require(
                rc_d2 == 1
                and d2_json["status"] == "FAIL"
                and "SCHEMA_INVALID" in d2_json["summary"]
                and (bad_wd / "pass_receipt.json").is_file()
                and not (bad_wd / "revised_target_preview.md").exists()
                and "revised_preview_md" not in d2_json["evidence_refs"],
                f"R3-D2 schema-invalid reply #{idx_bad} mishandled: rc={rc_d2}, out={d2_json}",
            )

        # R3-D3: build_context_envelope resets pending_table_caption across prose/headings and attaches bottom captions
        d3_leak_md, _ = extract_from_markdown(
            "# Leak Check\n\n## 2. Methods\n\nTable 1. External matrix caption only.\n\n"
            "Ordinary prose paragraph resets pending table caption.\n\n"
            "| Uncaptioned | Val |\n|---|---|\n| RowA | 0.11 |\n\n"
            "Closing methods paragraph separates T01 from the standalone caption below.\n\n"
            "Table 2. Caption before heading.\n\n## 3. Results\n\n"
            "| UncaptionedB | Val |\n|---|---|\n| RowB | 0.22 |\n"
        )
        d3_leak_spine = load_or_build_spine.__globals__["build_architecture_spine"](d3_leak_md, "sha_d3_leak")
        d3_tbl_blocks = [b for b in d3_leak_md if b["kind"] == "table"]
        require(
            d3_tbl_blocks[0]["display_key"] == "Table (T01)"
            and d3_tbl_blocks[1]["display_key"] == "Table (T02)"
            and "RowA" not in d3_leak_spine["display_inventory"]["Table 1"]
            and "RowB" not in d3_leak_spine["display_inventory"]["Table 2"],
            f"R3-D3(1) pending_table_caption leaked across prose or section heading: {d3_tbl_blocks}, {d3_leak_spine['display_inventory']}",
        )

        bottom_cap_tex = root / "bottom_cap.tex"
        bottom_cap_tex.write_text(
            "\\documentclass{article}\n\\begin{document}\n"
            "\\section{Results}\nTable 1 reports bottom-captioned Rumination shift of -3.8\\%.\n"
            "\\begin{table}[htbp]\n\\centering\n"
            "\\begin{tabular}{lc}\n\\hline\nOutcome & Delta \\\\\n\\hline\nRumination & -3.8\\% \\\\\n\\hline\n\\end{tabular}\n"
            "\\caption{Table 1: Bottom LaTeX table summary.}\n\\label{tab:one}\n\\end{table}\n"
            "\\begin{table}[htbp]\n\\begin{tabular}{lc}\nOther & 1.2\\% \\\\\n\\end{tabular}\n\\end{table}\n"
            "\\end{document}\n",
            encoding="utf-8",
        )
        b_tex_blocks, b_tex_spine = load_or_build_spine(bottom_cap_tex)
        b_tex_tables = [b for b in b_tex_blocks if b["kind"] == "table"]
        _, b_tex_meta = build_scoped_context_envelope(b_tex_blocks, b_tex_spine, target_locator="Results")
        require(
            len(b_tex_tables) == 2
            and b_tex_tables[0]["display_key"] == "Table 1"
            and b_tex_tables[1]["display_key"] == "Table (T02)"
            and "Table (T01)" not in b_tex_spine["display_inventory"]
            and "Bottom LaTeX table summary." in b_tex_spine["display_inventory"]["Table 1"]
            and "Rumination | -3.8%" in b_tex_meta["relevant_display_slices"]["Table 1"],
            f"R3-D3(2) bottom LaTeX caption attachment failed: {b_tex_tables}, {b_tex_spine['display_inventory']}",
        )

        # R3-D4: child .tex digest invalidates spine_cache + single-file .tex keeps raw sha256 + O(blocks) cache-hit annotation
        require(
            b_tex_spine["source_sha256"] == hashlib.sha256(bottom_cap_tex.read_bytes()).hexdigest(),
            "R3-D4(1) single-file .tex digest diverged from sha256(raw).hexdigest()",
        )
        tex_cache_file = root / "tex_child_spine_cache.json"
        _, t_spine_v1 = load_or_build_spine(main_tex_env, cache_file=tex_cache_file)
        sub_tex.write_text("Bootstrap uses 5,000 resamples across $N = 500$ households.\n\\input{tex_sections/nested_sub}\n", encoding="utf-8")
        _, t_spine_v2 = load_or_build_spine(main_tex_env, cache_file=tex_cache_file)
        require(
            t_spine_v2["source_sha256"] != t_spine_v1["source_sha256"]
            and any("5,000 resamples" in m for m in t_spine_v2["methods_and_identification_locks"]),
            f"R3-D4(1) editing child methods_sub.tex failed to invalidate spine_cache.json: {t_spine_v2}",
        )
        (tex_subdir / "nested_sub.tex").write_text("Equation (1) holds $N = 750$ fixed.\n", encoding="utf-8")
        fresh_blocks, t_spine_v3 = load_or_build_spine(main_tex_env, cache_file=tex_cache_file)
        require(
            t_spine_v3["source_sha256"] != t_spine_v2["source_sha256"]
            and any("N = 750" in m for m in t_spine_v3["methods_and_identification_locks"]),
            f"R3-D4(1) editing nested child .tex failed to invalidate spine_cache.json: {t_spine_v3}",
        )

        import build_context_envelope as _bce_mod

        orig_build_spine = _bce_mod.build_architecture_spine

        def _forbid_full_spine(*_a, **_kw):
            raise AssertionError("R3-D4(2) cache hit unexpectedly called full build_architecture_spine")

        _bce_mod.build_architecture_spine = _forbid_full_spine
        try:
            cached_blocks, cached_spine_hit = load_or_build_spine(main_tex_env, cache_file=tex_cache_file)
        finally:
            _bce_mod.build_architecture_spine = orig_build_spine
        require(
            cached_spine_hit["source_sha256"] == t_spine_v3["source_sha256"]
            and [(b.get("section_heading"), b.get("section_role"), b.get("display_key"), b.get("caption")) for b in cached_blocks]
            == [(b.get("section_heading"), b.get("section_role"), b.get("display_key"), b.get("caption")) for b in fresh_blocks],
            "R3-D4(2) cache-hit O(blocks) annotation did not match fresh block annotations",
        )

        # Round-4 adversarial review additions (comparator-tail polarity, cross-comma bystander swap,
        # structured-row unsigned verb polarity, falsy structured_output, adjacent T01+Table2+T02,
        # nested/unnumbered LaTeX \caption, companion .md table rows, dotted/repeated \input)
        require(
            verify_strict_preservation(
                "Tension decreased by 3.8% from the higher baseline.",
                "Tension increased by 3.8% from the lower baseline.",
            )["status"] == "FAIL",
            "Comparator-tail 'higher/lower baseline' cancelled governing strict-mode polarity flip",
        )
        require(
            verify_curated_salience(
                after_text="Insurance uptake decreased by 8.1% relative to the higher baseline.",
                source_texts=["Baseline Insurance uptake increased by 8.1%."],
            )["status"] == "FAIL",
            "Comparator-tail 'higher baseline' cancelled R3-D1(2) ENTITY_SIGN_REVERSAL",
        )
        require(
            verify_strict_preservation(
                "Across a 3.8% baseline, Rumination changed by -2.4%.",
                "Across a 2.4% baseline, Rumination decreased by 3.8%.",
            )["status"] == "FAIL"
            and verify_strict_preservation(
                "Rumination changed by -2.4% from the 3.8% baseline.",
                "Rumination decreased by 3.8% from the 2.4% baseline.",
            )["status"] == "FAIL",
            "Cross-comma or prepositional baseline swap bypassed verify_strict_preservation",
        )
        row_verb_swap = verify_curated_salience(
            after_text="Insurance decreased by 8.1%, whereas Rumination increased by 8.1%.",
            source_texts=["| Subscale | Change |\n| Insurance | increased by 8.1% |\n| Rumination | decreased by 8.1% |"],
        )
        require(
            row_verb_swap["status"] == "FAIL"
            and len([f for f in row_verb_swap["findings"] if f["code"] == "ENTITY_SIGN_REVERSAL"]) == 2,
            f"Unsigned directional verbs in structured rows missed sub-clause reversal: {row_verb_swap}",
        )
        require(
            parse_backend_output("agy", 0, '{"structured_output": {}, "finished_reason": "stop"}', "") == {}
            and parse_backend_output("agy", 0, '{"structured_output": [1], "finished_reason": "stop"}', "") == [1]
            and parse_backend_output("claude", 0, '{"structured_output": {}, "stop_reason": "end_turn"}', "") == {},
            "Empty/non-dict structured_output misclassified as timeout instead of schema-invalid payload",
        )
        adj_tbl_md, _ = extract_from_markdown(
            "# Study\n\n## Results\n\n| Uncap | V |\n|---|---|\n| A | 1.1 |\n\n"
            "Table 2. Actual second table caption.\n\n| Col | V |\n|---|---|\n| B | 2.2 |\n"
        )
        adj_tbl_spine = orig_build_spine(adj_tbl_md, "sha_adj")
        require(
            [(b["id"], b.get("display_key")) for b in adj_tbl_md if b["kind"] == "table"]
            == [("T01", "Table (T01)"), ("T02", "Table 2")]
            and "B | 2.2" in adj_tbl_spine["display_inventory"]["Table 2"],
            f"Adjacent uncaptioned T01 stole Table 2 top caption from T02: {adj_tbl_spine['display_inventory']}",
        )
        _, t01_only_meta = build_scoped_context_envelope(adj_tbl_md, adj_tbl_spine, target_locator="T02")
        require(
            "Actual second table caption." in t01_only_meta["relevant_display_slices"]["Table 2"],
            f"Embedded table target dropped attached caption in relevant_display_slices: {t01_only_meta}",
        )
        comp_sm_md = root / "companion_sm.md"
        comp_sm_md.write_text(
            "# Supplement\n\nTable S1. Full subscale breakdown.\n\n| Subscale | Delta |\n|---|---|\n| Avoidance | -4.5% |\n",
            encoding="utf-8",
        )
        comp_main_md = root / "companion_main.md"
        comp_main_md.write_text("# Main\n\n## Results\n\nAvoidance fell by -4.5% (Table S1).\n", encoding="utf-8")
        c_blocks, c_spine = load_or_build_spine(comp_main_md, companion_paths=[comp_sm_md])
        _, c_meta = build_scoped_context_envelope(c_blocks, c_spine, target_locator="Results")
        require(
            "Avoidance | -4.5%" in c_meta["relevant_display_slices"]["Table S1"],
            f"Companion Markdown table rows dropped for Table S1: {c_meta}",
        )
        adv_tex = root / "adv_captions_inputs.tex"
        (tex_subdir / "4.2_dotted.tex").write_text("Dotted section shift was +6.3\\%.\n", encoding="utf-8")
        (tex_subdir / "shared_snip.tex").write_text("Repeated macro phrase.\n", encoding="utf-8")
        adv_tex.write_text(
            "\\documentclass{article}\n\\begin{document}\n\\section{Results}\n"
            "See Table 1 (-3.8\\%) and Table 2 (+6.3\\%).\n"
            "\\input{tex_sections/4.2_dotted}\n\\input{tex_sections/shared_snip}\n\\input{tex_sections/shared_snip}\n"
            "\\begin{table}\\begin{tabular}{lc}Rumination & -3.8\\% \\\\\\end{tabular}"
            "\\caption{Unnumbered LaTeX table summary across \\textbf{all \\emph{three}} waves.}\\end{table}\n"
            "\\end{document}\n",
            encoding="utf-8",
        )
        adv_blocks, adv_spine = load_or_build_spine(adv_tex)
        adv_joined = " ".join(b["text"] for b in adv_blocks)
        _, adv_meta = build_scoped_context_envelope(adv_blocks, adv_spine, target_locator="Results")
        require(
            "+6.3%" in adv_joined
            and adv_joined.count("Repeated macro phrase.") == 2
            and "Unnumbered LaTeX table summary across all three waves." in adv_meta["relevant_display_slices"]["Table 1"],
            f"Nested/unnumbered LaTeX caption or dotted/repeated \\input failed: {adv_meta}",
        )

        # Round-5 regressions (R4-D1..R4-D3)
        # R4-D1 non-regressions: 'from/than baseline by 3.8%' and '(3.8%, p = .004)' / '(3.8%)' retain outer negative polarity
        for valid_neg_sentence, valid_src in [
            ("Losses decreased from baseline by 3.8%.", "| Metric | Delta |\n| Losses | -3.8% |"),
            ("Rumination was lower than baseline by 3.8%.", "| Subscale | Delta |\n| Rumination | -3.8% |"),
            ("Rumination decreased significantly (3.8%, p = .004).", "| Subscale | Delta | p |\n| Rumination | -3.8% | 0.004 |"),
            ("Across N = 1,400 respondents, Rumination decreased significantly (3.8%, p = .004).", "N = 1,400\n| Subscale | Delta | p |\n| Rumination | -3.8% | 0.004 |"),
            ("Rumination showed a steep reduction (3.8%) across waves.", "| Subscale | Delta |\n| Rumination | -3.8% |"),
            ("Rumination decreased across all three waves by 0.14 (Worry rose 0.14).", "| Subscale | Delta |\n| Rumination | -0.14 |\n| Worry | +0.14 |"),
            ("Rumination decreased by 0.14 compared with a 0.14 increase in Worry.", "| Subscale | Delta |\n| Rumination | -0.14 |\n| Worry | +0.14 |"),
        ]:
            r5_ok = verify_curated_salience(after_text=valid_neg_sentence, source_texts=[valid_src])
            require(r5_ok["status"] == "PASS", f"R4-D1 non-regression falsely failed on {valid_neg_sentence!r}: {r5_ok}")
        require(
            verify_strict_preservation(
                "Rumination changed by -3.8% (p = 0.004).",
                "Rumination decreased significantly (3.8%, p = .004).",
            )["status"] == "PASS",
            "R4-D1 strict_preservation falsely failed on '(3.8%, p = .004)'",
        )

        # R4-D1 catches: determiner+verb splitters, fronted/comparator/right boundaries, paren isolation, and attribution units
        r5_src_neg = "| Subscale | Delta |\n| Tension | -2.4% |\n| Rumination | -3.8% |"
        for leaked_sentence in [
            "Tension decreased by 2.4% and the control group averaged 3.8%.",
            "Despite a 2.4% drop in Tension, Rumination stabilized at 3.8%.",
            "In spite of a 2.4% drop in Tension, Rumination held at 3.8%.",
            "Compared to a 2.4% drop in Tension, Rumination averaged 3.8%.",
            "Rumination decreased from a baseline of 3.8%.",
            "Rumination was lower than the 3.8% benchmark.",
            "Rumination decreased vs. 3.8%.",
            "Tension decreased by 2.4 percentage points from 3.8%.",
            "Rumination averaged 3.8% before declining in Wave 3.",
            "Rumination held at 3.8% with lower variance.",
            "Under lower baseline scores, the Rumination mean of 3.8% remained stable.",
            "Rumination decreased (baseline 3.8%).",
            "Rumination decreased (3.8% at baseline).",
            "Rumination decreased (SD 3.8%).",
            "Tension decreased (3.8% for Rumination).",
        ]:
            r5_bad = verify_curated_salience(after_text=leaked_sentence, source_texts=[r5_src_neg])
            require(
                r5_bad["status"] == "FAIL" and any(f["code"] == "ENTITY_SIGN_REVERSAL" for f in r5_bad["findings"]),
                f"R4-D1 failed to catch polarity leak on {leaked_sentence!r}: {r5_bad}",
            )
        require(
            verify_strict_preservation(
                "Tension changed by -2.4% and the baseline control group held at 3.8%.",
                "Tension decreased by 2.4% and the baseline control group decreased by 3.8%.",
            )["status"] == "FAIL",
            "R4-D1 strict_preservation missed determiner-subject 'and the ... held' polarity leak",
        )

        for swap_prose in [
            "Rumination fell by -2.4% (Tension: -3.8%).",
            "Rumination fell by -2.4% [Tension: -3.8%].",
            "Rumination fell by -2.4% relative to -3.8% in Tension.",
            "Rumination fell by -2.4% vs. -3.8% in Tension.",
        ]:
            swap_res = verify_curated_salience(after_text=swap_prose, source_texts=[r5_src_neg])
            require(
                swap_res["status"] == "FAIL"
                and len([f for f in swap_res["findings"] if f["code"] == "CROSS_ENTITY_NUMBER_SWAP"]) == 2,
                f"R4-D1 attribution units missed dual CROSS_ENTITY_NUMBER_SWAP on {swap_prose!r}: {swap_res}",
            )
        for dual_flip_prose in [
            "Rumination increased by 0.14 (Worry: -0.14).",
            "Rumination increased by 0.14 (Worry decreased by 0.14, whereas Index fell by -2.0%).",
            "Index fell by -2.0% (Rumination increased by 0.14 [Worry: -0.14]).",
            "Rumination increased by 0.14 vs. a 0.14 drop in Worry.",
            "Rumination increased by 0.14 against -0.14 in Worry.",
        ]:
            dual_res = verify_curated_salience(
                after_text=dual_flip_prose,
                source_texts=["| Subscale | Delta |\n| Index | -2.0% |\n| Rumination | -0.14 |\n| Worry | +0.14 |"],
            )
            require(
                dual_res["status"] == "FAIL"
                and len([f for f in dual_res["findings"] if f["code"] == "ENTITY_SIGN_REVERSAL"]) == 2,
                f"R4-D1 attribution units missed dual ENTITY_SIGN_REVERSAL on {dual_flip_prose!r}: {dual_res}",
            )
        single_rel_flip = verify_curated_salience(
            after_text="Rumination increased by 0.14 relative to Worry.",
            source_texts=["| Subscale | Delta |\n| Rumination | -0.14 |\n| Worry | +0.14 |"],
        )
        require(
            single_rel_flip["status"] == "FAIL"
            and any(f["code"] == "ENTITY_SIGN_REVERSAL" for f in single_rel_flip["findings"]),
            f"R4-D1 missed ENTITY_SIGN_REVERSAL on 'Rumination increased by 0.14 relative to Worry': {single_rel_flip}",
        )

        # R4-D2: agy outer/trailing non-JSON "response" never overwrites structured_output (valid dict or {})
        valid_so = {
            "revised_target_prose": "Structured output preserved.",
            "declared_omitted_to_display": [],
            "cross_section_sync_alerts": [],
            "unverified_context_locks": [],
        }
        require(
            parse_backend_output(
                "agy",
                0,
                json.dumps({"status": "SUCCESS", "result": {"structured_output": valid_so}, "response": "Completed!", "finished_reason": "stop"}),
                "",
            ) == valid_so
            and parse_backend_output(
                "agy",
                0,
                json.dumps({"status": "SUCCESS", "result": {"structured_output": {}}, "response": "Completed!", "finished_reason": "stop"}),
                "",
            ) == {}
            and parse_backend_output(
                "agy",
                0,
                json.dumps({"structured_output": valid_so}) + "\n" + json.dumps({"status": "SUCCESS", "response": "Summary text", "finished_reason": "stop"}) + "\n",
                "",
            ) == valid_so
            and parse_backend_output(
                "agy",
                0,
                json.dumps({"structured_output": {}}) + "\n" + json.dumps({"status": "SUCCESS", "response": "Summary text", "finished_reason": "stop"}) + "\n",
                "",
            ) == {}
            and parse_backend_output(
                "agy",
                0,
                json.dumps({"structured_output": "", "response": "Summary text", "finished_reason": "stop"}),
                "",
            ) == "",
            "R4-D2 outer/trailing non-JSON response overwrote agy structured_output",
        )

        # R4-D3: .docx (<w:delText>, References, binary ZIP media) & .tex (% comments, \input, thebibliography) companion/source hygiene
        r4_d3_docx = root / "companion_hygiene.docx"
        with zipfile.ZipFile(r4_d3_docx, "w") as zf_d3:
            zf_d3.writestr(
                "word/document.xml",
                f'<w:document xmlns:w="{W}"><w:body>'
                '<w:p><w:r><w:t>Table S1. Companion subscale check.</w:t></w:r>'
                '<w:del><w:r><w:delText> 99.9% deleted draft</w:delText></w:r></w:del></w:p>'
                '<w:tbl><w:tr><w:tc><w:p><w:r><w:t>Subscale</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Delta</w:t></w:r></w:p></w:tc></w:tr>'
                '<w:tr><w:tc><w:p><w:r><w:t>Rumination</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>-3.8%</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
                '<w:p><w:r><w:t>References</w:t></w:r></w:p>'
                '<w:p><w:r><w:t>Doe (2024) 88.8% reference noise.</w:t></w:r></w:p>'
                '</w:body></w:document>',
            )
            zf_d3.writestr("word/media/image1.png", b"\x89PNG\r\n\x1a\n77.7% binary zip media payload")
        (tex_subdir / "d3_comp_child.tex").write_text("Expanded child supplement locks 5.4\\% uptake.\n", encoding="utf-8")
        r4_d3_tex = root / "companion_hygiene.tex"
        r4_d3_tex.write_text(
            "\\documentclass{article}\n\\begin{document}\n"
            "% Commented out 66.6% and Rumination | +3.8%\n"
            "\\section{Supplement}\n\\input{tex_sections/d3_comp_child}\n"
            "\\begin{thebibliography}{9}\n\\bibitem{z} Bib noise 55.5\\%.\n\\end{thebibliography}\n"
            "\\end{document}\n",
            encoding="utf-8",
        )
        d3_main_md = root / "d3_main.md"
        d3_main_md.write_text("# Main\n\n## 4. Results\n\nRumination fell by -3.8% with 5.4% uptake (Table S1).\n", encoding="utf-8")
        d3_good_reply = root / "d3_good_reply.json"
        d3_good_reply.write_text(
            json.dumps({
                "revised_target_prose": "Table S1 shows Rumination decreased by 3.8% while supplement uptake reached 5.4%.",
                "declared_omitted_to_display": [],
                "cross_section_sync_alerts": [],
                "unverified_context_locks": [],
            }),
            encoding="utf-8",
        )
        d3_bad_reply = root / "d3_bad_reply.json"
        d3_bad_reply.write_text(
            json.dumps({
                "revised_target_prose": "Table S1 shows Rumination increased by +3.8% with 99.9%, 88.8%, 77.7%, 66.6%, and 55.5%.",
                "declared_omitted_to_display": [{"value_or_entity": "5.4%", "display_ref": "Table S1", "rationale_tier": "other_display_archived"}],
                "cross_section_sync_alerts": [],
                "unverified_context_locks": [],
            }),
            encoding="utf-8",
        )
        d3_bad_buf = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()):
            rc_d3_good_v = verify_numbers_main([
                "--reply-json", str(d3_good_reply),
                "--source", str(r4_d3_docx), str(r4_d3_tex),
                "--json",
            ])
            rc_d3_good_r = run_scoped_pass_main([
                "--manuscript", str(d3_main_md),
                "--target", "4. Results",
                "--companion", str(r4_d3_docx), str(r4_d3_tex),
                "--backend", "envelope-only",
                "--verify-reply", str(d3_good_reply),
                "--workdir", str(root / "d3_good_wd"),
                "--json",
            ])
        with contextlib.redirect_stdout(d3_bad_buf):
            rc_d3_bad_v = verify_numbers_main([
                "--reply-json", str(d3_bad_reply),
                "--source", str(r4_d3_docx), str(r4_d3_tex),
                "--json",
            ])
        with contextlib.redirect_stdout(io.StringIO()):
            rc_d3_bad_r = run_scoped_pass_main([
                "--manuscript", str(d3_main_md),
                "--target", "4. Results",
                "--companion", str(r4_d3_docx), str(r4_d3_tex),
                "--backend", "envelope-only",
                "--verify-reply", str(d3_bad_reply),
                "--workdir", str(root / "d3_bad_wd"),
                "--json",
            ])
        d3_bad_report = json.loads(d3_bad_buf.getvalue())
        d3_unverified_f = next((f for f in d3_bad_report["findings"] if f["code"] == "UNVERIFIED_NUMBER_IN_PROSE"), {})
        require(
            rc_d3_good_v == 0
            and rc_d3_good_r == 0
            and rc_d3_bad_v == 1
            and rc_d3_bad_r == 1
            and {"99.9%", "88.8%", "77.7%", "66.6%", "55.5%"} <= set(d3_unverified_f.get("tokens", []))
            and any(f["code"] == "ENTITY_SIGN_REVERSAL" for f in d3_bad_report["findings"]),
            f"R4-D3 .docx/.tex companion/source structured extraction failed: good=({rc_d3_good_v},{rc_d3_good_r}), bad_report={d3_bad_report}",
        )

        # Round-5 reviewer adversarial additions:
        # (a) balanced locator scrubbing `(Table 1)`, entity-colon/right-paren isolation, prior-num-prep + 'by',
        #     trailing modifier before 'and', serial-comma & split-parenthetical attribution units, and dotted model IDs
        r5_adv_src = "Across 3 waves (p = .004):\n| Subscale | Delta |\n| Tension | -2.4% |\n| Rumination | -3.8% |\n| Worry | +0.14 |"
        for adv_bad_sent in [
            "Despite a steep decline (Table 1), Rumination averaged 3.8%.",
            "Tension decreased significantly (Rumination: 3.8%).",
            "Rumination averaged 3.8% (Tension: 2.4% drop).",
            "Rumination averaged 3.8% (Wave 2 drop of 2.4%).",
            "Tension decreased by 2.4% compared with Rumination changing by 3.8%.",
            "Tension decreased significantly in Wave 1 and Rumination averaged 3.8%.",
            "Overall (Tension: -2.4%; Worry: -3.8%), Rumination changed by +0.14.",
            "In our model (Tension fell by -2.4%, whereas Worry fell by -3.8%), Rumination rose by +0.14.",
            "Tension was -3.8%, Rumination was -2.4%, and Worry was +0.14.",
            "Tension fell by -3.8% in Wave 1 and Rumination fell by -2.4% in Wave 1.",
        ]:
            adv_bad_res = verify_curated_salience(after_text=adv_bad_sent, source_texts=[r5_adv_src])
            require(
                adv_bad_res["status"] == "FAIL"
                and any(f["code"] in {"ENTITY_SIGN_REVERSAL", "CROSS_ENTITY_NUMBER_SWAP"} for f in adv_bad_res["findings"]),
                f"Round-5 adversarial polarity/attribution check missed {adv_bad_sent!r}: {adv_bad_res}",
            )
        for adv_good_sent in [
            "Tension decreased significantly (Worry: 0.14).",
            "Tension and Rumination decreased by 2.4% and 3.8%.",
            "In 3 waves Rumination decreased from baseline by 3.8%.",
            "Rumination changed by 3.8% (a significant decrease, p = .004).",
            "Rumination decreased significantly (3.8%, Table 1).",
            "Llama-3.1-8B and Qwen2.5-7B showed a 3.8% reduction in Rumination.",
        ]:
            adv_good_res = verify_curated_salience(after_text=adv_good_sent, source_texts=[r5_adv_src])
            require(adv_good_res["status"] == "PASS", f"Round-5 adversarial non-regression falsely failed on {adv_good_sent!r}: {adv_good_res}")

        # (b) agy direct result schema object + delta stream with trailing non-JSON response summary
        require(
            parse_backend_output(
                "agy",
                0,
                json.dumps({"status": "SUCCESS", "result": valid_so, "response": "Completed!", "finished_reason": "stop"}),
                "",
            ) == valid_so
            and parse_backend_output(
                "agy",
                0,
                json.dumps({"delta": json.dumps(valid_so)}) + "\n" + json.dumps({"status": "SUCCESS", "response": "Completed!", "finished_reason": "stop"}) + "\n",
                "",
            ) == valid_so,
            "Round-5 agy result/delta fallback clobbered by trailing non-JSON response summary",
        )

        # (c) .docx References-styled heading followed by Normal bibliography + .tex nested-brace tabular colspecs
        ref_style_docx = root / "ref_style_heading.docx"
        with zipfile.ZipFile(ref_style_docx, "w") as zf_rs:
            zf_rs.writestr(
                "word/styles.xml",
                f'<w:styles xmlns:w="{W}"><w:style w:type="paragraph" w:styleId="RefHead"><w:name w:val="References"/><w:pPr><w:outlineLvl w:val="0"/></w:pPr></w:style></w:styles>',
            )
            zf_rs.writestr(
                "word/document.xml",
                f'<w:document xmlns:w="{W}"><w:body>'
                '<w:p><w:r><w:t>Main 5.4% text.</w:t></w:r></w:p>'
                '<w:p><w:pPr><w:pStyle w:val="RefHead"/></w:pPr><w:r><w:t>References</w:t></w:r></w:p>'
                '<w:p><w:r><w:t>Doe (2024) 88.8% reference noise.</w:t></w:r></w:p>'
                '</w:body></w:document>',
            )
        rs_blocks, _, _ = _bce_mod.load_manuscript_blocks(ref_style_docx)
        require(
            [b["text"] for b in rs_blocks] == ["Main 5.4% text."],
            f"DOCX References-styled heading leaked subsequent Normal bibliography blocks: {rs_blocks}",
        )
        nested_col_tex = root / "nested_colspec.tex"
        nested_col_tex.write_text(
            "\\begin{tabular}{lp{3.5 cm}*{2}{r}}\\toprule\nSubscale & Note & Delta & N \\\\\n"
            "\\midrule\nRumination & Text & -3.8\\% & 400 \\\\\n\\bottomrule\\end{tabular}\n",
            encoding="utf-8",
        )
        nc_blocks, _, _ = _bce_mod.load_manuscript_blocks(nested_col_tex)
        require(
            nc_blocks and nc_blocks[0]["rows"][0] == ["Subscale", "Note", "Delta", "N"],
            f"LaTeX nested-brace tabular column spec leaked into table cells: {nc_blocks}",
        )

        tests.append("Round-4 strict-mode polarity multiset, schema-invalid guard, bottom/scoped captions, and child-.tex cache regressions")

    print(json.dumps({"status": "PASS", "tests": tests}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
