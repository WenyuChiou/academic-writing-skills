#!/usr/bin/env python3
"""Report observable repetition and stock-prose patterns in manuscript artifacts."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from audit_text_consistency import extract_text


TOKEN_RE = re.compile(r"[A-Za-z]+(?:['’-][A-Za-z]+)*")
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "being", "but", "by",
    "for", "from", "had", "has", "have", "in", "into", "is", "it", "its", "of",
    "on", "or", "our", "that", "the", "their", "these", "this", "those", "to",
    "was", "were", "which", "while", "with", "within", "we",
}
DEFAULT_STOCK_PHRASES = {
    "it is important to note that",
    "it is worth noting that",
    "it should be noted that",
    "in today's rapidly evolving",
    "plays a crucial role",
    "this underscores the importance of",
    "in the realm of",
    "a myriad of",
    "delve into",
}


def tokens(text: str) -> list[str]:
    return [match.group(0).casefold().replace("’", "'") for match in TOKEN_RE.finditer(text)]


def normalized(text: str) -> str:
    return " ".join(tokens(text))


def sentences(text: str) -> list[str]:
    flattened = re.sub(r"\s+", " ", text).strip()
    return [item.strip() for item in re.split(r"(?<=[.!?])\s+", flattened) if item.strip()]


def protected_phrases(state: dict[str, Any]) -> set[str]:
    profile = state.get("style_profile", {})
    values = list(profile.get("protected_terms", [])) + list(profile.get("allowed_repetitions", []))
    values.extend(item.get("preferred", "") for item in state.get("terminology", []))
    return {normalized(str(value)) for value in values if normalized(str(value))}


def phrase_is_protected(phrase: str, protected: set[str]) -> bool:
    return any(item == phrase or item in phrase for item in protected)


def audit_text(text: str, artifact: str, state: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    profile = state.get("style_profile", {})
    protected = protected_phrases(state)
    protected_words = {word for phrase in protected for word in phrase.split()}
    sentence_list = sentences(text)
    sentence_tokens = [tokens(item) for item in sentence_list]

    normalized_sentences = [" ".join(item) for item in sentence_tokens if len(item) >= 8]
    for sentence, count in Counter(normalized_sentences).most_common():
        if count < 2:
            break
        findings.append({
            "code": "PROSE001", "artifact": artifact, "match": sentence,
            "count": count, "message": "exact or punctuation-only sentence repetition",
        })

    opening_words = max(2, int(profile.get("sentence_opening_words", 4)))
    openings: defaultdict[str, set[int]] = defaultdict(set)
    for index, item in enumerate(sentence_tokens):
        if len(item) >= opening_words:
            openings[" ".join(item[:opening_words])].add(index)
    for opening, locations in sorted(openings.items(), key=lambda pair: (-len(pair[1]), pair[0])):
        if len(locations) >= 3 and not phrase_is_protected(opening, protected):
            findings.append({
                "code": "PROSE002", "artifact": artifact, "match": opening,
                "count": len(locations), "message": "repeated sentence opening",
            })

    stock_phrases = DEFAULT_STOCK_PHRASES | {
        normalized(str(value)) for value in profile.get("discouraged_phrases", [])
    }
    lowered = normalized(text)
    for phrase in sorted(item for item in stock_phrases if item):
        count = len(re.findall(rf"(?<!\w){re.escape(phrase)}(?!\w)", lowered))
        if count:
            findings.append({
                "code": "PROSE003", "artifact": artifact, "match": phrase,
                "count": count, "message": "stock or project-discouraged phrase; inspect in context",
            })

    phrase_words = max(4, int(profile.get("phrase_words", 5)))
    minimum = max(2, int(profile.get("phrase_min_occurrences", 3)))
    phrase_locations: defaultdict[str, set[int]] = defaultdict(set)
    for sentence_index, item in enumerate(sentence_tokens):
        for start in range(0, len(item) - phrase_words + 1):
            gram = item[start:start + phrase_words]
            phrase = " ".join(gram)
            if sum(word not in STOPWORDS for word in gram) < 2:
                continue
            if phrase_is_protected(phrase, protected):
                continue
            phrase_locations[phrase].add(sentence_index)
    for phrase, locations in sorted(phrase_locations.items(), key=lambda pair: (-len(pair[1]), pair[0])):
        if len(locations) >= minimum:
            findings.append({
                "code": "PROSE004", "artifact": artifact, "match": phrase,
                "count": len(locations), "message": "repeated multiword phrase across sentences",
            })

    all_tokens = tokens(text)
    eligible = [
        word for word in all_tokens
        if len(word) >= 4 and word not in STOPWORDS and word not in protected_words
    ]
    threshold = max(8, math.ceil(len(all_tokens) * 0.02))
    for word, count in Counter(eligible).most_common(10):
        if count < threshold:
            break
        findings.append({
            "code": "PROSE005", "artifact": artifact, "match": word,
            "count": count, "message": "candidate nontechnical word overuse; preserve it if conceptually required",
        })
    return findings


def audit(state: dict[str, Any], project_root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for item in state.get("artifacts", []):
        if item.get("status") != "ACTIVE" or not item.get("path"):
            continue
        path = (project_root / item["path"]).resolve()
        artifact = str(item.get("id", item["path"]))
        try:
            findings.extend(audit_text(extract_text(path), artifact, state))
        except (OSError, ValueError) as exc:
            findings.append({"code": "PROSE000", "artifact": artifact, "message": str(exc)})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    state_path = Path(args.state).expanduser().resolve()
    root = Path(args.project_root).expanduser().resolve() if args.project_root else state_path.parent
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
        findings = audit(state, root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        findings = [{"code": "PROSE000", "artifact": "project", "message": str(exc)}]
    result = {"status": "FINDINGS" if findings else "PASS", "findings": findings}
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"{result['status']}: {len(findings)} finding(s)")
        for item in findings:
            print(f"{item['code']}: {item['message']} ({item.get('match', item.get('artifact', 'project'))})")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
