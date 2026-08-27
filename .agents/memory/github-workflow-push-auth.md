---
name: GitHub workflow push authentication
description: The reliable Git transport and diagnosis for pushing workflow changes from this Repl.
---

When a GitHub push includes workflow files, the connected Replit GitHub OAuth identity may authenticate successfully but lack the `workflow` scope. Use the existing workflow-scoped `GITHUB_PAT` through GitHub's Basic `x-access-token` HTTP transport for the push; a Bearer header can be rejected as invalid Git credentials even when the PAT is valid.

**Why:** The repository's Git remote can select the connected OAuth credential by default, while the workspace PAT is a separate credential. GitHub's smart HTTP Git endpoint accepted the same PAT only when supplied using the standard Basic token form.

**How to apply:** First fetch and audit divergence, then obtain the user's merge/rebase choice if histories diverge. Disable terminal prompts and use a bounded push command with the PAT without printing it. Never force-push. Verify local `HEAD` and `origin/main` match after the push.