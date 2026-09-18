"""Portable adapter integrity and extraction regression tests."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
from types import SimpleNamespace
import zipfile

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_adapter_bundle", ROOT / "scripts" / "build_adapter_bundle.py"
)
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


@pytest.fixture
def bundle(tmp_path: Path) -> Path:
    """Copy only the declared bundle, so tests also exercise portability."""
    root = tmp_path / "bundle"
    manifest = json.loads((ROOT / "adapter.json").read_text(encoding="utf-8"))
    for name in ["adapter.json", *manifest["files"]]:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    return root


def edit_manifest(root: Path, change) -> None:
    target = root / "adapter.json"
    manifest = json.loads(target.read_text(encoding="utf-8"))
    change(manifest)
    target.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def run_script(root: Path, script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-B", "-S", str(root / script), *args],
        cwd=root,
        text=True,
        capture_output=True,
        timeout=20,
        check=False,
    )


@pytest.mark.parametrize("first,second", [
    ("references/Collision.md", "references/collision.md/item.md"),
    ("references/Dir/a.md", "references/dir/b.md"),
    ("references/node/a.md", "references/node"),
    ("references/node", "references/node/a.md"),
])
def test_portable_prefix_collisions(first, second):
    nodes = {}
    builder.register_portable_node(nodes, first)
    with pytest.raises(builder.AdapterError, match="path collision"):
        builder.register_portable_node(nodes, second)


def test_binary_assets_are_not_git_text():
    names = [f"skills/paper-review/assets/example.{suffix}" for suffix in ("png", "jpg", "PNG", "JpG")]
    result = subprocess.run(["git", "-c", "core.ignorecase=false", "check-attr", "text", "--", *names], cwd=ROOT, text=True, capture_output=True, check=True)
    assert result.stdout.count("text: unset") == len(names)


def test_valid_manifest_and_complete_bundle(bundle: Path) -> None:
    manifest, files = builder.verify_bundle(bundle)
    assert manifest["skill_version"] == "1.1.6"
    assert manifest["state_schema_version"] == "1.1"
    assert {skill["mode"] for skill in manifest["skills"]} == {"write-proposals", "review-only"}
    assert set(files) == {"adapter.json", *manifest["files"]}
    assert builder.skill_closure(bundle) <= set(files)


def test_check_is_read_only(bundle: Path) -> None:
    before = {p.relative_to(bundle): (p.stat().st_mtime_ns, p.read_bytes())
              for p in bundle.rglob("*") if p.is_file()}
    result = run_script(bundle, "scripts/build_adapter_bundle.py", "--check")
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["status"] == "PASS"
    after = {p.relative_to(bundle): (p.stat().st_mtime_ns, p.read_bytes())
             for p in bundle.rglob("*") if p.is_file()}
    assert before == after


def test_tampered_file_fails_before_output(bundle: Path, tmp_path: Path) -> None:
    (bundle / "skills/paper-review/SKILL.md").write_text("tampered", encoding="utf-8")
    output = tmp_path / "invalid.zip"
    with pytest.raises(builder.AdapterError, match="SHA256 mismatch"):
        builder.build_bundle(bundle, output)
    assert not output.exists()


def test_missing_file_fails(bundle: Path) -> None:
    (bundle / "skills/paper-review/assets/icon.svg").unlink()
    with pytest.raises(builder.AdapterError, match="missing or non-regular file"):
        builder.verify_bundle(bundle)


@pytest.mark.parametrize("name", [
    "../outside.md", "/outside.md", "C:/outside.md", "skills/../outside.md",
    "skills\\paper-review\\SKILL.md", "skills//paper-review/SKILL.md",
    "skills/paper-review/references/CON.md", "skills/paper-review/references/x.md.",
    "skills/paper-review/references/x.md:stream", "skills/paper-review/references/x\n.md",
])
def test_unsafe_manifest_paths_fail(bundle: Path, name: str) -> None:
    edit_manifest(bundle, lambda data: data["files"].update({name: "0" * 64}))
    with pytest.raises(builder.AdapterError, match="unsafe relative path"):
        builder.verify_bundle(bundle)


@pytest.mark.parametrize("name", [
    ".env", "secrets/token.json", "skills/paper-review/references/.env",
    "skills/paper-review/assets/credentials.json", "skills/paper-review/assets/key.pem",
    "skills/academic-writing-skills/scripts/__pycache__/audit.pyc",
])
def test_nonpublic_paths_cannot_be_declared(bundle: Path, name: str) -> None:
    edit_manifest(bundle, lambda data: data["files"].update({name: "0" * 64}))
    with pytest.raises(builder.AdapterError):
        builder.verify_bundle(bundle)


def test_omitted_dependency_and_added_public_file_fail(bundle: Path) -> None:
    edit_manifest(bundle, lambda data: data["files"].pop("skills/paper-review/assets/icon.svg"))
    with pytest.raises(builder.AdapterError, match="incomplete public closure"):
        builder.verify_bundle(bundle)


def test_unlisted_dependency_fails(bundle: Path) -> None:
    (bundle / "skills/paper-review/references/new-module.md").write_text("new", encoding="utf-8")
    with pytest.raises(builder.AdapterError, match="incomplete public closure"):
        builder.verify_bundle(bundle)


def test_duplicate_keys_fail(bundle: Path) -> None:
    target = bundle / "adapter.json"
    target.write_text('{"schema_version": 1, "schema_version": 1}', encoding="utf-8")
    with pytest.raises(builder.AdapterError, match="duplicate JSON key"):
        builder.verify_bundle(bundle)


@pytest.mark.parametrize("field,value", [
    ("schema_version", True), ("schema_version", 2), ("adapter_version", "2.0.0"),
    ("state_schema_version", "9"), ("skill_version", "9.0.0"),
])
def test_metadata_mismatch_fails(bundle: Path, field: str, value) -> None:
    edit_manifest(bundle, lambda data: data.update({field: value}))
    with pytest.raises(builder.AdapterError):
        builder.verify_bundle(bundle)


def test_manifest_cannot_replace_operation_or_grant_authority(bundle: Path) -> None:
    edit_manifest(bundle, lambda data: data["operations"]["state"].update({"script": "evil.py"}))
    with pytest.raises(builder.AdapterError, match="operation contract mismatch"):
        builder.verify_bundle(bundle)


def test_review_authority_must_remain_read_only(bundle: Path) -> None:
    edit_manifest(bundle, lambda data: data["skills"][1].update({"mode": "write-proposals"}))
    with pytest.raises(builder.AdapterError, match="authority modes"):
        builder.verify_bundle(bundle)


@pytest.mark.parametrize("component", ["bundle", "skills", "SKILL.md"])
@pytest.mark.parametrize("kind", ["symlink", "reparse"])
def test_link_components_fail_on_all_platforms(
    bundle: Path, monkeypatch, component: str, kind: str,
) -> None:
    original = Path.lstat
    target = {"bundle": bundle, "skills": bundle / "skills",
              "SKILL.md": bundle / "skills/paper-review/SKILL.md"}[component]

    def linked(path: Path, *args, **kwargs):
        if path == target:
            return SimpleNamespace(
                st_mode=stat.S_IFLNK if kind == "symlink" else stat.S_IFDIR,
                st_file_attributes=0x400 if kind == "reparse" else 0,
            )
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "lstat", linked)
    with pytest.raises(builder.AdapterError, match="symlink or reparse point"):
        builder.verify_bundle(bundle)


def test_native_symlink_is_rejected(bundle: Path, tmp_path: Path) -> None:
    target = bundle / "skills/paper-review/references/link.md"
    outside = tmp_path / "outside.md"
    outside.write_text("outside", encoding="utf-8")
    try:
        target.symlink_to(outside)
    except OSError as exc:
        pytest.skip(f"native symlink creation unavailable: {exc}")
    with pytest.raises(builder.AdapterError, match="symlink or reparse point"):
        builder.verify_bundle(bundle)


def test_deterministic_archive_and_nonoverwriting_output(bundle: Path, tmp_path: Path) -> None:
    first, second = tmp_path / "first.zip", tmp_path / "second.zip"
    first_report = builder.build_bundle(bundle, first)
    for source in bundle.rglob("*"):
        if source.is_file():
            os.utime(source, (1700000000, 1700000000))
    second_report = builder.build_bundle(bundle, second)
    assert first.read_bytes() == second.read_bytes()
    assert first_report["bundle_sha256"] == second_report["bundle_sha256"]
    original = first.read_bytes()
    with pytest.raises(FileExistsError):
        builder.build_bundle(bundle, first)
    assert first.read_bytes() == original
    with zipfile.ZipFile(first) as archive:
        manifest = json.loads(archive.read("adapter.json"))
        assert archive.namelist() == sorted(["adapter.json", *manifest["files"]])
        for entry in archive.infolist():
            assert entry.date_time == (1980, 1, 1, 0, 0, 0)
            assert stat.S_ISREG(entry.external_attr >> 16)
            if entry.filename != "adapter.json":
                assert hashlib.sha256(archive.read(entry)).hexdigest() == manifest["files"][entry.filename]


def test_extracted_bundle_passes_actual_offline_regression(bundle: Path, tmp_path: Path) -> None:
    output = tmp_path / "adapter.zip"
    builder.build_bundle(bundle, output)
    extracted = tmp_path / "extracted"
    with zipfile.ZipFile(output) as archive:
        archive.extractall(extracted)
    result = run_script(extracted, "scripts/build_adapter_bundle.py", "--check")
    assert result.returncode == 0, result.stdout + result.stderr
    result = run_script(extracted, f"{builder.CORE}/scripts/run_regression_tests.py")
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "PASS"
    assert len(report["tests"]) == 22


@pytest.mark.parametrize("operation", ["state", "consistency", "prose", "candidate", "docx"])
def test_declared_arguments_match_actual_script_help(bundle: Path, operation: str) -> None:
    manifest = json.loads((bundle / "adapter.json").read_text(encoding="utf-8"))
    contract = manifest["operations"][operation]
    result = run_script(bundle, contract["script"], "--help")
    assert result.returncode == 0, result.stdout + result.stderr
    for option in contract["arguments"]["options"]:
        assert option.split()[0] in result.stdout


def test_cache_is_excluded_from_archive(bundle: Path, tmp_path: Path) -> None:
    cache = bundle / "skills/academic-writing-skills/scripts/__pycache__"
    cache.mkdir()
    (cache / "local.pyc").write_bytes(b"cache")
    output = tmp_path / "without-cache.zip"
    builder.build_bundle(bundle, output)
    with zipfile.ZipFile(output) as archive:
        assert not any("__pycache__" in name for name in archive.namelist())
