# Mermaid 12 runtime review

Reviewed September 20, 2026 for issue #96, starting from `2a54b8b8eec3e71ef7f7be2f106a706250dd7aca`.

## Publisher artifact

- Release: [Mermaid 12.0.0](https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.0.0), published September 10, 2026.
- Download: [npm publisher artifact](https://registry.npmjs.org/mermaid/-/mermaid-12.0.0.tgz), checked against [registry metadata](https://registry.npmjs.org/mermaid/12.0.0).
- Verified SHA-512 integrity: `sha512-/wQXC9iBxoGV8p3erbvaXs9h77VyLDBH6GdayVjj3hEcSQhFU4N1WUhUppotCEqlIxI2pRMwjwBSwTB1MfZBgQ==`.
- Replaced the complete minified ESM entry/chunk graph with publisher bytes and retained its LICENSE. VERSION and README now agree with the entry module. Previous runtime remains recoverable from Git history.

## Compatibility and security decisions

The release changes default layout to ELK and the appearance of several diagram types to redux-color/neo. This migration adds dagre/classic only where flowcharts previously inherited those defaults, while retaining explicitly authored neo/elk choices, brand themes, spacing, and click policy. Per-diagram configuration carries compatibility settings on pages using the shared initializer. Other page-owned initializers and the universe renderer set the same layout/look. No foundation file differs from the sibling sites as a result of this migration.

The removed defaultRenderer option occurs once as a redundant elk setting beside an existing top-level layout: elk; that diagram retains its effective request. Internal layout exports are not used here. Mindmap retains its existing cose-bilkent default and architecture retains its original configuration. Existing initialize/run/render APIs remain available. The browser floor rises to ES2024, including Safari 17.4+. Node's upstream floor is 22.12, which the repository's declared 22.19 satisfies; this change does not alter package or runtime declarations.

The tagged [configuration schema](https://github.com/mermaid-js/mermaid/blob/mermaid%4012.0.0/packages/mermaid/src/schemas/config.schema.yaml) still defaults to strict and protects securityLevel from diagram directives. The tagged [flowchart implementation](https://github.com/mermaid-js/mermaid/blob/mermaid%4012.0.0/packages/mermaid/src/diagrams/flowchart/flowDb.ts) still gates callback interaction on loose mode. Site security settings, exact link allowlists, link normalization, and restrictive CSP directives remain unchanged. CSP regeneration changes inline hashes only; no origins or capabilities were added.

## Validation

Local structural validation, generated HTML/search freshness, cache fingerprints, CSP policy checks, audit, internal links, performance budgets, and dark/light contrast checks pass. The inventory contains 56 shipped routes and 31 sitemap routes, with 23 intentional noindex exclusions.

Final local browser checks passed on Node 24.11.1, Playwright 1.63.0 and Chromium 153.0.8010.12:

- `node scripts/csp-qa.mjs --base-url=http://127.0.0.1:5017`: 56 routes, 21 inline diagrams, zero failures; includes all 15 heat-page diagrams.
- `node tests/test-universe-browser.mjs`: five additional diagrams, SVG links, 390/1440 widths, theme switching and no-JavaScript outline fallback.
- `node --test tests/mermaid-links.test.mjs`: keyboard order and link group semantics pass.
- `node scripts/phone-overflow-qa.mjs --base-url=http://127.0.0.1:5017`: all 56 routes pass at 320 pixels.
- `node scripts/responsive-qa.mjs --base=http://127.0.0.1:5017`: 560 route/viewport checks, zero failures.
- Separate actual-page inspection confirms eight allowlisted, keyboard-focusable SVG links on v2-heat-b and no page overflow at 390/1440 on both v2 heat pages and the workbench. Screenshots and logs remain in the ignored worktree `test-results/` directory.

An independent source review verified that every preexisting explicit layout/look choice remains intact, there are no duplicate configuration keys, and mindmap/architecture sources remain unchanged. The foundation audit reports the shared initializer in sync across all three local sibling checkouts.

Representative screenshots were compared with the deployed earlier runtime. Diagrams explicitly requesting ELK change geometry because Mermaid 12 now bundles that engine; their authored layout remains selected. Existing small/low-contrast labels on the large heat examples are also present in the deployed baseline and are not resolved by this migration.

Cross-origin resources are deliberately blocked in deterministic browser tests; external uptime is not claimed. The local lockfile install used a command-only `--engine-strict=false` override because this machine runs Node 24.11.1 while the repository declares 22.19.0; no engine declaration or npm policy changed. Exact declared-runtime CI and post-deployment verification remain separate release gates. Older Safari versions were not tested and are outside Mermaid 12's declared support floor.
