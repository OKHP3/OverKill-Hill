# Translation workflow assessment and cleanup plan

Assessment date: September 5, 2026. Status: **CLEAR for findings; proposed implementation, no cleanup applied.** This is an addendum to the comprehensive website assessment, prompted by the owner's clarification that translation is moving toward exact-pair Agent Skills and Python-assisted GitHub automation.

## Decision

Keep the static, skill-based translation approach. The current `i18n/` directory is active infrastructure for that approach, not evidence of an obsolete translation framework. The strongest cleanup opportunities are misleading instructions, incomplete release enforcement, undiscoverable package tests, and accumulated regional-generation special cases. No entire translation directory has been established as disposable.

The implementation should first make the current system explicit and reliable, then consolidate its policy records. Cosmetic renaming of `i18n/` would create work without fixing the identified defects.

## Evidence boundary

The owner checkout is `897df5d33202bd65924f9f3a35c84e0068cbee02`. The audit's isolated current-remote snapshot is `40e18ee7916f4a54196cc407d60999ba1d786d11`. Relevant differences are CSP-related reviewed HTML and French provenance/hash updates; the scripts and workflow relationships discussed here are unchanged. Do implementation on a fresh branch from the current remote revision, preserving the local audit artifacts.

This follow-up inspected callers, workflows, generation inputs, manifests, review records, skill instructions, tests, and relevant Git history. It did not perform a new linguistic review, change review approval, publish locales, or execute a cleanup. Prior AskJamie work informed the investigation method only; its locale inventory was not applied to this site.

The local Skillz mirror is accessible, but has unrelated working changes and differing French helper names/test coverage. Do not overwrite these site packages by copying that mirror wholesale. The comparison establishes divergence, not that either whole directory is the correct replacement.

## What actually runs

| Stage | Current authority and behavior |
| --- | --- |
| English authoring | `site-src/pages.json`, its content fragments, and `assets/partials/`; `scripts/build-site.py` renders English HTML. |
| Source-drift detection | `i18n/sync.config.json` selects four English routes and `fr`, `de`, `es`. The portable `.agents/skills/okhp3-i18n-page-sync/scripts/i18n-page-sync.py` compares source hashes with `i18n/sync-state.json`. |
| Site freshness policy | `scripts/check-i18n-release.py` treats French missing/stale/unbaselined routes as blocking and German/Spain Spanish drift as advisory. |
| Translation | Five exact-pair skill packages provide instructions and deterministic helpers. Reading a skill or running the detector does not invoke an automatic translation model. |
| Reviewed baseline adoption | The site wrapper requires explicit locale, routes, provenance, and matching source/target hashes. Adoption is a separate write operation. |
| Structural checks | `scripts/check-locale-links.py` consumes `i18n/pilot/manifest.json`; regional drafts use `scripts/check-regional-drafts.py` and their separate manifest. |
| Regional generation | `scripts/build-locale-drafts.py` generates en-GB from canonical English plus its dictionary, and es-MX from retained reviewed HTML plus the current English shell inputs. |
| Automation | `.github/workflows/i18n-page-sync.yml` runs the site freshness wrapper. It checks; it does not draft translations. |
| Deployment | `pages.yml` depends on reusable `validate.yml`. The latter runs wrapper regression tests and locale structural checks, but does not invoke the live site freshness command. |

Current coverage is four routes per locale: `/`, `/about/`, `/projects/`, `/contact/`. French has four released/indexable routes. German, Spain Spanish, en-GB, and es-MX each have four retained noindex draft routes. Noindex is an indexing boundary; these are publicly served pages, not access-controlled drafts.

## Confirmed findings and recommendations

### T01. Put the translation freshness check inside the deployment dependency

**Priority: high.** The standalone i18n workflow can fail independently of the Pages workflow. Pages waits for `validate.yml`, whose `test-i18n-release.py` invocation tests fixtures rather than validating the checkout's current translation state. Neither the release builder nor the structural locale checker bridges that dependency.

Add `python3 scripts/check-i18n-release.py --mode check --format json` to the reusable validation workflow. The separate i18n workflow can remain a fast diagnostic initially. Decide later whether its duplication has value. Required PR checks, if configured, do not replace this explicit deployment dependency for every dispatch/push path.

Acceptance: a fixture with stale French fails the release validation path; draft drift retains the declared advisory policy; current reviewed French passes. This is a workflow-graph finding, not a claim that stale translations were observed deploying.

### T02. Distinguish source freshness from reviewed-target integrity

**Priority: high.** The portable detector records `target_sha256` during adoption, but `scan()` compares only `synced_source_sha256` to current English. A disposable fixture changed French `/about/` while keeping English and the ledger unchanged. All 12 configured pairs remained `in_sync`.

Evidence: [target-only drift probe](../audit/translation-target-drift-2026-09-05.json). The probe changed copied files only.

Keep source-drift detection's meaning clear. Add reviewed-target integrity enforcement to the site release policy, or introduce a separately versioned detector status with compatible callers. A target-only edit must require a fresh review record before release. Adoption must also support a reviewed target-only update: the current portable adoption loop visits only missing-baseline/source-stale entries, so merely tightening the check is insufficient.

Acceptance: test unreviewed target changes, approved target-only updates, wrong source/target hashes, wrong locale, and unchanged pages. Handle generated CSP/fingerprint changes deliberately; do not silently normalize away meaningful translated content.

### T03. Make the five skill test suites discoverable and continuously exercised

**Priority: medium.** Every exact-pair package currently names its suite `tests/test-en-us-to-<pair>.py`. Standard `unittest discover` found zero tests in all five packages. Explicit execution passed ten tests per package. On the Python 3.14 runtime used here, the empty discovery runs returned exit code 5; the defect is skipped coverage, not a claimed successful discovery run.

Rename the five tests to Python-discoverable `test_en_us_to_<pair>.py`, update their callers, and register a CI command that fails if the expected suites are absent. Treat these filenames as a documented tool-required naming exception. Keep the existing hyphenated planner/validator filenames; they are active referenced helpers. Reconcile missing tests with canonical Skillz deliberately instead of choosing a whole package by timestamp.

### T04. Replace outdated instructions with the actual operating contract

**Priority: medium.** `i18n/pilot/README.md` omits both regional locales and the provenance-enforcing site wrapper. It incorrectly says the shared runtime uses only the English search index; `assets/js/app.js` selects the French index. `scripts/README.md` omits the active release wrapper, regional builder, and regional checker. The portable skill prose advertises `--adopt`/`--check` flags even though its actual parser requires `--mode adopt`/`--mode check`.

Update these in place. Document read-only checks separately from draft creation and baseline writes. The site's adoption recipe must use its wrapper and exact reviewed routes. Do not redefine generic detector semantics as if they were the site's stronger published-locale policy. Update reusable skill instructions through the appropriate source-family reconciliation as well.

### T05. Consolidate locale policy after mapping existing behavior

**Priority: medium; separate implementation change.** Coverage, statuses, source hashes, and release rules are spread among `sync.config.json`, `pilot/manifest.json`, `regional-drafts-manifest.json`, the regional source-hash record, and constants in two scripts. The main manifest says `human-reviewed-required`; individual evidence records explicitly claim AI review without human/native approval, while French is already indexable. These fields describe different concepts without a clear common vocabulary.

Define separate fields for draft/released status, source freshness, review method, review approval, and indexability. Preserve historical claims as history. The owner must decide the future publication-review requirement; the software should not infer native or human approval. Generate or validate consistent coverage from one versioned site policy, preserving the intentionally different draft-alternate behavior until an explicit decision changes it.

### T06. Simplify regional generation with protected-content regressions

**Priority: medium.** `build-locale-drafts.py` contains a literal no-op replacement of `class="lang-flag"` with itself, global replacements after its text-node-safe adapter, repeated shell patches, and source hashes tied to a historical release filename. Its docstring says existing target files are preserved during regeneration, but its write path regenerates outputs from English or reviewed inputs. An edit made only to a generated regional output can be overwritten.

Remove the no-op. Correct the generator's source/output instructions. Replace whole-document vocabulary substitutions with transformations that preserve URLs, code, attributes, and protected tokens. Move current shell composition into a clear adapter without re-translating reviewed prose. This is targeted logic work, not permission to regenerate or relabel translations without review.

## Exact cleanup disposition

All actions below are proposed. In-place edits are reversible in Git. No file deletion is proposed in this first batch.

| Existing path or family | Proposed destination/action | Reason and risk |
| --- | --- | --- |
| `i18n/` and its current config/state | Keep paths; improve documented ownership | Active callers. Removal would break checks. |
| `i18n/pilot/README.md` | Same path; rewrite operating guide per T04 | Low-risk documentation correction; preserve publication distinctions. |
| `scripts/README.md` | Same path; add three active translation scripts and read/write classifications | Low risk; fixes incomplete inventory. |
| `.agents/skills/okhp3-i18n-page-sync/SKILL.md` and script help prose | Same paths; correct CLI examples and generic/site-policy distinction | Low runtime risk; reconcile distributed copies before claiming synchronization. |
| `.github/workflows/validate.yml` | Same path; include actual site freshness check | Medium release-behavior change; T01 regression required. |
| `.github/workflows/i18n-page-sync.yml` | Keep initially; correct its generic introductory comments | Avoid removing the existing diagnostic before the dependent gate is verified. |
| `.agents/skills/okhp3-translation-en-us-de-de/tests/test-en-us-to-de-de.py` | `tests/test_en_us_to_de_de.py` in the same package | Discoverability fix; update references and preserve all tests. |
| `.agents/skills/okhp3-translation-en-us-en-uk/tests/test-en-us-to-en-uk.py` | `tests/test_en_us_to_en_uk.py` in the same package | Same. Do not rename the established skill identifier. |
| `.agents/skills/okhp3-translation-en-us-es-es/tests/test-en-us-to-es-es.py` | `tests/test_en_us_to_es_es.py` in the same package | Same. |
| `.agents/skills/okhp3-translation-en-us-es-mx/tests/test-en-us-to-es-mx.py` | `tests/test_en_us_to_es_mx.py` in the same package | Same. |
| `.agents/skills/okhp3-translation-en-us-fr-fr/tests/test-en-us-to-fr-fr.py` | `tests/test_en_us_to_fr_fr.py` in the same package | Same. |
| `i18n/pilot/es-mx/reviewed/*.html` | Keep | Active generator inputs and test references, not redundant output copies. |
| `i18n/pilot/source-hashes-release-0ee.json` | Keep until a tested source-record migration | Directly consumed by builder and checker. |
| `i18n/pilot/source-hashes-a39.json` | Keep; index as historical source evidence | No direct filename caller found, but its source revision matches translation records. Lack of a caller is insufficient to delete provenance. |
| Dated `*review*.json` and `translation-record.json` files | Keep; add an index describing source revision and supersession | Evidence records need not have runtime callers. Do not rewrite an old review to imply a new approval. |
| Skill `benchmarks/historical-webpage-v0.3.0/` | Keep | Already explicitly historical; no demonstrated cleanup benefit. |
| `unpublished-scaffold` and legacy manifest parsing branches | Retain pending fixture/caller review | Compatibility behavior, not proven dead code. |
| Draft HTML trees and empty draft search indexes | Keep | Intentional release-boundary artifacts exercised by checks. |
| `scripts/build-locale-drafts.py` | Same path; focused T06 refactor | Medium risk of content/protected-token changes; separate from mechanical cleanup. |

## Execution order and handoff

1. **Codex or Copilot: documentation and test-discovery cleanup.** Apply T03/T04 mappings in an isolated branch, preserve current helper interfaces and all regression coverage. No translated page changes. Verify exactly five discovered skill suites and the detector suite.
2. **Codex: release integrity.** Implement T01/T02 with failing negative fixtures first. Test the reusable workflow's actual release gate and reviewed target-only adoption. Preserve French versus draft severity.
3. **Codex or a bounded worker: regional generator.** Implement T06 with protected URLs/code/attribute fixtures and rendered-output comparisons for both regional pairs. Changes in translated prose require the corresponding exact-pair review.
4. **Owner policy decision, then implementation:** choose the approval requirement and consolidate T05. Replit is useful for a later rendered locale-switcher review; it adds little value to the initial file and workflow cleanup.

Each implementation package should return the exact changed files, tests executed and their counts, source revision, remaining review limits, and a reviewable diff. Do not push, deploy, change locale publication state, or synchronize sibling runtime files as part of this cleanup scope.

## Validation performed

| Check | Result |
| --- | --- |
| Site wrapper `--mode check` | Pass; French blocking policy, no current blocking drift. |
| `check-locale-links.py` | Pass for fr/de/es. |
| `check-regional-drafts.py` | Pass for four routes each in en-GB/es-MX. |
| Site-wrapper regressions | 7 passed; temporary fixture adoption only. |
| Five exact-pair suites, executed explicitly | 50 passed. |
| Portable detector suite | 9 passed. |
| Default test discovery in five exact-pair packages | Zero tests discovered in every package. |
| Target-only edit in disposable French fixture | Confirmed detector still reports `in_sync`; evidence linked above. |

There were 66 distinct passing regression tests. These establish mechanical behavior, not idiomatic translation, fidelity to the owner's voice, or publication approval. Original tracked source files and translation ledgers remain unchanged.
