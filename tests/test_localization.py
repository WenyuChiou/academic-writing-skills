"""Locale structural/failure checks, not a substitute for bilingual review."""
import hashlib
import importlib.util
import json
import re
from collections import Counter
from types import SimpleNamespace
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("locale_check", ROOT / "scripts/check_localizations.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

@pytest.fixture
def locale_tree(tmp_path):
    entries = []
    for base in checker.BASES:
        source = tmp_path / "skills" / base
        (source / "references").mkdir(parents=True)
        (source / "SKILL.md").write_text(f"---\nname: {base}\ndescription: Source.\n---\n# Source\n\nKeep `value` and [guide](references/guide.md).\n\n```json\n{{\"key\": \"value\"}}\n```\n", encoding="utf-8")
        (source / "references/guide.md").write_text("# Guide\n\nScope is not permission.\n", encoding="utf-8")
        for locale, suffix in checker.LOCALES.items():
            target = tmp_path / "skills" / f"{base}-{suffix}"
            (target / "references").mkdir(parents=True)
            (target / "SKILL.md").write_text(f"---\nname: {base}-{suffix}\ndescription: 中文指引。\n---\n# 中文指引\n\n保留 `value` 與 [guide](references/guide.md)。\n\n```json\n{{\"key\": \"value\"}}\n```\n", encoding="utf-8")
            (target / "references/guide.md").write_text("# 指引\n\n處理範圍不等於修改權限。\n", encoding="utf-8")
            for relative in ("SKILL.md", "references/guide.md"):
                original, localized = source / relative, target / relative
                entries.append({"locale":locale, "source":original.relative_to(tmp_path).as_posix(),
                    "target":localized.relative_to(tmp_path).as_posix(), "source_sha256":sha(original), "target_sha256":sha(localized)})
    (tmp_path / "locales").mkdir()
    manifest = {"schema_version":1,"source_revision":"1"*40,"locales":list(checker.LOCALES),"translations":entries}
    (tmp_path / "locales/translation-manifest.json").write_text(json.dumps(manifest),encoding="utf-8")
    return tmp_path

def test_complete_locale_fixture_passes_without_claiming_semantics(locale_tree):
    report = checker.check(locale_tree)
    assert report["status"] == "pass" and report["translations_checked"] == 8
    assert "semantic fidelity" in report["verification_scope"]

def test_english_rule_change_marks_locales_stale(locale_tree):
    source = locale_tree / "skills/academic-writing-skills/references/guide.md"
    source.write_text(source.read_text(encoding="utf-8") + "\nNew condition.\n",encoding="utf-8")
    report = checker.check(locale_tree)
    assert report["status"] == "fail"
    assert sum(row["check"] == "stale-source" for row in report["findings"]) == 2

def test_changed_translation_is_not_silently_reapproved(locale_tree):
    target = locale_tree / "skills/paper-review-zh-cn/references/guide.md"
    target.write_text("# 中文\n\n已修改內容。\n",encoding="utf-8")
    assert any(row["check"] == "changed-target" for row in checker.check(locale_tree)["findings"])

@pytest.mark.parametrize("mutation", ["missing", "duplicate", "path", "locale"])
def test_manifest_coverage_and_paths_fail_closed(locale_tree, mutation):
    path = locale_tree / "locales/translation-manifest.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    if mutation == "missing":
        record["translations"].pop()
    elif mutation == "duplicate":
        record["translations"].append(record["translations"][0])
    elif mutation == "path":
        record["translations"][0]["target"] = "../outside.md"
    else:
        record["translations"][0]["locale"] = "other"
    path.write_text(json.dumps(record),encoding="utf-8")
    assert checker.check(locale_tree)["status"] == "fail"

def test_duplicate_json_keys_rejected(locale_tree):
    path = locale_tree / "locales/translation-manifest.json"
    path.write_text('{"schema_version":1,"schema_version":1}',encoding="utf-8")
    assert checker.check(locale_tree)["status"] == "fail"

@pytest.mark.parametrize("before,after,expected", [
    ('`value`','`renamed`','changed-inline-code'),
    ('"key": "value"','"key": "changed"','changed-fenced-example'),
    ('references/guide.md','references/missing.md','changed-link-target'),
])
def test_protected_material_cannot_change_even_after_rehash(locale_tree,before,after,expected):
    path = locale_tree / "locales/translation-manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    entry = manifest["translations"][0]
    target = locale_tree / entry["target"]
    target.write_text(target.read_text(encoding="utf-8").replace(before,after),encoding="utf-8")
    entry["target_sha256"] = sha(target)
    path.write_text(json.dumps(manifest),encoding="utf-8")
    assert any(row["check"] == expected for row in checker.check(locale_tree)["findings"])

def test_resource_mirrors_cannot_drift(locale_tree):
    original=locale_tree / "skills/academic-writing-skills/scripts/audit.py"
    original.parent.mkdir()
    original.write_text('print("canonical")\n',encoding="utf-8")
    report=checker.check(locale_tree)
    assert sum(row["check"] == "runtime-or-asset-drift" for row in report["findings"]) == 2

def test_unexpected_executable_is_rejected_even_when_source_has_no_scripts(locale_tree):
    path=locale_tree/'skills/paper-review-zh-cn/scripts/unexpected.py'
    path.parent.mkdir(parents=True)
    path.write_text('print("not canonical")\n',encoding='utf-8')
    assert any(row['check']=='unexpected-runtime-or-asset' for row in checker.check(locale_tree)['findings'])

def test_extra_empty_resource_directory_is_rejected(locale_tree):
    (locale_tree/'skills/paper-review-zh-tw/assets/unexpected-empty').mkdir(parents=True)
    assert any(row['check']=='resource-directory-drift' for row in checker.check(locale_tree)['findings'])

def test_unreadable_resource_inventories_never_count_as_empty(locale_tree,monkeypatch):
    areas=[]
    for name in ('academic-writing-skills','academic-writing-skills-zh-tw','academic-writing-skills-zh-cn'):
        area=locale_tree/'skills'/name/'scripts'
        area.mkdir(parents=True)
        (area/'canonical.py').write_text('print("canonical")\n',encoding='utf-8')
        areas.append(area)
    (areas[1]/'unexpected.py').write_text('print("not canonical")\n',encoding='utf-8')
    original_scandir=checker.os.scandir
    def denied(path):
        if Path(path) in areas:
            raise PermissionError('simulated unreadable resource inventory')
        return original_scandir(path)
    monkeypatch.setattr(checker.os,'scandir',denied)
    report=checker.check(locale_tree)
    assert report['status']=='fail'
    assert any('unreadable resource inventory' in row.get('detail','') for row in report['findings'])

@pytest.mark.parametrize('section',['scripts','assets'])
@pytest.mark.parametrize('side',['academic-writing-skills','academic-writing-skills-zh-tw'])
def test_resource_reparse_components_rejected_before_reads(locale_tree,monkeypatch,section,side):
    area=locale_tree/'skills'/side/section
    area.mkdir(parents=True)
    probe=area/'probe.py'
    probe.write_text('never read this resource',encoding='utf-8')
    original_stat=Path.lstat
    original_read=Path.read_bytes
    def reparse(path,*args,**kwargs):
        info=original_stat(path,*args,**kwargs)
        if path==area:
            return SimpleNamespace(st_mode=info.st_mode,st_file_attributes=0x400)
        return info
    def guarded_read(path,*args,**kwargs):
        assert path!=probe,'resource content read before reparse rejection'
        return original_read(path,*args,**kwargs)
    monkeypatch.setattr(Path,'lstat',reparse)
    monkeypatch.setattr(Path,'read_bytes',guarded_read)
    report=checker.check(locale_tree)
    assert report['status']=='fail'
    assert any('reparse resource' in row.get('detail','') for row in report['findings'])

def test_current_locales_are_complete_and_current():
    report=checker.check(ROOT)
    assert report["status"] == "pass", report["findings"]
    assert report["translations_checked"] == 64

def test_anchor_aliases_preserve_english_fragment_targets():
    assert "english-heading" in checker.anchors('<a id="english-heading"></a>\n# 中文標題\n')
    assert "heading-1" in checker.anchors('# Heading\n\n# Heading\n')

def test_example_links_are_not_treated_as_live_file_dependencies(locale_tree):
    path=locale_tree/'locales/translation-manifest.json'
    manifest=json.loads(path.read_text(encoding='utf-8'))
    for entry in manifest['translations']:
        if entry['source'].endswith('/SKILL.md'):
            for key in ('source','target'):
                file=locale_tree/entry[key]
                if '[example](not-a-real-file.md)' not in file.read_text(encoding='utf-8'):
                    file.write_text(file.read_text(encoding='utf-8')+'\n```text\n[example](not-a-real-file.md)\n```\n',encoding='utf-8')
            entry['source_sha256']=sha(locale_tree/entry['source']);entry['target_sha256']=sha(locale_tree/entry['target'])
    path.write_text(json.dumps(manifest),encoding='utf-8')
    assert checker.check(locale_tree)['status']=='pass'

def test_nonobject_manifest_is_a_reported_failure(locale_tree):
    (locale_tree/'locales/translation-manifest.json').write_text('[]',encoding='utf-8')
    assert checker.check(locale_tree)['status']=='fail'

def test_inline_example_line_wraps_do_not_look_like_new_code():
    assert checker.codes('Use `existing text; no\nmanuscript change`.') == checker.codes('使用 `existing text; no manuscript change`。')
    assert checker.codes('Use `same  spaces`.') != checker.codes('使用 `same spaces`。')

def test_multiline_english_teaching_examples_stay_english():
    source='Repair: “Both groups\nreported a difference.”'
    assert not checker.missing_case_examples(source,'修正：“Both groups reported a difference.”')
    assert checker.missing_case_examples(source,'修正：「兩組回報差異。」') == ['Both groups reported a difference.']

def test_local_fragment_cannot_read_a_file_outside_the_root(locale_tree, monkeypatch):
    outside=locale_tree.parent/'outside-locale-reference.md'
    outside.write_text('# Outside\n',encoding='utf-8')
    manifest_path=locale_tree/'locales/translation-manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    for entry in manifest['translations']:
        if entry['source'].endswith('/SKILL.md'):
            for key in ('source','target'):
                path=locale_tree/entry[key]
                text=path.read_text(encoding='utf-8')
                path.write_text(text.replace('references/guide.md',outside.as_posix()+'#outside'),encoding='utf-8')
            entry['source_sha256']=sha(locale_tree/entry['source']);entry['target_sha256']=sha(locale_tree/entry['target'])
    manifest_path.write_text(json.dumps(manifest),encoding='utf-8')
    original=Path.read_text
    def guarded(path,*args,**kwargs):
        assert path.resolve()!=outside.resolve(),'outside content must not be read'
        return original(path,*args,**kwargs)
    monkeypatch.setattr(Path,'read_text',guarded)
    report=checker.check(locale_tree)
    assert any(item['check']=='unsafe-local-reference' for item in report['findings'])

def test_explicit_language_entries_have_platform_neutral_agent_prompts():
    names=[]
    for base in checker.BASES:
        for suffix in checker.LOCALES.values():
            folder=ROOT/'skills'/f'{base}-{suffix}'
            skill=(folder/'SKILL.md').read_text(encoding='utf-8')
            name=re.search(r'^name: (.+)$',skill,re.M).group(1)
            names.append(name)
            metadata=(folder/'agents/openai.yaml').read_text(encoding='utf-8')
            assert f'{name} skill' in metadata
            assert '$'+name not in metadata and '@'+name not in metadata
            assert 'allow_implicit_invocation: true' in metadata
    assert len(set(names))==4

def test_translated_guidance_preserves_heading_and_table_topology():
    manifest=json.loads((ROOT/'locales/translation-manifest.json').read_text(encoding='utf-8'))
    def topology(text):
        text=checker.prose(text)
        headings=Counter(re.findall(r'^(#{1,6})\s',text,re.M))
        tables=[]
        active=False
        for line in text.splitlines():
            if line.startswith('|'):
                if not active:
                    masked=re.sub(r'`[^`]+`','CODE',line)
                    tables.append(len(re.split(r'(?<!\\)\|',masked))-2)
                active=True
            else:active=False
        return headings,tables
    for entry in manifest['translations']:
        source=(ROOT/entry['source']).read_text(encoding='utf-8')
        target=(ROOT/entry['target']).read_text(encoding='utf-8')
        assert topology(source)==topology(target),entry['target']
