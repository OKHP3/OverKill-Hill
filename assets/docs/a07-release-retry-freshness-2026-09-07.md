# A07 release retry and committed freshness

Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`. Local implementation for D02/V2; A21 owns integration and release acceptance.

## Confirmed changes

- Validation checks committed HTML, search index, and universe output before the first regeneration step. Existing regeneration and subsequent checks remain as reproducibility checks.
- The validated release name includes commit, workflow run ID, and producer attempt. The reusable workflow exports that name. Pages consumes the successful producer's output and rejects an empty identity before downloading; a deploy-only rerun does not infer the producer attempt from its own attempt number.
- Pages upload `name` and deployment `artifact_name` use the same run/attempt expression. Live-edge evidence is also attempt-specific. Earlier artifacts are retained; no deletion or overwrite fallback was added.
- `scripts/build-release.py` is unchanged. Schema 3, complete inventory/digest checks, exact commit verification, publication exclusions, and the serialized deployment remain intact.

The pinned [upload action input](https://github.com/actions/upload-pages-artifact/blob/fc324d3547104276b827a68afc52ff2a11cc49c9/action.yml) and [deployment action input](https://github.com/actions/deploy-pages/blob/368f82528645a54fb793d4d04e342629a3f51346/action.yml) support the paired names (verified September 7, 2026).

## Local verification

| Check | Result | Evidence |
|---|---|---|
| `py -3 -X utf8 tests/test-release-package.py` | PASS | 11 tests, including clean package verification, schema/inventory/tamper rejection, retry wiring, and stale-output preflight |
| Deliberately stale HTML and search in temporary source copy | PASS | Each fails with its specific stale diagnostic; before/after hashes prove no source file was repaired by the gate |
| `py -3 -X utf8 scripts/build-site.py --check` | PASS | 36 generated pages current before regeneration |
| `py -3 -X utf8 scripts/build-search-index.py --check` | PASS | 160 entries current before regeneration |
| `py -3 -X utf8 scripts/sync-universe-map.py --check` | PASS | Universe map current |
| Workflow YAML parsing; `git diff --check` | PASS | Both files parse; no whitespace errors |

Local runtime: Windows, Python 3.14. The retry assertions verify workflow wiring, not GitHub scheduler execution. No browser rerun was needed for this workflow-only change; no site source, generated content, art, locale, or runtime file changed.

## Outstanding acceptance

An authorized CI release must still exercise both a full rerun and a deploy-only rerun. Capture run ID/attempt, producer output, downloaded artifact identity, Pages artifact identity, schema 3 verification, and live SHA. Expected: full rerun produces a new validation artifact; deploy-only rerun reuses the earlier successful validation artifact and creates a new Pages artifact. These are expected outcomes, not observed hosted evidence. Workers must not merge, deploy, or manufacture that evidence.

A08 owns Node selectors, A10 owns QA inventory/reporting, and A17 owns concurrency. Their edits must preserve the artifact output and pre-generation gate. A01 is satisfied by the baseline; hosted rerun evidence remains open for A21.
