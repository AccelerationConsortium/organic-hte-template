# CLAUDE.md — Claude Code notes — PROJECT_NAME

Start with **`AGENTS.md`** — the shared, model-agnostic instruction file
(binding contract pointers, repo layout, working conventions, memory policy).
Everything there applies to Claude too. This file adds only what is specific to
Claude Code.

@./AGENTS.md

## Binding contract

`AGENT_RULES.md` (this repo → links the lab-wide canon in
`ac-organic-lab/docs/AGENT_RULES.md`) and `ac-organic-lab/docs/STATUS_SPEC.md`
are binding and take precedence. Do not weaken, bypass, or rewrite them unless
the human explicitly asks. See `AGENTS.md` §1.

## Claude-specific

<!-- Fill in when the project is stamped:
- Repo memory dir: ~/.claude/projects/<slugified-repo-path>/memory/
  One fact per file with frontmatter; index each in that dir's MEMORY.md.
  Cross-repo / MacBook-wide facts do NOT go here (see AGENTS.md §4).
- Any project-specific slash commands or skills.
-->

- **Repo memory dir:** `~/.claude/projects/<slugified-repo-path>/memory/`.
  One fact per file with frontmatter; index each in `MEMORY.md`. Cross-repo or
  MacBook-wide facts go to global memory instead (`AGENTS.md` §4), not here.
- **Skills / slash commands** are listed at session start; invoke a skill only
  when it appears in the available list. Don't guess names.
