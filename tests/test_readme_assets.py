"""Guard the concise bilingual entry points and approved image delivery contract.

These checks cover file/entry-point structure, not visual or scientific quality.
"""

from pathlib import Path
import re
import struct

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("name", ["README.md", "README.zh-TW.md"])
def test_readme_names_agent_clients_without_a_testing_badge(name):
    text = (ROOT / name).read_text(encoding="utf-8")
    assert "actions/workflows/test.yml/badge.svg" not in text
    opening = text.split("## ", 1)[0]
    for client in ("Codex", "Claude Code", "OpenCode", "Hermes Agent", "Agent Skills"):
        assert client in opening, (name, client)
    assert "depend on the host" in opening or "依 host 而定" in opening


@pytest.mark.parametrize("name", ["README.md", "README.zh-TW.md"])
def test_readme_links_parent_project_cover_and_five_task_prompts(name):
    text = (ROOT / name).read_text(encoding="utf-8")
    assert "[ai-research-skills](https://github.com/WenyuChiou/ai-research-skills)" in text
    assert re.search(r"!\[[^\]]+\]\(\./docs/images/workflow-cover\.png\)", text)
    prompts = re.findall(r"```text\n(.*?)\n```", text, re.DOTALL)
    assert len(prompts) == 5
    assert sum("academic-writing-skills" in prompt for prompt in prompts) == 4
    assert sum("paper-review" in prompt for prompt in prompts) == 1


@pytest.mark.parametrize(
    ("name", "required"),
    [
        (
            "README.md",
            [
                "Frame & outline", "Plan & write", "Check & revise",
                "Section reviews", "four passes", "shared terminology record",
                "Proposed names remain separate until the author confirms them",
                "A local grammar edit does not trigger every stage",
            ],
        ),
        (
            "README.zh-TW.md",
            [
                "研究定位與大綱", "規劃與撰寫", "檢查與修改",
                "章節審查", "四輪", "共用詞彙紀錄",
                "新提議的名稱須與作者已確認的選擇分開",
                "單句文法修改不會啟動所有階段",
            ],
        ),
    ],
)
def test_workflow_and_shared_record_boundaries_remain_visible(name, required):
    text = (ROOT / name).read_text(encoding="utf-8")
    for phrase in required:
        assert phrase in text, (name, phrase)


@pytest.mark.parametrize(
    ("name", "expected_size", "maximum_bytes"),
    [
        ("workflow-cover.png", (1774, 887), 2_000_000),
        ("social-preview.png", (1280, 640), 1_000_000),
    ],
)
def test_png_assets_have_the_approved_delivery_dimensions(name, expected_size, maximum_bytes):
    data = (ROOT / "docs" / "images" / name).read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    assert data[12:16] == b"IHDR"
    assert struct.unpack(">II", data[16:24]) == expected_size
    assert len(data) < maximum_bytes
