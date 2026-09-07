# A20 independent accessibility acceptance

## Disposition and candidate

**REJECT baseline for accessibility acceptance. Integrated candidate acceptance remains BLOCKED pending A21's named candidate.** This review independently reproduces X01, X02, and X03 against `98922aebf71d90b2b18ecc34c8b00a041fff51c7`. Passing existing automation does not close these failures. A01/A02 are committed in this baseline; the advancement plan's uncommitted wording is historical.

Reviewed on September 7, 2026 in the isolated Windows checkout `C:\Users\jamie\.codex\worktrees\269e\overkill-hill`. Initial status was clean, HEAD detached at the named baseline. No candidate source, generated pages, CSS, JS, policies, or dependencies were changed. Existing locked dependencies were installed with `npm ci --ignore-scripts`. The review adds only this report and two machine evidence files on `codex/a20-accessibility-acceptance`.

Local preview used the unchanged `server.py` with `HOST=127.0.0.1`, `PORT=5220`. SHA-256 comparison confirmed the HTTP root response matched this checkout's `index.html`. This establishes local root identity, not an all-file release manifest or deployment identity.

Environment: Node v24.11.1, Playwright 1.62.1, Chromium 151.0.7922.34, Firefox 153.0, and Playwright WebKit 26.5. Browser sessions were headless automation on Windows. They were not human sessions. No actual screen reader was operated. WebKit is not Safari.

## Five visitor tasks

These are bounded visitor tasks with observable success criteria. Desktop viewport was 1280 x 800; compact navigation used 390 x 844. The focused search retest used Playwright's default 1280 x 720 viewport. Keyboard input was sent through Playwright; DOM observations measured focus and state, rather than claiming spoken announcements.

| Task and reproduction | Success criterion | Chromium | Firefox | WebKit |
| --- | --- | --- | --- | --- |
| T1: Read the homepage and identify its purpose when enhancements fail. Load `/` normally, with JavaScript disabled, with `**/assets/js/app.js*` aborted, with `window.IntersectionObserver=undefined` before load, and with reduced motion. | Essential hero heading remains painted. | FAIL: ancestor opacity 0 in all three failure modes. Normal content was mid-reveal at 0.861; reduced motion was 1. | FAIL: ancestor opacity 0 in all three failure modes; normal and reduced motion were 1. | BLOCKED: stylesheet and runtime failed to load; opacity 1 is not a successful styled-site check. |
| T2: Skip repeated navigation and continue reading. From fresh `/`, press Tab, Enter, Tab. | First focus is the skip link; URL becomes `#main`; next link is inside main. | PASS: next focus was `The Forge`. | PASS: next focus was `The Forge`. | BLOCKED by asset-loading failure. |
| T3: Find contact information from compact navigation. At 390 x 844, Tab to navigation toggle, Enter, Tab to Contact, Enter. | Toggle exposes expanded state and keyboard navigation reaches Contact with its heading visible and no horizontal document overflow. | PASS: expanded true; `/contact/`; `How to Reach The Hill`; no overflow. | PASS: same observations. | BLOCKED by runtime-loading failure. |
| T4: Retrieve relevant work by search. Open search with keyboard, wait until input owns focus, type `mermaid`, ArrowDown; inspect selected destination. Escape returns to opener. On `/search/`, wait for its autofocus, type `MurderBird`, Enter. | Selection has a coherent accessible focus/state relationship; excerpts contain clean text; Enter opens the intended story. | FAIL selection/excerpts; dedicated Enter PASS on retest. Initial fast typing timed out and is retained as a harness limitation. | FAIL selection/excerpts; Escape returned focus to opener. Dedicated Enter PASS on retest. Initial Tab search missed the already-autofocused input. | BLOCKED by runtime-loading failure. |
| T5: Begin a long story through its reading shortcut. On `/writings/murderbird/`, Tab to `Read the story`, Enter, Tab. | URL and focus move to `#the-maker`; keyboard continuation stays within the story. | PASS: section received focus; next focus was `I · The Maker`. | PASS: same observations. | BLOCKED by asset-loading failure. |

### Reproduced failures and retest interpretation

- **X01, confirmed:** Chromium and Firefox keep the hero heading in the DOM while its ancestor opacity is zero under no-JS, blocked-app, and missing-observer conditions. The Chromium no-JS screenshot was visually inspected and showed the background without hero heading, art, or buttons. A03 owns the correction; this review does not patch it.
- **X02, confirmed:** After ArrowDown in both Chromium and Firefox, focus stays on `.okh-search-input`; it has no `aria-activedescendant`. The selected result has only `data-active="true"`, with no selected state or result focus. This is an observed semantic gap, not a claim about a particular screen reader's speech.
- **X03, confirmed:** Both engines render related-resource snippets containing literal `</div` or truncated `</di` fragments. A04 owns parsed snippets and the selection model.
- **Search harness correction:** The first run typed before reliably waiting for overlay focus and tried to Tab to a dedicated input that already had autofocus. The retest waits for actual input focus and types with a 75 ms delay. It reproduces X02/X03 and confirms dedicated-search Enter reaches `/writings/murderbird/` in both engines. Initial failures remain in the evidence instead of being recast as site defects.
- **WebKit, confirmed environment limitation:** Requests for CSS, JS, manifest, and images were upgraded to `https://127.0.0.1:5220/`, where the plain HTTP preview cannot complete SSL. Console and request evidence report `SSL connect error`. No CSP bypass or policy edits were applied. All five WebKit task outcomes are BLOCKED, including the misleading unstyled T1 opacity result. Retest unchanged bytes on an HTTPS preview before interpreting WebKit behavior.

## Supporting checks

| Exact command | Result and limit |
| --- | --- |
| `py -3 scripts/validate-site.py` | PASS: 56 HTML pages; 32 existing warnings; MTB/banner checks pass; 35 reviewed voice warnings do not exceed baseline. |
| `py -3 scripts/build-site.py --check` | PASS: 36 generated English pages current. |
| `py -3 scripts/build-search-index.py --check` | PASS: 160 entries current. Freshness does not imply clean snippets. |
| `py -3 scripts/cache-bust.py --check` | PASS: scanned 146 HTML files; zero substitutions. |
| `py -3 .agents/skills/okhp3-site-release-validation/scripts/inventory-routes.py --root . --sitemap sitemap.xml` | PASS: 31 sitemap routes. This is indexing scope, not every shipped route. |
| `node scripts/accessibility-qa.mjs --base-url=http://127.0.0.1:5220` | PASS: four representative keyboard/focus/reduced-motion samples and 31 route checks. |
| `node scripts/screen-reader-tree-audit.mjs --base-url=http://127.0.0.1:5220` | PASS: six Chromium accessibility-tree samples. The script's historical Linux header does not describe this Windows host, and its claim about exactly what is announced is not accepted as speech evidence. |
| `py -3 -X utf8 assets/scripts/check-contrast.py` | PASS: declared dark/light token pairs. Does not certify every rendered combination. The stale `scripts/check-accent-contrast.py` path was absent; the actual command without UTF-8 initially failed on console encoding. |
| `git diff --check` | PASS before report commit. |

Evidence: [initial task observations](../audit/a20-baseline-tasks-2026-09-07.json) and [focused search retest and WebKit diagnostics](../audit/a20-search-retest-2026-09-07.json). These are generated observations, not blanket pass/fail automation. External Analytics requests aborted during Chromium navigation; their query parameters are omitted from retained evidence. External uptime was not assessed. Disposable probes and no-JS screenshots remain in ignored `output/a20-*` in this checkout; the five recipes above and committed JSON retain the durable reproduction record.

## Concrete remaining acceptance evidence

1. A21 must provide a frozen integrated SHA and exact candidate artifact with its all-file manifest/digests. Recheck identity and all five tasks on that candidate, including A03 controller-failure recovery and A04 loading/error/query/category/Back/Tab/selection bounds. This baseline report does not accept later commits by inference.
2. Run WebKit on an HTTPS preview serving unchanged candidate bytes. Record full asset loading and keyboard behavior; retain the local HTTP failures as environment evidence.
3. Obtain actual Safari plus VoiceOver on a named macOS/iOS device, and NVDA plus Firefox when available. Record tester, date, browser/AT/OS versions, five task outcomes, spoken selection/loading/error announcements, focus return, failures, and retests. No accessible native-app control or audio-backed AT session was available here; no claim is made that installed software was exhaustively inventoried.
4. Record physical-phone touch/screen-reader behavior, browser zoom and text enlargement, short-height layout, light/dark rendered focus and contrast, long-form orientation, and third-party embeds. A 390-pixel viewport is not a physical-phone test.
5. A21 must independently verify final install instructions/full pinned Skillz package, concept labels, cross-surface status consistency, combined route coverage, release manifest, CI, staging, and live deployment. These candidate-dependent acceptance items were not performed against a nonexistent integrated package.

No WCAG conformance, human usability acceptance, CI success, staging acceptance, or live deployment acceptance is asserted. A21 confirmed that no integrated candidate was available during this review. Keep A20 open for the named-candidate retest and actual assistive-technology evidence.
