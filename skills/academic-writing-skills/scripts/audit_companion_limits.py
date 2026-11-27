#!/usr/bin/env python3
"""Deterministic checks for submission companion limits, caption sync, LaTeX/Word tables, and BibTeX keys."""

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
HIDDEN_TAGS = {f"{W_PREFIX}del", f"{W_PREFIX}moveFrom", f"{W_PREFIX}instrText"}
SEP_TAGS = {f"{W_PREFIX}br", f"{W_PREFIX}cr", f"{W_PREFIX}tab"}
CAPTION_RE = re.compile(r"((?:Figure|Table)\s+S?\d+)\s*[.:]\s*(.*)", re.IGNORECASE)
BLOCK_BREAK_RE = re.compile(r"^(?:#{1,6}\s|```|---+$|\*\*\*+$)")
MISPLACED_CURRENCY_MINUS_RE = re.compile(r"\$-(?=[0-9])")
TEX_MISPLACED_CURRENCY_MINUS_RE = re.compile(r"\\\$-(?=(?:\\text\{)?[0-9])")
MISSING_BRACKET_SPACE_RE = re.compile(r"\d\[(?:\d|[-+])")
LATEX_FLOAT_ENV_RE = re.compile(
    r"\\begin\{(figure\*?|table\*?|longtable)\}(.*?)\\end\{\1\}", re.DOTALL | re.IGNORECASE
)
LATEX_TABULAR_BEGIN_RE = re.compile(r"\\begin\{(tabular\*?|tabularx|longtable)\}")
LATEX_CITE_CMD_RE = re.compile(
    r"\\(?:cite(?:t(?:itle)?|p|alt|alp|author|yearpar|year|num|url|field|list|name|date|s)?|"
    r"(?:paren|text|auto|footfull|foot|full|super|smart|no|multi|vol|fvol|pvol|tvol|ftvol|svol|avol)cites?)\*?(?![A-Za-z])",
    re.IGNORECASE,
)


def _strip_latex_comments(text: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines())


def _unwrap_latex_inline(text: str) -> str:
    cleaned = re.sub(r"\\label\{[^}]*\}", "", text)
    unwrap_re = re.compile(r"\\(?:textbf|textit|emph|textrm|text)\{([^{}]*)\}")
    for _ in range(4):
        updated = unwrap_re.sub(r"\1", cleaned)
        if updated == cleaned:
            break
        cleaned = updated
    cleaned = re.sub(r"(?<!\\)\$((?:\\.|[^$\\])+?)(?<!\\)\$", r"\1", cleaned)
    return re.sub(r"\s+", " ", cleaned.replace(r"\%", "%").replace(r"\$", "$")).strip()


def _extract_balanced_braces(text: str, open_pos: int) -> tuple[str, int] | None:
    if open_pos >= len(text) or text[open_pos] != "{":
        return None
    depth = 0
    idx = open_pos
    while idx < len(text):
        ch = text[idx]
        if ch == "\\":
            idx += 2
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[open_pos + 1:idx], idx + 1
        idx += 1
    return None


def _iter_latex_tables(text: str) -> list[tuple[str, str]]:
    """Extract (col_spec, body) for LaTeX tabular/tabular*/tabularx/longtable environments with optional [pos]."""
    tables: list[tuple[str, str]] = []
    for match in LATEX_TABULAR_BEGIN_RE.finditer(text):
        env = match.group(1)
        pos = match.end()
        opt = re.match(r"\s*(?:\[[^\]]*\]\s*)?", text[pos:])
        pos += opt.end() if opt else 0
        if env in {"tabular*", "tabularx"}:
            width = _extract_balanced_braces(text, pos)
            if not width:
                continue
            pos = width[1]
            opt2 = re.match(r"\s*(?:\[[^\]]*\]\s*)?", text[pos:])
            pos += opt2.end() if opt2 else 0
        col_extract = _extract_balanced_braces(text, pos)
        if not col_extract:
            continue
        col_spec, body_start = col_extract
        end_match = re.search(rf"\\end\{{{re.escape(env)}\}}", text[body_start:])
        if not end_match:
            continue
        tables.append((col_spec, text[body_start:body_start + end_match.start()]))
    return tables


def _collect_visible_text(node: ET.Element, parts: list[str]) -> None:
    if node.tag in HIDDEN_TAGS:
        return
    if node.tag in SEP_TAGS:
        parts.append("\t" if node.tag == f"{W_PREFIX}tab" else " ")
        return
    if node.tag == f"{W_PREFIX}t" and node.text:
        parts.append(node.text)
    for child in node:
        _collect_visible_text(child, parts)


def _walk_visible_paragraphs(node: ET.Element, paragraphs: list[str]) -> None:
    """Traverse Word XML top-down, pruning hidden revision containers before inspecting paragraphs."""
    if node.tag in HIDDEN_TAGS:
        return
    if node.tag == f"{W_PREFIX}p":
        parts: list[str] = []
        _collect_visible_text(node, parts)
        line = re.sub(r"[ \t]+", " ", "".join(parts)).strip()
        if line:
            paragraphs.append(line)
        return
    for child in node:
        _walk_visible_paragraphs(child, paragraphs)


def _extract_docx_paragraphs(path: Path) -> list[str]:
    """Read accepted visible paragraphs from a Word .docx package, skipping w:del/w:moveFrom/w:instrText."""
    with zipfile.ZipFile(path, "r") as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    paragraphs: list[str] = []
    _walk_visible_paragraphs(root, paragraphs)
    return paragraphs


def read_raw_lines(path: Path) -> list[str]:
    """Load paragraph/file lines while preserving blank separators in text files."""
    if path.suffix.lower() == ".docx":
        out: list[str] = []
        for para in _extract_docx_paragraphs(path):
            out.append(para)
            out.append("")
        return out
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".tex":
        raw = _strip_latex_comments(raw)
    return [line.strip() for line in raw.splitlines()]


def read_lines(path: Path) -> list[str]:
    """Load non-empty lines from .txt, .md, .tex, or .docx."""
    return [line for line in read_raw_lines(path) if line]


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
    """Flag abstract body exceeding max_words (extracting \\begin{abstract}...\\end{abstract} for .tex when present)."""
    text = "\n".join(read_lines(path))
    if path.suffix.lower() == ".tex":
        abs_match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.DOTALL)
        text = _unwrap_latex_inline(abs_match.group(1) if abs_match else text)
    words = re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", text)
    if len(words) > max_words:
        return [{
            "code": "COMP002", "artifact": str(path),
            "word_count": len(words), "limit": max_words,
            "message": f"abstract is {len(words)} words (limit {max_words})",
        }]
    return []


def _extract_tex_captions(path: Path) -> dict[str, str]:
    text = _strip_latex_comments(path.read_text(encoding="utf-8"))
    counters = {"figure": 0, "table": 0}
    captions: dict[str, str] = {}
    for match in LATEX_FLOAT_ENV_RE.finditer(text):
        env = match.group(1).lower()
        kind = "figure" if env.startswith("figure") else "table"
        body = match.group(2)
        search_area = body.split(r"\endfirsthead", 1)[0] if env == "longtable" and r"\endfirsthead" in body else body
        cap_cmd = re.search(r"\\caption(?!\*)(?:\[[^\]]*\])?\s*\{", search_area)
        if not cap_cmd and search_area is not body:
            cap_cmd = re.search(r"\\caption(?!\*)(?:\[[^\]]*\])?\s*\{", body)
            search_area = body
        if not cap_cmd:
            continue
        extracted = _extract_balanced_braces(search_area, cap_cmd.end() - 1)
        if not extracted:
            continue
        raw_cap = _unwrap_latex_inline(extracted[0])
        counters[kind] += 1
        cap_match = CAPTION_RE.match(raw_cap)
        if cap_match:
            label = cap_match.group(1).title()
            cap_text = re.sub(r"\s+", " ", cap_match.group(2)).strip()
        else:
            label = f"{kind.title()} {counters[kind]}"
            cap_text = raw_cap
        captions[label] = cap_text
    return captions


def _normalize_md_caption_line(line: str) -> str:
    """Strip blockquote '>' prefixes and bold/italic emphasis wrappers around Figure/Table labels."""
    cleaned = re.sub(r"^(?:>\s*)+", "", line).strip()
    return re.sub(
        r"^(?:\*\*|__|[*_])*\s*((?:Figure|Table)\s+S?\d+)\s*(?:([.:])\s*(?:\*\*|__|[*_])*|(?:\*\*|__|[*_])+\s*([.:])\s*)",
        lambda m: f"{m.group(1)}{m.group(2) or m.group(3)} ",
        cleaned,
        flags=re.IGNORECASE,
    )


def _extract_captions(path: Path) -> dict[str, str]:
    """Collect complete multi-line Figure/Table captions until a blank line or block boundary (plus LaTeX \\caption{})."""
    if path.suffix.lower() == ".tex":
        return _extract_tex_captions(path)
    captions: dict[str, str] = {}
    current_label: str | None = None
    chunks: list[str] = []

    def flush() -> None:
        nonlocal current_label, chunks
        if current_label is not None:
            captions[current_label] = re.sub(r"\s+", " ", " ".join(chunks)).strip()
        current_label = None
        chunks = []

    for line in read_raw_lines(path):
        stripped = _normalize_md_caption_line(line)
        if not stripped or BLOCK_BREAK_RE.match(stripped):
            flush()
            continue
        match = CAPTION_RE.match(stripped)
        if match:
            flush()
            current_label = match.group(1).title()
            if match.group(2).strip():
                chunks.append(match.group(2).strip())
        elif current_label is not None:
            chunks.append(stripped)
    flush()
    return captions


def check_caption_sync(manuscript: Path, captions: Path) -> list[dict[str, Any]]:
    """Compare standalone Figure/Table captions against manuscript captions."""
    ms_caps, stand_caps = _extract_captions(manuscript), _extract_captions(captions)
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
    """Check misplaced negative currency signs (without flagging valid LaTeX $-0.25$ math) and missing space before [CI]."""
    text = "\n".join(read_lines(path))
    findings: list[dict[str, Any]] = []
    cur_pattern = TEX_MISPLACED_CURRENCY_MINUS_RE if path.suffix.lower() == ".tex" else MISPLACED_CURRENCY_MINUS_RE
    for match in cur_pattern.finditer(text):
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


def check_latex_tables(path: Path) -> list[dict[str, Any]]:
    """Flag LaTeX vertical table rules (| or \\vline) and double horizontal rules instead of booktabs."""
    text = _strip_latex_comments(path.read_text(encoding="utf-8"))
    findings: list[dict[str, Any]] = []
    for index, (col_spec, body) in enumerate(_iter_latex_tables(text), start=1):
        if "|" in col_spec or r"\vline" in body:
            findings.append({
                "code": "COMP007", "artifact": str(path), "table": index,
                "message": f"LaTeX table {index} uses vertical rules ({col_spec!r}); prefer booktabs three-line horizontal rules",
            })
        if re.search(r"\\hline\s*\\hline", body):
            findings.append({
                "code": "COMP007", "artifact": str(path), "table": index,
                "message": f"LaTeX table {index} uses double \\hline; use \\toprule/\\midrule/\\bottomrule from booktabs",
            })
    return findings


def _skip_optional_cite_args(text: str, pos: int) -> int:
    opt = re.match(r"(?:\s*(?:\([^)]*\)|\[[^\]]*\]))*\s*", text[pos:])
    return pos + (opt.end() if opt else 0)


def _extract_cite_keys_from_tex(text: str) -> tuple[set[str], bool]:
    cited: set[str] = set()
    nocite_all = False
    for match in LATEX_CITE_CMD_RE.finditer(text):
        cmd = match.group(0).lstrip("\\").rstrip("*").lower()
        pos = match.end()
        is_multicite = cmd.endswith("s") or "multicite" in cmd
        is_volcite = "volcite" in cmd
        while pos < len(text):
            pos = _skip_optional_cite_args(text, pos)
            if is_volcite:
                if pos >= len(text) or text[pos] != "{":
                    break
                vol_grp = _extract_balanced_braces(text, pos)
                if not vol_grp:
                    break
                _, pos = vol_grp
                pos = _skip_optional_cite_args(text, pos)
            if pos >= len(text) or text[pos] != "{":
                break
            grp = _extract_balanced_braces(text, pos)
            if not grp:
                break
            keys_str, pos = grp
            for part in keys_str.split(","):
                key = part.strip()
                if key == "*":
                    nocite_all = True
                elif key:
                    cited.add(key)
            if not is_multicite:
                break
    return cited, nocite_all


def _extract_bib_keys(bib_text: str) -> set[str]:
    """Extract active BibTeX entry keys while skipping comments and balanced @comment/@preamble/@string blocks."""
    keys: set[str] = set()
    header_re = re.compile(r"@([a-zA-Z]+)\s*([{(])")
    n = len(bib_text)
    pos = 0
    while pos < n:
        at_idx = bib_text.find("@", pos)
        pct_idx = bib_text.find("%", pos)
        if pct_idx != -1 and (at_idx == -1 or pct_idx < at_idx):
            nl_idx = bib_text.find("\n", pct_idx)
            pos = n if nl_idx == -1 else nl_idx + 1
            continue
        if at_idx == -1:
            break
        match = header_re.match(bib_text, at_idx)
        if not match:
            pos = at_idx + 1
            continue
        entry_type = match.group(1).lower()
        open_ch = match.group(2)
        close_ch = "}" if open_ch == "{" else ")"
        ignore_quotes = entry_type == "comment"
        body_start = match.end()
        idx = body_start
        brace_depth = 0
        paren_depth = 0
        in_quotes = False
        end_body = n
        while idx < n:
            ch = bib_text[idx]
            if ch == "\\":
                idx += 2
                continue
            if brace_depth > 0:
                if ch == "{":
                    brace_depth += 1
                elif ch == "}":
                    brace_depth -= 1
                idx += 1
                continue
            if in_quotes:
                if ch == "{":
                    brace_depth = 1
                elif ch == '"':
                    in_quotes = False
                idx += 1
                continue
            if ch == '"' and not ignore_quotes:
                in_quotes = True
            elif ch == "{":
                brace_depth = 1
            elif open_ch == "(" and ch == "(":
                paren_depth += 1
            elif ch == close_ch:
                if open_ch == "(" and paren_depth > 0:
                    paren_depth -= 1
                else:
                    end_body = idx
                    idx += 1
                    break
            idx += 1
        block_body = bib_text[body_start:end_body]
        if entry_type not in {"comment", "preamble", "string"}:
            key_match = re.match(r"\s*([^,\s{}()]+)\s*,", block_body)
            if key_match:
                keys.add(key_match.group(1).strip())
        pos = max(idx, match.end())
    return keys


def check_latex_citations(tex_paths: list[Path], bib_paths: list[Path]) -> list[dict[str, Any]]:
    """Reconcile LaTeX \\cite keys against .bib entries across line breaks and multicite groups in both directions."""
    cited: set[str] = set()
    nocite_all = False
    for tex in tex_paths:
        text = _strip_latex_comments(tex.read_text(encoding="utf-8"))
        tex_cited, tex_nocite_all = _extract_cite_keys_from_tex(text)
        cited.update(tex_cited)
        nocite_all = nocite_all or tex_nocite_all

    bib_keys: set[str] = set()
    for bib in bib_paths:
        bib_keys.update(_extract_bib_keys(bib.read_text(encoding="utf-8")))

    findings: list[dict[str, Any]] = []
    for key in sorted(cited - bib_keys):
        findings.append({
            "code": "COMP008", "artifact": str(tex_paths[0]), "key": key,
            "message": f"LaTeX citation key '{key}' is missing from supplied .bib file(s)",
        })
    if not nocite_all:
        for key in sorted(bib_keys - cited):
            findings.append({
                "code": "COMP008", "artifact": str(bib_paths[0]), "key": key,
                "message": f"BibTeX entry '{key}' is uncited in supplied .tex file(s)",
            })
    return findings


def _resolve_style_border(
    style_id: str, edge_local: str, styles_by_id: dict[str, ET.Element], seen: set[str]
) -> str | None:
    if not style_id or style_id in seen or style_id not in styles_by_id:
        return None
    seen.add(style_id)
    style = styles_by_id[style_id]
    edge = style.find(f"./{W_PREFIX}tblPr/{W_PREFIX}tblBorders/{W_PREFIX}{edge_local}")
    if edge is not None:
        return edge.get(f"{W_PREFIX}val", "")
    based_on = style.find(f"./{W_PREFIX}basedOn")
    if based_on is not None:
        parent_id = based_on.get(f"{W_PREFIX}val", "")
        if parent_id:
            return _resolve_style_border(parent_id, edge_local, styles_by_id, seen)
    return None


def check_docx_tables(path: Path) -> list[dict[str, Any]]:
    """Flag Word .docx tables with visible or inherited vertical borders or multi-row tables missing w:tblHeader."""
    with zipfile.ZipFile(path, "r") as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
        styles_by_id: dict[str, ET.Element] = {}
        if "word/styles.xml" in archive.namelist():
            styles_root = ET.fromstring(archive.read("word/styles.xml"))
            for style in styles_root.findall(f"./{W_PREFIX}style"):
                sid = style.get(f"{W_PREFIX}styleId")
                if sid:
                    styles_by_id[sid] = style

    findings: list[dict[str, Any]] = []
    vert_edges = ("left", "right", "insideV")
    for idx, tbl in enumerate(root.findall(f".//{W_PREFIX}body/{W_PREFIX}tbl"), start=1):
        has_vertical = False
        unverified_style: str | None = None
        tbl_style_el = tbl.find(f"./{W_PREFIX}tblPr/{W_PREFIX}tblStyle")
        style_id = tbl_style_el.get(f"{W_PREFIX}val", "") if tbl_style_el is not None else ""

        for edge_name in vert_edges:
            for cell_edge in tbl.findall(f".//{W_PREFIX}tcPr/{W_PREFIX}tcBorders/{W_PREFIX}{edge_name}"):
                val = cell_edge.get(f"{W_PREFIX}val", "")
                if val and val.lower() not in {"none", "nil"}:
                    has_vertical = True
                    break
            tbl_edge = tbl.find(f"./{W_PREFIX}tblPr/{W_PREFIX}tblBorders/{W_PREFIX}{edge_name}")
            if tbl_edge is not None:
                val = tbl_edge.get(f"{W_PREFIX}val", "")
                if val and val.lower() not in {"none", "nil"}:
                    has_vertical = True
            elif style_id:
                if style_id in styles_by_id:
                    inherited = _resolve_style_border(style_id, edge_name, styles_by_id, set())
                    if inherited and inherited.lower() not in {"none", "nil"}:
                        has_vertical = True
                else:
                    unverified_style = style_id

        if has_vertical:
            findings.append({
                "code": "COMP009", "artifact": str(path), "table": idx,
                "message": f"Word table {idx} uses visible vertical borders; prefer horizontal three-line rules (insideV=none)",
            })
        elif unverified_style:
            findings.append({
                "code": "COMP009", "artifact": str(path), "table": idx,
                "message": f"Word table {idx} references style '{unverified_style}' whose vertical borders could not be checked without word/styles.xml",
            })

        rows = tbl.findall(f"./{W_PREFIX}tr")
        if len(rows) >= 2:
            header_pr = rows[0].find(f"./{W_PREFIX}trPr/{W_PREFIX}tblHeader")
            header_val = header_pr.get(f"{W_PREFIX}val", "1") if header_pr is not None else None
            if header_pr is None or header_val.lower() in {"0", "false", "off"}:
                findings.append({
                    "code": "COMP009", "artifact": str(path), "table": idx,
                    "message": f"Word table {idx} ({len(rows)} rows) is missing w:tblHeader on row 1 for continuation pages",
                })
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--highlights", type=Path)
    parser.add_argument("--abstract", type=Path)
    parser.add_argument("--manuscript", type=Path)
    parser.add_argument("--captions", type=Path)
    parser.add_argument("--csv", type=Path, action="append", default=[])
    parser.add_argument("--text", type=Path, action="append", default=[])
    parser.add_argument("--tex", type=Path, action="append", default=[])
    parser.add_argument("--bib", type=Path, action="append", default=[])
    parser.add_argument("--docx-tables", type=Path, action="append", default=[])
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
    for tex_path in args.tex:
        findings.extend(check_text_formatting(tex_path))
        findings.extend(check_latex_tables(tex_path))
    if args.tex and args.bib:
        findings.extend(check_latex_citations(args.tex, args.bib))
    for docx_path in args.docx_tables:
        findings.extend(check_docx_tables(docx_path))
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
