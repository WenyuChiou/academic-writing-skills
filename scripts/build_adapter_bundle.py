#!/usr/bin/env python3
"""Verify the public writing adapter and optionally create a deterministic ZIP.

The manifest describes files and argument contracts, never executable commands.
This tool requires only Python's standard library and never imports audit scripts.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import zipfile


SKILLS = {
    "academic-writing-skills": "write-proposals",
    "paper-review": "review-only",
}
CORE = "skills/academic-writing-skills"
OPERATIONS = {
    "state": "audit_manuscript_state.py",
    "consistency": "audit_text_consistency.py",
    "prose": "audit_prose_patterns.py",
    "candidate": "audit_candidate_text.py",
    "docx": "audit_docx_structure.py",
    "regression": "run_regression_tests.py",
}
ENTRYPOINTS = {
    "state_template": f"{CORE}/assets/manuscript_state_template.json",
    "initialize_state": f"{CORE}/scripts/init_manuscript_state.py",
}
PUBLIC_EXTRAS = {
    ".claude-plugin/plugin.json",
    "LICENSE",
    "scripts/build_adapter_bundle.py",
    "docs/workspace-adapter.md",
}
CACHE_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
SECRET_PARTS = {"secrets", "credentials", "private", "id_rsa", "id_ed25519"}
PUBLIC_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".svg", ".png", ".jpg", ".txt"}
RESERVED_NAMES = {"con", "prn", "aux", "nul"} | {
    f"{prefix}{number}" for prefix in ("com", "lpt") for number in range(1, 10)
}


class AdapterError(ValueError):
    """The bundle or manifest does not satisfy the public adapter contract."""


def validate_path(name: str) -> None:
    """Require unambiguous portable relative paths, including on Windows."""
    if not isinstance(name, str) or not name:
        raise AdapterError("file path must be a nonempty string")
    for part in name.split("/"):
        if (
            part in {"", ".", ".."}
            or not re.fullmatch(r"[A-Za-z0-9_.-]+", part)
            or part.endswith(".")
            or part.split(".")[0].lower() in RESERVED_NAMES
        ):
            raise AdapterError(f"unsafe relative path: {name}")


def reject_links(path: Path) -> None:
    """Reject links and Windows reparse points in every existing component."""
    for item in (*reversed(path.parents), path):
        try:
            info = item.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or (
            getattr(info, "st_file_attributes", 0)
            & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        ):
            raise AdapterError(f"symlink or reparse point is not allowed: {item}")


def public_path(name: str) -> None:
    """Restrict declared inputs to public skill material and named extras."""
    validate_path(name)
    if name in PUBLIC_EXTRAS:
        return
    parts = name.split("/")
    if len(parts) < 3 or parts[0] != "skills" or parts[1] not in SKILLS:
        raise AdapterError(f"undeclared public area: {name}")
    if len(parts) == 3 and parts[2] == "SKILL.md":
        return
    if len(parts) < 4 or parts[2] not in {"scripts", "references", "assets", "agents"}:
        raise AdapterError(f"unsupported skill file: {name}")
    for part in parts[2:]:
        lower = part.lower()
        if lower.startswith(".") or lower in CACHE_PARTS or lower.split(".")[0] in SECRET_PARTS:
            raise AdapterError(f"secret, hidden, or cache path is not public: {name}")
    if Path(name).suffix.lower() not in PUBLIC_SUFFIXES:
        raise AdapterError(f"unsupported public file type: {name}")


def read_file(root: Path, name: str) -> bytes:
    """Read a regular in-root file after checking its entire path."""
    validate_path(name)
    target = root.joinpath(*name.split("/"))
    reject_links(target)
    if not target.resolve().is_relative_to(root):
        raise AdapterError(f"path escapes bundle root: {name}")
    if not target.is_file():
        raise AdapterError(f"missing or non-regular file: {name}")
    with target.open("rb") as source:
        if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
            raise AdapterError(f"non-regular file: {name}")
        return source.read()


def read_object(raw: bytes, label: str) -> dict:
    """Read a JSON object without accepting ambiguous duplicate keys."""
    def unique(pairs: list[tuple[str, object]]) -> dict:
        result = {}
        for key, value in pairs:
            if key in result:
                raise AdapterError(f"duplicate JSON key in {label}: {key}")
            result[key] = value
        return result

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise AdapterError(f"invalid JSON in {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise AdapterError(f"{label} must contain a JSON object")
    return value


def argument_contract(operation: str) -> dict:
    """Return the existing script's declarative positional and option syntax."""
    if operation == "regression":
        return {"positional": [], "options": []}
    if operation == "candidate":
        return {
            "positional": ["state", "candidate"],
            "options": ["--label LABEL", "--json"],
        }
    if operation == "docx":
        return {
            "positional": ["docx [docx ...]"],
            "options": ["--require-clean", "--require-valid-comments", "--json"],
        }
    return {"positional": ["state"], "options": ["--project-root PROJECT_ROOT", "--json"]}


def skill_closure(root: Path) -> set[str]:
    """Discover both complete public skill trees without following links."""
    paths = set()
    for skill in SKILLS:
        base = root / "skills" / skill
        reject_links(base)
        paths.add(f"skills/{skill}/SKILL.md")
        for directory in ("scripts", "references", "assets", "agents"):
            start = base / directory
            reject_links(start)
            if not start.exists():
                continue
            if not start.is_dir():
                raise AdapterError(f"expected skill directory: {start}")
            for current, dirs, files in os.walk(start, followlinks=False):
                current_path = Path(current)
                for name in dirs + files:
                    reject_links(current_path / name)
                dirs[:] = [name for name in dirs if name not in CACHE_PARTS]
                for name in files:
                    if name.endswith((".pyc", ".pyo")):
                        continue
                    relative = (current_path / name).relative_to(root).as_posix()
                    public_path(relative)
                    paths.add(relative)
    return paths


def register_portable_node(nodes: dict, name: str) -> None:
    """Reject case aliases and file/directory conflicts at every path prefix."""
    parts = name.split("/")
    for index in range(1, len(parts) + 1):
        prefix = "/".join(parts[:index])
        kind = "file" if index == len(parts) else "directory"
        node = (prefix, kind)
        if nodes.setdefault(prefix.casefold(), node) != node:
            raise AdapterError(f"case or file/directory path collision: {prefix}")


def verify_bundle(root: Path) -> tuple[dict, dict[str, bytes]]:
    """Validate metadata, closure and hashes; return exactly the verified bytes."""
    root = root.absolute()
    reject_links(root)
    root = root.resolve(strict=True)
    manifest_raw = read_file(root, "adapter.json")
    manifest = read_object(manifest_raw, "adapter.json")
    if type(manifest.get("schema_version")) is not int or manifest["schema_version"] != 1:
        raise AdapterError("unsupported adapter schema_version")
    if manifest.get("id") != "academic-writing-skills":
        raise AdapterError("unexpected adapter id")
    if manifest.get("adapter_version") != "1.0.0":
        raise AdapterError("unsupported adapter_version")
    if manifest.get("state_schema_version") != "1.1":
        raise AdapterError("unsupported state_schema_version")
    expected_skills = [
        {"id": skill, "path": f"skills/{skill}/SKILL.md", "mode": mode}
        for skill, mode in SKILLS.items()
    ]
    if manifest.get("skills") != expected_skills:
        raise AdapterError("skill paths or authority modes differ from the contract")
    if manifest.get("entrypoints") != ENTRYPOINTS:
        raise AdapterError("entrypoints differ from existing template and initializer")
    operations = manifest.get("operations")
    if not isinstance(operations, dict) or set(operations) != set(OPERATIONS):
        raise AdapterError("the six named operations are required")
    for name, filename in OPERATIONS.items():
        expected = {
            "script": f"{CORE}/scripts/{filename}",
            "arguments": argument_contract(name),
            "json_output": {
                "supported": True,
                "flag": None if name == "regression" else "--json",
                "default": name == "regression",
            },
            "success_exit_code": 0,
        }
        if operations[name] != expected:
            raise AdapterError(f"operation contract mismatch: {name}")
    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        raise AdapterError("files must map public relative paths to SHA256 values")
    folded = set()
    portable_nodes = {}
    verified = {"adapter.json": manifest_raw}
    for name, expected_hash in files.items():
        public_path(name)
        if name.casefold() in folded:
            raise AdapterError(f"case-colliding file path: {name}")
        folded.add(name.casefold())
        register_portable_node(portable_nodes, name)
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            raise AdapterError(f"invalid SHA256: {name}")
        raw = read_file(root, name)
        if hashlib.sha256(raw).hexdigest() != expected_hash:
            raise AdapterError(f"SHA256 mismatch: {name}")
        verified[name] = raw
    required = skill_closure(root) | PUBLIC_EXTRAS
    if set(files) != required:
        raise AdapterError(
            f"incomplete public closure; missing={sorted(required - set(files))}; "
            f"extra={sorted(set(files) - required)}"
        )
    plugin = read_object(verified[".claude-plugin/plugin.json"], "plugin.json")
    if manifest.get("skill_version") != plugin.get("version") or not plugin.get("version"):
        raise AdapterError("skill_version does not match plugin version")
    template = read_object(verified[ENTRYPOINTS["state_template"]], "state template")
    if template.get("schema_version") != manifest["state_schema_version"]:
        raise AdapterError("template schema does not match state_schema_version")
    return manifest, verified


def build_bundle(root: Path, output: Path | None = None) -> dict:
    """Verify a bundle, optionally creating an exclusive deterministic archive."""
    manifest, verified = verify_bundle(root)
    report = {
        "status": "PASS",
        "id": manifest["id"],
        "adapter_version": manifest["adapter_version"],
        "skill_version": manifest["skill_version"],
        "verified_files": len(verified) - 1,
        "manifest_sha256": hashlib.sha256(verified["adapter.json"]).hexdigest(),
    }
    if output is not None:
        output = output.absolute()
        reject_links(output)
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED) as archive:
            for name, raw in sorted(verified.items()):
                entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                entry.create_system = 3
                entry.external_attr = (stat.S_IFREG | 0o644) << 16
                archive.writestr(entry, raw)
        payload = buffer.getvalue()
        # Exclusive creation also protects against a destination appearing mid-build.
        with output.open("xb") as target:
            target.write(payload)
        report["output"] = str(output)
        report["bundle_sha256"] = hashlib.sha256(payload).hexdigest()
    return report


def main(argv: list[str] | None = None) -> int:
    """Run verification/build and emit a machine-readable report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).absolute().parents[1])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="verify without writing anything")
    mode.add_argument("--output", type=Path, help="create a new ZIP; never overwrite")
    args = parser.parse_args(argv)
    try:
        report = build_bundle(args.root, args.output)
    except (AdapterError, OSError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, indent=2))
        return 2
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
