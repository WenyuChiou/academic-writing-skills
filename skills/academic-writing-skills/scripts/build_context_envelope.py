#!/usr/bin/env python3
"""Deterministic Manuscript Architecture Spine & Scoped Context Envelope builder.

Extracts a compact, structured global context anchor (<= 4,500 estimated tokens by
default, SHA-256 cacheable) from a full manuscript (.docx, .tex, or .md) plus
optional companion files (CSV/TSV tables, SM, Highlights, manuscript_state.json,
and read-only .paper/claims.yml + .paper/figures.yml), so that any single-agent
scoped pass or Agent A -> Agent B delegated paragraph/subsection pass retains
whole-paper architectural invariants and downstream empirical dependency locks.
"""

from __future__ import annotations

import argparse
import csv
from hashlib import sha256
from io import BytesIO
import json
import math
from pathlib import Path
import re
import sys
from typing import Any
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"

SKIP_XML_LOCAL_TAGS = {"del", "moveFrom", "instrText", "delText", "rt", "Fallback", "sdtPr", "sdtEndPr"}

HEADING_RE = re.compile(
    r"^(?:#{1,6}\s+.+"
    r"|(?:\d+(?:\.\d+)*\.?\s+[A-Z][^\n]{1,100})"
    r"|(?:Abstract|Highlights?|Key\s+Points?|Introduction|Background|Study\s+Area(?:\s+and\s+Data)?"
    r"|Data(?:\s+and\s+Measures?)?|Materials?\s+and\s+Methods?|Methods?|Methodology"
    r"|Results?(?:\s+and\s+Discussion)?|Findings?|Discussion(?:\s+and\s+Limitations?)?"
    r"|Limitations?(?:\s+and\s+Future\s+(?:Work|Research))?|Conclusions?(?:\s+and\s+Implications?)?"
    r"|Tables?|Figures?|Figure\s+Captions?"
    r"|Appendix(?:\s+[A-Z0-9]+)?|Supplement(?:ary|al)?\s+(?:Materials?|Information)|Supporting\s+Information)\s*:?)$",
    re.IGNORECASE,
)

EXCLUDED_BACK_MATTER_RE = re.compile(
    r"^(?:#{1,6}\s+)?(?:\d+(?:\.\d+)*\.?\s+)?"
    r"(?:References?(?:\s+from\s+the\s+Supporting\s+Information)?|Bibliography|Works\s+Cited|Literature\s+Cited"
    r"|Acknowledgements?|Acknowledgments?|Open\s+Research"
    r"|Data\s+Availability(?:\s+Statement)?|Code\s+Availability"
    r"|Author\s+Contributions?|CRediT\s+Authorship.*"
    r"|Competing\s+Interests?|Conflict\s+of\s+Interest.*"
    r"|Declaration\s+of\s+(?:Competing\s+Interests?|Generative\s+AI.*)"
    r"|Funding(?:\s+Sources?)?|Ethics\s+Statement)\s*:?$",
    re.IGNORECASE,
)

RESUMABLE_BACK_SECTION_RE = re.compile(
    r"^(?:#{1,6}\s+)?(?:\d+(?:\.\d+)*\.?\s+)?"
    r"(?:Tables?|Figures?|Figure\s+Captions?"
    r"|Appendix(?:\s+[A-Z0-9]+)?.*|Supplement(?:ary|al)?\s+(?:Materials?|Information|Tables?|Figures?).*"
    r"|Supporting\s+Information.*)\s*:?$",
    re.IGNORECASE,
)

RQ_RE = re.compile(
    r"(?:^|\b)(?:RQ|SQ|H|Hypothesis|Research\s+Question|Scientific\s+Question|Proposition)\s*\d*[a-z]?[\.:)\s]"
    r"|\b(?:overarching\s+goal|primary\s+objective|main\s+objective|aim\s+of\s+this\s+(?:study|paper|work)"
    r"|this\s+(?:study|paper)\s+(?:examines|evaluates|investigates|tests|asks|develops|compares|addresses)"
    r"|we\s+(?:ask|test|examine|evaluate|investigate)\s+(?:whether|how|to\s+what\s+extent|two|three|four)"
    r"|specifically,\s+we\s+(?:test|examine|evaluate|ask|compare))\b",
    re.IGNORECASE,
)

GAP_RE = re.compile(
    r"\b(?:remains?\s+(?:unclear|untested|unresolved|underexplored|unknown|open)"
    r"|leave[s]?\s+(?:open|untested|unresolved|unclear)"
    r"|little\s+is\s+known|yet\s+to\s+be\s+(?:evaluated|tested|quantified)"
    r"|few\s+studies\s+have|rarely\s+(?:examine|quantify|compare|test)"
    r"|however,\s+(?:prior|existing|few|most|previous|current)"
    r"|gap\s+in\s+(?:existing|prior|the\s+literature|understanding)|lack[s]?\s+(?:direct|empirical|systematic))\b",
    re.IGNORECASE,
)

METHODS_STRUCTURAL_RE = re.compile(
    r"(?:=|±|≤|≥|×|÷|\bEq(?:uation)?s?\.?\s*\(?\d+|\bdefined\s+as\b|\bcalculated\s+as\b|\bcomputed\s+as\b"
    r"|\bsubtract(?:ed|ing|ion)?\b|\bminus\b|\bdifference\s+between\b|\bratio\s+of\b|\bnormaliz(?:ed|ation)\b|\bz-score\b"
    r"|\bbaseline\b|\bbenchmark\b|\bzero-change\b|\bcarry-forward\b|\bheld\s+fixed\b|\bidentical\s+across\b"
    r"|\bbootstrap\b|\bresampl(?:e|es|ing)\b|\brepetition[s]?\b|\breplicate[s]?\b|\bseed[s]?\b|\bensemble\b|\brun[s]?\b"
    r"|\bconfidence\s+interval[s]?\b|\b95%\s*CI\b|\bcredible\s+interval[s]?\b|\buncertaint(?:y|ies)\b"
    r"|\bbundl(?:e|ed|es|ing)\b|\bsimultaneously\b|\bcondition[s]?\b|\bscenario[s]?\b|\bprompt\s+length\b|\btoken[s]?\b"
    r"|\bscale\s+(?:from|of|ranging)\b|\b[01]\s*[–-]\s*[4579]\b|\bthreshold[s]?\b|\bcutoff[s]?\b"
    r"|\bN\s*=\s*[\d,]+|\bn\s*=\s*[\d,]+|\binconclusive\b|\bequivalence\b|\bcannot\s+isolate\b)",
    re.IGNORECASE,
)

NONCLAIM_RE = re.compile(
    r"\b(?:does\s+not\s+(?:establish|identify|measure|imply|predict|validate|justify|prove|isolate|capture|replace)"
    r"|do\s+not\s+(?:establish|identify|measure|imply|predict|validate|justify|prove|isolate|capture|replace)"
    r"|cannot\s+(?:isolate|replace|establish|be\s+interpreted\s+as|distinguish|identify)"
    r"|rather\s+than\s+(?:isolated|causal|clinical|actual|verified|forecasting|predicting)"
    r"|not\s+(?:future\s+prediction|clinical|diagnostic|actual\s+adoption|verified|equivalence)"
    r"|stated\s+[a-z\s]{1,25}\s+intention[s]?|retrospective\s+(?:self-report\s+)?agreement"
    r"|bounded\s+by|limit[s]?\s+(?:what\s+can\s+be\s+inferred|inference|generalizability))\b",
    re.IGNORECASE,
)

ACRONYM_DEF_RE = re.compile(r"\b([A-Z][A-Za-z0-9/-]+(?:\s+[A-Za-z0-9/-]+){1,6})\s*\(([A-Z][A-Z0-9-]{1,9})\)")

DISPLAY_CAPTION_START_RE = re.compile(
    r"^(?:\*\*|__)?((?:Figure|Fig\.|Table)\s+S?\d+[A-Za-z]?)(?:\*\*|__)?\s*[\.:—–-]\s*(.+)$",
    re.IGNORECASE,
)

DISPLAY_REF_RE = re.compile(
    r"\b(Figure|Fig\.|Figs\.|Table|Tables|Equation|Eq\.|Eqs\.)\s*\(?(S?\d+[A-Za-z]?)\)?",
    re.IGNORECASE,
)

ABBREV_PATTERNS = (
    r"\bet al\.",
    r"\be\.g\.",
    r"\bi\.e\.",
    r"\bFig\.",
    r"\bFigs\.",
    r"\bEq\.",
    r"\bEqs\.",
    r"\bSec\.",
    r"\bSecs\.",
    r"\bTab\.",
    r"\bDr\.",
    r"\bProf\.",
    r"\bMr\.",
    r"\bMs\.",
    r"\bvs\.",
    r"\bcf\.",
    r"\bca\.",
    r"\bapprox\.",
    r"\bNo\.",
    r"\bp\.",
    r"\bpp\.",
    r"\bU\.S\.",
    r"\bU\.K\.",
)

UNARY_ENDASH_RE = re.compile(r"(?:^|(?<=[\s(\[{<:=,;|/]))\u2013(?=\$?(?:\d|\.\d))")

INFORMATIVE_NUMBER_RE = re.compile(
    r"(?<![A-Za-z0-9.%)\]])"
    r"(?:[-+−]?\$(?:\d[\d,]*(?:\.\d+)?|\.\d+)[KMBkmb]?"
    r"|[-+−]?(?:\d[\d,]*\.\d+|\.\d+)(?:[eE][+−-]?\d+)?%?"
    r"|[-+−]?\d[\d,]*(?:[eE][+−-]?\d+)%?"
    r"|[-+−]\d[\d,]*%?"
    r"|\b\d+%"
    r"|\b[Nn]\s*=\s*\d[\d,]*)"
    r"(?![A-Za-z0-9]|\.\d)"
)

COMMON_CAP_STOPWORDS = {
    "The", "This", "These", "Those", "That", "In", "On", "At", "To", "For", "From", "With",
    "Under", "Across", "Between", "Within", "Among", "After", "Before", "During", "While",
    "Whereas", "Although", "However", "Moreover", "Furthermore", "Therefore", "Thus",
    "Overall", "Specifically", "First", "Second", "Third", "Finally", "Figure", "Figures",
    "Fig", "Figs", "Table", "Tables", "Section", "Sections", "Equation", "Eq", "Panel",
    "Panels", "Model", "Models", "Wave", "Waves", "Group", "Groups", "Study", "Results",
    "Methods", "Discussion", "Conclusion", "Abstract", "Highlights", "Supplementary",
    "Supporting", "Material", "Materials", "Information", "Appendix", "Mean", "Median",
    "Standard", "Confidence", "Interval", "Intervals", "Error", "Comparison", "Contrasts",
    "Base", "Analysis", "Data", "Survey", "Respondents", "Households", "Participants",
}


def estimate_tokens(text: str) -> int:
    """Conservative UTF-8 byte/3 estimator aligned with strict host packet gates."""
    if not text:
        return 0
    return math.ceil(len(text.encode("utf-8")) / 3.0)


def split_sentences(text: str) -> list[str]:
    """Split academic prose into sentences without breaking common abbreviations."""
    flattened = re.sub(r"\s+", " ", text).strip()
    if not flattened:
        return []
    protected = flattened
    for pattern in ABBREV_PATTERNS:
        protected = re.sub(
            pattern,
            lambda m: m.group(0).replace(".", "<DOT>"),
            protected,
            flags=re.IGNORECASE,
        )
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9(\[\"“'-])", protected) if p.strip()]
    return [p.replace("<DOT>", ".") for p in parts]


def _local_tag(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _extract_ooxml_text(elem: ET.Element, stats: dict[str, int] | None = None) -> str:
    chunks: list[str] = []

    def walk_math(mnode: ET.Element, acc: list[str]) -> None:
        mlocal = _local_tag(mnode.tag)
        if mlocal in SKIP_XML_LOCAL_TAGS:
            return
        if mnode.tag in (f"{{{M_NS}}}t", f"{{{W_NS}}}t") and mnode.text:
            acc.append(mnode.text)
            return
        for mchild in mnode:
            walk_math(mchild, acc)

    def walk(node: ET.Element) -> None:
        local = _local_tag(node.tag)
        if local in SKIP_XML_LOCAL_TAGS:
            return
        if node.tag == f"{{{M_NS}}}oMath":
            math_parts: list[str] = []
            walk_math(node, math_parts)
            if math_parts:
                if stats is not None:
                    stats["omath_count"] = stats.get("omath_count", 0) + 1
                chunks.append("".join(math_parts))
            return
        if node.tag == f"{{{W_NS}}}t" and node.text:
            chunks.append(node.text)
            return
        if local in {"tab", "br", "cr"}:
            chunks.append(" ")
        for child in node:
            walk(child)
        if node is not elem and local in {"p", "tc", "tr"}:
            chunks.append(" ")

    walk(elem)
    return re.sub(r"\s+", " ", "".join(chunks)).strip()


def _iter_unwrapped_ooxml_children(container: ET.Element) -> list[ET.Element]:
    """Recursively unwrap sdt/sdtContent/ins/moveTo/customXml wrappers while skipping deleted subtrees."""
    out: list[ET.Element] = []
    for child in container:
        local = _local_tag(child.tag)
        if local in SKIP_XML_LOCAL_TAGS:
            continue
        if local in {"sdt", "sdtContent", "ins", "moveTo", "customXml"}:
            out.extend(_iter_unwrapped_ooxml_children(child))
        else:
            out.append(child)
    return out


def _infer_heading_level_from_text(text: str, default: int = 1) -> int:
    stripped = text.strip()
    if stripped.startswith("#"):
        return min(6, len(stripped) - len(stripped.lstrip("#")))
    m = re.match(r"^(\d+(?:\.\d+)*)\.?\s+", stripped)
    if m:
        return min(6, m.group(1).count(".") + 1)
    return default


def _parse_docx_styles(zf: ZipFile) -> dict[str, dict[str, Any]]:
    styles: dict[str, dict[str, Any]] = {}
    if "word/styles.xml" not in zf.namelist():
        return styles
    root = ET.fromstring(zf.read("word/styles.xml"))
    raw_parents: dict[str, str] = {}
    for st in root.findall(f".//{{{W_NS}}}style"):
        sid = st.attrib.get(f"{{{W_NS}}}styleId", "")
        if not sid:
            continue
        nm_el = st.find(f"./{{{W_NS}}}name")
        nm = nm_el.attrib.get(f"{{{W_NS}}}val", sid) if nm_el is not None else sid
        out_el = st.find(f".//{{{W_NS}}}outlineLvl")
        out_val: int | None = None
        if out_el is not None:
            raw_v = out_el.attrib.get(f"{{{W_NS}}}val", "")
            if raw_v.isdigit():
                iv = int(raw_v)
                if 0 <= iv <= 8:
                    out_val = iv
        based_el = st.find(f"./{{{W_NS}}}basedOn")
        if based_el is not None:
            parent_id = based_el.attrib.get(f"{{{W_NS}}}val", "")
            if parent_id:
                raw_parents[sid] = parent_id
        styles[sid] = {"name": nm, "outline_lvl": out_val}
    # Resolve single-hop/multi-hop inherited outlineLvl safely
    for sid, info in styles.items():
        seen = {sid}
        cur = raw_parents.get(sid)
        while info["outline_lvl"] is None and cur and cur not in seen and cur in styles:
            seen.add(cur)
            if styles[cur]["outline_lvl"] is not None:
                info["outline_lvl"] = styles[cur]["outline_lvl"]
                break
            cur = raw_parents.get(cur)
    return styles


def extract_from_docx(raw_bytes: bytes) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Parse OOXML paragraphs, custom heading styles, <m:oMath>, <w:tbl>, and substantive footnotes."""
    stats: dict[str, int] = {"omath_count": 0, "table_count": 0, "skipped_reference_blocks": 0}
    note_texts: list[str] = []
    with ZipFile(BytesIO(raw_bytes)) as zf:
        styles = _parse_docx_styles(zf)
        doc = ET.fromstring(zf.read("word/document.xml"))
        for xml_name, tag_name in (("word/footnotes.xml", "footnote"), ("word/endnotes.xml", "endnote")):
            if xml_name not in zf.namelist():
                continue
            note_root = ET.fromstring(zf.read(xml_name))
            for note_el in note_root.findall(f".//{{{W_NS}}}{tag_name}"):
                if note_el.attrib.get(f"{{{W_NS}}}type") in {"separator", "continuationSeparator", "continuationNotice"}:
                    continue
                ntxt = _extract_ooxml_text(note_el, stats)
                if ntxt and re.search(r"[A-Za-z\u3400-\u9fff]", ntxt):
                    nid = note_el.attrib.get(f"{{{W_NS}}}id", "")
                    note_texts.append(f"[Note {nid}] {ntxt}" if nid else ntxt)

    body = doc.find(f"./{{{W_NS}}}body")
    if body is None:
        return [], stats

    blocks: list[dict[str, Any]] = []
    idx = 0
    in_excluded_back_matter = False
    in_highlights_or_abstract = False

    for child in _iter_unwrapped_ooxml_children(body):
        local = _local_tag(child.tag)
        if local == "p":
            text = _extract_ooxml_text(child, stats)
            if not text:
                continue
            p_pr = child.find(f"./{{{W_NS}}}pPr")
            style_id = "Normal"
            p_out_lvl: int | None = None
            has_num_pr = False
            if p_pr is not None:
                st_el = p_pr.find(f"./{{{W_NS}}}pStyle")
                if st_el is not None:
                    style_id = st_el.attrib.get(f"{{{W_NS}}}val", "Normal")
                out_el = p_pr.find(f"./{{{W_NS}}}outlineLvl")
                if out_el is not None:
                    rv = out_el.attrib.get(f"{{{W_NS}}}val", "")
                    if rv.isdigit() and 0 <= int(rv) <= 8:
                        p_out_lvl = int(rv)
                has_num_pr = p_pr.find(f"./{{{W_NS}}}numPr") is not None

            st_info = styles.get(style_id, {"name": style_id, "outline_lvl": None})
            style_name = str(st_info["name"])
            sname_low = style_name.lower()
            eff_outline = p_out_lvl if p_out_lvl is not None else st_info["outline_lvl"]

            if sname_low in {"bibliography", "references", "reference"}:
                if EXCLUDED_BACK_MATTER_RE.match(text.lstrip("#").strip()):
                    in_excluded_back_matter = True
                    in_highlights_or_abstract = False
                stats["skipped_reference_blocks"] += 1
                continue

            is_heading = False
            heading_level = 1
            if sname_low == "title":
                is_heading = True
                heading_level = 0
            elif eff_outline is not None and 0 <= eff_outline <= 5:
                if idx == 0 and eff_outline == 0 and len(text) > 45 and not HEADING_RE.match(text):
                    # Manuscript title styled as Heading 1 at block 0
                    is_heading = False
                else:
                    is_heading = True
                    heading_level = eff_outline + 1
            elif "heading" in sname_low:
                is_heading = True
                m_lvl = re.search(r"(\d+)", sname_low)
                heading_level = int(m_lvl.group(1)) if m_lvl else 2
            elif len(text) <= 105 and (HEADING_RE.match(text) or EXCLUDED_BACK_MATTER_RE.match(text)):
                is_heading = True
                heading_level = _infer_heading_level_from_text(text, 1)
            elif (
                has_num_pr
                and not in_highlights_or_abstract
                and "abstract" not in sname_low
                and len(text) <= 90
                and not text.endswith((".", ";", "?", "!"))
                and not re.search(
                    r"\b(?:is|are|was|were|have|has|had|can|could|may|might|reduce|reduces|show|shows)\b",
                    text.lower(),
                )
            ):
                is_heading = True
                heading_level = 1

            if is_heading:
                clean_h = text.lstrip("#").strip()
                if EXCLUDED_BACK_MATTER_RE.match(clean_h):
                    in_excluded_back_matter = True
                    in_highlights_or_abstract = False
                    stats["skipped_reference_blocks"] += 1
                    continue
                if in_excluded_back_matter:
                    if RESUMABLE_BACK_SECTION_RE.match(clean_h):
                        in_excluded_back_matter = False
                    else:
                        stats["skipped_reference_blocks"] += 1
                        continue
                in_highlights_or_abstract = bool(
                    re.search(r"\b(?:key\s+points?|highlights?|abstract)\b", clean_h, re.IGNORECASE)
                )
            else:
                if in_excluded_back_matter:
                    stats["skipped_reference_blocks"] += 1
                    continue

            blocks.append(
                {
                    "id": f"P{idx:03d}",
                    "index": idx,
                    "kind": "heading" if is_heading else "paragraph",
                    "style": style_name,
                    "style_id": style_id,
                    "is_heading": is_heading,
                    "heading_level": heading_level if is_heading else None,
                    "text": text,
                }
            )
            idx += 1

        elif local == "tbl":
            if in_excluded_back_matter:
                continue
            rows_out: list[list[str]] = []
            for tr in _iter_unwrapped_ooxml_children(child):
                if _local_tag(tr.tag) != "tr":
                    continue
                cells = [
                    _extract_ooxml_text(tc, stats)
                    for tc in _iter_unwrapped_ooxml_children(tr)
                    if _local_tag(tc.tag) == "tc"
                ]
                if any(cells):
                    rows_out.append(cells)
            if not rows_out:
                continue
            stats["table_count"] += 1
            rendered_rows = [" | ".join(r) for r in rows_out]
            blocks.append(
                {
                    "id": f"T{stats['table_count']:02d}",
                    "index": idx,
                    "kind": "table",
                    "style": "Table",
                    "style_id": "Table",
                    "is_heading": False,
                    "heading_level": None,
                    "rows": rows_out,
                    "text": "\n".join(rendered_rows),
                }
            )
            idx += 1

    if note_texts:
        blocks.append(
            {
                "id": f"P{idx:03d}",
                "index": idx,
                "kind": "heading",
                "style": "Heading 2",
                "style_id": "Heading2",
                "is_heading": True,
                "heading_level": 1,
                "text": "Supporting Information: Footnotes",
            }
        )
        idx += 1
        for ntxt in note_texts:
            blocks.append(
                {
                    "id": f"P{idx:03d}",
                    "index": idx,
                    "kind": "paragraph",
                    "style": "Footnote Text",
                    "style_id": "FootnoteText",
                    "is_heading": False,
                    "heading_level": None,
                    "text": ntxt,
                }
            )
            idx += 1

    return blocks, stats


def _expand_latex_inputs(
    path: Path,
    allowed_root: Path,
    seen: set[Path] | None = None,
    depth: int = 0,
    child_digests: dict[str, str] | None = None,
    expansion_budget: list[int] | None = None,
) -> str:
    ancestors = set() if seen is None else set(seen)
    if expansion_budget is None:
        expansion_budget = [64]
    resolved = path.resolve()
    if (
        depth > 5
        or expansion_budget[0] <= 0
        or resolved in ancestors
        or not resolved.is_relative_to(allowed_root)
        or not resolved.is_file()
    ):
        return ""
    expansion_budget[0] -= 1
    next_ancestors = ancestors | {resolved}
    raw_bytes = resolved.read_bytes()
    if depth > 0 and child_digests is not None:
        child_digests[resolved.relative_to(allowed_root).as_posix()] = sha256(raw_bytes).hexdigest()
    raw_text = raw_bytes.decode("utf-8", errors="replace")
    lines = [re.sub(r"(?<!\\)%.*$", "", ln) for ln in raw_text.splitlines()]
    stripped = "\n".join(lines)

    def repl(match: re.Match[str]) -> str:
        rel = match.group(1).strip()
        if not rel or ".." in Path(rel).parts:
            return ""
        cand_res: Path | None = None
        for base_dir in (allowed_root, resolved.parent):
            raw_cand = base_dir / rel
            candidates = (
                (raw_cand, raw_cand.with_name(raw_cand.name + ".tex"))
                if raw_cand.suffix.lower() != ".tex"
                else (raw_cand,)
            )
            for candidate in candidates:
                try:
                    resolved_cand = candidate.resolve()
                except OSError:
                    continue
                if resolved_cand.is_relative_to(allowed_root) and resolved_cand.is_file():
                    cand_res = resolved_cand
                    break
            if cand_res is not None:
                break
        if cand_res is None:
            return ""
        return (
            "\n"
            + _expand_latex_inputs(
                cand_res,
                allowed_root,
                next_ancestors,
                depth + 1,
                child_digests=child_digests,
                expansion_budget=expansion_budget,
            )
            + "\n"
        )

    return re.sub(r"\\(?:input|include)\s*\{([^}]+)\}", repl, stripped)


def _find_tex_command_span(text: str, cmd_names: tuple[str, ...]) -> tuple[int, int, str] | None:
    pattern = re.compile(rf"\\(?:{'|'.join(cmd_names)})\*?(?:\[[^\]]*\])?\s*\{{", flags=re.DOTALL)
    m = pattern.search(text)
    if not m:
        return None
    arg_start = m.end()
    depth = 1
    idx = arg_start
    while idx < len(text) and depth > 0:
        ch = text[idx]
        if ch == "\\":
            idx += 2
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return m.start(), idx + 1, text[arg_start:idx]
        idx += 1
    return None


def _strip_tex_commands(text: str, cmd_names: tuple[str, ...]) -> str:
    cur = text
    for _ in range(32):
        span = _find_tex_command_span(cur, cmd_names)
        if span is None:
            break
        s_idx, e_idx, _ = span
        cur = cur[:s_idx] + " " + cur[e_idx:]
    return cur


def _clean_tex_inline(text: str) -> str:
    cur = _strip_tex_commands(text, ("thanks", "footnote"))
    unwrap_re = re.compile(r"\\(?:textbf|textit|emph|textrm|texttt|text)\{([^{}]*)\}")
    for _ in range(6):
        nxt = unwrap_re.sub(r"\1", cur)
        if nxt == cur:
            break
        cur = nxt
    cur = re.sub(r"\$([^$]+)\$", r"\1", cur)
    cur = cur.replace(r"\\", " ")
    return re.sub(r"\s+", " ", cur).strip()


def extract_from_tex(path: Path, raw_text: str | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    child_digests: dict[str, str] = {}
    stats: dict[str, Any] = {
        "omath_count": 0,
        "table_count": 0,
        "skipped_reference_blocks": 0,
        "child_tex_digests": child_digests,
    }
    allowed_root = path.resolve().parent
    body = _expand_latex_inputs(path, allowed_root, child_digests=child_digests) if raw_text is None and path.is_file() else (
        "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in (raw_text or "").splitlines())
    )
    abstract_env_re = re.compile(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", flags=re.DOTALL)

    title_span = _find_tex_command_span(body, ("title",))
    extracted_title = _clean_tex_inline(title_span[2]) if title_span else ""

    has_custom_table_num = bool(re.search(r"\\(?:renewcommand\*?\s*\{\\thetable\}|setcounter\{table\})", body))
    has_custom_fig_num = bool(re.search(r"\\(?:renewcommand\*?\s*\{\\thefigure\}|setcounter\{figure\})", body))

    preamble_abstract = ""
    doc_m = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", body, flags=re.DOTALL)
    if doc_m:
        preamble = body[:doc_m.start()]
        body = doc_m.group(1)
        if not abstract_env_re.search(body):
            pre_abs_m = abstract_env_re.search(preamble)
            if pre_abs_m:
                preamble_abstract = pre_abs_m.group(1).strip()
            else:
                abs_span = _find_tex_command_span(preamble, ("abstract",))
                if abs_span:
                    preamble_abstract = abs_span[2].strip()

    body = _strip_tex_commands(body, ("title", "author", "affil", "affiliation", "address", "date", "thanks"))

    # Count display math environments before unwrapping
    math_envs = re.findall(r"\\begin\{(?:equation\*?|align\*?|gather\*?)\}.*?\\end\{(?:equation\*?|align\*?|gather\*?)\}", body, flags=re.DOTALL)
    inline_maths = re.findall(r"\$[^$\n]+\$", body)
    stats["omath_count"] = len(math_envs) + len(inline_maths)

    # Cut explicit bibliography environments
    bib_m = re.search(r"\\(?:begin\{thebibliography\}|bibliography\{|printbibliography\b)", body)
    if bib_m:
        tail = body[bib_m.start():]
        stats["skipped_reference_blocks"] += max(1, len(re.findall(r"\\bibitem\b|\n\s*\n", tail)))
        appendix_m = re.search(r"\\appendix\b|\\section\*?\{(?:Appendix|Supplement|Tables?|Figures?)", tail, re.IGNORECASE)
        body = body[:bib_m.start()] + ("\n\n" + tail[appendix_m.start():] if appendix_m else "")

    if preamble_abstract:
        body = f"\n\n\\begin{{abstract}}\n{preamble_abstract}\n\\end{{abstract}}\n\n" + body

    # Extract tabular tables as markdown-style pipe blocks
    tables_captured: list[list[list[str]]] = []

    def _tbl_repl(m: re.Match[str]) -> str:
        content = m.group(1)
        rows: list[list[str]] = []
        for raw_row in content.split(r"\\"):
            cleaned_row = re.sub(r"\\(?:toprule|midrule|bottomrule|hline|cline\{[^}]*\})", " ", raw_row)
            for _ in range(4):
                cleaned_row = re.sub(r"\\(?:textbf|textit|emph|textrm|texttt|text)\{([^{}]*)\}", r"\1", cleaned_row)
            cleaned_row = re.sub(r"\$([^$]+)\$", r"\1", cleaned_row).strip()
            if not cleaned_row or not re.search(r"(?<!\\)&", cleaned_row):
                continue
            cells = [
                re.sub(
                    r"\s+",
                    " ",
                    c.replace(r"\%", "%").replace(r"\$", "$").replace(r"\&", "&").replace("---", "—").replace("--", "–"),
                ).strip()
                for c in re.split(r"(?<!\\)&", cleaned_row)
            ]
            if any(cells):
                rows.append(cells)
        if not rows:
            return "\n"
        tables_captured.append(rows)
        return f"\n\n<<LATEX_TABLE_{len(tables_captured) - 1}>>\n\n"

    body = re.sub(
        r"\\begin\{(?:tabular\*?|tabularx|longtable)\}(?:\[[^\]]*\])?(?:\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\})*(.*?)\\end\{(?:tabular\*?|tabularx|longtable)\}",
        _tbl_repl,
        body,
        flags=re.DOTALL,
    )
    body = re.sub(
        r"\\begin\{abstract\}(.*?)\\end\{abstract\}",
        lambda m: f"\n\n# Abstract\n\n{m.group(1).strip()}\n\n",
        body,
        flags=re.DOTALL,
    )

    def _unwrap_captions(seg: str, auto_kind: str | None = None, counter: list[int] | None = None) -> str:
        cur = seg
        for _ in range(64):
            span = _find_tex_command_span(cur, ("caption",))
            if span is None:
                break
            s_idx, e_idx, inner = span
            probe = _clean_tex_inline(re.sub(r"\\label(?:\[[^\]]*\])*\{[^}]*\}", " ", inner))
            already_labeled = bool(
                re.match(r"^(?:\*\*|__)?(?:Table|Tab\.|Figure|Fig\.|Figs\.)\s+S?\d+", probe, re.IGNORECASE)
            )
            if auto_kind is not None and counter is not None and inner.strip():
                counter[0] += 1
                if not already_labeled:
                    inner = f"{auto_kind} {counter[0]}: {inner.lstrip()}"
            cur = cur[:s_idx] + f"\n\n{inner}\n\n" + cur[e_idx:]
        return cur

    app_split = re.search(r"\\appendix\b", body)
    pre_app = body[:app_split.start()] if app_split else body
    post_app = body[app_split.start():] if app_split else ""
    tbl_counter = [0]
    fig_counter = [0]

    def _float_env_repl(m: re.Match[str]) -> str:
        env_nm = m.group(1)
        env_body = m.group(2)
        if env_nm.startswith("table") and not has_custom_table_num:
            env_body = _unwrap_captions(env_body, auto_kind="Table", counter=tbl_counter)
        elif env_nm.startswith("figure") and not has_custom_fig_num:
            env_body = _unwrap_captions(env_body, auto_kind="Figure", counter=fig_counter)
        else:
            env_body = _unwrap_captions(env_body)
        return f"\\begin{{{env_nm}}}{env_body}\\end{{{env_nm}}}"

    pre_app = re.sub(
        r"\\begin\{(table\*?|figure\*?)\}(.*?)\\end\{\1\}",
        _float_env_repl,
        pre_app,
        flags=re.DOTALL,
    )
    body = _unwrap_captions(pre_app) + (_unwrap_captions(post_app) if post_app else "")

    sec_map = {"section": "#", "subsection": "##", "subsubsection": "###", "paragraph": "####"}
    for cmd, hashes in sec_map.items():
        body = re.sub(
            rf"\\{cmd}\*?(?:\[[^\]]*\])?\{{([^{{}}]*(?:\{{[^{{}}]*\}}[^{{}}]*)*)\}}",
            lambda m, h=hashes: f"\n\n{h} {re.sub(r'\\s+', ' ', m.group(1)).strip()}\n\n",
            body,
        )
    body = re.sub(r"\\label(?:\[[^\]]*\])*\{[^}]*\}", " ", body)
    body = re.sub(r"\\(?:ref|eqref|autoref|pageref|cite[a-zA-Z*]*)(?:\[[^\]]*\])*\{([^}]*)\}", r"(\1)", body)
    unwrap_re = re.compile(r"\\(?:textbf|textit|emph|textrm|texttt|text)\{([^{}]*)\}")
    for _ in range(6):
        nxt_body = unwrap_re.sub(r"\1", body)
        if nxt_body == body:
            break
        body = nxt_body
    body = re.sub(r"\$([^$]+)\$", r"\1", body)
    body = body.replace(r"\%", "%").replace(r"\$", "$").replace(r"\&", "&").replace("---", "—").replace("--", "–")
    body = re.sub(r"\\(?:begin|end)\{[^}]+\}(?:\[[^\]]*\])?", "\n", body)
    body = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", " ", body)

    if extracted_title:
        body = extracted_title + "\n\n" + body

    blocks, md_stats = extract_from_markdown(body, pre_extracted_tables=tables_captured)
    stats["table_count"] = md_stats["table_count"]
    stats["skipped_reference_blocks"] += md_stats["skipped_reference_blocks"]
    return blocks, stats


def extract_from_markdown(
    text: str,
    pre_extracted_tables: list[list[list[str]]] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    stats: dict[str, int] = {"omath_count": len(re.findall(r"\$[^$\n]+\$", text)), "table_count": 0, "skipped_reference_blocks": 0}
    blocks: list[dict[str, Any]] = []
    raw_chunks: list[tuple[str, str]] = []
    buf: list[str] = []
    fence_buf: list[str] = []
    fence_marker: str | None = None
    in_pipe_table = False
    for raw_ln in text.strip().splitlines():
        s_ln = raw_ln.strip()
        if fence_marker is not None:
            fence_buf.append(raw_ln)
            if re.match(rf"^{re.escape(fence_marker[0])}{{{len(fence_marker)},}}\s*$", s_ln):
                raw_chunks.append(("fenced", "\n".join(fence_buf)))
                fence_buf = []
                fence_marker = None
            continue
        m_fence = re.match(r"^(?:(`{3,})[^`]*|(~{3,}).*)$", s_ln)
        if m_fence:
            if buf:
                raw_chunks.append(("normal", "\n".join(buf)))
                buf = []
            in_pipe_table = False
            fence_marker = m_fence.group(1) or m_fence.group(2)
            fence_buf = [raw_ln]
            continue
        if not s_ln:
            if buf:
                raw_chunks.append(("normal", "\n".join(buf)))
                buf = []
            in_pipe_table = False
            continue
        is_atx = bool(re.match(r"^#{1,6}\s+\S", s_ln))
        is_placeholder = bool(re.fullmatch(r"<<LATEX_TABLE_\d+>>", s_ln))
        is_pipe = s_ln.startswith("|") and s_ln.endswith("|")
        if is_atx or is_placeholder:
            if buf:
                raw_chunks.append(("normal", "\n".join(buf)))
                buf = []
            in_pipe_table = False
            raw_chunks.append(("normal", s_ln))
            continue
        if is_pipe != in_pipe_table:
            if buf:
                raw_chunks.append(("normal", "\n".join(buf)))
                buf = []
            in_pipe_table = is_pipe
        buf.append(s_ln)
    if fence_buf:
        raw_chunks.append(("fenced", "\n".join(fence_buf)))
    if buf:
        raw_chunks.append(("normal", "\n".join(buf)))
    idx = 0
    in_excluded_back_matter = False

    def emit_heading(h_line: str) -> None:
        nonlocal idx, in_excluded_back_matter
        clean_h = h_line.lstrip("#").strip()
        lvl = _infer_heading_level_from_text(h_line, 1)
        if idx == 0 and lvl == 1 and len(clean_h) > 45 and not HEADING_RE.match(clean_h):
            blocks.append(
                {
                    "id": f"P{idx:03d}",
                    "index": idx,
                    "kind": "paragraph",
                    "style": "Title",
                    "style_id": "Title",
                    "is_heading": False,
                    "heading_level": None,
                    "text": clean_h,
                }
            )
            idx += 1
            return
        if EXCLUDED_BACK_MATTER_RE.match(clean_h):
            in_excluded_back_matter = True
            stats["skipped_reference_blocks"] += 1
            return
        if in_excluded_back_matter:
            if RESUMABLE_BACK_SECTION_RE.match(clean_h):
                in_excluded_back_matter = False
            else:
                stats["skipped_reference_blocks"] += 1
                return
        blocks.append(
            {
                "id": f"P{idx:03d}",
                "index": idx,
                "kind": "heading",
                "style": f"Heading {lvl}",
                "style_id": f"Heading{lvl}",
                "is_heading": True,
                "heading_level": lvl,
                "text": clean_h,
            }
        )
        idx += 1

    for chunk_kind, chunk in raw_chunks:
        cleaned = chunk.strip()
        if not cleaned:
            continue
        if chunk_kind == "fenced":
            if in_excluded_back_matter:
                stats["skipped_reference_blocks"] += 1
                continue
            blocks.append(
                {
                    "id": f"P{idx:03d}",
                    "index": idx,
                    "kind": "paragraph",
                    "style": "Code Block",
                    "style_id": "CodeBlock",
                    "is_heading": False,
                    "heading_level": None,
                    "text": cleaned,
                }
            )
            idx += 1
            continue
        m_placeholder = re.fullmatch(r"<<LATEX_TABLE_(\d+)>>", cleaned)
        if m_placeholder and pre_extracted_tables is not None:
            if in_excluded_back_matter:
                continue
            rows = pre_extracted_tables[int(m_placeholder.group(1))]
            stats["table_count"] += 1
            blocks.append(
                {
                    "id": f"T{stats['table_count']:02d}",
                    "index": idx,
                    "kind": "table",
                    "style": "Table",
                    "style_id": "Table",
                    "is_heading": False,
                    "heading_level": None,
                    "rows": rows,
                    "text": "\n".join(" | ".join(r) for r in rows),
                }
            )
            idx += 1
            continue

        lines = [ln.strip() for ln in cleaned.splitlines() if ln.strip()]
        if not lines:
            continue

        # Markdown pipe table
        if len(lines) >= 2 and all(ln.startswith("|") and ln.endswith("|") for ln in lines[:2]):
            if in_excluded_back_matter:
                continue
            rows = []
            for ln in lines:
                if re.fullmatch(r"\|[\s:-]+\|([\s:-]+\|)*", ln):
                    continue
                cells = [c.strip() for c in ln.strip("|").split("|")]
                rows.append(cells)
            if rows:
                stats["table_count"] += 1
                blocks.append(
                    {
                        "id": f"T{stats['table_count']:02d}",
                        "index": idx,
                        "kind": "table",
                        "style": "Table",
                        "style_id": "Table",
                        "is_heading": False,
                        "heading_level": None,
                        "rows": rows,
                        "text": "\n".join(" | ".join(r) for r in rows),
                    }
                )
                idx += 1
                continue

        if lines[0].startswith("#"):
            emit_heading(lines[0])
            rest_lines = lines[1:]
            if rest_lines and not in_excluded_back_matter:
                rest = re.sub(r"\s+", " ", " ".join(rest_lines)).strip()
                if rest:
                    blocks.append(
                        {
                            "id": f"P{idx:03d}",
                            "index": idx,
                            "kind": "paragraph",
                            "style": "Normal",
                            "style_id": "Normal",
                            "is_heading": False,
                            "heading_level": None,
                            "text": rest,
                        }
                    )
                    idx += 1
            continue

        single = re.sub(r"\s+", " ", " ".join(lines)).strip()
        if len(single) <= 105 and (HEADING_RE.match(single) or EXCLUDED_BACK_MATTER_RE.match(single)):
            emit_heading(single)
            continue

        if in_excluded_back_matter:
            stats["skipped_reference_blocks"] += 1
            continue

        blocks.append(
            {
                "id": f"P{idx:03d}",
                "index": idx,
                "kind": "paragraph",
                "style": "Normal",
                "style_id": "Normal",
                "is_heading": False,
                "heading_level": None,
                "text": single,
            }
        )
        idx += 1

    return blocks, stats


def load_manuscript_blocks(path: Path) -> tuple[list[dict[str, Any]], str, dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(f"Manuscript file not found: {path}")
    raw = path.read_bytes()
    digest = sha256(raw).hexdigest()
    suffix = path.suffix.lower()
    if suffix == ".docx":
        blocks, stats = extract_from_docx(raw)
        return blocks, digest, stats
    if suffix == ".tex":
        blocks, stats = extract_from_tex(path)
        child_digests = stats.get("child_tex_digests") or {}
        if child_digests:
            hasher = sha256()
            hasher.update(f"root:{digest}\n".encode("utf-8"))
            for child_rel, child_sha in sorted(child_digests.items()):
                hasher.update(f"child:{child_rel}:{child_sha}\n".encode("utf-8"))
            digest = hasher.hexdigest()
        return blocks, digest, stats
    blocks, stats = extract_from_markdown(raw.decode("utf-8", errors="replace"))
    return blocks, digest, stats


def classify_section_role(heading: str, parent_role: str = "other") -> str:
    h = heading.lower().strip()
    if re.search(r"\b(?:highlights?|key\s+points?)\b", h):
        return "highlights"
    if re.match(r"^(?:\d+\.?\s*)?abstract\b", h):
        return "abstract"
    if re.match(r"^(?:tables?|figures?|figure\s+captions?)\s*:?$", h):
        return "displays"
    if "limitation" in h and "discussion" not in h:
        return "limitations"
    if any(k in h for k in ("supplement", "supporting information", "appendix")) or re.search(r"\b(?:table|figure)\s+s\d", h):
        return "supplement"
    if any(k in h for k in ("introduction", "background", "motivation", "literature review")):
        return "introduction"
    if any(k in h for k in ("conclusion", "concluding")):
        return "conclusion"
    if "discussion" in h:
        return "discussion"
    if any(k in h for k in ("result", "finding", "empirical evaluation", "model diagnostics")):
        return "results"
    if any(
        k in h
        for k in (
            "study area", "data", "measure", "method", "material", "experimental",
            "simulation", "estimand", "protocol", "questionnaire", "framework",
            "model", "module", "scenario",
        )
    ):
        return parent_role if parent_role in {"results", "discussion", "supplement"} else "methods"
    return parent_role if parent_role != "other" else "other"


def _normalize_display_key(kind: str, num: str) -> str:
    k = kind.lower().rstrip("s.")
    n = num.upper() if num.upper().startswith("S") else num
    if k.startswith("fig"):
        return f"Figure {n}"
    if k.startswith("tab"):
        return f"Table {n}"
    if k.startswith("eq"):
        return f"Equation ({n})"
    return f"{kind} {n}"


def _load_companion_displays(companion_paths: list[Path]) -> tuple[dict[str, str], dict[str, str]]:
    """Read companion CSV/TSV/MD/DOCX files into display slices and hashes."""
    slices: dict[str, str] = {}
    hashes: dict[str, str] = {}
    for cpath in companion_paths:
        if not cpath.is_file():
            raise FileNotFoundError(f"Companion file not found: {cpath}")
        raw = cpath.read_bytes()
        hashes[cpath.name] = sha256(raw).hexdigest()
        suf = cpath.suffix.lower()
        stem_m = re.search(r"(table|figure|fig)[_\s-]*(s?\d+[a-z]?)", cpath.stem, re.IGNORECASE)
        inferred_key = _normalize_display_key(stem_m.group(1), stem_m.group(2)) if stem_m else cpath.name
        if suf in {".csv", ".tsv"}:
            delim = "\t" if suf == ".tsv" else ","
            text = raw.decode("utf-8", errors="replace")
            reader = list(csv.reader(text.splitlines(), delimiter=delim))
            rendered = "\n".join(" | ".join(row) for row in reader[:40] if any(row))
            slices[inferred_key] = f"[Companion {cpath.name}]\n{rendered}"
        else:
            c_blocks, c_digest, _ = load_manuscript_blocks(cpath)
            hashes[cpath.name] = c_digest
            c_table_caps: dict[str, str] = {}
            annotate_manuscript_blocks(c_blocks, table_captions=c_table_caps)
            for b in c_blocks:
                if b["is_heading"]:
                    continue
                if b["kind"] == "table":
                    t_dkey = b.get("display_key") or f"Table ({b['id']})"
                    cap_txt = c_table_caps.get(b["id"]) or b.get("caption", "")
                    cap_prefix = f"{cap_txt}\n" if cap_txt else ""
                    if t_dkey != f"Table ({b['id']})":
                        slices[t_dkey] = f"[{cpath.name} {b['id']}] {cap_prefix}{b['text']}"
                    else:
                        slices[f"{cpath.name}:{b['id']}"] = f"[{cpath.name} {b['id']}]\n{b['text']}"
            for b in c_blocks:
                if b["is_heading"] or b["kind"] == "table":
                    continue
                cap_m = DISPLAY_CAPTION_START_RE.match(b["text"])
                if cap_m:
                    parts = cap_m.group(1).split(None, 1)
                    if len(parts) == 2:
                        dkey = _normalize_display_key(parts[0], parts[1])
                        if dkey not in slices:
                            slices[dkey] = f"[{cpath.name} {b['id']}] {b['text']}"
            if inferred_key not in slices and c_blocks:
                joined = "\n".join(f"[{b['id']}] {b['text']}" for b in c_blocks[:20])
                slices[inferred_key] = f"[Companion {cpath.name}]\n{joined}"
    return slices, hashes


def _load_simple_yaml_records(path: Path) -> list[dict[str, Any]]:
    """Read list-of-dicts YAML safely using PyYAML when installed or stdlib fallback."""
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        import yaml  # type: ignore
        loaded = yaml.safe_load(text)
        if isinstance(loaded, list):
            return [x for x in loaded if isinstance(x, dict)]
        if isinstance(loaded, dict):
            for v in loaded.values():
                if isinstance(v, list) and all(isinstance(x, dict) for x in v):
                    return v
            return [loaded]
    except Exception:
        pass

    records: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m_item = re.match(r"^\s*-\s+([A-Za-z0-9_]+)\s*:\s*(.*)$", line)
        if m_item:
            if current:
                records.append(current)
            current = {m_item.group(1): m_item.group(2).strip().strip("\"'")}
            continue
        m_kv = re.match(r"^\s+([A-Za-z0-9_]+)\s*:\s*(.*)$", line)
        if m_kv and current is not None:
            val = m_kv.group(2).strip().strip("\"'")
            if val:
                current[m_kv.group(1)] = val
    if current:
        records.append(current)
    return records


CI_LABEL_RE = re.compile(
    r"\b(?:90|95|99)%\s*(?:CIs?|CrIs?|confidence\s+intervals?|credible\s+intervals?)\b",
    re.IGNORECASE,
)


def _canonical_dep_number(raw_tok: str) -> tuple[str, str] | None:
    cleaned = raw_tok.replace("−", "-").replace("\u2013", "-").strip()
    if re.match(r"^[Nn]\s*=", cleaned):
        surface = re.sub(r"^[Nn]\s*=\s*", "", cleaned).strip()
        digits = surface.replace(",", "")
        return (digits, surface) if digits else None
    unsigned = cleaned.lstrip("+-").replace(",", "").strip()
    if not unsigned or re.fullmatch(r"(?:19|20)\d{2}", unsigned):
        return None
    prefix = ""
    if unsigned.startswith("$"):
        prefix = "$"
        unsigned = unsigned[1:]
    if unsigned.startswith("."):
        unsigned = "0" + unsigned
    sci_m = re.fullmatch(r"(\d+(?:\.\d+)?)[eE]([+-]?)0*(\d+)(%?)", unsigned)
    if sci_m:
        mant, exp_sgn, exp_num, pct = sci_m.groups()
        exp_prefix = "-" if exp_sgn == "-" else ""
        unsigned = f"{mant}e{exp_prefix}{exp_num or '0'}{pct}"
    canon = (prefix + unsigned.upper()) if prefix else unsigned
    return canon, cleaned


DEP_LOCATOR_RE = re.compile(
    r"\b(?:Figures?|Figs?\.|Tables?|Sections?|Secs?\.|Subsections?|Chapters?|Equations?|Eqs?\.|Panels?|Appendix)"
    r"\s*(?:\(S?\d+(?:\.\d+)*[A-Za-z]?\)|S?\d+(?:\.\d+)*[A-Za-z]?)"
    r"|\b(?:RQ|SQ|H|Hypothesis|Proposition|Study|Wave|Step|Pass|Stage|Tier|Model)\s*\d+[A-Za-z]?\b"
    r"|\[\s*\d+(?:\s*(?:,|–|-)\s*\d+)*\s*\]",
    re.IGNORECASE,
)
DEP_MODEL_SIZE_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9.]*(?:-[A-Za-z0-9.]+)*-\d+(?:\.\d+)?[BMKbmk]\b")


def _extract_entities_and_numbers(text: str) -> tuple[dict[str, str], set[str]]:
    scrubbed = CI_LABEL_RE.sub(" ", text).replace("\u2212", "-")
    scrubbed = DEP_MODEL_SIZE_RE.sub(" ", scrubbed)
    scrubbed = DEP_LOCATOR_RE.sub(" ", scrubbed)
    scrubbed = re.sub(r"\b(?:19|20)\d{2}\s*[–-]\s*(?:19|20)\d{2}\b", " ", scrubbed)
    scrubbed = re.sub(r"\b[01]\s*[–-]\s*[4579](?=-point|\s+scale)\b", " ", scrubbed, flags=re.IGNORECASE)
    scrubbed = UNARY_ENDASH_RE.sub("-", scrubbed)
    nums_by_canon: dict[str, str] = {}
    for m in INFORMATIVE_NUMBER_RE.finditer(scrubbed):
        parsed = _canonical_dep_number(m.group(0))
        if parsed is None:
            continue
        canon, surface = parsed
        # Prefer explicitly signed surface representation if present
        if canon not in nums_by_canon or (surface[:1] in "+-" and nums_by_canon[canon][:1] not in "+-"):
            nums_by_canon[canon] = surface
    # Named subscales, models, groups, scenarios (capitalized tokens or hyphenated model/group IDs)
    entities: set[str] = set()
    for m in re.finditer(r"\b([A-Z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)+|[A-Z][a-z]{3,18}s?|[A-Z]{2,8})\b", text):
        tok = m.group(1)
        if tok in COMMON_CAP_STOPWORDS or tok.rstrip("s") in COMMON_CAP_STOPWORDS:
            continue
        if re.fullmatch(r"(?:19|20)\d{2}[a-z]?", tok):
            continue
        entities.add(tok)
    return nums_by_canon, entities


def compute_downstream_dependencies(
    blocks: list[dict[str, Any]],
    target_indices: list[int],
) -> list[dict[str, Any]]:
    """Find numbers and named analytical entities in target blocks also cited in Abstract/Highlights/Discussion/Conclusion."""
    target_set = set(target_indices)
    prose_indices = [
        i for i in target_indices
        if i < len(blocks) and not blocks[i]["is_heading"] and blocks[i].get("kind") != "table"
    ]
    eff_indices = prose_indices if prose_indices else [
        i for i in target_indices if i < len(blocks) and not blocks[i]["is_heading"]
    ]
    target_text = " ".join(blocks[i]["text"] for i in eff_indices)
    target_nums, target_entities = _extract_entities_and_numbers(target_text)
    if not target_nums and not target_entities:
        return []

    deps_by_item: dict[str, dict[str, Any]] = {}
    downstream_roles = {"abstract", "highlights", "discussion", "limitations", "conclusion", "results"}

    for idx, b in enumerate(blocks):
        if idx in target_set or b["is_heading"] or b["kind"] == "table":
            continue
        role = b.get("section_role", "other")
        if role not in downstream_roles:
            continue
        # For other results subsections, only track downstream subsections after target
        if role == "results" and target_indices and idx < max(target_indices):
            continue

        b_text = b["text"]
        b_nums, b_entities = _extract_entities_and_numbers(b_text)
        shared_num_keys = sorted(set(target_nums.keys()) & set(b_nums.keys()))
        shared_ents = sorted(target_entities & b_entities)

        for canon_key in shared_num_keys:
            item = target_nums[canon_key]
            rec = deps_by_item.setdefault(
                canon_key,
                {"item": item, "kind": "numeric_value", "downstream_locations": []},
            )
            if len(rec["downstream_locations"]) < 4:
                rec["downstream_locations"].append(
                    {
                        "block_id": b["id"],
                        "section_role": role,
                        "section_heading": b.get("section_heading", ""),
                        "snippet": b_text[:200],
                    }
                )
        for ent in shared_ents:
            # Only flag entities that appear in substantive summary/discussion claims
            if role in {"abstract", "highlights", "discussion", "conclusion"}:
                rec = deps_by_item.setdefault(
                    ent,
                    {"item": ent, "kind": "named_subgroup_or_entity", "downstream_locations": []},
                )
                if len(rec["downstream_locations"]) < 4:
                    rec["downstream_locations"].append(
                        {
                            "block_id": b["id"],
                            "section_role": role,
                            "section_heading": b.get("section_heading", ""),
                            "snippet": b_text[:200],
                        }
                    )

    # Prioritize numeric matches first, then named entities
    ordered = sorted(
        deps_by_item.values(),
        key=lambda r: (0 if r["kind"] == "numeric_value" else 1, -len(r["downstream_locations"]), r["item"]),
    )
    return ordered[:30]


def annotate_manuscript_blocks(
    blocks: list[dict[str, Any]],
    table_captions: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Annotate blocks in-place with section_heading, section_role, and table display_key in O(blocks)."""
    current_heading = "Front Matter"
    current_role = "front_matter"
    parent_chapter_role = "other"
    sections: list[dict[str, Any]] = []

    for b in blocks:
        if b["is_heading"]:
            current_heading = b["text"].lstrip("# ").strip()
            lvl = b.get("heading_level") or 1
            if lvl <= 1:
                current_role = classify_section_role(current_heading, "other")
                parent_chapter_role = current_role
            else:
                current_role = classify_section_role(current_heading, parent_chapter_role)
            sections.append(
                {
                    "id": b["id"],
                    "level": lvl,
                    "heading": current_heading,
                    "role": current_role,
                    "word_count": 0,
                }
            )
        else:
            b["section_heading"] = current_heading
            b["section_role"] = current_role
            if sections and b["kind"] != "table":
                sections[-1]["word_count"] += len(b["text"].split())

    pending_table_caption: tuple[str, str] | None = None
    claimed_table_keys: set[str] = set()

    for i, b in enumerate(blocks):
        if b["is_heading"]:
            pending_table_caption = None
            continue
        txt = b["text"]

        if b["kind"] == "table":
            if pending_table_caption is not None:
                t_label, cap_txt = pending_table_caption
                b["display_key"] = t_label
                b["caption"] = cap_txt
                claimed_table_keys.add(t_label)
                if table_captions is not None:
                    table_captions[b["id"]] = cap_txt
            else:
                b["display_key"] = f"Table ({b['id']})"
                b["caption"] = ""
            pending_table_caption = None
            continue

        cap_m = DISPLAY_CAPTION_START_RE.match(txt)
        if not cap_m:
            pending_table_caption = None
            continue
        parts = cap_m.group(1).split(None, 1)
        if len(parts) != 2:
            pending_table_caption = None
            continue

        dkey = _normalize_display_key(parts[0], parts[1])
        if dkey.startswith("Table "):
            prev_b = blocks[i - 1] if i > 0 else None
            next_b = blocks[i + 1] if i + 1 < len(blocks) else None
            belongs_to_next_table = False
            if (
                prev_b is not None
                and prev_b.get("kind") == "table"
                and prev_b.get("display_key") == f"Table ({prev_b['id']})"
                and next_b is not None
                and next_b.get("kind") == "table"
            ):
                after_next = blocks[i + 2] if i + 2 < len(blocks) else None
                after_cap_m = (
                    DISPLAY_CAPTION_START_RE.match(after_next["text"])
                    if (after_next is not None and not after_next["is_heading"] and after_next.get("kind") != "table")
                    else None
                )
                next_has_bottom_cap = bool(after_cap_m and after_cap_m.group(1).lower().startswith("tab"))
                prev_id_digits = str(prev_b.get("id", ""))[1:]
                next_id_digits = str(next_b.get("id", ""))[1:]
                if (
                    not next_has_bottom_cap
                    and prev_id_digits.isdigit()
                    and next_id_digits.isdigit()
                    and dkey == f"Table {int(next_id_digits)}"
                    and dkey != f"Table {int(prev_id_digits)}"
                ):
                    belongs_to_next_table = True

            if (
                prev_b is not None
                and prev_b.get("kind") == "table"
                and prev_b.get("display_key") == f"Table ({prev_b['id']})"
                and dkey not in claimed_table_keys
                and not belongs_to_next_table
            ):
                prev_b["display_key"] = dkey
                prev_b["caption"] = txt
                claimed_table_keys.add(dkey)
                if table_captions is not None:
                    table_captions[prev_b["id"]] = txt
                pending_table_caption = None
            elif dkey not in claimed_table_keys:
                pending_table_caption = (dkey, txt)
            else:
                pending_table_caption = None
        else:
            pending_table_caption = None

    return sections


def build_architecture_spine(
    blocks: list[dict[str, Any]],
    source_sha256: str,
    stats: dict[str, Any] | None = None,
    companion_paths: list[Path] | None = None,
    state_path: Path | None = None,
    paper_dir: Path | None = None,
) -> dict[str, Any]:
    stats = stats or {}
    title = "Untitled"
    for b in blocks[:4]:
        if b["kind"] != "table":
            title = b["text"].lstrip("# ").strip()
            break

    table_captions: dict[str, str] = {}
    sections = annotate_manuscript_blocks(blocks, table_captions=table_captions)

    abstract_texts: list[str] = []
    highlights_texts: list[str] = []
    rq_locks: list[str] = []
    gap_sentences: list[str] = []
    methods_subsection_leads: list[str] = []
    methods_locks: list[str] = []
    nonclaims_and_limits: list[str] = []
    acronyms: dict[str, str] = {}
    display_inventory: dict[str, str] = {}
    supplement_anchors: list[str] = []

    intro_paragraphs = [b for b in blocks if not b["is_heading"] and b["kind"] == "paragraph" and b.get("section_role") == "introduction"]
    seen_methods_subheadings: set[str] = set()

    for b in blocks:
        if b["is_heading"]:
            continue
        role = b.get("section_role", "other")
        txt = b["text"]

        if b["kind"] == "table":
            t_label = b.get("display_key") or f"Table ({b['id']})"
            cap_txt = table_captions.get(b["id"], "")
            cap_prefix = f"{cap_txt}\n" if cap_txt else ""
            rows_lines = txt.splitlines()
            preview = "\n".join(rows_lines[:12])
            if len(rows_lines) > 12:
                preview += f"\n... ({len(rows_lines) - 12} more rows; full table stored at block {b['id']})"
            display_inventory[t_label] = f"[{b['id']}] {cap_prefix}{preview}"
            continue

        cap_m = DISPLAY_CAPTION_START_RE.match(txt)
        if cap_m:
            parts = cap_m.group(1).split(None, 1)
            if len(parts) == 2:
                dkey = _normalize_display_key(parts[0], parts[1])
                existing_disp = display_inventory.get(dkey, "")
                if not re.match(r"^\[T\d+\]", existing_disp):
                    display_inventory[dkey] = f"[{b['id']}] {txt}"
                elif txt not in existing_disp:
                    m_tid = re.match(r"^(\[T\d+\])\s*(.*)$", existing_disp, flags=re.DOTALL)
                    if m_tid:
                        display_inventory[dkey] = f"{m_tid.group(1)} {txt}\n{m_tid.group(2)}"

        # Standalone equation lines like "... (1)"
        eq_end_m = re.search(r"\((\d{1,2}[a-z]?)\)\s*$", txt)
        if eq_end_m and len(txt) <= 140 and ("=" in txt or "≤" in txt or "≥" in txt):
            display_inventory[f"Equation ({eq_end_m.group(1)})"] = f"[{b['id']}|{b.get('section_heading','')}] {txt}"

        for m in ACRONYM_DEF_RE.finditer(txt):
            acronyms.setdefault(m.group(2), m.group(1).strip())

        if role == "abstract" and len(abstract_texts) < 4:
            abstract_texts.append(f"[{b['id']}] {txt}")
        elif role == "highlights":
            highlights_texts.append(f"[{b['id']}] {txt}")
        elif role == "introduction":
            sents = split_sentences(txt)
            is_closing_intro = bool(intro_paragraphs and b["id"] in {p["id"] for p in intro_paragraphs[-2:]})
            for s in sents:
                if RQ_RE.search(s):
                    rq_locks.append(f"[{b['id']}] {s}")
                elif GAP_RE.search(s) and len(gap_sentences) < 5:
                    gap_sentences.append(f"[{b['id']}] {s}")
                elif is_closing_intro and len(rq_locks) < 2 and len(s.split()) >= 10:
                    rq_locks.append(f"[{b['id']}] {s}")
                if NONCLAIM_RE.search(s) and len(nonclaims_and_limits) < 12:
                    nonclaims_and_limits.append(f"[{b['id']}|Intro] {s}")
        elif role == "methods":
            sents = split_sentences(txt)
            sub_h = b.get("section_heading", "Methods")
            if sents and sub_h not in seen_methods_subheadings:
                seen_methods_subheadings.add(sub_h)
                methods_subsection_leads.append(f"[{b['id']}|{sub_h}] {sents[0]}")
            for s in sents:
                if METHODS_STRUCTURAL_RE.search(s) and len(methods_locks) < 14:
                    methods_locks.append(f"[{b['id']}|{sub_h}] {s}")
                if NONCLAIM_RE.search(s) and len(nonclaims_and_limits) < 10:
                    nonclaims_and_limits.append(f"[{b['id']}|Methods] {s}")
        elif role in {"limitations", "discussion", "conclusion"}:
            for s in split_sentences(txt):
                if (NONCLAIM_RE.search(s) or role == "limitations") and len(nonclaims_and_limits) < 12:
                    nonclaims_and_limits.append(f"[{b['id']}|{b.get('section_heading','')}] {s}")
        elif role == "supplement":
            # Full block retention (no arbitrary 360-character mid-sentence cut)
            supplement_anchors.append(f"[{b['id']}|{b.get('section_heading','')}] {txt}")

    companion_slices, companion_hashes = _load_companion_displays(companion_paths or [])
    for dkey, slice_txt in companion_slices.items():
        if dkey in display_inventory:
            display_inventory[dkey] = display_inventory[dkey] + "\n" + slice_txt
        else:
            display_inventory[dkey] = slice_txt

    external_memory: dict[str, Any] = {"state_locks": [], "paper_claims": [], "paper_figures": []}
    if state_path is not None:
        if not state_path.is_file():
            raise FileNotFoundError(f"State file not found: {state_path}")
        st_obj = json.loads(state_path.read_text(encoding="utf-8"))
        if not isinstance(st_obj, dict):
            raise ValueError(f"State file must contain a JSON object: {state_path}")
        for lock in st_obj.get("semantic_locks", []):
            if isinstance(lock, dict) and lock.get("canonical"):
                external_memory["state_locks"].append(f"[{lock.get('id','LOCK')}:{lock.get('kind','lock')}] {lock['canonical']}")
        for term in st_obj.get("terminology", []):
            if isinstance(term, dict) and term.get("status") == "CONFIRMED" and term.get("preferred"):
                forb = ", ".join(term.get("forbidden", []))
                note = f" (forbid: {forb})" if forb else ""
                external_memory["state_locks"].append(f"[TERM:{term.get('id','term')}] {term['preferred']}{note}")

    if paper_dir is not None:
        if not paper_dir.is_dir():
            raise FileNotFoundError(f"Paper memory directory not found: {paper_dir}")
        for rec in _load_simple_yaml_records(paper_dir / "claims.yml")[:20]:
            cid = rec.get("id", "C?")
            stmt = rec.get("statement") or rec.get("claim") or rec.get("text") or ""
            status = rec.get("status", "")
            if stmt:
                external_memory["paper_claims"].append(f"[{cid}{':' + status if status else ''}] {stmt}")
        for rec in _load_simple_yaml_records(paper_dir / "figures.yml")[:20]:
            fid = rec.get("id", "F?")
            desc = rec.get("key_numbers") or rec.get("caption") or rec.get("summary") or ""
            if desc:
                external_memory["paper_figures"].append(f"[{fid}] {desc}")

    def dedup(items: list[str]) -> list[str]:
        seen: set[str] = set()
        out: list[str] = []
        for x in items:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    # Map explicit RQ/SQ/H labels across Results/Discussion sections
    rq_labels = sorted(set(re.findall(r"\b(?:RQ|SQ|H)\d+[a-z]?\b", " ".join(rq_locks), re.IGNORECASE)))
    results_text = " ".join(b["text"] for b in blocks if not b["is_heading"] and b.get("section_role") in {"results", "discussion"})
    unmapped_rqs = [lbl for lbl in rq_labels if not re.search(rf"\b{re.escape(lbl)}\b", results_text, re.IGNORECASE)]

    return {
        "schema": "manuscript_architecture_spine.v2",
        "source_sha256": source_sha256,
        "companion_sha256": companion_hashes,
        "title": title,
        "total_blocks": len(blocks),
        "total_words": sum(len(b["text"].split()) for b in blocks if not b["is_heading"] and b["kind"] != "table"),
        "extraction_stats": {
            "omath_count": stats.get("omath_count", 0),
            "table_count": stats.get("table_count", 0),
            "skipped_reference_blocks": stats.get("skipped_reference_blocks", 0),
        },
        "section_map": sections,
        "summary_claims_digest": {
            "abstract": abstract_texts,
            "highlights": highlights_texts,
        },
        "research_framing_contract": {
            "gap_and_motivation": dedup(gap_sentences),
            "locked_questions_and_goals": dedup(rq_locks),
            "unmapped_rq_labels_in_results": unmapped_rqs,
        },
        "methods_and_identification_locks": dedup(methods_subsection_leads + methods_locks),
        "display_inventory": display_inventory,
        "supplement_evidence_anchors": dedup(supplement_anchors),
        "inference_boundaries_and_nonclaims": dedup(nonclaims_and_limits),
        "defined_acronyms": acronyms,
        "external_memory": external_memory,
    }


def locate_target_blocks(blocks: list[dict[str, Any]], target_locator: str) -> list[int]:
    """Locate a section/subsection by heading substring or block ID range (e.g., P050..P055)."""
    loc = target_locator.strip()
    range_m = re.fullmatch(r"([PT]\d{2,5})(?:\s*\.\.\s*|\s*-\s*)([PT]\d{2,5})", loc, re.IGNORECASE)
    if range_m:
        start_id, end_id = range_m.group(1).upper(), range_m.group(2).upper()
        id_to_pos = {b["id"].upper(): i for i, b in enumerate(blocks)}
        if start_id not in id_to_pos or end_id not in id_to_pos:
            raise ValueError(f"Target block range {target_locator!r} not found in manuscript")
        start_pos, end_pos = id_to_pos[start_id], id_to_pos[end_id]
        if start_pos > end_pos:
            raise ValueError(f"Target block range {target_locator!r} has start after end")
        return list(range(start_pos, end_pos + 1))

    single_id_m = re.fullmatch(r"[PT]\d{2,5}", loc, re.IGNORECASE)
    if single_id_m:
        indices = [i for i, b in enumerate(blocks) if b["id"].upper() == loc.upper()]
        if indices:
            return indices
        raise ValueError(f"Target block ID {target_locator!r} not found in manuscript")

    target_indices: list[int] = []
    in_target = False
    target_level = 1
    for i, b in enumerate(blocks):
        if b["is_heading"]:
            lvl = b.get("heading_level") or 1
            if not in_target and loc.lower() in b["text"].lower():
                in_target = True
                target_level = lvl
                target_indices.append(i)
            elif in_target:
                if lvl <= target_level:
                    break
                target_indices.append(i)
        elif in_target:
            target_indices.append(i)

    if not target_indices:
        # Fallback: substring search in body paragraphs
        for i, b in enumerate(blocks):
            if loc.lower() in b["text"].lower():
                return [i]
        raise ValueError(f"Target locator {target_locator!r} not found in manuscript")
    return target_indices


def select_relevant_displays(
    blocks: list[dict[str, Any]],
    target_blocks: list[dict[str, Any]],
    spine: dict[str, Any],
) -> list[tuple[str, str]]:
    target_text = " ".join(b["text"] for b in target_blocks)
    cited_keys: list[str] = []
    for m in DISPLAY_REF_RE.finditer(target_text):
        key = _normalize_display_key(m.group(1), m.group(2))
        if key not in cited_keys:
            cited_keys.append(key)

    full_tables_by_key = {
        b.get("display_key"): f"[{b['id']}]\n{b['text']}"
        for b in blocks
        if b.get("kind") == "table" and b.get("display_key")
    }
    selected: list[tuple[str, str]] = []
    seen_selected: set[str] = set()
    inventory: dict[str, str] = spine.get("display_inventory", {})
    for key in cited_keys:
        if key in seen_selected:
            continue
        if key in full_tables_by_key:
            cap = inventory.get(key, "").splitlines()[0] if key in inventory else ""
            val = (cap + "\n" + full_tables_by_key[key]).strip()
            selected.append((key, val))
            seen_selected.add(key)
        elif key in inventory:
            selected.append((key, inventory[key]))
            seen_selected.add(key)
        else:
            base_key = re.sub(r"[A-Za-z]$", "", key)
            if base_key in seen_selected:
                continue
            if base_key in full_tables_by_key:
                cap = inventory.get(base_key, "").splitlines()[0] if base_key in inventory else ""
                selected.append((base_key, (cap + "\n" + full_tables_by_key[base_key]).strip()))
                seen_selected.add(base_key)
            elif base_key in inventory:
                selected.append((base_key, inventory[base_key]))
                seen_selected.add(base_key)
            elif base_key.startswith("Table ") and base_key.split()[-1].isdigit():
                fallback_tid = f"Table (T{int(base_key.split()[-1]):02d})"
                if fallback_tid in full_tables_by_key and fallback_tid not in seen_selected:
                    selected.append((base_key, full_tables_by_key[fallback_tid]))
                    seen_selected.add(base_key)
                    seen_selected.add(fallback_tid)

    cited_nums = {
        re.sub(r"[A-Za-z]$", "", ref_k.split()[-1]).upper()
        for ref_k in cited_keys
        if ref_k.split()
    }
    for k, v in inventory.items():
        if k in dict(selected):
            continue
        if k.startswith("[Companion") or ":" in k:
            tokens_in_k = {t.upper() for t in re.findall(r"S?\d+", k, re.IGNORECASE)}
            if cited_nums & tokens_in_k:
                selected.append((k, v))

    # Ensure any table directly embedded inside target_blocks is included once in Section 5
    selected_keys = {k for k, _ in selected}
    for tb in target_blocks:
        if tb.get("kind") == "table":
            tkey = tb.get("display_key") or f"Table ({tb['id']})"
            if tkey not in selected_keys and f"[{tb['id']}]" not in " ".join(v for _, v in selected):
                tb_cap = str(tb.get("caption") or "").strip()
                if not tb_cap and tkey in inventory:
                    inv_first = re.sub(rf"^\[{re.escape(tb['id'])}\]\s*", "", inventory[tkey].splitlines()[0]).strip()
                    if DISPLAY_CAPTION_START_RE.match(inv_first):
                        tb_cap = inv_first
                val = f"[{tb['id']}] {tb_cap}\n[{tb['id']}]\n{tb['text']}" if tb_cap else f"[{tb['id']}]\n{tb['text']}"
                selected.append((tkey, val))
                selected_keys.add(tkey)
    return selected


def _boundary_excerpt(block: dict[str, Any], keep_end: bool, compact: bool) -> str:
    txt = block["text"]
    if not compact or block["is_heading"]:
        return txt
    sents = split_sentences(txt)
    if len(sents) <= 2:
        return txt
    return ("... " + " ".join(sents[-2:])) if keep_end else (" ".join(sents[:2]) + " ...")


def build_scoped_context_envelope(
    blocks: list[dict[str, Any]],
    spine: dict[str, Any],
    target_locator: str,
    task_instruction: str = "Revise or check ONLY the authorized target unit in alignment with the spine and evidence-salience contract.",
    mode: str = "revise",
    max_tokens: int = 4500,
) -> tuple[str, dict[str, Any]]:
    """Build a bounded <= max_tokens context envelope for Agent A -> Agent B handoff."""
    if max_tokens <= 0:
        raise ValueError("max_tokens must be > 0")
    target_indices = locate_target_blocks(blocks, target_locator)
    first_idx, last_idx = target_indices[0], target_indices[-1]
    prev_neighbors = [blocks[j] for j in range(max(0, first_idx - 2), first_idx) if blocks[j]["kind"] != "table"]
    next_neighbors = [blocks[j] for j in range(last_idx + 1, min(len(blocks), last_idx + 3)) if blocks[j]["kind"] != "table"]
    target_blocks = [blocks[j] for j in target_indices]

    downstream_deps = compute_downstream_dependencies(blocks, target_indices)
    relevant_displays = select_relevant_displays(blocks, target_blocks, spine)

    target_text = " ".join(b["text"] for b in target_blocks)
    cited_supp_ids = {
        m.group(2).upper()
        for m in DISPLAY_REF_RE.finditer(target_text)
        if m.group(2).upper().startswith("S")
    }
    supp_all: list[str] = list(spine.get("supplement_evidence_anchors", []))
    supp_cited = [s for s in supp_all if any(re.search(rf"\b{re.escape(cid)}\b", s.upper()) for cid in cited_supp_ids)]
    supp_other = [s for s in supp_all if s not in supp_cited]

    target_words = {w.lower() for w in re.findall(r"[A-Za-z]{4,}", target_text)}
    raw_methods = list(spine.get("methods_and_identification_locks", []))
    methods_locks = sorted(
        raw_methods,
        key=lambda item: -len(target_words & {w.lower() for w in re.findall(r"[A-Za-z]{4,}", item)}),
    )
    nonclaims = list(spine.get("inference_boundaries_and_nonclaims", []))
    acronyms = dict(spine.get("defined_acronyms", {}))

    has_target_prose = any(not b["is_heading"] and b.get("kind") != "table" for b in target_blocks)

    def render(
        m_limit: int,
        nc_limit: int,
        supp_other_limit: int,
        acr_limit: int,
        sec_map_limit: int,
        compact_neighbors: bool,
        dep_limit: int,
        compact_abstract: bool,
        compact_contract: bool,
        ultra_compact: bool = False,
        display_row_cap: int | None = None,
        supp_char_cap: int | None = None,
        display_char_cap: int | None = None,
    ) -> str:
        lines: list[str] = [
            "=== SCOPED MANUSCRIPT CONTEXT ENVELOPE (manuscript_architecture_spine.v2) ===",
            f"Source SHA-256: {spine['source_sha256']} | Mode: {mode}",
            f"Title: {spine['title']}",
            "",
            "1. GLOBAL SECTION ARCHITECTURE (READ-ONLY):",
        ]
        for s in spine["section_map"][:sec_map_limit]:
            indent = "  " * max(1, int(s.get("level", 1)))
            lines.append(f"{indent}- [{s['id']}] {s['heading']} ({s['role']}, {s['word_count']}w)")

        lines.append("\n2. LOCKED RESEARCH FRAMING & EXACT QUESTIONS:")
        gap_cap = 1 if ultra_compact else 3
        rq_list = spine["research_framing_contract"]["locked_questions_and_goals"]
        rq_use = rq_list[:3] if ultra_compact else rq_list
        for item in spine["research_framing_contract"]["gap_and_motivation"][:gap_cap]:
            lines.append(f"  - Gap: {item}")
        for item in rq_use:
            lines.append(f"  - Locked RQ/Goal: {item}")

        lines.append("\n3. UPSTREAM METHODS, FORMULAS, SIGN & UNCERTAINTY LOCKS (ANTI-ECHO: DO NOT COPY INTO RESULTS):")
        for item in methods_locks[:m_limit]:
            lines.append(f"  - {item}")

        ext = spine.get("external_memory", {})
        if ext.get("state_locks") or ext.get("paper_claims") or ext.get("paper_figures"):
            lines.append("\n4. PROJECT STATE & .PAPER MEMORY LOCKS (READ-ONLY):")
            ext_cap = 4 if ultra_compact else 10
            for item in (ext.get("state_locks", []) + ext.get("paper_claims", []) + ext.get("paper_figures", []))[:ext_cap]:
                lines.append(f"  - {item}")

        if relevant_displays or supp_cited or supp_other[:supp_other_limit]:
            lines.append("\n5. VERIFIED DISPLAY & SUPPLEMENTARY EVIDENCE SLICE:")
            for dkey, dval in relevant_displays:
                rendered_dval = dval
                if display_row_cap is not None:
                    d_lines = dval.splitlines()
                    if len(d_lines) > display_row_cap:
                        omitted_n = len(d_lines) - display_row_cap
                        rendered_dval = (
                            "\n".join(d_lines[:display_row_cap])
                            + f"\n... ({omitted_n} more rows omitted for packet budget; full slice retained in spine metadata)"
                        )
                if display_char_cap is not None and len(rendered_dval) > display_char_cap:
                    rendered_dval = (
                        rendered_dval[:display_char_cap]
                        + "\n... (display slice truncated for packet budget; full slice retained in spine metadata)"
                    )
                lines.append(f"  - {dkey}: {rendered_dval}")
            supp_use = supp_cited + supp_other[:supp_other_limit]
            if display_row_cap is not None:
                supp_use = supp_cited[: max(1, min(len(supp_cited), display_row_cap // 3 or 1))]
            for item in supp_use:
                rendered_supp = (
                    (item[:supp_char_cap] + " ...")
                    if (supp_char_cap is not None and len(item) > supp_char_cap)
                    else item
                )
                lines.append(f"  - Supplement: {rendered_supp}")

        lines.append("\n6. INFERENCE BOUNDARIES, LIMITATIONS & TERMINOLOGY:")
        for item in nonclaims[:nc_limit]:
            lines.append(f"  - {item}")
        if acronyms and acr_limit > 0:
            acr_items = sorted(acronyms.items())[:acr_limit]
            lines.append("  - Acronyms: " + "; ".join(f"{k}={v}" for k, v in acr_items))

        lines.append("\n7. ABSTRACT, HIGHLIGHTS & DOWNSTREAM DEPENDENCY LOCKS (SYNC ANCHORS — DO NOT EDIT):")
        hl_list = spine["summary_claims_digest"]["highlights"]
        for item in (hl_list[:2] if ultra_compact else hl_list):
            lines.append(f"  - Highlight/KeyPoint: {item}")
        if not compact_abstract:
            for item in spine["summary_claims_digest"]["abstract"]:
                lines.append(f"  - Abstract: {item}")
        elif spine["summary_claims_digest"]["abstract"]:
            ab_sents = split_sentences(spine["summary_claims_digest"]["abstract"][0])
            lines.append("  - Abstract (core): " + " ".join(ab_sents[: (2 if ultra_compact else 3)]))
        if downstream_deps and dep_limit > 0:
            lines.append("  - Downstream Dependencies (pruning any item below is CLASS B; flag in `cross_section_sync_alerts`):")
            for dep in downstream_deps[:dep_limit]:
                locs = ", ".join(f"{loc['block_id']}({loc['section_role']})" for loc in dep["downstream_locations"])
                lines.append(f"    * {dep['kind']} `{dep['item']}` -> {locs}")

        lines.append("\n8. IMMEDIATE NEIGHBORING CONTEXT (READ-ONLY BOUNDARY):")
        prev_use = ([] if ultra_compact else prev_neighbors[-1:]) if compact_neighbors else prev_neighbors
        next_use = ([] if ultra_compact else next_neighbors[:1]) if compact_neighbors else next_neighbors
        for b in prev_use:
            lines.append(f"  [PRECEDING {b['id']}] {_boundary_excerpt(b, keep_end=True, compact=compact_neighbors)}")
        for b in next_use:
            lines.append(f"  [FOLLOWING {b['id']}] {_boundary_excerpt(b, keep_end=False, compact=compact_neighbors)}")

        lines.append("\n9. AUTHORIZED TARGET UNIT (ONLY REVISE / AUDIT THIS UNIT):")
        for b in target_blocks:
            if has_target_prose and b.get("kind") == "table":
                t_ref = b.get("display_key") or b["id"]
                lines.append(
                    f"  [{b['id']}] (Embedded {t_ref} — authoritative table rows provided in Section 5 above; keep table cells in display and revise prose only)"
                )
            else:
                lines.append(f"  [{b['id']}] {b['text']}")

        if compact_contract:
            lines.append(
                "\n10. SCOPED CONTRACT: Edit ONLY Sec 9 using Secs 1-8. Never copy Methods recipes into Results; never guess sign order or leak questions into prose (`unverified_context_locks`). "
                "Apply Two-Stage Salience (plain relational prose by default; report exact numbers/CIs only for magnitude calibration, verdict-shifting CIs, or subgroup exceptions; log omissions in `declared_omitted_to_display` and Sec 7 hits in `cross_section_sync_alerts`)."
            )
        else:
            lines.append(
                "\n10. SCOPED EXECUTION, TWO-STAGE EVIDENCE SALIENCE & ANTI-BIAS CONTRACT:\n"
                "  - Edit Scope != Context Anchor Scope: keep edits strictly inside Section 9 while honoring locks in Sections 1-8.\n"
                "  - Anti-Methods-Echo Rule: use Section 3 only to calibrate sign direction, denominators, and bundled-condition caveats; NEVER copy multi-sentence Methods formulas or bootstrap procedures into Results openings.\n"
                "  - Missing-Context Fail-Safe: never guess subtraction order, never invent mechanisms/thresholds, never confuse bootstrap resamples with generative/simulation runs, and NEVER place editorial verification questions inside `revised_target_prose` (isolate them in `unverified_context_locks`).\n"
                "  - Two-Stage Evidence Salience (`plan`/`draft`/substantive `revise`; `proofread` preserves all verified numbers): "
                "(A) foreground primary RQ contrasts, capability limits/nulls, cross-level dissociations, and subgroup reversals; leave conforming subscales to displays/SM; "
                "(B) default to plain relational prose and quote exact numbers/CIs ONLY when calibrating headline magnitude, shifting interval verdicts (e.g., CIs crossing zero), or anchoring subgroup exceptions. "
                "Record omitted draft numbers in `declared_omitted_to_display` and Section 7 hits in `cross_section_sync_alerts`."
            )
        lines.append("\n11. TASK INSTRUCTION:\n" + task_instruction.strip())
        return "\n".join(lines) + "\n"

    trim_schedule = [
        (16, 10, 3, 22, 36, False, 14, False, False, False),
        (12, 7, 1, 12, 28, True, 10, False, False, False),
        (8, 5, 0, 6, 24, True, 8, True, False, False),
        (5, 3, 0, 3, 18, True, 6, True, True, False),
        (3, 2, 0, 0, 12, True, 4, True, True, False),
        (1, 1, 0, 0, 6, True, 2, True, True, True),
    ]
    envelope_text = ""
    for params in trim_schedule:
        envelope_text = render(*params)
        if estimate_tokens(envelope_text) <= max_tokens:
            break
    if estimate_tokens(envelope_text) > max_tokens:
        for row_cap, char_cap in ((25, 4500), (15, 2700), (10, 1800), (6, 1080), (3, 540), (2, 260)):
            envelope_text = render(
                1, 1, 0, 0, 6, True, 2, True, True, True,
                display_row_cap=row_cap,
                supp_char_cap=row_cap * 120,
                display_char_cap=char_cap,
            )
            if estimate_tokens(envelope_text) <= max_tokens:
                break

    meta = {
        "source_sha256": spine["source_sha256"],
        "target_locator": target_locator,
        "target_block_ids": [b["id"] for b in target_blocks],
        "envelope_utf8_bytes": len(envelope_text.encode("utf-8")),
        "est_tokens": estimate_tokens(envelope_text),
        "max_tokens": max_tokens,
        "within_budget": estimate_tokens(envelope_text) <= max_tokens,
        "downstream_dependencies": downstream_deps,
        "relevant_displays": [k for k, _ in relevant_displays],
        "relevant_display_slices": dict(relevant_displays),
    }
    return envelope_text, meta


def _compute_inputs_sha256(
    manuscript_digest: str,
    companion_paths: list[Path] | None,
    state_path: Path | None,
    paper_dir: Path | None,
) -> str:
    hasher = sha256()
    hasher.update(f"manuscript:{manuscript_digest}\n".encode("utf-8"))
    for cpath in sorted((companion_paths or []), key=lambda p: str(p)):
        if cpath.is_file():
            c_sha = load_manuscript_blocks(cpath)[1] if cpath.suffix.lower() == ".tex" else sha256(cpath.read_bytes()).hexdigest()
            hasher.update(f"companion:{cpath.name}:{c_sha}\n".encode("utf-8"))
    if state_path and state_path.is_file():
        hasher.update(f"state:{sha256(state_path.read_bytes()).hexdigest()}\n".encode("utf-8"))
    if paper_dir and paper_dir.is_dir():
        for fname in ("claims.yml", "figures.yml"):
            fpath = paper_dir / fname
            if fpath.is_file():
                hasher.update(f"paper:{fname}:{sha256(fpath.read_bytes()).hexdigest()}\n".encode("utf-8"))
    return hasher.hexdigest()


def load_or_build_spine(
    manuscript_path: Path,
    companion_paths: list[Path] | None = None,
    state_path: Path | None = None,
    paper_dir: Path | None = None,
    cache_file: Path | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if companion_paths:
        for cpath in companion_paths:
            if not cpath.is_file():
                raise FileNotFoundError(f"Companion file not found: {cpath}")
    if state_path is not None:
        if not state_path.is_file():
            raise FileNotFoundError(f"State file not found: {state_path}")
        st_check = json.loads(state_path.read_text(encoding="utf-8"))
        if not isinstance(st_check, dict):
            raise ValueError(f"State file must contain a JSON object: {state_path}")
    if paper_dir is not None:
        if not paper_dir.is_dir():
            raise FileNotFoundError(f"Paper memory directory not found: {paper_dir}")
        eff_paper_dir: Path | None = paper_dir
    else:
        auto_paper = manuscript_path.parent / ".paper"
        eff_paper_dir = auto_paper if auto_paper.is_dir() else None

    blocks, digest, stats = load_manuscript_blocks(manuscript_path)
    inputs_digest = _compute_inputs_sha256(digest, companion_paths, state_path, eff_paper_dir)
    if cache_file and cache_file.is_file():
        try:
            cached = json.loads(cache_file.read_text(encoding="utf-8"))
            if (
                isinstance(cached, dict)
                and cached.get("source_sha256") == digest
                and cached.get("inputs_sha256") == inputs_digest
                and cached.get("schema") == "manuscript_architecture_spine.v2"
            ):
                annotate_manuscript_blocks(blocks)
                return blocks, cached
        except (OSError, json.JSONDecodeError):
            pass

    spine = build_architecture_spine(
        blocks,
        digest,
        stats=stats,
        companion_paths=companion_paths,
        state_path=state_path,
        paper_dir=eff_paper_dir,
    )
    spine["inputs_sha256"] = inputs_digest
    if cache_file:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(spine, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return blocks, spine


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path, help="Path to .docx, .tex, or .md manuscript")
    parser.add_argument("--target", default=None, help="Target section heading substring or block ID/range (e.g., '4.2' or 'P050..P055')")
    parser.add_argument("--task", default="Revise or check ONLY the authorized target unit in alignment with the spine and evidence-salience contract.")
    parser.add_argument("--mode", choices=("plan", "draft", "revise", "proofread", "review"), default="revise")
    parser.add_argument("--companion", type=Path, nargs="*", default=[], help="Optional companion CSV/TSV/SM/Highlights files")
    parser.add_argument("--state", type=Path, default=None, help="Optional manuscript_state.json")
    parser.add_argument("--paper-dir", type=Path, default=None, help="Optional .paper/ directory (read-only)")
    parser.add_argument("--cache-file", type=Path, default=None, help="Optional spine cache JSON path")
    parser.add_argument("--max-tokens", type=int, default=4500, help="Hard token ceiling (default: 4500)")
    parser.add_argument("--output", type=Path, default=None, help="Write envelope text or spine JSON to file")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON output")
    args = parser.parse_args(argv)

    try:
        if isinstance(args.max_tokens, bool) or args.max_tokens <= 0:
            raise ValueError("max_tokens must be > 0")
        blocks, spine = load_or_build_spine(
            args.manuscript,
            companion_paths=args.companion,
            state_path=args.state,
            paper_dir=args.paper_dir,
            cache_file=args.cache_file,
        )
        if args.target is None:
            core_spine = {k: v for k, v in spine.items() if k != "display_inventory"}
            core_bytes = len(json.dumps(core_spine, ensure_ascii=False).encode("utf-8"))
            full_bytes = len(json.dumps(spine, ensure_ascii=False).encode("utf-8"))
            summary = {
                "status": "PASS",
                "file": args.manuscript.name,
                "sha256": spine["source_sha256"],
                "title": spine["title"],
                "total_blocks": spine["total_blocks"],
                "total_words": spine["total_words"],
                "omath_count": spine["extraction_stats"]["omath_count"],
                "table_count": spine["extraction_stats"]["table_count"],
                "skipped_reference_blocks": spine["extraction_stats"]["skipped_reference_blocks"],
                "sections_found": len(spine["section_map"]),
                "rq_locks_found": len(spine["research_framing_contract"]["locked_questions_and_goals"]),
                "methods_locks_found": len(spine["methods_and_identification_locks"]),
                "displays_indexed": len(spine["display_inventory"]),
                "nonclaims_found": len(spine["inference_boundaries_and_nonclaims"]),
                "core_spine_utf8_bytes": core_bytes,
                "est_core_spine_tokens": math.ceil(core_bytes / 3.0),
                "full_spine_with_displays_bytes": full_bytes,
            }
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(json.dumps(spine, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            payload = {"summary": summary, "spine": spine} if args.as_json else summary
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0

        envelope_text, meta = build_scoped_context_envelope(
            blocks,
            spine,
            target_locator=args.target,
            task_instruction=args.task,
            mode=args.mode,
            max_tokens=args.max_tokens,
        )
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(envelope_text, encoding="utf-8")
        if args.as_json:
            status_str = "PASS" if meta["within_budget"] else "PACKET_BUDGET_EXCEEDED"
            print(json.dumps({"status": status_str, "meta": meta, "envelope": envelope_text}, ensure_ascii=False, indent=2))
        else:
            print(envelope_text, end="")
        return 0 if meta["within_budget"] else 1
    except (OSError, ValueError, BadZipFile, ET.ParseError, KeyError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
