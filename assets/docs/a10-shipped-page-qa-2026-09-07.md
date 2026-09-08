# A10: Shipped-page QA coverage

Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`. Implementation is isolated
on `codex/a10-shipped-page-qa`. No content, generated pages, sitemap, search,
locale policy, release builder, dependencies, or sibling files changed.

## Changes and dependency contracts

V3 is reproduced: four functional loops previously consumed 31 sitemap routes.
They now share the release builder's read-only `load_public_pages` inventory.
All 56 shipped HTML routes are tested, including noindex drafts, review pages,
utilities, and the legacy Found-Ry notice. There are zero exceptions. Indexing
checks remain separate. ARIA/diagram checks cover every route; keyboard/focus
and reduced-motion interaction checks remain four representative samples.

V4 is reproduced by injected import and launch failures: both previously
returned success after static fallback. Browser execution is now mandatory by
default. Missing Playwright/Chromium produces nonzero status and JSON with
`BLOCKED`, browser acceptance `NOT RUN`, and zero checked pages. Explicit
`--static` remains structural lint only and records browser acceptance `NOT RUN`.

V6 is corrected: responsive JSON defaults to ignored
`test-results/responsive-qa/results.json`; `--report=<path>` selects another
destination. Audit-site retains `--report <path>` and defaults to ignored
`test-results/audit-site/report.md`. Reports record commit, environment, and
mode; responsive reports also record inventory and browser version. Existing
tracked historical reports remain intact. CI uploads the new output folders.

A07 confirmed the inventory API unchanged, then delivered
`7f4aa0b15c5c676c1a1babb113c30428c85158bf`. A08 confirmed Node 24, unchanged
dependencies/API, then delivered `f524d7fc31303d18fca826394746c031cba9418e`.
A21 confirmed independent integration of both contracts. This patch adds only
the QA regression command and report upload step to the workflow; preserve
A07 pre-generation checks/output propagation and A08 Node selectors when
integrating. No upstream branch was merged into this worker checkout.

## Local evidence

Environment: Windows x64, Node 24.11.1, Chromium 151.0.7922.34, Python
3.14.0rc1. Existing dependencies installed with `npm ci --ignore-scripts
--no-audit --no-fund`; no dependency graph changes. Preview is this checkout's
`server.py`, bound to `127.0.0.1:5107`.

| Check | Result |
| --- | --- |
| `node --test tests/release-qa-inventory.test.mjs tests/responsive-mode.test.mjs` | PASS, 5 tests; new noindex fixture discovery, excluded template, import/launch failures, explicit static mode and tracked diff preservation |
| `node --test tests/csp-qa.test.mjs` | PASS, 5 existing CSP/external regression tests (also run together with the original 4 QA tests) |
| `py tests/test-audit-site-portability.py` | PASS, 3 tests including new default report path case, relative/absolute overrides and encoding |
| `node scripts/phone-overflow-qa.mjs --base-url=http://127.0.0.1:5107` | PASS, 56 routes at 320px |
| `node scripts/responsive-qa.mjs --base=http://127.0.0.1:5107 --report=.local/a10/final-responsive.json` | PASS, 560 checks, 56 routes by 10 viewports, zero failures |
| `node scripts/accessibility-qa.mjs --base-url=http://127.0.0.1:5107` | PASS, 56 route-wide checks and 4 representative interactions |
| `node scripts/csp-qa.mjs --base-url=http://127.0.0.1:5107` (final isolated full sweep) | PASS, 56 routes, 21 rendered diagrams, zero route failures |
| `py scripts/audit-site.py --quiet` | PASS, zero issues, ignored report output |
| `py scripts/check-regional-drafts.py` | PASS, eight regional routes remain noindex and absent from search/public alternates |
| `py scripts/build-site.py --check` | PASS, 36 generated pages current |
| `py scripts/build-search-index.py --check` | PASS, 160 entries current |

Logs and full responsive JSON are retained in ignored `.local/a10/`. Tests were
run against the baseline plus this scoped uncommitted implementation; report
commit fields identify the baseline. No generators were used to repair source.

## Explicit limits

The first full CSP sweep under concurrent browser load failed on two already
indexable article heat routes: v1-heat-a rendered 1/4 diagrams and v1-heat-b
rendered 2/3. A focused isolated rerun passed both (7/7 diagrams). The original
failure remains in `.local/a10/csp.log`; isolated evidence is in
`.local/a10/csp-isolated.log`. This suggests timing sensitivity in the existing
fixed-delay CSP runner; it is not proof of a production defect or its repair.
The final full sweep without competing browser suites passed all 56 routes and
21 diagrams; `.local/a10/csp-final.log` retains that result.

Third-party resources are intentionally blocked in deterministic browser QA.
External uptime, full WCAG conformance, assistive-technology sessions, other
browsers, CI execution, merge, deployment, and production acceptance are not
established by this worker. A21 owns combined candidate acceptance.
