import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "skills" / "academic-writing-skills"
REVIEW = ROOT / "skills" / "paper-review"


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
    assert manifest["version"] == "1.1.2"
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


def test_core_includes_lifecycle_impact_and_release_gates():
    skill = read(CORE / "SKILL.md")
    lifecycle = read(CORE / "references" / "lifecycle-and-routing.md")
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
    assert len(report["tests"]) == 10


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
        for item in data["evals"]:
            assert item["prompt"].strip()
            assert item["expected_output"].strip()
            assert isinstance(item["files"], list)


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
