# A07: Release retry and committed freshness

September 7, 2026. Status: local implementation tested; CI retry acceptance pending.

## Baseline and scope

Worktree: `/Users/okh/.codex/worktrees/a694/OverKill-Hill`.
Branch: `codex/a07-release-retry-freshness`.
Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`, initially clean and detached.
This includes reviewed A01 schema 3 integrity repair and A02 documentation.
The package commit is the commit containing this handoff; resolve with
`git log -1 --format=%H -- assets/docs/remediation-a07-2026-09-07.md`.
Production SHA was not queried or assumed. No publication, remote writes,
deployment, owner-checkout edits, or sibling edits occurred.

## Reproduction and correction

D02: Pages upload/deploy omitted artifact names and selected the default.
New names match: `github-pages-<run-id>-<run-attempt>`. Validated source
artifacts also include SHA, run ID, and attempt. The successful validation
job exposes its name through the reusable workflow output; the download
consumes that output instead of reconstructing it from the deployment
attempt. This is intended to retain successful validation on deploy-only
retries. The release edge evidence artifact also includes attempt.
One-day artifact retention remains: expired input requires full validation.
Fork contrast and scheduled monitor names are unchanged; the fork-report
workflow consumes the old contrast name and must be updated with its producer
if A17 later changes it.

V2: baseline CI ran HTML/search generators before freshness checks. The new
preflight checks HTML, search, and universe before regeneration. Existing
regeneration and later freshness checks remain to check the resulting tree.
Tests exercise the actual preflight block against a clean isolated copy and
against deliberately stale HTML and JSON, requiring rejection without repair.

Changed paths:

- `.github/workflows/validate.yml`: early freshness and validated artifact output/name.
- `.github/workflows/pages.yml`: output-based download and attempt-specific upload/deploy/evidence.
- `tests/test-release-package.py`: naming, ordering, and executable stale-output regression tests.
- `docs/publishing.md`: updated artifact names and retry/retention contract.
- This handoff.

No authoring sources or generated outputs changed. No regeneration is needed
for A07 alone. A21 must regenerate combined content through its owning scripts,
then pass the new freshness gate; generated files must not be hand-merged.

## Local evidence

Environment: macOS, Python 3.14.5, Beautiful Soup 4.15.0. System Python lacks
Beautiful Soup; the existing assessment virtual environment was used read-only
with `PYTHONDONTWRITEBYTECODE=1`, without installation or dependency changes.
Interpreter: `/Volumes/OKH-Local/04_GitHub_Mirrors/OverKill-Hill/.local/audit-validation-2026-09-07/venv/bin/python3`.
Commands below use that interpreter where Beautiful Soup is required.

| Check | Result |
| --- | --- |
| Two new workflow contract tests against original workflow | FAIL as expected: missing attempt name; freshness follows generation |
| `python3 tests/test-release-package.py` after repair | PASS, 12 tests, no skips; includes actual stale HTML/search rejection and untouched bytes |
| `python3 -m unittest tests/test_verify_live_edge.py` | PASS, 9 tests |
| `python3 scripts/build-site.py --check` | PASS, 36 generated pages |
| `python3 scripts/build-search-index.py --check` | PASS, 160 entries |
| `python3 scripts/sync-universe-map.py --check` | PASS |
| Temporary full `build-release.py --output <temp>/release --commit 98922aebf71d90b2b18ecc34c8b00a041fff51c7`, then same with `--verify` | PASS, 56 HTML pages, 371 files, schema 3, 370 integrity entries |
| `git diff --check` | PASS |
| Actionlint, full browser suite, Linux/Python 3.11 CI | NOT RUN; actionlint unavailable; no browser/runtime source change |
| Controlled CI rerun or deployment | NOT RUN; outside delegated publication authority |

Confirmed the pinned official action inputs on September 7:
[upload name](https://github.com/actions/upload-pages-artifact/blob/fc324d3547104276b827a68afc52ff2a11cc49c9/action.yml)
and [deploy artifact_name](https://github.com/actions/deploy-pages/blob/368f82528645a54fb793d4d04e342629a3f51346/action.yml).
Local text-contract tests do not emulate GitHub Actions scheduling or output
retention across attempts.

## A21 acceptance remaining

Serialize these workflow hunks with A08/A10/A17/T01. Re-run the package tests
on the combined candidate. At an authorized release, retain evidence for an
initial run, full rerun, and deploy-only rerun: successful validation output,
matching download, unique Pages artifact name, matching deploy input, and
verified SHA/file bytes. No deletion of earlier artifacts is needed. Confirm
previous successful validation outputs remain available to the deploy-only
rerun. Do not close A07 acceptance until this CI evidence exists. A17 owns
concurrency behavior independently; this package preserves the current queue.
