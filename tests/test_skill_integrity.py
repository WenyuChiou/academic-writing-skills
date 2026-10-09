import hashlib
import json
import re
import subprocess
import struct
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "skills" / "academic-writing-skills"
REVIEW = ROOT / "skills" / "paper-review"


CORE_REFERENCES = {
    "banned_words.md",
    "conclusion-and-abstract.md",
    "discussion-and-limitations.md",
    "execution-and-acceptance.md",
    "figures-tables-and-supplements.md",
    "introduction-and-study-context.md",
    "lifecycle-and-routing.md",
    "methods-and-assumptions.md",
    "overlay-contract.md",
    "prose-and-citation-editing.md",
    "professor-teaching-cases.md",
    "reviewer-red-team-and-release.md",
    "reviewer-response-workflow.md",
    "results-and-explanation.md",
    "state-and-authority.md",
    "study-design-adapters.md",
    "universal-integrity.md",
}
CORE_SCRIPTS = {
    "audit_candidate_text.py",
    "audit_docx_structure.py",
    "audit_handoff.py",
    "audit_manuscript_state.py",
    "audit_prose_patterns.py",
    "audit_text_consistency.py",
    "init_manuscript_state.py",
    "run_regression_tests.py",
}
REVIEW_REFERENCES = {
    "ai-llm-computational.md",
    "display-notation-provenance.md",
    "ethan-style-overlay.md",
    "flood-hydrodynamics-catastrophe.md",
    "overlay-contract.md",
    "project-precedents.md",
    "quantitative-psychometrics-sem.md",
    "round-calibration.md",
    "water-cnhs-uncertainty.md",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter(path: Path) -> dict[str, str]:
    text = read(path)
    assert text.startswith("---\n")
    block = text.split("---", 2)[1].strip().splitlines()
    parsed = {}
    for line in block:
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def test_plugin_manifest_marks_major_architecture_release():
    manifest = json.loads(read(ROOT / ".claude-plugin" / "plugin.json"))
    assert manifest["name"] == "academic-writing-skills"
    assert manifest["version"] == "1.3.8"
    assert "progressive" in manifest["description"].lower()
    assert "domain" in manifest["description"].lower()


def test_both_skill_frontmatters_are_valid_and_minimal():
    core = frontmatter(CORE / "SKILL.md")
    review = frontmatter(REVIEW / "SKILL.md")
    assert set(core) == {"name", "description"}
    assert set(review) == {"name", "description"}
    assert core["name"] == "academic-writing-skills"
    assert review["name"] == "paper-review"
    assert "submission" in core["description"].lower()
    assert "progressive" in review["description"].lower()
    assert "psychometrics" in review["description"].lower()


def test_skill_file_sets_match_the_release_contract():
    assert {p.name for p in (CORE / "references").glob("*.md")} == CORE_REFERENCES
    assert {p.name for p in (CORE / "scripts").glob("*.py")} == CORE_SCRIPTS
    assert {p.name for p in (REVIEW / "references").glob("*.md")} == REVIEW_REFERENCES
    for skill in (CORE, REVIEW):
        assert (skill / "agents" / "openai.yaml").is_file()
        assert (skill / "assets" / "icon.svg").is_file()
    assert (CORE / "assets" / "manuscript_state_template.json").is_file()


def test_markdown_reference_routes_resolve():
    pattern = re.compile(r"\]\((references/[^)#]+\.md)(?:#[^)]+)?\)")
    for skill in (CORE, REVIEW):
        routes = pattern.findall(read(skill / "SKILL.md"))
        assert routes
        for route in routes:
            assert (skill / route).is_file(), f"missing route: {skill.name}/{route}"


def test_markdown_links_resolve_inside_reference_files():
    pattern = re.compile(r"\]\(([^)#]+\.md)(?:#[^)]+)?\)")
    for skill in (CORE, REVIEW):
        for source in (skill / "references").glob("*.md"):
            for route in pattern.findall(read(source)):
                assert (source.parent / route).is_file(), f"missing route: {source.name} -> {route}"


def test_core_includes_lifecycle_impact_and_release_gates():
    skill = read(CORE / "SKILL.md")
    lifecycle = read(CORE / "references" / "lifecycle-and-routing.md")
    prose = read(CORE / "references" / "prose-and-citation-editing.md")
    banned = read(CORE / "references" / "banned_words.md")
    release = read(CORE / "references" / "reviewer-red-team-and-release.md")
    adapters = read(CORE / "references" / "study-design-adapters.md")
    assert "lightweight mode" in skill
    assert "managed-project mode" in skill
    assert "Class A" in skill and "Class D" in skill
    assert "Functional-Completeness Retrospective" in skill
    assert "Draft from Explicit Writing Contracts" in skill
    assert "audit_prose_patterns.py" in skill
    assert "revise-and-resubmit" in lifecycle
    assert "Do not require headings" in lifecycle
    assert "S3 and S4 open blockers equal zero" in release
    assert "separate standardized coefficients" in adapters
    assert "broad field context" in prose
    assert "contextual judgment" in banned
    assert "signal AI-generated" not in banned
    assert "reliable LLM-prose tells" not in banned
    assert "`abstract-writer`" not in banned
    assert "`verify-references`" not in banned
    assert "closest precedent" in prose
    assert "cumulative argument rather than a list" in prose
    assert "broad disciplinary readership" in prose
    assert "draw on data" in prose
    assert "intended scholarly audience" in prose
    assert "read the exact passage aloud" in prose
    assert "do not append the citations as an unexplained contradiction" in prose
    assert "reflects the current sample or location" in prose
    assert "Keep this disclaimer brief and evidence-backed" in prose
    assert "Do not recast a calibrated relationship as a model assumption" in prose


def test_reviewer_response_contract_keeps_answers_direct_and_sensitivity_reproducible():
    workflow = read(CORE / "references" / "reviewer-response-workflow.md")
    normalized = " ".join(workflow.split())
    assert "must never distract from, replace, or leave incomplete" in normalized
    assert "enough local context, the key result, and its meaning" in normalized
    assert "adopted baseline model specification distinct from the sensitivity" in normalized
    assert "Do not present a robustness-only sensitivity test" in normalized
    assert "understands the paper's broad research direction" in normalized
    assert "read the completed response aloud" in normalized
    assert "name the comparison reference in the same sentence" in normalized.lower()
    assert "cite the relevant figure or table" in normalized.lower()
    assert "robustness-only sensitivity test" in normalized
    assert "latest advisor-edited document" in normalized
    assert "response addressed to the reviewer" in normalized
    assert "opening revision summary" in normalized
    assert "brief acknowledgment" in normalized
    assert "different reader functions" in normalized
    assert "when specification choice is at issue" in normalized
    assert "does not by itself select or validate the baseline setting" in normalized
    assert "Do not invent a new empirical, theoretical, or practical reason" in normalized
    assert "locally defined whole-model comparison" in normalized
    assert "When a final model decision is required" in normalized
    assert "does not establish the effect of a separate scenario contrast" in normalized
    assert "Do not leave a stale reply" in normalized


def test_reviewer_labels_record_revision_provenance_not_topic_membership():
    workflow = read(CORE / "references" / "reviewer-response-workflow.md")
    normalized = " ".join(workflow.split())
    assert "actual submitted manuscript" in normalized
    assert "effective revised text" in normalized
    assert "provenance of a revision; it is not a subject index" in normalized
    assert "existing text; no manuscript change" in normalized
    assert "without claiming that it was revised" in normalized
    assert "only to text, displays, or locations that were actually changed" in normalized
    assert "unchanged source passage may support the response, but it should remain unlabeled" in normalized
    assert "smallest sufficient revision" in normalized
    assert "one comment box listing the applicable reviewer IDs" in normalized
    assert "Do not treat a definition or derived outcome as an assumption" in normalized
    assert "sampling, measurement, intervention, procedure, coding, or analysis" in normalized


def test_results_gate_requires_meaning_without_discussion_overreach():
    lifecycle = read(CORE / "references" / "lifecycle-and-routing.md")
    normalized = " ".join(lifecycle.split())
    assert "what the observed pattern means" in normalized
    assert "Numbers alone are not a substantive answer" in normalized
    assert "untested mechanisms" in normalized


def test_section_guides_are_routed_without_forcing_full_review():
    skill = read(CORE / "SKILL.md")
    for name in (
        "introduction-and-study-context.md", "methods-and-assumptions.md",
        "results-and-explanation.md", "discussion-and-limitations.md",
        "conclusion-and-abstract.md", "figures-tables-and-supplements.md",
    ):
        assert f"](references/{name})" in skill
    lifecycle = read(CORE / "references" / "lifecycle-and-routing.md")
    assert "Chapter-Closure Blind-Spot Check" in lifecycle
    assert "At every chapter completion or substantial chapter revision" in lifecycle
    assert "Timing is mandatory; diagnostic content is conditional" in lifecycle
    assert "not a certification that all unknown unknowns were found" in lifecycle
    assert "Develop Supporting Material in parallel" in lifecycle


def test_results_and_extension_analysis_keep_inference_boundaries():
    results = read(CORE / "references" / "results-and-explanation.md")
    discussion = read(CORE / "references" / "discussion-and-limitations.md")
    shared = read(CORE / "references" / "universal-integrity.md")
    assert "Results may contain findings and explanations directly supported by the analysis" in shared
    assert "reserve extended, literature-based, or untested mechanism interpretations" in shared
    assert "findings in Results, and mechanisms or implications in Discussion" not in shared
    assert "one primary question" in results
    assert "not a mandatory one-figure/one-question ratio" in results
    assert "composition" in results and "aggregation" in results
    assert "rule alone" in results and "causal" in results
    assert "extension-analysis" in discussion
    assert "not require sensitivity analyses" in discussion
    assert "direction, ranking, magnitude, or metric" in discussion
    assert "specific constraint" in discussion
    assert "not a blanket ban" in discussion


def test_summary_guidance_removes_universal_abstract_templates():
    summary = read(CORE / "references" / "conclusion-and-abstract.md")
    for meaning in (
        "This study examined", "method and research task", "information functions",
        "not six mandatory blocks", "No universal word or sentence cap",
        "Do not invent optimization objectives", "Ask only when",
        "raw numbers", "compression",
    ):
        assert meaning in summary


def test_visual_and_response_guidance_reconciles_exact_artifacts():
    displays = read(CORE / "references" / "figures-tables-and-supplements.md")
    workflow = read(CORE / "references" / "reviewer-response-workflow.md")
    prose = read(CORE / "references" / "prose-and-citation-editing.md")
    assert "actual final display size" in displays
    assert "nonfunctional whitespace" in displays
    assert "not universal journal rules" in displays
    assert "**Figures S4** to **S6**" in displays
    assert "caption" in displays and "table note" in displays
    assert "Promise-to-Artifact Reconciliation" in workflow
    assert "rendered target version" in workflow
    assert "never calculate line numbers" in workflow
    assert "nonprobability" in workflow
    assert "flood adaptation decision-making process" in prose


def test_new_chapter_behavioral_probes_are_registered():
    data = json.loads(read(ROOT / "evals" / "evals.json"))
    required = {
        "chapter_closure_checks_are_content_conditional",
        "results_composition_not_individual_decay",
        "discussion_extension_unchanged_ranking_not_validation",
        "abstract_identity_without_fixed_template",
        "visual_legibility_without_whitespace_overcorrection",
        "response_promises_and_rendered_locators",
    }
    registered = {item["id"] for item in data["evals"]}
    assert required <= registered


def test_abm_display_examples_preserve_verified_source_text():
    displays = read(CORE / "references" / "figures-tables-and-supplements.md")
    table_section = displays.split("### Original Table 1", 1)[1].split(
        "### Teaching note", 1
    )[0]
    rows = [line for line in table_section.splitlines() if line.startswith("|")]
    data = [[re.sub(r"\s+", " ", cell.strip()) for cell in row.strip("|").split("|")]
            for row in rows[2:]]
    assert len(data) == 6 and all(len(row) == 5 for row in data)
    canonical_table = "\n".join("|".join(row) for row in data)
    assert hashlib.sha256(canonical_table.encode()).hexdigest() == (
        "dac3dd913a33fde402a1b39781e79fd70eb48d9156f10626cc8ade4ec085543c"
    )
    caption = re.search(r"^> \*\*Figure 6\.\*\* (.+)$", displays, re.MULTILINE)
    assert caption is not None
    canonical_caption = "Figure 6. " + re.sub(r"\s+", " ", caption.group(1).strip())
    assert hashlib.sha256(canonical_caption.encode()).hexdigest() == (
        "65d6e2976a61796dab18897e950227932e20b11b3c311c987244f46fb4e5111e"
    )


def test_abm_figure_example_preserves_original_asset():
    image = CORE / "assets" / "examples" / "abm-figure-6.png"
    data = image.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    assert struct.unpack(">II", data[16:24]) == (1433, 1765)
    assert hashlib.sha256(data).hexdigest() == (
        "3e1461f1c0468534d3bc3b73e1f222bef6d6f09cdb2e4b458a8b66f39e60dd0c"
    )
    displays = read(CORE / "references" / "figures-tables-and-supplements.md")
    assert "(../assets/examples/abm-figure-6.png)" in displays


def test_abm_example_distinguishes_source_from_teaching_additions():
    displays = read(CORE / "references" / "figures-tables-and-supplements.md")
    assert "ABM_manuscript_20260812_WC_clean_label.docx" in displays
    assert "5464b65aa813777fe00fe90bd41255b7be07b842487ee13db42bd4b9815c5176" in displays
    assert "### Teaching note (added here, not in the manuscript)" in displays
    assert "not empirically estimated confidence intervals" in displays
    assert "do not substantiate these exact bounds" in displays
    assert "Do not copy the ABM's thresholds, six-panel layout, 50 runs" in displays
    data = json.loads(read(ROOT / "evals" / "evals.json"))
    assert any(case["id"] == "abm_display_example_transfer_without_fact_copying"
               for case in data["evals"])


def test_venue_guidance_is_routed_and_scope_conditional():
    skill = read(CORE / "SKILL.md")
    overlay = read(CORE / "references" / "overlay-contract.md")
    lifecycle = read(CORE / "references" / "lifecycle-and-routing.md")
    assert "Confirm Venue Direction, Format, and Style" in skill
    assert "Venue Profile" in overlay
    assert "aims and scope" in overlay and "article type" in overlay
    assert "checked date" in overlay and "production" in overlay
    assert "grammar-only" in overlay
    assert "does not authorize new analyses" in overlay
    assert "venue profile" in lifecycle


def test_abm_map_preserves_source_and_distinguishes_denominators():
    displays = read(CORE / "references" / "figures-tables-and-supplements.md")
    caption = re.search(r"^> \*\*Figure 1\.\*\* (.+)$", displays, re.MULTILINE)
    assert caption is not None
    text = "Figure 1. " + re.sub(r"\s+", " ", caption.group(1).strip())
    assert hashlib.sha256(text.encode()).hexdigest() == (
        "4ab4a2d2e900a46c8f92d9235f57ae39d43b694acf8440197c764d5dfc506684"
    )
    data = (CORE / "assets" / "examples" / "abm-figure-1.png").read_bytes()
    assert struct.unpack(">II", data[16:24]) == (6671, 4355)
    assert hashlib.sha256(data).hexdigest() == (
        "7ce2d3c69498c2805a7a3183e228f0ea60967babef3a8638a96fdfb9854bb501"
    )
    assert "(../assets/examples/abm-figure-1.png)" in displays
    assert "zero" in displays and "missing" in displays
    assert "not a household percentage" in displays
    assert "cannot establish the coordinate reference system" in displays


def test_borders_and_citations_distinguish_source_from_requirement():
    displays = read(CORE / "references" / "figures-tables-and-supplements.md")
    overlay = read(CORE / "references" / "overlay-contract.md")
    assert "1 pt" in displays and "0.5 pt" in displays
    assert "nonprinting Word gridlines" in displays
    assert "not a universal three-line-table requirement" in displays
    assert "not equivalent to inspecting the rendered table" in displays
    assert "Mondino et al., 2020" in overlay
    assert "not validation of the ABM's tract-level proxy" in overlay
    assert "exact thresholds" in overlay
    assert "2026a/2026b" in overlay
    assert "not a generic APA edition" in overlay
    data = json.loads(read(ROOT / "evals" / "evals.json"))
    ids = {item["id"] for item in data["evals"]}
    assert {"venue_first_without_scope_expansion",
            "map_and_borders_without_false_certification",
            "citation_rationale_not_parameter_validation"} <= ids


def test_review_uses_progressive_modules_and_conditional_ethan_overlay():
    skill = read(REVIEW / "SKILL.md")
    contract = read(REVIEW / "references" / "overlay-contract.md")
    precedents = read(REVIEW / "references" / "project-precedents.md")
    ethan = read(REVIEW / "references" / "ethan-style-overlay.md")
    psych = read(REVIEW / "references" / "quantitative-psychometrics-sem.md")
    ai = read(REVIEW / "references" / "ai-llm-computational.md")
    displays = read(REVIEW / "references" / "display-notation-provenance.md")
    rounds = read(REVIEW / "references" / "round-calibration.md")
    assert "Use `academic-writing-skills` as the manuscript-integrity base" in skill
    assert "Select Modules Progressively" in skill
    assert "Ask one targeted question only when" in skill
    assert "Support New Domain Modules" in skill
    assert "display-notation-provenance.md" in skill
    assert "only when the user explicitly requests Ethan-style review" in skill
    assert "latest Ethan-edited draft" in ethan
    assert "Keep the reviewer response" in ethan
    assert "I revised" in ethan
    assert "when specification choice is at issue" in ethan
    assert "Do not perform a global terminology replacement" in ethan
    assert "robustness, not" in ethan
    assert "Update the reply to Ethan after the revision" in " ".join(ethan.split())
    assert "Select the smallest sufficient set" in contract
    assert "Load this file only after" in precedents
    assert "Do not import sample sizes, funding, model versions" in precedents
    assert "Do not claim to be Prof. Ethan Yang" in ethan
    assert "one significant path and one nonsignificant path" in psych
    assert "LLM consistency is not behavioral validity" in ai
    assert "Build an Equation and Notation Ledger" in displays
    assert "Do not load it merely because" in displays
    assert "source data or model output -> transformation or equation" in displays
    assert "Never upgrade a thread to `RESOLVED`" in rounds
    assert "response letter or resolved comment thread" in skill
    assert "acting as Prof. Ethan Yang" not in skill


def test_state_template_is_valid_and_starts_working():
    state = json.loads(read(CORE / "assets" / "manuscript_state_template.json"))
    assert state["schema_version"] == "1.1"
    assert state["project"]["active_release"] == "working"
    assert state["release"]["status"] == "WORKING"
    assert state["style_profile"]["phrase_words"] == 5
    assert "functional_completeness" in state["release"]["required_checks"]


def test_python_sources_parse_and_regressions_pass():
    for path in (CORE / "scripts").glob("*.py"):
        compile(read(path), str(path), "exec")
    result = subprocess.run(
        [sys.executable, str(CORE / "scripts" / "run_regression_tests.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "PASS"
    assert len(report["tests"]) == 27


def test_evals_cover_core_and_progressive_review_behavior():
    files = {
        "academic-writing-skills": ROOT / "evals" / "evals.json",
        "paper-review": ROOT / "evals" / "paper-review.json",
    }
    for skill_name, path in files.items():
        data = json.loads(read(path))
        assert data["skill_name"] == skill_name
        assert len(data["evals"]) >= 4
        ids = [item["id"] for item in data["evals"]]
        assert len(ids) == len(set(ids))
        if skill_name == "academic-writing-skills":
            assert "sensitivity_response_names_baseline_conclusion_and_final_setting" in ids
            assert "sensitivity_robustness_does_not_select_baseline" in ids
        for item in data["evals"]:
            assert item["prompt"].strip()
            assert item["expected_output"].strip()
            assert isinstance(item["files"], list)


def test_scope_behavioral_probes_remain_registered():
    """Guard probe coverage; semantic outcomes require independent evaluation."""
    data = json.loads(read(ROOT / "evals" / "evals.json"))
    required = {
        "scope_sentence_grammar_only",
        "scope_results_paragraph_so_what",
        "scope_subsection_multi_figure",
        "scope_chapter_reader_prerequisites",
        "scope_whole_manuscript_claim_chain",
        "scope_local_metric_cross_artifact_trigger",
    }
    registered = {item["id"] for item in data["evals"]}
    assert required <= registered, f"Missing behavioral probes: {required - registered}"


def test_reference_refinement_probes_have_routes_and_semantic_criteria():
    """Check runnable probe inputs; this does not certify semantic outcomes."""
    data = json.loads(read(ROOT / "evals" / "evals.json"))
    cases = {item["id"]: item for item in data["evals"]}
    routes = {
        "topic_sentence_reverse_outline_preserves_actual_draft": "lifecycle-and-routing.md",
        "current_gap_and_sequential_questions_without_age_cutoff": "introduction-and-study-context.md",
        "response_working_draft_does_not_certify_pending_test": "reviewer-response-workflow.md",
        "chart_function_from_axes_not_filename": "figures-tables-and-supplements.md",
    }
    for case_id, reference in routes.items():
        assert case_id in cases, f"Missing behavioral probe: {case_id}"
        case = cases[case_id]
        assert case["prompt"].strip() and case["expected_output"].strip()
        criteria = case["acceptance_criteria"]
        assert isinstance(criteria, list) and len(criteria) >= 3
        assert all(isinstance(item, str) and item.strip() for item in criteria)
        route = Path("skills") / "academic-writing-skills" / "references" / reference
        assert case["files"] == [route.as_posix()]
        assert (ROOT / route).is_file()


def test_professor_teaching_cases_are_routed_and_source_bounded():
    """Guard routing and boundaries, not the model's semantic performance."""
    name = "professor-teaching-cases.md"
    assert f"](references/{name})" in read(CORE / "SKILL.md")
    text = read(CORE / "references" / name)
    headings = (
        "Paragraphs and Extended Outlines", "Abstracts with Missing Findings",
        "Reviewer Responses and Actual Work Status",
        "Figures and Tables: Existing ABM Check Entries",
    )
    for heading in headings:
        assert f"## {heading}" in text
    positions = [text.index(f"## {heading}") for heading in headings]
    assert positions == sorted(positions)
    for field in ("Problem", "Trigger", "Judgment", "Minimal repair", "Boundary"):
        assert text.count(f"**{field}:**") == 4
    for boundary in (
        "teaching paraphrases", "not universal rules",
        "do not redistribute the complete private documents",
        "do not force a Study", "do not invent a result",
        "keep the concern open", "not a current data, reference, venue",
        "not duplicate caption rules",
    ):
        assert boundary in " ".join(text.split())
    for source_id in (
        "1LXp2SjM4eNSgC5i2axud4egZv1C_RzIN",
        "1xGAM52kDe0kY4TqZGPDMkdG9x6_kjP_s",
        "1oykntLNoC6pt7_eZiNXsBqG-enj3Jo5r",
        "1VGBJxzK7pFxgo19w_sC_zLtr55Zkmur5",
    ):
        assert f"https://docs.google.com/document/d/{source_id}/edit" in text


def test_professor_teaching_behavioral_probes_have_scoped_inputs():
    """Registered cases need independent answers before claiming behavior PASS."""
    data = json.loads(read(ROOT / "evals" / "evals.json"))
    cases = {case["id"]: case for case in data["evals"]}
    route = "skills/academic-writing-skills/references/professor-teaching-cases.md"
    for case_id in (
        "teaching_case_grammar_only_preserves_scope",
        "teaching_case_conceptual_outline_no_imrad",
        "teaching_case_abstract_missing_findings",
        "teaching_case_response_pending_not_completed",
    ):
        case = cases[case_id]
        assert case["files"] == ["skills/academic-writing-skills/SKILL.md", route]
        assert len(case["acceptance_criteria"]) >= 3
        assert all(item.strip() for item in case["acceptance_criteria"])
        assert case["prompt"].strip() and case["expected_output"].strip()


def test_reader_continuity_and_limitation_allocation_probes_are_registered():
    data = json.loads(read(ROOT / "evals" / "evals.json"))
    cases = {case["id"]: case for case in data["evals"]}
    execution = "skills/academic-writing-skills/references/execution-and-acceptance.md"
    limitations = "skills/academic-writing-skills/references/discussion-and-limitations.md"
    required = {
        "limitations_reader_continuity_and_consequence_allocation": [
            "skills/academic-writing-skills/SKILL.md", execution, limitations,
        ],
        "limitations_frame_research_boundary_not_paper_defect": [
            "skills/academic-writing-skills/SKILL.md", limitations,
        ],
        "bounded_copyedit_preserves_coherent_expert_prose": [
            "skills/academic-writing-skills/SKILL.md", execution,
        ],
    }
    for case_id, routed_files in required.items():
        case = cases[case_id]
        assert case["files"] == routed_files
        assert case["prompt"].strip() and case["expected_output"].strip()
        assert len(case["acceptance_criteria"]) >= 3
        assert all(item.strip() for item in case["acceptance_criteria"])

    prose = " ".join(read(ROOT / execution).split())
    discussion = " ".join(read(ROOT / limitations).split())
    assert "adjacent-sentence transition" in prose
    assert "adding a transition word alone is not a repair" in prose
    assert "Do not force an explicit connector between every sentence" in prose
    assert "Allocate Limitation Claims to Their Actual Consequences" in discussion
    assert "does not show that it caused a nonsignificant finding" in discussion
    assert "a new sample can check" in discussion
    assert "state each one and its distinct consequence" in discussion
    assert "not as a defect in" in discussion
    assert "correctable analytical" in discussion


def test_readmes_are_bilingual_user_facing_entrypoints():
    english = read(ROOT / "README.md")
    chinese = read(ROOT / "README.zh-TW.md")
    version = json.loads(read(ROOT / ".claude-plugin" / "plugin.json"))["version"]

    for text in (english, chinese):
        assert "$academic-writing-skills" not in text
        assert "$paper-review" not in text
        assert "@academic-writing-skills" not in text
        assert "@paper-review" not in text
        assert "academic-writing-skills" in text
        assert "paper-review" in text
        assert "claude plugin marketplace add WenyuChiou/ai-research-skills" in text
        assert "claude plugin install academic-writing-skills@ai-research-skills" in text
        assert "OpenCode" in text
        assert "Hermes Agent" in text
        assert "outline" in text.lower()
        assert "psychometrics" in text.lower()
        assert "AI/LLM" in text or "AI／LLM" in text
        assert f"plugin-v{version}-blue.svg" in text
        assert len(text.splitlines()) <= 150
        for internal_detail in (
            "functional-completeness",
            "audit_prose_patterns.py",
            "S3 and S4",
            "authority sources",
        ):
            assert internal_detail not in text

    assert "## From research architecture to submission" in english
    assert "argument architecture" in english
    assert "top-down" in english
    assert "bottom-up" in english
    assert "top-to-bottom" in english
    assert "Use the academic-writing-skills skill" in english
    assert "Use the paper-review skill" in english
    assert "[繁體中文](./README.zh-TW.md)" in english
    assert "[Full usage guide](./docs/USER_GUIDE.md)" in english

    assert "## 從研究架構到最終投稿" in chinese
    assert "架構發想" in chinese
    assert "由上而下" in chinese
    assert "由下而上" in chinese
    assert "從頭到尾" in chinese
    assert "請使用 academic-writing-skills skill" in chinese
    assert "請使用 paper-review skill" in chinese
    assert "[English](./README.md)" in chinese
    assert "[完整使用指南](./docs/USER_GUIDE.zh-TW.md)" in chinese

    relative_link = re.compile(r"\]\((\./[^)#]+)")
    for source in (ROOT / "README.md", ROOT / "README.zh-TW.md"):
        for route in relative_link.findall(read(source)):
            assert (ROOT / route.removeprefix("./")).exists(), (
                f"broken README link: {source.name} -> {route}"
            )


def test_user_facing_prompts_are_platform_neutral():
    paths = [
        ROOT / "README.md",
        ROOT / "README.zh-TW.md",
        ROOT / "docs" / "USER_GUIDE.md",
        ROOT / "docs" / "USER_GUIDE.zh-TW.md",
        CORE / "agents" / "openai.yaml",
        REVIEW / "agents" / "openai.yaml",
    ]
    prohibited = (
        "$academic-writing-skills",
        "$paper-review",
        "@academic-writing-skills",
        "@paper-review",
    )
    for path in paths:
        text = read(path)
        for marker in prohibited:
            assert marker not in text, f"client-specific invocation in {path}: {marker}"


def test_no_common_mojibake_or_internal_skill_ids():
    markers = ["\uFFFD", "\uE73F", "\uEC27", "\uE4C7", "\u929D", "\u5697", "?" + "?"]
    internal_id = re.compile(r"skill-[0-9a-f]{20,}")
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".json", ".py", ".yaml", ".yml", ".svg"}:
            continue
        text = read(path)
        for marker in markers:
            assert marker not in text, f"{marker!r} found in {path.relative_to(ROOT)}"
        assert not internal_id.search(text), f"internal id found in {path.relative_to(ROOT)}"
