#!/usr/bin/env python3
"""Host- and model-agnostic Agent A -> Agent B scoped manuscript pass runner & verifier.

Builds a deterministic <= 4,500-token context envelope (`build_context_envelope.py`),
dispatches to a pluggable Agent B backend (`agy`, `codex`, `claude`, `command`, or
`envelope-only` for host-native subagents), enforces a strict four-field dual-channel
JSON return schema, blocks silent CLI timeouts (`print_timeout` with exit 0), runs
partitioned numeric & downstream Class B orphan verification (`verify_delegate_numbers.py`)
plus candidate prose checks (`audit_candidate_text.py` / `audit_prose_patterns.py`),
writes disk `evidence_refs` with SHA-256 hashes, and emits a <= 200-word compliance receipt.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
from typing import Any
from xml.etree import ElementTree as ET
from zipfile import BadZipFile

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from audit_candidate_text import audit_candidate  # noqa: E402
from audit_prose_patterns import audit_text as audit_prose_text  # noqa: E402
from build_context_envelope import (  # noqa: E402
    build_scoped_context_envelope,
    load_or_build_spine,
    locate_target_blocks,
)
from verify_delegate_numbers import (  # noqa: E402
    extract_authoritative_spine_texts,
    read_source_file_text,
    verify_curated_salience,
    verify_strict_preservation,
)

DELEGATE_RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "revised_target_prose",
        "declared_omitted_to_display",
        "cross_section_sync_alerts",
        "unverified_context_locks",
    ],
    "properties": {
        "revised_target_prose": {
            "type": "string",
            "description": "Complete revised prose for ONLY the authorized target unit (zero editorial meta-questions).",
        },
        "declared_omitted_to_display": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["value_or_entity", "display_ref", "rationale_tier"],
                "properties": {
                    "value_or_entity": {"type": "string"},
                    "display_ref": {"type": "string"},
                    "rationale_tier": {
                        "type": "string",
                        "enum": [
                            "routine_conforming_subscale",
                            "non_shifting_interval",
                            "secondary_wave_or_cell",
                            "other_display_archived",
                        ],
                    },
                },
            },
        },
        "cross_section_sync_alerts": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["affected_section", "severity_class", "issue"],
                "properties": {
                    "affected_section": {"type": "string"},
                    "severity_class": {
                        "type": "string",
                        "enum": ["Class A", "Class B", "Class C", "Class D"],
                    },
                    "issue": {"type": "string"},
                },
            },
        },
        "unverified_context_locks": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
}

BAD_FINISH_REASONS = {
    "print_timeout",
    "timeout",
    "timed_out",
    "max_tokens",
    "length",
    "error",
    "cancelled",
    "canceled",
    "aborted",
}

MODEL_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@-]{0,127}$")
RESUME_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
WINDOWS_BATCH_METACHAR_RE = re.compile(r"[&|<>^%!\r\n]")
WINDOWS_FLAG_QUOTED_RE = re.compile(r'^(-+[A-Za-z0-9_-]+=)(["\'])(.*)\2$')


class BackendExecutionError(RuntimeError):
    """Raised when an Agent B CLI backend times out silently, truncates, or fails."""

    def __init__(self, code: str, message: str, exit_code: int = 2) -> None:
        super().__init__(message)
        self.code = code
        self.exit_code = exit_code


def _sha256_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _word_count(text: str) -> int:
    return len(re.findall(r"\S+", text.strip()))


def validate_delegate_reply_schema(payload: Any) -> list[str]:
    """Deterministic stdlib validation of the 4-field Dual-Channel JSON contract."""
    if not isinstance(payload, dict):
        return ["reply root must be a JSON object"]
    required = set(DELEGATE_RESPONSE_SCHEMA["required"])
    errors: list[str] = []
    missing = sorted(required - set(payload.keys()))
    extra = sorted(set(payload.keys()) - required)
    if missing:
        errors.append(f"missing required keys: {missing}")
    if extra:
        errors.append(f"unexpected keys not allowed: {extra}")
    if "revised_target_prose" in payload and not isinstance(payload["revised_target_prose"], str):
        errors.append("revised_target_prose must be a string")
    if "revised_target_prose" in payload and isinstance(payload["revised_target_prose"], str):
        if not payload["revised_target_prose"].strip():
            errors.append("revised_target_prose must not be empty")

    if "declared_omitted_to_display" in payload:
        arr = payload["declared_omitted_to_display"]
        if not isinstance(arr, list):
            errors.append("declared_omitted_to_display must be an array")
        else:
            allowed_tiers = {
                "routine_conforming_subscale",
                "non_shifting_interval",
                "secondary_wave_or_cell",
                "other_display_archived",
            }
            for idx, item in enumerate(arr):
                if not isinstance(item, dict) or set(item.keys()) != {"value_or_entity", "display_ref", "rationale_tier"}:
                    errors.append(f"declared_omitted_to_display[{idx}] must have exact keys value_or_entity, display_ref, rationale_tier")
                    continue
                if not all(isinstance(item[k], str) and item[k].strip() for k in ("value_or_entity", "display_ref", "rationale_tier")):
                    errors.append(f"declared_omitted_to_display[{idx}] fields must be non-empty strings")
                elif item["rationale_tier"] not in allowed_tiers:
                    errors.append(f"declared_omitted_to_display[{idx}] invalid rationale_tier: {item['rationale_tier']}")

    if "cross_section_sync_alerts" in payload:
        arr = payload["cross_section_sync_alerts"]
        if not isinstance(arr, list):
            errors.append("cross_section_sync_alerts must be an array")
        else:
            for idx, item in enumerate(arr):
                if not isinstance(item, dict) or set(item.keys()) != {"affected_section", "severity_class", "issue"}:
                    errors.append(f"cross_section_sync_alerts[{idx}] must have exact keys affected_section, severity_class, issue")
                    continue
                if not all(isinstance(item[k], str) and item[k].strip() for k in ("affected_section", "severity_class", "issue")):
                    errors.append(f"cross_section_sync_alerts[{idx}] fields must be non-empty strings")
                elif item["severity_class"] not in {"Class A", "Class B", "Class C", "Class D"}:
                    errors.append(f"cross_section_sync_alerts[{idx}] invalid severity_class: {item['severity_class']}")

    if "unverified_context_locks" in payload:
        arr = payload["unverified_context_locks"]
        if not isinstance(arr, list) or not all(isinstance(x, str) for x in arr):
            errors.append("unverified_context_locks must be an array of strings")

    return errors


def _validate_cli_identifiers(
    model: str | None = None,
    resume_id: str | None = None,
    timeout_seconds: int = 180,
    max_tokens: int | None = None,
) -> None:
    if isinstance(timeout_seconds, bool) or timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be > 0")
    if max_tokens is not None and (isinstance(max_tokens, bool) or max_tokens <= 0):
        raise ValueError("max_tokens must be > 0")
    if model is not None:
        if not isinstance(model, str) or not MODEL_ID_RE.fullmatch(model):
            raise ValueError(f"Invalid model identifier: {model!r}")
    if resume_id is not None:
        if not isinstance(resume_id, str) or not RESUME_ID_RE.fullmatch(resume_id):
            raise ValueError(f"Invalid resume_id: {resume_id!r}")


def _split_command_template(cmd_template: str, use_posix: bool | None = None) -> list[str]:
    eff_posix = (os.name != "nt") if use_posix is None else use_posix
    raw_tokens = shlex.split(cmd_template, posix=eff_posix)
    if not eff_posix:
        cleaned: list[str] = []
        for tok in raw_tokens:
            if len(tok) >= 2 and tok[0] == tok[-1] and tok[0] in {'"', "'"}:
                tok = tok[1:-1]
            else:
                tok = WINDOWS_FLAG_QUOTED_RE.sub(r"\1\3", tok)
            cleaned.append(tok)
        return cleaned
    return raw_tokens


def _prepare_windows_safe_exec_cmd(
    cmd: list[str],
    resolved_exe: str | None = None,
    is_windows: bool | None = None,
) -> list[str]:
    eff_windows = (os.name == "nt") if is_windows is None else is_windows
    if resolved_exe is None:
        resolved_exe = shutil.which(cmd[0])
        if resolved_exe is None and Path(cmd[0]).is_file():
            resolved_exe = str(Path(cmd[0]).resolve())
    if resolved_exe is None and not Path(cmd[0]).is_file():
        raise BackendExecutionError(
            "BACKEND_NOT_FOUND",
            f"Backend executable {cmd[0]!r} was not found on PATH",
            exit_code=2,
        )
    if resolved_exe and ("/" in resolved_exe or "\\" in resolved_exe) and Path(resolved_exe).exists():
        resolved_exe = str(Path(resolved_exe).resolve())
    exec_cmd = [resolved_exe, *cmd[1:]] if resolved_exe else list(cmd)
    if eff_windows and exec_cmd[0].lower().endswith((".cmd", ".bat")):
        shim_path = Path(exec_cmd[0])
        npm_js_targets = {
            "codex": ("@openai", "codex", "bin", "codex.js"),
            "claude": ("@anthropic-ai", "claude-code", "cli.js"),
        }
        stem_low = shim_path.stem.lower()
        if stem_low in npm_js_targets:
            shim_dir = shim_path.parent
            entry_js = shim_dir.joinpath("node_modules", *npm_js_targets[stem_low])
            if entry_js.is_file():
                local_node = shim_dir / "node.exe"
                node_exe = str(local_node) if local_node.is_file() else shutil.which("node")
                if node_exe:
                    return [node_exe, str(entry_js), *cmd[1:]]
        for arg in exec_cmd[1:]:
            if WINDOWS_BATCH_METACHAR_RE.search(arg):
                raise BackendExecutionError(
                    "UNSAFE_WINDOWS_BATCH_ARG",
                    f"Refusing to pass argument containing Windows batch metacharacters to {shim_path.name}: {arg!r}",
                    exit_code=2,
                )
    return exec_cmd


def assemble_backend_command(
    backend: str,
    prompt_file: Path,
    schema_file: Path,
    raw_output_file: Path,
    spine_file: Path,
    model: str | None = None,
    resume_id: str | None = None,
    agy_format: str = "stream-json",
    timeout_seconds: int = 180,
    sandbox: bool = True,
    cmd_template: str | None = None,
    use_posix: bool | None = None,
) -> tuple[list[str], bool]:
    """Assemble subprocess argv and whether prompt_text should be piped via stdin."""
    _validate_cli_identifiers(model=model, resume_id=resume_id, timeout_seconds=timeout_seconds)
    if backend == "agy":
        cmd = [
            "agy",
            "--print",
            "--mode",
            "plan",
            "--output-format",
            agy_format,
            "--json-schema",
            str(schema_file),
            "--print-timeout",
            f"{timeout_seconds}s",
        ]
        if sandbox:
            cmd.append("--sandbox")
        if model:
            cmd.extend(["--model", model])
        if resume_id:
            cmd.extend(["--resume", resume_id])
        return cmd, True

    if backend == "codex":
        if resume_id:
            cmd = ["codex", "exec", "resume", "--skip-git-repo-check"]
            if sandbox:
                cmd.extend(["-c", 'sandbox_mode="read-only"'])
            if model:
                cmd.extend(["-m", model])
            cmd.extend(["--output-schema", str(schema_file), "-o", str(raw_output_file), resume_id, "-"])
        else:
            cmd = ["codex", "exec", "--skip-git-repo-check"]
            if sandbox:
                cmd.extend(["--sandbox", "read-only"])
            if model:
                cmd.extend(["-m", model])
            cmd.extend(["--output-schema", str(schema_file), "-o", str(raw_output_file), "-"])
        return cmd, True

    if backend == "claude":
        inline_schema = json.dumps(DELEGATE_RESPONSE_SCHEMA, separators=(",", ":"))
        cmd = [
            "claude",
            "-p",
            "--output-format",
            "json",
            "--json-schema",
            inline_schema,
        ]
        if model:
            cmd.extend(["--model", model])
        if resume_id:
            cmd.extend(["--resume", resume_id])
        cmd.extend(["--tools", ""])
        return cmd, True

    if backend == "command":
        if not cmd_template or not cmd_template.strip():
            raise ValueError("--cmd-template is required when --backend command is selected")
        raw_tokens = _split_command_template(cmd_template, use_posix=use_posix)
        if not raw_tokens or not raw_tokens[0].strip():
            raise ValueError("--cmd-template must begin with a non-empty executable token")
        substitutions = {
            "{prompt_file}": str(prompt_file),
            "{schema_file}": str(schema_file),
            "{output_file}": str(raw_output_file),
            "{spine_file}": str(spine_file),
        }
        uses_prompt_placeholder = "{prompt_file}" in cmd_template
        argv: list[str] = []
        for tok in raw_tokens:
            replaced = tok
            for k, v in substitutions.items():
                replaced = replaced.replace(k, v)
            argv.append(replaced)
        return argv, (not uses_prompt_placeholder)

    raise ValueError(f"Unsupported subprocess backend: {backend}")


def _extract_json_object(raw_text: str) -> dict[str, Any]:
    stripped = raw_text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*\n?", "", stripped)
        stripped = re.sub(r"\n?```\s*$", "", stripped).strip()
    try:
        parsed = json.loads(stripped)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    # Fallback: locate outermost {...}
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start != -1 and end > start:
        try:
            parsed = json.loads(stripped[start:end + 1])
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
    raise BackendExecutionError("INVALID_BACKEND_JSON", "Backend did not return a valid JSON object", exit_code=2)


def parse_backend_output(
    backend: str,
    returncode: int,
    stdout_text: str,
    stderr_text: str,
    raw_output_file: Path | None = None,
) -> Any:
    """Parse backend output and fail closed on silent timeouts, truncations, or empty responses."""
    if backend == "agy":
        finished_reasons: list[str] = []
        candidate_payload: Any = None
        has_structured_output = False
        streamed_chunks: list[str] = []

        def _inspect_agy_obj(obj: dict[str, Any]) -> None:
            nonlocal candidate_payload, has_structured_output
            fr = obj.get("finished_reason") or obj.get("stop_reason")
            if isinstance(fr, str) and fr.strip():
                finished_reasons.append(fr.strip().lower())
            res_sub = obj.get("result")
            if isinstance(res_sub, dict):
                sub_fr = res_sub.get("finished_reason") or res_sub.get("stop_reason")
                if isinstance(sub_fr, str) and sub_fr.strip():
                    finished_reasons.append(sub_fr.strip().lower())
                if "structured_output" in res_sub and res_sub["structured_output"] is not None:
                    candidate_payload = res_sub["structured_output"]
                    has_structured_output = True
                elif not has_structured_output and "revised_target_prose" in res_sub:
                    candidate_payload = res_sub
                elif not has_structured_output and not isinstance(candidate_payload, dict) and isinstance(res_sub.get("response"), str) and res_sub["response"].strip():
                    candidate_payload = res_sub["response"]
            if "structured_output" in obj and obj["structured_output"] is not None:
                candidate_payload = obj["structured_output"]
                has_structured_output = True
            elif not has_structured_output and "revised_target_prose" in obj:
                candidate_payload = obj
            elif not has_structured_output and not isinstance(candidate_payload, dict) and isinstance(obj.get("response"), str) and obj["response"].strip():
                candidate_payload = obj["response"]
            if isinstance(obj.get("delta"), str):
                streamed_chunks.append(obj["delta"])

        parsed_any = False
        stripped_out = stdout_text.strip()
        if stripped_out:
            try:
                whole_obj = json.loads(stripped_out)
                if isinstance(whole_obj, dict):
                    _inspect_agy_obj(whole_obj)
                    parsed_any = True
            except json.JSONDecodeError:
                pass
        if not parsed_any:
            for ln in stdout_text.splitlines():
                ln_s = ln.strip()
                if not ln_s:
                    continue
                try:
                    obj = json.loads(ln_s)
                except json.JSONDecodeError:
                    continue
                if isinstance(obj, dict):
                    _inspect_agy_obj(obj)
                    parsed_any = True

        bad_hits = [r for r in finished_reasons if r in BAD_FINISH_REASONS]
        if bad_hits:
            code_num = 124 if any("timeout" in r for r in bad_hits) else 2
            raise BackendExecutionError(
                "SILENT_TIMEOUT_OR_TRUNCATION",
                f"agy finished_reason={bad_hits[0]!r} (exit={returncode}); rejecting partial/empty output",
                exit_code=code_num,
            )
        if returncode != 0:
            raise BackendExecutionError(
                "NONZERO_BACKEND_EXIT",
                f"agy exited with code {returncode}: {stderr_text.strip()[:240]}",
                exit_code=2,
            )
        if isinstance(candidate_payload, dict) or (has_structured_output and not isinstance(candidate_payload, str)):
            return candidate_payload
        if has_structured_output and isinstance(candidate_payload, str):
            s_cand = candidate_payload.strip()
            return _extract_json_object(s_cand) if s_cand.startswith(("{", "```")) else candidate_payload
        joined_deltas = "".join(streamed_chunks)
        text_out = (
            candidate_payload
            if (isinstance(candidate_payload, str) and candidate_payload.strip())
            else (joined_deltas or ("" if parsed_any else stdout_text))
        )
        if not text_out or not text_out.strip():
            raise BackendExecutionError(
                "EMPTY_BACKEND_RESPONSE",
                "agy returned exit 0 with empty response payload",
                exit_code=124,
            )
        try:
            return _extract_json_object(text_out)
        except BackendExecutionError:
            if joined_deltas.strip() and text_out != joined_deltas:
                return _extract_json_object(joined_deltas)
            raise

    if backend == "claude":
        if returncode != 0:
            raise BackendExecutionError(
                "NONZERO_BACKEND_EXIT",
                f"claude exited with code {returncode}: {stderr_text.strip()[:240]}",
                exit_code=2,
            )
        if not stdout_text.strip():
            raise BackendExecutionError("EMPTY_BACKEND_RESPONSE", "claude returned empty stdout", exit_code=124)
        wrapper = _extract_json_object(stdout_text)
        subtype = str(wrapper.get("subtype", "")).lower()
        stop_reason = str(wrapper.get("stop_reason", "")).lower()
        if wrapper.get("is_error") is True or subtype in {"error_max_turns", "timeout", "max_tokens"} or stop_reason in BAD_FINISH_REASONS:
            raise BackendExecutionError(
                "SILENT_TIMEOUT_OR_TRUNCATION",
                f"claude reported error/truncation (is_error={wrapper.get('is_error')}, subtype={subtype!r}, stop_reason={stop_reason!r})",
                exit_code=124 if "timeout" in subtype or "timeout" in stop_reason else 2,
            )
        if "structured_output" in wrapper and wrapper["structured_output"] is not None:
            so = wrapper["structured_output"]
            return _extract_json_object(so) if isinstance(so, str) else so
        if "revised_target_prose" in wrapper:
            return wrapper
        res = wrapper.get("result", "")
        if isinstance(res, dict):
            return res
        if not isinstance(res, str) or not res.strip():
            raise BackendExecutionError("EMPTY_BACKEND_RESPONSE", "claude wrapper contained empty result", exit_code=124)
        return _extract_json_object(res)

    if backend in {"codex", "command"}:
        if returncode != 0:
            raise BackendExecutionError(
                "NONZERO_BACKEND_EXIT",
                f"{backend} exited with code {returncode}: {stderr_text.strip()[:240]}",
                exit_code=2,
            )
        raw_content = ""
        if raw_output_file and raw_output_file.is_file():
            raw_content = raw_output_file.read_text(encoding="utf-8", errors="replace")
        if not raw_content.strip():
            raw_content = stdout_text
        if not raw_content.strip():
            raise BackendExecutionError(
                "EMPTY_BACKEND_RESPONSE",
                f"{backend} returned exit 0 with empty output",
                exit_code=124,
            )
        return _extract_json_object(raw_content)

    raise ValueError(f"Unsupported backend for output parsing: {backend}")


def build_compact_receipt_summary(
    status: str,
    target_locator: str,
    backend: str,
    packet_tokens: int,
    prose_words: int,
    omitted_count: int,
    sync_alert_count: int,
    finding_codes: list[str],
    workdir: Path,
) -> str:
    """Construct a host-budget-safe summary strictly <= 200 words."""
    findings_part = ", ".join(finding_codes[:8]) if finding_codes else "none"
    summary = (
        f"[{status}] Scoped pass on '{target_locator}' via backend={backend} "
        f"(packet={packet_tokens} est_tokens; revised_words={prose_words}; "
        f"omitted_to_display={omitted_count}; sync_alerts={sync_alert_count}; "
        f"findings={findings_part}). Full verified artifacts saved under {workdir.name}/."
    )
    words = summary.split()
    if len(words) > 195:
        summary = " ".join(words[:195]) + " ..."
    return summary


def evaluate_delegate_reply(
    reply_obj: Any,
    before_text: str | None,
    spine: dict[str, Any],
    envelope_meta: dict[str, Any],
    envelope_text: str,
    companion_paths: list[Path],
    state_path: Path | None,
    verification_mode: str,
    mode: str = "revise",
    extra_source_texts: list[str] | None = None,
) -> dict[str, Any]:
    for p in companion_paths:
        if not p.is_file():
            raise FileNotFoundError(f"Companion file not found: {p}")
    state_obj: dict[str, Any] | None = None
    if state_path is not None:
        if not state_path.is_file():
            raise FileNotFoundError(f"State file not found: {state_path}")
        loaded_state = json.loads(state_path.read_text(encoding="utf-8"))
        if not isinstance(loaded_state, dict):
            raise ValueError(f"State file must contain a JSON object: {state_path}")
        state_obj = loaded_state

    schema_errors = validate_delegate_reply_schema(reply_obj)
    if schema_errors:
        return {
            "status": "FAIL",
            "schema_errors": schema_errors,
            "numeric_verification": None,
            "prose_audit": None,
            "prose_findings": [],
            "blocking_prose_codes": [],
        }

    revised_prose = reply_obj["revised_target_prose"]
    omitted_list = reply_obj["declared_omitted_to_display"]
    sync_alerts = reply_obj["cross_section_sync_alerts"]

    if verification_mode == "strict_preservation":
        if before_text is None:
            raise ValueError("strict_preservation requires existing target text")
        num_report = verify_strict_preservation(before_text, revised_prose)
    else:
        source_texts: list[str] = extract_authoritative_spine_texts(spine)
        rel_slices = envelope_meta.get("relevant_display_slices")
        if isinstance(rel_slices, dict):
            source_texts.extend(str(v) for v in rel_slices.values())
        if extra_source_texts:
            source_texts.extend(extra_source_texts)
        for p in companion_paths:
            source_texts.append(read_source_file_text(p))
        if not source_texts and envelope_text:
            cut_m = re.search(r"\n8\.\s+IMMEDIATE NEIGHBORING CONTEXT", envelope_text)
            source_texts.append(envelope_text[:cut_m.start()] if cut_m else envelope_text)
        num_report = verify_curated_salience(
            after_text=revised_prose,
            source_texts=source_texts,
            before_text=before_text,
            declared_omitted_to_display=omitted_list,
            downstream_dependencies=envelope_meta.get("downstream_dependencies", []),
            cross_section_sync_alerts=sync_alerts,
        )

    if state_obj is not None:
        prose_findings = audit_candidate(revised_prose, "revised_target_prose", state_obj)
    else:
        prose_findings = audit_prose_text(revised_prose, "revised_target_prose", {})

    # Enforce PROSE018 only in curated_salience (proofread / strict_preservation preserves verified CI walls)
    enforce_numeric_salience = verification_mode != "strict_preservation" and mode not in {"proofread", "review"}
    blocking_set = {"PROSE016", "PROSE017", "PROSE018"} if enforce_numeric_salience else {"PROSE016", "PROSE017"}
    blocking_prose_codes = [
        f["code"]
        for f in prose_findings
        if f["code"] in blocking_set
        or f["code"].startswith("TEXT")
        or (f["code"].startswith("CAND") and f["code"] != "CAND001")
    ]
    overall_ok = num_report["status"].startswith("PASS") and not blocking_prose_codes
    overall_status = (
        num_report["status"]
        if overall_ok
        else "FAIL"
    )

    return {
        "status": overall_status,
        "schema_errors": [],
        "numeric_verification": num_report,
        "prose_findings": prose_findings,
        "blocking_prose_codes": blocking_prose_codes,
    }


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manuscript", type=Path, required=True, help="Path to .docx, .tex, or .md manuscript")
    parser.add_argument("--target", required=True, help="Target section heading substring or block ID/range")
    parser.add_argument(
        "--backend",
        choices=("agy", "codex", "claude", "command", "envelope-only"),
        default="envelope-only",
        help="Agent B execution backend",
    )
    parser.add_argument("--mode", choices=("plan", "draft", "revise", "proofread", "review"), default="revise")
    parser.add_argument(
        "--verification-mode",
        choices=("auto", "strict_preservation", "curated_salience"),
        default="auto",
    )
    parser.add_argument("--task", default="Revise ONLY the authorized target unit using the architecture spine and two-stage evidence-salience contract.")
    parser.add_argument("--workdir", type=Path, required=True, help="Directory to store envelope, schema, and evidence_refs")
    parser.add_argument("--companion", type=Path, nargs="*", default=[], help="Optional companion CSV/TSV/SM files")
    parser.add_argument("--state", type=Path, default=None, help="Optional manuscript_state.json")
    parser.add_argument("--paper-dir", type=Path, default=None, help="Optional .paper/ directory (read-only)")
    parser.add_argument("--max-tokens", type=int, default=4500, help="Hard packet token ceiling (default: 4500)")
    parser.add_argument("--model", default=None, help="Optional model name forwarded to agy/codex/claude")
    parser.add_argument("--resume", default=None, help="Optional session/conversation ID to resume")
    parser.add_argument("--agy-format", choices=("json", "stream-json"), default="stream-json")
    parser.add_argument("--timeout", type=int, default=180, help="Backend timeout in seconds")
    parser.add_argument("--no-sandbox", action="store_true", help="Disable read-only/sandbox flag on backend CLI")
    parser.add_argument("--cmd-template", default=None, help="Command template for --backend command")
    parser.add_argument("--verify-reply", type=Path, default=None, help="Verify an existing Agent B JSON reply (for envelope-only / native subagents)")
    parser.add_argument("--dry-run-command", action="store_true", help="Emit assembled envelope + CLI command without executing backend")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit machine-readable JSON receipt")
    args = parser.parse_args(argv)

    try:
        _validate_cli_identifiers(
            model=args.model,
            resume_id=args.resume,
            timeout_seconds=args.timeout,
            max_tokens=args.max_tokens,
        )
        if args.verify_reply is not None and not args.verify_reply.is_file():
            raise FileNotFoundError(f"--verify-reply file not found: {args.verify_reply}")
        workdir = args.workdir.resolve()
        workdir.mkdir(parents=True, exist_ok=True)

        blocks, spine = load_or_build_spine(
            args.manuscript,
            companion_paths=args.companion,
            state_path=args.state,
            paper_dir=args.paper_dir,
            cache_file=workdir / "spine_cache.json",
        )
        target_indices = locate_target_blocks(blocks, args.target)
        non_heading_blocks = [blocks[i] for i in target_indices if not blocks[i]["is_heading"]]
        prose_blocks = [b for b in non_heading_blocks if b.get("kind") != "table"]
        embedded_table_texts = [
            (f"{b['caption']}\n{b['text']}" if b.get("caption") else b["text"])
            for b in non_heading_blocks
            if b.get("kind") == "table"
        ]
        eff_target_blocks = prose_blocks if prose_blocks else non_heading_blocks
        before_text = "\n\n".join(b["text"] for b in eff_target_blocks) if args.mode in {"revise", "proofread", "review"} else None

        schema_instruction = (
            args.task.strip()
            + "\nReturn ONLY valid JSON matching the attached 4-key Dual-Channel Schema: "
            "{revised_target_prose, declared_omitted_to_display, cross_section_sync_alerts, unverified_context_locks}."
        )
        envelope_text, env_meta = build_scoped_context_envelope(
            blocks,
            spine,
            target_locator=args.target,
            task_instruction=schema_instruction,
            mode=args.mode,
            max_tokens=args.max_tokens,
        )
        if not env_meta["within_budget"]:
            print(
                json.dumps(
                    {
                        "status": "PACKET_BUDGET_EXCEEDED",
                        "task_packet_tokens": env_meta["est_tokens"],
                        "max_tokens": args.max_tokens,
                    },
                    indent=2,
                ),
                file=sys.stderr,
            )
            return 2

        spine_file = workdir / "spine.json"
        envelope_file = workdir / "context_envelope.txt"
        schema_file = workdir / "delegate_response_schema.json"
        raw_reply_file = workdir / "backend_raw_reply.json"

        spine_file.write_text(json.dumps({"meta": env_meta, "spine": spine}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        envelope_file.write_text(envelope_text, encoding="utf-8")
        schema_file.write_text(json.dumps(DELEGATE_RESPONSE_SCHEMA, indent=2) + "\n", encoding="utf-8")

        evidence_refs: dict[str, dict[str, str]] = {
            "spine": {"path": str(spine_file), "sha256": _sha256_file(spine_file)},
            "envelope": {"path": str(envelope_file), "sha256": _sha256_file(envelope_file)},
            "schema": {"path": str(schema_file), "sha256": _sha256_file(schema_file)},
        }

        eff_vmode = (
            ("strict_preservation" if args.mode == "proofread" else "curated_salience")
            if args.verification_mode == "auto"
            else args.verification_mode
        )

        # Envelope-only preparation step (for native host subagents)
        if args.backend == "envelope-only" and args.verify_reply is None:
            summary = build_compact_receipt_summary(
                status="ENVELOPE_READY",
                target_locator=args.target,
                backend="envelope-only",
                packet_tokens=env_meta["est_tokens"],
                prose_words=0,
                omitted_count=0,
                sync_alert_count=0,
                finding_codes=[],
                workdir=workdir,
            )
            receipt = {
                "status": "ENVELOPE_READY",
                "backend": "envelope-only",
                "verification_mode": eff_vmode,
                "task_packet_tokens": env_meta["est_tokens"],
                "summary_words": _word_count(summary),
                "summary": summary,
                "evidence_refs": evidence_refs,
            }
            (workdir / "pass_receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(receipt, ensure_ascii=False, indent=2) if args.as_json else summary)
            return 0

        if args.verify_reply is not None:
            reply_obj = json.loads(args.verify_reply.read_text(encoding="utf-8"))
            evidence_refs["verified_reply_input"] = {
                "path": str(args.verify_reply.resolve()),
                "sha256": _sha256_file(args.verify_reply.resolve()),
            }
        else:
            cmd, pipe_stdin = assemble_backend_command(
                backend=args.backend,
                prompt_file=envelope_file,
                schema_file=schema_file,
                raw_output_file=raw_reply_file,
                spine_file=spine_file,
                model=args.model,
                resume_id=args.resume,
                agy_format=args.agy_format,
                timeout_seconds=args.timeout,
                sandbox=not args.no_sandbox,
                cmd_template=args.cmd_template,
            )
            if args.dry_run_command:
                dry = {
                    "status": "DRY_RUN",
                    "backend": args.backend,
                    "command": cmd,
                    "pipe_stdin": pipe_stdin,
                    "task_packet_tokens": env_meta["est_tokens"],
                    "evidence_refs": evidence_refs,
                }
                print(json.dumps(dry, ensure_ascii=False, indent=2))
                return 0

            raw_reply_file.unlink(missing_ok=True)
            exec_cmd = _prepare_windows_safe_exec_cmd(cmd)
            isolated_cwd = workdir / "empty_delegate_cwd"
            isolated_cwd.mkdir(parents=True, exist_ok=True)
            try:
                proc = subprocess.run(
                    exec_cmd,
                    input=envelope_text if pipe_stdin else None,
                    cwd=isolated_cwd,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    capture_output=True,
                    timeout=args.timeout + 15,
                    check=False,
                )
            except subprocess.TimeoutExpired as exc:
                raise BackendExecutionError(
                    "SUBPROCESS_WALL_TIMEOUT",
                    f"{args.backend} exceeded wall timeout of {args.timeout + 15}s",
                    exit_code=124,
                ) from exc

            (workdir / "backend_stdout.log").write_text(proc.stdout or "", encoding="utf-8")
            (workdir / "backend_stderr.log").write_text(proc.stderr or "", encoding="utf-8")
            reply_obj = parse_backend_output(
                backend=args.backend,
                returncode=proc.returncode,
                stdout_text=proc.stdout or "",
                stderr_text=proc.stderr or "",
                raw_output_file=raw_reply_file,
            )
            parsed_reply_path = workdir / "parsed_delegate_reply.json"
            parsed_reply_path.write_text(json.dumps(reply_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            evidence_refs["parsed_reply"] = {
                "path": str(parsed_reply_path),
                "sha256": _sha256_file(parsed_reply_path),
            }

        eval_report = evaluate_delegate_reply(
            reply_obj=reply_obj,
            before_text=before_text,
            spine=spine,
            envelope_meta=env_meta,
            envelope_text=envelope_text,
            companion_paths=args.companion,
            state_path=args.state,
            verification_mode=eff_vmode,
            mode=args.mode,
            extra_source_texts=embedded_table_texts,
        )

        verification_file = workdir / "verification_report.json"
        verification_file.write_text(json.dumps(eval_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        evidence_refs["verification_report"] = {
            "path": str(verification_file),
            "sha256": _sha256_file(verification_file),
        }

        raw_prose = reply_obj.get("revised_target_prose") if isinstance(reply_obj, dict) else None
        raw_om = reply_obj.get("declared_omitted_to_display") if isinstance(reply_obj, dict) else None
        raw_sync = reply_obj.get("cross_section_sync_alerts") if isinstance(reply_obj, dict) else None

        prose_text = raw_prose if isinstance(raw_prose, str) else ""
        omitted_items = raw_om if isinstance(raw_om, list) else []
        sync_items = raw_sync if isinstance(raw_sync, list) else []

        preview_md = workdir / "revised_target_preview.md"
        if prose_text and not eval_report["schema_errors"]:
            preview_lines = [prose_text.strip(), ""]
            if omitted_items:
                preview_lines.append("## Display-Omission Reconciliation Ledger")
                for om in omitted_items:
                    if isinstance(om, dict):
                        preview_lines.append(f"- `{om.get('value_or_entity')}` -> {om.get('display_ref')} ({om.get('rationale_tier')})")
                preview_lines.append("")
            if sync_items or (eval_report.get("numeric_verification") or {}).get("class_b_downstream_sync_checklist"):
                preview_lines.append("## Downstream Section Sync Checklist (Class A/B)")
                for sa in sync_items:
                    if isinstance(sa, dict):
                        preview_lines.append(f"- **[{sa.get('severity_class')}] {sa.get('affected_section')}**: {sa.get('issue')}")
                for cb in (eval_report.get("numeric_verification") or {}).get("class_b_downstream_sync_checklist", []):
                    locs = ", ".join(
                        f"{loc.get('block_id')} ({loc.get('section_heading')})"
                        for loc in cb.get("downstream_locations", [])
                    )
                    preview_lines.append(f"- **[CLASS_B_SYNC_REQUIRED] `{cb.get('pruned_item')}`**: referenced in {locs}")
                preview_lines.append("")
            preview_md.write_text("\n".join(preview_lines), encoding="utf-8")
            evidence_refs["revised_preview_md"] = {
                "path": str(preview_md),
                "sha256": _sha256_file(preview_md),
            }
        else:
            preview_md.unlink(missing_ok=True)

        finding_codes: list[str] = []
        if eval_report["schema_errors"]:
            finding_codes.append("SCHEMA_INVALID")
        num_ver = eval_report.get("numeric_verification") or {}
        finding_codes.extend(f["code"] for f in num_ver.get("findings", []))
        finding_codes.extend(eval_report.get("blocking_prose_codes", []))

        summary = build_compact_receipt_summary(
            status=eval_report["status"],
            target_locator=args.target,
            backend=args.backend,
            packet_tokens=env_meta["est_tokens"],
            prose_words=_word_count(prose_text),
            omitted_count=len(omitted_items),
            sync_alert_count=len(sync_items),
            finding_codes=finding_codes,
            workdir=workdir,
        )
        receipt = {
            "status": eval_report["status"],
            "backend": args.backend,
            "verification_mode": eff_vmode,
            "task_packet_tokens": env_meta["est_tokens"],
            "summary_words": _word_count(summary),
            "summary": summary,
            "evidence_refs": evidence_refs,
        }
        receipt_file = workdir / "pass_receipt.json"
        receipt_file.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        print(json.dumps(receipt, ensure_ascii=False, indent=2) if args.as_json else summary)
        return 0 if eval_report["status"].startswith("PASS") else 1

    except BackendExecutionError as exc:
        err_payload = {"status": exc.code, "error": str(exc)}
        print(json.dumps(err_payload, ensure_ascii=False, indent=2), file=sys.stderr)
        return exc.exit_code
    except (OSError, ValueError, BadZipFile, ET.ParseError, KeyError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
