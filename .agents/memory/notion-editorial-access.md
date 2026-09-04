---
name: Notion editorial access
description: Reusable constraints for using the connected Notion workspace as an editorial staging surface.
---

An authorized Notion connection can still be unbound from the current Replit environment. Bind the existing connection before attempting page search or content reads. Notion search is title-oriented, so resolve likely page records first and fetch their properties and block children explicitly. Treat a successful content write as staged review material, not as owner sign-off; preserve the pending-review state until a human approves it.

**Why:** A configured workspace is not proof that the current environment can use it, and title matches alone do not establish that a page contains the intended editorial source.

**How to apply:** For future editorial passes, verify the connection state, search by route or project title, fetch the canonical page and any linked content page, check comments, stage notes on an existing appropriate review record, and export the same record into the repository without committing account-specific Notion IDs or URLs.