"""Synthetic OOXML/CLI boundaries, not a Word editor or readability certification."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile
from xml.sax.saxutils import escape

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/academic-writing-skills/scripts/inspect_comment_targets.py"
SPEC = importlib.util.spec_from_file_location("comment_targets", SCRIPT)
reader = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reader)
W, W14, W15 = reader.W, reader.W14, reader.W15


def run(text):
    return f'<w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def start(cid="0"):
    return f'<w:commentRangeStart w:id="{cid}"/>'


def end(cid="0"):
    return f'<w:commentRangeEnd w:id="{cid}"/><w:r><w:commentReference w:id="{cid}"/></w:r>'


def comment(cid="0", pid="AAA00001", text="Connect these results to their meaning."):
    return f'<w:comment w:id="{cid}" w:author="Advisor"><w:p w14:paraId="{pid}">{run(text)}</w:p></w:comment>'


def package(tmp_path, body, comments=None, extension="", extras=None, name="source.docx"):
    path = tmp_path / name
    parts = {
        "word/document.xml": f'<w:document xmlns:w="{W}" xmlns:w14="{W14}"><w:body>{body}</w:body></w:document>',
        "word/comments.xml": f'<w:comments xmlns:w="{W}" xmlns:w14="{W14}">{comment() if comments is None else comments}</w:comments>',
        "word/commentsExtended.xml": f'<w15:commentsEx xmlns:w15="{W15}">{extension}</w15:commentsEx>',
        "word/_rels/document.xml.rels": '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="c" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments" Target="comments.xml"/></Relationships>',
        "[Content_Types].xml": '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Override PartName="/word/comments.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/></Types>',
    }
    parts.update(extras or {})
    with zipfile.ZipFile(path, "w") as archive:
        for part, text in parts.items():
            archive.writestr(part, text)
    return path


def target(path, cid="0"):
    return next(c for c in reader.inspect(path)["comments"] if c["id"] == cid)


def test_split_runs_use_effective_text_without_modifying_any_package_bytes(tmp_path):
    body = ('<w:p w14:paraId="BBB00001">' + run("Read Figure 4. ") +
            '<w:ins w:author="Advisor" w:id="1">' + run("Scale 0–100. ") + '</w:ins>' + start() +
            '<w:del w:author="Advisor" w:id="2"><w:r><w:delText>Old 75.0.</w:delText></w:r></w:del>' +
            run("Group A 84.6; ") + '<w:ins w:author="Advisor" w:id="3">' +
            run("group B 78.2.") + '</w:ins>' + end() + run(" See Text S3.") + '</w:p>')
    path = package(tmp_path, body)
    before = path.read_bytes()
    report = reader.inspect(path)
    item = report["comments"][0]
    assert item["anchor_status"] == "range"
    assert item["selected_text"] == "Group A 84.6; group B 78.2."
    assert item["raw_selected_text"].startswith("Old 75.0.")
    assert item["paragraph_context"][0]["text"] == "Read Figure 4. Scale 0–100. Group A 84.6; group B 78.2. See Text S3."
    assert report["source_sha256"] == hashlib.sha256(before).hexdigest()
    assert path.read_bytes() == before
    assert report["editing_authorization_assessed"] is False


def test_synthetic_tracked_candidate_preserves_unselected_xml_authors_and_threads(tmp_path):
    prefix = '<w:p>' + '<w:ins w:author="Advisor" w:id="9">' + run("Figure 4 compares groups. ") + '</w:ins>' + run("Scale 0–100. ") + start()
    selected = "A scored 84.6 and B 78.2. This indicates higher willingness in A."
    suffix = end() + run(" Instrument details are in Text S3.") + '</w:p>'
    comments = comment() + comment("1", "AAA00002", "Keep the surrounding orientation.")
    extended = '<w15:commentEx w15:paraId="AAA00002" w15:paraIdParent="AAA00001"/>'
    source = package(tmp_path, prefix + run(selected) + suffix, comments, extended)
    replacement = "A reported greater willingness, with scores of 84.6 versus 78.2 for B."
    edits = '<w:del w:author="Editor" w:id="10"><w:r><w:delText>' + escape(selected) + '</w:delText></w:r></w:del>'
    edits += '<w:ins w:author="Editor" w:id="11">' + run(replacement) + '</w:ins>'
    candidate = package(tmp_path, prefix + edits + suffix, comments, extended, name="candidate.docx")
    with zipfile.ZipFile(source) as old, zipfile.ZipFile(candidate) as new:
        for part in old.namelist():
            if part != "word/document.xml":
                assert old.read(part) == new.read(part)
        for text in (prefix, suffix):
            assert text.encode() in old.read("word/document.xml")
            assert text.encode() in new.read("word/document.xml")
    assert target(candidate)["selected_text"] == replacement
    assert target(candidate, "1")["target_comment_id"] == "0"
    with zipfile.ZipFile(candidate) as archive:
        assert b'w:author="Advisor" w:id="9"' in archive.read("word/document.xml")
    # This tests the constructed fixture, not a production edit implementation.


@pytest.mark.parametrize("inner, expected", [
    ('<w:del w:author="Advisor"><w:r><w:delText>old value</w:delText></w:r></w:del>', "deleted_only"),
    ('<w:moveFrom>' + run("old value") + '</w:moveFrom>', "deleted_only"),
    ('<w:moveTo>' + run("current value") + '</w:moveTo>', "range"),
    ("", "point"),
])
def test_deleted_and_moved_text_are_distinguished(tmp_path, inner, expected):
    assert target(package(tmp_path, '<w:p>' + start() + inner + end() + '</w:p>'))["anchor_status"] == expected


def test_anchors_inside_deleted_content_are_not_current_targets(tmp_path):
    path = package(tmp_path, '<w:p><w:del>' + start() + run("old") + end() + '</w:del>' + run("new") + '</w:p>')
    assert target(path)["anchor_status"] == "deleted_anchor"


@pytest.mark.parametrize("body,status", [
    ('<w:p>' + run("unselected") + '</w:p>', "missing_anchor"),
    ('<w:p>' + start() + run("one") + '</w:p>', "missing_anchor"),
    ('<w:p><w:r><w:commentReference w:id="0"/></w:r></w:p>', "point"),
    ('<w:p>' + start() + run("one") + end() + start() + run("two") + end() + '</w:p>', "multiple_anchors"),
    ('<w:p><w:commentRangeEnd w:id="0"/>' + run("reversed") + start() + '<w:r><w:commentReference w:id="0"/></w:r></w:p>', "invalid_range"),
])
def test_missing_point_multiple_and_reversed_ranges(tmp_path, body, status):
    assert target(package(tmp_path, body))["anchor_status"] == status


def test_cross_paragraph_range_retains_both_partial_boundaries(tmp_path):
    body = '<w:p>' + run("Keep opening. ") + start() + run("First selected.") + '</w:p><w:p>' + run("Second selected.") + end() + run(" Keep closing.") + '</w:p>'
    item = target(package(tmp_path, body))
    assert item["selected_text"] == "First selected.\nSecond selected."
    assert (item["start"]["paragraph"], item["end"]["paragraph"]) == (1, 2)


def test_overlapping_comments_are_reported_not_flattened(tmp_path):
    body = '<w:p>' + start() + run("A ") + start("1") + run("B ") + end() + run("C") + end("1") + '</w:p>'
    path = package(tmp_path, body, comment() + comment("1", "AAA00002"))
    a, b = reader.inspect(path)["comments"]
    assert a["selected_text"] == "A B " and b["selected_text"] == "B C"
    assert a["overlaps"] == ["1"] and b["overlaps"] == ["0"]


def test_reply_links_use_all_comment_paragraphs_and_keep_parent_target(tmp_path):
    comments = '<w:comment w:id="0" w:author="Advisor"><w:p w14:paraId="AAA00001">' + run("First.") + '</w:p><w:p w14:paraId="AAA00003">' + run("Second.") + '</w:p></w:comment>'
    comments += comment("1", "AAA00002", "Acknowledged.")
    ext = '<w15:commentEx w15:paraId="AAA00002" w15:paraIdParent="AAA00003"/>'
    path = package(tmp_path, '<w:p>' + start() + run("Selected.") + end() + '</w:p>', comments, ext)
    reply = target(path, "1")
    assert reply["anchor_status"] == "reply" and reply["parent_id"] == "0"
    assert reply["target_comment_id"] == "0" and reply["selected_text"] is None
    assert target(path)["text"] == "First.\nSecond."


@pytest.mark.parametrize("parent", ["MISSING", "AAA00002"])
def test_missing_and_self_linked_reply_stay_unresolved(tmp_path, parent):
    ext = f'<w15:commentEx w15:paraId="AAA00002" w15:paraIdParent="{parent}"/>'
    path = package(tmp_path, '<w:p>' + run("Body.") + '</w:p>', comment() + comment("1", "AAA00002"), ext)
    assert target(path, "1")["anchor_status"] == "unresolved_thread"


def test_reply_with_its_own_body_anchor_is_not_silently_retargeted(tmp_path):
    ext = '<w15:commentEx w15:paraId="AAA00002" w15:paraIdParent="AAA00001"/>'
    body = '<w:p>' + start() + run("Parent.") + end() + start("1") + run("Separate.") + end("1") + '</w:p>'
    path = package(tmp_path, body, comment() + comment("1", "AAA00002"), ext)
    assert target(path, "1")["anchor_status"] == "unresolved_thread"
    assert {i["code"] for i in reader.inspect(path)["issues"]} == {"reply_has_body_anchor"}


def test_snapshot_change_rejects_old_id_even_if_it_still_exists(tmp_path):
    path = package(tmp_path, '<w:p>' + start() + run("Old target.") + end() + '</w:p>')
    original = hashlib.sha256(path.read_bytes()).hexdigest()
    package(tmp_path, '<w:p>' + run("New context.") + start() + run("Different target.") + end() + '</w:p>')
    with pytest.raises(ValueError, match="source snapshot changed"):
        reader.inspect(path, original)
    assert target(path)["selected_text"] == "Different target."


@pytest.mark.parametrize("kind", ["fldSimple", "drawing"])
def test_protected_content_inside_selection_is_not_plain_text_authority(tmp_path, kind):
    path = package(tmp_path, f'<w:p><w:{kind}>' + start() + run("Text.") + end() + f'</w:{kind}></w:p>')
    assert target(path)["anchor_status"] == "complex_content"


def test_unrelated_drawing_does_not_invalidate_a_clear_selection(tmp_path):
    path = package(tmp_path, '<w:p>' + start() + run("Text.") + end() + '<w:drawing/></w:p>')
    assert target(path)["anchor_status"] == "range"


def test_reference_in_other_story_is_not_a_valid_body_range(tmp_path):
    body = '<w:p>' + start() + run("Text.") + '<w:commentRangeEnd w:id="0"/></w:p>'
    header = f'<w:hdr xmlns:w="{W}"><w:p><w:r><w:commentReference w:id="0"/></w:r></w:p></w:hdr>'
    assert target(package(tmp_path, body, extras={"word/header1.xml": header}))["anchor_status"] == "invalid_range"


def test_missing_comment_definition_is_not_an_inferred_instruction(tmp_path):
    path = package(tmp_path, '<w:p>' + start() + run("Text.") + end() + '</w:p>', comments="")
    assert target(path)["anchor_status"] == "ambiguous_definition"


def test_duplicate_comment_id_is_explicit(tmp_path):
    path = package(tmp_path, '<w:p>' + start() + run("Text.") + end() + '</w:p>', comment() + comment())
    assert target(path)["anchor_status"] == "ambiguous_definition"


def test_resolved_metadata_is_read_not_changed(tmp_path):
    ext = '<w15:commentEx w15:paraId="AAA00001" w15:done="1"/>'
    path = package(tmp_path, '<w:p>' + start() + run("Text.") + end() + '</w:p>', extension=ext)
    before = path.read_bytes()
    assert target(path)["resolved"] is True
    assert path.read_bytes() == before


def test_unicode_and_tab_positions_are_snapshot_python_characters(tmp_path):
    body = '<w:p>' + run("α🙂 ") + start() + run("中文") + '<w:r><w:tab/></w:r>' + run("text") + end() + '</w:p>'
    item = target(package(tmp_path, body))
    assert item["selected_text"] == "中文\ttext" and item["start"]["offset"] == 3


def test_field_instruction_is_not_selected_visible_text(tmp_path):
    body = '<w:p>' + start() + '<w:r><w:instrText>REF old_bookmark</w:instrText></w:r>' + run("Figure 5") + end() + '</w:p>'
    assert target(package(tmp_path, body))["selected_text"] == "Figure 5"


def test_nonbreaking_hyphen_preserves_lexical_text_and_source_bytes(tmp_path):
    body = '<w:p>' + start() + run("high") + '<w:r><w:noBreakHyphen/></w:r>' + run("risk") + end() + '</w:p>'
    path = package(tmp_path, body)
    before = path.read_bytes()
    item = target(path)
    assert item["selected_text"] == "high-risk"
    assert item["anchor_status"] == "range"
    assert path.read_bytes() == before


@pytest.mark.parametrize("token", [
    '<w:sym w:font="Wingdings" w:char="F04A"/>', '<w:softHyphen/>',
])
def test_font_symbols_and_conditional_hyphens_are_not_plain_ranges(tmp_path, token):
    path = package(tmp_path, '<w:p>' + start() + run("Use ") + '<w:r>' + token + '</w:r>' + run(" here.") + end() + '</w:p>')
    before = path.read_bytes()
    assert target(path)["anchor_status"] == "complex_content"
    assert path.read_bytes() == before


def field(kind):
    return f'<w:r><w:fldChar w:fldCharType="{kind}"/></w:r>'


@pytest.mark.parametrize("inner", [
    field("begin") + '<w:r><w:instrText>REF label</w:instrText></w:r>' + field("separate") + run("Figure 5") + field("end"),
    '<w:r><w:instrText>REF label</w:instrText></w:r>' + run("Figure 5"),
])
def test_selected_field_controls_or_instructions_are_uncertain(tmp_path, inner):
    item = target(package(tmp_path, '<w:p>' + start() + inner + end() + '</w:p>'))
    assert item["selected_text"] == "Figure 5"
    assert item["anchor_status"] == "complex_content"


@pytest.mark.parametrize("prefix,suffix", [
    (field("begin") + field("separate"), field("end")),
    (field("begin") + field("separate") + field("begin") + field("end"), field("end")),
    (field("begin"), ""),
])
def test_selection_inside_external_or_nested_field_delimiters_is_uncertain(tmp_path, prefix, suffix):
    item = target(package(tmp_path, '<w:p>' + prefix + start() + run("Result") + end() + suffix + '</w:p>'))
    assert item["selected_text"] == "Result"
    assert item["anchor_status"] == "complex_content"


@pytest.mark.parametrize("outside", [
    '<w:drawing/>', '<w:r><w:sym w:font="Wingdings" w:char="F04A"/></w:r>',
    field("begin") + field("separate") + field("end"),
])
@pytest.mark.parametrize("side", ["before", "after"])
def test_protected_nodes_outside_selection_at_same_text_offset_do_not_invalidate_it(tmp_path, outside, side):
    selected = start() + run("Text.") + end()
    body = '<w:p>' + (outside + selected if side == "before" else selected + outside) + '</w:p>'
    assert target(package(tmp_path, body))["anchor_status"] == "range"


@pytest.mark.parametrize("encoding", ["ascii", "cp950"])
def test_cli_returns_unicode_json_under_non_utf8_output_encoding(tmp_path, encoding):
    path = package(tmp_path, '<w:p>' + start() + run("中文🙂") + end() + '</w:p>',
                   comments=comment(text="Keep 🙂."), name="來源🙂.docx")
    before = path.read_bytes()
    env = {**os.environ, "PYTHONIOENCODING": encoding}
    result = subprocess.run([sys.executable, str(SCRIPT), str(path)], env=env, capture_output=True)
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout.decode("ascii"))
    assert report["comments"][0]["selected_text"] == "中文🙂"
    assert report["comments"][0]["text"] == "Keep 🙂."
    assert path.read_bytes() == before
    missing = path.with_name("missing🙂.docx")
    error = subprocess.run([sys.executable, str(SCRIPT), str(missing)], env=env, capture_output=True)
    assert error.returncode == 2, error.stderr
    assert json.loads(error.stdout.decode("ascii"))["status"] == "ERROR"


@pytest.mark.parametrize("expected", ["invalid", "a" * 63, "a" * 65])
def test_malformed_expected_hash_is_not_accepted(tmp_path, expected):
    path = package(tmp_path, '<w:p>' + run("Body.") + '</w:p>')
    with pytest.raises(ValueError, match="exactly 64"):
        reader.inspect(path, expected)


def test_duplicate_zip_members_fail_closed(tmp_path):
    path = package(tmp_path, '<w:p>' + run("Body.") + '</w:p>')
    with zipfile.ZipFile(path, "a") as archive, pytest.warns(UserWarning):
        archive.writestr("word/document.xml", '<not-a-document/>')
    with pytest.raises(ValueError, match="duplicate ZIP"):
        reader.inspect(path)


def test_cli_is_read_only_and_stale_or_corrupt_input_fails_explicitly(tmp_path):
    path = package(tmp_path, '<w:p>' + start() + run("Current.") + end() + '</w:p>')
    before = path.read_bytes()
    good = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True, encoding="utf-8")
    assert good.returncode == 0 and json.loads(good.stdout)["status"] == "INSPECTED"
    stale = subprocess.run([sys.executable, str(SCRIPT), str(path), "--expected-sha256", "0" * 64], capture_output=True, text=True, encoding="utf-8")
    assert stale.returncode == 2 and json.loads(stale.stdout)["status"] == "ERROR"
    assert path.read_bytes() == before
    malformed = package(tmp_path, '<w:p>broken', name="broken.docx")
    bad = subprocess.run([sys.executable, str(SCRIPT), str(malformed)], capture_output=True, text=True, encoding="utf-8")
    assert bad.returncode == 2 and json.loads(bad.stdout)["status"] == "ERROR"
