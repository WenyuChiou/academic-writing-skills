#!/usr/bin/env python3
"""Install one-level flat skill discovery shims for hosts that only scan top-level skill directories."""

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
MARKER_NAME = ".flat_shim_origin.json"


def _copy_tree(src: Path, dst: Path) -> int:
    if dst.exists():
        if not (dst / MARKER_NAME).is_file():
            raise RuntimeError(f"refusing to overwrite unmanaged directory: {dst}")
        shutil.rmtree(dst)
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


def install_shims(repo_root: Path, dest_dir: Path, include_locales: bool = False, force: bool = False) -> list[dict[str, object]]:
    """Copy nested skills/<name>/ trees into one-level <dest>/<shim>/ directories safely."""
    plugin = json.loads((repo_root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    version = plugin["version"]
    mapping = dict(DEFAULT_SHIMS)
    if include_locales:
        mapping.update(LOCALE_SHIMS)

    dest_dir.mkdir(parents=True, exist_ok=True)
    installed: list[dict[str, object]] = []
    for shim_name, source_name in mapping.items():
        src = repo_root / "skills" / source_name
        if not (src / "SKILL.md").is_file():
            raise FileNotFoundError(f"missing source SKILL.md: {src / 'SKILL.md'}")
        dst = dest_dir / shim_name
        if dst.exists() and force and not (dst / MARKER_NAME).is_file():
            shutil.rmtree(dst)
        count = _copy_tree(src, dst)
        marker = {
            "source_repo": str(repo_root.resolve()),
            "source_skill": f"skills/{source_name}",
            "skill_version": version,
            "file_count": count,
        }
        (dst / MARKER_NAME).write_text(json.dumps(marker, indent=2) + "\n", encoding="utf-8")
        installed.append({"shim": shim_name, "dest": str(dst), "version": version, "files": count})
    return installed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dest", type=Path, required=True, help="Target ~/.agents/skills directory")
    parser.add_argument("--include-locales", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    result = install_shims(args.root, args.dest, include_locales=args.include_locales, force=args.force)
    print(json.dumps({"status": "PASS", "installed": result}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
