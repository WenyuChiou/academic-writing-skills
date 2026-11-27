#!/usr/bin/env python3
"""Static linter for Matplotlib figure scripts and exported PNG dimensions."""

from __future__ import annotations

import argparse
import ast
import json
import re
import struct
from pathlib import Path
from typing import Any


CUR_MINUS_RE = re.compile(r"\$-(?=[0-9])")


def _literal_number_list(node: ast.AST) -> list[float] | None:
    if not isinstance(node, (ast.List, ast.Tuple)):
        return None
    values: list[float] = []
    for elt in node.elts:
        if isinstance(elt, ast.Constant) and isinstance(elt.value, (int, float)):
            values.append(float(elt.value))
        elif isinstance(elt, ast.UnaryOp) and isinstance(elt.op, ast.USub) and isinstance(elt.operand, ast.Constant):
            values.append(-float(elt.operand.value))
        else:
            return None
    return values if len(values) >= 4 else None


def lint_python_script(path: Path) -> list[dict[str, Any]]:
    """Inspect a Python plotting script AST for baked-in titles, inside legends, glyph traps, and y-axis drift."""
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    tree = ast.parse(source, filename=str(path))
    findings: list[dict[str, Any]] = []
    uses_jhenghei = "Microsoft JhengHei" in source
    has_unicode_minus_false = bool(re.search(
        r"unicode_minus[\"']?\s*\]\s*=\s*False"
        r"|[\"']axes\.unicode_minus[\"']\s*:\s*False"
        r"|unicode_minus\s*=\s*False",
        source,
    ))
    has_plt_plot = ".savefig(" in source or "plt.subplots" in source or "plt.figure" in source

    if has_plt_plot and not has_unicode_minus_false:
        findings.append({
            "code": "FIG003", "artifact": str(path), "line": 1,
            "message": "plotting script does not explicitly set axes.unicode_minus = False",
        })

    if uses_jhenghei:
        for lineno, line in enumerate(lines, start=1):
            if "\u2264" in line and r"\leq" not in line and "# allow-raw-leq" not in line:
                findings.append({
                    "code": "FIG003", "artifact": str(path), "line": lineno,
                    "message": "raw Unicode U+2264 used with Microsoft JhengHei; use mathtext r'$\\leq$' to prevent missing-glyph boxes",
                })

    ylim_records: list[tuple[int, str, float, float]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if CUR_MINUS_RE.search(node.value):
                findings.append({
                    "code": "FIG003", "artifact": str(path), "line": node.lineno,
                    "message": f"misplaced minus after dollar sign in string: {node.value!r}",
                })
        if not isinstance(node, ast.Call):
            continue
        line_text = lines[node.lineno - 1] if 0 < node.lineno <= len(lines) else ""
        attr = node.func.attr if isinstance(node.func, ast.Attribute) else None
        receiver = node.func.value.id if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) else ""

        if attr in {"suptitle", "set_title"} and "# intentional-title" not in line_text:
            findings.append({
                "code": "FIG001", "artifact": str(path), "line": node.lineno,
                "message": f"baked-in figure/axis title via .{attr}(); move title to manuscript caption",
            })

        if attr == "legend" and receiver != "fig" and "# intentional-legend" not in line_text:
            has_outside_anchor = any(kw.arg == "bbox_to_anchor" for kw in node.keywords)
            if not has_outside_anchor:
                findings.append({
                    "code": "FIG002", "artifact": str(path), "line": node.lineno,
                    "message": f"inside-axes {receiver or 'ax'}.legend() may cover data; place outside axes or use fig.legend(...)",
                })

        if attr in {"set_yticks", "set_xticks"} and node.args and "# intentional-ticks" not in line_text:
            ticks = _literal_number_list(node.args[0])
            if ticks:
                ordered = sorted(ticks)
                gaps = [round(b - a, 9) for a, b in zip(ordered, ordered[1:]) if b > a]
                if len(gaps) >= 3:
                    hi_gap = max(gaps)
                    if hi_gap > 0 and min(gaps) <= 0.55 * hi_gap:
                        findings.append({
                            "code": "FIG004", "artifact": str(path), "line": node.lineno,
                            "message": f"uneven close neighbor ticks {ordered}; remove neighbor tick colliding with reference cutoff",
                        })

        if attr == "set_ylim" and len(node.args) >= 2 and "# intentional-ylim-diff" not in line_text:
            pair: list[float] = []
            for arg in node.args[:2]:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, (int, float)):
                    pair.append(float(arg.value))
                elif isinstance(arg, ast.UnaryOp) and isinstance(arg.op, ast.USub) and isinstance(arg.operand, ast.Constant):
                    pair.append(-float(arg.operand.value))
            if len(pair) == 2:
                ylim_records.append((node.lineno, receiver or "ax", pair[0], pair[1]))

    if len(ylim_records) >= 2 and "# intentional-ylim-diff" not in source:
        distinct = {(lo, hi) for _, _, lo, hi in ylim_records}
        if len(distinct) > 1:
            findings.append({
                "code": "FIG005", "artifact": str(path), "line": ylim_records[0][0],
                "message": f"mismatched set_ylim across sibling axes {[ (r, lo, hi) for _, r, lo, hi in ylim_records ]}; match paired limits or mark # intentional-ylim-diff",
            })

    return findings


def lint_png_file(path: Path, min_width: int = 900) -> list[dict[str, Any]]:
    """Verify PNG header and ensure raster width meets publication clarity threshold."""
    header = path.read_bytes()[:24]
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        return [{"code": "FIG006", "artifact": str(path), "message": "not a valid PNG file"}]
    width, height = struct.unpack(">II", header[16:24])
    if width < min_width:
        return [{
            "code": "FIG006", "artifact": str(path), "width": width, "height": height,
            "message": f"PNG width {width}px is below recommended minimum {min_width}px",
        }]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help=".py scripts or .png figures")
    parser.add_argument("--min-width", type=int, default=900)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    findings: list[dict[str, Any]] = []
    for item in args.paths:
        suffix = item.suffix.lower()
        if suffix == ".py":
            findings.extend(lint_python_script(item))
        elif suffix == ".png":
            findings.extend(lint_png_file(item, args.min_width))

    result = {"status": "FINDINGS" if findings else "PASS", "findings": findings}
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"{result['status']}: {len(findings)} finding(s)")
        for item in findings:
            print(f"{item['code']}: {item['message']} ({item['artifact']})")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
