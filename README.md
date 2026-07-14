# organic-hte-template

Starter template for an SDL2 project repo — the **git side** of the lab's
record layer. Authored artifacts (protocols, analysis code, agent rules) live
here under pull-request review; operational records (plans, notes,
measurements, analyses) live in **AnaliticaDB**; a commit hash on each
database row ties the two together.

Design rationale: `AnaliticaDB/docs/eln-lims-generalization.md`, section
*"Project-repo blueprint — the git side of the record layer"* (mirrored as
`ac-organic-lab/docs/ANALITICADB_ELN_LIMS_DESIGN.md`).

## Using this template

1. Click **Use this template** on GitHub and name the new repo after the
   science (e.g. `organic-solubility`), matching its AnaliticaDB `project`
   string.
2. Put real reviewers in `.github/CODEOWNERS`.
3. Protect `main`: run `scripts/create_ruleset.sh` (needs the `gh` CLI with
   admin rights — rulesets are not copied by "Use this template"). It creates
   the `protect-main` ruleset: pull requests only with CODEOWNERS review,
   **squash merges only** (one commit on `main` = one approved change = the
   `source_commit` recorded on the Plan), the `protocols` CI check required,
   no force-pushes, no branch deletion, linear history, no bypass actors.
   Merging to `main` is the human sign-off — the orchestrator only executes
   protocols from `main`.
4. Replace `protocols/example-protocol.yaml` with real protocols; extend
   `schema/protocol.schema.json` as your step vocabulary grows.
5. Fill in the project-specific sections of `AGENT_RULES.md` (safety/project
   rules) and `AGENTS.md` (working conventions), and the Claude-specific block in
   `CLAUDE.md` (set the repo memory-dir path). These three files follow the
   canonical base in `ac-organic-lab`; keep the structure, add only specifics.
6. In `pins.yaml`, keep the `organic-hte-template` pin at the
   `TEMPLATE_VERSION` you stamped from, and add an `analiticadb-contract`
   pin once the project writes records. Delete the `TEMPLATE_VERSION` and
   `CHANGELOG.md` files — they belong to the template; your conformance
   declaration is the pin.

## Layout

```
├── AGENTS.md                     # shared agent working instructions (all agents); canonical base = ac-organic-lab
├── CLAUDE.md                     # Claude-Code-specific notes (imports AGENTS.md)
├── AGENT_RULES.md                # agent rules: link to lab-wide canon + project-specific
├── protocols/                    # parameterized procedures (commented YAML) — the authored layer
├── schema/protocol.schema.json   # machine-checkable protocol shape; CI validates every PR
├── analysis/                     # code that computes AnaliticaDB Analysis rows (commit-stamped)
├── configs/                      # config examples; real configs are *.local.json (gitignored)
├── pins.yaml                     # cross-repo version pins (template, AnaliticaDB contract)
├── scripts/validate_protocols.py # the CI check, runnable locally
├── scripts/check_pins.py         # upstream-drift check (non-blocking CI job)
└── .github/                      # CODEOWNERS (human sign-off) + validate workflow
```

## What the CI enforces

`scripts/validate_protocols.py` (run by `.github/workflows/validate.yaml` on
every PR, and runnable locally) checks each file in `protocols/`:

1. Parses as YAML and conforms to `schema/protocol.schema.json`.
2. `step_id`s are unique within the file.
3. The `protocol` field matches the filename.
4. On PRs: **`step_id`s that already exist on `main` are never removed or
   renamed** — notes and measurements in AnaliticaDB anchor to them. Adding
   steps is always fine.

## Versioning & staying current

Three version surfaces keep the lab's repos updatable against each other:

- **`TEMPLATE_VERSION`** (this repo) — the template contract, semver,
  bumped in the same PR as any change projects should adopt
  (`CHANGELOG.md` says what and why).
- **`pins.yaml`** (every project repo; this repo carries one as a live
  example) — the project's declaration of which upstream versions it
  conforms to: the template contract, and AnaliticaDB's ontology
  `SCHEMA_VERSION` for projects that write records (AnaliticaDB enforces
  that pin exact-match at runtime; the CI check is early warning).
- **The CI `pins` job** — re-reads each upstream on every PR and fails
  *non-blocking* (`continue-on-error`) when one moved, so drift is
  visible without freezing work. Adopting an upstream bump = one PR that
  applies the changes and updates the pin together.

## How a run flows

1. **Propose** — a protocol change arrives as a pull request (human- or
   agent-authored); the diff is the design discussion.
2. **Approve** — a CODEOWNER reviews and merges. Merge to `main` = sign-off.
3. **Run** — the orchestrator renders the protocol with per-run parameters
   and registers a `Plan` in AnaliticaDB (rendered steps, `source_commit`,
   `protocol_path`), then executes.
4. **Record** — notes, measurements, files, and analyses append in
   AnaliticaDB, anchored to the plan's `step_id`s. No run data in this repo.
