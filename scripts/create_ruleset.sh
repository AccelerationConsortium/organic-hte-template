#!/usr/bin/env bash
# Create the standard `protect-main` ruleset on a project repo.
#
# Rulesets are NOT copied by "Use this template" (GitHub templates copy files
# only), so run this once per new project repo. Requires the `gh` CLI,
# authenticated with admin rights on the repo.
#
# Usage:
#   scripts/create_ruleset.sh                # current repo (from git remote)
#   scripts/create_ruleset.sh owner/repo     # explicit target
#
# What it enforces on main:
#   - changes arrive only by pull request, with CODEOWNERS review
#   - squash merges only (one commit on main = one approved change; that
#     commit hash is what the orchestrator records as Plan.source_commit)
#   - the `protocols` CI check (validate.yaml) must pass
#   - no force-pushes, no branch deletion, linear history
#   - no bypass actors
set -euo pipefail

repo="${1:-$(gh repo view --json nameWithOwner -q .nameWithOwner)}"

gh api "repos/${repo}/rulesets" --input - <<'JSON'
{
  "name": "protect-main",
  "target": "branch",
  "enforcement": "active",
  "bypass_actors": [],
  "conditions": {
    "ref_name": {
      "include": ["~DEFAULT_BRANCH"],
      "exclude": []
    }
  },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    { "type": "required_linear_history" },
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 1,
        "require_code_owner_review": true,
        "dismiss_stale_reviews_on_push": true,
        "require_last_push_approval": false,
        "required_review_thread_resolution": false,
        "allowed_merge_methods": ["squash"]
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": false,
        "required_status_checks": [
          { "context": "protocols" }
        ]
      }
    }
  ]
}
JSON

echo "ruleset 'protect-main' created on ${repo}"
