# Visitor experience and content assessment

Assessment: September 7, 2026 UTC. Source baseline: `ca38d5b9fc46746ea8b41e2ba32e39685c53f511`. Site: https://overkillhill.com/. Author: Project Architect, with engineering assessment delegated through a Project Manager and two Workers.

## Judgment

Keep the industrial visual identity, MurderBird, source-generated static site, and substantial writing. The strongest improvement is a shorter path from a visitor's question to a usable artifact and credible evidence. The site already has the material; its entry hierarchy and status consistency lag behind that material.

There are also concrete reliability defects. On desktop, essential homepage content disappears visually when JavaScript is disabled. Search exposes selected results visually without equivalent focus/selection semantics, and some snippets contain literal HTML fragments. These merit correction before visual experimentation.

The successful skip-link, dedicated-search Enter, chapter navigation, and recent artwork fixes deserve to remain closed. This assessment does not repeat old failures simply because they appeared in the September 5 report.

## Evidence and coverage

- Inventoried all 36 authoritative English main-body sources, including headings, links, word counts, hashes and comparison with the prior audit's `897df5d3` source: [machine inventory](../audit/assessment-2026-09-07/content-inventory.json).
- Thirty-two main bodies are byte-identical to that earlier source. The four changed bodies are homepage, Mermaid Theme Builder, Universe, and MurderBird. This makes earlier source findings useful when rechecked, but does not make every old browser finding current.
- Read current source and prior content findings for installation, status, draft boundaries, workbench chronology, claims, licensing wording, metadata and reader orientation. Reviewed changed bodies and the MTB diff. Inventoried all routes; detailed human editorial review was focused, not a line-by-line factual certification of every quoted artifact or external project.
- Interacted with the live site in Edge on macOS: homepage, contact, overlay search, dedicated search, BPMN result/deep link, MurderBird chapters, and French homepage/search. Captured screenshots and accessibility states in the assessment conversation. These interactive screenshots remain session evidence, not committed screenshot files.
- Tested 390×844 phone emulation and 1280×800 desktop, plus the initial large desktop viewport. Temporary viewport, JavaScript and cache overrides were restored. Initial resize-transition imagery was discarded in favor of a fresh mobile reload.
- Worker Chromium checks cover the broader route/viewport matrix; see [validation report](audit-validation-2026-09-07.md). Browser automation and an accessibility tree are not VoiceOver/NVDA testing or WCAG certification.

The public web retrieval returned an older hero description than the directly inspected browser. Current browser observations and local sources govern the hero findings; a crawler's cached text is not treated as exact deployed-byte evidence.

## Reproduced visitor findings

| ID | Priority and tier | Evidence and consequence | Recommended change and acceptance |
| --- | --- | --- | --- |
| X01 | P1, confirmed | At 1280×800 with script execution disabled before loading `/`, the screenshot shows the hero background without its heading, text, art or buttons. The accessibility tree still contains them. `theme.css:1161` defaults `.reveal-on-scroll` to opacity zero; visibility depends on `app.js` initialization. | Make content visible by default. Enable optional reveal only after its controller is ready and fail open if it fails. Check desktop JS-disabled, blocked `app.js`, missing observer and reduced-motion states, with working links. A `noscript` patch alone would not cover a failed script download. |
| X02 | P1, confirmed | Overlay search for `mermaid`, followed by ArrowDown, leaves focus in the input. The input has no active-descendant relationship; selection is `data-active` only. The accessibility state does not change when the selected destination changes; Enter does navigate to that destination. | Use one complete interaction model: focused ordinary links, or a correctly implemented combobox. Preserve typed input, first/last behavior, Escape/focus return and URL state. Confirm the selected destination is exposed to assistive technology. |
| X03 | P1, confirmed | `mermaid` results include a literal `</div` fragment in the BPMN related-resources excerpt and a similar fragment in MTB results. Other snippets repeat headings. This is visible retrieval pollution; no executable injection was demonstrated. | Extract section text with an HTML parser and explicit section boundaries, then normalize whitespace and avoid duplicate heading insertion. Test nested markup, inline tags, entities, truncated tags, empty query and accents. Rebuild all affected search indexes. |
| X04 | P2, measured geometry; design proposal | At 390×844, homepage `h1` starts at x=0; the hero has no horizontal content gutter. `Start with the work` begins at y=1581 and `Selected work` at y=2351. Later sections have about 15.6px side spacing. Content extends far beyond the first screen before practical choices appear. | Restore a consistent phone gutter in the canonical CSS and move concise task choices earlier. Preserve art and motto. Compare two rendered variants with newcomer tasks. These positions indicate hierarchy cost, not a measured conversion loss or automatic WCAG violation. |
| X05 | P2, confirmed content mismatch | Homepage says its diagram feature is the most recent public work. The Writings shelf places the September MurderBird story first and labels the diagram piece Featured; the diagram article retains May metadata. | Make Featured and Latest distinct. Preserve the chosen diagram feature if desired; stop making it a chronological claim. Prefer one editorial metadata source for ordering and dates. |
| X06 | P2, confirmed | French homepage has French body text, but language/theme/search controls and search dialog use English names and instructions. `projets` returns French pages with English category labels and `3 results found for projets.` Full-search link routes to `/search/?q=projets`. | Complete exact-pair French interaction copy after English search semantics settle. Preserve a stated fallback to English content, with destination language visible where useful. Do not promote regional drafts through a string-only fix. |
| X07 | P2, proposal based on current content | Contact gives a usable email link, but no concise prompts for what an inquiry should include. The long support narrative follows a small contact block. | Add optional prompts for the problem, current process, desired result and constraints. Keep creator support separate from project inquiry. A form, CRM, calendar service or promised response time is not required. |
| X08 | P2, proposal | The first visible homepage text largely explains the forge metaphor and iteration status. The primary tool CTA still leads through a project page. The project shelf mixes case studies, prototypes and tools without a consistent front-of-card distinction. | Lead with a plain description of the work and an evidence-linked selected set. Use explicit `Try tool`, `Inspect project`, `Read journal` and `View concept` actions. Keep ecosystem terms as identity and optional depth. |

Current successes: the homepage skip link updates `#main`; the following Tab enters a link inside main. Dedicated search for MurderBird followed by Enter opens its story. `Read the story` moves focus to `the-maker` and updates the fragment. Expanded mobile navigation successfully reaches Contact. Search results now have listitem wrappers in current source. These are narrower observed successes, not complete accessibility certification.

## Content truth and useful next actions

| ID | Priority | Current source evidence | Recommendation |
| --- | --- | --- | --- |
| C01 | P1 | Skillz steps 4/5 at `site-src/pages/projects/skillz/index.main.html:655-669` teach a raw single-file download to `.agents/skills/my-skill.md`. The URL is explicitly an example placeholder, but the package shape is still incomplete for a normal skill-directory installation. | Use a real public full-directory package, immutable revision, named client and fresh-project validation. Include companion resources and a no-overwrite guard. Separate manually loading a document from installing a discoverable skill. |
| C02 | P1 | Mac workbench lines 130/131 and May 30 entry say RAG and strict benchmarks completed; lines 1001 onward still list them as next steps. | Frame this as a dated build journal. Preserve historical tables, mark superseded plans as historical, and state what the cited evidence establishes. Do not claim to have audited today's workstation. |
| C03 | P1 | Registry contains two records among 14 project detail pages. Shelf introduction describes its mixed set as shipped and maintained. Telling Forward, LifeTrkr and BPMN detail pages contain maturity qualifications missing on the shelf. | Expand a single status authority after inventorying its consumers. Separate page publication, software maturity and delivery evidence. Use explicit unknowns where current evidence is missing. |
| C04 | P1 | Hometools, Pathscrib-r and Un-nocked Truth are noindex concepts with present-tense capability claims and no visible concept notice in their main bodies. | Add visible status, planned wording and a useful return/inquiry route. Keep their noindex decisions and URLs. Exclusion from search does not communicate status to someone following a direct link. |
| C05 | P1 editorial correction | Found-Ry FAQ line 619 combines Apache-2.0 reuse with an unqualified assertion that attribution is not required. | Separate optional promotional credit from redistribution requirements, linking to the actual license and applicable notices. Keep the code license distinct from rights in separately created exported content. |
| C06 | P2 | Homepage says every system is road-tested and ready for a daily stack; BPMN says valid first-try generation with no syntax repair; Vault describes all offered artifact categories as production-tested while only one download is available. | Preserve confidence and humor, but attach measurable claims to a named version/sample or describe the design intent. Align cards, metadata and detail-page limitations. Do not rewrite protected fiction or the original manifesto to satisfy a marketing template. |
| C07 | P2 | Main diagram article is an 18,000-plus-word combined essay/artifact archive with a 45-minute label. It already supplies a short argument/evidence/archive jump menu. MurderBird now has a reading estimate and chapter navigation. | Build on these working entry aids. Add a short reader route or annotated example when useful; retain original URLs, anchors and complete archives. Do not split long writing solely to achieve an arbitrary word count. |
| C08 | P2 | Vault metadata advertises several downloadable artifact types while its visible list contains one template and explicit future resources. Workbench metadata says build complete without the same historical framing as the journal. | Align descriptions with actual destinations before cosmetic SEO work. Validate social cards in real previews and verify search indexing in owner tools before claiming discoverability gains. |
| C09 | P2 | Active operational docs contain old future work and retired commands. Historical closeouts mention other-machine stashes/worktrees. | Use one dated active plan and evidence per acceptance condition. Retain historical reports with clear dates; do not reclassify older machine observations as today's Git state. A bounded runbook repair is delegated in this session. |

The Agent Skills specification defines the package as a directory with `SKILL.md` and optional supporting resources. This supports C01's package correction, not a claim that every client has identical discovery rules. [Agent Skills specification](https://agentskills.io/specification).

Apache-2.0 section 4 states redistribution conditions concerning the license, changes and applicable notices. That supports replacing the FAQ's blanket wording; it does not establish the license of unrelated generated content. [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Route-by-route editorial disposition

These are website-content observations. External tool functionality and business outcomes remain separate assessments. Source identity and content volumes are reproducible from the linked inventory.

| English route | Role / disposition | Next useful action |
| --- | --- | --- |
| `/` | Public orientation, selected work, feature and ecosystem links | X01, X04, X05, X08; keep current identity |
| `/about/` | Public biography and positioning | Preserve approved credentials and unnamed-employer boundary; link to concrete work |
| `/contact/` | Direct inquiry and support | X07; test copy/email fallback without sending |
| `/legal/` | Privacy and use disclosure | Align with observed runtime and owner policy; account/legal review not performed |
| `/manifesto/` | Protected origin and long-form principles | Preserve original; improve navigation only with voice intact |
| `/projects/` | Mixed project shelf | C03; one status and one primary action per card |
| `/projects/abrahamic-reference-engine/` | Active v1.1 reference tool description | Verify version/source rights when updating; no theological accuracy certification here |
| `/projects/bfs-framing-intelligent-futures/` | Explicit independent public-information prototype | Preserve unofficial boundary; qualify broader influence claims |
| `/projects/bpmn-for-mermaid/` | Prototype parser/playground plus skill suite | Carry honest prototype scope into hero/card; validate examples and downloads separately |
| `/projects/first-diagram-is-a-liar/` | Writing companion and evidence archive | Retain unverified tutorial-route qualification until tested |
| `/projects/found-ry/` | Browser workbench description | C05; distinguish rubric passage from proven production behavior |
| `/projects/glee-fully-chai-chasers/` | Game and multi-agent case study | Preserve fictional currency and storage/iframe boundaries |
| `/projects/hometools/` | Noindex concept | C04; visible status and planned wording |
| `/projects/kierans-lifetrkr/` | Pre-production personal application description | Carry detail-page limitation onto shelf |
| `/projects/mac-studio-local-ai-workbench/` | Dated build journal | C02; current versus historical clarity |
| `/projects/mermaid-theme-builder/` | Shipped workbench and skill family description | Retain versioned full-package examples; measure embedded first-task experience |
| `/projects/pathscrib-r/` | Noindex concept | C04; no inferred relationship/replacement with Telling Forward |
| `/projects/skillz/` | Live catalog, variable contract maturity | C01; preserve maturity/evidence distinction |
| `/projects/telling-forward/` | Early prototype, separate service surfaces | Keep qualified description consistent across cards and metadata |
| `/projects/un-nocked-truth/` | Noindex concept | C04; do not imply launched advice tools without evidence |
| `/prompt-forge/` | Methods and public/internal capability descriptions | Make reusable public material easy to distinguish from internal patterns |
| `/vault/` | One template plus planned artifacts | C06/C08; one truthful download boundary |
| `/universe/` | Generated published-page map with HTML links | Preserve no-JS outline and explicit page-publication versus project-completion distinction |
| `/writings/` | Published writing and concept shelf | Use as model for Featured versus Latest |
| `/writings/murderbird/` | Expanded fictional origin with accepted stills | Preserve chapters, alt text, source/artwork provenance and fiction framing |
| `/writings/first-diagram-is-a-liar/` | Essay and historical experiment archive | C07; preserve sample qualifications, failures and artifacts |
| `/writings/first-diagram-is-a-liar/v03/v1-heat-a/` | First-pass field guide | Retain experiment/date context and route to argument |
| `/writings/first-diagram-is-a-liar/v03/v1-heat-b/` | First-pass field guide | Same; do not treat old voting language as an open poll |
| `/writings/first-diagram-is-a-liar/v03/v2-heat-a/` | Revised field guide | Retain round/role boundaries and historical results |
| `/writings/first-diagram-is-a-liar/v03/v2-heat-b/` | Revised field guide | Same; preserve diagram source and output pairs |
| `/writings/biases-as-constants/` | Visibly labeled research draft | Preserve status; publish substantive evidence only when ready |
| `/writings/magnus-saga/` | Visibly labeled fiction concept | Preserve intentional unpublished boundary |
| `/found-ry/` | Legacy redirect | Retain URL continuity |
| `/search/` | Noindex utility | X02/X03; preserve working Enter/query/category behavior |
| `/404.html` | Recovery utility | Consider a direct missing-page heading; keep recovery paths |
| `/under-construction.html` | Holding utility | Keep local meaning; do not imply the entire site is unfinished |

The additional 20 locale HTML pages are five four-route variants of homepage, projects, about and contact. French is the indexable pilot; German, Spain Spanish, UK English and Mexican Spanish retain draft/noindex boundaries. Linguistic quality was not certified. French interaction testing is detailed above; broader locale structural checks belong to the validation report.

## Performance observation and next experiment

A single cache-disabled live Edge load at 1280×800 produced 433,582 encoded network bytes for HTTPS site/third-party requests observed after loading `/`. Of those, 192,076 were first-party. The selected 960px WebP was 75,476 bytes; shared CSS 49,558; shared JS 14,179; Google tag script 173,771; observed Google font CSS/fonts together 67,735. Browser-extension requests were excluded. Analytics query identifiers and client parameters are intentionally omitted from durable evidence.

This is one existing-profile, unthrottled desktop load with HTTP cache disabled. It excludes unrequested lazy media and unfinished request lengths, is not a fresh-user profile, and supplies neither LCP/INP/CLS percentiles nor a mobile field baseline. It does show that the source budget's roughly 5.45 MB inventory is not this visitor's initial transfer. Keep both metrics with their different meanings.

Next, measure cold and warm loads on homepage, long diagram article, MurderBird and one embed page at fixed phone/desktop network and CPU settings. Record browser-selected images, font behavior, external requests, scrolling and interaction responsiveness. Review whether analytics provides useful decisions before altering its loading or policy. Preserve accepted source illustrations; optimize served derivatives based on measured contributors and visual comparison.

## Source ledger and claim limits

All sources below retrieved September 7, 2026. Local source paths above support current implementation and content facts. External sources support criteria, not findings that were never tested.

| Source / publisher | Supported criterion | Authority and limitation |
| --- | --- | --- |
| [Progressive enhancement, MDN](https://developer.mozilla.org/en-US/docs/Glossary/Progressive_Enhancement) | Essential content should survive unavailable enhancements, X01 | Maintained platform guidance; not a site-specific audit |
| [Combobox pattern, W3C WAI](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/) | Coherent selection/focus semantics if choosing that model, X02 | Official authoring pattern; ordinary focused links remain an alternative |
| [Reflow, W3C WAI](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) | 320 CSS-pixel reflow and exceptions for inherently two-dimensional content | Official criterion explanation; a responsive suite alone is not conformance |
| [Focus Visible, W3C WAI](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html) | Visible keyboard focus during task continuation | Official criterion explanation; real assistive-technology review still needed |
| [Web Vitals, Google web.dev](https://web.dev/articles/vitals) | Distinguish experience metrics and field evidence from asset counts | Primary browser performance guidance; no current field measurements retrieved |
| [Agent Skills specification](https://agentskills.io/specification) | Directory/package shape, C01 | Format authority; client discovery differs |
| [Apache License 2.0, ASF](https://www.apache.org/licenses/LICENSE-2.0) | Redistribution notice conditions, C05 | Actual license text; exported artifacts need their own rights determination |

The consequence of mistaking these recommendations for facts would be unnecessary redesign, changed owner claims, or false readiness assurances. Resolve that through small tested corrections, owner review of new positioning, and observed visitor tasks. Next action: implement X01-X03 and C01-C05 through the scoped packages in the [current advancement plan](website-advancement-plan-2026-09-07.md).
