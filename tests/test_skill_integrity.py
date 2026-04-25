import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_skill_frontmatter_is_valid():
    content = read("SKILL.md")
    assert content.startswith("---\n")
    frontmatter = content.split("---", 2)[1]
    assert re.search(r"^name:\s*academic-writing-skills$", frontmatter, re.M)
    description = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
    assert description
    assert "reviewer response" in description.group(1).lower()
    assert "claim-evidence" in description.group(1).lower()


def test_referenced_files_exist():
    required = [
        "references/writing_principles.md",
        "references/banned_words.md",
        "references/section_checklists.md",
        "references/figure_conventions.md",
        "references/claim_evidence_audit.md",
        "references/reviewer_response_workflow.md",
        "references/submission_checklist.md",
        "references/paper_context_packet.md",
        "references/journal_format_template.md",
        "references/style_overrides_example.md",
    ]
    for relative_path in required:
        assert (ROOT / relative_path).exists(), relative_path


def test_eval_file_has_realistic_prompts():
    data = json.loads(read("evals/evals.json"))
    assert data["skill_name"] == "academic-writing-skills"
    evals = data["evals"]
    assert len(evals) >= 5
    ids = [item["id"] for item in evals]
    assert len(ids) == len(set(ids))
    for item in evals:
        assert item["prompt"].strip()
        assert item["expected_output"].strip()
        assert isinstance(item["files"], list)


def test_no_common_mojibake_markers_in_markdown():
    markers = [
        "\uFFFD",
        "\uE73F",
        "\uEC27",
        "\uE4C7",
        "\u875C\u875C"[0],
        "\u929D",
        "\u5697",
        "\u79AE",
        "?" + "?",
    ]
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            assert marker not in text, f"{marker!r} found in {path.relative_to(ROOT)}"


def test_readmes_describe_public_positioning():
    english = read("README.md")
    traditional_chinese = read("README.zh-TW.md")
    for text in [english, traditional_chinese]:
        assert "Zotero" in text
        assert "NotebookLM" in text
        assert ".paper/" in text
    assert "Traditional Chinese README" in english
    assert "English README" in traditional_chinese
