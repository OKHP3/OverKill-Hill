---
name: Repository janitor SSH prompt
description: The branch audit can traverse transient Replit remotes and trigger SSH prompts unless Git is forced into noninteractive batch mode.
---

Run branch audits with terminal prompts disabled and SSH in batch mode when the checkout contains transient `subrepl-*` remotes.

**Why:** The audit script refreshes all remotes, and Replit-generated SSH remotes can otherwise block the audit on an interactive password prompt even though the GitHub `origin` sync is healthy.

**How to apply:** Set `GIT_TERMINAL_PROMPT=0` and `GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=3'` for audit-only fetches. Never use those transient remotes for the user's GitHub pull/push.