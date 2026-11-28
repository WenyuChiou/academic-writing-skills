#!/usr/bin/env python3
"""Install one-level flat skill discovery shims and the host-neutral manuscript-delegate-pass alias."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


DEFAULT_SHIMS = {
    "academic-writing-flat": "academic-writing-skills",
    "paper-review": "paper-review",
}
LOCALE_SHIMS = {
    "academic-writing-flat-zh-tw": "academic-writing-skills-zh-tw",
    "academic-writing-flat-zh-cn": "academic-writing-skills-zh-cn",
    "paper-review-zh-tw": "paper-review-zh-tw",
    "paper-review-zh-cn": "paper-review-zh-cn",
}
DELEGATE_ALIAS_NAME = "manuscript-delegate-pass"
DELEGATE_REQUIRED_SCRIPTS = (
    "build_context_envelope.py",
    "verify_delegate_numbers.py",
    "run_scoped_manuscript_pass.py",
    "audit_prose_patterns.py",
    "audit_candidate_text.py",
    "audit_text_consistency.py",
    "audit_docx_structure.py",
)
DELEGATE_REQUIRED_REFERENCES = (
    "state-and-authority.md",
    "universal-integrity.md",
    "prose-and-citation-editing.md",
    "results-and-explanation.md",
    "execution-and-acceptance.md",
    "lifecycle-and-routing.md",
)
MARKER_NAME = ".flat_shim_origin.json"

DELEGATE_SKILL_MD = """---
name: manuscript-delegate-pass
description: Host- and model-agnostic Agent A -> Agent B scoped manuscript handoff and verification entry point powered by academic-writing-skills. Use when any primary session (Claude Code, Codex/GPT, Antigravity, OpenCode, Hermes Agent) delegates a bounded paragraph, subsection, or chapter check/revision to any subagent, plugin, or external CLI, enforcing a deterministic <= 4,500-token architecture spine, two-stage evidence-value salience, dual-channel JSON isolation, silent-timeout interception, and partitioned numeric + downstream Class B sync verification.
---

# Manuscript Delegate Pass (`Agent A -> Agent B`)

## When to Use

Use this lightweight, host-neutral entry point whenever a primary session (`Agent A`) delegates a scoped manuscript paragraph, subsection, or chapter pass to a secondary agent, plugin, or CLI (`Agent B`), or when preparing an isolated envelope for a host-native subagent. All scholarly rules, five-step Results guidance, and two-stage evidence-value triage inherit from `academic-writing-skills` (single source of truth).

## Required Workflow

1. **Never pass oral summaries or isolated snippets:** always build a deterministic `<= 4,500`-token architecture spine envelope from the active `.docx`, `.tex`, or `.md` manuscript (fusing companion CSVs, `manuscript_state.json`, and read-only `.paper/` memory when present):
   ```sh
   python scripts/build_context_envelope.py "<manuscript>" --target "<heading-or-Pxxx>" --mode revise --output "<workdir>/context_envelope.txt"
   ```
2. **Dispatch or prepare via the pluggable runner (`scripts/run_scoped_manuscript_pass.py`):**
   - Host-native subagent (`invoke_subagent`, `Agent`, or manual chat window):
     ```sh
     python scripts/run_scoped_manuscript_pass.py --manuscript "<manuscript>" --target "<target>" --backend envelope-only --workdir "<workdir>" --json
     ```
     Pass `<workdir>/context_envelope.txt` and `<workdir>/delegate_response_schema.json` to `Agent B`, then verify `Agent B`'s JSON reply:
     ```sh
     python scripts/run_scoped_manuscript_pass.py --manuscript "<manuscript>" --target "<target>" --backend envelope-only --verify-reply "<reply.json>" --workdir "<workdir>" --json
     ```
   - External CLI backends (`agy`, `codex`, `claude`, or custom `command` template):
     ```sh
     python scripts/run_scoped_manuscript_pass.py --manuscript "<manuscript>" --target "<target>" --backend agy --workdir "<workdir>" --json
     ```
3. **Enforce Dual-Channel Isolation & Partitioned Verification before adoption:**
   - Require `Agent B` to return `{revised_target_prose, declared_omitted_to_display, cross_section_sync_alerts, unverified_context_locks}` so editorial questions never leak into manuscript prose.
   - Use `strict_preservation` for `proofread` / `Class D` passes and `curated_salience` for `draft` / substantive `revise` passes (`scripts/verify_delegate_numbers.py`).
   - Treat any pruned number or subscale hitting `Abstract`, `Highlights`, `Discussion`, or `Conclusion` as a `Class B` synchronization requirement before updating the manuscript.
"""

DELEGATE_OPENAI_YAML = """interface:
  display_name: Manuscript Delegate Pass
  short_description: Host-neutral Agent A -> Agent B scoped manuscript handoff
  default_prompt: Use the manuscript-delegate-pass skill to build a deterministic
    architecture spine envelope, run a bounded Agent A -> Agent B manuscript pass,
    and verify numeric provenance and cross-section sync before adopting edits.
  icon_small: assets/icon.svg
  icon_large: assets/icon.svg
policy:
  products:
  - chatgpt
  - codex
  - api
  - atlas
  allow_implicit_invocation: true
"""


def _prepare_clean_dest(dst: Path, force: bool = False) -> None:
    if dst.exists():
        if not (dst / MARKER_NAME).is_file() and not force:
            raise RuntimeError(f"refusing to overwrite unmanaged directory: {dst}")
        shutil.rmtree(dst)


def _copy_tree(src: Path, dst: Path, force: bool = False) -> int:
    _prepare_clean_dest(dst, force=force)
    copied = 0
    for item in sorted(src.rglob("*")):
        if "__pycache__" in item.parts or item.suffix in {".pyc", ".pyo"}:
            continue
        rel = item.relative_to(src)
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(item, target)
            copied += 1
    return copied


def _install_delegate_alias(repo_root: Path, dest_dir: Path, version: str, force: bool = False) -> dict[str, object]:
    core_src = repo_root / "skills" / "academic-writing-skills"
    dst = dest_dir / DELEGATE_ALIAS_NAME
    core_res, dst_res = core_src.resolve(), dst.resolve()
    if dst_res == core_res or dst_res in core_res.parents or core_res in dst_res.parents:
        raise ValueError(f"refusing overlapping source and destination paths: {core_src} -> {dst}")

    _prepare_clean_dest(dst, force=force)
    (dst / "scripts").mkdir(parents=True, exist_ok=True)
    (dst / "references").mkdir(parents=True, exist_ok=True)
    (dst / "agents").mkdir(parents=True, exist_ok=True)
    (dst / "assets").mkdir(parents=True, exist_ok=True)

    (dst / "SKILL.md").write_text(DELEGATE_SKILL_MD, encoding="utf-8", newline="\n")
    (dst / "agents" / "openai.yaml").write_text(DELEGATE_OPENAI_YAML, encoding="utf-8", newline="\n")
    icon_src = core_src / "assets" / "icon.svg"
    copied = 2
    if icon_src.is_file():
        shutil.copyfile(icon_src, dst / "assets" / "icon.svg")
        copied += 1
    for script_name in DELEGATE_REQUIRED_SCRIPTS:
        src_script = core_src / "scripts" / script_name
        if not src_script.is_file():
            raise FileNotFoundError(f"missing required delegate script: {src_script}")
        shutil.copyfile(src_script, dst / "scripts" / script_name)
        copied += 1
    for ref_name in DELEGATE_REQUIRED_REFERENCES:
        src_ref = core_src / "references" / ref_name
        if not src_ref.is_file():
            raise FileNotFoundError(f"missing required delegate reference: {src_ref}")
        shutil.copyfile(src_ref, dst / "references" / ref_name)
        copied += 1

    marker = {
        "source_repo": str(repo_root.resolve()),
        "source_skill": "skills/academic-writing-skills#manuscript-delegate-pass",
        "skill_version": version,
        "file_count": copied,
    }
    (dst / MARKER_NAME).write_text(json.dumps(marker, indent=2) + "\n", encoding="utf-8", newline="\n")
    return {"shim": DELEGATE_ALIAS_NAME, "dest": str(dst), "version": version, "files": copied}


def install_shims(
    repo_root: Path,
    dest_dir: Path,
    include_locales: bool = False,
    include_delegate_alias: bool = True,
    force: bool = False,
) -> list[dict[str, object]]:
    """Copy nested skills/<name>/ trees into one-level <dest>/<shim>/ directories safely."""
    plugin = json.loads((repo_root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    version = plugin["version"]
    mapping = dict(DEFAULT_SHIMS)
    if include_locales:
        mapping.update(LOCALE_SHIMS)
    else:
        # Auto-refresh any managed locale shims already present in dest_dir to prevent version skew
        for loc_shim, loc_src in LOCALE_SHIMS.items():
            if (dest_dir / loc_shim / MARKER_NAME).is_file():
                mapping[loc_shim] = loc_src

    pairs: list[tuple[str, str, Path, Path]] = []
    for shim_name, source_name in mapping.items():
        src = repo_root / "skills" / source_name
        if not (src / "SKILL.md").is_file():
            raise FileNotFoundError(f"missing source SKILL.md: {src / 'SKILL.md'}")
        dst = dest_dir / shim_name
        src_res, dst_res = src.resolve(), dst.resolve()
        if dst_res == src_res or dst_res in src_res.parents or src_res in dst_res.parents:
            raise ValueError(f"refusing overlapping source and destination paths: {src} -> {dst}")
        pairs.append((shim_name, source_name, src, dst))

    dest_dir.mkdir(parents=True, exist_ok=True)

    installed: list[dict[str, object]] = []
    for shim_name, source_name, src, dst in pairs:
        count = _copy_tree(src, dst, force=force)
        marker = {
            "source_repo": str(repo_root.resolve()),
            "source_skill": f"skills/{source_name}",
            "skill_version": version,
            "file_count": count,
        }
        (dst / MARKER_NAME).write_text(json.dumps(marker, indent=2) + "\n", encoding="utf-8", newline="\n")
        installed.append({"shim": shim_name, "dest": str(dst), "version": version, "files": count})

    if include_delegate_alias:
        installed.append(_install_delegate_alias(repo_root, dest_dir, version=version, force=force))
    return installed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dest", type=Path, required=True, help="Target ~/.agents/skills directory")
    parser.add_argument("--include-locales", action="store_true")
    parser.add_argument("--no-delegate-alias", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    result = install_shims(
        args.root,
        args.dest,
        include_locales=args.include_locales,
        include_delegate_alias=not args.no_delegate_alias,
        force=args.force,
    )
    print(json.dumps({"status": "PASS", "installed": result}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
