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


def _extract_float_pair(args: list[ast.AST]) -> tuple[float, float] | None:
    if len(args) < 2:
        return None
    pair: list[float] = []
    for arg in args[:2]:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, (int, float)):
            pair.append(float(arg.value))
        elif isinstance(arg, ast.UnaryOp) and isinstance(arg.op, ast.USub) and isinstance(arg.operand, ast.Constant):
            pair.append(-float(arg.operand.value))
        else:
            return None
    return (pair[0], pair[1])


def _extract_target_names(target: ast.AST) -> list[str]:
    if isinstance(target, ast.Name):
        return [target.id]
    if isinstance(target, (ast.Tuple, ast.List)):
        names: list[str] = []
        for elt in target.elts:
            names.extend(_extract_target_names(elt))
        return names
    return []


def _check_paired_ylim_in_scope(stmts: list[ast.stmt], lines: list[str], artifact: str) -> list[dict[str, Any]]:
    """Compare final set_ylim values only among distinct axes belonging to the same subplots group/figure."""
    findings: list[dict[str, Any]] = []
    axis_groups: list[set[str]] = []
    ax_to_group: dict[str, int] = {}
    final_ylim: dict[str, tuple[int, float, float]] = {}
    ylabels: dict[str, str] = {}

    def register_group(names: list[str]) -> None:
        if len(names) < 2:
            return
        idx = len(axis_groups)
        axis_groups.append(set(names))
        for name in names:
            ax_to_group[name] = idx

    def walk_scope(nodes: list[ast.stmt]) -> None:
        fig_axes: dict[str, list[str]] = {}
        for stmt in nodes:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Call):
                call = stmt.value
                attr = call.func.attr if isinstance(call.func, ast.Attribute) else None
                if attr == "subplots" and len(stmt.targets) == 1:
                    target = stmt.targets[0]
                    if isinstance(target, (ast.Tuple, ast.List)) and len(target.elts) == 2:
                        ax_names = _extract_target_names(target.elts[1])
                        register_group(ax_names)
                elif attr in {"add_subplot", "add_axes"} and len(stmt.targets) == 1 and isinstance(call.func.value, ast.Name):
                    fig_var = call.func.value.id
                    fig_axes.setdefault(fig_var, []).extend(_extract_target_names(stmt.targets[0]))
            for node in ast.walk(stmt):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) or not isinstance(node, ast.Call):
                    continue
                if not isinstance(node.func, ast.Attribute) or not isinstance(node.func.value, ast.Name):
                    continue
                receiver = node.func.value.id
                attr = node.func.attr
                line_text = lines[node.lineno - 1] if 0 < node.lineno <= len(lines) else ""
                if attr == "set_ylabel" and node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    ylabels[receiver] = node.args[0].value
                elif attr == "set_ylim" and "# intentional-ylim-diff" not in line_text:
                    pair = _extract_float_pair(node.args)
                    if pair is not None:
                        final_ylim[receiver] = (node.lineno, pair[0], pair[1])
            if hasattr(stmt, "body") and isinstance(stmt.body, list):
                walk_scope(stmt.body)
            if hasattr(stmt, "orelse") and isinstance(stmt.orelse, list):
                walk_scope(stmt.orelse)
        for axes_list in fig_axes.values():
            register_group(axes_list)

    walk_scope(stmts)
    for group in axis_groups:
        paired = {ax: final_ylim[ax] for ax in sorted(group) if ax in final_ylim}
        if len(paired) < 2:
            continue
        distinct_limits = {(lo, hi) for _, lo, hi in paired.values()}
        distinct_labels = {ylabels[ax] for ax in paired if ax in ylabels}
        if len(distinct_limits) > 1 and len(distinct_labels) <= 1:
            first_line = min(lineno for lineno, _, _ in paired.values())
            details = [(ax, lo, hi) for ax, (_, lo, hi) in paired.items()]
            findings.append({
                "code": "FIG005", "artifact": artifact, "line": first_line,
                "message": f"mismatched set_ylim across paired sibling axes {details}; match limits or mark # intentional-ylim-diff",
            })
    return findings


def lint_python_script(path: Path) -> list[dict[str, Any]]:
    """Inspect a Python plotting script AST for baked-in titles, inside legends, glyph traps, and paired y-axis drift."""
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

    findings.extend(_check_paired_ylim_in_scope(tree.body, lines, str(path)))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            findings.extend(_check_paired_ylim_in_scope(node.body, lines, str(path)))

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
