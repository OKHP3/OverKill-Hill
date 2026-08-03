---
name: okhp3 skills scoped to other projects
description: Some .agents/skills entries in this repo are written for a sibling project, not OverKill Hill itself — check the skill's own project contract before applying it.
---

`okhp3-vite-github-pages` is a runbook for a different repo entirely: its "Project contract" section names `vite.config.ts`, `src/App.tsx` with `HashRouter`, and a GitHub Pages production base of `/kierans-lifetrkr/` (Kieran's LifeTrkr). OverKill Hill is a static HTML site served by `server.py` — no Vite, no React, no `src/` tree. Confirmed by checking for `vite.config.ts` / `src/App.tsx` (neither exists) on 2026-08-03.

**Why:** these `.agents/skills/okhp3-*` packages are shared across the author's projects and get vendored into each repo's skill directory wholesale. A skill's presence in `.agents/skills/` does not mean it targets *this* repository.

**How to apply:** before following any okhp3-* skill's specific file paths, config values, or "current facts" section, verify those paths actually exist in this repo. If they don't, the skill is out of scope here — say so rather than trying to force-fit it.
