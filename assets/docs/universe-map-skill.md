# Universe map skill

Canonical package: `OKHP3/skillz/mermaid/okhp3-universe-map`, version 0.1.0.
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
