# A12: Featured writing and preview descriptions

Date: 2026-09-07. Disposition: prepared and locally tested; upstream integration acceptance remains open.

## Baseline and scope

Worktree: `/Users/okh/.codex/worktrees/e388/OverKill-Hill`.
Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7` (clean, detached before branch creation).
Branch: `codex/a12-featured-descriptions`. No production revision was inferred or verified.

Reproduction: homepage `latest-okh-heading` claimed the diagram writing was the most recent public work, despite the writing shelf featuring September MurderBird above the May diagram article. Vault descriptions advertised multiple download types while its available list contains one template. Workbench descriptions ended with unqualified “Build complete” while the destination is a May 2026 journal. Its JSON-LD described a SoftwareApplication.

## Authoritative changes

- `site-src/pages/index.main.html`: Featured from the Forge heading/pill and selected-writing introduction. Existing anchor, classes, link, artwork and writing retained.
- `site-src/pages.json`: standard, Open Graph and Twitter descriptions for Vault name the available template and queued resources; workbench descriptions identify the May 2026 build journal and recorded work.
- `site-src/pages/projects/mac-studio-local-ai-workbench/index.extras.html`: Article classification and matching journal description; removed application category and operating-system properties. No publication/modification dates, ratings, software maturity or current runtime proof added.

The source-only commit deliberately leaves generated integration to A21. The local generated output was reviewed and tested, then returned to the baseline bytes before committing sources. No generated files were hand-merged.

## Generation and validation evidence

System Python and bundled Python could not import Beautiful Soup. Existing `/private/tmp/okh-overkill-hill-qa-venv-20260906/bin/python` with Beautiful Soup 4.15.0 ran the checks successfully; no dependencies were added.

| Command (using that Python) | Actual result on locally generated A12 sources |
| --- | --- |
| `scripts/build-site.py` | PASS: 36 pages generated |
| `scripts/build-search-index.py` | PASS: 160 entries; owning universe generator refreshed its source/output |
| `scripts/build-site.py --check` | PASS: 36 pages |
| `scripts/build-search-index.py --check` | PASS: 160 entries |
| `scripts/validate-site.py` | PASS: 56 pages; existing locale/voice warnings retained, no new voice warnings |
| `scripts/test-seo-fixtures.py` | PASS: 15 tests |
| `scripts/check-links.py` | PASS: zero broken links, 31 sitemap URLs, 24 noindex exclusions |
| `scripts/cache-bust.py --check` | PASS: zero substitutions |
| `scripts/audit-site.py --quiet` | PASS: zero issues |
| `assets/scripts/check-contrast.py` | PASS |
| `git diff --check` | PASS |

No new test file was added for this bounded copy correction. Existing metadata fixtures and direct source/output inspection cover the changed contract. Browser/assistive-technology checks, real social-card previews, owner search-console indexing and live deployment were NOT RUN. No discoverability or performance gains are claimed.

## Integration acceptance still required

1. A06 source owner confirmed reviewed commit `8c2aaab813978bd91f2e308df0ad5973c14195cf` aligns: Vault has one template and queued artifacts; Mac journal distinguishes May history from later recorded work. This commit was not incorporated here. A21 must integrate that reviewed source and A11 status work, then confirm the descriptions remain accurate. A11 has not supplied a reviewed commit at this checkpoint.
2. Regenerate with `scripts/build-site.py`, then `scripts/build-search-index.py` (which invokes site/universe generation); rerun freshness and combined gates. Expected generated paths from A12 alone: `index.html`, `vault/index.html`, `projects/mac-studio-local-ai-workbench/index.html`, `assets/data/search-index.json`, `site-src/pages/universe/index.main.html`, `universe/index.html`. Workbench JSON-LD changes also alter CSP inline bytes; the site generator owns that output.
3. Review the three changed homepage strings using each exact locale pair. Locale report identifies French/German/Spanish homepage staleness. Locale routes, indexing policy and source hashes were not altered to hide pending review. Run the full locale report; the route-filtered report spuriously labels excluded routes orphaned and must not be treated as nine confirmed removals.
4. A21/A20 own final combined source, locale and rendered acceptance. No publication, sibling synchronization, protected writing or artwork change occurred.

## Verified closeout: September 8, 2026

The preparation status above is historical. Current GitHub main was fetched
and verified at `f4a353c323fc1caa848e03f6f0aa1ea1e520210c`.
PR #65 is merged (2026-09-08 12:10:12 UTC):
https://github.com/OKHP3/OverKill-Hill/pull/65
Its required Site Validation and i18n Page Sync checks both succeeded.

A separate integrated A12 implementation satisfies this package's requirements:
Featured labels, one-template Vault previews, historical Mac journal previews,
A06/A11 consistency and combined generation/locale review. Verified source
contracts are `assets/docs/a12-featured-descriptions-2026-09-07.md` and
`assets/docs/a21-content-integration-checkpoint-2026-09-08.md` on main;
PR #65 records the final candidate checks and independent acceptance with limits.
A bounded independent small-model review also found no missing A12 requirement.

The merged contract intentionally preserves non-description SoftwareApplication
fields. This Mac task's Article alternative is optional and was not imposed on
the integrated release. Real social-provider previews and owner indexing tools
were not exercised by this task; no discoverability gain or broader manual
accessibility completion is claimed. Broader program followups remain owned by
the integration/closeout tasks and are not A12 implementation blockers.

Original Mac source commit `e0fd2ed6cfc472e887a5179d73ad19b150ca581b`
and this disposition are preserved on GitHub branch
`codex/archive-a12-mac-20260908`. The similarly named remote feature branch
belongs to the alternate integrated implementation and was not overwritten.
Do not merge this old-baseline preservation branch into main.
A12 is complete within its assigned scope and this task can be archived.
