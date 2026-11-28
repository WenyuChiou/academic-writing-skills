#!/usr/bin/env python3
"""Verify numeric provenance, sign polarity, partitioned conservation, and downstream sync for Agent A -> Agent B passes.

Supports two verification contracts:
  1. strict_preservation: exact multiset conservation of numbers/signs (allowing explicit
     negative-sign <-> negative-polarity-verb equivalence) for proofread / Class D passes.
  2. curated_salience: entity + sign provenance check, Mode R partitioned conservation
     (every number in `before` must be either retained in `after` or declared in
     `declared_omitted_to_display`), downstream Class B orphan detection against
     `downstream_empirical_dependencies`, and meta-commentary leakage detection.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import re
import sys
from typing import Any
from xml.etree import ElementTree as ET
from zipfile import BadZipFile

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_context_envelope import annotate_manuscript_blocks, load_manuscript_blocks  # noqa: E402

STRUCTURAL_LOCATOR_RE = re.compile(
    r"\b(?:Figures?|Figs?\.|Tables?|Sections?|Secs?\.|Subsections?|Chapters?|Equations?|Eqs?\.|Panels?|Appendix)"
    r"\s*(?:\(S?\d+(?:\.\d+)*[A-Za-z]?\)|S?\d+(?:\.\d+)*[A-Za-z]?)"
    r"|\b(?:RQ|SQ|H|Hypothesis|Proposition|Study|Wave|Step|Pass|Stage|Tier|Model)\s*\d+[A-Za-z]?\b"
    r"|\b(?:90|95|99)%\s*(?:CIs?|CrIs?|confidence\s+intervals?|credible\s+intervals?)\b"
    r"|\[\s*(?:[PT]\d{2,5}|Note\s+\d+)\s*\]"
    r"|\[\s*\d+(?:\s*(?:,|–|-)\s*\d+)*\s*\]",
    re.IGNORECASE,
)

YEAR_SPAN_RE = re.compile(r"\b(?:19|20)\d{2}(?:\s*[–-]\s*(?:19|20)\d{2})?\b")
SCALE_RANGE_RE = re.compile(r"\b[01]\s*[–-]\s*[4579](?=-point|\s+scale)\b", re.IGNORECASE)
MODEL_SIZE_TOKEN_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9.]*(?:-[A-Za-z0-9.]+)*-\d+(?:\.\d+)?[BMKbmk]\b")
UNARY_ENDASH_RE = re.compile(r"(?:^|(?<=[\s(\[{<:=,;|/]))\u2013(?=\$?(?:\d|\.\d))")
BLOCK_PREFIX_RE = re.compile(
    r"^(?:\[(?:[PT]\d{2,5}(?:\|[^\]]*)?|[^\]]*\b[PT]\d{2,5}|Companion\s+[^\]]+|Note\s+\d+)\]\s*)+",
    re.IGNORECASE,
)
LINE_BLOCK_PREFIX_RE = re.compile(
    r"^(?:[-*+]\s+)?(?:(?:Gap|Locked\s+RQ/Goal|Supplement|Abstract(?:\s*\(core\))?|Highlight/KeyPoint"
    r"|(?:Figure|Fig\.|Table|Equation)\s*\(?S?\d+[A-Za-z]?\)?)\s*:\s+)?"
    r"(?:\[(?:[PT]\d{2,5}(?:\|[^\]]*)?|[^\]]*\b[PT]\d{2,5}|Companion\s+[^\]]+|Note\s+\d+|LOCK:[^\]]+|TERM:[^\]]+|[CF][^:\]]*(?::[^\]]*)?)\]\s*)+",
    re.IGNORECASE,
)

NUMERIC_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9.%)\]])"
    r"([+−-]?)"
    r"("
    r"\$(?:\d[\d,]*(?:\.\d+)?|\.\d+)[KMBkmb]?"
    r"|(?:\d[\d,]*(?:\.\d+)?|\.\d+)(?:[eE][+−-]?\d+)?%?"
    r")"
    r"(?![A-Za-z0-9]|\.\d)"
)

ABBREV_PROTECT_RE = re.compile(
    r"\b(?:et\s+al|e\.g|i\.e|Fig|Figs|Eq|Eqs|Sec|Secs|Tab|Dr|Prof|Mr|Ms|vs|cf|ca|approx|No|pp|p)\.",
    re.IGNORECASE,
)

_CLAUSE_VERB_ALT = (
    r"had|has|have|was|were|is|are|showed|shows|rose|fell|increased|decreased|dropped|declined"
    r"|remained|reached|achieved|yielded|shifted|changed|improved|worsened|trailed|exceeded"
    r"|averaged|stood|equaled|totaled|held|persisted|stabilized"
)

CLAUSE_FINITE_VERB_RE = re.compile(rf"\b(?:{_CLAUSE_VERB_ALT})\b", re.IGNORECASE)

CONTRAST_CONJ_RE = re.compile(
    r"(?:(?:,\s*|\s+)(?:whereas|while|but|yet|although|though)\b"
    r"|,\s*and\s+(?=[A-Z])"
    rf"|,\s+(?=(?:(?:the|a|an|its|their)\s+)?(?!(?:which|that|who|whom|whose|where|when|and|or|but|yet|while|whereas|although|though)\b)[A-Za-z][A-Za-z0-9_-]*(?:\s+[A-Za-z0-9_-]+){{0,2}}\s+(?:{_CLAUSE_VERB_ALT})\b)"
    rf"|\s+and\s+(?=(?:(?:the|a|an|its|their)\s+)?[A-Za-z][A-Za-z0-9_-]*(?:\s+[A-Za-z0-9_-]+){{0,2}}\s+(?:{_CLAUSE_VERB_ALT})\b)"
    r"|;\s*|\s+[—–]\s+)",
    re.IGNORECASE,
)

FRONTED_CONTRAST_RE = re.compile(
    r"^\s*(?:whereas|while|although|though|unlike|despite|in\s+spite\s+of|compared\s+(?:with|to)|relative\s+to|in\s+contrast\s+to)\b",
    re.IGNORECASE,
)

NEGATIVE_POLARITY_CUES = re.compile(
    r"\b(?:decreas(?:e|ed|es|ing)|drop(?:ped|s|ping)?|declin(?:e|ed|es|ing)"
    r"|reduc(?:e|ed|es|ing|tion|tions)|lower(?:ed|ing|s)?|fell|fall(?:s|ing)?"
    r"|loss(?:es)?|deficit(?:s)?|shrink(?:s|ing)?|shrank|trail(?:ed|s|ing)?"
    r"|worse|worsen(?:ed|s|ing)?|below|minus|(?<!non-)negative|subtract(?:ed|ing)?)\b",
    re.IGNORECASE,
)

POSITIVE_POLARITY_CUES = re.compile(
    r"\b(?:increas(?:e|ed|es|ing)|gain(?:ed|s|ing)?|ris(?:e|es|ing)|rose"
    r"|improv(?:e|ed|es|ing|ement)|higher|exceed(?:ed|s|ing)?|above|plus|(?<!non-)positive)\b",
    re.IGNORECASE,
)

DOUBLE_NEGATED_CUE_RE = re.compile(
    r"(?:\b(?:not|never|cannot)|n['\u2019]t)\s+(?:(?!(?:and|but|or|while|whereas|yet)\b)[A-Za-z-]+\s+){0,2}"
    r"(?:without\s+|non-|non\s+|fail(?:ed|s|ing)?\s+to\s+|unable\s+to\s+)"
    r"(?:(?!(?:and|but|or|while|whereas|yet)\b)[A-Za-z0-9$.%+−-]+\s+){0,4}$",
    re.IGNORECASE,
)

NEGATED_CUE_PREFIX_RE = re.compile(
    r"(?:(?:\b(?:not|no|never|neither|nor|without|cannot|non)|n['\u2019]t)\s+"
    r"(?:(?!(?:and|but|or|while|whereas|yet)\b)[A-Za-z0-9$.%+−-]+\s+){0,4}"
    r"|\bnon-"
    r"|\b(?:fail(?:ed|s|ing)?\s+to|unable\s+to|rather\s+than|instead\s+of)\s+"
    r"(?:(?!(?:and|but|or|while|whereas|yet)\b)[A-Za-z0-9$.%+−-]+\s+){0,3})$",
    re.IGNORECASE,
)

MAGNITUDE_QUALIFIER_RE = re.compile(r"\b(?:absolute|magnitude|width)\b", re.IGNORECASE)

SUBTRACTION_FLIP_CUES = re.compile(
    r"\b(?:Base\s*[-–−]\s*Memory|MAE_Base\s*-\s*MAE_Memory|smaller\s+(?:change\s+)?(?:MAE|RMSE|error)"
    r"|error\s+reduction|positive\s+(?:values?\s+)?(?:denote|indicate|represent)s?\s+(?:smaller|lower|reduced))\b",
    re.IGNORECASE,
)

META_LEAKAGE_RE = re.compile(
    r"\b(?:not\s+specified\s+in\s+this\s+(?:subsection|excerpt|passage)"
    r"|cannot\s+(?:be\s+)?verif(?:y|ied)\s+from\s+(?:this|the\s+supplied)\s+(?:excerpt|subsection|passage)"
    r"|please\s+(?:verify|confirm|clarify)\s+whether"
    r"|author\s+should\s+(?:verify|check|confirm)"
    r"|\[TODO\b|\[VERIFY\b|\[CHECK\b)\b",
    re.IGNORECASE,
)

GENERATIVE_CONFUSION_RE = re.compile(
    r"\b(\d[\d,]*)\s+(?:generative\s+runs?|LLM\s+runs?|model\s+runs?|climate\s+simulations?|hydrological\s+(?:climate\s+)?simulations?)\b",
    re.IGNORECASE,
)


def _has_unnegated_cue(pattern: re.Pattern[str], clause: str) -> bool:
    for m in pattern.finditer(clause):
        prefix = re.sub(r"\s+", " ", clause[max(0, m.start() - 80):m.start()])
        if DOUBLE_NEGATED_CUE_RE.search(prefix):
            return True
        if NEGATED_CUE_PREFIX_RE.search(prefix):
            continue
        return True
    return False


def _is_valid_magnitude_qualification(clause: str) -> bool:
    if not MAGNITUDE_QUALIFIER_RE.search(clause):
        return False
    has_any_dir_word = bool(NEGATIVE_POLARITY_CUES.search(clause) or POSITIVE_POLARITY_CUES.search(clause))
    has_unneg_dir = _has_unnegated_cue(NEGATIVE_POLARITY_CUES, clause) or _has_unnegated_cue(POSITIVE_POLARITY_CUES, clause)
    if has_any_dir_word and not has_unneg_dir:
        return False
    return True


def _strip_non_data_tokens(text: str) -> str:
    normalized = text.replace("\u2212", "-")
    normalized = MODEL_SIZE_TOKEN_RE.sub(lambda m: " " * len(m.group(0)), normalized)
    normalized = STRUCTURAL_LOCATOR_RE.sub(lambda m: " " * len(m.group(0)), normalized)
    normalized = SCALE_RANGE_RE.sub(lambda m: " " * len(m.group(0)), normalized)
    normalized = YEAR_SPAN_RE.sub(lambda m: " " * len(m.group(0)), normalized)
    normalized = UNARY_ENDASH_RE.sub("-", normalized)
    return normalized


def _canonical_magnitude(raw_mag: str) -> str:
    cleaned = raw_mag.replace(",", "").replace("\u2212", "-").strip()
    prefix = ""
    if cleaned.startswith("$"):
        prefix = "$"
        cleaned = cleaned[1:]
    if cleaned.startswith("."):
        cleaned = "0" + cleaned
    sci_m = re.fullmatch(r"(\d+(?:\.\d+)?)[eE]([+-]?)0*(\d+)(%?)", cleaned)
    if sci_m:
        mant, exp_sgn, exp_num, pct = sci_m.groups()
        exp_prefix = "-" if exp_sgn == "-" else ""
        cleaned = f"{mant}e{exp_prefix}{exp_num or '0'}{pct}"
    if prefix:
        return "$" + cleaned.upper()
    return cleaned


COMPARATOR_PREP_RE = re.compile(
    r"(?:\b(?:from|than|relative\s+to|compared\s+(?:with|to)|versus|despite|in\s+spite\s+of|against)\b"
    r"|\bvs\.(?=\s|$|[(\[{+\-−$\d.,;)])|\bvs\b)",
    re.IGNORECASE,
)

RIGHT_POLARITY_BOUNDARY_RE = re.compile(
    r"(?:\b(?:from|than|relative\s+to|compared\s+(?:with|to)|versus|despite|in\s+spite\s+of|against|across|among|under|within|while|whereas|although|though|after|before|with)\b"
    r"|\bvs\.(?=\s|$|[(\[{+\-−$\d.,;)])|\bvs\b)",
    re.IGNORECASE,
)

PRIOR_NUM_PREP_BOUNDARY_RE = re.compile(
    r"\$?(?:\d[\d,]*(?:\.\d+)?|\.\d+)[KMBkmb]?%?(?:\s+[A-Za-z-]+){0,5}[\s),]*"
    r"(?:\b(?:from|than|relative\s+to|compared\s+(?:with|to)|versus|despite|in\s+spite\s+of|against|across|among|under|within|with)\b"
    r"|\bvs\.(?=\s|$|[(\[{+\-−$\d.,;)])|\bvs\b)",
    re.IGNORECASE,
)

POST_COMMA_FINITE_VERB_RE = re.compile(
    r"\b(?:was|were|is|are|had|has|have|averaged|remained|stood|equaled|totaled|reached|changed|shifted|held|persisted|stabilized)\b",
    re.IGNORECASE,
)

PAREN_ISOLATION_MARKER_RE = re.compile(
    r"(?i:\b(?:baseline|benchmark|control|reference|versus|compared\s+(?:with|to)|relative\s+to|from|SD|SE|IQR)\b"
    r"|\bvs\.(?=\s|$|[(\[{+\-−$\d.,;)])|\bvs\b)"
    r"|\b(?:[Ff]or|[Ii]n)\s+[A-Z][A-Za-z0-9_-]{2,}"
    r"|(?:^|[,;]\s*)(?!(?:CI|CIs|CrI|CrIs)\b)[A-Z][A-Za-z0-9_-]{2,}\s*[:=]"
)

PAREN_SUBJ_VERB_RE = re.compile(
    rf"\b(?:(?:[Tt]he|[Aa]|[Aa]n|[Ii]ts|[Tt]heir)\s+[A-Za-z0-9_-]+(?:\s+[A-Za-z0-9_-]+){{0,2}}|[A-Z][A-Za-z0-9_-]*(?:\s+[A-Za-z0-9_-]+){{0,2}})\s+(?:{_CLAUSE_VERB_ALT})\b"
)

ATTRIBUTION_SPLIT_RE = re.compile(
    r"(?:\b(?:relative\s+to|compared\s+(?:with|to)|versus|in\s+contrast\s+to|unlike|despite|in\s+spite\s+of|against)\b"
    r"|\bvs\.(?=\s|$|[(\[{+\-−$\d.,;)])|\bvs\b)",
    re.IGNORECASE,
)

STAT_IDENTIFIER_PREFIX_RE = re.compile(
    r"\b(?:[Nn]|df|p|r|t|F|z|SD|SE)\s*[=<≤≥]\s*$",
)


def _enclosing_bracket_span(
    text: str,
    start: int,
    end: int,
    tok_start: int,
    tok_end: int,
) -> tuple[int, int] | None:
    pairs = {"(": ")", "[": "]", "{": "}"}
    closing = {")", "]", "}"}
    stack: list[tuple[str, int]] = []
    for idx in range(start, tok_start):
        ch = text[idx]
        if ch in pairs:
            stack.append((ch, idx))
        elif ch in closing and stack and pairs[stack[-1][0]] == ch:
            stack.pop()
    if not stack:
        return None
    open_ch, open_idx = stack[-1]
    want_close = pairs[open_ch]
    depth = 1
    close_idx = end
    for idx in range(tok_end, end):
        ch = text[idx]
        if ch == open_ch:
            depth += 1
        elif ch == want_close:
            depth -= 1
            if depth == 0:
                close_idx = idx
                break
    return open_idx, close_idx


def _mask_bracket_interiors(segment: str) -> str:
    chars = list(segment)
    depth = 0
    for idx, ch in enumerate(chars):
        if ch in "([{":
            depth += 1
            chars[idx] = " "
        elif ch in ")]}" and depth > 0:
            chars[idx] = " "
            depth -= 1
        elif depth > 0:
            chars[idx] = " "
    return "".join(chars)


def _find_top_level_comma(segment: str) -> int:
    depth = 0
    for idx, ch in enumerate(segment):
        if ch in "([{":
            depth += 1
        elif ch in ")]}" and depth > 0:
            depth -= 1
        elif ch == "," and depth == 0:
            return idx
    return -1


def _find_last_top_level_comma(segment: str) -> int:
    depth = 0
    last_idx = -1
    for idx, ch in enumerate(segment):
        if ch in "([{":
            depth += 1
        elif ch in ")]}" and depth > 0:
            depth -= 1
        elif ch == "," and depth == 0:
            last_idx = idx
    return last_idx


def _min_unnegated_cue_distance(
    pattern: re.Pattern[str],
    cleaned: str,
    c_start: int,
    left_start: int,
    tok_start: int,
    tok_end: int,
    right_end: int,
) -> int | None:
    best: int | None = None
    for seg_start, seg_end, is_left in ((left_start, tok_start, True), (tok_end, right_end, False)):
        if seg_end <= seg_start:
            continue
        for cm in pattern.finditer(cleaned, seg_start, seg_end):
            prefix = re.sub(r"\s+", " ", cleaned[max(c_start, cm.start() - 80):cm.start()])
            if not DOUBLE_NEGATED_CUE_RE.search(prefix) and NEGATED_CUE_PREFIX_RE.search(prefix):
                continue
            dist = (tok_start - cm.end()) if is_left else (cm.start() - tok_end)
            if best is None or dist < best:
                best = dist
    return best


def _last_unclosed_open_offset(segment: str) -> int:
    pairs = {"(": ")", "[": "]", "{": "}"}
    closing = {")", "]", "}"}
    stack: list[tuple[str, int]] = []
    for idx, ch in enumerate(segment):
        if ch in pairs:
            stack.append((ch, idx))
        elif ch in closing and stack and pairs[stack[-1][0]] == ch:
            stack.pop()
    return stack[-1][1] if stack else -1


def _subclause_spans(text: str) -> list[tuple[int, int]]:
    """Partition prose into abbreviation- and decimal-safe local contrast sub-clauses."""
    if not text:
        return []
    protected = ABBREV_PROTECT_RE.sub(lambda m: m.group(0)[:-1] + "_", text)
    sent_spans: list[tuple[int, int]] = []
    start = 0
    for m in re.finditer(r"(?<!\d)[.!?](?!\d)\s+|\n+", protected):
        sent_spans.append((start, m.start() + (1 if text[m.start()] in ".!?" else 0)))
        start = m.end()
    if start < len(text):
        sent_spans.append((start, len(text)))

    clause_spans: list[tuple[int, int, bool]] = []
    for s_start, s_end in sent_spans:
        if s_end <= s_start:
            continue
        cur = s_start
        can_be_fronted = True
        for cm in CONTRAST_CONJ_RE.finditer(text, s_start, s_end):
            if cm.start() <= cur:
                continue
            matched_conj = cm.group(0)
            conj_stripped = matched_conj.lstrip(", \t")
            if matched_conj.startswith(",") and not conj_stripped:
                raw_pre = text[cur:cm.start()]
                unclosed_off = _last_unclosed_open_offset(raw_pre)
                active_pre = raw_pre[unclosed_off + 1:] if unclosed_off != -1 else raw_pre
                masked_pre = _mask_bracket_interiors(active_pre)
                if not (CLAUSE_FINITE_VERB_RE.search(masked_pre) and NUMERIC_TOKEN_RE.search(masked_pre)):
                    continue
            elif not matched_conj.startswith(",") and conj_stripped.lower().startswith("and"):
                raw_pre = text[cur:cm.start()]
                unclosed_off = _last_unclosed_open_offset(raw_pre)
                active_pre = raw_pre[unclosed_off + 1:] if unclosed_off != -1 else raw_pre
                last_c = _find_last_top_level_comma(active_pre)
                clause_pre = active_pre[last_c + 1:] if last_c != -1 else active_pre
                masked_pre = _mask_bracket_interiors(clause_pre)
                if not (CLAUSE_FINITE_VERB_RE.search(masked_pre) or NUMERIC_TOKEN_RE.search(masked_pre)):
                    continue
            clause_spans.append((cur, cm.start(), can_be_fronted))
            is_semi = text[cm.start()] == ";"
            cur = cm.start() + (1 if text[cm.start()] in ",;" else 0)
            can_be_fronted = is_semi
        if cur < s_end:
            clause_spans.append((cur, s_end, can_be_fronted))

    refined: list[tuple[int, int]] = []
    for c_start, c_end, can_be_fronted in clause_spans:
        seg = text[c_start:c_end]
        if can_be_fronted and FRONTED_CONTRAST_RE.match(seg):
            comma_off = _find_top_level_comma(seg)
            if comma_off != -1 and comma_off + 1 < len(seg):
                refined.append((c_start, c_start + comma_off))
                refined.append((c_start + comma_off + 1, c_end))
                continue
        refined.append((c_start, c_end))
    return refined


def _split_contrast_clauses(text: str) -> list[str]:
    return [text[s:e].strip() for s, e in _subclause_spans(text) if text[s:e].strip()]


def extract_numeric_tokens(text: str) -> list[dict[str, Any]]:
    """Extract data-bearing numeric tokens with explicit sign and local clause polarity."""
    cleaned = _strip_non_data_tokens(text)
    spans = _subclause_spans(cleaned)
    tokens: list[dict[str, Any]] = []
    for m in NUMERIC_TOKEN_RE.finditer(cleaned):
        raw_sign = m.group(1)
        raw_mag = m.group(2)
        mag = _canonical_magnitude(raw_mag)
        # Skip bare small structural integers 0..2 unless explicitly signed or %, $, sci
        if not raw_sign and not mag.startswith("$") and not mag.endswith("%") and "." not in mag and "e" not in mag.lower():
            try:
                iv = int(mag)
                if iv in {0, 1, 2} and not re.search(
                    rf"\b(?:N|n|equal\s+to|of|across|fixed)\s+{iv}\b",
                    cleaned[max(0, m.start() - 20):min(len(cleaned), m.end() + 20)],
                ):
                    if iv == 0:
                        continue
            except ValueError:
                pass

        sign: str | None = None
        if raw_sign in {"-", "−"}:
            sign = "-"
        elif raw_sign == "+":
            sign = "+"

        c_start, c_end = 0, len(cleaned)
        span_id = 0
        for sp_idx, (s_idx, e_idx) in enumerate(spans):
            if s_idx <= m.start() < e_idx:
                c_start, c_end = s_idx, e_idx
                span_id = sp_idx
                break
        clause = cleaned[max(c_start, m.start() - 95):min(c_end, m.end() + 75)]
        is_stat_neutral = sign is None and bool(
            STAT_IDENTIFIER_PREFIX_RE.search(cleaned[max(0, m.start() - 10):m.start()])
        )

        if is_stat_neutral:
            polarity = "neutral"
        elif sign == "-":
            polarity = "negative"
        elif sign == "+":
            polarity = "positive"
        else:
            left_abs = max(c_start, m.start() - 95)
            right_abs = min(c_end, m.end() + 75)

            enclosing = _enclosing_bracket_span(cleaned, c_start, c_end, m.start(), m.end())
            if enclosing is not None:
                open_idx, close_idx = enclosing
                right_abs = min(right_abs, close_idx)
                pre_open_clause = cleaned[c_start:open_idx]
                last_pre_comma = _find_last_top_level_comma(pre_open_clause)
                pre_open_seg = pre_open_clause[last_pre_comma + 1:] if last_pre_comma != -1 else pre_open_clause
                paren_inner = cleaned[open_idx + 1:close_idx]
                if (
                    NUMERIC_TOKEN_RE.search(pre_open_seg)
                    or _has_unnegated_cue(NEGATIVE_POLARITY_CUES, paren_inner)
                    or _has_unnegated_cue(POSITIVE_POLARITY_CUES, paren_inner)
                    or PAREN_ISOLATION_MARKER_RE.search(paren_inner)
                    or PAREN_SUBJ_VERB_RE.search(paren_inner)
                ):
                    left_abs = max(left_abs, open_idx + 1)

            right_seg = cleaned[m.end():right_abs]
            r_comma = _find_top_level_comma(right_seg)
            if r_comma != -1:
                right_abs = m.end() + r_comma
                right_seg = cleaned[m.end():right_abs]
            r_prep = RIGHT_POLARITY_BOUNDARY_RE.search(right_seg)
            if r_prep is not None:
                right_abs = m.end() + r_prep.start()
                right_seg = cleaned[m.end():right_abs]

            left_seg = cleaned[left_abs:m.start()]
            last_comma = _find_last_top_level_comma(left_seg)
            if last_comma != -1:
                post_comma_abs = left_abs + last_comma + 1
                top_post_comma = _mask_bracket_interiors(cleaned[post_comma_abs:right_abs])
                if (
                    NUMERIC_TOKEN_RE.search(left_seg[:last_comma])
                    or POST_COMMA_FINITE_VERB_RE.search(top_post_comma)
                    or _min_unnegated_cue_distance(
                        NEGATIVE_POLARITY_CUES, cleaned, c_start, post_comma_abs, m.start(), m.end(), m.end()
                    ) is not None
                    or _min_unnegated_cue_distance(
                        POSITIVE_POLARITY_CUES, cleaned, c_start, post_comma_abs, m.start(), m.end(), m.end()
                    ) is not None
                ):
                    left_abs = post_comma_abs
                    left_seg = cleaned[left_abs:m.start()]

            advance_off = 0
            for pm in PRIOR_NUM_PREP_BOUNDARY_RE.finditer(left_seg):
                tail = left_seg[pm.end():]
                pm_text = pm.group(0)
                pm_has_gov_cue = _has_unnegated_cue(NEGATIVE_POLARITY_CUES, pm_text) or _has_unnegated_cue(
                    POSITIVE_POLARITY_CUES, pm_text
                )
                if not (pm_has_gov_cue and re.search(r"\bby\b", tail, re.IGNORECASE)):
                    advance_off = max(advance_off, pm.end())
            for cm in COMPARATOR_PREP_RE.finditer(left_seg):
                tail = left_seg[cm.end():]
                if not re.search(r"\bby\b", tail, re.IGNORECASE) and not POST_COMMA_FINITE_VERB_RE.search(tail):
                    advance_off = max(advance_off, cm.end())
            if advance_off > 0:
                left_abs += advance_off

            r_open_m = re.search(r"[(\[{]", cleaned[m.end():right_abs])
            if r_open_m is not None:
                r_open_abs = m.end() + r_open_m.start()
                r_open_ch = cleaned[r_open_abs]
                r_close_ch = {"(": ")", "[": "]", "{": "}"}[r_open_ch]
                r_depth = 1
                r_close_abs = c_end
                for r_idx in range(r_open_abs + 1, c_end):
                    if cleaned[r_idx] == r_open_ch:
                        r_depth += 1
                    elif cleaned[r_idx] == r_close_ch:
                        r_depth -= 1
                        if r_depth == 0:
                            r_close_abs = r_idx
                            break
                r_paren_inner = cleaned[r_open_abs + 1:r_close_abs]
                r_raw_paren_inner = text[r_open_abs + 1:r_close_abs]
                if (
                    PAREN_ISOLATION_MARKER_RE.search(r_paren_inner)
                    or PAREN_SUBJ_VERB_RE.search(r_paren_inner)
                    or (
                        NUMERIC_TOKEN_RE.search(r_paren_inner)
                        and (
                            STRUCTURAL_LOCATOR_RE.search(r_raw_paren_inner)
                            or _min_unnegated_cue_distance(
                                NEGATIVE_POLARITY_CUES, cleaned, c_start, left_abs, m.start(), m.end(), m.end()
                            ) is not None
                            or _min_unnegated_cue_distance(
                                POSITIVE_POLARITY_CUES, cleaned, c_start, left_abs, m.start(), m.end(), m.end()
                            ) is not None
                        )
                    )
                ):
                    right_abs = r_open_abs

            min_neg = _min_unnegated_cue_distance(
                NEGATIVE_POLARITY_CUES, cleaned, c_start, left_abs, m.start(), m.end(), right_abs
            )
            min_pos = _min_unnegated_cue_distance(
                POSITIVE_POLARITY_CUES, cleaned, c_start, left_abs, m.start(), m.end(), right_abs
            )
            if min_neg is not None and (min_pos is None or min_neg < min_pos):
                polarity = "negative"
            elif min_pos is not None and (min_neg is None or min_pos < min_neg):
                polarity = "positive"
            else:
                polarity = "neutral"

        tokens.append(
            {
                "raw": (raw_sign or "") + raw_mag,
                "sign": sign,
                "magnitude": mag,
                "polarity": polarity,
                "context": re.sub(r"\s+", " ", clause).strip(),
                "span_id": span_id,
                "start": m.start(),
                "end": m.end(),
            }
        )
    return tokens


def verify_strict_preservation(
    before_text: str,
    after_text: str,
    allow_sign_verb_pairs: bool = True,
) -> dict[str, Any]:
    """Mode 1: strict multiset conservation of all data numbers and signs."""
    before_toks = extract_numeric_tokens(before_text) if isinstance(before_text, str) else []
    if not isinstance(after_text, str) or not after_text.strip():
        return {
            "status": "FAIL",
            "mode": "strict_preservation",
            "before_token_count": len(before_toks),
            "after_token_count": 0,
            "paired_sign_verb_equivalences": [],
            "findings": [{"code": "EMPTY_CANDIDATE_PROSE", "detail": "Candidate prose must not be empty."}],
        }
    after_toks = extract_numeric_tokens(after_text)

    b_pool = list(before_toks)
    a_pool = list(after_toks)

    def _eff_pol(tok: dict[str, Any]) -> str:
        if tok["sign"] == "-" or tok["polarity"] == "negative":
            return "negative"
        if tok["sign"] == "+" or tok["polarity"] == "positive":
            return "positive"
        return "neutral"

    # Pass 1a: consume exact (sign, magnitude, polarity, is_mag_qualified) matches one-for-one
    for bt in list(b_pool):
        bt_mq = _is_valid_magnitude_qualification(bt["context"])
        match_a = next(
            (
                at for at in a_pool
                if (at["sign"], at["magnitude"], at["polarity"], _is_valid_magnitude_qualification(at["context"]))
                == (bt["sign"], bt["magnitude"], bt["polarity"], bt_mq)
            ),
            None,
        )
        if match_a is not None:
            b_pool.remove(bt)
            a_pool.remove(match_a)

    # Pass 1b: consume exact (sign, magnitude, polarity) matches one-for-one
    for bt in list(b_pool):
        match_a = next(
            (
                at for at in a_pool
                if (at["sign"], at["magnitude"], at["polarity"])
                == (bt["sign"], bt["magnitude"], bt["polarity"])
            ),
            None,
        )
        if match_a is not None:
            b_pool.remove(bt)
            a_pool.remove(match_a)

    paired_equivalences: list[dict[str, str]] = []
    sign_flips: list[dict[str, str]] = []

    if allow_sign_verb_pairs and (b_pool or a_pool):
        b_span_converted_pols: dict[int, Counter[str]] = {}
        a_span_converted_pols: dict[int, Counter[str]] = {}

        # Pass 2a: explicit sign <-> matching directional polarity verb equivalences
        for bt in list(b_pool):
            b_sign, b_mag, b_pol = bt["sign"], bt["magnitude"], bt["polarity"]
            if b_sign == "-":
                match_a = next(
                    (at for at in a_pool if at["magnitude"] == b_mag and at["sign"] is None and at["polarity"] == "negative"),
                    None,
                )
                if match_a is not None:
                    b_pool.remove(bt)
                    a_pool.remove(match_a)
                    a_span_converted_pols.setdefault(match_a["span_id"], Counter())["negative"] += 1
                    paired_equivalences.append({"before": f"-{b_mag}", "after": match_a["context"]})
            elif b_sign == "+":
                match_a = next(
                    (at for at in a_pool if at["magnitude"] == b_mag and at["sign"] is None and at["polarity"] == "positive"),
                    None,
                )
                if match_a is not None:
                    b_pool.remove(bt)
                    a_pool.remove(match_a)
                    a_span_converted_pols.setdefault(match_a["span_id"], Counter())["positive"] += 1
                    paired_equivalences.append({"before": f"+{b_mag}", "after": match_a["context"]})
            elif b_sign is None and b_pol == "negative":
                match_a = next(
                    (at for at in a_pool if at["magnitude"] == b_mag and at["sign"] == "-"),
                    None,
                )
                if match_a is not None:
                    b_pool.remove(bt)
                    a_pool.remove(match_a)
                    b_span_converted_pols.setdefault(bt["span_id"], Counter())["negative"] += 1
                    paired_equivalences.append({"before": bt["context"], "after": f"-{b_mag}"})
            elif b_sign is None and b_pol == "positive":
                match_a = next(
                    (at for at in a_pool if at["magnitude"] == b_mag and at["sign"] == "+"),
                    None,
                )
                if match_a is not None:
                    b_pool.remove(bt)
                    a_pool.remove(match_a)
                    b_span_converted_pols.setdefault(bt["span_id"], Counter())["positive"] += 1
                    paired_equivalences.append({"before": bt["context"], "after": f"+{b_mag}"})

        # Pass 2b: signed/directional -> magnitude-qualified neutral (respecting MAGNITUDE_QUALIFIER_RE)
        for bt in list(b_pool):
            if _eff_pol(bt) in {"negative", "positive"}:
                b_mag = bt["magnitude"]
                match_a = next(
                    (
                        at for at in a_pool
                        if at["magnitude"] == b_mag
                        and at["sign"] is None
                        and at["polarity"] == "neutral"
                        and _is_valid_magnitude_qualification(at["context"])
                    ),
                    None,
                )
                if match_a is not None:
                    b_pool.remove(bt)
                    a_pool.remove(match_a)
                    paired_equivalences.append(
                        {"before": f"{bt['sign']}{b_mag}" if bt["sign"] else bt["context"], "after": match_a["context"]}
                    )

        # Pass 2c: unsigned bystander tokens in the same sub-clause colored solely by a Pass 2a sign<->verb conversion
        if b_span_converted_pols or a_span_converted_pols:
            def _count_unneg_cues(pol: str, ctx: str) -> int:
                pat = NEGATIVE_POLARITY_CUES if pol == "negative" else POSITIVE_POLARITY_CUES
                cnt = 0
                for cm in pat.finditer(ctx):
                    pref = ctx[max(0, cm.start() - 55):cm.start()]
                    if DOUBLE_NEGATED_CUE_RE.search(pref) or not NEGATED_CUE_PREFIX_RE.search(pref):
                        cnt += 1
                return cnt

            for bt in list(b_pool):
                if bt["sign"] is not None:
                    continue
                b_mag = bt["magnitude"]
                match_a = next(
                    (
                        at for at in a_pool
                        if at["magnitude"] == b_mag
                        and at["sign"] is None
                        and (
                            (
                                bt["polarity"] == "neutral"
                                and at["polarity"] in a_span_converted_pols.get(at["span_id"], {})
                                and _count_unneg_cues(at["polarity"], at["context"])
                                <= a_span_converted_pols[at["span_id"]][at["polarity"]]
                            )
                            or (
                                at["polarity"] == "neutral"
                                and bt["polarity"] in b_span_converted_pols.get(bt["span_id"], {})
                                and _count_unneg_cues(bt["polarity"], bt["context"])
                                <= b_span_converted_pols[bt["span_id"]][bt["polarity"]]
                            )
                        )
                    ),
                    None,
                )
                if match_a is not None:
                    b_pool.remove(bt)
                    a_pool.remove(match_a)

    # Pass 3a: opposite-polarity flips (including unsigned negative_verb <-> positive_verb)
    for bt in list(b_pool):
        b_eff = _eff_pol(bt)
        if b_eff not in {"negative", "positive"}:
            continue
        opp_eff = "positive" if b_eff == "negative" else "negative"
        match_a = next(
            (at for at in a_pool if at["magnitude"] == bt["magnitude"] and _eff_pol(at) == opp_eff),
            None,
        )
        if match_a is not None:
            b_pool.remove(bt)
            a_pool.remove(match_a)
            sign_flips.append(
                {
                    "magnitude": bt["magnitude"],
                    "before_sign": bt["sign"] or f"{bt['polarity']}_verb",
                    "after_sign": match_a["sign"] or f"{match_a['polarity']}_verb",
                }
            )

    # Pass 3b: neutral sign-drops (e.g., "-3.8%" -> "had a mean change of 3.8%") or ungrounded sign/polarity additions
    for bt in list(b_pool):
        b_eff = _eff_pol(bt)
        match_a = next(
            (
                at for at in a_pool
                if at["magnitude"] == bt["magnitude"]
                and ((b_eff != "neutral" and _eff_pol(at) == "neutral") or (b_eff == "neutral" and _eff_pol(at) != "neutral"))
            ),
            None,
        )
        if match_a is not None:
            b_pool.remove(bt)
            a_pool.remove(match_a)
            sign_flips.append(
                {
                    "magnitude": bt["magnitude"],
                    "before_sign": bt["sign"] or (f"{bt['polarity']}_verb" if bt["polarity"] != "neutral" else "unsigned_neutral"),
                    "after_sign": match_a["sign"] or (f"{match_a['polarity']}_verb" if match_a["polarity"] != "neutral" else "unsigned_neutral"),
                }
            )

    missing = [
        f"{t['sign'] or ''}{t['magnitude']}"
        for t in sorted(b_pool, key=lambda tok: (tok["sign"] or "", tok["magnitude"]))
    ]
    added = [
        f"{t['sign'] or ''}{t['magnitude']}"
        for t in sorted(a_pool, key=lambda tok: (tok["sign"] or "", tok["magnitude"]))
    ]
    meta_leaks = [m.group(0) for m in META_LEAKAGE_RE.finditer(after_text)]

    findings: list[dict[str, Any]] = []
    for flip in sign_flips:
        findings.append({"code": "NUM_SIGN_FLIP", "detail": flip})
    if missing:
        findings.append({"code": "NUM_MISSING_IN_STRICT_MODE", "tokens": missing})
    if added:
        findings.append({"code": "NUM_ADDED_IN_STRICT_MODE", "tokens": added})
    if meta_leaks:
        findings.append({"code": "META_COMMENTARY_LEAKAGE", "matches": meta_leaks})

    return {
        "status": "PASS" if not findings else "FAIL",
        "mode": "strict_preservation",
        "before_token_count": len(before_toks),
        "after_token_count": len(after_toks),
        "paired_sign_verb_equivalences": paired_equivalences,
        "findings": findings,
    }


def _parse_structured_rows(source_texts: list[str]) -> list[dict[str, Any]]:
    """Extract entity-bound signed numbers from Markdown/CSV/TSV/spine table rows."""
    rows: list[dict[str, Any]] = []
    for src in source_texts:
        for line in src.splitlines():
            raw_ln = line.strip()
            if not raw_ln:
                continue
            stripped_ln = LINE_BLOCK_PREFIX_RE.sub("", raw_ln).strip()
            if not stripped_ln:
                continue
            if "|" in stripped_ln:
                raw_cells = [c.strip() for c in stripped_ln.strip("|").split("|") if c.strip()]
                if (
                    not stripped_ln.startswith("|")
                    and stripped_ln.endswith((".", "?", "!"))
                    and any(len(c.split()) > 12 for c in raw_cells)
                ):
                    continue
                cells = raw_cells
            elif "\t" in stripped_ln and re.search(r"\d", stripped_ln):
                parsed = next(csv.reader([stripped_ln], delimiter="\t"), [])
                cells = [c.strip().strip("\"'").strip() for c in parsed if c.strip()]
            elif "," in stripped_ln and re.search(r"\d", stripped_ln) and not stripped_ln.startswith(("-", "*", "#")):
                if "=" in stripped_ln or re.search(r"\(\d+[a-z]?\)\s*$", stripped_ln):
                    continue
                try:
                    parsed = next(csv.reader([stripped_ln]), [])
                except csv.Error:
                    parsed = stripped_ln.split(",")
                if len(parsed) < 2:
                    continue
                # Avoid treating ordinary prose sentences with commas as CSV unless cells look tabular
                non_empty = [c.strip() for c in parsed if c.strip()]
                if len(non_empty) < 2 or any(len(c.split()) > 7 for c in non_empty):
                    continue
                cells = [c.strip("\"'").strip() for c in non_empty if c.strip("\"'").strip()]
            else:
                continue
            if len(cells) < 2 or re.fullmatch(r"[\s:|-]+", stripped_ln):
                continue
            entity_labels: list[str] = []
            row_tokens: list[tuple[str | None, str]] = []
            row_token_polarities: list[tuple[str | None, str, str]] = []
            for cell in cells:
                stripped_cell = BLOCK_PREFIX_RE.sub("", cell).strip()
                if not stripped_cell:
                    continue
                cell_nums = extract_numeric_tokens(stripped_cell)
                if cell_nums:
                    for t in cell_nums:
                        row_tokens.append((t["sign"], t["magnitude"]))
                        row_token_polarities.append((t["sign"], t["magnitude"], t["polarity"]))
                else:
                    # Non-numeric label cell (e.g., outcome/subscale or model name)
                    clean_label = stripped_cell.strip("\"'").strip()
                    if (
                        len(clean_label) <= 45
                        and "[" not in clean_label
                        and "]" not in clean_label
                        and "=" not in clean_label
                        and re.search(r"[A-Za-z]", clean_label)
                    ):
                        entity_labels.append(clean_label)
            if entity_labels and row_tokens:
                rows.append(
                    {
                        "entities": entity_labels,
                        "tokens": row_tokens,
                        "token_polarities": row_token_polarities,
                        "raw": raw_ln,
                    }
                )
    deduped_rows: list[dict[str, Any]] = []
    seen_row_keys: set[tuple[tuple[str, ...], tuple[tuple[str | None, str, str], ...]]] = set()
    for row in rows:
        rkey = (tuple(row["entities"]), tuple(row["token_polarities"]))
        if rkey not in seen_row_keys:
            seen_row_keys.add(rkey)
            deduped_rows.append(row)
    return deduped_rows


def _extract_bootstrap_locks(source_texts: list[str]) -> set[str]:
    """Find integers explicitly locked to bootstrap/resample draws rather than generative runs."""
    locked: set[str] = set()
    pattern = re.compile(r"\b(\d[\d,]*)\s+(?:respondent-level\s+|household-level\s+|paired\s+|cluster\s+)*bootstrap\b", re.IGNORECASE)
    for src in source_texts:
        for m in pattern.finditer(src):
            locked.add(_canonical_magnitude(m.group(1)))
    return locked


def _contains_known_entity(segment: str, entities: set[str]) -> bool:
    return any(re.search(rf"\b{re.escape(ent)}\b", segment, re.IGNORECASE) for ent in entities)


def _build_attribution_units(
    after_text: str,
    cleaned: str,
    after_toks: list[dict[str, Any]],
    all_known_peer_entities: set[str],
) -> list[tuple[str, list[dict[str, Any]]]]:
    """Slice after_toks (retaining full-sentence polarities) into local entity-number attribution units."""
    spans = _subclause_spans(cleaned)
    working_chars = list(after_text)
    raw_units: list[tuple[int, str, list[dict[str, Any]]]] = []
    b_pairs = {"(": ")", "[": "]"}
    matched_close: dict[int, int] = {}
    g_stack: list[tuple[str, int]] = []
    for idx, ch in enumerate(after_text):
        if ch in b_pairs:
            g_stack.append((ch, idx))
        elif ch in {")", "]"} and g_stack and b_pairs[g_stack[-1][0]] == ch:
            _, open_pos = g_stack.pop()
            matched_close[open_pos] = idx

    for s_idx, e_idx in spans:
        span_toks = [t for t in after_toks if s_idx <= t["start"] < e_idx]
        if not span_toks:
            continue
        paren_spans = sorted(
            [
                (
                    max(b_open, s_idx),
                    b_open + 1 if b_open >= s_idx else s_idx,
                    min(g_close, e_idx),
                    min(g_close + 1, e_idx) if g_close < e_idx else e_idx,
                )
                for b_open, g_close in matched_close.items()
                if b_open < e_idx and g_close >= s_idx
            ],
            key=lambda quad: (quad[2] - quad[1], quad[1]),
        )

        claimed_tok_ids: set[int] = set()
        extracted_inner: list[tuple[int, str, list[dict[str, Any]]]] = []
        for mask_start, inner_start, inner_end, mask_end in paren_spans:
            inner_str = "".join(working_chars[inner_start:inner_end])
            inner_toks = [
                t for t in span_toks
                if id(t) not in claimed_tok_ids and inner_start <= t["start"] and t["end"] <= inner_end
            ]
            if inner_toks and _contains_known_entity(inner_str, all_known_peer_entities):
                for t in inner_toks:
                    claimed_tok_ids.add(id(t))
                extracted_inner.append((inner_start, inner_str, inner_toks))
                working_chars[mask_start:mask_end] = [" "] * (mask_end - mask_start)
            elif (
                not inner_toks
                and _contains_known_entity(inner_str, all_known_peer_entities)
                and FRONTED_CONTRAST_RE.match(inner_str)
            ):
                working_chars[mask_start:mask_end] = [" "] * (mask_end - mask_start)

        outer_toks = [t for t in span_toks if id(t) not in claimed_tok_ids]
        if outer_toks:
            outer_str = "".join(working_chars[s_idx:e_idx])
            raw_units.append((s_idx, outer_str, outer_toks))
        raw_units.extend(extracted_inner)

    final_units: list[tuple[str, list[dict[str, Any]]]] = []
    for u_base, u_text, u_toks in raw_units:
        match_iter = list(ATTRIBUTION_SPLIT_RE.finditer(u_text))
        if not match_iter:
            final_units.append((u_text, u_toks))
            continue
        depth = 0
        depths = [0] * (len(u_text) + 1)
        for idx, ch in enumerate(u_text):
            depths[idx] = depth
            if ch in "([{":
                depth += 1
            elif ch in ")]}" and depth > 0:
                depth -= 1
        depths[len(u_text)] = depth
        top_split_matches = [sm for sm in match_iter if depths[sm.start()] == 0]
        if not top_split_matches:
            final_units.append((u_text, u_toks))
            continue

        cur_local = 0
        for sm in top_split_matches:
            if sm.start() <= cur_local:
                continue
            left_abs_s = u_base + cur_local
            left_abs_e = u_base + sm.start()
            right_abs_s = u_base + sm.end()
            right_abs_e = u_base + len(u_text)
            left_toks = [t for t in u_toks if left_abs_s <= t["start"] < left_abs_e]
            right_toks = [t for t in u_toks if right_abs_s <= t["start"] < right_abs_e]
            left_seg = u_text[cur_local:sm.start()]
            right_seg = u_text[sm.end():]
            should_split = bool(left_toks and right_toks) or (
                bool(left_toks and not right_toks)
                and _contains_known_entity(left_seg, all_known_peer_entities)
                and _contains_known_entity(right_seg, all_known_peer_entities)
            )
            if should_split:
                final_units.append((left_seg, left_toks))
                cur_local = sm.end()
        tail_abs_s = u_base + cur_local
        tail_abs_e = u_base + len(u_text)
        tail_toks = [t for t in u_toks if tail_abs_s <= t["start"] < tail_abs_e]
        if tail_toks:
            final_units.append((u_text[cur_local:], tail_toks))

    return final_units


def _collect_omitted_strings(declared_omitted: list[Any]) -> list[str]:
    strings: list[str] = []
    for item in declared_omitted:
        if isinstance(item, str):
            strings.append(item)
        elif isinstance(item, dict):
            for k in ("value_or_entity", "values", "value", "entity", "omitted", "rationale_tier", "display_ref"):
                if k in item and item[k] is not None:
                    val = item[k]
                    if isinstance(val, list):
                        strings.extend(str(x) for x in val)
                    else:
                        strings.append(str(val))
    return strings


def verify_curated_salience(
    after_text: str,
    source_texts: list[str],
    before_text: str | None = None,
    declared_omitted_to_display: list[Any] | None = None,
    downstream_dependencies: list[dict[str, Any]] | None = None,
    cross_section_sync_alerts: list[Any] | None = None,
) -> dict[str, Any]:
    """Mode 2: entity+sign provenance, Mode R partitioned conservation, and Class B orphan detection."""
    declared_omitted_to_display = declared_omitted_to_display or []
    downstream_dependencies = downstream_dependencies or []
    cross_section_sync_alerts = cross_section_sync_alerts or []

    if not isinstance(after_text, str) or not after_text.strip():
        return {
            "status": "FAIL",
            "mode": "curated_salience",
            "after_token_count": 0,
            "declared_omitted_token_count": 0,
            "undeclared_drops": [],
            "class_b_downstream_sync_checklist": [],
            "findings": [{"code": "EMPTY_CANDIDATE_PROSE", "detail": "Candidate prose must not be empty."}],
        }

    findings: list[dict[str, Any]] = []

    # Build authoritative pool of allowed magnitudes & signs (upstream/display sources take precedence over draft `before_text`)
    auth_source_toks: list[dict[str, Any]] = []
    for src in source_texts:
        auth_source_toks.extend(extract_numeric_tokens(src))
    before_toks = extract_numeric_tokens(before_text) if before_text else []

    bootstrap_only_ints = _extract_bootstrap_locks(source_texts)
    allowed_magnitudes = {t["magnitude"] for t in auth_source_toks} | {t["magnitude"] for t in before_toks}
    signs_by_mag: dict[str, set[str | None]] = {}
    eff_polarities_by_mag: dict[str, set[str]] = {}

    def _eff_source_polarity(tok: dict[str, Any]) -> str:
        if tok["sign"] == "-" or tok["polarity"] == "negative":
            return "negative"
        if tok["sign"] == "+" or tok["polarity"] == "positive":
            return "positive"
        return "unsigned_nonneg"

    for t in auth_source_toks:
        signs_by_mag.setdefault(t["magnitude"], set()).add(t["sign"])
        eff_polarities_by_mag.setdefault(t["magnitude"], set()).add(_eff_source_polarity(t))
    auth_magnitudes = set(signs_by_mag.keys())
    for t in before_toks:
        if t["magnitude"] not in auth_magnitudes:
            signs_by_mag.setdefault(t["magnitude"], set()).add(t["sign"])
            eff_polarities_by_mag.setdefault(t["magnitude"], set()).add(_eff_source_polarity(t))

    after_toks = extract_numeric_tokens(after_text)

    # Check A1: 100% numeric provenance
    unverified = sorted({t["raw"] for t in after_toks if t["magnitude"] not in allowed_magnitudes})
    if unverified:
        findings.append({"code": "UNVERIFIED_NUMBER_IN_PROSE", "tokens": unverified})

    # Check A2: Generative-run vs. bootstrap resample drift
    for m_gen in GENERATIVE_CONFUSION_RE.finditer(after_text):
        mag = _canonical_magnitude(m_gen.group(1))
        if mag in bootstrap_only_ints:
            findings.append(
                {
                    "code": "POPULATION_INTEGER_DRIFT",
                    "match": m_gen.group(0),
                    "detail": f"{mag} is locked to bootstrap resamples in Methods, not generative/simulation runs",
                }
            )

    # Check A3: Entity + Sign provenance against structured source rows and unambiguous global signs
    structured_rows = _parse_structured_rows(source_texts)
    has_doc_subtraction_flip = bool(SUBTRACTION_FLIP_CUES.search(" ".join(source_texts) + " " + after_text))

    def _has_local_subtraction_flip(ctx: str, tok_sign: str | None, tok_polarity: str) -> bool:
        if tok_sign == "-" or tok_polarity == "neutral":
            return False
        if SUBTRACTION_FLIP_CUES.search(ctx):
            return True
        return bool(has_doc_subtraction_flip and re.search(r"\b(?:MAE|RMSE|error)\b", ctx, re.IGNORECASE))

    for t in after_toks:
        mag = t["magnitude"]
        known_signs = signs_by_mag.get(mag, set())
        known_eff_pols = eff_polarities_by_mag.get(mag, set())
        is_mag_qualified = _is_valid_magnitude_qualification(t["context"])
        tok_sub_flip = _has_local_subtraction_flip(t["context"], t["sign"], t["polarity"])
        # Unambiguously negative across all source occurrences (no unsigned/positive counterpart)
        if known_eff_pols == {"negative"} and not is_mag_qualified and not tok_sub_flip:
            if (
                t["sign"] == "+"
                or (t["sign"] is None and t["polarity"] == "positive")
                or (known_signs == {"-"} and t["sign"] is None and t["polarity"] != "negative")
            ):
                findings.append(
                    {
                        "code": "ENTITY_SIGN_REVERSAL",
                        "token": t["raw"],
                        "expected_sign": "-",
                        "context": t["context"],
                    }
                )
        elif (known_signs == {"+"} or known_eff_pols == {"positive"}) and not tok_sub_flip:
            if t["sign"] == "-" or (t["sign"] is None and t["polarity"] == "negative" and not is_mag_qualified):
                findings.append(
                    {
                        "code": "ENTITY_SIGN_REVERSAL",
                        "token": t["raw"],
                        "expected_sign": "+",
                        "context": t["context"],
                    }
                )
        elif (
            known_eff_pols
            and known_eff_pols <= {"positive", "unsigned_nonneg"}
            and "-" not in known_signs
            and not tok_sub_flip
        ):
            if t["sign"] == "-":
                findings.append(
                    {
                        "code": "ENTITY_SIGN_REVERSAL",
                        "token": t["raw"],
                        "expected_sign": "+",
                        "context": t["context"],
                    }
                )

    # Sub-clause entity-sign & peer-entity swap check
    if structured_rows:
        rows_by_mag: dict[str, list[dict[str, Any]]] = {}
        all_known_peer_entities: set[str] = set()
        for row in structured_rows:
            for ent in row["entities"]:
                if len(ent) >= 3:
                    all_known_peer_entities.add(ent)
            for sgn, mag, pol in row.get(
                "token_polarities",
                [(s, m, "negative" if s == "-" else ("positive" if s == "+" else "neutral")) for s, m in row["tokens"]],
            ):
                eff_pol = (
                    "negative"
                    if (sgn == "-" or pol == "negative")
                    else ("positive" if (sgn == "+" or pol == "positive") else "unsigned_nonneg")
                )
                rows_by_mag.setdefault(mag, []).append({"entities": row["entities"], "sign": sgn, "eff_pol": eff_pol})

        cleaned_after = _strip_non_data_tokens(after_text)
        attribution_units = _build_attribution_units(after_text, cleaned_after, after_toks, all_known_peer_entities)
        for unit_text, unit_toks in attribution_units:
            unit_ctx = re.sub(r"\s+", " ", unit_text).strip()[:180]
            for t in unit_toks:
                mag = t["magnitude"]
                cand_rows = rows_by_mag.get(mag, [])
                if not cand_rows:
                    continue
                matched_rows = [
                    r for r in cand_rows
                    if any(re.search(rf"\b{re.escape(ent)}\b", unit_text, re.IGNORECASE) for ent in r["entities"])
                ]
                if matched_rows:
                    req_signs = {r["sign"] for r in matched_rows}
                    req_eff_pols = {r["eff_pol"] for r in matched_rows}
                    is_sub_mag_qualified = _is_valid_magnitude_qualification(unit_text)
                    sub_tok_flip = _has_local_subtraction_flip(unit_text, t["sign"], t["polarity"])
                    if (
                        req_eff_pols == {"negative"}
                        and not is_sub_mag_qualified
                        and not sub_tok_flip
                        and (
                            t["sign"] == "+"
                            or (t["sign"] is None and t["polarity"] == "positive")
                            or (req_signs == {"-"} and t["sign"] is None and t["polarity"] != "negative")
                        )
                    ):
                        findings.append(
                            {
                                "code": "ENTITY_SIGN_REVERSAL",
                                "token": t["raw"],
                                "expected_sign": "-",
                                "context": unit_ctx,
                            }
                        )
                    elif (
                        req_eff_pols <= {"positive", "unsigned_nonneg"}
                        and "-" not in req_signs
                        and not sub_tok_flip
                        and (
                            t["sign"] == "-"
                            or (
                                (req_signs == {"+"} or req_eff_pols == {"positive"})
                                and not is_sub_mag_qualified
                                and t["sign"] is None
                                and t["polarity"] == "negative"
                            )
                        )
                    ):
                        findings.append(
                            {
                                "code": "ENTITY_SIGN_REVERSAL",
                                "token": t["raw"],
                                "expected_sign": "+",
                                "context": unit_ctx,
                            }
                        )
                elif len({tuple(r["entities"]) for r in cand_rows}) == 1:
                    if t["sign"] is None and re.fullmatch(r"\d", mag):
                        continue
                    owner_ents = cand_rows[0]["entities"]
                    mentioned_peers = [
                        pe for pe in all_known_peer_entities
                        if pe not in owner_ents and re.search(rf"\b{re.escape(pe)}\b", unit_text, re.IGNORECASE)
                    ]
                    owner_mentioned = any(re.search(rf"\b{re.escape(oe)}\b", unit_text, re.IGNORECASE) for oe in owner_ents)
                    if mentioned_peers and not owner_mentioned:
                        findings.append(
                            {
                                "code": "CROSS_ENTITY_NUMBER_SWAP",
                                "token": t["raw"],
                                "owner_entities": owner_ents,
                                "attributed_to": mentioned_peers,
                                "context": unit_ctx,
                            }
                        )

    # Deduplicate any overlapping global vs sub-clause ENTITY_SIGN_REVERSAL on the same token
    deduped_findings: list[dict[str, Any]] = []
    seen_reversals: set[tuple[str, str]] = set()
    for f in findings:
        if f["code"] == "ENTITY_SIGN_REVERSAL":
            key = (str(f.get("token", "")), str(f.get("expected_sign", "")))
            if key in seen_reversals:
                continue
            seen_reversals.add(key)
        deduped_findings.append(f)
    findings = deduped_findings

    # Check B: Mode R Partitioned Conservation (before <= after + declared_omitted_to_display)
    undeclared_drops: list[str] = []
    omitted_strings = _collect_omitted_strings(declared_omitted_to_display)
    omitted_toks = extract_numeric_tokens(" ; ".join(omitted_strings))

    if before_text is not None:
        before_mags = Counter(t["magnitude"] for t in before_toks)
        after_mags = Counter(t["magnitude"] for t in after_toks)
        omitted_mags = Counter(t["magnitude"] for t in omitted_toks)
        # Exclude any known erroneous bootstrap-confused number from mandatory retention if omitted
        unaccounted = before_mags - (after_mags + omitted_mags)
        for mag, count in sorted(unaccounted.items()):
            if mag in bootstrap_only_ints:
                continue
            for _ in range(count):
                undeclared_drops.append(mag)
        if undeclared_drops:
            findings.append(
                {
                    "code": "UNDECLARED_OMITTED_NUMBER",
                    "tokens": undeclared_drops,
                    "detail": "Mode R requires every number removed from `before` to be accounted for in `declared_omitted_to_display`.",
                }
            )

    # Check C: Downstream cross-section orphan detection (Class B sync gate)
    omitted_blob = " ".join(omitted_strings).lower()
    before_low = (before_text or "").lower()
    alerts_blob = json.dumps(cross_section_sync_alerts, ensure_ascii=False).lower()

    downstream_sync_required: list[dict[str, Any]] = []
    for dep in downstream_dependencies:
        item = str(dep.get("item", "")).strip()
        if not item:
            continue
        kind = dep.get("kind", "item")
        item_mag = _canonical_magnitude(item.lstrip("+−-\u2013"))
        after_has_item = (
            any(t["magnitude"] == item_mag for t in after_toks)
            if kind == "numeric_value"
            else bool(re.search(rf"\b{re.escape(item)}\b", after_text, re.IGNORECASE))
        )
        before_has_item = bool(
            before_text is not None
            and (
                any(t["magnitude"] == item_mag for t in before_toks)
                if kind == "numeric_value"
                else item.lower() in before_low
            )
        )
        was_pruned_or_declared = (
            item.lower() in omitted_blob
            or item_mag.lower() in omitted_blob
            or (before_has_item and not after_has_item)
        )
        if was_pruned_or_declared and not after_has_item:
            locs = dep.get("downstream_locations", [])
            ack = (
                item.lower() in alerts_blob
                or item_mag.lower() in alerts_blob
                or any(
                    bool(loc.get("block_id")) and str(loc["block_id"]).lower() in alerts_blob
                    for loc in locs
                )
            )
            alert_entry = {
                "code": "CLASS_B_SYNC_REQUIRED",
                "pruned_item": item,
                "kind": kind,
                "acknowledged_in_sync_alerts": ack,
                "downstream_locations": locs,
            }
            downstream_sync_required.append(alert_entry)
            if not ack:
                findings.append(
                    {
                        "code": "UNACKNOWLEDGED_DOWNSTREAM_ORPHAN",
                        "pruned_item": item,
                        "downstream_locations": [f"{loc.get('block_id')}:{loc.get('section_role')}" for loc in locs],
                        "detail": "Item pruned from Results is still referenced downstream without a matching `cross_section_sync_alerts` entry.",
                    }
                )

    # Check D: Meta-leakage check
    meta_leaks = [m.group(0) for m in META_LEAKAGE_RE.finditer(after_text)]
    if meta_leaks:
        findings.append({"code": "META_COMMENTARY_LEAKAGE", "matches": meta_leaks})

    status = "PASS"
    if findings:
        status = "FAIL"
    elif downstream_sync_required:
        status = "PASS_WITH_CLASS_B_SYNC_CHECKLIST"

    return {
        "status": status,
        "mode": "curated_salience",
        "after_token_count": len(after_toks),
        "declared_omitted_token_count": len(omitted_toks),
        "undeclared_drops": undeclared_drops,
        "class_b_downstream_sync_checklist": downstream_sync_required,
        "findings": findings,
    }


def extract_authoritative_spine_texts(spine: dict[str, Any]) -> list[str]:
    """Extract verified upstream/display/memory texts from a spine object without neighbor/target contamination."""
    texts: list[str] = []
    for val in spine.get("display_inventory", {}).values():
        texts.append(str(val))
    texts.extend(str(x) for x in spine.get("methods_and_identification_locks", []))
    texts.extend(str(x) for x in spine.get("supplement_evidence_anchors", []))
    framing = spine.get("research_framing_contract", {})
    if isinstance(framing, dict):
        texts.extend(str(x) for x in framing.get("locked_questions_and_goals", []))
        texts.extend(str(x) for x in framing.get("gap_and_motivation", []))
    texts.extend(str(x) for x in spine.get("inference_boundaries_and_nonclaims", []))
    ext = spine.get("external_memory", {})
    if isinstance(ext, dict):
        for k in ("state_locks", "paper_claims", "paper_figures"):
            texts.extend(str(x) for x in ext.get(k, []))
    return texts


def read_source_file_text(path: Path) -> str:
    """Read authoritative source/companion text, using structured extraction for .docx and .tex."""
    if not path.is_file():
        raise FileNotFoundError(f"Source file not found: {path}")
    if path.suffix.lower() in {".docx", ".tex"}:
        blocks, _, _ = load_manuscript_blocks(path)
        annotate_manuscript_blocks(blocks)
        parts = [
            chunk
            for b in blocks
            if (chunk := f"{b.get('caption', '')}\n{b['text']}".strip())
        ]
        return "\n\n".join(parts)
    return path.read_text(encoding="utf-8", errors="replace")


def _load_source_bundle(source_paths: list[Path], spine_path: Path | None) -> tuple[list[str], list[dict[str, Any]]]:
    texts: list[str] = []
    deps: list[dict[str, Any]] = []
    for sp in source_paths:
        texts.append(read_source_file_text(sp))
    if spine_path is not None:
        if not spine_path.is_file():
            raise FileNotFoundError(f"Spine file not found: {spine_path}")
        raw = json.loads(spine_path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError(f"Spine file must contain a JSON object: {spine_path}")
        spine = raw.get("spine", raw if "display_inventory" in raw else {})
        meta = raw.get("meta", {})
        if isinstance(meta, dict):
            if isinstance(meta.get("downstream_dependencies"), list):
                deps.extend(meta["downstream_dependencies"])
            rel_slices = meta.get("relevant_display_slices")
            if isinstance(rel_slices, dict):
                texts.extend(str(v) for v in rel_slices.values())
        if isinstance(spine, dict):
            if isinstance(spine.get("downstream_empirical_dependencies"), list):
                deps.extend(spine["downstream_empirical_dependencies"])
            texts.extend(extract_authoritative_spine_texts(spine))
        if not spine and isinstance(raw.get("envelope"), str):
            env_str = raw["envelope"]
            cut_m = re.search(r"\n8\.\s+IMMEDIATE NEIGHBORING CONTEXT", env_str)
            texts.append(env_str[:cut_m.start()] if cut_m else env_str)
    return texts, deps


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("strict_preservation", "curated_salience"), default="curated_salience")
    parser.add_argument("--before", type=Path, default=None, help="Original target passage file (required for strict_preservation and Mode R)")
    parser.add_argument("--after", type=Path, default=None, help="Revised prose text file")
    parser.add_argument("--reply-json", type=Path, default=None, help="Structured Agent B JSON reply containing revised_target_prose and declared_omitted_to_display")
    parser.add_argument("--source", type=Path, nargs="*", default=[], help="Authoritative table/CSV/text source files")
    parser.add_argument("--spine", type=Path, default=None, help="Spine or envelope JSON produced by build_context_envelope.py")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON report")
    args = parser.parse_args(argv)

    try:
        for sp in args.source:
            if not sp.is_file():
                raise FileNotFoundError(f"Source file not found: {sp}")
        if args.spine is not None and not args.spine.is_file():
            raise FileNotFoundError(f"Spine file not found: {args.spine}")
        if args.before is not None and not args.before.is_file():
            raise FileNotFoundError(f"--before file not found: {args.before}")
        before_text = args.before.read_text(encoding="utf-8") if args.before is not None else None
        declared_omitted: list[Any] = []
        sync_alerts: list[Any] = []
        if args.reply_json is not None:
            if not args.reply_json.is_file():
                raise FileNotFoundError(f"--reply-json file not found: {args.reply_json}")
            reply_obj = json.loads(args.reply_json.read_text(encoding="utf-8"))
            if not isinstance(reply_obj, dict):
                raise ValueError("--reply-json root must be a JSON object")
            raw_prose = reply_obj.get("revised_target_prose")
            if raw_prose is None:
                after_text = ""
            elif isinstance(raw_prose, str):
                after_text = raw_prose
            else:
                raise ValueError("revised_target_prose in --reply-json must be a string")
            raw_omitted = reply_obj.get("declared_omitted_to_display")
            if raw_omitted is None:
                declared_omitted = []
            elif isinstance(raw_omitted, list):
                declared_omitted = list(raw_omitted)
            else:
                raise ValueError("declared_omitted_to_display in --reply-json must be a list or null")
            raw_alerts = reply_obj.get("cross_section_sync_alerts")
            if raw_alerts is None:
                sync_alerts = []
            elif isinstance(raw_alerts, list):
                sync_alerts = list(raw_alerts)
            else:
                raise ValueError("cross_section_sync_alerts in --reply-json must be a list or null")
        elif args.after is not None:
            if not args.after.is_file():
                raise FileNotFoundError(f"--after file not found: {args.after}")
            after_text = args.after.read_text(encoding="utf-8")
        else:
            raise ValueError("Provide either --after <prose.txt> or --reply-json <reply.json>")

        if args.mode == "strict_preservation":
            if before_text is None:
                raise ValueError("--before is required for --mode strict_preservation")
            report = verify_strict_preservation(before_text, after_text)
        else:
            source_texts, deps = _load_source_bundle(args.source, args.spine)
            report = verify_curated_salience(
                after_text=after_text,
                source_texts=source_texts,
                before_text=before_text,
                declared_omitted_to_display=declared_omitted,
                downstream_dependencies=deps,
                cross_section_sync_alerts=sync_alerts,
            )

        if args.as_json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(f"{report['status']} ({report['mode']}): {len(report['findings'])} finding(s)")
            for item in report["findings"]:
                print(f"  - {item['code']}: {json.dumps(item, ensure_ascii=False)}")
        return 0 if report["status"].startswith("PASS") else 1
    except (OSError, ValueError, json.JSONDecodeError, BadZipFile, ET.ParseError, KeyError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
