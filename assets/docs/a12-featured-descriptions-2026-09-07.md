# A12 Featured labels and destination descriptions

## Scope and dependency review

Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`. Source-only branch: `codex/a12-featured-descriptions`.

Confirmed X05: the homepage called the diagram feature the most recent public work. Its article metadata records April 7 publication and May 24 modification, while MurderBird records September 5 publication. The homepage feature and mixed Writings shelf now say Featured. Existing selections, dates, links, anchors and artwork are preserved. The first source commit is `2074a969825e81e742d728b6816fb0adb364b445`.

Reviewed A06 commit `d763059a58a5b60aaefb1d47773a00939ce090a0` and its content-truth report. Its workbench descriptions distinguish a May build journal and dated benchmarks from unverified RAG integration. Its Vault social descriptions identify one available template and planned resources. Independent review found Vault's ordinary `meta:description` was still the old multi-download claim. A12 corrects that field to match A06's social descriptions and aligns the workbench JSON-LD description with A06's ordinary/social descriptions. No new dates or schema fields are introduced.

A11's owner confirmed that the registry will preserve these editorial descriptions and expose project status separately. Full A11 implementation was still pending at this checkpoint. A21 must verify the combined result against that contract. A06 body and social metadata changes are required dependencies, not duplicated in this branch.

## Exact source changes

- `site-src/pages/index.main.html`: Featured heading, description and pill.
- `site-src/pages/writings/index.main.html`: Featured shelf heading.
- `site-src/pages.json`: Vault ordinary description only.
- `site-src/pages/projects/mac-studio-local-ai-workbench/index.extras.html`: JSON-LD description only, plus final newline normalization.

## Verification

| Check | Result | Evidence and limits |
| --- | --- | --- |
| Direct `build-site.py` renderer with BeautifulSoup assertions | PASS | Homepage and Writings Featured labels present; all hrefs, image sources, IDs and structured data match the previous generated pages. |
| Combined A06 metadata plus A12 source, parsed in memory | PASS | Vault ordinary/OG/Twitter descriptions agree. Rendered workbench ordinary/OG/Twitter/JSON-LD descriptions agree. Non-description SoftwareApplication fields unchanged. |
| `py -3 scripts/build-site.py --check` | Expected FAIL | Source-only handoff leaves generated pages stale; initially exactly homepage and Writings, with Vault and workbench added by the final metadata changes. A21 must regenerate. |
| `git diff --check` | PASS | No whitespace errors. Windows line-ending normalization notices are not test failures. |
| Browser/social-provider previews, search-owner tools, CI, live publication | NOT RUN | No visual redesign or discoverability improvement is claimed. Combined release acceptance belongs to A21. |

## Integration requirements

Apply A06 and both A12 source commits, preserving all scoped hunks in shared files. After A11 status integration, regenerate HTML, search/universe and CSP through the active release pipeline; verify freshness, links, locale boundaries and affected preview descriptions. Do not hand-merge generated output. This source-only branch is not independently release-ready.

The homepage English label changes require exact-pair locale review together with A06's homepage changes. No locale file, approval hash, publication date or noindex boundary was changed here. A06's report records the existing pilot/regional drift; A21 must resolve the applicable release requirements without claiming translation acceptance from structural checks. Writings, Vault and the workbench are outside the configured four-route translation pilot.

C08 source coverage is complete when A06 and A12 are combined. Final A11 consistency, generated previews, actual social previews, locale acceptance and publication remain unverified. No worker merge or deployment occurred.

## A11 dependency review addendum

Reviewed `9bfe170badf3133fab8119643aafeb1f04d2d0c9` after its handoff. Confirmed: it does not change `pages.json` or the workbench extras fragment. Its renderer applies project status only to main content, and its search integration adds a status summary to body text without replacing editorial metadata. The workbench record explicitly says published build journal, dated build record with current readiness unverified, May 30 benchmark, August 2 end-to-end RAG unverified, and delivery unknown. Those fields agree with A06/A12 descriptions. A12 accepts the source compatibility contract; combined rendering and release validation remain A21 responsibilities. This resolves the pending A11 source-contract review recorded above without claiming integrated execution.
