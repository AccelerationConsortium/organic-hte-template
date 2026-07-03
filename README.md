# sdl2-hte-template

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
5. Fill in the project-specific section of `AGENT_RULES.md`.

## Layout

```
├── AGENT_RULES.md                # agent rules: link to lab-wide canon + project-specific
├── protocols/                    # parameterized procedures (commented YAML) — the authored layer
├── schema/protocol.schema.json   # machine-checkable protocol shape; CI validates every PR
├── analysis/                     # code that computes AnaliticaDB Analysis rows (commit-stamped)
├── configs/                      # config examples; real configs are *.local.json (gitignored)
├── scripts/validate_protocols.py # the CI check, runnable locally
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

## How a run flows

1. **Propose** — a protocol change arrives as a pull request (human- or
   agent-authored); the diff is the design discussion.
2. **Approve** — a CODEOWNER reviews and merges. Merge to `main` = sign-off.
3. **Run** — the orchestrator renders the protocol with per-run parameters
   and registers a `Plan` in AnaliticaDB (rendered steps, `source_commit`,
   `protocol_path`), then executes.
4. **Record** — notes, measurements, files, and analyses append in
   AnaliticaDB, anchored to the plan's `step_id`s. No run data in this repo.
