---
name: Brand style registry location
description: Where the OverKill Hill visual style profile lives now that it's project-owned, vs. the skill's bundled seed copy.
---

The `okhp3-brand-style-registry` skill ships an example/seed profile at `.agents/skills/okhp3-brand-style-registry/assets/profile-seeds/overkill-hill.yaml`. That seed is not the live source of truth — it's reference material bundled with the skill package.

On 2026-08-03 the profile was promoted into a project-owned registry at `brand-styles/registry.yaml` + `brand-styles/profiles/overkill-hill.yaml` (status `active`), after re-verifying every declared token (colors, spacing, radius, shadow, content width, font roles) against the live `assets/css/theme.css` and confirming they still matched exactly.

**Why:** the skill's Phase 2 storage model expects a project-level registry, not reliance on the bundled seed, so future style work has a place to record real changes/versions without touching the skill package itself.

**How to apply:** when doing brand/style work on this repo, read and update `brand-styles/profiles/overkill-hill.yaml`, not the skill's seed copy. Bump `version`/`updated_on` on real token changes rather than silently editing in place.
