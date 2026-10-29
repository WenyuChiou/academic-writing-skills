#!/usr/bin/env python3
"""Read-only locale integrity checks; hashes never certify translation meaning."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
from collections import Counter
from urllib.parse import unquote

BASES = ("academic-writing-skills", "paper-review")
LOCALES = {"zh-TW": "zh-tw", "zh-CN": "zh-cn"}

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result

def safe_file(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ValueError("invalid locale path")
    parts = PurePosixPath(relative).parts
    if PurePosixPath(relative).is_absolute() or any(p in {".", "..", ""} for p in relative.split("/")):
        raise ValueError("unsafe locale path")
    target = root.joinpath(*parts)
    for item in (target, *target.parents):
        if item == root.parent:
            break
        if item.is_symlink() or (hasattr(item, "is_junction") and item.is_junction()):
            raise ValueError("locale links are not allowed")
    if not target.resolve().is_relative_to(root.resolve()) or not target.is_file():
        raise ValueError(f"missing or outside locale file: {relative}")
    return target

def fences(text: str) -> list[str]:
    return re.findall(r"^```[^\n]*\n.*?^```[^\n]*(?:\n|$)", text, re.M | re.S)

def codes(text: str, suffix: str = "") -> list[str]:
    if suffix:
        for name in BASES:
            text = text.replace(f"`{name}-{suffix}`", f"`{name}`")
    # A Markdown inline span may wrap across lines; the line break renders as
    # a space. Fenced executable blocks have a separate exact-byte check.
    return [value.replace("\n", " ") for value in re.findall(r"`[^`]+`", prose(text), re.S)]

def prose(text: str) -> str:
    return re.sub(r"^```[^\n]*\n.*?^```[^\n]*(?:\n|$)", "", text, flags=re.M|re.S)

def anchors(text: str) -> set[str]:
    text = prose(text)
    result = set(re.findall(r'<a\s+id="([^"]+)"', text))
    counts = Counter()
    for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.M):
        slug = re.sub(r"[^\w\s-]", "", heading.strip().rstrip("#").strip().lower())
        slug = re.sub(r"\s+", "-", slug)
        number = counts[slug]
        result.add(slug + (f"-{number}" if number else ""))
        counts[slug] += 1
    return result

def missing_case_examples(english: str, translated: str) -> list[str]:
    """English editing examples remain usable English, including wrapped quotes."""
    source = re.sub(r"`[^`]+`", "", prose(english), flags=re.S)
    normalize = lambda value: re.sub(r"\s+", " ", value).strip()
    target = normalize(translated)
    missing = []
    for match in re.finditer(r'"([^\"]+)"|“([^”]+)”', source, re.S):
        value = normalize(match.group(1) or match.group(2))
        if re.search(r"[A-Za-z]", value) and value not in target:
            missing.append(value)
    return missing

def reject_resource_links(root: Path, path: Path) -> None:
    """Check every lexical component before traversing a resource tree."""
    for item in (path, *path.parents):
        if item == root.parent:
            break
        try:
            info = item.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or (
            getattr(info, "st_file_attributes", 0)
            & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        ):
            raise ValueError(f"linked or reparse resource is not allowed: {item}")
    if not path.resolve().is_relative_to(root):
        raise ValueError(f"resource escapes locale root: {path}")

def resource_tree(root: Path, start: Path) -> tuple[dict[str, Path], set[str]]:
    """Exact regular-file and directory inventory, without following links."""
    reject_resource_links(root, start)
    files, directories = {}, set()
    if not start.exists():
        return files, directories
    if not start.is_dir():
        raise ValueError(f"resource area is not a directory: {start}")
    caches = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    def enumeration_error(error):
        raise error
    for current, children, names in os.walk(start, topdown=True, followlinks=False, onerror=enumeration_error):
        current = Path(current)
        reject_resource_links(root, current)
        directories.add(current.relative_to(start).as_posix())
        # Inspect entries before os.walk can descend into a Windows junction.
        for name in children + names:
            reject_resource_links(root, current / name)
        children[:] = [name for name in children if name not in caches]
        for name in names:
            path = current / name
            if path.suffix in {".pyc", ".pyo"}:
                continue
            files[path.relative_to(start).as_posix()] = safe_file(root, path.relative_to(root).as_posix())
    return files, directories

def check(root: Path) -> dict:
    root = root.resolve()
    findings = []
    checked = 0
    try:
        manifest = json.loads(safe_file(root, "locales/translation-manifest.json").read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        if not isinstance(manifest, dict) or manifest.get("schema_version") != 1 or set(manifest.get("locales", [])) != set(LOCALES):
            raise ValueError("unsupported localization manifest")
        if not re.fullmatch(r"[0-9a-f]{40}", manifest.get("source_revision", "")):
            raise ValueError("missing immutable source revision")
        expected = set()
        for base in BASES:
            source_root = root / "skills" / base
            for source in [source_root / "SKILL.md", *sorted((source_root / "references").rglob("*.md"))]:
                rel = source.relative_to(root).as_posix()
                for locale, suffix in LOCALES.items():
                    expected.add((locale, rel, rel.replace(f"skills/{base}/", f"skills/{base}-{suffix}/", 1)))
        actual = set()
        for entry in manifest.get("translations", []):
            key = (entry["locale"], entry["source"], entry["target"])
            if key in actual or key not in expected:
                raise ValueError("duplicate or unexpected translation record")
            actual.add(key)
            source = safe_file(root, entry["source"])
            target = safe_file(root, entry["target"])
            if digest(source.read_bytes()) != entry["source_sha256"]:
                findings.append({"path":entry["target"], "check":"stale-source"})
            if digest(target.read_bytes()) != entry["target_sha256"]:
                findings.append({"path":entry["target"], "check":"changed-target"})
            english = source.read_text(encoding="utf-8")
            translated = target.read_text(encoding="utf-8")
            if not re.search(r"[\u3400-\u9fff]", translated):
                findings.append({"path":entry["target"], "check":"missing-Chinese-prose"})
            if fences(english) != fences(translated):
                findings.append({"path":entry["target"], "check":"changed-fenced-example"})
            suffix = LOCALES[entry["locale"]]
            if Counter(codes(english)) != Counter(codes(translated, suffix)):
                findings.append({"path":entry["target"], "check":"changed-inline-code"})
            if source.name.endswith("-cases.md"):
                for example in missing_case_examples(english, translated):
                    findings.append({"path":entry["target"], "check":"changed-English-editing-example", "example":example})
            # Templates can contain illustrative paths; only real prose links resolve.
            english_prose, target_prose = prose(english), prose(translated)
            original_links = re.findall(r"\]\(([^\n)]+)\)", english_prose)
            target_links = re.findall(r"\]\(([^\n)]+)\)", target_prose)
            if Counter(original_links) != Counter(target_links):
                findings.append({"path":entry["target"], "check":"changed-link-target"})
            for link in target_links:
                if "://" in link or link.startswith("mailto:"):
                    continue
                path, _, fragment = link.partition("#")
                linked = target.parent / unquote(path) if path else target
                if not linked.resolve().is_relative_to(root):
                    findings.append({"path":entry["target"], "check":"unsafe-local-reference", "target":link})
                elif not linked.is_file():
                    findings.append({"path":entry["target"], "check":"missing-local-reference", "target":link})
                elif fragment and linked.suffix.lower() == ".md" and unquote(fragment) not in anchors(linked.read_text(encoding="utf-8")):
                    findings.append({"path":entry["target"], "check":"missing-local-anchor", "target":link})
            checked += 1
        if actual != expected:
            raise ValueError("translation coverage is incomplete")
        for base in BASES:
            for suffix in LOCALES.values():
                localized = root / "skills" / f"{base}-{suffix}"
                front = (localized / "SKILL.md").read_text(encoding="utf-8").split("---",2)[1]
                if f"name: {base}-{suffix}\n" not in front:
                    findings.append({"path":str(localized), "check":"wrong-skill-identity"})
                for section in ("scripts", "assets"):
                    original = root / "skills" / base / section
                    source_files, source_dirs = resource_tree(root, original)
                    target_files, target_dirs = resource_tree(root, localized / section)
                    for name in sorted(source_dirs ^ target_dirs):
                        findings.append({"path":str(localized / section / name), "check":"resource-directory-drift"})
                    for name in sorted(target_files.keys() - source_files.keys()):
                        findings.append({"path":str(target_files[name]), "check":"unexpected-runtime-or-asset"})
                    for name, resource in source_files.items():
                        mirror = localized / section / name
                        if name not in target_files:
                            findings.append({"path":str(mirror), "check":"runtime-or-asset-drift"})
                            continue
                        reject_resource_links(root, resource)
                        reject_resource_links(root, target_files[name])
                        if target_files[name].read_bytes() != resource.read_bytes():
                            findings.append({"path":str(mirror), "check":"runtime-or-asset-drift"})
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        findings.append({"check":"manifest-or-path-error", "detail":str(exc)})
    return {"status":"pass" if not findings else "fail", "translations_checked":checked,
            "findings":findings, "verification_scope":"identity, coverage, protected material and source freshness; semantic fidelity and actual review remain unverified by this checker"}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = check(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 2

if __name__ == "__main__":
    raise SystemExit(main())
