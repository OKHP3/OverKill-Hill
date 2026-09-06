# Comprehensive assessment: validation record

Run date: September 5, 2026, America/Chicago. Live observations cross into September 6 UTC.

## Identity and environment

- Owner checkout: `897df5d33202bd65924f9f3a35c84e0068cbee02`, preserved.
- Independent audit snapshot: `40e18ee7916f4a54196cc407d60999ba1d786d11`.
- Runtime: macOS ARM64, Python 3.14.5, Node 26.0.0, installed Playwright 1.62.1 / Chromium 151.0.7922.34 (cache 1234). This differs from CI Python 3.11 / Node 20.
- Existing pinned `requirements-qa.txt` installed in a disposable virtual environment; existing Playwright reused. No repository dependencies or lockfiles changed.
- Preview: repository server on `http://127.0.0.1:5057`, loopback explicitly selected. All test writes occurred in the isolated snapshot; selected evidence copied back.
- Durable evidence: `assets/audit/comprehensive-2026-09-05/checks/`. Logs may be ignored by Git but remain available locally.

## Static and fixture commands

Commands below ran from the frozen snapshot with its temporary virtual environment first on PATH.

| Check | Command | Initial result | Evidence |
| --- | --- | --- | --- |
| structural | `python3 scripts/validate-site.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/structural.log) |
| route-inventory | `python3 .agents/skills/okhp3-site-release-validation/scripts/inventory-routes.py --root . --sitemap sitemap.xml --origin https://overkillhill.com` | PASS | [log](../audit/comprehensive-2026-09-05/checks/route-inventory.log) |
| generated-html | `python3 scripts/build-site.py --check` | PASS | [log](../audit/comprehensive-2026-09-05/checks/generated-html.log) |
| search-index | `python3 scripts/build-search-index.py --check` | PASS | [log](../audit/comprehensive-2026-09-05/checks/search-index.log) |
| cache | `python3 scripts/cache-bust.py --check` | PASS | [log](../audit/comprehensive-2026-09-05/checks/cache.log) |
| static-audit | `python3 scripts/audit-site.py --quiet --report <external-report.md>` | PASS | [log](../audit/comprehensive-2026-09-05/checks/static-audit.log) |
| internal-links | `python3 scripts/check-links.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/internal-links.log) |
| locale-links | `python3 scripts/check-locale-links.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/locale-links.log) |
| contrast | `python3 assets/scripts/check-contrast.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/contrast.log) |
| csp-generation | `python3 scripts/generate-csp.py --check` | PASS | [log](../audit/comprehensive-2026-09-05/checks/csp-generation.log) |
| csp-static | `python3 scripts/check-csp.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/csp-static.log) |
| project-status | `python3 scripts/check-project-status.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/project-status.log) |
| regional-drafts | `python3 scripts/check-regional-drafts.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/regional-drafts.log) |
| performance-budget | `python3 scripts/check-performance-budget.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/performance-budget.log) |
| seo-fixtures | `python3 scripts/test-seo-fixtures.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/seo-fixtures.log) |
| audit-portability | `python3 tests/test-audit-site-portability.py` | FAIL | [log](../audit/comprehensive-2026-09-05/checks/audit-portability.log) |
| release-package | `python3 tests/test-release-package.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/release-package.log) |
| live-edge-regressions | `python3 -m unittest tests/test_verify_live_edge.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/live-edge-regressions.log) |
| foundation-sync-regressions | `python3 -m unittest tests/test-sync-foundation-files.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/foundation-sync-regressions.log) |
| i18n-release-regressions | `python3 -m unittest tests/test-i18n-release.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/i18n-release-regressions.log) |
| hero-parity | `python3 tests/test-homepage-hero-parity.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/hero-parity.log) |
| banner-regressions | `python3 scripts/test-check-banner.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/banner-regressions.log) |
| csp-discovery | `python3 tests/test_csp_page_discovery.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/csp-discovery.log) |
| merge-markers | `python3 tests/test-template-conflict-markers.py` | PASS | [log](../audit/comprehensive-2026-09-05/checks/merge-markers.log) |
| performance-regressions | `python3 -m unittest tests/test-performance-budget.py` | FAIL | [log](../audit/comprehensive-2026-09-05/checks/performance-regressions.log) |
| csp-browser-fixtures | `node --test tests/csp-qa.test.mjs` | PASS | [log](../audit/comprehensive-2026-09-05/checks/csp-browser-fixtures.log) |
| search-embed-fixtures | `node --test tests/search-page.test.mjs tests/search-index.test.mjs tests/search-index-locale.test.mjs tests/embed-workflow.test.mjs` | PASS | [log](../audit/comprehensive-2026-09-05/checks/search-embed-fixtures.log) |

Initial result: 25 command groups passed, two portability groups failed. The failures were not hidden by later successes.

### Resolved-path diagnostic reruns

`TMPDIR=/private/tmp/okh-assessment-20260905-oiP7ek` was supplied to both failing commands. No source was modified.

- Audit portability: 3 tests pass with canonical TMPDIR; ordinary Mac temporary-root run fails one test.
- Performance fixtures: 5 tests pass with canonical TMPDIR; ordinary run errors in two tests.
- Cause: helpers compare resolved `/private/var/...` resource paths with unresolved `/var/...` roots. Treat as a remaining portability defect.
- Evidence: [audit rerun](../audit/comprehensive-2026-09-05/checks/audit-portability-canonical-temp.log), [performance rerun](../audit/comprehensive-2026-09-05/checks/performance-regressions-canonical-temp.log).

## Browser checks

| Command | Result | Coverage and limitation |
| --- | --- | --- |
| `node scripts/phone-overflow-qa.mjs --base-url=http://127.0.0.1:5057` | PASS | 31 sitemap routes at 320px; targeted table/grid assertions |
| `node scripts/responsive-qa.mjs --base=http://127.0.0.1:5057` | PASS | Real Playwright mode, 31 routes × 10 widths = 310 combinations, zero failures; sizes 320/360/375/390/430/768/1024/1280/1440/1920 |
| `node scripts/accessibility-qa.mjs --base-url=http://127.0.0.1:5057` | PASS | Four representative task pages plus 31 public routes; no formal WCAG certification |
| `node scripts/screen-reader-tree-audit.mjs --base-url=http://127.0.0.1:5057` | PASS | Six pages using Chromium CDP accessibility tree; no real screen-reader session |
| `node scripts/csp-qa.mjs --base-url=http://127.0.0.1:5057` | PASS | 31 routes, 22 Mermaid diagrams, zero route failures; cross-origin requests deliberately blocked by this deterministic gate |

The initial CSP-browser invocation mistakenly supplied `--report` without `--external-health`; the CLI rejected it before testing. That was an audit harness argument error. The exact supported command above then passed; both logs are retained. Browser tests that deliberately block external requests do not establish third-party uptime.

Focused live browser probes separately reproduced defects missed by these suites: skip continuation, JS-disabled content, short-height menu, exact breakpoint, reduced-motion transforms, search selection/shortcuts/semantics/snippets and hero gutters. See the [UI report](audit-ui-ux-2026-09-05.md) and its `ui-*.json` evidence. A later JavaScript-enabled control/treatment test confirmed that blocking only app.js leaves all eight homepage reveal containers transparent; the control reaches opacity one. See `disruptor-blocked-app-js.json`.

Screenshots were relocated to `assets/audit/screenshots/comprehensive-2026-09-05/`; raw capture paths in machine evidence describe their original capture location.

## Live and external checks

| Check | Result | Evidence |
| --- | --- | --- |
| GET every release HTML route and compare LF-normalized body | PASS: 56/56 HTTP 200, 56/56 match frozen source | [parity JSON](../audit/comprehensive-2026-09-05/checks/live-route-parity.json) |
| `python3 scripts/check-links.py --external-archives` | PASS: seven article links, seven destinations | [external archive log](../audit/comprehensive-2026-09-05/checks/external-archives.log) |
| Public release manifest and latest successful Pages run | Same `40e18ee7` SHA | Security report and downloaded API evidence |
| CI post-deploy edge report | PARTIAL: 427 checks, 0 failures, 38 blocked, 315 warnings | [complete report](../audit/comprehensive-2026-09-05/ci-live-edge/live-edge-report.json) |
| Fresh header GET samples | Expected content reachable, desired headers absent | [headers JSON](../audit/comprehensive-2026-09-05/live-security-headers.json) |
| Npm advisory query | Zero returned advisories for QA dependency tree | [npm audit](../audit/comprehensive-2026-09-05/npm-audit.json); not runtime/vendor-wide clearance |
| Copied release JS alteration then verifier | Verifier accepts changed JS, confirming limited digest coverage | [negative probe](../audit/comprehensive-2026-09-05/release-integrity-probe.json) |
| Network samples | Eight initial-load diagnostics; no field-performance claim | [samples](../audit/comprehensive-2026-09-05/checks/network-samples.json) |

The direct `/404.html` document returning 200 is expected for a named file. The 56-route pass does not test the HTTP status of every invented missing route. Excluded governance paths received 404 in separate sampled requests.

## Checks not run or not established

- Formal WCAG conformance, real VoiceOver/NVDA, Safari/Firefox/device matrix, exhaustive zoom/text-spacing/forced-color and rendered-state contrast.
- Field Core Web Vitals, Search Console indexing/ranking, real inquiry conversion, email delivery, and representative usability study.
- Complete external application functions, authenticated Replit production configuration, DNS/registrar controls, and Analytics account policy.
- All downloadable PDF/PowerPoint content and their accessibility. Only link/asset scope described above was checked.
- Complete Python/vendor advisory inventory, adversarial penetration test, secret-history audit or supply-chain certification.
- Native-language quality certification or scientific replication of the archived Diagram experiment.

These remain explicit follow-up boundaries. No not-run check is counted as passing. The site is reachable and its tested release content is current; acceptance of the recommendation packet does not certify the site or authorize implementation.
