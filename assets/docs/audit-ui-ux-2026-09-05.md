# OverKill Hill UI, UX, and accessibility assessment

Assessment date: September 5, 2026, America/Chicago. Live browser measurements occurred September 6 UTC. This is a recommendation report; no site implementation was changed.

## Scope and evidence boundary

Reviewed the owner checkout at `897df5d3`, then compared the shared JavaScript, stylesheet, and homepage source with the frozen remote snapshot at `40e18ee7`. Those three files match byte-for-byte. Live observations below were made against `https://overkillhill.com/` and its article/search routes with headless Chromium; they are observations of the served site, not proof of a specific deployed commit.

Read `AGENTS.md`, `replit.md`, `web-design-guidelines`, and `okhp3-overkill-hill-brand`. The brand profile is version 1.1.0, status `seed`; its declared palette, Alfa Slab One / DM Sans / JetBrains Mono roles, and forge narrative inform the proposed direction. Reviewed shared interactions, navigation, language control, contact journey, homepage, long article, search, and Mermaid Theme Builder embed source. Parent assessment owns the existing test-suite results and broader content/infrastructure inventory.

JSON evidence is under `assets/audit/comprehensive-2026-09-05/`. Screenshots are retained under `assets/audit/screenshots/comprehensive-2026-09-05/`; original machine capture paths predate this placement.

Evidence files:

- `ui-focused-browser.json`: homepage desktop/mobile and JavaScript-disabled cases, skip link, search selection, reduced motion.
- `ui-focused-browser-followup.json`: settled mobile menus and article anchor behavior.
- `ui-journey-browser.json`: short-screen menu scrolling and dedicated search shortcuts.
- `ui-desktop-home-scrolled.png`: complete homepage after scrolling to activate reveal effects.
- `ui-nojs-desktop-home.png`: content hidden when JavaScript is disabled.
- `ui-nav-390-640-settled.png`: clipped mobile navigation.
- `ui-nav-390-844-settled.png`, `ui-nav-768-800-settled.png`, and other `ui-*.png` captures: supplementary visual evidence.

The initial full-page desktop screenshot contains offscreen sections still awaiting scroll reveal. That is an artifact of taking a full-page screenshot without scrolling; use the `-scrolled` capture for normal-page visual assessment. The initial mobile-nav measurement/capture precedes the 200 ms transition; use the explicitly settled follow-up instead.

This is not a WCAG conformance certification. It does not include VoiceOver/NVDA sessions, physical iOS/Android devices, reader interviews, or measured task-completion/conversion rates. Findings distinguish measured behavior, source-confirmed behavior, and editorial judgment. Lack of a reported violation does not establish accessibility.

## Judgment

The site has a recognizable identity and unusually strong public documentation for an independently maintained static portfolio. Its architecture remains suitable. A framework migration would not address the defects found here.

The best next investment is to make the existing experience dependable at its edges: working keyboard bypass, readable content if enhancements fail, scrollable compact navigation, accessible search selection, and motion that actually stops when requested. The next design pass should improve hierarchy and visitor orientation while retaining the MurderBird, industrial palette, heavy display headings, technical labels, and Jamie's voice.

## Findings and recommended work

### UI-01 - P1: the skip link does not bypass navigation

**Measured and source-confirmed.** `assets/js/app.js:395` intercepts every local hash link, prevents native navigation, and only scrolls. On the live homepage, pressing Tab then Enter leaves focus on the skip link; the following Tab reaches the logo. The URL hash stays empty. The bypass affordance is present but its intended keyboard behavior does not work.

Restore native hash navigation where possible. If custom handling remains, distinguish skip links, update the location, and transfer focus to a suitable main target with `tabindex="-1"` and `preventScroll` as appropriate. Test Enter, the next Tab, URL state, and Back. Existing `scripts/accessibility-qa.mjs:172` checks presence and first-Tab visibility, not activation success; extend that check.

This concerns the purpose of [WCAG 2.4.1 Bypass Blocks](https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html). A page-level conformance conclusion needs evaluation of all available bypass mechanisms; the concrete finding is that this advertised mechanism fails.

### UI-02 - P1: static content disappears when JavaScript is unavailable

**Measured and source-confirmed.** `assets/css/theme.css:1161` makes `.reveal-on-scroll` transparent by default; `assets/js/app.js:374` reveals it. At 1440×1000 with JavaScript disabled, all eight homepage reveal containers remain at opacity zero, including the hero and primary visitor paths. Mobile CSS happens to make them visible, so narrow-screen tests conceal this defect.

Render content visibly by default. Apply enhancement-only initial states after capability detection, or remove reveal effects from essential text. Ensure script blocking, script errors, and a failed app.js request leave the homepage, contact details, and articles readable. A `noscript` override alone would not cover a downloaded script that throws before initialization.

Acceptance: primary copy and CTAs remain visible at 1440px with JavaScript disabled and with app.js blocked. Visible default content is particularly justified for this static publishing architecture; this is not a blanket claim that WCAG requires all sites to work without JavaScript.

### UI-03 - P1: short mobile screens cannot see the bottom of the navigation panel

**Measured and source-confirmed.** `assets/css/theme.css:3397` positions the expanded navigation at y=60 with no height limit or internal scrolling. At 390×640, it measures 718.44px high, ending at y=778.44; Legal begins at y=716.55. Contact and related destinations are below the visible screen. The complete menu fits the tested 390×844 viewport, which explains why a conventional mobile screenshot can miss this.

Give the panel an available-viewport maximum block size and `overflow-y:auto`, account for safe areas, and retain a visible close control. Choose a clear disclosure model; avoid turning ordinary site navigation into an ARIA application menu. Consider collapsing project children under an explicit disclosure instead of expanding every section. Acceptance includes 320×568, 390×640, landscape, keyboard focus, touch scrolling, and text enlargement.

The [WAI disclosure-navigation example](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/) provides an appropriate reference for ordinary website links.

### UI-04 - P2: reduced-motion CSS does not stop JavaScript-driven movement

**Measured and source-confirmed.** `assets/js/app.js:500` starts an endless animation-frame loop on the long article. With `prefers-reduced-motion:reduce`, scrolling produced TOC transforms of 25.2, 153.34, 216.97, and 264.69px across four samples approximately 100ms apart. The CSS media query cannot suppress imperative transform updates. The hash-link handler also explicitly requests smooth scrolling.

Prefer CSS sticky positioning within the article layout. If the moving TOC remains, stop animation under reduced motion, update only when needed, and stop when the viewport becomes narrow. Existing resize logic does not cancel its loop. Extend `scripts/accessibility-qa.mjs:216`: checking computed CSS durations misses JavaScript movement. Measure transform stability after interaction in reduced-motion mode.

Reference: [WCAG 2.3.3 Animation from Interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html), a Level AAA criterion. Do not describe this finding as an automatic AA failure.

### UI-05 - P2: arrow-key search selection is visual only

**Measured and source-confirmed.** `assets/js/app.js:833` uses `data-active` to highlight a result. After ArrowDown, focus stays in the input; it has no active-descendant relationship, and the status only announces the result count. Enter navigates to the visually selected result. A screen-reader user cannot reliably identify the arrow-selected destination from that state.

Choose either a standard link list with actual focus movement, or a correctly implemented editable combobox pattern with stable option IDs, active-descendant state, and suitable popup roles. Do not add one ARIA attribute without reconciling the whole interaction. Preserve ordinary link activation and modifier-key behavior. Test query changes, first/last result, no results, loading failure, reopening, Tab, Escape, and focus return. Reference: [WAI combobox pattern](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/).

The overlay already has a label, a live status, Escape handling, focus trapping, and return focus. Those are strengths to preserve. The page beneath is not inert; confirm virtual-cursor isolation with real assistive technology before selecting a modal implementation.

### UI-06 - P2: local article navigation loses shareable location state

**Measured and source-confirmed.** Clicking the TOC link for `#what-mermaid-actually-is` scrolls the target to y=136.39, safely below the measured 124.05px header. However, the URL hash remains empty and focus stays on the TOC link. Sharing or reloading the current location does not retain the chosen section. The same handler causes UI-01.

Restore normal anchor semantics and test URL, Back, reload, and keyboard continuation. Keep the existing scroll-padding offset; this measurement does not support a claim that the tested heading is obscured by the header. Consolidate this repair with UI-01 rather than creating a competing anchor system.

### UI-07 - P2: mobile hero typography has no side gutters

**Measured and source-confirmed.** At 390px the homepage h1 starts at x=0 and occupies the full 390px width. Paragraphs and buttons also touch the viewport edge. `assets/css/theme.css:882` applies `padding:4rem 0 3rem` to the same element that receives `.container` padding at line 300.

Use block-axis padding for `.hero-inner` and preserve the container's inline gutters. Check the shared change against representative OKH hero variants and sibling brand scope fixtures. Preserve the dramatic heading and illustration; this is a layout defect, not a reason to replace the brand. Acceptance: usable inline padding at 320, 390, and 768px without horizontal overflow or clipped heading letters.

### UI-08 - P2: the navigation breakpoint has conflicting definitions

**Measured and source-confirmed.** Desktop CSS begins at `min-width:768px` (`theme.css:3284`) while mobile CSS and JavaScript include `max-width:768px` (`theme.css:3321`, `app.js:80`). At exactly 768×800 the open mobile menu measures 192.19px high and the Legal submenu link has a zero-size box. Desktop's more specific hidden-submenu rule applies inside the mobile navigation model.

Use one boundary and mutually exclusive rules. Test 767, 768, and 769px, including resize while open and keyboard access to child links. This is an inexpensive targeted regression fixture.

### UI-09 - P2: dedicated search instructions and semantics do not match its behavior

**Measured and source-confirmed; browser evidence in `ui-journey-browser.json`.** `site-src/pages/search/index.main.html:6` promises Enter to follow and says Escape will “bail out.” `assets/js/app.js:1081` initializes the dedicated search input, but only attaches an input listener; its Enter navigation handler is confined to the overlay. With 46 results for `mermaid`, Enter leaves the user on the same search URL. Escape clears the native search field and removes the query from the URL; describe that behavior explicitly rather than using ambiguous exit wording. The full-page results container declares `role="list"`, while line 1034 renders direct anchors rather than list items.

Either implement the advertised shortcuts consistently or rewrite the instruction to describe the dedicated page's actual behavior. Use semantic `ul/li` or valid list-item structure. Preserve URL query/category state and popstate handling, which are already implemented. Avoid forcing input focus on mobile unless the user initiated search and the viewport behavior is verified.

### UI-10 - P2: search excerpts expose broken markup and noisy metadata

**Measured.** Live `mermaid` results contain literal `</div` or `</di…` in snippets for Related Resources. Other snippets begin with route text and status metadata instead of a concise explanation. This is escaped text, not evidence of script execution, but it reduces trust in a site emphasizing precision.

Inspect `scripts/build-search-index.py:318` and its manual nested-tag walker. Extract clean text from parsed section nodes, exclude navigation/resource-only boilerplate where appropriate, and add fixtures for nested containers and closing-tag boundaries. Keep the generated JSON script-owned. Consider author-controlled short result summaries for page-level entries and a separate label for section results.

### UI-11 - P2: navigation and promotion compete with the first useful action

**Editorial judgment, not measured conversion loss.** On a 390×844 screen, the header and promotion occupy about 163px; the hero occupies the remainder and continues below it. The current homepage correctly adds “Start with the work” and “Selected work,” but both follow the large hero. “Read the manifesto” is the secondary hero CTA, while the practical project-conversation route appears later. The same featured article recurs in the global banner, selected work, and Fresh from the Forge.

Keep the three-part motto. Put one plain visitor benefit immediately beside it and shorten the active-build notice. Offer three clear paths near the top: use a tool, inspect evidence, discuss a problem. The existing Start with the work section supplies the content; integrate or elevate it rather than duplicating it. Reduce repeated promotion of the same article. Treat any expected improvement in conversion as a hypothesis to test with five representative visitors and simple task observations.

### UI-12 - P2: contact is reachable but provides little help composing a useful inquiry

**Source-confirmed plus editorial judgment.** `site-src/pages/contact/index.main.html` provides a direct mailto address and Central Time location. That is a legitimate low-maintenance contact model. Most subsequent content concerns creator support, not inquiry preparation.

Add three short prompts beside the address: the problem, current situation, and desired outcome/timeframe. An optional copy-email button can help visitors without a configured mail client, while retaining visible selectable text and the mailto link. Explain expected response timing only if Jamie supplies a commitment. Keep support/donation content as a clearly secondary section. A hosted contact form adds processing and privacy obligations; it is not necessary to solve the current usability gap.

## Visual direction worth preserving and refining

**Preserve:** MurderBird illustration, forge metaphor, warm industrial colors, slab display type, technical labels, owner's wit, public process notes, and visible distinction between shipped work and concepts. Current selected-work cards with source/live destinations are useful evidence-oriented design.

**Refine:** give paragraphs and controls room on mobile; use fewer repeated card grids; vary long-page rhythm with editorial rows, selected artifacts, and concise evidence links; keep implementation details beneath a clear visitor explanation. The homepage uses multiple stacked groups of similarly weighted cards, which weakens the distinction between first action, proof, philosophy, latest writing, concepts, and the wider ecosystem. This is a design judgment, not a standards violation.

Use the existing stylesheet and source renderer. Prefer a small shared set of patterns: visitor-path links, project cards with consistent status/proof/action, long-form evidence blocks, readable tables, and an accessible search result. Avoid generic enterprise copy and a cosmetic framework rewrite.

Language flags have accessible names and expanded-state attributes in current markup. A visible locale label such as EN or Français would improve discoverability without removing the existing explicit language names. Distinguish draft locale availability in the visitor flow; the broader content assessment determines which pages are approved translations.

Do not treat every small link as a WCAG target-size violation. [WCAG 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) includes spacing and inline-text exceptions. A 44px comfort target for principal touch controls is a proposed design standard, not the WCAG 2.2 AA minimum. Full target-spacing and contrast measurement belongs in a dedicated representative-state matrix.

## Execution packages

| Package | Suggested implementer | Scope | Acceptance |
|---|---|---|---|
| A. Essential browsing reliability | Codex or Copilot, isolated PR | UI-01, UI-02, UI-06; shared JS/CSS and focused QA | Skip activates and next Tab enters main; anchors preserve URL/Back; blocked JS leaves primary content visible |
| B. Compact layout and navigation | Codex or Copilot, separate PR | UI-03, UI-07, UI-08 | 320/390px short screens and 767/768/769px boundaries; touch/keyboard scroll; mobile gutters; sibling scope regression check |
| C. Search behavior and indexing | Codex or Copilot, separate PR | UI-05, UI-09, UI-10 | Accessible selected destination, valid results structure, truthful shortcuts, clean snippets, query/back/filter state and failure recovery |
| D. Motion and article navigation | Codex | UI-04 plus TOC implementation simplification | No imperative motion under reduced preference; no permanent idle loop; desktop-to-mobile resize works |
| E. Editorial and visual refinement | Replit design exploration followed by owner-reviewed implementation | UI-11/UI-12; homepage hierarchy, project proof, contact guidance | Prototype current copy/brand in separate preview; owner reviews wording; five visitor tasks; no prototype applied to production implicitly |
| F. Independent assistive-technology review | Human tester assisted by Codex | VoiceOver/Safari, NVDA/Firefox or Chromium, phone browser | Main journeys usable at zoom/text enlargement; menu/search/embeds understandable; report includes failures and retests |

Dependencies: A should precede visual refinement because a hidden-content or focus defect invalidates visitor testing. B and C can proceed independently in isolated changes, coordinated around shared files. D should reuse A's anchor decision. Publish only after the repository's complete release gate and a review of representative live routes.

## Reference policy

The [Vercel Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md) were retrieved for this review. They inform focus, motion, semantic controls, and image checks, but they are not a compliance standard. Their generic writing preferences do not override this repository's en-US standard or the owner's established voice. WAI sources linked at the relevant findings define the accessibility basis and its limits.
