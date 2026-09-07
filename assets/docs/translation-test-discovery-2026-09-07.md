# T03 translation test discovery validation

Date: September 7, 2026. Status: CLEAR for mechanical discovery and regression checks.
Starting commit after fetching origin/main: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`.
Branch: `codex/t03-translation-test-discovery`.

## Outcome and boundary

The September 5 T03 finding remained reproducible at the September 7 dispatch
baseline. Default unittest discovery returned zero tests and exit 5 for every
exact-pair package on Python 3.14.5. Explicit execution passed ten per package.
Renaming only the test files fixes discovery; the tests remain byte-identical.
Python's importable-module requirement makes these five underscore filenames a
documented tool-required exception to the repository's kebab-case default.
Package-local SKILL.md instructions now give discovery and explicit commands.
No active caller of the old test paths was found. Historical French benchmark
records retain their original paths and claims; the rename mapping is
`tests/test-en-us-to-<pair>.py` to `tests/test_en_us_to_<pair>.py`.

This is a test integration change for Python unittest clients. Helper behavior,
package version metadata, translation instructions, locales, review records,
site content, and generated output are unchanged. No fresh live linguistic
benchmark or unseen release holdout was run. No translation-quality or
publication-readiness claim follows from these mechanical results.

## Validation

| Package | Before discovery | After discovery | Explicit execution | Unchanged test SHA-256 |
| --- | ---: | ---: | ---: | --- |
| `okhp3-translation-en-us-de-de` | 0 | 10 | 10 | `4bba5c2fbbcfaca3b84bc82c1c2ea01298f79382dc8e0d377d798b121d1afdd2` |
| `okhp3-translation-en-us-en-uk` | 0 | 10 | 10 | `9cb19edbf449278936cb004dfe296be9fd3f36c52db98f42ddb2d39f935010fc` |
| `okhp3-translation-en-us-es-es` | 0 | 10 | 10 | `6ec9708e25adf592f33c2c4cf1ed083b1ac7f874d00e2797c1d39b62d13604cd` |
| `okhp3-translation-en-us-es-mx` | 0 | 10 | 10 | `620aa6d00c43f6df3e6ac5990ce72de989c55dd722e49d84971d6fdb4be048fa` |
| `okhp3-translation-en-us-fr-fr` | 0 | 10 | 10 | `b3d18397fc1c0dd95ba3f6215f5c1aa2f11632489321d5c9124da1e6af35fbcf` |

- `python3 scripts/test-translation-skills.py`: 59 passed, comprising the five
  ten-test suites and nine detector tests. Uses standard library only.
- `python3 tests/test-translation-skill-discovery.py`: eight guard regressions
  passed: complete inventory; missing translation file; missing detector
  directory; empty suite; reduced suite; unrelated tests masking an empty
  required suite; import error; failing test propagation.
- Per-package `python3 -m unittest discover -s <package>/tests -v` and explicit
  `python3 <package>/tests/test_en_us_to_<pair>.py -v`: ten passed each.
  Byte equality against the starting commit establishes preservation beyond
  count equality. Repeated execution is not additional distinct coverage.
- Detector default discovery: nine passed. Coverage includes no-config no-op,
  missing translation, bootstrap adoption, source drift, stale re-adoption,
  route scoping, fragment/localized URL exclusions, nonfatal orphan reporting,
  and missing-index errors. Target-only integrity remains outside T03.
- Foundry package validator: five packages passed independently.
- `git diff --check`: passed.

There are 67 distinct regression tests in the new workflow: 59 package tests
plus eight guard tests. Local runtime is Python 3.14.5. The workflow uses Python
3.11 and the checkout/setup-python commit pins already established in the
repository. It runs on relevant PR/main path changes or manual dispatch, with
read-only repository permissions and a five-minute timeout. It is separate
from validate.yml and does not establish a Pages deployment dependency.
Hosted execution remains pending coordinated publication. actionlint was not
installed, so no actionlint pass is claimed.

## Read-only source-family reconciliation

Compared the five local packages with the accessible Skillz mirror's
`language-mediation/okhp3-translation-en-us-*` files. Mirror HEAD was
`1a8686ce386928cccef04b53ac6bb98e0ab40b61`; comparisons used working files,
so that revision is context, not a claim of a clean or canonical snapshot.
All five test-method inventories share eight cases. Each local package has
two additional tests for relative links/email/media targets and rejection of
identical source/target roots. Each mirror package instead has
`test_approved_output_requires_a_complete_review_record`.

The inspected French helper diff explains the competing strengths: the local
validator protects additional link/email forms and the planner rejects equal
roots; the mirror validates approved review-record fields more fully and uses
underscore helper imports. Every pair has differing planner and validator
bytes. Neither whole family is selected as a replacement. Keep the local
hyphenated helper names and existing ten cases. Reconcile the review-record
behavior and its test separately with the relevant policy/integrity owner;
copying a test alone would assert behavior this change does not implement.
No sibling checkout or source-family file was written.

## Integration handoff

Changed files: five byte-identical test renames, five package SKILL.md test
instructions, `.github/workflows/translation-skill-tests.yml`,
`scripts/test-translation-skills.py`, `tests/test-translation-skill-discovery.py`,
`scripts/README.md` (one inventory row), and this report.
The scripts README row may overlap T04's inventory edits; preserve both.
No generated-output reconciliation is required by T03 itself. A21 owns
publication/integration scheduling. No independent merge or deployment.
