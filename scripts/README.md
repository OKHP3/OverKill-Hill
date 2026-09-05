# OverKill Hill P³ maintenance scripts

This directory contains the scripts that are safe to use for the current
overkill-hill repository. The active scripts are the only scripts kept at
this level. Historical and manual tools are preserved in `scripts/archive/`
so they cannot be mistaken for current pipeline commands. Classification
follows the same convention as `askjamie/scripts/README.md`.

## Classification

| Script | Classification | Use |
| --- | --- | --- |
| `accessibility-qa.mjs` | active | Accessibility QA (`npm run test:*`) |
| `audit-site.py` | active | Site audit |
| `build-search-index.py` | active | Rebuild the generated search index |
| `build-site.py` | active | Regenerate HTML from `site-src/` sources |
| `cache-bust.py` | active | Cache-busting query params |
| `check-banner.py` | active | Construction-banner consistency check (invoked by `validate-site.py`) |
| `check-csp.py` | active | CI guard against CSP drift |
| `csp-qa.mjs` | active | Route-wide browser CSP and runtime QA (`npm run test:csp`) |
| `check-links.py` | active | Internal/external link check |
| `check-locale-links.py` | active | Locale link check |
| `check-mtb-version.py` | active | MTB version consistency (invoked by `post-merge.sh` and `validate-site.py`) |
| `csp.py` | active | Canonical CSP policy generation module |
| `generate-csp.py` | active | Apply CSP policies to every page |
| `lint-voice.py` | active | Voice/style lint (invoked by `validate-site.py`) |
| `phone-overflow-qa.mjs` | active | Phone-viewport overflow QA (`npm run test:*`) |
| `check-performance-budget.py` | active | Deterministic first-party asset-weight regression guard for three representative routes |
| `post-merge.sh` | active | Post-merge rebuild and validation hook |
| `responsive-qa.mjs` | active | Responsive QA entry point |
| `screen-reader-tree-audit.mjs` | active | Screen-reader accessibility tree audit (`npm run test:*`) |
| `sync-foundation-files.py` | active | Audit-first, explicit-revision sync of theme.css/app.js/mermaid-init.js across the three sibling repos |
| `test-check-banner.py` | active | Focused regression checks for localized construction-banner validation |
| `validate-site.py` | active | Structural site validation |
| `verify-live-edge.py` | active | Live-edge deployment verification |

The following scripts are **reference-only**. They may still be useful for a
deliberately scoped maintenance or migration task, but they are not part of
the current validation or release pipeline: `apply-modern-baseline.py`,
`audit-assets.py`, `audit-meta-versions.py`, `check-accent-contrast.py`,
`cross-site-sync.py`, `enhance-pages.py`, `extract-templates.py`,
`fix-audit-2026-05-12.py`, `fix-image-performance.py`,
`fix-placeholder-gpt-links.py`, `generate-illustrations.py`,
`generate-templates.py`, `inject-gpt-icon-picture.py`,
`inject-keep-exploring.py`, `inject-sparkle-loader.py`,
`inject-toolette-hub.py`, `kebab-rename-images.py`, `modernize-pages.py`,
`move-orphans-to-library.py`, `normalize-head.py`, `picture-upgrade.py`,
`png-to-webp.py`, `reclassify-construction-banners.py`,
`remove-deprecated-meta.py`, `rename-img-kebab.py`, `reorg-theme-css.py`,
`responsive-audit.py`, `sync-portfolio-stats.py`, `update-card-srcsets.py`,
`update-image-refs.py`, and `update-placeholder-dimensions.py`.

The following scripts are **retired**. They are preserved for history only
and must not be run against overkill-hill: `activate-icons.py`,
`add-toolbox-to-footer.py`, `convert-gpt-icons-webp.py`,
`convert-hero-webp.py`, `fix-banner-text.py`, `generate-feed.py`,
`inject-breadcrumb.py`, `inject-color-scheme-init.py`,
`inject-hero-picture.py`, `inject-jsonld.py`, `inject-nav-logo-webp.py`,
`inject-showcase-footer.py`, `inject-showcase-subnav.py`,
`push-to-github.py`, `release-mtb.py`, `run-viewport-qa.py`,
`site-audit.py`, `viewport-qa.py`, and `wire-illustrations.py`.

`site-audit.py` is retired rather than reference-only specifically: it is a
different, superseded tool from the active `audit-site.py` (3.3% code
similarity between the two — not a variant, a different script with a
confusingly similar name), byte-identical to glee-fullytools' own retired
copy of the same file, and had zero references anywhere in this repo,
including its own governance docs, before this move.

All reference-only and retired scripts live in `scripts/archive/`. Read
their headers and review their target paths before adapting any of them.

## Provenance

This classification and the `scripts/archive/` convention were ported from
`askjamie/scripts/README.md` as part of the 2026-08-30 scripts/ unification
pass (see `docs/sxs-infrastructure-audit-2026-08-29.md`). AskJamie triaged
this same body of shared migration tooling first; this file reclassifies
overkill-hill's copies against that precedent plus a live repo-wide
reference check (CI workflows, `post-merge.sh`, `package.json`, and
cross-script `Path(__file__)`/`subprocess` calls).

## Foundation synchronization safety contract

`sync-foundation-files.py` is read-only unless `--apply` or `--commit` is
supplied. It does not infer a canonical copy from timestamps. A write requires
both `--source-repo` and an owner-reviewed, full 40-character
`--source-revision` commit SHA; content is read from that commit, never from a
working tree. It refuses all writes when any sibling repository has a Git lock,
staged/unstaged change, or untracked file. It never moves or removes a lock.

Use a dry run to inspect divergence, then only after R04 has produced the
reviewed compatible superset, use `--apply` or `--commit` with that exact
revision. Configured post-write generators run by default. Their changed paths
are reported as generated changes and included in a `--commit`; a generator
failure prevents every commit and leaves the written paths reported for manual,
reviewed recovery. `--no-hooks` is an explicit exceptional mode, not a default.
