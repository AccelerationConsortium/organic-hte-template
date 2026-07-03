#!/usr/bin/env python3
"""Validate protocol YAML files against schema/protocol.schema.json.

Checks, per file in protocols/:
  1. YAML parses and conforms to the JSON Schema.
  2. step_ids are unique within the file.
  3. The `protocol` field matches the filename.
  4. (PR only, BASE_REF set) step_ids that exist on the base branch are
     never removed or renamed — records in AnaliticaDB anchor to them.

Usage:
  python scripts/validate_protocols.py                        # checks 1-3
  BASE_REF=origin/main python scripts/validate_protocols.py   # + check 4

Requires: pyyaml, jsonschema.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schema" / "protocol.schema.json").read_text())


def base_step_ids(path: Path) -> set | None:
    """step_ids of this file on BASE_REF, or None if new/no base configured."""
    base = os.environ.get("BASE_REF")
    if not base:
        return None
    rel = path.relative_to(ROOT).as_posix()
    proc = subprocess.run(
        ["git", "show", f"{base}:{rel}"],
        capture_output=True, text=True, cwd=ROOT,
    )
    if proc.returncode != 0:  # file does not exist on the base branch
        return None
    try:
        doc = yaml.safe_load(proc.stdout) or {}
    except yaml.YAMLError:
        return None
    steps = doc.get("steps") or []
    return {s.get("step_id") for s in steps if isinstance(s, dict)} - {None}


def main() -> int:
    files = sorted((ROOT / "protocols").glob("*.yaml")) + sorted(
        (ROOT / "protocols").glob("*.yml")
    )
    validator = Draft202012Validator(SCHEMA)
    errors: list[str] = []

    for path in files:
        rel = path.relative_to(ROOT)
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
        except yaml.YAMLError as exc:
            errors.append(f"{rel}: YAML parse error: {exc}")
            continue

        schema_errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
        for err in schema_errors:
            where = "/".join(str(p) for p in err.path) or "<root>"
            errors.append(f"{rel}: {where}: {err.message}")
        if schema_errors or not isinstance(doc, dict):
            continue

        if doc.get("protocol") != path.stem:
            errors.append(
                f"{rel}: protocol name {doc.get('protocol')!r} must equal "
                f"filename stem {path.stem!r}"
            )

        ids = [s["step_id"] for s in doc["steps"]]
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        if dupes:
            errors.append(f"{rel}: duplicate step_id(s): {dupes}")

        old_ids = base_step_ids(path)
        if old_ids:
            missing = sorted(old_ids - set(ids))
            if missing:
                errors.append(
                    f"{rel}: step_id(s) removed or renamed vs "
                    f"{os.environ['BASE_REF']}: {missing} — step_ids are "
                    f"permanent once merged; add steps, never rename ids"
                )

    if not files:
        print("warning: no protocol files found in protocols/")
    for err in errors:
        print(f"ERROR: {err}")
    print(f"{len(files)} protocol file(s) checked, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
