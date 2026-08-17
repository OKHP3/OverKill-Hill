# Site-Wide Accessibility, Usability, Readability & Functional QA Audit

Audit date: 2026-08-16  
Target: `https://overkillhill.com/`  
Scope: 32 production HTML pages, including six live pages absent from `sitemap.xml`  
Status: findings-only; no production code was changed during this audit

## 1. Executive Summary

- **P1 — Mobile navigation exposes closed links to assistive technology.** At 390px, the closed `.primary-nav` is translated off-screen but remains present in the accessibility tree. This can place invisible menu links in the screen-reader and keyboard sequence. Affects the shared header on the whole site.
- **P2 — Search result updates are not announced.** The overlay replaces the result list with `innerHTML`, but the result container has no live-region semantics. A screen-reader user can type a successful query without hearing that results changed.
- **P2 — The site is not yet ready for a conformance claim at 400% zoom.** The available browser surface tested responsive widths, not true browser zoom. A real 400% reflow pass remains required before claiming WCAG 2.2 AA.
- **P2 — The site has no contact form.** The Contact page provides a `mailto:` link and external Ko-fi link. This is functional, but users expecting a web form are not told that no form is provided.
- **P2 — One live editorial image lacks intrinsic dimensions.** `manifesto/index.html` omits `width` and `height` on its main image, leaving a layout-stability/performance issue for slow-connection and low-vision users.
- **P2 — Readability is above the stated plain-language target for most non-article templates.** Homepage, hubs, project detail, interior, contact, holding, and utility samples measure below a Flesch Reading Ease target of 60 and/or above an eighth-grade target.
- **Pass — Core page structure is consistent.** All 32 tested production pages loaded with one `main`, one `h1`, a skip link, and no browser console errors in the sampled live runs.
- **Pass — Responsive width checks found no horizontal overflow** at 390×844, 768×900, or 1440×900 on the homepage, Contact, Search, long-form article, or BPMN project page.
- **Pass — Mermaid rendering succeeded** at all three requested widths on the representative article: two SVG diagrams rendered with no console errors.
- **Unknown — Native screen-reader output, true 400% zoom, and cross-origin iframe internals require human/device verification.** The accessibility-tree results below are best-evidence observations, not a substitute for NVDA, VoiceOver, JAWS, or TalkBack.

## 2. Methodology

The audit used a template-first approach against the live public site and the current checkout at commit `a3e09b9`.

- Loaded all 32 production pages listed in the repository's template map, plus `/found-ry/`, and recorded title, `h1`, `main`, navigation, skip-link, form/control, image, iframe, overflow, and console-error signals.
- Deep-sampled one live instance of each of the ten declared templates: homepage, hub, article, article-study, project-detail, interior-single, interior-form, error, holding, and utility.
- Spot-checked the remaining live pages through direct navigation for common structural signals; page-specific deviations are called out below.
- Used the in-app browser accessibility tree for landmark, heading, control-name, mobile-menu, search-dialog, iframe-title, and Mermaid-rendering observations.
- Exercised the mobile menu, theme toggle, search overlay, search query, redirect path, and page navigation through browser controls. No forms were submitted and no external side effect was triggered.
- Tested responsive rendering at 390×844, 768×900, and 1440×900. Measured document width against viewport width for overflow.
- Measured representative rendered color pairs where foreground/background were directly available as opaque computed styles. Transparent/gradient compositing pairs were not promoted to numeric pass/fail claims.
- Calculated Flesch Reading Ease and Flesch-Kincaid Grade using a local standard-library script over representative template source text. The target used here is Reading Ease ≥60 and grade level ≤8; this is a usability target, not a WCAG requirement.
- Ran repository validation and link checking separately: `python3 scripts/validate-site.py` passed; `python3 scripts/check-links.py` found zero broken links and six sitemap omissions.
- No axe-core, Lighthouse, WAVE, NVDA, JAWS, VoiceOver, TalkBack, or true browser-zoom scan was available in this run. Therefore no automated/manual disagreement is claimed, and the relevant rows remain limited or marked for human verification.

## 3. Page & Template Inventory

Deep sample means the page was used for the full live-browser interaction and accessibility-tree pass. Structural spot-check means it was directly loaded and checked for the shared signals; the result is inherited only for findings explicitly marked as shared.

| Page | Template | Coverage |
|---|---|---|
| `/` | homepage | Deep sample |
| `/projects/` | hub | Deep sample |
| `/writings/` | hub | Structural spot-check |
| `/writings/first-diagram-is-a-liar/` | article | Deep sample |
| `/writings/first-diagram-is-a-liar/v03/v1-heat-a/` | article-study | Deep sample |
| `/writings/first-diagram-is-a-liar/v03/v1-heat-b/` | article-study | Structural spot-check |
| `/writings/first-diagram-is-a-liar/v03/v2-heat-a/` | article-study | Structural spot-check |
| `/writings/first-diagram-is-a-liar/v03/v2-heat-b/` | article-study | Structural spot-check |
| `/projects/abrahamic-reference-engine/` | project-detail | Deep sample / iframe variant |
| `/projects/bfs-framing-intelligent-futures/` | project-detail | Structural spot-check |
| `/projects/bpmn-for-mermaid/` | project-detail | Deep sample / iframe variant |
| `/projects/found-ry/` | project-detail | Structural spot-check / iframe variant |
| `/found-ry/` | redirect to project-detail | Direct redirect check |
| `/projects/glee-fully-chai-chasers/` | project-detail | Structural spot-check / iframe variant |
| `/projects/hometools/` | project-detail | Structural spot-check; sitemap omission |
| `/projects/mac-studio-local-ai-workbench/` | project-detail | Structural spot-check |
| `/projects/mermaid-theme-builder/` | project-detail | Structural spot-check / iframe variant |
| `/projects/pathscrib-r/` | project-detail | Structural spot-check; sitemap omission |
| `/projects/skillz/` | project-detail | Structural spot-check / iframe variant |
| `/projects/un-nocked-truth/` | project-detail | Structural spot-check; sitemap omission |
| `/writings/biases-as-constants/` | project-detail | Structural spot-check; sitemap omission |
| `/writings/magnus-saga/` | project-detail | Structural spot-check; sitemap omission |
| `/about/` | interior-single | Deep sample |
| `/legal/` | interior-single | Structural spot-check |
| `/manifesto/` | interior-single | Structural spot-check / image variant |
| `/universe/` | interior-single | Structural spot-check / Mermaid variant |
| `/prompt-forge/` | interior-single | Structural spot-check |
| `/contact/` | interior-form | Deep sample; no HTML form present |
| `/search/` | utility | Deep sample |
| `/404.html` | error | Deep sample |
| `/under-construction.html` | holding | Deep sample |
| `/vault/` | interior-single | Structural spot-check |

The repository template map classifies `/writings/biases-as-constants/` and `/writings/magnus-saga/` as project-detail pages; that classification was retained for scope consistency and should be reviewed separately if those pages are intended to become article pages.

## 4. Accessibility Findings

### 4.1 Criterion scorecard by template

`Pass` means the tested evidence did not expose a defect in the sampled surface. `Partial` means a defect or limitation was observed. `Needs human verification` means the available tools could not establish conformance.

| WCAG 2.2 criterion | Template/site result | Evidence boundary |
|---|---|---|
| 1.1.1 Non-text Content | Partial | Images generally have alt text; the live source scan found one editorial image without intrinsic dimensions, but no missing `alt` was found. Alt quality still requires human review for long decorative/editorial descriptions. |
| 1.3.1 Info and Relationships | Pass with P1 mobile exception | All sampled pages exposed `main`, headings, navigation, and named controls; closed mobile navigation is still exposed when visually off-screen. |
| 1.3.2 Meaningful Sequence | Pass in sampled DOM | The accessibility tree followed the document sequence; visual/mobile menu state remains a separate issue. |
| 1.4.3 Contrast (Minimum) | Pass for measured opaque samples; incomplete overall | Measured opaque pairs included 12.97:1 for a representative link and 15.07:1 for the forge banner. Gradients, transparency, hover/focus states, and all tokens were not exhaustively measured. |
| 1.4.10 Reflow | Pass at tested widths; 400% unknown | No horizontal overflow at 390, 768, or 1440px on five representative pages. True 400% browser zoom was not available. |
| 2.1.1 Keyboard | Partial / needs human verification | Native buttons and links are used, and the menu/search controls respond to browser interaction. A reliable full Tab traversal could not be completed with this browser surface; closed mobile links therefore remain an unresolved keyboard concern. |
| 2.4.1 Bypass Blocks | Pass | A visible-on-focus skip link to `#main` was present on all directly loaded pages. |
| 2.4.2 Page Titled | Pass | All 32 loaded pages exposed a non-empty, page-specific title. |
| 2.4.3 Focus Order | Partial | The hidden-by-transform mobile navigation remains in the accessibility tree and may insert off-screen links into the focus order. |
| 2.4.4 Link Purpose (In Context) | Pass with usability caveats | Primary links were named; generic brand vocabulary can still require surrounding context for unfamiliar visitors. |
| 2.4.7 Focus Visible | Needs human verification | Source CSS defines global `:focus-visible` rules, but a complete browser Tab traversal and visual focus inspection were not reliable in the available surface. |
| 2.4.11 Focus Not Obscured (Minimum) | Needs human verification | Sticky header, mobile menu, and anchor targets need a real keyboard/zoom pass. |
| 3.2.1 On Focus | Pass in sampled interaction | No unexpected navigation or context change was observed from focus alone. |
| 3.2.2 On Input | Pass in sampled interaction | Search updates results without navigation; the URL is updated on the dedicated search page as the query changes. |
| 4.1.2 Name, Role, Value | Partial | Menu and theme controls expose names and `aria-expanded`; the closed mobile navigation has no equivalent hidden/inert state. Cross-origin iframe internals were not inspectable. |
| 4.1.3 Status Messages | Partial | Search result changes are injected into `.okh-search-results` without `aria-live` or an equivalent status announcement. |

### 4.2 Findings

| ID | Page/Template | WCAG 2.2 Success Criterion | Severity | Persona(s) Affected | Evidence | Recommended Fix |
|---|---|---|---|---|---|---|
| A11Y-01 | Shared header; all pages at ≤768px | **2.4.3 Focus Order; 4.1.2 Name, Role, Value** | **P1 serious** | 1 Screen reader, 2 Keyboard-only, 5 Cognitive/attention, 6 Motor-impaired on mobile | At 390px with the menu closed, the accessibility tree still exposed the full Primary navigation and all submenu links. `assets/css/theme.css:830-853` moves `.primary-nav` with `transform: translateY(-120%)` but does not remove it from the accessibility/focus sequence. `assets/js/app.js:44-51` toggles only the header class and `aria-expanded`. | When closed, apply `inert` and `aria-hidden="true"` to the navigation and ensure the hidden state cannot receive focus. On open, remove `inert`, set `aria-hidden="false"`, and move focus predictably into the menu. Add a regression check that closed mobile nav links are absent from the accessibility tree/focusable set. |
| A11Y-02 | Shared search overlay and `/search/` | **4.1.3 Status Messages** | **P2 moderate** | 1 Screen reader, 5 Cognitive/attention, 8 Slow/mobile | `assets/js/app.js:452` creates a result container with `role="list"`; `assets/js/app.js:519-557` replaces its contents on every query without `aria-live`, a result count announcement, or focus movement. Browser testing confirmed 12 results appear for “Mermaid,” but no announcement mechanism is present. | Add a concise `role="status" aria-live="polite" aria-atomic="true"` result-count element and update it after each search. Keep focus in the search field; do not move focus into the result list on every keystroke. |
| A11Y-03 | `manifesto/index.html` | **1.4.10 Reflow** (performance evidence supporting reflow risk) | **P2 moderate** | 3 Low vision, 8 Slow/mobile | The live/source image `/assets/img/library/over-kill-hill-p3-title-low-right-bird-perch-comp-square-1024.webp` has `alt` text but no `width` or `height`. The same page was the only production page found by the image-attribute scan with missing intrinsic dimensions. | Add the image's intrinsic dimensions to the markup or wrap it in a stable aspect-ratio container; verify no content shift at mobile and 400% zoom. |
| A11Y-04 | Site-wide, all templates | **2.1.1 Keyboard; 2.4.7 Focus Visible; 2.4.11 Focus Not Obscured** | **P2 moderate / needs human verification** | 2 Keyboard-only, 3 Low vision, 6 Motor-impaired | The source contains global focus-visible rules (`assets/css/theme.css:259-264`), but the available browser automation did not produce a reliable full Tab sequence for visual inspection. The theme-toggle rule later suppresses `outline` and relies on a border-color change (`assets/css/theme.css:888-892`). | Run a real keyboard pass in Chrome + VoiceOver/NVDA at desktop and mobile widths. Confirm every control has a visible 2px-equivalent focus indicator, that it meets contrast against its immediate background, and that sticky header/menu layers do not obscure the focused target. |

### 4.3 Persona coverage

| Persona | Concrete result |
|---|---|
| 1 Screen reader user | **Issue found:** closed mobile navigation remains in the accessibility tree; search results lack a status announcement. Native page landmarks and titles passed the tree inspection. |
| 2 Keyboard-only user | **Issue found / human verification needed:** the hidden mobile menu is a focus-order risk; full Tab traversal was not reliable in this browser surface. |
| 3 Low-vision user at 200%/400% | **Needs manual verification:** no overflow at tested CSS widths; true 400% zoom was not run. One image lacks dimensions and may contribute to layout movement. |
| 4 Color-blind user | **No direct issue found in the sampled tree:** state controls have text/ARIA labels and links use text, not color alone. Color-state contrast across every hover/focus combination remains unmeasured. |
| 5 Cognitive/attention differences | **Issue found:** invisible mobile navigation can create unexpected navigation choices; search does not announce result changes. Forge vocabulary and dense copy add comprehension load. |
| 6 Motor-impaired touch user | **No target-size failure directly measured:** theme toggle is declared at least 44×44px in CSS. Mobile menu and search were operable by browser click; real-device spacing and touch error tolerance remain unverified. |
| 7 Older/general-public visitor | **Usability issue:** technical terms and brand vocabulary are not consistently explained; contact is a mailto path rather than an on-site form. |
| 8 Slow/mobile user | **Issue found:** one image lacks intrinsic dimensions; third-party fonts, analytics, and iframe surfaces add requests. Network timing and transfer budgets were not measured. |

## 5. Usability Findings

| ID | Page/Task | Heuristic Violated | Persona(s) Affected | Evidence | Recommended Fix |
|---|---|---|---|---|---|
| UX-01 | Mobile menu / find a project | **H1 Visibility of system status; H3 User control and freedom** | 1, 2, 5, 6 | The menu button exposes `aria-expanded`, but the closed menu remains present in the accessibility tree while visually translated away. | Couple the visual state and assistive-technology state; expose the menu only when open and return focus to the toggle on close. |
| UX-02 | Search / find a specific project | **H1 Visibility of system status** | 1, 5, 8 | “Mermaid” produced 12 results, but the result count is not announced and the result list has no explicit empty/loading status beyond visual content. | Add polite result-count and loading/error status text; preserve the input as the stable interaction point. |
| UX-03 | Contact / contact or hire | **H6 Recognition rather than recall; H10 Help and documentation** | 5, 7 | The page offers email and Ko-fi but no explicit “Contact form unavailable—email us” explanation. A visitor must infer the intended contact path from prose. | Add a short plain-language contact instruction near the first CTA, including what to send and expected next step, without adding a form if email is intentional. |
| UX-04 | All long-form/project pages / understand the offer | **H2 Match between system and real world; H10 Help and documentation** | 5, 7 | Representative copy uses terms such as “protocol-first promptcraft,” “ROY,” “Custom GPT,” “ship gate,” “knowledge routing,” and “Mermaid” without a consistent first-use plain-language explanation. | Add short first-use explanations or a glossary link for domain terms; retain the forge visual language. |
| UX-05 | Project pages with embedded tools / use the live demo | **H1 Visibility of system status; H3 User control and freedom** | 3, 5, 6, 8 | Iframes have descriptive titles and lazy loading, but their cross-origin loading state and internal keyboard behavior cannot be verified from the parent page. | Add visible “Loading live demo…” / “Open full demo” fallback text and verify the embedded application independently with keyboard and mobile AT testing. |

## 6. Readability Scorecard

Target: Flesch Reading Ease **≥60** and Flesch-Kincaid Grade **≤8**. Scores are calculated from representative page text with a heuristic syllable counter; they are directional and should not be treated as a certification.

| Template | Representative page | Reading Ease | Grade | Target result | Jargon/density flag |
|---|---|---:|---:|---|---|
| homepage | `/` | 56.8 | 10.0 | Fail | “protocols,” “agentic workflows,” “local inference,” and “multi-model pipelines” appear before a plain-language explanation. |
| hub | `/projects/` | 49.2 | 10.6 | Fail | Project cards assume familiarity with Custom GPTs, Mermaid, BPMN, and promptcraft. |
| article | `/writings/first-diagram-is-a-liar/` | 63.5 | 7.2 | Mixed pass | Reading ease passes, but technical terms and very long article length still require navigation support. |
| article-study | `.../v03/v1-heat-a/` | 66.7 | 10.2 | Mixed | Shorter sentences improve ease, but diagram/evaluation terminology raises grade complexity. |
| project-detail | `/projects/abrahamic-reference-engine/` | 43.2 | 10.2 | Fail | Dense product claims, implementation vocabulary, and embedded-tool context need a plain-language lead. |
| interior-single | `/about/` | 50.0 | 11.4 | Fail | Brand narrative and technical positioning are not consistently translated for general visitors. |
| interior-form | `/contact/` | 58.0 | 9.6 | Fail | Contact intent is understandable, but the page is prose-heavy and uses platform/payment terms. |
| error | `/404.html` | 61.9 | 8.9 | Mixed | Main recovery copy is readable; navigation choices still use site-specific names. |
| holding | `/under-construction.html` | 52.8 | 10.9 | Fail | Forge metaphor and ecosystem language obscure what the visitor can do next. |
| utility | `/search/` | 51.7 | 10.5 | Fail | Search controls are simple, but explanatory copy uses the site's internal categories. |

## 7. Functional QA Matrix

`Pass` means observed in the live browser. `Partial` means the parent page passed but a meaningful part of the behavior remained unverified. `Needs human verification` means the input/AT surface was not reliably available.

| Feature | 390px | 768px | 1440px | Mouse/touch | Keyboard | Screen-reader-equivalent |
|---|---|---|---|---|---|---|
| Primary navigation | Partial: opens; closed links remain exposed in tree | Pass structural | Pass structural | Pass via browser click | Partial; full traversal not reliable | Partial; closed state is exposed |
| Search overlay | Pass: opens and returns 12 Mermaid results | Pass structural | Pass structural | Pass | Partial: shortcut and full arrow/Enter traversal not fully verified | Partial: no result announcement |
| Dedicated search page | Pass loads and accepts query | Pass structural | Pass structural | Pass | Needs human verification for full results traversal | Partial: result status not announced |
| Contact path | Pass: mailto and Ko-fi links present | Pass structural | Pass structural | Pass | Pass link semantics | Pass tree naming; no form to test |
| Theme toggle | Pass: three-state label/state changes | Pass structural | Pass structural | Pass | Needs human focus-visibility verification | Pass name/value observed |
| Mermaid diagrams | Pass: 2 SVGs | Pass: 2 SVGs | Pass: 2 SVGs | Not applicable | Needs human keyboard review of diagram navigation | Needs human review of diagram semantics/description |
| BPMN iframe | Partial: titled iframe, cross-origin internals unverified | Partial | Partial | Parent surface present; child touch unverified | Child focus behavior unverified | Child tree unavailable cross-origin |
| 400% zoom/reflow | Not run | Not run | Not run | Not applicable | Not run | Not run |
| Console errors | No errors in sampled pages | No errors in sampled pages | No errors in sampled pages | N/A | N/A | N/A |

## 8. Prioritized Remediation Backlog

1. **[P1][WCAG 2.4.3, 4.1.2] Remove the closed mobile navigation from the accessibility and keyboard sequence with `inert`/`aria-hidden`, then restore it and manage focus when opened.** Affects screen-reader, keyboard-only, cognitive, and mobile motor-impaired users.
2. **[P2][WCAG 4.1.3] Add a polite, atomic result-count status message to the shared search overlay and dedicated search page.** Affects screen-reader, cognitive, and slow/mobile users.
3. **[P2][WCAG 2.1.1, 2.4.7, 2.4.11] Run and document a real Chrome + VoiceOver/NVDA keyboard/focus pass at desktop and mobile widths, including the theme toggle, sticky header, menu, search dialog, and anchor links.** Affects keyboard-only and low-vision users.
4. **[P2][WCAG 1.4.10 verification] Add intrinsic dimensions to the manifesto hero/editorial image and verify stable layout at mobile and 400% zoom.** Affects low-vision and slow/mobile users.
5. **[P2][H1/H6/H10] Add a plain-language contact instruction that states the intended email path, what to include, and the expected next step.** Affects cognitive and general-public users.
6. **[P2][H2/H10] Add first-use explanations or a glossary route for protocol-first promptcraft, ROY, ship gate, knowledge routing, and related technical terms.** Affects cognitive and general-public users.
7. **[P2][H1/H3] Add visible loading/fallback copy and an independent keyboard/mobile QA gate for each cross-origin embedded application.** Affects low-vision, cognitive, motor-impaired, and slow/mobile users.

### Automatable

- Detect mobile navigation containers that use off-screen transforms without `inert`/`aria-hidden` state synchronization.
- Detect dynamically rendered search result containers without a `role="status"`/`aria-live` result announcement.
- Detect production images missing `alt`, `width`, or `height` attributes.
- Detect pages with horizontal overflow at configured viewport widths.
- Detect iframe elements missing a descriptive `title`, and report cross-origin iframe URLs for separate QA.
- Add a machine-readable audit for heading/landmark counts, skip-link targets, control names, and `aria-expanded` state transitions.

## 9. Appendix

### Test conditions

- Audit date: 2026-08-16.
- Live target: `https://overkillhill.com/`.
- Browser surface: Codex in-app browser using a Chromium-backed accessibility tree and DOM evaluation.
- Browser/OS/AT versions: not exposed by the available browser surface; native NVDA, JAWS, VoiceOver, and TalkBack were not run.
- Viewports: 390×844, 768×900, and 1440×900.
- Directly exercised: mobile menu open/close, theme state control, search overlay open/query/close, `/found-ry/` redirect, Mermaid render, BPMN iframe parent surface, and page navigation.
- Repository checks: `python3 scripts/validate-site.py` passed; `python3 scripts/check-links.py` reported 0 broken links and six pages missing from the sitemap.
- Prior audit material consulted: `assets/audit/links-report-2026-08-08.json` and `assets/docs/audit-bpmn-for-mermaid-public-page-2026-08-06.md`. No previously resolved finding was reopened solely because it appeared in those artifacts.
- Browser limitations: no native screen-reader speech output, no reliable full Tab traversal, no true browser zoom override, no cross-origin iframe DOM access, and no network-transfer timing budget. Those limitations are marked as unknown or needs human verification above.
- External UI guidance consulted: [Vercel Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md), used as an additional heuristic reference rather than as a WCAG conformance substitute.
