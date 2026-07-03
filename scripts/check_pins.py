#!/usr/bin/env python3
"""Report drift between pins.yaml and live upstream versions.

Non-blocking by design: the CI `pins` job runs with `continue-on-error`, so
a moved upstream shows as a visibly failed job on the PR without blocking
the merge. Unreachable upstreams (private repo, Tailnet-only service) are
SKIPPED, not failed — this check is best-effort awareness; any runtime
exact-match check (e.g. AnaliticaDB's ontology pin) is the enforcement.

Usage:  python scripts/check_pins.py          (exit 1 on drift)
Requires: pyyaml.
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def fetch_version(url: str, json_path: str | None = None) -> str:
    with urllib.request.urlopen(url, timeout=5) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    if json_path:
        node = json.loads(body)
        for key in json_path.split("."):
            node = node[key]
        return str(node).strip()
    return body.strip()


def main() -> int:
    doc = yaml.safe_load((ROOT / "pins.yaml").read_text()) or {}
    pins = doc.get("pins") or {}
    if not pins:
        print("no pins declared in pins.yaml")
        return 0

    drifted: list[tuple[str, str, str]] = []
    for name, spec in pins.items():
        pinned = str((spec or {}).get("version", "")).strip()
        url = (spec or {}).get("check")
        if not pinned or not url:
            print(f"skipped {name}: pin needs both `version` and `check`")
            continue
        try:
            current = fetch_version(url, (spec or {}).get("json_path"))
        except Exception as exc:  # noqa: BLE001 — unreachable upstream = skip
            print(f"skipped {name}: upstream unreachable ({exc})")
            continue
        if current == pinned:
            print(f"ok      {name}: {pinned}")
        else:
            drifted.append((name, pinned, current))

    for name, pinned, current in drifted:
        print(
            f"DRIFT   {name}: pinned {pinned}, upstream is now {current} — "
            "review the upstream changes and bump the pin when adopted"
        )
    return 1 if drifted else 0


if __name__ == "__main__":
    sys.exit(main())
