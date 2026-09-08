# A09 review fixture portability

Status: COMPLETE as of September 8, 2026. Implementation is integrated on main;
Windows and native macOS regression checks pass. The original September 7
evidence below is retained as a dated record and superseded by this closeout.

## September 8 closeout

- Original implementation `c9fa89490c4e7477f5ef1b09a10dec3f942884af` was
  integrated through PR62, merge `eeb3960778ddb56d99a80c3ae36c2e2db46c082b`.
  PR61 is closed and superseded. The fixture and archived builder were compared
  to current main `f4a353c3` and match exactly.
- Native macOS acceptance passed in
  [run 34231307833](https://github.com/OKHP3/OverKill-Hill/actions/runs/34231307833)
  at `7325953737000bf69bf4c2b724826cbed29546f9`, using the hosted
  `macos-26-arm64` image and CPython 3.11.9 with existing pinned QA dependencies.
- All 3 review-boundary tests pass: the host default temporary root, an explicit
  canonical root, and a real POSIX symlink alias root. No temporary-root
  environment override was applied.
- All 9 release-package tests pass, including the complete archive preservation
  receipt and release exclusions. No builder, artwork, manifest, or receipt
  bytes changed.
- `.github/workflows/a09-macos-review-fixture.yml` is retained on the task
  branch as the executable acceptance runner. This closeout does not claim
  that the additional workflow is installed on main or is a required check.
- No A09 implementation or platform acceptance blockers remain. This closes
  A09 only; unrelated advancement-program acceptance and device checks remain
  with their assigned owners.

## Original September 7 evidence

Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`.
Scope: `tests/test-murderbird-review-boundary.py` and this evidence record.

PR56 was inspected before editing. It merged as
`4aa8f26f6347a596e167c61169bdcb0ee8e121eb` and is already in the baseline.
It changes only `scripts/audit-site.py` and
`scripts/check-performance-budget.py`, so it does not resolve V1.

The historical builder resolves its own `__file__` when defining roots. The
fixture replaced those roots with lexical temporary paths. Normalize that
fixture input to match the real entry point, without modifying the archived
builder or its preservation receipt.

The expanded fixture exercises default, canonical, and explicitly aliased
temporary roots. POSIX uses a directory symlink; Windows uses a directory
junction without requiring symbolic-link privileges. The alias test verifies
that its lexical root differs from its resolved root before invoking the
shared fixture. Alias creation errors fail the test rather than silently skip.

Every case retains full generation, two markup-only refreshes, unchanged
manifest/image bytes, noindex markup, local HTML placement, refusal to write
review HTML into assets, and search exclusion. Links must exist within the
fixture assets/review directories and use the relative path derived from
canonical endpoints. This rejects host-specific alias detours even when a
filesystem happens to resolve them successfully.

## Evidence

- PASS: the original single test on Windows at the baseline.
- Confirmed reproduction: the new alias regression failed before normalization,
  producing `../../../../private/var/review-.../assets/murderbird/v2/manifest.json`
  instead of `../../assets/murderbird/v2/manifest.json`.
- PASS: `py -3 tests/test-murderbird-review-boundary.py`, 3 tests after the fix.
- PASS: `py -3 tests/test-release-package.py`, 9 tests, including the complete
  archived-source preservation receipt and packaged archive exclusions.
- PASS: `git diff --check`; no changes to archived builder, images, manifest,
  receipt, public pages, or generated site outputs.
- Environment: Windows, Python 3.14.0rc1. No dependencies added or changed.
- NOT RUN: native macOS default temporary-root execution and POSIX symlink
  branch on this Windows host. The junction run demonstrates the path alias
  regression, but does not establish native macOS acceptance.
- NOT RUN: publication or deployment. A21 owns integration and release.

Next action: A21 should obtain native macOS execution of
`python3 tests/test-murderbird-review-boundary.py` under the normal temporary
environment before claiming all A09 platform acceptance criteria complete.
