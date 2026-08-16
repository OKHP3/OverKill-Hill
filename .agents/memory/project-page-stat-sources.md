---
name: Project page stat sources
description: Where each project page's numeric claims come from when source-verifying against repos
---
# Project page stat sources

- Skillz page counts must match `https://okhp3.github.io/skillz/data/project-summary.json` (skillCount/familyCount/generatedAt), NOT a raw SKILL.md file count of the repo — the two differ (catalog excludes some packages). Update banner + both `data-fallback` attrs + visible text + as-of date together.
- Chai Chasers source of truth is the repo README (numbers re-measured per commit) plus `docs/DECISION-LOG.md` (settled = `| S<n>` rows; two rows share label S30 — count rows, not max ID).
- Mac Studio page carries both "29 models" (inventory storage table) and "10 local models" (README "models with routing logic") — repo docs conflict internally; both figures are repo-backed, so don't "fix" one to the other without owner input.
- BPMN page's "15-skill BP-SKILL suite" is correct even though `skills/` holds 18 SKILL.md — README defines 15 suite + 3 supplemental/meta packages.
- Under-construction pages (pathscrib-r, hometools, un-nocked-truth) and bfs-framing carry no repo-backed numeric claims.

**How to apply:** when auditing stats, fetch these sources first; only edit page numbers that a current repo artifact contradicts.
