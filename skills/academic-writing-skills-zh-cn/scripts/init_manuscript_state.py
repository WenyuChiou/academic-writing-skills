#!/usr/bin/env python3
"""Initialize a manuscript state file without overwriting existing work."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", help="Target manuscript_state.json path")
    parser.add_argument("--project-id", default=None)
    parser.add_argument("--title", default=None)
    args = parser.parse_args()

    target = Path(args.output).expanduser().resolve()
    if target.exists():
        parser.error(f"refusing to overwrite existing file: {target}")

    template = Path(__file__).resolve().parents[1] / "assets" / "manuscript_state_template.json"
    state = json.loads(template.read_text(encoding="utf-8"))
    if args.project_id:
        state["project"]["id"] = args.project_id
    if args.title:
        state["project"]["title"] = args.title

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
