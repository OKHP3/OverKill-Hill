# A11 registry implementation handoff

September 7, 2026. Source candidate built on baseline `98922aeb` and reviewed A06 `d763059a58a5b60aaefb1d47773a00939ce090a0` (local cherry-pick `74179e4b`). The earlier inventory checkpoint remains a historical audit, not the current implementation disposition.

## Result and source contract

`site-src/project-status.json` is schema 2 and owns 18 records: all 14 detail pages and four named shelf exceptions. `availability`, `maturity`, and `evidence` are separate fields. Records include review scope/date, explicit shelf membership/exclusion reasons, and immutable public source links. These are source-described editorial facts. All current runtime delivery remains `unknown`; schema 2 deliberately cannot certify delivery merely by editing a status string. A future delivery-proof extension must add a scoped acceptance contract and tests.

`scripts/project-status.py` validates source coverage and renders one summary per detail or applicable card. The summary uses `data-project-status`, with canonical text in `data-project-status-text` and an evidence link/date. Generated content carries `AUTOGEN:PROJECT-STATUS` comments and is idempotent. `scripts/build-site.py` calls it without requiring hand-edited generated HTML. Current maturity pills were removed from eight detail source fragments; their history and descriptive tags remain. The homepage selected records use the same summaries. Projects uses explicit `data-project-shelf` markers so coverage does not depend on heading wording. Existing Status and proof heading anchors remain and link to the shelf instead of repeating a separate two-record authority.

`scripts/build-search-index.py` prefixes English project page bodies with the same summary before excerpt truncation. Editorial descriptions are untouched and remain A06/A12-owned. Noindex concepts stay excluded. A04's parser/extraction patch is disjoint from this small entry-construction hook; A21 must regenerate from both. Universe generation remains owned by its existing generator and skill; A11 changes only its obsolete status-card section, retaining the heading anchor.

Evidence links use the already public baseline page records, with the workbench linking the public August readiness report at `863d48a8`. The unpushed A06 local commit is not exposed as a supposedly public evidence link. These links describe source evidence, not fresh external functional tests. Workbench summary preserves the May benchmark/August RAG distinction, LifeTrkr stays pre-production, BPMN stays a prototype, and Telling Forward stays a static Author App prototype with separate service operations.

## Validation

| Check | Result | Evidence / limit |
| --- | --- | --- |
| `py -3 tests/test-project-status.py` | PASS | Seven tests: missing detail, duplicate route, undeclared shelf exception, unsupported delivery proof, missing source, idempotent rendering, and deliberate homepage/card/detail/search corruption. |
| `py -3 scripts/check-project-status.py` | PASS | 18 records; detail, shelf, evidence link/date, indexing and page-search summaries agree. |
| `py -3 scripts/build-site.py --check` | PASS | 36 generated English pages after local regeneration. |
| `py -3 scripts/build-search-index.py --check` | PASS | 160 entries after local regeneration; concepts excluded. |
| `py -3 scripts/validate-site.py` | PASS with warnings | 56 HTML pages; 32 existing structural warnings; no new voice warnings. MTB version/banner checks pass. |
| `py -3 scripts/check-locale-links.py` | PASS | Existing pilot link structure retained. This is not linguistic acceptance. |
| `py -3 scripts/check-csp.py` | PASS | 56 pages. No runtime or policy edits. |
| `py -3 scripts/check-links.py` | PASS | Zero broken internal links or style issues; 31 sitemap URLs, 24 explicit noindex exclusions in this check's broader inventory. |
| Browser | PASS, scoped | Installed existing lockfile dependencies with `npm ci` (no graph change). `node scripts/phone-overflow-qa.mjs --base-url=http://127.0.0.1:5911` passed all 31 indexable routes at 320px. Targeted Playwright checks passed homepage, shelf and all 14 details at 320/1280px (32 route/viewport cases), including noindex concepts. Summaries visible and contained; served registry matched this candidate. |
| Assistive technology / presentation selection | NOT RUN | No human AT session or owner design selection. A14/A20/A21 retain those boundaries. |
| CI / live / external application acceptance | NOT RUN | Worker did not push, merge or deploy, and did not exercise external applications. |

The workflow's existing project-status step now also runs the seven regression tests. A21 should retain those two commands when reconciling the separately owned workflow edits.

## Integration and unresolved evidence

A21 owns combined generated HTML, search data, universe AUTOGEN content, CSP and fingerprints. Worker regeneration was verification only; none of those generated changes is included in the source commit. Regenerate with `build-site.py`, `build-search-index.py`, and `generate-csp.py`, then run freshness/status/regression checks and the full combined release gates. Tests that inspect generated consumers require that regeneration first on this source-only candidate.

A11 changes English homepage/Projects source and adds generated status copy. Locale provenance requires actual exact-pair review of those rendered strings, including registry-generated content, before adoption. Existing regional draft/noindex boundaries remain; no hash adoption was performed. A06's outstanding locale facts still apply. No blanket language or accessibility acceptance is claimed.

A12 retains description and Mac JSON-LD ownership. A14 can style or reorganize a selected set while preserving the canonical summary contract and explicit shelf markers; A11 did not change CSS or choose a visual direction. A15 must not turn source-described maturity into a service promise. External runtime delivery and current workstation readiness remain UNKNOWN; dated functional evidence is the next check that could change that classification.

Browser evidence: `a11-project-status-320.png` and `a11-project-status-1280.png` are retained in this task artifact folder outside the repository. The reusable browser test writes screenshots to a unique temporary directory, keeping tracked source clean. `node tests/test-project-status-browser.mjs --base-url=http://127.0.0.1:5911` reproduces this scoped check. Visual review identified repetitive evidence text in the initial pass; final generic evidence was shortened to Source description only / Shelf reference only, retaining explicit Delivery: unknown. External requests were blocked in the targeted rendering probe; it establishes local layout, not external health.

## Exact A11 implementation files

- `.github/workflows/validate.yml`
- `assets/docs/a11-project-status-implementation-2026-09-07.md`
- `scripts/build-search-index.py`
- `scripts/build-site.py`
- `scripts/check-project-status.py`
- `scripts/project-status.py`
- `site-src/pages/index.main.html`
- `site-src/pages/projects/abrahamic-reference-engine/index.main.html`
- `site-src/pages/projects/bpmn-for-mermaid/index.main.html`
- `site-src/pages/projects/found-ry/index.main.html`
- `site-src/pages/projects/glee-fully-chai-chasers/index.main.html`
- `site-src/pages/projects/index.main.html`
- `site-src/pages/projects/kierans-lifetrkr/index.main.html`
- `site-src/pages/projects/mermaid-theme-builder/index.main.html`
- `site-src/pages/projects/skillz/index.main.html`
- `site-src/pages/projects/telling-forward/index.main.html`
- `site-src/pages/universe/index.main.html`
- `site-src/project-status.json`
- `tests/test-project-status-browser.mjs`
- `tests/test-project-status.py`
