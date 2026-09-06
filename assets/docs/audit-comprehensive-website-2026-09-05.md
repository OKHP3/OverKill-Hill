# OverKill Hill P³ website: comprehensive assessment

Assessment date: September 5, 2026, America/Chicago. Live evidence was collected September 6 UTC. Decision: how to advance the public website as it stands, including its unfinished work, without losing its voice or useful engineering controls.

## Overall judgment

**Keep the static architecture. Repair the gap between the site's engineering discipline and the reliability, clarity, and proof visitors actually receive.**

This is a substantial portfolio and public working archive with a recognizable identity. Its best qualities are the source-first publishing model, detailed original writing, deliberate prototype boundaries on several project pages, and a release pipeline considerably more capable than a simple file upload. These are assets to improve.

The principal weakness is inconsistent assurance. Automated checks can pass while the advertised skip link does not move keyboard focus, desktop content disappears without JavaScript, and an operator-facing release verifier accepts changed JavaScript. Some project pages carefully distinguish concepts from services; their cards then lose that distinction. A fresh review date appears beside older claims that still contradict one another. The result is a site whose stated precision is stronger than several of its visitor and maintenance contracts.

My recommendation is a sequence of targeted repairs, then a measured editorial and visual refinement. A migration to React, Next.js, a CMS, or an application backend has no demonstrated benefit for the problems found here. Those changes would introduce additional work without fixing these particular failures by themselves.

This packet contains **36 workstream findings, consolidated into 20 execution packages**, plus two additional parent findings on asset performance and Mac tooling portability. Counts are navigation aids, not risk scores; overlapping anchor, status, and documentation findings should be repaired together.

## Read this packet

| Artifact | Purpose |
| --- | --- |
| This assessment | Integrated judgment, coverage, priorities, architecture, measurement, and evidence limits |
| [Execution plan](website-advancement-plan-2026-09-05.md) | Ordered packages, ownership, dependency boundaries, acceptance tests, and ready-to-use delegation briefs |
| [UI, UX, and accessibility](audit-ui-ux-2026-09-05.md) | 12 findings with browser measurements, source locations, and visual direction |
| [Content, localization, and Git estate](audit-content-estate-2026-09-05.md) | 12 findings, disposition of all 36 English pages, project maturity, branches, notes, and translation policy |
| [Security and delivery](audit-security-delivery-2026-09-05.md) | 12 findings covering production headers, artifacts, CI, Replit, dependencies, analytics, and operating controls |
| [Validation record](audit-validation-record-2026-09-05.md) | Exact commands, initial failures, corrective reruns, coverage, and test limitations |
| [Machine evidence](../audit/comprehensive-2026-09-05/) | Logs, JSON, source inventory, API observations, network samples, and review record |
| [Visual evidence](../audit/screenshots/comprehensive-2026-09-05/) | Live captures of mobile, desktop, navigation, and JavaScript failure states |

These are local assessment artifacts. No site source, Git branch, account setting, or deployed page was changed. No commits, PRs, external messages, or Replit/Copilot dispatches were created.

## What was actually assessed

| Boundary | Evidence and coverage |
| --- | --- |
| Owner checkout | Initially clean `main`, `897df5d33202bd65924f9f3a35c84e0068cbee02`; cached origin was at the same older SHA |
| Current GitHub release | Separate frozen snapshot at `40e18ee7916f4a54196cc407d60999ba1d786d11`, one commit ahead; original checkout preserved |
| Live parity | All **56 released HTML files** returned HTTP 200 and matched the frozen source after CRLF-to-LF normalization; includes the directly addressed 404 document, not an unknown-route 404 test |
| Indexing inventory | **31 sitemap routes, 25 published noindex HTML files**; public availability and indexing are different boundaries |
| English content | **36 source page bodies**, including **14 project details: 11 indexable and 3 noindex concepts**; full disposition table in the content report |
| Locales | 20 localized routes: four each for fr, de, es, en-GB, es-MX; only French is approved for indexing; the other four locale sets are publicly addressable noindex drafts |
| Source and build | Renderer, shared shell, scripts, CSS, JS, CSP generator, search indexes, release builder, tests, workflows, publication docs, and active/historical notes |
| Browser regression | 31 routes at 320px; 31 routes across 10 responsive widths in deterministic mode with external fonts/tagging blocked; 31 route-wide ARIA checks plus four focused accessibility pages; six accessibility-tree pages; 31 CSP routes with 22 Mermaid diagrams |
| Focused live journeys | Homepage, project discovery, contact, article anchors/TOC, search overlay/results, mobile navigation, JavaScript disabled, and reduced-motion behavior |
| Network diagnostics | Eight cold-cache initial-load samples, including three mobile homepage repetitions; desktop/phone viewport emulation on a Mac Chromium engine |
| Git estate | Live remote heads, 27 returned PR records, local branches, two worktrees, no stashes; no open PRs, one live remote branch |
| External basis | Current W3C/WAI, MDN, web.dev, Node, GitHub Actions, Cloudflare, Google, Agent Skills, Python, and Apache primary references |

The source validator discovers 60 HTML files, while the release contains 56. Its wider discovery includes authoring/pilot material; it is not an alternative public-route count. The release inventory, sitemap, browser inventory, and authoring inventory serve different purposes and should become more explicitly reconciled in the tooling.

The latest successful [Pages run 34007868479](https://github.com/OKHP3/OverKill-Hill/actions/runs/34007868479) and the public release manifest identify the same current SHA. Browser and HTTP evidence did not reveal content deployment drift. Older local CSP failures are recorded separately and must not be promoted into a current production defect.

## What is already good

- **Appropriate runtime:** generated HTML, a shared stylesheet, and ordinary browser JavaScript fit a portfolio, archive, and collection of external project entry points.
- **Reviewable authoring:** English fragments and common shell are generated; search and fingerprints have freshness gates. The first repair should happen in the authoritative source, not in rendered copies.
- **Deliberate release boundary:** Pages receives an allowlisted artifact rather than the entire repository. Sampled governance/source exclusions work on the canonical site.
- **Meaningful regression coverage:** the 310 responsive combinations passed in real Playwright mode. The route-wide CSP, overflow, link, and generated-content checks are useful evidence, even though they do not cover every state.
- **Security foundations:** HTTPS enforcement, SHA-pinned Actions, limited workflow permissions, page CSP, escaped search text, strict-default Mermaid, and separate embedded-app origins are worth retaining.
- **Distinctive content:** the manifesto, MurderBird story, long Diagram experiment, build journals, and candid failed-results material give this site its reason to exist. Do not flatten them into generic sales copy.
- **Existing visitor orientation:** “Use a tool,” “Inspect the work,” and “Discuss a project” already exist. Improve their placement and usefulness rather than adding a fourth competing orientation scheme.
- **Some excellent maturity boundaries:** Telling Forward, LifeTrkr, BPMN, and Skillz already distinguish stages or limits on their detail pages. Reuse that discipline everywhere.

## Priorities that change the experience

Priority is the order of useful work for this site, not a vulnerability severity label. P1 means next repair cycle; P2 means the following improvement cycle or a conditional architecture decision. No critical remote exploit or active compromise was demonstrated.

| Rank | Finding and consequence | Evidence | Recommended action |
| --- | --- | --- | --- |
| 1 | Desktop content disappears when JS fails or is disabled | UI-02; eight homepage reveal containers stay transparent | Visible HTML by default; enhancement-only animation; test disabled JS and blocked app.js |
| 2 | Skip and article links scroll but do not preserve keyboard/navigation state | UI-01/UI-06; next Tab returns to the logo, article hash stays empty | Restore native anchors or implement focus, hash, Back, and reload semantics completely |
| 3 | Short mobile navigation puts Contact/Legal beyond the usable panel | UI-03/UI-08; 718px panel in a 640px screen; 768px rule overlap | Bounded scrollable panel, coherent breakpoint, short-height and resize fixtures |
| 4 | A tool-install journey can produce an incomplete, undiscoverable package | C01; flat `.agents/skills/my-skill.md` example | Tested complete skill directory at a pinned revision, named client, and real smoke task |
| 5 | Release verification does not verify all released bytes | SD-03; harmless temporary JS alteration still passed | Per-file digests, sizes, inventory and SHA verification; negative tampering fixtures |
| 6 | Project status and readiness claims disagree across surfaces | C02-C06; completed/pending workbench claims, prototype cards, concept notices, broad success language | One status/proof model plus bounded editorial corrections |
| 7 | Search supports visual keyboard selection without exposing it accessibly | UI-05/UI-09/UI-10; no active-result announcement, dead advertised Enter action, markup fragments | One coherent accessible interaction contract and clean parsed excerpts |
| 8 | Reduced-motion preference does not stop the moving TOC | UI-04; transform continues changing | Prefer CSS sticky; otherwise stop JS animation and idle work under the preference |
| 9 | Delivery retries and instructions have avoidable failure modes | SD-05/SD-10; duplicate `github-pages` artifacts; retired PAT writer in active guide | Attempt-specific artifact names and a current PR-based runbook |
| 10 | Tooling/runtime support and portability are inconsistent | SD-06 and P-02 below | Supported Node LTS, normalized filesystem paths, explicit tested environments |
| 11 | Desired edge policy is not delivered; its proposed adapter is not ready | SD-01/SD-02 | Keep accepted Pages limits visible; prepare a host-specific, tested decision before migration |
| 12 | Desktop initial load includes an avoidable 2.5MB PNG | P-01 below | Responsive modern derivative with preserved original; realistic initial-load budgets |

The full workstream reports retain lower-priority issues and conditions. A 768px submenu anomaly, an outdated publication command, and an unverified external service do not all have the same severity or the same solution.

## Additional performance and maintainability findings

A subsequent controlled probe left JavaScript enabled and blocked only `app.js`. All eight desktop reveal containers remained transparent, while the otherwise identical control revealed them normally. This confirms a script-delivery failure mode, not merely a user preference scenario. See [blocked-script evidence](../audit/comprehensive-2026-09-05/disruptor-blocked-app-js.json). It does not establish how often real visitors encounter that failure.

### P-01: optimize the expensive image and measure the right budget

**Confirmed:** the existing source-weight gate passes the homepage at **4,623,516 of 5,767,168 bytes**, the Diagram article at 3,507,772 of 4,194,304, and MTB at 417,016 of 655,360. The configuration explicitly counts source assets and excludes external resources, iframe contents, dynamic requests, compression, caching, and timing. This is a regression guard, not a claim that a phone downloads those totals.

The measured live results support a targeted improvement:

| Sample | Encoded bytes observed | Main interpretation |
| --- | ---: | --- |
| Mobile homepage, 390×844, three runs | 388,018-388,062 | Existing responsive MurderBird WebP is doing useful work |
| Desktop homepage, 1440×900 | 3,019,812 | A 2,495,707-byte Etch-AI-Sketch PNG dominates this initial sample |
| Diagram article, phone | 694,774 | Initial load only; lazy diagrams/media and full-page scrolling add later work |
| MTB page, phone | 882,229 | Includes observed external embedded-app requests; source gate excludes these |
| Contact page, phone | 538,059 | The 216,948-byte illustration is a candidate for an appropriate smaller source |
| MurderBird story, phone | 424,062 | Initial viewport only; not the whole story's image cost |

The desktop PNG is `assets/img/etch-ai-sketch-using-a-council-to-design-at-velocity.png`, referenced by the homepage writing feature. Generate a WebP/AVIF derivative, retain the original as a source/download when needed, and use responsive sizing. Do not delete the owner's art or replace it with an unrelated stock image.

Google tagging was about **174KB** in these initial samples, making it the largest individual mobile homepage request. That informs the analytics value decision; it does not imply a legal violation or prove that analytics causes a user-visible delay.

Sampled mobile homepage LCP entries were 704, 220, and 984ms. These are diagnostics on this machine and network with no CPU/network throttle. They do not establish field Core Web Vitals. Adopt separate source, initial-transfer, and field-observation budgets. Initial proposed acceptance: reduce the desktop sample below 1MB while retaining the art's readability; keep phone first-load weight at or below the measured baseline unless a justified feature changes it. Validate at fixed conditions and then seek field evidence. The current field targets are LCP ≤2.5s, INP ≤200ms, and CLS ≤0.1 at the 75th percentile, assessed separately by device class. [Google Web Vitals](https://web.dev/articles/vitals), [LCP optimization](https://web.dev/articles/optimize-lcp).

### P-02: two portability suites fail under ordinary Mac temporary paths

**Confirmed:** `tests/test-audit-site-portability.py` fails one of three tests; `tests/test-performance-budget.py` errors in two of five. The failure compares resolved `/private/var/...` paths with unresolved `/var/...` roots. Production source-weight calculation succeeds when its normal root is already resolved.

Both suites pass unchanged when `TMPDIR` is explicitly set to a canonical `/private/tmp/...` path. This is diagnostic evidence of a path-normalization defect, not a reason to label the original runs as passing. Normalize roots at the entry boundary and exercise symlinked temporary roots in regression fixtures. It is a tooling portability issue, not a current site outage. See `scripts/audit-site.py:544` and `scripts/check-performance-budget.py:125`.

## Recommended product and architecture direction

### Public site: one clear entry, optional depth

Keep the motto and MurderBird. Make the first usable screen answer: what can I do here, what is ready, and what should I open next? Bring the existing three visitor paths closer to the hero; shorten the generic active-build notice; avoid promoting the same article in three equally prominent places. Treat this as a testable design proposal, not an asserted conversion improvement.

On the project shelf, put status and proof beside every project rather than in a separate two-record section. Use ordinary destination labels: open tool, inspect prototype, read case study, view concept. A prototype is legitimate work when labeled accurately.

Give each substantial project page a brief top summary with purpose, intended user, current maturity, one primary action, an example result, data/storage boundary, and known limits. Preserve complete architecture, history, tutorials, and source evidence below stable anchors. The ecosystem map should be optional context; visitors should not have to learn the naming system before doing something useful.

Keep long writing intact. Offer a short reading path, clear version/date context, and dependable navigation through the original material. Fiction should remain fiction; historical experiments should retain their original conditions and qualifications. A long page is not inherently a defect.

The contact page's visible email address is a sensible low-maintenance design. Put brief inquiry prompts beside it and keep support/donation content secondary. A contact form is optional and does not need to precede these improvements. Email clicks measure intent, not delivery or qualified leads.

### Authoring: extend existing registries

Use the existing page manifest, project-status data, and generator as the foundation. Proposed project metadata should distinguish:

- **Editorial availability:** published, draft, historical, retired.
- **Software maturity:** concept, prototype, pre-production, live, when applicable.
- **Delivery evidence:** checked URL, version/SHA if available, observation date, and specific verified capability.
- **Primary action and limits:** where the visitor goes, what that destination can currently do, and what remains unknown.

Do not replace these axes with a percentage-complete badge. An accessible article about an early prototype can be finished writing; a live app can still have experimental features. Render the same facts in cards, detail summaries, and search metadata. A missing fact should remain unknown until checked.

For locales, preserve the exact-pair translation workflow and separate editorial review from hash freshness. Released French needs complete search microcopy, including loading, error, empty, and announcement states. German, Spain Spanish, and the regional drafts must retain their release boundaries. Document why draft alternates are handled differently today and settle that deliberately.

### Delivery: one artifact, host-specific policies

Continue building a static release and deploying a validated SHA. Upgrade the manifest to cover every released file. Make retry behavior deterministic. Bring Replit publication, if retained, onto the same allowlisted artifact boundary; `publicDir='.'` is not equivalent to Pages packaging.

Retain direct GitHub Pages while evaluating whether controlled response headers justify an edge layer. Current missing hardening headers are an accepted hosting limitation, and the sampled site still has page CSP. The existing `_headers` file needs a selected-host adapter: its 4,358-character CSP line exceeds Cloudflare Pages' 2,000-character line limit, and overlapping header rules do not simply override each other there. A blind host switch would not complete the security work. [Cloudflare header behavior](https://developers.cloudflare.com/pages/configuration/headers/).

Keep the strict byte-identical shared-runtime contract already recorded in ADR-0001. One integrator should own changes to shared CSS/JS and generated outputs. Test all three brand markup contracts before any approved sibling propagation. If W07 replaces the ADR's current default moving-TOC behavior, record that decision in ADR-0001; preserving that default while honoring reduced motion is another valid repair. A future reusable library or workflow can be evaluated when maintenance cost warrants it; it is not required to fix this site.

### Operating discipline: current facts must outrank historical notes

Active runbooks currently conflict with safer current tooling. `replit.md` still describes timestamp-based sync and lock behavior superseded by `scripts/README.md`; `docs/publishing.md` points at a retired cross-repository PAT writer. Update current instructions with precise source/revision controls and links to historical records. Preserve the history, but prevent agents from treating it as an active recipe.

Do not clean branches based on old reports. This Mac clone has two worktrees, three local branches, no stashes, and one actual remote branch. The repair branch's unique commit IDs need patch-equivalence review because its PR was squash-merged. There is no evidence-backed need to merge every old ref or delete preservation refs.

Use an operational summary that separates content delivery, source validation, edge policy, and third-party availability. A green deployment with a `PARTIAL` edge report is not full policy enforcement. The observed CI report had **427 checks, 0 failures, 38 blocked, and 315 warnings**. Keep the details, but summarize repeated accepted limitations once per control for an operator.

## What successful advancement would look like

| Outcome | Acceptance evidence |
| --- | --- |
| Reliable reading | Essential content visible with JS disabled or blocked; anchors preserve focus/history; no lost content on short screens |
| Understandable project maturity | Every project card and detail summary agrees, with dated proof or an explicit unknown |
| Completed primary task | A visitor opens a real tool, installs one complete skill package, or finds a contact route using the displayed instructions |
| Accessible interaction | Keyboard and assistive-technology checks cover actual menu/search/anchor completion, not only attribute presence |
| Honest release assurance | Changed files fail manifest verification; retries deploy one unambiguous artifact; live SHA matches validated SHA |
| Measured performance | Known heavy asset reduced; initial transfer and controlled timing recorded; field metrics only claimed with field data |
| Maintainable multilingual content | Approved French interactions are complete; all draft and published locale states have an explicit owner and freshness gate |
| Useful evidence | Five representative visitor task sessions identify whether status and next steps are understood; failed tasks become backlog items |

Suggested visitor tasks: find a usable diagram tool; distinguish Telling Forward's prototype from a hosted service; install a real Skillz package; locate and share a specific Diagram section; prepare a project inquiry. Five sessions are a qualitative discovery exercise, not statistically representative proof. Do not invent traffic, conversion, revenue, or user-satisfaction baselines.

## Limits and judgment boundaries

This was a broad source and live-product assessment, not exhaustive security testing, formal WCAG certification, native-language certification, or scientific replication of archived experiments. The existing browser matrix is Chromium-based. Accessibility-tree inspection does not replace VoiceOver/Safari or NVDA with an actual browser. Rendered gradients, hover/focus states, zoom/text-spacing, forced colors, every downloaded document, and every external application's complete workflow were not exhaustively evaluated.

No account-side Analytics settings, mail delivery, registrar controls, authenticated Replit deployment, or external project internals were inspected. Current external app reachability is not proof of data persistence, privacy, or feature completeness. Source skills in this repo were sufficient for the assessment; the additional Windows paths were not mounted or requested, and sibling repositories were not silently turned into a fleet remediation task.

Current model branding and release timing were not used as evidence. The findings stand on source, tests, rendered behavior, and primary references.

The [final Equilibrium record](../audit/comprehensive-2026-09-05/equilibrium-review.json) records the evidence, outcome, safety/portability, and conditional falsification passes. Final decision: **approve-with-limits for use as a recommendation packet**. The reviewers share a model and prior workstream context; this is not external certification or an unseen benchmark. Agreed corrections to source paths, locale wording, test scope, and release dependencies were applied. Approval of this packet is separate from approval of implementation or publication.

**Recommended next action:** execute packages W01-W03 and W05 from the plan as small coordinated PRs: essential reading/focus, mobile navigation, complete release verification/retry behavior, and the concrete content trust corrections. Defer broad visual exploration until those failures are fixed.
