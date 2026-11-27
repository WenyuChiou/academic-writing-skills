#!/usr/bin/env python3
"""Deterministic checks for submission companion limits, caption sync, and numeric hygiene."""

from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W_PREFIX = f"{{{W_NS}}}"
CAPTION_RE = re.compile(r"((?:Figure|Table)\s+S?\d+)\s*[.:]\s*([^\n]+)", re.IGNORECASE)
MISPLACED_CURRENCY_MINUS_RE = re.compile(r"\$-(?=[0-9])")
MISSING_BRACKET_SPACE_RE = re.compile(r"\d\[(?:\d|[-+])")


def _extract_docx_paragraphs(path: Path) -> list[str]:
    """Read accepted visible paragraphs from a Word .docx package."""
    with zipfile.ZipFile(path, "r") as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    paragraphs: list[str] = []
    for para in root.iter(f"{W_PREFIX}p"):
        parts: list[str] = []
        for node in para.iter():
            tag = node.tag
            if tag in {f"{W_PREFIX}delText", f"{W_PREFIX}instrText"}:
                continue
            if tag == f"{W_PREFIX}t" and node.text:
                parts.append(node.text)
        line = "".join(parts).strip()
        if line:
            paragraphs.append(line)
    return paragraphs


def read_lines(path: Path) -> list[str]:
    """Load non-empty lines from .txt, .md, or .docx."""
    if path.suffix.lower() == ".docx":
        return _extract_docx_paragraphs(path)
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def check_highlights(path: Path, max_chars: int = 85) -> list[dict[str, Any]]:
    """Flag highlight bullets exceeding max_chars (including spaces)."""
    findings: list[dict[str, Any]] = []
    for index, raw in enumerate(read_lines(path), start=1):
        cleaned = re.sub(r"^(?:[-*•]|\d+[.)])\s*", "", raw).strip()
        if cleaned.lower() in {"highlights", "highlights:"}:
            continue
        if len(cleaned) > max_chars:
            findings.append({
                "code": "COMP001", "artifact": str(path), "line": index,
                "length": len(cleaned), "limit": max_chars, "match": cleaned,
                "message": f"highlight bullet is {len(cleaned)} chars (limit {max_chars} with spaces)",
            })
    return findings


def check_abstract(path: Path, max_words: int = 250) -> list[dict[str, Any]]:
    """Flag abstract body exceeding max_words."""
    text = "\n".join(read_lines(path))
    words = re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", text)
    if len(words) > max_words:
        return [{
            "code": "COMP002", "artifact": str(path),
            "word_count": len(words), "limit": max_words,
            "message": f"abstract is {len(words)} words (limit {max_words})",
        }]
    return []


def check_caption_sync(manuscript: Path, captions: Path) -> list[dict[str, Any]]:
    """Compare standalone Figure/Table captions against manuscript captions."""
    norm = lambda value: re.sub(r"\s+", " ", value).strip()
    extract = lambda path: {
        m.group(1).title(): norm(m.group(2))
        for line in read_lines(path)
        for m in [CAPTION_RE.match(line)]
        if m
    }
    ms_caps, stand_caps = extract(manuscript), extract(captions)
    findings: list[dict[str, Any]] = []
    for label in sorted(set(ms_caps) | set(stand_caps)):
        if label not in ms_caps:
            findings.append({
                "code": "COMP003", "artifact": str(captions), "label": label,
                "message": f"{label} exists in standalone captions but not in manuscript",
            })
        elif label not in stand_caps:
            findings.append({
                "code": "COMP003", "artifact": str(captions), "label": label,
                "message": f"{label} exists in manuscript but not in standalone captions",
            })
        elif ms_caps[label] != stand_caps[label]:
            findings.append({
                "code": "COMP003", "artifact": str(captions), "label": label,
                "message": f"{label} differs between manuscript and standalone caption file",
            })
    return findings


def check_text_formatting(path: Path) -> list[dict[str, Any]]:
    """Check misplaced negative currency signs ($-40K) and missing space before [CI]."""
    text = "\n".join(read_lines(path))
    findings: list[dict[str, Any]] = []
    for match in MISPLACED_CURRENCY_MINUS_RE.finditer(text):
        findings.append({
            "code": "COMP004", "artifact": str(path), "match": match.group(0),
            "message": "misplaced minus after dollar sign ($-N); use -$N",
        })
    for match in MISSING_BRACKET_SPACE_RE.finditer(text):
        findings.append({
            "code": "COMP004", "artifact": str(path), "match": match.group(0),
            "message": "missing space between estimate and bracketed interval (e.g., 0.208[...])",
        })
    return findings


def check_csv_table(path: Path) -> list[dict[str, Any]]:
    """Check CSV tables for available-status rows containing NA cells or $-N typos."""
    findings: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row_index, row in enumerate(rows, start=2):
        lowered = {str(k).strip().lower(): ("" if v is None else str(v).strip()) for k, v in row.items()}
        status_val = lowered.get("status", "").lower()
        for col, val in row.items():
            text = "" if val is None else str(val).strip()
            if MISPLACED_CURRENCY_MINUS_RE.search(text) or MISSING_BRACKET_SPACE_RE.search(text):
                findings.append({
                    "code": "COMP004", "artifact": str(path), "row": row_index, "column": col,
                    "match": text, "message": "numeric/currency formatting error in table cell",
                })
            if status_val == "available" and text.upper() in {"NA", "N/A", ""}:
                findings.append({
                    "code": "COMP005", "artifact": str(path), "row": row_index, "column": col,
                    "message": "row marked status=available contains missing/NA cell",
                })
    return findings


def check_discrete_band(scale_items: int, band: float) -> list[dict[str, Any]]:
    """Warn when a stability band is narrower than one discrete step on a mean scale."""
    if scale_items <= 0:
        raise ValueError("scale_items must be positive")
    step = 1.0 / scale_items
    if band < step:
        return [{
            "code": "COMP006", "scale_items": scale_items, "step": round(step, 4), "band": band,
            "message": f"stability band (+-{band}) is smaller than minimum discrete item step (1/{scale_items}={step:.4f})",
        }]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--highlights", type=Path)
    parser.add_argument("--abstract", type=Path)
    parser.add_argument("--manuscript", type=Path)
    parser.add_argument("--captions", type=Path)
    parser.add_argument("--csv", type=Path, action="append", default=[])
    parser.add_argument("--text", type=Path, action="append", default=[])
    parser.add_argument("--max-highlight-chars", type=int, default=85)
    parser.add_argument("--max-abstract-words", type=int, default=250)
    parser.add_argument("--scale-items", type=int)
    parser.add_argument("--band", type=float)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    findings: list[dict[str, Any]] = []
    if args.highlights:
        findings.extend(check_highlights(args.highlights, args.max_highlight_chars))
    if args.abstract:
        findings.extend(check_abstract(args.abstract, args.max_abstract_words))
    if args.manuscript and args.captions:
        findings.extend(check_caption_sync(args.manuscript, args.captions))
    if args.manuscript:
        findings.extend(check_text_formatting(args.manuscript))
    for text_path in args.text:
        findings.extend(check_text_formatting(text_path))
    for csv_path in args.csv:
        findings.extend(check_csv_table(csv_path))
    if args.scale_items and args.band is not None:
        findings.extend(check_discrete_band(args.scale_items, args.band))

    result = {"status": "FINDINGS" if findings else "PASS", "findings": findings}
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"{result['status']}: {len(findings)} finding(s)")
        for item in findings:
            print(f"{item['code']}: {item['message']}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
