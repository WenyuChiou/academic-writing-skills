#!/usr/bin/env python3
"""Static linter for Matplotlib figure scripts and exported PNG dimensions."""

from __future__ import annotations

import argparse
import ast
import json
import math
import re
import struct
from pathlib import Path
from typing import Any


NONLINEAR_SCALES = {"log", "symlog", "logit", "function", "functionlog"}


CUR_MINUS_RE = re.compile(r"\$-(?=[0-9])")
VALID_NEGATIVE_MATHTEXT_RE = re.compile(
    r"(?<!\\)\$-[0-9]+(?:\.[0-9]+)?(?:\s*[-+*/^_=<>\\][A-Za-z0-9{}\\]*)*\$"
)


_SKIP_EXPR_CHILDREN = (
    (ast.stmt, ast.excepthandler, ast.match_case)
    if hasattr(ast, "match_case")
    else (ast.stmt, ast.excepthandler)
)


def _iter_expr_calls(node: ast.AST):
    """Yield Call AST nodes within a single statement's expressions without descending into nested statements or defs."""
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return
    if isinstance(node, ast.Call):
        yield node
    for child in ast.iter_child_nodes(node):
        if isinstance(child, _SKIP_EXPR_CHILDREN):
            continue
        yield from _iter_expr_calls(child)


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
    """Compare final set_ylim values only among distinct axes belonging to the same subplots group/figure instance."""
    findings: list[dict[str, Any]] = []
    axis_groups: list[list[tuple[int, str]]] = []
    final_ylim: dict[int, tuple[int, float, float]] = {}
    ylabels: dict[int, str] = {}
    current_axis: dict[str, int] = {}
    current_fig: dict[str, int] = {}
    fig_axes: dict[int, list[tuple[int, str]]] = {}
    next_id = 0

    def alloc_id() -> int:
        nonlocal next_id
        next_id += 1
        return next_id

    def bind_axes(names: list[str], in_group: bool = False, fig_id: int | None = None) -> None:
        pairs: list[tuple[int, str]] = []
        for name in names:
            ax_id = alloc_id()
            current_axis[name] = ax_id
            pairs.append((ax_id, name))
        if in_group and len(pairs) >= 2:
            axis_groups.append(pairs)
        if fig_id is not None:
            fig_axes.setdefault(fig_id, []).extend(pairs)

    def walk_scope(nodes: list[ast.stmt]) -> None:
        for stmt in nodes:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.value, ast.Call):
                call = stmt.value
                attr = call.func.attr if isinstance(call.func, ast.Attribute) else None
                target = stmt.targets[0]
                if attr == "subplots":
                    if isinstance(target, (ast.Tuple, ast.List)) and len(target.elts) == 2:
                        for fn in _extract_target_names(target.elts[0]):
                            current_fig[fn] = alloc_id()
                        bind_axes(_extract_target_names(target.elts[1]), in_group=True)
                elif attr == "figure":
                    for fn in _extract_target_names(target):
                        current_fig[fn] = alloc_id()
                elif attr in {"add_subplot", "add_axes"} and isinstance(call.func.value, ast.Name):
                    fig_var = call.func.value.id
                    fig_id = current_fig.setdefault(fig_var, alloc_id())
                    bind_axes(_extract_target_names(target), fig_id=fig_id)
                else:
                    for name in _extract_target_names(target):
                        current_axis.pop(name, None)
            elif isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    for name in _extract_target_names(target):
                        current_axis.pop(name, None)
            def inspect_calls(root_node: ast.AST) -> None:
                for node in _iter_expr_calls(root_node):
                    if not isinstance(node.func, ast.Attribute) or not isinstance(node.func.value, ast.Name):
                        continue
                    receiver = node.func.value.id
                    ax_id = current_axis.get(receiver)
                    if ax_id is None:
                        continue
                    attr = node.func.attr
                    line_text = lines[node.lineno - 1] if 0 < node.lineno <= len(lines) else ""
                    if attr == "set_ylabel" and node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                        ylabels[ax_id] = node.args[0].value
                    elif attr == "set_ylim" and "# intentional-ylim-diff" not in line_text:
                        pair = _extract_float_pair(node.args)
                        if pair is not None:
                            final_ylim[ax_id] = (node.lineno, pair[0], pair[1])

            inspect_calls(stmt)
            if hasattr(stmt, "body") and isinstance(stmt.body, list):
                walk_scope(stmt.body)
            if hasattr(stmt, "orelse") and isinstance(stmt.orelse, list):
                walk_scope(stmt.orelse)
            for handler in getattr(stmt, "handlers", []):
                if getattr(handler, "type", None) is not None:
                    inspect_calls(handler.type)
                if hasattr(handler, "body") and isinstance(handler.body, list):
                    walk_scope(handler.body)
            if hasattr(stmt, "finalbody") and isinstance(stmt.finalbody, list):
                walk_scope(stmt.finalbody)
            for case in getattr(stmt, "cases", []):
                if getattr(case, "guard", None) is not None:
                    inspect_calls(case.guard)
                if hasattr(case, "body") and isinstance(case.body, list):
                    walk_scope(case.body)

    walk_scope(stmts)
    for fig_group in fig_axes.values():
        if len(fig_group) >= 2:
            axis_groups.append(fig_group)
    for group in axis_groups:
        paired = [(ax_id, name, final_ylim[ax_id]) for ax_id, name in group if ax_id in final_ylim]
        if len(paired) < 2:
            continue
        distinct_limits = {(lo, hi) for _, _, (_, lo, hi) in paired}
        distinct_labels = {ylabels[ax_id] for ax_id, _, _ in paired if ax_id in ylabels}
        if len(distinct_limits) > 1 and len(distinct_labels) <= 1:
            first_line = min(lineno for _, _, (lineno, _, _) in paired)
            details = [(name, lo, hi) for _, name, (_, lo, hi) in paired]
            findings.append({
                "code": "FIG005", "artifact": artifact, "line": first_line,
                "message": f"mismatched set_ylim across paired sibling axes {details}; match limits or mark # intentional-ylim-diff",
            })
    return findings


def _lint_legends_in_scope(
    nodes: list[ast.stmt], lines: list[str], artifact: str, fig_vars: set[str] | None = None
) -> list[dict[str, Any]]:
    """Track current figure-bound variable names lexically so reassigned axis vars trigger FIG002."""
    current_fig_vars = set(fig_vars) if fig_vars is not None else {"fig"}
    findings: list[dict[str, Any]] = []

    def walk(stmts: list[ast.stmt], active_figs: set[str]) -> None:
        for stmt in stmts:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                walk(stmt.body, set(active_figs) | {"fig"})
                continue
            def inspect_legend_calls(root_node: ast.AST, figs: set[str]) -> None:
                for node in _iter_expr_calls(root_node):
                    if not isinstance(node.func, ast.Attribute):
                        continue
                    attr = node.func.attr
                    receiver = node.func.value.id if isinstance(node.func.value, ast.Name) else ""
                    line_text = lines[node.lineno - 1] if 0 < node.lineno <= len(lines) else ""
                    if attr == "legend" and receiver not in figs and "# intentional-legend" not in line_text:
                        if not any(kw.arg == "bbox_to_anchor" for kw in node.keywords):
                            findings.append({
                                "code": "FIG002", "artifact": artifact, "line": node.lineno,
                                "message": f"inside-axes {receiver or 'ax'}.legend() may cover data; place outside axes or use fig.legend(...)",
                            })

            inspect_legend_calls(stmt, active_figs)
            if isinstance(stmt, ast.Assign):
                for t in stmt.targets:
                    for name in _extract_target_names(t):
                        active_figs.discard(name)
                if len(stmt.targets) == 1 and isinstance(stmt.value, ast.Call):
                    func = stmt.value.func
                    attr = func.attr if isinstance(func, ast.Attribute) else (func.id if isinstance(func, ast.Name) else None)
                    target = stmt.targets[0]
                    if attr == "figure":
                        active_figs.update(_extract_target_names(target))
                    elif attr == "subplots" and isinstance(target, (ast.Tuple, ast.List)) and len(target.elts) == 2:
                        active_figs.update(_extract_target_names(target.elts[0]))
            elif isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                active_figs.discard(stmt.target.id)
                if isinstance(stmt.value, ast.Call):
                    func = stmt.value.func
                    attr = func.attr if isinstance(func, ast.Attribute) else (func.id if isinstance(func, ast.Name) else None)
                    if attr == "figure":
                        active_figs.add(stmt.target.id)
            if hasattr(stmt, "body") and isinstance(stmt.body, list):
                walk(stmt.body, active_figs)
            if hasattr(stmt, "orelse") and isinstance(stmt.orelse, list):
                walk(stmt.orelse, active_figs)
            for handler in getattr(stmt, "handlers", []):
                if getattr(handler, "type", None) is not None:
                    inspect_legend_calls(handler.type, active_figs)
                if hasattr(handler, "body") and isinstance(handler.body, list):
                    walk(handler.body, active_figs)
            if hasattr(stmt, "finalbody") and isinstance(stmt.finalbody, list):
                walk(stmt.finalbody, active_figs)
            for case in getattr(stmt, "cases", []):
                if getattr(case, "guard", None) is not None:
                    inspect_legend_calls(case.guard, active_figs)
                if hasattr(case, "body") and isinstance(case.body, list):
                    walk(case.body, active_figs)

    walk(nodes, current_fig_vars)
    return findings


def _call_name(call: ast.Call) -> tuple[str | None, str]:
    if isinstance(call.func, ast.Attribute):
        receiver = call.func.value.id if isinstance(call.func.value, ast.Name) else ""
        return call.func.attr, receiver
    if isinstance(call.func, ast.Name):
        return call.func.id, ""
    return None, ""


def _extract_scale_arg(call: ast.Call) -> str | None:
    arg = call.args[0] if call.args else next((kw.value for kw in call.keywords if kw.arg == "value"), None)
    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
        return arg.value.lower()
    return None


def _subplot_spec_key(call: ast.Call) -> tuple[int, ...] | None:
    if call.keywords:
        return None
    vals: list[int] = []
    for arg in call.args:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, int) and not isinstance(arg.value, bool):
            vals.append(arg.value)
        else:
            return None
    if not vals:
        return (1, 1, 1)
    if len(vals) == 1 and 100 <= vals[0] <= 999:
        v = vals[0]
        return (v // 100, (v // 10) % 10, v % 10)
    return tuple(vals)


def _collect_pyplot_bindings(tree: ast.AST) -> tuple[set[str], set[str]]:
    """Collect imported pyplot module aliases and directly imported pyplot title symbols."""
    pyplot_aliases = {"plt", "pyplot"}
    imported_title_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "matplotlib.pyplot" and alias.asname:
                    pyplot_aliases.add(alias.asname)
        elif isinstance(node, ast.ImportFrom):
            if node.module == "matplotlib":
                for alias in node.names:
                    if alias.name == "pyplot":
                        pyplot_aliases.add(alias.asname or "pyplot")
            elif node.module == "matplotlib.pyplot":
                for alias in node.names:
                    if alias.name in {"title", "suptitle"}:
                        imported_title_names.add(alias.asname or alias.name)
                    elif alias.name == "*":
                        imported_title_names.update({"title", "suptitle"})
    return pyplot_aliases, imported_title_names


def _lint_ticks_in_scope(
    stmts: list[ast.stmt], lines: list[str], artifact: str, pyplot_aliases: set[str] | None = None
) -> list[dict[str, Any]]:
    """Track axis scales per binding lifetime and class/function/module scope to avoid cross-figure leakage."""
    aliases = pyplot_aliases if pyplot_aliases is not None else {"plt", "pyplot"}
    current_axis: dict[str, int] = {}
    current_fig_vars: dict[str, int] = {}
    subplot_slots: dict[tuple[int, tuple[int, ...]], int] = {}
    current_plt_axis: int | None = None
    scale_by_axis: dict[tuple[int, str], str] = {}
    tick_calls: list[tuple[int, int, str, list[float]]] = []
    next_id = 0

    def alloc_id() -> int:
        nonlocal next_id
        next_id += 1
        return next_id

    current_plt_fig = alloc_id()

    def get_axis(name: str) -> int:
        if name not in current_axis:
            current_axis[name] = alloc_id()
        return current_axis[name]

    def ensure_plt_axis() -> int:
        nonlocal current_plt_axis
        if current_plt_axis is None:
            current_plt_axis = alloc_id()
        return current_plt_axis

    def drop_slot(old_id: int | None) -> None:
        if old_id is None:
            return
        for key in [k for k, v in subplot_slots.items() if v == old_id]:
            subplot_slots.pop(key, None)

    def resolve_subplot_axis(call: ast.Call, receiver: str) -> int:
        fig_id = (
            current_fig_vars.setdefault(receiver, alloc_id())
            if receiver and receiver not in aliases
            else current_plt_fig
        )
        spec = _subplot_spec_key(call)
        if spec is not None:
            key = (fig_id, spec)
            if key not in subplot_slots:
                subplot_slots[key] = alloc_id()
            return subplot_slots[key]
        return alloc_id()

    def bind_new_axes(names: list[str], reset_plt: bool = False) -> None:
        nonlocal current_plt_axis
        created: list[int] = []
        for name in names:
            ax_id = alloc_id()
            current_axis[name] = ax_id
            created.append(ax_id)
        if reset_plt:
            current_plt_axis = created[-1] if created else alloc_id()
        elif created:
            current_plt_axis = created[-1]

    def inspect_expr(root_node: ast.AST, skip_call: ast.Call | None = None) -> None:
        nonlocal current_plt_axis, current_plt_fig
        for node in _iter_expr_calls(root_node):
            if node is skip_call:
                continue
            attr, receiver = _call_name(node)
            if not attr:
                continue
            is_plt_recv = receiver in aliases
            if attr == "figure":
                current_plt_fig = alloc_id()
                current_plt_axis = None
            elif attr == "clf":
                if receiver and not is_plt_recv:
                    current_fig_vars[receiver] = alloc_id()
                else:
                    current_plt_fig = alloc_id()
                current_plt_axis = None
            elif attr == "subplot":
                current_plt_axis = resolve_subplot_axis(node, receiver)
            elif attr in {"subplots", "add_subplot"}:
                if attr == "subplots":
                    current_plt_fig = alloc_id()
                current_plt_axis = alloc_id()
            elif attr == "axes":
                current_plt_axis = alloc_id()
            elif attr == "cla":
                if receiver and not is_plt_recv:
                    drop_slot(current_axis.get(receiver))
                    current_axis[receiver] = alloc_id()
                else:
                    drop_slot(current_plt_axis)
                    current_plt_axis = alloc_id()
            elif attr in {"set_xscale", "set_yscale"} and receiver:
                scale_val = _extract_scale_arg(node)
                if scale_val is not None:
                    scale_by_axis[(get_axis(receiver), "x" if attr == "set_xscale" else "y")] = scale_val
            elif attr in {"xscale", "yscale"}:
                scale_val = _extract_scale_arg(node)
                if scale_val is not None:
                    scale_by_axis[(ensure_plt_axis(), "x" if attr == "xscale" else "y")] = scale_val
            elif attr in {"semilogx", "semilogy", "loglog"}:
                ax_id = (
                    get_axis(receiver)
                    if receiver and not is_plt_recv
                    else ensure_plt_axis()
                )
                if attr in {"semilogx", "loglog"}:
                    scale_by_axis[(ax_id, "x")] = "log"
                if attr in {"semilogy", "loglog"}:
                    scale_by_axis[(ax_id, "y")] = "log"
            elif attr in {"set_yticks", "set_xticks"} and node.args:
                line_text = lines[node.lineno - 1] if 0 < node.lineno <= len(lines) else ""
                if "# intentional-ticks" in line_text:
                    continue
                ticks = _literal_number_list(node.args[0])
                if ticks:
                    ax_id = get_axis(receiver) if receiver else alloc_id()
                    tick_calls.append((node.lineno, ax_id, "x" if attr == "set_xticks" else "y", ticks))
            elif attr in {"yticks", "xticks"} and node.args and (is_plt_recv or not receiver):
                line_text = lines[node.lineno - 1] if 0 < node.lineno <= len(lines) else ""
                if "# intentional-ticks" in line_text:
                    continue
                ticks = _literal_number_list(node.args[0])
                if ticks:
                    tick_calls.append((node.lineno, ensure_plt_axis(), "x" if attr == "xticks" else "y", ticks))

    def walk_scope(nodes: list[ast.stmt]) -> None:
        nonlocal current_plt_axis, current_plt_fig
        for stmt in nodes:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            skip_call: ast.Call | None = None
            if isinstance(stmt, ast.Assign):
                handled_rhs = False
                if len(stmt.targets) == 1 and isinstance(stmt.value, ast.Call):
                    attr, call_recv = _call_name(stmt.value)
                    target = stmt.targets[0]
                    if attr == "subplots":
                        handled_rhs = True
                        skip_call = stmt.value
                        current_plt_fig = alloc_id()
                        if isinstance(target, (ast.Tuple, ast.List)) and len(target.elts) == 2:
                            for fn in _extract_target_names(target.elts[0]):
                                current_axis.pop(fn, None)
                                current_fig_vars[fn] = current_plt_fig
                            bind_new_axes(_extract_target_names(target.elts[1]), reset_plt=True)
                        else:
                            for fn in _extract_target_names(target):
                                current_axis.pop(fn, None)
                                current_fig_vars[fn] = current_plt_fig
                            current_plt_axis = alloc_id()
                    elif attr == "figure":
                        handled_rhs = True
                        skip_call = stmt.value
                        current_plt_fig = alloc_id()
                        for fn in _extract_target_names(target):
                            current_axis.pop(fn, None)
                            current_fig_vars[fn] = current_plt_fig
                        current_plt_axis = None
                    elif attr == "subplot":
                        handled_rhs = True
                        skip_call = stmt.value
                        ax_id = resolve_subplot_axis(stmt.value, call_recv)
                        for name in _extract_target_names(target):
                            current_axis[name] = ax_id
                        current_plt_axis = ax_id
                    elif attr in {"add_subplot", "add_axes", "axes"}:
                        handled_rhs = True
                        skip_call = stmt.value
                        bind_new_axes(_extract_target_names(target), reset_plt=True)
                    elif attr == "gca":
                        handled_rhs = True
                        skip_call = stmt.value
                        plt_ax = ensure_plt_axis()
                        for name in _extract_target_names(target):
                            current_axis[name] = plt_ax
                if not handled_rhs:
                    for t in stmt.targets:
                        for name in _extract_target_names(t):
                            current_axis.pop(name, None)
            elif isinstance(stmt, ast.AnnAssign):
                for name in _extract_target_names(stmt.target):
                    current_axis.pop(name, None)
            inspect_expr(stmt, skip_call=skip_call)
            if hasattr(stmt, "body") and isinstance(stmt.body, list):
                walk_scope(stmt.body)
            if hasattr(stmt, "orelse") and isinstance(stmt.orelse, list):
                walk_scope(stmt.orelse)
            for handler in getattr(stmt, "handlers", []):
                if getattr(handler, "type", None) is not None:
                    inspect_expr(handler.type)
                if hasattr(handler, "body") and isinstance(handler.body, list):
                    walk_scope(handler.body)
            if hasattr(stmt, "finalbody") and isinstance(stmt.finalbody, list):
                walk_scope(stmt.finalbody)
            for case in getattr(stmt, "cases", []):
                if getattr(case, "guard", None) is not None:
                    inspect_expr(case.guard)
                if hasattr(case, "body") and isinstance(case.body, list):
                    walk_scope(case.body)

    walk_scope(stmts)
    findings: list[dict[str, Any]] = []
    for lineno, ax_id, axis_ch, ticks in tick_calls:
        scale = scale_by_axis.get((ax_id, axis_ch), "linear")
        ordered = sorted(ticks)
        if scale == "log":
            if not all(val > 0 for val in ordered):
                continue
            transformed = [math.log10(val) for val in ordered]
        elif scale in NONLINEAR_SCALES:
            continue
        else:
            transformed = ordered
        gaps = [round(b - a, 9) for a, b in zip(transformed, transformed[1:]) if b > a]
        if len(gaps) >= 3:
            hi_gap = max(gaps)
            if hi_gap > 0 and min(gaps) <= 0.55 * hi_gap:
                findings.append({
                    "code": "FIG004", "artifact": artifact, "line": lineno,
                    "message": f"uneven close neighbor ticks {ordered}; remove neighbor tick colliding with reference cutoff",
                })
    return findings


def lint_python_script(path: Path) -> list[dict[str, Any]]:
    """Inspect a Python plotting script AST for baked-in titles, inside legends, glyph traps, and paired y-axis drift."""
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    tree = ast.parse(source, filename=str(path))
    pyplot_aliases, imported_title_names = _collect_pyplot_bindings(tree)
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
            stripped_math = VALID_NEGATIVE_MATHTEXT_RE.sub("", node.value)
            if CUR_MINUS_RE.search(stripped_math):
                findings.append({
                    "code": "FIG003", "artifact": str(path), "line": node.lineno,
                    "message": f"misplaced minus after dollar sign in string: {node.value!r}",
                })
        if not isinstance(node, ast.Call):
            continue
        line_text = lines[node.lineno - 1] if 0 < node.lineno <= len(lines) else ""
        call_name, receiver = _call_name(node)

        is_title_call = (
            (
                isinstance(node.func, ast.Attribute)
                and (
                    call_name in {"suptitle", "set_title"}
                    or (receiver in pyplot_aliases and call_name == "title")
                )
            )
            or (isinstance(node.func, ast.Name) and call_name in imported_title_names)
        )
        if is_title_call and "# intentional-title" not in line_text:
            findings.append({
                "code": "FIG001", "artifact": str(path), "line": node.lineno,
                "message": f"baked-in figure/axis title via .{call_name}(); move title to manuscript caption",
            })

    findings.extend(_lint_ticks_in_scope(tree.body, lines, str(path), pyplot_aliases))
    findings.extend(_lint_legends_in_scope(tree.body, lines, str(path)))
    findings.extend(_check_paired_ylim_in_scope(tree.body, lines, str(path)))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            findings.extend(_lint_ticks_in_scope(node.body, lines, str(path), pyplot_aliases))
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
