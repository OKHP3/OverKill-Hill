# A10: Shipped-page browser coverage and explicit failures

Status: implementation tested locally; prepared pending A07/A08 integration and CI acceptance.

Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`, initially clean detached worktree
`/Users/okh/.codex/worktrees/9108/OverKill-Hill`. Branch: `codex/remediation-a10`.
No production SHA was assumed or reverified. No owner checkout, sibling, runtime
asset, generated HTML, indexing boundary, or workflow was changed.

## Reproduction and changes

The baseline phone, responsive, route-wide ARIA, and CSP loops read 31 sitemap
routes while `build-release.py` includes 56 HTML pages. Responsive QA silently
fell back to static lint after missing Playwright or failed Chromium launch.
Responsive and static audit defaults targeted tracked documentation reports.

- `scripts/qa-release-inventory.mjs`: reads `build-release.py`'s existing
  `load_public_pages` function through Python, matching the established TOC
  suite approach. No copied route list or publication expansion.
- `scripts/phone-overflow-qa.mjs`, `responsive-qa.mjs`, `accessibility-qa.mjs`,
  `csp-qa.mjs`: use all shipped routes. All 56 were exercised; no exceptions.
  Search, 404, holding, legacy FoundRy, draft projects, and draft locales stay
  in functional coverage regardless of indexing. Historical local review HTML
  outside the allowlist remains outside runtime inventory. CSP `--paths` remains
  explicitly focused diagnostic coverage and cannot establish full coverage.
- Responsive requires browser execution by default, exits 2 with BLOCKED evidence
  when unavailable/incomplete, and closes a launched browser after errors.
  Explicit `--static` reports browser NOT RUN and `browser_acceptance: false`.
  Default JSON: `test-results/responsive-qa/results.json`; override: `--report=PATH`.
  Failure screenshots stay beside the report. Evidence includes mode, routes,
  exceptions (empty), commit, dirty state, Node/platform/architecture, and browser
  version for completed browser execution.
- `scripts/audit-site.py`: default `test-results/static-audit/report.md`; existing
  `--report PATH` preserved. Report adds static mode, commit, Python, platform.
- `tests/qa-release-inventory.test.mjs`: inventory growth without sitemap edits,
  missing Chromium, explicit static mode, and tracked-source preservation.
- `scripts/README.md`: current inventory/report contract and active helper.

These are QA source changes. No site generator must run for this package.
Reports remain machine-produced in ignored test output. Historical tracked
reports are preserved and are no longer rewritten by default.

## Verification

Host: macOS arm64, Node 26.0.0, Python 3.14.5, Chromium 151.0.7922.34.
Installed only existing package-lock dependencies with `npm ci --ignore-scripts`.
Preview: isolated worktree `server.py`, `127.0.0.1:5190`.

| Check | Actual result |
| --- | --- |
| `node --test tests/qa-release-inventory.test.mjs` | PASS, 5 tests |
| Phone overflow, `--base-url=http://127.0.0.1:5190` | PASS, 56 routes at 320px |
| Responsive, `--base=http://127.0.0.1:5190` | PASS, 560 checks, 56 routes x 10 sizes; repeated after metadata/cleanup change |
| Accessibility, same base URL | PASS, 56 route-wide checks and 4 interaction samples |
| CSP, same base URL | PASS, 56 routes, 21 Mermaid diagrams, zero route failures |
| `node --test tests/csp-qa.test.mjs` | PASS, 5 tests after approved local server/browser access |
| `python3 scripts/audit-site.py --quiet` | PASS, zero issues; ignored default report |
| `python3 tests/test-audit-site-portability.py` | PASS, 3 tests |
| `python3 tests/test-release-package.py` | PASS, 9 tests |
| `git diff --check` | PASS |

Initial dependency download and loopback binding were sandbox-blocked, then
rerun with approved access. Missing Playwright was reproduced before install;
the committed regression simulates missing Chromium through an empty browser
cache and confirms exit 2 plus BLOCKED JSON. Static lint retains its own
structural outcome but explicitly cannot satisfy browser acceptance.
Browser tests block declared cross-origin resources; they do not establish
external service availability, full WCAG conformance, or production behavior.
Local logs: `/private/tmp/a10-{phone,responsive,accessibility,csp}.log`.
Responsive evidence remains in the default ignored JSON path above.

## A21 integration requirements

A07/A08 reviewed commits were not incorporated here. This avoids overwriting
shared workflow edits. Apply this package after those upstream changes, then:

1. Run `node --test tests/qa-release-inventory.test.mjs` in validation after locked
   dependencies are installed. Python is required for the release inventory,
   including default CSP external-health discovery in the monitoring job.
2. Add an always-running upload step using the existing pinned upload action,
   retaining `test-results/responsive-qa/` and `test-results/static-audit/report.md`.
   There is no existing responsive report upload in the baseline to retarget.
   Choose missing-artifact handling to avoid obscuring an earlier failed gate.
3. Re-run all four browser gates on A08's supported runtime and the combined
   generated candidate, preserving results and their actual route counts.
4. Authorized GitHub CI rerun and A20 independent review remain unverified.

Do not call A10 fully accepted until those integration conditions are met.
No branch publication, PR, main merge, or deployment was performed.
