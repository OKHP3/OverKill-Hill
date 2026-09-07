# Validation and release engineering assessment - September 7, 2026

## Baseline and verdict

**AMBER: current generated/static/browser checks pass, but one reproducible macOS fixture failure and several evidence-coverage gaps remain.** This is a local assessment, not deployment approval or proof of production uptime.

- Repository: OverKill-Hill; baseline `ca38d5b9fc46746ea8b41e2ba32e39685c53f511`; initial tracked and untracked status clean.
- Environment: macOS, Python 3.14.5, Node 26.0.0, Playwright Chromium 151.0.7922.34. CI declares Python 3.11 and Node 20; this run does not establish parity with those versions.
- Python system interpreter lacked Beautiful Soup. Installed the repository's pinned `requirements-qa.txt` in ignored `.local/audit-validation-2026-09-07/venv`; blocked generated HTML and project-status checks then passed. No global package changes.
- Browser preview: repository `server.py`, loopback port 5097, stopped after each run. No source generators were run against production sources.
- Skill used: `.agents/skills/okhp3-site-release-validation/SKILL.md`. Current repository commands supersede stale skill example paths. Historical memory served only as a reminder to recheck current state; no old failure is carried forward as current evidence.

## What the current gates establish

The route helper finds **31 sitemap routes**. Structural validation passes. English generated HTML is current for **36 pages**; search is current with **160 entries**; universe, cache fingerprints, canonical CSP policies (**56 pages**), locale links, regional publication boundaries, and project-status records all pass. The project-status registry validates two records; that count does not certify all projects' claims.

The internal-link report scans **60 pages, 2,369 internal links, and 1,354 external links**, finding **zero broken internal links**, zero style issues, and no sitemap/file mismatches. The external count is an inventory, not 1,354 successful network checks. Twenty-four pages are excluded from the sitemap by explicit noindex. See `assets/audit/links-report-2026-09-07.json` and the exact listing in `.local/audit-validation-2026-09-07/gate-16.log`.

Indexing exclusions include four routes in each of `de`, `es`, `en-gb`, and `es-mx`; the legacy `/found-ry/` redirect; the Spanish-Mexico pilot review page; draft Hometools, Pathscrib-r, Un-nocked Truth, Biases as Constants, and Magnus Saga routes; and `/search/`. These are not evidence of broken navigation. A noindex page can still be visitor-accessible and needs appropriate functional coverage.

Chromium results:

| Gate | Result | Actual coverage |
|---|---|---|
| Phone overflow | PASS | 31 sitemap routes at 320×800; targeted table/card assertions on three routes |
| Responsive | PASS | 310 page×viewport rows, 31 routes × 10 sizes; no reported failures |
| Accessibility | PASS | Keyboard/focus/reduced motion on 4 representative pages; basic ARIA and diagram alternatives on 31 sitemap routes |
| CSP runtime | PASS with declared external limitations | 31 routes, 21 rendered Mermaid diagrams, zero route failures |
| Search/embed/Mermaid/CSP fixtures | PASS | 20 Node tests; none skipped |

Responsive viewport matrix: 320×720, 360×780, 375×812, 390×844, 430×932, 768×1024, 1024×768, 1280×800, 1440×900, 1920×1080. External fonts, analytics, GitHub-hosted embeds and other declared origins are blocked by deterministic browser gates and reported separately. This run cannot establish their appearance, availability, or speed. Responsive output is preserved at `.local/audit-validation-2026-09-07/responsive-results.json`; the runner's tracked default output was restored to its initial bytes after preservation.

## Fresh findings and delegated work

### V1 - Resolve canonical-path portability in the review fixture (P2, confirmed)

`tests/test-murderbird-review-boundary.py` fails at line 50 with the default macOS temporary directory. Its generated manifest URL includes `../../../../../../../../private/var/...`, while the target page uses `/var/...`. In `assets/murderbird/v2/build-library.py:37-40`, the destination is resolved before `os.path.relpath`, but the target parent is not. macOS aliases `/var` to `/private/var`, so mixing lexical and canonical paths creates a nonexistent destination. The exact default-run traceback is `fixture-05.log`.

A controlled rerun using a canonical temporary directory below `.local/audit-validation-2026-09-07/temp` passes the same test with no source edits (`review-boundary-canonical-temp.log`). This bounds the finding to symlinked-root portability; it is not a claim that deployed Pages links are broken. The builder is a preserved historical/local review utility, and the failing test is an active CI fixture.

**Worker:** first canonicalize the fixture root while preserving the archived builder bytes; if builder changes are separately authorized under its preservation contract, normalize both operands before deriving relative paths. Add a symlink-root regression that asserts generated URLs resolve to the intended files, preserve image/manifest bytes and noindex/release exclusions. **Acceptance:** default macOS test passes, canonical temporary-root test passes, release-boundary and preservation-receipt tests still pass. Since archived source bytes have a preservation receipt, review the preservation contract before editing this historical builder; a fixture-only canonical-root adaptation may be appropriate if production code remains immutable.

### V2 - Separate committed freshness from build reproducibility (P2, confirmed workflow gap)

`.github/workflows/validate.yml:55-62` runs `build-site.py` and `build-search-index.py` before later committed-freshness checks. Thus later `--check` calls prove the post-generation workspace is current, rather than proving the submitted generated files were current. The actual baseline passes direct checks before generation; there is no current generated drift.

**Worker:** run freshness checks before any mutator, or explicitly compare the tracked generated tree after regeneration and fail on differences. Keep release generation deterministic and SHA-bound. **Acceptance:** a fixture or isolated checkout with deliberately stale committed HTML/search is rejected; clean baseline passes; packaged bytes still match release provenance.

### V3 - Use the release inventory for functional coverage (P2, confirmed coverage gap)

The release builder includes **56 HTML pages**, but phone, responsive, route-wide ARIA and CSP loops use only the **31 sitemap routes**. Their labels say public routes, but their scope is indexable routes. `/search/` has dedicated regressions, `/404.html` has representative accessibility checks, and the TOC suite already uses the broader release inventory, so coverage is not absent everywhere. The gap is consistent route-wide browser checks for shipped noindex pages and utilities.

**Worker:** derive shipped HTML inventory from `build-release.py` for runtime/overflow checks; preserve sitemap-only assertions for indexing. Partition intentional redirects/reviews/utility behavior explicitly. **Acceptance:** every shipped route is either tested or has a named, justified exception; locale drafts remain noindex and absent from sitemap/search; no publication expansion.

### V4 - Fail explicitly when responsive browser dependencies are unavailable (P2, confirmed)

`scripts/responsive-qa.mjs:82-96,405-419` returns to static analysis when Playwright loading or Chromium launch fails. The static report labels its mode, but a successful process exit can be mistaken for completed browser QA. Other CI browser gates launch Chromium directly and would normally fail, which limits the current release risk.

**Worker:** require browser mode by default or add a mandatory `--require-browser` CI/local gate; retain static analysis only as an explicitly selected mode. **Acceptance:** simulated missing launch yields nonzero status and clear NOT RUN/BLOCKED evidence; explicit static mode is labeled and cannot satisfy browser acceptance; normal Chromium suite still passes.

### V5 - Add measured performance and broader accessibility evidence (P2, proposal)

`check-performance-budget.py` explicitly measures source assets rather than transfer bytes or Core Web Vitals. It sums all srcset candidates and local CSS dependencies, ignores external resources, iframe contents, dynamic requests, compression and caching. Current passes are **5,451,266 / 5,767,168 bytes** for `/`, **3,522,173 / 4,194,304** for the main article, and **431,286 / 655,360** for MTB. These source totals are optimization leads, not actual page-load measurements.

Accessibility QA is a focused custom regression suite, as its own header states. Four interaction samples and basic ARIA checks do not establish full WCAG conformance; Chromium-only execution does not establish Safari/Firefox behavior. Contrast token pairs do not cover every rendered text/image/overlay combination.

**Workers:** add repeatable cold/warm load evidence on representative real pages, distinguishing first-party and external costs; exercise browser-selected image sizes and lazy loading. Evaluate an established automated accessibility engine as an optional proposal requiring a separate explicit dependency request before installation; retain existing behavioral tests and add manual keyboard/screen-reader review of navigation, search, contact, locales, long articles and embeds. **Acceptance:** retain device/network/cache settings, concrete violations and traces, check light/dark/reduced-motion states, and report external failures separately. Set performance targets after measurements rather than lowering artwork quality based on source totals alone.

### V6 - Avoid ambiguous generated audit output (P3, confirmed)

The responsive runner writes machine-generated `assets/docs/responsive-qa/results.json` to a tracked path; a fresh audit changes it even without source changes. This contradicts the governance placement distinction between human reports and machine QA output. `audit-site.py --quiet` also writes its default Markdown report, although it produced no tracked diff in this run.

**Worker:** add explicit report output arguments and direct default machine results to `assets/audit/` or ignored test output; update CI artifact upload paths. **Acceptance:** read-only audit operation leaves tracked sources unchanged, results retain environment/commit/mode, existing consumers remain valid.

## Strengths worth retaining

The Pages pipeline validates a release revision, builds an allowlisted artifact, verifies downloaded hashes/commit identity, and deploys that artifact. Seven release-package regressions passed, including source/media exclusion and tamper checks. HTML/source/SEO, canonical CSP discovery, explicit locale publication boundaries, preserved artwork hashes and accepted derivative registers have focused regression tests. The broad static suite and deterministic browser suites are substantive controls, not just lint claims. Preserve them during improvements.

## Exact command ledger

All paths below are local retained logs under the baseline run folder. A dependency-blocked first attempt is included transparently and superseded only by its successful pinned-venv rerun. The failing review fixture remains a failure under the default host environment despite its diagnostic canonical-root pass.

| Status | Command | Evidence |
|---|---|---|
| PASS | `python3 .agents/skills/okhp3-site-release-validation/scripts/inventory-routes.py --root . --sitemap sitemap.xml --origin https://overkillhill.com` | `.local/audit-validation-2026-09-07/gate-04.log` |
| PASS | `python3 scripts/validate-site.py` | `.local/audit-validation-2026-09-07/gate-05.log` |
| BLOCKED (dependency; rerun passes) | `python3 scripts/build-site.py --check` | `.local/audit-validation-2026-09-07/gate-06.log` |
| PASS | `python3 scripts/build-search-index.py --check` | `.local/audit-validation-2026-09-07/gate-07.log` |
| PASS | `python3 scripts/sync-universe-map.py --check` | `.local/audit-validation-2026-09-07/gate-08.log` |
| PASS | `python3 scripts/cache-bust.py --check` | `.local/audit-validation-2026-09-07/gate-09.log` |
| PASS | `python3 scripts/generate-csp.py --check` | `.local/audit-validation-2026-09-07/gate-10.log` |
| PASS | `python3 scripts/check-csp.py` | `.local/audit-validation-2026-09-07/gate-11.log` |
| PASS | `python3 scripts/check-locale-links.py` | `.local/audit-validation-2026-09-07/gate-12.log` |
| BLOCKED (dependency; rerun passes) | `python3 scripts/check-project-status.py` | `.local/audit-validation-2026-09-07/gate-13.log` |
| PASS | `python3 scripts/check-performance-budget.py` | `.local/audit-validation-2026-09-07/gate-14.log` |
| PASS | `python3 scripts/audit-site.py --quiet` | `.local/audit-validation-2026-09-07/gate-15.log` |
| PASS | `python3 scripts/check-links.py` | `.local/audit-validation-2026-09-07/gate-16.log` |
| PASS | `python3 assets/scripts/check-contrast.py` | `.local/audit-validation-2026-09-07/gate-17.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python scripts/build-site.py --check` | `.local/audit-validation-2026-09-07/fixture-00.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python scripts/check-project-status.py` | `.local/audit-validation-2026-09-07/fixture-01.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python scripts/test-seo-fixtures.py` | `.local/audit-validation-2026-09-07/fixture-02.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python tests/test-audit-site-portability.py` | `.local/audit-validation-2026-09-07/fixture-03.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python tests/test-release-package.py` | `.local/audit-validation-2026-09-07/fixture-04.log` |
| FAIL | `.local/audit-validation-2026-09-07/venv/bin/python tests/test-murderbird-review-boundary.py` | `.local/audit-validation-2026-09-07/fixture-05.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python -m unittest tests/test_verify_live_edge.py` | `.local/audit-validation-2026-09-07/fixture-06.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python -m unittest tests/test-sync-foundation-files.py` | `.local/audit-validation-2026-09-07/fixture-07.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python -m unittest tests/test-i18n-release.py` | `.local/audit-validation-2026-09-07/fixture-08.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python tests/test-homepage-hero-parity.py` | `.local/audit-validation-2026-09-07/fixture-09.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python scripts/build-murderbird-release-register.py --check` | `.local/audit-validation-2026-09-07/fixture-10.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python tests/test-murderbird-still-release.py` | `.local/audit-validation-2026-09-07/fixture-11.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python tests/test-murderbird-png-fallback.py` | `.local/audit-validation-2026-09-07/fixture-12.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python tests/test-review-closeout.py` | `.local/audit-validation-2026-09-07/fixture-13.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python scripts/check-regional-drafts.py` | `.local/audit-validation-2026-09-07/fixture-14.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python scripts/test-check-banner.py` | `.local/audit-validation-2026-09-07/fixture-15.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python tests/test_csp_page_discovery.py` | `.local/audit-validation-2026-09-07/fixture-16.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python tests/test-template-conflict-markers.py` | `.local/audit-validation-2026-09-07/fixture-17.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python -m unittest tests/test-performance-budget.py` | `.local/audit-validation-2026-09-07/fixture-18.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python tests/test-universe-integration.py` | `.local/audit-validation-2026-09-07/fixture-19.log` |
| PASS | `.local/audit-validation-2026-09-07/venv/bin/python .agents/skills/okhp3-universe-map/tests/test-universe-map.py` | `.local/audit-validation-2026-09-07/fixture-20.log` |
| PASS | `node scripts/phone-overflow-qa.mjs --base-url=http://127.0.0.1:5097` | `.local/audit-validation-2026-09-07/browser-0.log` |
| PASS | `node scripts/responsive-qa.mjs --base=http://127.0.0.1:5097` | `.local/audit-validation-2026-09-07/browser-1.log` |
| PASS | `node scripts/accessibility-qa.mjs --base-url=http://127.0.0.1:5097` | `.local/audit-validation-2026-09-07/browser-2.log` |
| PASS | `node scripts/csp-qa.mjs --base-url=http://127.0.0.1:5097` | `.local/audit-validation-2026-09-07/browser-3.log` |
| PASS | `node --test tests/search-page.test.mjs tests/search-index.test.mjs tests/search-index-locale.test.mjs tests/embed-workflow.test.mjs tests/mermaid-links.test.mjs tests/csp-qa.test.mjs` | `.local/audit-validation-2026-09-07/browser-4.log` |

## Limits and unexecuted gates

This worker did not rerun external archive destinations, production-edge monitoring, real third-party runtime monitoring, field Core Web Vitals, Safari/Firefox/device accessibility, or deployment. Other assessment workers may supply that evidence. No claim of full CI parity or production readiness follows from this report. Source and generated-site files were not modified during baseline assessment; only permitted reports and ignored local evidence were produced.

## Supplemental baseline checks

- PASS: `node scripts/toc-follow-qa.mjs --base-url=http://127.0.0.1:5097` - inventory 56 shipped pages; all 14 sidebar menus and legacy MediaQueryList behavior pass. Evidence: `.local/audit-validation-2026-09-07/toc.log`.
- PASS: `node tests/test-universe-browser.mjs` - 5 diagrams, SVG links, 31-page outline, two widths, theme switch, no-JavaScript fallback. Evidence: `.local/audit-validation-2026-09-07/universe-browser.log`.

## Authorized documentation correction after baseline

The first documentation correction changed `replit.md` after baseline testing to correct the foundation sync runbook: explicit source repository/full immutable SHA, no timestamp winner, clean-checkout/lock preflight, accounted post-write generation and commits. No sync operation ran and no sibling files changed.

Also corrected the false claim that active MTB `--update` and `--dry-run` flags are historical-only: the current script supports both. Distinguished read-only modes from the optional auto-fixer and retained source-first regeneration guidance. Marked the old SEO count and deferred list as historical so it cannot masquerade as the current backlog.

Verification: read actual command source; ran `python3 scripts/sync-foundation-files.py --help` and `python3 scripts/check-mtb-version.py --help`; documentation diff checked. These edits do not remediate the fresh portability or coverage findings above.


Additional authorized documentation corrections: `docs/publishing.md` now describes the one-repository review/Pages artifact flow, marks the PAT writer as archived, uses the current direct-Pages verification flags, and labels September 3 observations as historical. `ROADMAP.md` records verified script CSP hardening and analytics disclosure, retains the historical Shipped section, and points proposed priorities to the Architect's advancement plan. No credentials, account permissions, remote refs or deployments changed.
