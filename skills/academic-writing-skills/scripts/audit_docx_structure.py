#!/usr/bin/env python3
"""Inspect DOCX OOXML with exact tags; never confuse field instructions with edits."""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
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


def inspect(path: Path) -> dict:
    counts = {key: 0 for key in TAGS}
    counts["comments"] = 0
    placeholders: list[str] = []
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
            if name == "word/comments.xml":
                counts["comments"] += sum(1 for _ in root.iter(f"{{{W}}}comment"))
            text = " ".join((node.text or "") for node in root.iter(f"{{{W}}}t"))
            placeholders.extend(match.group(0) for match in PLACEHOLDER.finditer(text))
    tracked = counts["insertions"] + counts["deletions"] + counts["moves_from"] + counts["moves_to"]
    return {"path": str(path), "tracked_changes": tracked, "counts": counts, "placeholders": sorted(set(placeholders))}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", nargs="+")
    parser.add_argument("--require-clean", action="store_true")
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
    blocked = bool(errors) or (args.require_clean and any(item["tracked_changes"] or item["counts"]["comments"] or item["placeholders"] for item in reports))
    result = {"status": "BLOCKED" if blocked else "PASS", "reports": reports, "errors": errors}
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        for item in reports:
            print(f"{item['path']}: {item['tracked_changes']} tracked change(s), {item['counts']['comments']} comment(s), {len(item['placeholders'])} placeholder(s), {item['counts']['field_instructions']} field instruction(s)")
        for item in errors:
            print(f"ERROR {item['path']}: {item['error']}")
    return 2 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
