"""Fixture, routing and public-entrypoint checks, not semantic writing grades."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDES = ROOT / "skills/academic-writing-skills/references"


def test_public_identity_requests_are_seven_hypothetical_controls():
    document = json.loads((ROOT / "evals/research_identity_cases.json").read_text(encoding="utf-8"))
    cases = document["cases"]
    assert {case["id"] for case in cases} == {f"Q{i}" for i in range(2, 9)}
    assert len(cases) == 7
    for case in cases:
        assert set(case) == {"id", "request", "source_facts", "paragraph"}
        assert case["request"].strip() and case["paragraph"].strip()
        assert case["source_facts"]
        assert all(isinstance(value, str) and value.strip() for value in case["source_facts"].values())


def test_identity_guidance_is_on_the_existing_summary_and_handoff_routes():
    skill = (ROOT / "skills/academic-writing-skills/SKILL.md").read_text(encoding="utf-8")
    conclusion = (GUIDES / "conclusion-and-abstract.md").read_text(encoding="utf-8")
    execution = (GUIDES / "execution-and-acceptance.md").read_text(encoding="utf-8")
    cases = (GUIDES / "evidence-context-cases.md").read_text(encoding="utf-8")
    assert "references/conclusion-and-abstract.md" in skill
    assert "conclusion-and-abstract.md" in execution
    assert "evidence-context-cases.md#12-research-identity-before-sentence-compression" in conclusion
    assert "## 12. Research identity before sentence compression" in cases
    assert "evals/research_identity_cases.json" in cases
    assert "evidence-context case 12" in execution


def _local_targets(text):
    return {
        target.split("#", 1)[0] for target in re.findall(r"\]\(([^)]+)\)", text)
        if not re.match(r"[a-z]+:", target) and target.split("#", 1)[0]
    }


def _table_widths(text):
    return [len(line.split("|")) for line in text.splitlines() if line.startswith("|")]


def test_readme_local_targets_resolve_and_locale_table_topology_matches():
    english = (ROOT / "README.md").read_text(encoding="utf-8")
    chinese = (ROOT / "README.zh-TW.md").read_text(encoding="utf-8")
    simplified = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    for text in (english, chinese, simplified):
        for target in _local_targets(text):
            assert (ROOT / target).exists(), target
    # A structural guard only; bilingual meaning receives independent review.
    assert _table_widths(english) == _table_widths(chinese)
    assert _table_widths(english) == _table_widths(simplified)
    assert len(re.findall(r"^## ", english, re.M)) == len(re.findall(r"^## ", chinese, re.M))
    assert len(re.findall(r"^## ", english, re.M)) == len(re.findall(r"^## ", simplified, re.M))
    def guide_targets(text):
        targets=set()
        for path in _local_targets(text):
            if path.startswith("./skills/"):
                for base in ("academic-writing-skills", "paper-review"):
                    for suffix in ("zh-tw", "zh-cn"):
                        path=path.replace(f"/{base}-{suffix}/",f"/{base}/")
                targets.add(path)
        return targets
    assert guide_targets(english) == guide_targets(chinese) == guide_targets(simplified)
