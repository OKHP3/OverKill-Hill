# A06 content truth correction

Reviewed September 7, 2026. Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`.

## Question and decision

Which C02/C04/C05/C06 statements overstate the public evidence, and how can the English source correct them while retaining the author's journal, voice, URLs and original writing?

The September 5 content-estate audit and September 7 visitor/content audit were checked against current `site-src` fragments. All four findings remained reproducible. The correction changes source copy and selected description fields only. A21 owns combined generated output, release checks and publication.

## Public source ledger

All sources retrieved September 7, 2026. GitHub repository files were also read through the GitHub API; revisions below were resolved before the source reads. These are first-party project records, not independent runtime tests.

| Source / publisher | Exact source | Supported claim |
| --- | --- | --- |
| Benchmark Results / OKHP3 | [May 30 record at 863d48a8](https://github.com/OKHP3/mac-studio-local-ai-workbench/blob/863d48a80958d91452e5ccac0bb0d181f7192688/docs/05-benchmark-results.md) | May 12 loose/default prompting covered two Ollama models; May 30 strict output-only prompting covered six models and five tests. Zero outright failures still included functional outputs with formatting defects. |
| Runtime Readiness Audit / OKHP3 | [August 2 record at 863d48a8](https://github.com/OKHP3/mac-studio-local-ai-workbench/blob/863d48a80958d91452e5ccac0bb0d181f7192688/reports/openclaw-related-runtime-readiness-audit-2026-08-02.md) | Local service availability was observed; Qdrant integration and document ingestion, retrieval and citation were unverified. |
| RAG Roadmap / OKHP3 | [Plan at 863d48a8](https://github.com/OKHP3/mac-studio-local-ai-workbench/blob/863d48a80958d91452e5ccac0bb0d181f7192688/docs/07-rag-roadmap.md) | The retained roadmap describes planned retrieval work. It does not settle current workstation readiness. |
| FoundRy LICENSE / OKHP3 | [License at 452cea7b](https://github.com/OKHP3/OverKill-Hill-FoundRy/blob/452cea7bf81d54c3e9c2ae450bd8603d470d6818/LICENSE) | Repository license is Apache 2.0. Root tree inspection found no root NOTICE file at this revision; the FAQ retains the conditional NOTICE requirement. |
| Apache License 2.0 / Apache Software Foundation | [License, section 4](https://www.apache.org/licenses/LICENSE-2.0) | Redistribution conditions cover providing the license, identifying modified files, relevant source notices and applicable supplied NOTICE attributions. |
| OverKill Hill source / OKHP3 | [Public site source at baseline](https://github.com/OKHP3/OverKill-Hill/tree/98922aebf71d90b2b18ecc34c8b00a041fff51c7/site-src) | Three concept routes have noindex records but present-tense capabilities. The identified success claims lack a named measured success rate in the page copy and conflict with explicit prototype/renderer limits. |

## Claim disposition

| Claim | Tier | Evidence / correction | Consequence if false | Next check |
| --- | --- | --- | --- | --- |
| May benchmark and pending sections contradict each other as current statements | Confirmed | Preserve original May 12 table; label journal and earlier plan historically; link May 30 record with prompt/sample limitations | Reader confuses a dated sample with current reliability | A21 review generated page; separate machine audit for current operation |
| Deployed RAG components prove integrated retrieval | Unknown | August readiness explicitly leaves it unverified; visible summary and status now distinguish components from workflow | Reader relies on unproved retrieval | Disposable ingestion/retrieval/citation test on the workstation, outside A06 |
| Hometools, PathScrib-R and Un-NOCKed Truth are usable public launches | Unknown | Static visible concept notices, planned verbs and shelf/contact links; noindex preserved | Direct-link visitor expects unavailable tools | Owner supplies public launch evidence before changing status |
| Optional credit removes redistribution duties | Confirmed correction | FAQ links actual license, distinguishes promotional credit and section 4 conditions; exported/third-party content rights remain separate | Incorrect reuse assumptions | Review the actual material and its notices for a specific use |
| BPMN/MTB first-try success, Prompt Forge repeatability/self-report, BFS broad model influence and universal homepage/Vault readiness are proven | Unknown as broad outcomes | Replace guarantees with design intent, test expectations or a clearly labeled hypothesis; retain project voice and scoped prototype story | Reader assumes reliability or influence beyond evidence | Versioned samples and independent behavior evidence before stronger claims |

## Scope and integration contract

Changed source: `site-src/pages.json`; `site-src/pages/index.main.html`; the project `index.main.html` fragments for `bfs-framing-intelligent-futures`, `bpmn-for-mermaid`, `found-ry`, `hometools`, `mac-studio-local-ai-workbench`, `mermaid-theme-builder`, `pathscrib-r`, and `un-nocked-truth`; `site-src/pages/prompt-forge/index.main.html`; `site-src/pages/vault/index.main.html`.

Description metadata changes are confined to the six records for BPMN, the three concepts, Mac workbench and Vault. No status registry, shared runtime, stylesheet, art, manifesto, fiction, URL or locale approval record changes. A12 owns the follow-up Mac `index.extras.html` JSON-LD description alignment. A11 owns shelf/status consistency using these evidence limits. A06 does not declare their dependent work complete.

## Validation and remaining limits

Generation was exercised locally with `build-site.py`, `build-search-index.py` (including universe generation) and `generate-csp.py`. Final checks: `build-site.py --check` PASS (36 pages); `build-search-index.py --check` PASS (160 entries); `check-csp.py` PASS (56 pages); `validate-site.py` PASS (32 structural warnings and no new voice warnings); `check-locale-links.py` PASS. `i18n-page-sync.py --mode check` exits 1: nine stale pairs, of which eight de/es pairs already differed from the baseline ledger and the French homepage becomes stale with this change. `check-regional-drafts.py` exits 1 for the changed homepage in both regional pairs. Baseline source hashes were compared directly with the sync ledger to distinguish pre-existing drift. Full local command output was retained in the task artifact directory outside the repository. Generated files are excluded from the source-only commit and must be rebuilt by A21.

Static HTML checks confirmed all three concept notices and return/contact links are present without script execution, noindex remains, and concepts remain excluded from search. Protected manifesto, MurderBird and First Diagram authoring fragments were compared with the baseline and remain unchanged. No new dependencies or runtime behavior were introduced. No full browser or assistive-technology acceptance is claimed.

Locale handoff: changed homepage text needs `okhp3-translation-en-us-fr-fr`, `okhp3-translation-en-us-de-de`, `okhp3-translation-en-us-es-es`, plus the regional `okhp3-translation-en-us-en-uk` and `okhp3-translation-en-us-es-mx` reviews. Run adoption only after actual pair review, retaining regional draft/noindex boundaries. The page-sync report also lists pre-existing de/es drift on About, Contact and Projects; those English fragments are unchanged by A06. Other changed routes are outside the configured four-route translation pilot. No translation has been reviewed or adopted by this task.

Next action: A11/A12 review this factual contract, then A21 integrates source corrections, resolves locale requirements, regenerates outputs and performs combined release acceptance. Fresh workstation readiness, new success-rate evidence, external tool behavior and live publication remain unknown here.
