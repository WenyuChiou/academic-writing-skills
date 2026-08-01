import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "skills" / "academic-writing-skills"
OVERLAY = ROOT / "skills" / "paper-review"


CORE_REFERENCES = {
    "lifecycle-and-routing.md",
    "overlay-contract.md",
    "reviewer-red-team-and-release.md",
    "state-and-authority.md",
    "study-design-adapters.md",
    "universal-integrity.md",
}
CORE_SCRIPTS = {
    "audit_docx_structure.py",
    "audit_manuscript_state.py",
    "audit_text_consistency.py",
    "init_manuscript_state.py",
    "run_regression_tests.py",
}
OVERLAY_REFERENCES = {
    "abm-computational-and-ai.md",
    "cnhs-water-and-uncertainty.md",
    "flood-and-hydrodynamics.md",
    "overlay-contract.md",
    "project-precedents.md",
    "round-calibration.md",
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
    assert manifest["version"] == "1.0.0"
    assert "Ethan-style" in manifest["description"]


def test_both_skill_frontmatters_are_valid_and_minimal():
    core = frontmatter(CORE / "SKILL.md")
    overlay = frontmatter(OVERLAY / "SKILL.md")
    assert set(core) == {"name", "description"}
    assert set(overlay) == {"name", "description"}
    assert core["name"] == "academic-writing-skills"
    assert overlay["name"] == "paper-review"
    assert "submission" in core["description"].lower()
    assert "ethan-style" in overlay["description"].lower()


def test_skill_file_sets_match_the_release_contract():
    assert {p.name for p in (CORE / "references").glob("*.md")} == CORE_REFERENCES
    assert {p.name for p in (CORE / "scripts").glob("*.py")} == CORE_SCRIPTS
    assert {p.name for p in (OVERLAY / "references").glob("*.md")} == OVERLAY_REFERENCES
    for skill in (CORE, OVERLAY):
        assert (skill / "agents" / "openai.yaml").is_file()
        assert (skill / "assets" / "icon.svg").is_file()
    assert (CORE / "assets" / "manuscript_state_template.json").is_file()


def test_markdown_reference_routes_resolve():
    pattern = re.compile(r"\]\((references/[^)#]+\.md)(?:#[^)]+)?\)")
    for skill in (CORE, OVERLAY):
        routes = pattern.findall(read(skill / "SKILL.md"))
        assert routes
        for route in routes:
            assert (skill / route).is_file(), f"missing route: {skill.name}/{route}"


def test_core_includes_lifecycle_impact_and_release_gates():
    skill = read(CORE / "SKILL.md")
    lifecycle = read(CORE / "references" / "lifecycle-and-routing.md")
    release = read(CORE / "references" / "reviewer-red-team-and-release.md")
    adapters = read(CORE / "references" / "study-design-adapters.md")
    assert "lightweight mode" in skill
    assert "managed-project mode" in skill
    assert "Class A" in skill and "Class D" in skill
    assert "Functional-Completeness Retrospective" in skill
    assert "revise-and-resubmit" in lifecycle
    assert "Do not require headings" in lifecycle
    assert "S3 and S4 open blockers equal zero" in release
    assert "separate standardized coefficients" in adapters


def test_overlay_remains_conditional_and_evidence_safe():
    skill = read(OVERLAY / "SKILL.md")
    contract = read(OVERLAY / "references" / "overlay-contract.md")
    precedents = read(OVERLAY / "references" / "project-precedents.md")
    assert "Use `academic-writing-skills` as the manuscript-integrity base" in skill
    assert "Do not claim to be Prof. Ethan Yang" in skill
    assert "MUST / SHOULD / QUERY / PREFERENCE" in skill
    assert "Reviewer preference never overrides evidence" in contract
    assert "Load this file only after" in precedents
    assert "Do not import sample sizes, funding, model versions" in precedents
    assert "acting as Prof. Ethan Yang" not in skill


def test_state_template_is_valid_and_starts_working():
    state = json.loads(read(CORE / "assets" / "manuscript_state_template.json"))
    assert state["schema_version"] == "1.0"
    assert state["project"]["active_release"] == "working"
    assert state["release"]["status"] == "WORKING"
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
    assert len(report["tests"]) == 9


def test_evals_cover_core_and_overlay_behavior():
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
        for item in data["evals"]:
            assert item["prompt"].strip()
            assert item["expected_output"].strip()
            assert isinstance(item["files"], list)


def test_readmes_describe_two_skill_architecture():
    english = read(ROOT / "README.md")
    chinese = read(ROOT / "README.zh-TW.md")
    for text in (english, chinese):
        assert "$academic-writing-skills" in text
        assert "$paper-review" in text
        assert "functional-completeness" in text
        assert "Zotero" in text
        assert "NotebookLM" in text
    assert "Traditional Chinese README" in english
    assert "English README" in chinese


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
