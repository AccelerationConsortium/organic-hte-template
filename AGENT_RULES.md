# Agent rules — PROJECT_NAME

Read this before proposing or editing anything in this repo.

## Lab-wide rules (canonical — read first)

Lab-wide safety and operating rules live in
`ac-organic-lab/docs/AGENT_RULES.md` and apply to every project. This file
adds only project-specific rules and never overrides the lab-wide ones.

Rules here are guidance, not enforcement: anything safety-critical also
exists as a hard check (interlocks, CI validation, human approval gate).
The absence of a rule is not permission.

## Repo rules (every project)

1. **Protocols are the only executable artifacts.** They live in
   `protocols/` as commented YAML validated by
   `schema/protocol.schema.json`. Changes arrive by pull request; merge to
   `main` is the human sign-off; only `main` is executed.
2. **`step_id`s are permanent** once a protocol has merged and executed —
   add steps freely, never rename or reuse an id. Notes and measurements in
   AnaliticaDB anchor to them. CI rejects removals on PRs.
3. **Comments are for humans, fields are for machines.** YAML comments are
   dropped when a protocol is rendered into a database `Plan`; anything the
   executor needs must be a field. The Plan's `source_commit` points back to
   the commented source.
4. **No run data in this repo.** Measurements, summary tables, and images go
   to AnaliticaDB through its REST API. Run-specific values (plate ids,
   operator, the day's materials) belong to the per-run `Plan`, never to a
   protocol file.
5. **Never rewrite published history.** `main` is protected (no force-push,
   no deletion); corrections are new commits. The database records what ran
   regardless.
6. **Local configs stay local.** Copy `configs/*.example.json` to
   `*.local.json` (gitignored); never commit machine paths, hostnames you
   don't want published, or secrets.

## Project-specific rules

<!-- Add rules for this project: materials limits, forbidden actions,
     instrument constraints, approval thresholds. Delete this comment. -->
