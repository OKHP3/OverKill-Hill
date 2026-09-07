# A08: Supported QA runtime

September 7, 2026. D03, P1. Status: local implementation prepared for A21 integration; combined CI and Replit execution remain unverified.

## Baseline and reproduction

Isolated worktree: `/Users/okh/.codex/worktrees/4bf9/OverKill-Hill`.
Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`, including A01/A02.
Branch: `codex/a08-supported-qa-runtime`. This handoff accompanies the package commit; obtain its SHA with `git log -1 --format=%H -- assets/docs/remediation-a08-2026-09-07.md`.
No production SHA or live deployment was queried or assumed current.

At baseline both active Node setup steps in `.github/workflows/validate.yml`
selected Node 20. `.replit` declared `nodejs-20`. The local default was Node
26.0.0/npm 11.12.1, with no repository engine constraint or version selector.
The [official release table](https://nodejs.org/en/about/previous-releases),
retrieved September 7, 2026, lists Node 20 as end-of-life, Node 24 as LTS,
and Node 26 as Current. Node 24 is the selected QA major.

## Changes and source ownership

- `.nvmrc`: shared local/CI selector, `24`; use the latest available 24.x patch.
- `.npmrc`: `engine-strict=true`, rejecting incompatible npm installation.
- `package.json`: `engines.node` is `>=24 <25`.
- `package-lock.json`: npm-generated root engine metadata only. All dependency versions, integrity hashes, URLs, and package entries are unchanged.
- `.github/workflows/validate.yml`: both setup-node steps read `.nvmrc`. No other workflow changes.
- `README.md`: local setup, major-update procedure, static delivery distinction, and preview assessment link.
- This handoff: reproduction, test evidence, and integration limits.

No site source, HTML, shared runtime, artwork, locale, indexing, publication
allowlist, or dependency change. No site regeneration is required. For future
engine changes, regenerate lock metadata with `npm install --package-lock-only
--ignore-scripts`, then review it and run clean `npm ci`; do not hand-merge the
lockfile. Responsive QA wrote its usual tracked result file; its transient
output was copied to `/private/tmp/a08-responsive-results.json` and the original
tracked bytes restored, so it is excluded from this package.

## Runtime and validation evidence

Official macOS arm64 Node 24.20.0/npm 11.19.0 was extracted into
`/private/tmp/a08-runtime/node-v24.20.0-darwin-arm64/`. Archive SHA-256
`40e5607e5ecb3db9192723776da2d75d966260fc74a7a9e731c1bd67dda96bc8`
matched the [official checksums](https://nodejs.org/dist/v24.20.0/SHASUMS256.txt).
This temporary installation does not change the machine's default Node.

Clean installation: `npm ci --cache /private/tmp/a08-npm-cache --no-audit
--no-fund`, with that Node directory first in PATH, exited 0 and installed the
three existing packages. npm 11.19.0 reported an optional `fsevents@2.3.2`
install-script approval warning; no approval or dependency change was added.
Node 26 `npm ci --dry-run --ignore-scripts --offline` exited 1 with EBADENGINE,
confirming the local installation contract rejects the previous default.

Playwright 1.62.1 used its existing Chromium revision 1234 installation
(browser metadata 151.0.7922.34). The first sandboxed browser/loopback attempt
was blocked by macOS permissions and was stopped; it is not passing evidence.
The following suites ran with approved browser/loopback access against this
worktree, using `HOST=127.0.0.1 PORT=18088 python3 server.py` where needed.

| Check | Actual result |
| --- | --- |
| Node CSP, search-page, search-index, locale-index, embed-workflow, Mermaid-link fixtures | 20 passed, 0 failed, 0 skipped |
| Phone overflow | Passed |
| Responsive browser QA | 310 checks, 0 failures, actual browser execution |
| TOC follow | Passed all 14 release sidebar menus and legacy MediaQueryList regression |
| Accessibility QA | Passed 4 representative pages and 31 public routes |
| CSP route browser QA | Passed: 31 routes, 21 Mermaid diagrams, 0 route failures; expected blocked third-party requests reported |
| Universe browser test | Passed: 5 diagrams, SVG links, 31-page outline, two widths, theme switching, no-JavaScript fallback |
| `scripts/validate-site.py` | Passed, 0 errors, 32 structural warnings and no new voice warnings beyond baseline |
| `scripts/build-site.py --check` | Passed for 36 generated pages |
| `scripts/build-search-index.py --check` | Passed, 160 entries |
| Dependency inventory comparison | All non-root lockfile package entries and root dependencies identical to baseline |
| CI version references / `git diff --check` | Both jobs read `.nvmrc`; whitespace check passed |

HTML freshness initially could not import Beautiful Soup in system Python.
It passed with the existing `/private/tmp/okh-overkill-hill-qa-venv-20260906`
environment (Beautiful Soup 4.15.0). Browser suites that invoke Python used this
environment in PATH. This is not evidence of a clean Python dependency install.
Local logs are `/private/tmp/a08-node-fixtures-permitted.log`,
`/private/tmp/a08-{phone,responsive,toc,accessibility,csp,universe}.log`,
`/private/tmp/a08-browser-results.json`, and `/private/tmp/a08-site-validation.log`.
These are temporary machine evidence; the result summary above is retained here.

## Separate Replit preview assessment

The baseline `.replit` Run workflows execute Python: the preview server,
contrast checker, and locale-link checker. Node is tooling, not the site's
production server. Node 20 remains an unsupported declared development module;
the repository's new npm engine check will reject it for QA installation.
`.nvmrc` does not automatically change a Replit module. Replit's
[configuration documentation](https://docs.replit.com/features/project-setup/configuration)
explains that modules and the Nix channel select available language packages;
this review did not verify a Node 24 module in the actual Replit workspace.

A08 therefore leaves `.replit` untouched. A18 independently owns preview
binding and publication-boundary repairs, and confirmed its changes are to the
Python start command and unsafe static deployment block. Before claiming Replit
QA parity, select an available Node 24 runtime there, record `node --version`
and `npm --version`, and run clean installation and the relevant browser gates.
If Node 24 cannot be provided there, run QA in the supported local/CI environment.
Actual Replit execution and exposure remain unverified by A08.

## Remaining integration acceptance

A21 instructed workflow integration in order A07, A08, A10, A17, with T01 also
coordinated. A21 accepted this baseline-based two-setting patch after integrating
reviewed A07. Preserve its retry/freshness changes when applying A08. Regenerate
any combined lock metadata through npm if another package changes package.json.
Run the combined candidate's fixture/browser suites on Node 24 after subsequent
coverage/runtime changes. A08's existing suite passes do not establish A10's
expanded coverage or unrelated visitor fixes.

No hosted Actions run, Linux execution, Replit runtime migration, live external
health check, branch publication, PR, main merge, or deployment occurred.
CI acceptance stays unverified until an authorized run of the combined candidate.
