# Changelog — organic-hte-template

`TEMPLATE_VERSION` is the template's contract version (semver). Bump it in
the same PR as any change a stamped project should adopt:

- **MAJOR** — restructure requiring manual migration in projects
- **MINOR** — new files, checks, or rules projects should copy in
- **PATCH** — fixes/wording that change no obligations

Projects declare the version they conform to in their `pins.yaml`; their CI
surfaces (without blocking) when this file moves past their pin.

## 1.1.0 — 2026-07-13

- Add `AGENTS.md` (shared, model-agnostic agent working instructions for all
  agents — Hermes, Codex, Claude Code) and a thin `CLAUDE.md` (Claude-Code
  specifics; imports `AGENTS.md`). These follow the canonical base established
  in `ac-organic-lab` (`AGENTS.md` + `CLAUDE.md`): `AGENTS.md` references the
  binding contract (`AGENT_RULES.md` + the lab-wide canon) without restating it,
  and encodes the memory/instruction policy (AGENTS.md = shared, CLAUDE.md =
  Claude-only, cross-repo facts → global memory by proposal). Projects should
  copy both files in and fill the project-specific sections (MINOR — new files
  projects should adopt).

## 1.0.1 — 2026-07-04

- `pins.yaml`: add a commented `analiticadb-contract` example (0.6.0) so
  stamped projects have the pattern for pinning the ontology
  `SCHEMA_VERSION` they write records against. Docs-only; no obligation
  change (PATCH).

## 1.0.0 — 2026-07-03

Initial contract:

- `protocols/` as the authored-artifact home; commented YAML validated
  against `schema/protocol.schema.json` by CI (unique + permanent
  `step_id`s enforced on PRs).
- `AGENT_RULES.md` (links the lab-wide canon), `CODEOWNERS`,
  `scripts/create_ruleset.sh` (protect-main: PR-only, squash-only,
  required `protocols` check).
- `pins.yaml` + `scripts/check_pins.py` + the non-blocking CI `pins` job:
  cross-repo version pinning (template contract, AnaliticaDB ontology
  `SCHEMA_VERSION`).
- No run data, no filename versioning; local configs gitignored.
