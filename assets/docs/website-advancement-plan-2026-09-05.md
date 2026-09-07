# OverKill Hill website advancement and delegation plan

Prepared September 5, 2026, America/Chicago. Basis: [comprehensive assessment](audit-comprehensive-website-2026-09-05.md), current release `40e18ee7916f4a54196cc407d60999ba1d786d11`. All items are proposals; this assessment did not dispatch work to GitHub Copilot/Replit, change source, or publish.

## Delivery strategy

Keep the static site and its current authoring model. Start with visitor and artifact correctness, correct bounded content contradictions, then refine information architecture and visual hierarchy. Evaluate hosting and privacy changes as explicit decisions with concrete prototypes and rollback plans.

Use one release integrator. A Codex sub-agent or Copilot can implement a bounded package; Replit is useful for isolated visual comparison and its own preview configuration. The integrator owns source-of-truth decisions, final generation, cross-site shared-runtime compatibility, combined validation, and release evidence. Completion by a worker is not completion of a release.

Effort labels are planning estimates, not measured commitments: **S** roughly half a focused day; **M** one to two focused days; **L** three to five days or dependent on external review. Do not sum them into a promised calendar deadline. Access, owner decisions, translation review, test failures, and shared-file conflicts can change the estimate.

## Ordered backlog

| ID | Priority / effort | Package and scope | Preferred executor | Depends on | Done when |
| --- | --- | --- | --- | --- | --- |
| W01 | P1 / M | Essential content and native navigation: UI-01/UI-02/UI-06; shared CSS/JS and focused tests | Codex | Frozen current baseline | Desktop reads with JS disabled and app.js blocked; skip's next Tab enters main; article anchors update hash, Back and reload correctly |
| W02 | P1 / M | Short-screen navigation, gutters, breakpoint: UI-03/UI-07/UI-08 | Codex or Copilot | W01 anchor contract; serialized shared files | 320×568, 390×640, landscape and 767/768/769px work; panel scrolls internally; last link/close remain reachable; hero retains inline padding |
| W03 | P1 / M | Artifact digests and retry naming: SD-03/SD-05; builder, Pages workflow, tests | Copilot or Codex | Current release flow read | Any changed/replaced/added/removed release file fails verification; manifest SHA checked; rerun selects unique intended Pages artifact |
| W04 | P1 / M | Search interaction and text extraction: UI-05/UI-09/UI-10 | Codex | W01; shared-runtime integration slot | Selected result is exposed accessibly; full search shortcuts are implemented or described accurately; valid list structure; no raw closing tags; URL/back/error paths work |
| W05 | P1 / M | Concrete content corrections: C01/C02/C04/C05 and bounded C06 | Codex, owner editorial review | Source evidence for each changed claim | Real complete-package install works; no currently-complete/currently-pending contradiction; three concepts visibly labeled; license and outcome claims bounded |
| W06 | P1 / L | Extend existing project status/proof registry to all 14 details and intentional shelf entries: C03 | Codex design, Copilot implementation | Owner-approved statuses; W05 | Cards, detail summaries and search use same facts; unknowns stay explicit; consistency fixture catches divergence |
| W07 | P2 / S-M | Reduced-motion TOC and idle-work cleanup: UI-04 | Codex | W01 and shared-runtime integration slot | TOC remains stable under reduce preference, no permanent idle follow loop, resize safe, anchors still work |
| W08 | P2 / M | Responsive image derivatives and realistic budgets: P-01 | Copilot or Codex | Existing source-art inventory | Desktop feature PNG has an appropriate modern derivative; original retained; fixed-condition sample below proposed 1MB target; visual quality reviewed |
| W09 | P1 / S | Current runbooks and historical supersession: SD-10/C10 plus replit sync contradiction | Copilot | Read actual scripts/ADR and current practices | Every active command resolves; no retired PAT writer; explicit revision/lock controls; historical records clearly linked, preserved |
| W10 | P1 / M | Supported QA runtime and Mac portability: SD-06/P-02; dependency inventory | Copilot | W03 test baseline | Node24 or selected supported LTS passes clean install/full suite; both Mac tests pass with ordinary/symlinked temp roots; runtime/vendor inventory recorded |
| W11 | Conditional P1 / M | Preview and Replit publication boundary: SD-04/SD-08 | Codex; Replit only for its verified config | W03; explicit supported-host decision | Default workstation loopback; bounded report receiver; external preview serves approved artifact; Replit release inventory matches Pages or production route retired |
| W12 | Conditional P2 / L | Host-specific response-header adapter: SD-01/SD-02 | Codex proposal; owner infrastructure decision | W03/W11, chosen host | Cost/operations tradeoff documented; line limits/overlaps validated; staging real headers and embeds pass; rollback rehearsed before authorized deployment |
| W13 | Decision P2 / M | Analytics value, visitor choice, disclosure: SD-09 | Codex plus owner measurement decision | Defined necessary metrics | Accepted/rejected/withdrawn states and account settings documented; network/cookies match chosen policy; content remains functional; no invented legal conclusion |
| W14 | P2 / M-L | Released French search microcopy and locale operations: C08 | Exact en-US to fr-FR skill plus qualified reviewer | Final W04 strings and affected English copy | French loading/error/empty/selection announcements reviewed; 20 routes have documented review/freshness ownership; draft boundaries preserved |
| W15 | P2 / L | Homepage and shelf hierarchy refinement: UI-11/C07/C09 | Replit isolated design variants, Codex integration | W01/W02/W06/W08 | Existing visitor paths appear promptly; featured/latest distinction works; no duplicate status authority; selected variant passes task review and mobile QA |
| W16 | P2 / M | Long-form project/article orientation and contact guidance: C09/UI-12 | Codex or Replit preview | W01/W05/W06 | Short evidence route, example result, clear limits and next action; stable original anchors/text preserved; inquiry prompts added without fictional response commitment |
| W17 | P2 / M | Metadata and social previews: C12 | Copilot | W05/W06/W15 wording | Descriptions reflect maturity; per-page share cards readable; canonical/alternate/noindex tests pass; no unsupported structured-data claims |
| W18 | P2 / M | Operations summary and proportionate agent governance: SD-07/SD-11/SD-12 | Copilot implementation, owner settings review | W03/W09/W10 | Content, edge, external-health states visible separately; runtime advisory coverage documented; rapid pushes/reruns predictable; selected sensitive-path review rules work |
| W19 | P1 release evidence / L | Independent human/browser task validation | Human testers assisted by Codex | Selected scope of each release; broader study after W15-W17 | VoiceOver/Safari and NVDA/browser results; phone/zoom/text-spacing/forced-color findings; five task sessions; failures repaired/retested, no blanket certification |
| W20 | P1 release evidence / M | Integrate, publish authorized release, verify, retain rollback | Main integrator | Selected release packages and their acceptance evidence | Full combined gates, exact artifact digest/SHA, live routes and primary journeys, explicit policy limits, rollback record |

Conditional P1 means required before using the affected path. Replit publication changes are not grounds to call the current Pages deployment exposed. W12 need not block independent visitor repairs while direct Pages limitations remain explicitly accepted. W13 revisits an existing owner policy; it does not silently reinstate a previously rejected consent UI.

## Practical sequence

**Release A: correctness.** W01, W02, W03, W05 and W09. Prepare independent source investigations concurrently; serialize changes to shared runtime. Run W19's focused keyboard/phone checks and W20 for this release. This yields a usable, more truthful site without waiting for a redesign.

**Release B: retrieval and proof.** W04, W06, W07, W08, W10, then the relevant W14 translations. Complete the registry before reshaping the shelf, and correct search strings before translating them.

**Release C: clearer presentation.** W15, W16, W17 after selected preview and task observations. Retain the complete archive and owner-authored voice. Include W19's broader assistive-technology review.

**Operations track.** W11, W12, W13 and W18 can be designed in parallel with product work because they have explicit decisions and account boundaries. Host/account changes wait for a concrete reviewed proposal and existing authorization; source preparation and staging evidence proceed first.

A realistic planning hypothesis is several focused weeks spread across these releases, rather than one unreviewable transformation. If time is constrained, ship Release A and the search/install fixes first; retain all later work as an evidence-backed backlog.

## Concurrency and file ownership

| Surface | Rule |
| --- | --- |
| `assets/js/app.js`, `assets/css/theme.css`, `assets/js/mermaid-init.js` | One implementation owner/integration branch at a time; W01/W02/W04/W07 are coordinated changes, not concurrent blind edits |
| `site-src/pages/**` | Workers can own disjoint source fragments; project registry work and editorial corrections need an agreed schema before overlapping |
| `assets/partials/**`, `scripts/build-site.py`, `site-src/project-status.json` | One schema/shell owner; record consumers before changing fields |
| Generated HTML, search JSON, CSP output, cache fingerprints | Release integrator regenerates from reviewed sources; workers do not hand-merge generated conflicts |
| Release builder/workflows/tests | W03 owner; W10/W18 rebase after it; inspect current job logs before changing triggers |
| Shared sibling foundation copies | Follow ADR-0001 and current sync tool's explicit source/revision contract; smoke-test brand hooks before authorized propagation |
| Translation files/ledgers | Exact language-pair owner; source hash adoption is not linguistic approval |
| Historical notes, branch refs and old worktrees | Preserve during implementation; any cleanup gets a separate disposition with incorporation proof |

When one package completes, its worker returns the changed source paths, why each is needed, test commands/results, failed/not-run checks, screenshot/evidence links, and remaining risks. Do not grade completion from a confident summary alone.

## Ready-to-use delegation briefs

These are prepared prompts, not sent messages. Substitute the task's actual starting SHA after refreshing remote state. Never paste account credentials or private working notes into them.

### Brief A: Codex, essential browsing reliability

> Assess and implement W01 against the current approved OverKill-Hill main revision in an isolated checkout. Read AGENTS.md, replit.md and the current shared-runtime ADR. Reproduce the documented desktop hidden-content and skip/hash defects before editing. Limit the first change to shared reveal/anchor behavior, any necessary target markup in authoritative sources, and focused regression tests. Preserve the existing brand, useful content, theme controls, and ordinary modified-link behavior. Essential content must remain visible with JavaScript disabled and when app.js is blocked. Activating the skip link must place the next keyboard step in main content. Article anchors must preserve URL, reload and Back semantics. Run the relevant generators and then the repository's complete gates. Return a coherent PR-ready diff and evidence. Do not push, merge, change account settings, propagate sibling copies, or publish without the authorization attached to the implementation task.

### Brief B: GitHub Copilot, release correctness

> Implement W03 in an isolated branch from the approved release SHA. Inspect scripts/build-release.py, tests/test-release-package.py and .github/workflows/pages.yml. The current custom verifier hashes only two generated files; a copied JS mutation can pass. Add a deterministic SHA-256 and size manifest for every released file except the self-referential manifest, plus exact inventory and source-SHA verification. Preserve the publication allowlist. Add negative fixtures for HTML, CSS, JS, locale JSON, vendor content, additions/removals and wrong SHA. Inspect the duplicate github-pages artifact failure from run 34007584411; make upload and deploy use the same attempt-specific artifact name. Preserve the validated-artifact dependency, permissions, pinned Actions and serialized deployment. Return test evidence and a reviewable PR. No new service, credentials or broad workflow rewrite.

### Brief C: Codex, content trust and usable installation

> Implement W05 in authoritative English source fragments. Use audit-content-estate-2026-09-05.md findings C01-C06 as hypotheses to verify, not permission to invent evidence. Replace the Skillz flat-file example with a real full-directory install at a pinned public revision and a named client; test it in a fresh disposable project and check every relative resource. Reconcile Mac journal current/pending statements from actual dated records while preserving the journal. Give the three noindex concept pages a visible static notice. Correct the Found-Ry FAQ's distinction between optional credit and required license/notice retention. Bound automatic-success claims to their evidence. Preserve owner humor, short standalone lines, manifesto text and fictional writing. Generate English HTML/search/CSP as required, detect affected locales, and stop short of claiming translations reviewed without exact-pair review. Return a concise editorial diff and task evidence.

### Brief D: Codex or Copilot, accessible search

> Implement W04 after the agreed W01 runtime change. Reproduce visual-only ArrowDown selection, the dedicated search Enter mismatch, invalid result-list structure and literal closing tags in excerpts. Choose one complete interaction model: ordinary focused links, or the WAI combobox pattern with correct roles/state. Do not apply a single ARIA attribute as a cosmetic fix. Preserve URL query/category/back behavior and useful announcements. Use parsed section text in the index generator, with nested markup fixtures. Test loading, empty, failed index request, zero results, query change, first/last selection, Enter, Tab, Escape and focus return. Export strings so the subsequent French work can localize the whole interaction. Return source changes, generated artifacts and browser evidence in one coherent PR-ready package.

### Brief E: Replit, visual exploration

> Prepare two isolated design proposals for W15/W16 using the existing OverKill Hill static sources, theme tokens, typography and MurderBird art. Do not apply either to the public artifact. Preserve the motto, owner voice, full writing and existing URLs. Build on the existing Use a tool / Inspect the work / Discuss a project paths. One variant should emphasize a compact evidence-first project shelf; the other should emphasize an editorial homepage with a small selected-work set. Each must show consistent approved maturity labels, one primary action per project, a clear featured-versus-latest distinction, useful mobile gutters and brief inquiry prompts. Show homepage, project shelf, one long project page, contact, phone and desktop. Use canonical theme.css for an accepted implementation; do not create a competing production stylesheet or framework. Return rendered previews, source-diff scope, task-review questions and unresolved decisions. A canvas frame or saved prompt is not proof that a preview rendered successfully.

### Brief F: Codex, edge-host decision packet

> Prepare W12 as a concrete read-only decision packet. Start from current direct GitHub Pages and its recorded PARTIAL security-header posture. Compare retaining accepted limitations, adding a controlled edge in front of Pages, and a static host with supported response-header configuration. Use current official provider capabilities/pricing and the owner's available accounts only when authorized. Do not simply deploy the existing _headers file: verify the 2,000-character Cloudflare Pages line limit and overlapping header semantics against the generated policy. Inventory stable versus fingerprinted asset URLs. Produce a host-specific adapter, staging test plan, iframe/social-image/error-route compatibility matrix, DNS/TLS cutover plan, rollback path, and cost/maintenance tradeoff. Do not alter DNS, hosting, HSTS preload, credentials, or production settings as part of this packet.

### Brief G: Independent acceptance review

> Review the frozen integrated release candidate, not an individual worker's summary. Use the original assessment findings and new acceptance criteria. Re-run the failed visitor tasks first: disabled/blocked JS, skip then next Tab, short-height navigation, 767/768/769 resize, search active-result announcement, clean excerpts, reduced-motion TOC and complete skill installation. Run the existing full deterministic gates and test actual Safari/assistive technology where available; mark unavailable checks NOT RUN. Verify all-file artifact digests and the candidate SHA. Distinguish source, CI, staging, live and third-party observations. Report approve-with-limits, defer-for-evidence or reject with reproducible reasons. Do not rewrite the candidate while judging it or publish merely because tests pass.

W19 repeats for each release: focused regression and keyboard/phone checks accompany Release A, while the broader assistive-technology and visitor study accompanies the presentation release. A focused pass does not mark the entire W19 program complete. W07 may preserve the existing default moving TOC while honoring reduced motion; replacing that default with CSS sticky also requires an explicit ADR-0001 amendment and sibling compatibility review.

## Acceptance matrix for the release integrator

| Layer | Minimum evidence |
| --- | --- |
| Source | Clean intended diff; correct source fragment/registry ownership; no unrelated refactor; no sensitive private locators |
| Generation | build-site, search-index, CSP and cache freshness; affected locale detection and release policy |
| Structure | Site validator, internal links/sitemap, project status, regional boundaries, release-package fixtures |
| Interaction | Mouse/touch/keyboard menu, skip/anchors, search, theme, reduced motion, blocked JS, embed fallback |
| Layout | Existing ten-width inventory plus short heights, exact breakpoints, landscape and enlarged text |
| Accessibility | Existing ARIA/tree checks plus actual task continuation and named assistive-tech results; no conformance claim from lint alone |
| Performance | Source budget, controlled initial transfer, selected slow-network/CPU runs; field evidence separately |
| Delivery | One verified artifact, full digest inventory, expected SHA, retry proof, no root publication escape |
| Post-deploy | All expected routes, representative bytes and tasks, actual response policies, explicit third-party limitations |
| Rollback | Retained last-good artifact/SHA, documented trigger and tested reversal procedure |

## Decisions that require the owner's judgment

The work can begin with correctness packages without resolving every strategic preference. Before dependent implementation, settle: which project statuses are accurate where evidence is missing; whether a visual variant expresses the intended voice; whether and how analytics should continue; whether full response-header control justifies a hosting change; whether Replit remains a publication route; and who can review sensitive delivery/runtime changes in a single-owner agent workflow.

No performance gain, conversion uplift, universal installation compatibility, production-readiness, translation quality, or release security should be claimed until the corresponding evidence exists.
