#!/usr/bin/env python3
"""Inspect DOCX OOXML with exact tags; never confuse field instructions with edits."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14 = "http://schemas.microsoft.com/office/word/2010/wordml"
W15 = "http://schemas.microsoft.com/office/word/2012/wordml"
TAGS = {
    "insertions": f"{{{W}}}ins",
    "deletions": f"{{{W}}}del",
    "moves_from": f"{{{W}}}moveFrom",
    "moves_to": f"{{{W}}}moveTo",
    "comment_ranges": f"{{{W}}}commentRangeStart",
    "comment_references": f"{{{W}}}commentReference",
    "field_instructions": f"{{{W}}}instrText",
    "simple_fields": f"{{{W}}}fldSimple",
}
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME)\b|\[(INSERT|ADD|CHECK|CITATION)[^\]]*\]", re.I)


def local_name(name: str) -> str:
    return name.rsplit("}", 1)[-1]


def inspect(path: Path) -> dict:
    counts = {key: 0 for key in TAGS}
    counts["comments"] = 0
    placeholders: list[str] = []
    revision_authors: Counter[str] = Counter()
    comment_authors: Counter[str] = Counter()
    comments_by_para: dict[str, dict[str, str]] = {}
    comment_extensions: list[dict[str, str]] = []
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if not name.startswith("word/") or not name.endswith(".xml"):
                continue
            try:
                root = ET.fromstring(archive.read(name))
            except ET.ParseError:
                continue
            for key, tag in TAGS.items():
                counts[key] += sum(1 for _ in root.iter(tag))
            for key in ("insertions", "deletions", "moves_from", "moves_to"):
                for node in root.iter(TAGS[key]):
                    author = node.attrib.get(f"{{{W}}}author", "[missing]")
                    revision_authors[author] += 1
            if name == "word/comments.xml":
                comments = list(root.iter(f"{{{W}}}comment"))
                counts["comments"] += len(comments)
                for comment in comments:
                    author = comment.attrib.get(f"{{{W}}}author", "[missing]")
                    comment_authors[author] += 1
                    paragraph = next(comment.iter(f"{{{W}}}p"), None)
                    para_id = paragraph.attrib.get(f"{{{W14}}}paraId") if paragraph is not None else None
                    if para_id:
                        comments_by_para[para_id] = {
                            "comment_id": comment.attrib.get(f"{{{W}}}id", ""),
                            "author": author,
                        }
            if name == "word/commentsExtended.xml":
                for node in root.iter(f"{{{W15}}}commentEx"):
                    comment_extensions.append({local_name(key): value for key, value in node.attrib.items()})
            text = " ".join((node.text or "") for node in root.iter(f"{{{W}}}t"))
            placeholders.extend(match.group(0) for match in PLACEHOLDER.finditer(text))
    reply_authors: Counter[str] = Counter()
    orphan_reply_para_ids: list[str] = []
    orphan_parent_para_ids: list[str] = []
    for extension in comment_extensions:
        parent_id = extension.get("paraIdParent")
        if not parent_id:
            continue
        reply_id = extension.get("paraId", "")
        reply = comments_by_para.get(reply_id)
        if reply is None:
            orphan_reply_para_ids.append(reply_id)
        else:
            reply_authors[reply["author"]] += 1
        if parent_id not in comments_by_para:
            orphan_parent_para_ids.append(parent_id)
    tracked = counts["insertions"] + counts["deletions"] + counts["moves_from"] + counts["moves_to"]
    return {
        "path": str(path),
        "tracked_changes": tracked,
        "counts": counts,
        "revision_authors": dict(sorted(revision_authors.items())),
        "comment_authors": dict(sorted(comment_authors.items())),
        "parent_linked_replies": sum(reply_authors.values()) + len(orphan_reply_para_ids),
        "reply_authors": dict(sorted(reply_authors.items())),
        "orphan_reply_para_ids": sorted(set(orphan_reply_para_ids)),
        "orphan_parent_para_ids": sorted(set(orphan_parent_para_ids)),
        "placeholders": sorted(set(placeholders)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", nargs="+")
    parser.add_argument("--require-clean", action="store_true")
    parser.add_argument("--require-valid-comments", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    reports = []
    errors = []
    for name in args.docx:
        path = Path(name).expanduser().resolve()
        try:
            reports.append(inspect(path))
        except (OSError, zipfile.BadZipFile) as exc:
            errors.append({"path": str(path), "error": str(exc)})
    invalid_comments = any(item["orphan_reply_para_ids"] or item["orphan_parent_para_ids"] for item in reports)
    blocked = (
        bool(errors)
        or (args.require_clean and any(item["tracked_changes"] or item["counts"]["comments"] or item["placeholders"] for item in reports))
        or (args.require_valid_comments and invalid_comments)
    )
    result = {"status": "BLOCKED" if blocked else "PASS", "reports": reports, "errors": errors}
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        for item in reports:
            print(f"{item['path']}: {item['tracked_changes']} tracked change(s), {item['counts']['comments']} comment(s), {item['parent_linked_replies']} parent-linked reply/replies, {len(item['placeholders'])} placeholder(s), {item['counts']['field_instructions']} field instruction(s)")
            print(f"  revision authors: {item['revision_authors']}")
            print(f"  comment authors: {item['comment_authors']}")
            print(f"  reply authors: {item['reply_authors']}")
            if item["orphan_reply_para_ids"] or item["orphan_parent_para_ids"]:
                print(f"  orphan reply paraIds: {item['orphan_reply_para_ids']}")
                print(f"  orphan parent paraIds: {item['orphan_parent_para_ids']}")
        for item in errors:
            print(f"ERROR {item['path']}: {item['error']}")
    return 2 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
