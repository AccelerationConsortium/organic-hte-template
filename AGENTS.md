# AGENTS.md — shared agent instructions — PROJECT_NAME

**Read this before proposing or editing anything in this repo.** It is the
shared instruction file for every coding agent — Hermes, Codex, Claude Code, and
any future agent. Keep it model-agnostic: anything specific to one agent goes in
that agent's own file (e.g. `CLAUDE.md`), never here.

This repo follows the **canonical base** established in `ac-organic-lab`
(`ac-organic-lab/AGENTS.md` + `CLAUDE.md`). This file keeps that structure and
adds only what is specific to this project.

## 1. The binding contract — do not weaken

These take precedence over everything here. Agents reference them; they do not
restate, reinterpret, or work around them. If a working convention here ever
conflicts, the contract wins — stop and flag it.

- **`ac-organic-lab/docs/AGENT_RULES.md`** — canonical lab-wide operating rules
  (safety, records, change control, chemicals, escalation). The "lab contract."
- **`ac-organic-lab/docs/STATUS_SPEC.md`** — the authoritative device contract,
  for any code here that talks to equipment.
- **`AGENT_RULES.md`** (this repo) — links the lab canon and adds this project's
  rules. Read it; the numbered rules there are authoritative for this repo.

Load-bearing points worth internalizing (authoritative text lives in the files
above):

- Never drive hardware directly — go through the `lab-skills` SDK, never raw
  device `/control/*`. Never bypass or weaken an interlock.
- Only human-approved, `main`-merged, validated protocols execute. Merge to
  `main` is the sign-off.
- **No run data in git.** Measurements, tables, images, plate/well actuals go to
  AnaliticaDB through its REST API — never into this repo. Git holds authored
  artifacts only (protocols, analysis code, rules).
- Local machine paths, hostnames, and secrets stay in gitignored `*.local.json`
  files, never in commits.
- When something is irreversible, ambiguous, or uncovered: stop and ask a human.

## 2. What this repo is

The **git side of the lab's record layer** for one science campaign. Authored
artifacts live here under pull-request review; operational records live in
**AnaliticaDB**; a commit hash on each database row ties the two together.

```
├── AGENTS.md         # this file — shared agent working instructions
├── CLAUDE.md         # Claude-Code-specific notes (imports AGENTS.md)
├── AGENT_RULES.md    # agent rules: lab-wide canon link + project rules
├── protocols/        # parameterized procedures (commented YAML) — authored layer
├── schema/           # machine-checkable protocol shape; CI validates every PR
├── analysis/         # code computing AnaliticaDB Analysis rows (commit-stamped)
├── configs/          # examples; real configs are *.local.json (gitignored)
├── pins.yaml         # cross-repo version pins (template, AnaliticaDB contract)
└── scripts/          # validate_protocols.py (the CI check) + check_pins.py
```

## 3. Working conventions

- **Protocols are the only executable artifacts.** Commented YAML in
  `protocols/`, validated against `schema/protocol.schema.json`. Changes arrive
  by PR; merge to `main` is the human sign-off; only `main` executes.
- **`step_id`s are permanent** once merged and executed — add steps freely,
  never rename or reuse an id. CI rejects removals on PRs.
- **Comments are for humans, fields are for machines.** YAML comments are dropped
  when a protocol renders into a database `Plan`; anything the executor needs
  must be a schema field.
- **Validate locally before pushing:** run `scripts/validate_protocols.py`
  (the same check CI runs on every PR).
- **Environment: `uv`.** Use `uv sync` / `uv run …`. Prefer reading source in
  `.venv/` over searching online for a dependency's usage.
- **Fail-fast style.** Don't add defensive code that swallows and hides errors;
  report failures truthfully.
- **Never rewrite published history.** `main` is protected (no force-push, no
  deletion, squash-only). Corrections are new commits.
- **Versioning / staying current:** `pins.yaml` declares which upstream versions
  this repo conforms to (the template `TEMPLATE_VERSION`; the AnaliticaDB
  ontology `SCHEMA_VERSION` once it writes records). The CI `pins` job flags
  drift non-blocking. Adopting an upstream bump = one PR that applies the change
  and updates the pin together.

## 4. Memory & instruction policy (how agents keep notes)

Durable, repo-wide convention — keeps all agents on the same page.

- **`AGENTS.md` (this file)** — shared, model-agnostic instructions: durable
  conventions, commands, layout, pitfalls, memory policy. Update it when you
  learn one of those.
- **`CLAUDE.md`** — Claude-Code-specific only (slash commands, Claude memory
  dir, Claude behavior). Other agents keep their own equivalent. Nothing another
  agent needs belongs here.
- **`AGENT_RULES.md`** — rules; changes only when a human explicitly asks. Never
  edit it to smooth over a working problem.
- **Cross-repo / MacBook-wide facts** (repo roles, stable machine setup, durable
  preferences) belong in the **agent's global memory** (Hermes, Codex
  `~/.codex/memories/`, Claude user memory) — *proposed for approval*, not
  silently written, and never stored in this repo.
- **Never** put temporary debugging notes, stale TODOs, or one-off observations
  into any memory or instruction file.

## 5. Safety protocol for edits outside this repo

Before editing anything outside this repository — another repo, `~/.hermes`,
`~/.claude`, `~/.codex`, shell config — first show the human: the exact file
path, the reason, the proposed change, and whether it affects only this repo or
future global behavior. Do not modify other repos or global settings until the
human approves.

## Project-specific instructions

<!-- Add working conventions specific to this project: extra commands, analysis
     entry points, dataset locations, campaign-specific pitfalls. Project safety
     rules go in AGENT_RULES.md, not here. Delete this comment. -->
