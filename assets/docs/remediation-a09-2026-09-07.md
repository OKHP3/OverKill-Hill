# A09: macOS review fixture portability

Status: implemented and locally verified; ready for A21 integration review.
Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7` (includes A01/A02).
Branch: `codex/a09-review-fixture-portability`. The package commit contains this handoff and the test change.

## Reproduction and repair

The original `tests/test-murderbird-review-boundary.py` failed on this Mac's default `/var/folders/...` temporary root. Its manifest link resolved to a nonexistent path containing an extra `private/var` segment. The historical builder derives its normal root from `__file__.resolve()`, but the fixture replaced its roots with unresolved temporary paths.

Read the preservation contract in `assets/docs/murderbird-source-archive-2026-09-06.md` and the historical builder's header before execution. The fixture now resolves its root before patching builder constants. No archived builder, artwork, manifest, or preservation receipt bytes changed.

Changed paths:

- `tests/test-murderbird-review-boundary.py`: shared behavioral assertion, default and canonical root cases, explicit unequal-depth directory symlink case; checks every src/href/srcset target exists inside the fixture, the manifest link reaches the intended manifest, and image sources reach preserved fixture images.
- `assets/docs/remediation-a09-2026-09-07.md`: this handoff.

Every case still tests full generation plus two markup-only rebuilds, unchanged image/manifest bytes, noindex, exactly two local review pages, rejection of accidental HTML in the archive, and exclusion from search. Symlink creation failure is an explicit unittest skip, never reported as executed coverage.

## Actual validation

Used the existing assessment environment read-only at `/Volumes/OKH-Local/04_GitHub_Mirrors/OverKill-Hill/.local/audit-validation-2026-09-07/venv/bin/python` with `PYTHONDONTWRITEBYTECODE=1`; no dependency installation or owner-checkout writes. The initial system `python3` attempt lacked Beautiful Soup and did not execute tests.

- Before repair: original fixture failed at the reported link assertion on default macOS temporary storage.
- After repair: `tests/test-murderbird-review-boundary.py`, 3 passed, zero skips. Includes default macOS temporary root, canonical root and explicit directory alias to a deeper target.
- Mutation check: executing an in-memory copy with root normalization removed made the explicit alias case fail on a nonexistent manifest destination. No mutation was written to disk.
- `tests/test-release-package.py`: 9 passed, including all 108 preservation-receipt entries, source/archive release exclusions, accepted-media hashes and schema-3 integrity regressions.
- `git diff --check`: passed.

No source generation, search regeneration, CSP update or cache fingerprint refresh is required: this package changes only a test and documentation. Do not regenerate the preserved v2 archive during integration.

## Remaining boundary

No package-specific owner decision remains. A21 should review and incorporate this local commit and rerun the two test files on the combined candidate. Linux/Windows and GitHub Actions were not executed here; no CI, production SHA, live-site, browser, publication or deployment claim is made. Runtime/workflow serialization is unaffected.
