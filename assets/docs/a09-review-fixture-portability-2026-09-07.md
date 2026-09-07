# A09 review fixture portability

Status: implementation and Windows regression checks pass; native macOS acceptance remains unverified.

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
