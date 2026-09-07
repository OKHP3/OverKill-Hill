# A06 content truth handoff

September 7, 2026. Disposition: English corrections implemented and locally tested; combined generation and locale review remain integration requirements.

## Baseline and scope

Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`, initially detached and clean. Branch: `codex/a06-content-truth`. Worktree: `/Users/okh/.codex/worktrees/862f/OverKill-Hill`. No owner-checkout or sibling content writes, publication, main merge, dependency changes or deployment. Production SHA was not reverified; public text retrieval is not deployed-byte proof.

Eight authoritative fragments changed under `site-src/pages/`:

- `index.main.html`: replace blanket road-testing/readiness with intent and project-specific evidence/limits.
- `vault/index.main.html`: identify the one downloadable template and planned resources; remove unproved production-testing claim.
- `projects/bpmn-for-mermaid/index.main.html`: qualify first-try/no-repair assertions in feature, scope and FAQ copy.
- `projects/found-ry/index.main.html`: distinguish optional promotional credit from Apache redistribution conditions and separately created export rights.
- `projects/mac-studio-local-ai-workbench/index.main.html`: date the journal, retain the original May 12 table and task list, link May 30 results, distinguish deployment from corpus ingestion, label superseded plans as historical.
- `projects/hometools/index.main.html`, `projects/pathscrib-r/index.main.html`, `projects/un-nocked-truth/index.main.html`: visible concept notices, proposed capability wording, project return and inquiry links. Existing URLs and noindex remain.

This handoff is the ninth committed file. Metadata/status-registry work stays with A11/A12. The homepage fragment overlaps their broader work; preserve these specific qualifications when combining changes.

## Reproduction and public evidence

At baseline the Mac journal reported RAG and six-model strict benchmarking complete on May 29/30 while its later section still presented both as next steps. The three concept main bodies lacked visible notices. Found-Ry's FAQ said attribution was not required. Homepage, BPMN and Vault made unqualified testing/readiness/syntax claims identified by C06.

Public sources checked September 7, 2026:

- [Published Mac journal](https://overkillhill.com/projects/mac-studio-local-ai-workbench/): dated owner-reported build history, not an independent workstation or benchmark audit. Existing failures and historical conclusions preserved.
- [Found-Ry license](https://github.com/OKHP3/OverKill-Hill-FoundRy/blob/main/LICENSE): GitHub license API confirmed `Apache-2.0`; web-page/raw retrieval failed, so the API supplied verification.
- [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0): Section 4 supports the scoped redistribution summary. No repository license or export rights were changed.

No new benchmark, customer, availability or workstation-current-state claim was introduced. Unsupported claims were qualified instead of replaced with new success claims.

## Actual validation

Used existing `/private/tmp/okh-overkill-hill-qa-venv-20260906/bin/python` with Beautiful Soup 4.15.0. Default Python lacked Beautiful Soup; no installation performed.

After running `scripts/build-site.py` then `scripts/build-search-index.py`:

- PASS `scripts/build-site.py --check`: 36 generated English pages.
- PASS `scripts/build-search-index.py --check`: 160 entries. Generator reports Universe current.
- PASS `scripts/validate-site.py`: 56 HTML pages, 32 existing structural warnings, MTB/banner checks, no new voice warnings. Initial two new passive-voice warnings were fixed in source and rerun successfully.
- PASS `scripts/check-links.py`.
- PASS `scripts/check-locale-links.py`, `scripts/generate-csp.py --check`, `scripts/cache-bust.py --check`.
- PASS `git diff --check`.
- PASS focused Beautiful Soup assertions: all three notices and recovery links present, all three noindex tags retained; original benchmark table and historical task-list content exactly equal baseline; May 30 anchor resolves. Git diff confirms protected writing, art, sitemap and locale files untouched.
- PASS actual headless Chromium at 390 x 844: visible concept notice and inquiry link on all three routes, served from this worktree at loopback port 18606. Initial sandbox browser launch failed with Mach-port permission denial; approved rerun passed. Used existing Playwright read-only from the owner checkout; browser temporary data stayed outside that checkout.

No full browser matrix, assistive-technology session, external product runtime test, independent benchmark verification, translation quality certification, CI or live deployment check was performed.

## Locale and integration requirements

The page-sync skill's report exits 0 but reports nine stale route/locale pairs; that is detection, not a clean locale result. Changed homepage requires `okhp3-translation-en-us-fr-fr`, `okhp3-translation-en-us-de-de`, and `okhp3-translation-en-us-es-es`. German/Spanish About, Contact and Projects are also reported stale and were not changed here. `scripts/check-regional-drafts.py` exits 1 for the homepage source drift in its two regional draft records. Review UK English and Mexican Spanish counterparts with their exact-pair skills as part of the combined source update. No ledger adoption or translation edits performed.

A21 must incorporate these authoritative source changes, then run the owning site and search generators in its combined candidate; check Universe, CSP and cache fingerprints. Generated outputs were exercised locally and deliberately excluded from this source-only commit, then restored to baseline. Consequently the source-only checkout requires regeneration before freshness gates can pass. Do not hand-merge generated HTML or search JSON.

A11/A12 should align their registry/metadata to the dated journal and concept/evidence boundaries above. Any new completion or benchmark claim still requires supporting public evidence or owner judgment. No owner decision is needed to retain the bounded English corrections. Publication and complete locale acceptance remain pending A21 coordination.
