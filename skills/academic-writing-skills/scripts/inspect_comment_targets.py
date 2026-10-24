#!/usr/bin/env python3
"""Read current DOCX comment selections and threads without editing the package.

Offsets refer to this snapshot's XML text projection, not Word Range positions.
Successful extraction does not authorize an edit or validate its prose or layout.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile
from xml.etree import ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14 = "http://schemas.microsoft.com/office/word/2010/wordml"
W15 = "http://schemas.microsoft.com/office/word/2012/wordml"
STORY = re.compile(r"word/(document|header\d+|footer\d+|footnotes|endnotes)\.xml\Z")
HIDDEN = {f"{{{W}}}del", f"{{{W}}}moveFrom"}
MARKERS = {f"{{{W}}}commentRangeStart": "starts",
           f"{{{W}}}commentRangeEnd": "ends", f"{{{W}}}commentReference": "references"}
PROTECTED = {"drawing", "pict", "oMath", "oMathPara", "altChunk", "AlternateContent",
             "fldSimple", "fldChar", "instrText", "sym", "softHyphen"}


def _story(root: ET.Element, part: str, events: dict) -> dict:
    visible, raw, paragraphs, protected = [], [], [], []
    offset = raw_offset = xml_order = field_depth = 0

    def add(text: str, hidden: bool) -> None:
        nonlocal offset, raw_offset
        raw.append(text)
        raw_offset += len(text)
        if not hidden:
            visible.append(text)
            offset += len(text)

    def walk(node: ET.Element, hidden: bool = False, para: dict | None = None,
             complex_context: bool = False) -> None:
        nonlocal xml_order, field_depth
        xml_order += 1
        hidden = hidden or node.tag in HIDDEN
        complex_context = complex_context or node.tag.rsplit("}", 1)[-1] in PROTECTED
        field_kind = node.get(f"{{{W}}}fldCharType") if node.tag == f"{{{W}}}fldChar" and not hidden else None
        if field_kind == "begin":
            field_depth += 1
        if node.tag == f"{{{W}}}p":
            if paragraphs:
                add("\n", hidden)
            if para is not None:
                protected.append(xml_order)
                complex_context = True
            para = {"index": len(paragraphs) + 1,
                    "para_id": node.get(f"{{{W14}}}paraId"), "start": offset}
            paragraphs.append(para)
            # Deleted/inserted paragraph marks require a richer accepted-view editor.
            paragraph_mark_revision = any(
                node.find(f"{{{W}}}pPr/{{{W}}}rPr/{{{W}}}{kind}") is not None
                for kind in ("del", "ins", "moveFrom", "moveTo"))
        if node.tag.rsplit("}", 1)[-1] in PROTECTED:
            protected.append(xml_order)
        marker = MARKERS.get(node.tag)
        if marker:
            comment_id = node.get(f"{{{W}}}id", "")
            events[comment_id][marker].append({
                "part": part, "offset": offset, "raw_offset": raw_offset,
                "paragraph": para["index"] if para else None,
                "para_id": para["para_id"] if para else None, "hidden": hidden,
                "complex_context": complex_context or field_depth > 0, "xml_order": xml_order,
            })
        if node.tag in (f"{{{W}}}t", f"{{{W}}}delText"):
            add(node.text or "", hidden or node.tag == f"{{{W}}}delText")
        elif node.tag in (f"{{{W}}}tab", f"{{{W}}}br", f"{{{W}}}cr"):
            add("\t" if node.tag == f"{{{W}}}tab" else "\n", hidden)
        elif node.tag == f"{{{W}}}noBreakHyphen":
            # Same lexical glyph as U+002D; line-breaking behavior is not projected.
            add("-", hidden)
        for child in node:
            walk(child, hidden, para, complex_context)
        if node.tag == f"{{{W}}}p":
            para["end"] = offset
            if paragraph_mark_revision:
                xml_order += 1
                protected.append(xml_order)
        if field_kind == "end":
            field_depth = max(0, field_depth - 1)

    walk(root)
    text = "".join(visible)
    for para in paragraphs:
        para["text"] = text[para["start"]:para["end"]]
    return {"text": text, "raw_text": "".join(raw), "paragraphs": paragraphs,
            "protected_orders": protected}


def inspect(path: Path, expected_sha256: str | None = None) -> dict:
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if expected_sha256 is not None:
        if not re.fullmatch(r"[0-9a-fA-F]{64}", expected_sha256):
            raise ValueError("expected SHA256 must contain exactly 64 hexadecimal characters")
        if expected_sha256.lower() != digest:
            raise ValueError(f"source snapshot changed; reread comments before using IDs (actual SHA256 {digest})")
    events = defaultdict(lambda: {"starts": [], "ends": [], "references": []})
    definitions, para_ids, parent_links, stories = {}, defaultdict(set), defaultdict(set), {}
    issues = []
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("duplicate ZIP member names; package identity is ambiguous")
        if "word/document.xml" not in names:
            raise ValueError("missing word/document.xml")
        for name in names:
            if STORY.fullmatch(name):
                stories[name] = _story(ET.fromstring(archive.read(name)), name, events)
        if "word/comments.xml" in names:
            root = ET.fromstring(archive.read("word/comments.xml"))
            for node in root.iter(f"{{{W}}}comment"):
                cid = node.get(f"{{{W}}}id", "")
                if not cid or cid in definitions:
                    issues.append({"code": "duplicate_or_missing_comment_id", "comment_id": cid})
                definitions.setdefault(cid, {
                    "id": cid, "author": node.get(f"{{{W}}}author"),
                    "resolved": None,
                    "text": "\n".join("".join(t.text or "" for t in p.iter(f"{{{W}}}t"))
                                        for p in node.findall(f"{{{W}}}p")),
                })
                for para in node.iter(f"{{{W}}}p"):
                    if pid := para.get(f"{{{W14}}}paraId"):
                        para_ids[pid].add(cid)
        if "word/commentsExtended.xml" in names:
            root = ET.fromstring(archive.read("word/commentsExtended.xml"))
            for node in root.iter(f"{{{W15}}}commentEx"):
                linked_ids = para_ids.get(node.get(f"{{{W15}}}paraId"), set())
                done = node.get(f"{{{W15}}}done")
                if done in ("0", "1", "true", "false") and len(linked_ids) == 1:
                    definitions[next(iter(linked_ids))]["resolved"] = done in ("1", "true")
                if parent := node.get(f"{{{W15}}}paraIdParent"):
                    replies = para_ids.get(node.get(f"{{{W15}}}paraId"), set())
                    parents = para_ids.get(parent, set())
                    if len(replies) != 1 or len(parents) != 1:
                        issues.append({"code": "unresolved_reply_link", "para_id": node.get(f"{{{W15}}}paraId"),
                                       "parent_para_id": parent})
                        for cid in replies:
                            parent_links[cid].add(None)
                    else:
                        parent_links[next(iter(replies))].add(next(iter(parents)))

    duplicate_ids = {i["comment_id"] for i in issues if i["code"] == "duplicate_or_missing_comment_id"}
    comments = []
    for cid in sorted(set(definitions) | set(events)):
        item = {**definitions.get(cid, {"id": cid, "author": None, "text": None, "resolved": None}),
                "parent_id": None, "target_comment_id": cid, "anchor_status": "missing_anchor",
                "selected_text": None, "raw_selected_text": None, "start": None, "end": None,
                "overlaps": []}
        if cid in parent_links:
            seen, current = set(), cid
            while current in parent_links and current not in seen:
                seen.add(current)
                links = parent_links[current]
                current = next(iter(links)) if len(links) == 1 else None
            links = parent_links[cid]
            item["parent_id"] = next(iter(links)) if len(links) == 1 else None
            item["target_comment_id"] = current if current in definitions and current not in seen else None
            item["anchor_status"] = "reply" if item["target_comment_id"] else "unresolved_thread"
            if any(events[cid].values()):
                issues.append({"code": "reply_has_body_anchor", "comment_id": cid})
                item["anchor_status"] = "unresolved_thread"
                item["target_comment_id"] = None
            comments.append(item)
            continue
        markers = events[cid]
        if cid not in definitions or cid in duplicate_ids:
            item["anchor_status"] = "ambiguous_definition"
        elif any(len(markers[key]) > 1 for key in markers):
            item["anchor_status"] = "multiple_anchors"
        elif not markers["starts"] and not markers["ends"] and len(markers["references"]) == 1:
            item["start"] = markers["references"][0]
            item["anchor_status"] = ("deleted_anchor" if item["start"]["hidden"] else
                                     "complex_content" if item["start"]["complex_context"] else "point")
        elif all(len(markers[key]) == 1 for key in markers):
            start, end = markers["starts"][0], markers["ends"][0]
            item.update(start=start, end=end)
            reference = markers["references"][0]
            if (start["part"] != end["part"] or start["part"] != reference["part"]
                    or start["raw_offset"] > end["raw_offset"]
                    or reference["raw_offset"] < end["raw_offset"]):
                item["anchor_status"] = "invalid_range"
            else:
                story = stories[start["part"]]
                item["selected_text"] = story["text"][start["offset"]:end["offset"]]
                item["raw_selected_text"] = story["raw_text"][start["raw_offset"]:end["raw_offset"]]
                if start["hidden"] or end["hidden"] or markers["references"][0]["hidden"]:
                    item["anchor_status"] = "deleted_anchor"
                elif (start["complex_context"] or end["complex_context"]
                      or any(start["xml_order"] < pos < end["xml_order"] for pos in story["protected_orders"])):
                    item["anchor_status"] = "complex_content"
                elif not item["selected_text"].strip():
                    item["anchor_status"] = "deleted_only" if item["raw_selected_text"].strip() else "point"
                else:
                    item["anchor_status"] = "range"
        if item["start"] is not None:
            story = stories[item["start"]["part"]]
            first = item["start"]["paragraph"]
            last = item["end"]["paragraph"] if item["end"] else first
            item["paragraph_context"] = [p for p in story["paragraphs"]
                                         if first is not None and last is not None and first <= p["index"] <= last]
        comments.append(item)
    for a in comments:
        if a["anchor_status"] != "range":
            continue
        for b in comments:
            if a is b or b["anchor_status"] != "range" or a["start"]["part"] != b["start"]["part"]:
                continue
            if max(a["start"]["offset"], b["start"]["offset"]) < min(a["end"]["offset"], b["end"]["offset"]):
                a["overlaps"].append(b["id"])
    return {"status": "INSPECTED", "path": str(path), "source_sha256": digest,
            "text_basis": "XML text projection retaining insertions/moveTo and excluding deletions/moveFrom; not Word Range offsets or rendered layout",
            "editing_authorization_assessed": False, "selection_scope_inferred": False,
            "comments": comments, "issues": issues,
            "limits": "Read full threads and current context; ranges alone do not determine requested scope. OPC relationships/content types and rendered layout are not validated here. Unsupported or uncertain anchors require confirmation, not guessed edits."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx")
    parser.add_argument("--expected-sha256")
    args = parser.parse_args()
    try:
        report = inspect(Path(args.docx).expanduser().resolve(), args.expected_sha256)
    except (OSError, ValueError, RuntimeError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, ensure_ascii=True))
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
