# Universe map skill

Canonical package: `OKHP3/skillz/mermaid/okhp3-universe-map`, version 0.1.2.
Installed copy: `.agents/skills/okhp3-universe-map/SKILL.md`.
Site configuration: `universe-map.config.json`.

From the repository root:

```text
py -3 -B .agents/skills/okhp3-universe-map/scripts/build-universe-map.py --config universe-map.config.json --output assets/audit/universe-map --write
py -3 -B .agents/skills/okhp3-universe-map/scripts/build-universe-map.py --config universe-map.config.json --output assets/audit/universe-map --check
```

Use `python3` instead of `py -3` on Linux/macOS. Rebuild the search index first.
The retained artifacts are staging outputs, not the published universe page.
The skill's `references/integration.md` defines the page-build integration,
search feedback exclusion, render checks, and peer-refresh contract.
Installing the skill does not schedule execution or change deployment.

Keep configuration outside the shared package. Update the canonical source first,
inspect divergence before copying, and verify SHA-256 equality across all core files.
No planned concepts were inferred or imported from the old diagrams.

## Published integration

`scripts/build-search-index.py` now refreshes the universe source block and
rebuilds published HTML after writing the default index. The release workflow
also runs `scripts/sync-universe-map.py` before validation and checks freshness.
Generated navigation is excluded from search text to prevent a feedback loop.
The page uses strict Mermaid rendering with safe same-origin SVG links and an
ordinary linked outline. Sibling universe links lead to their own current maps.
The original conceptual page is preserved in
`docs/archive/2026-09-06-universe-map-handwritten.md`.
