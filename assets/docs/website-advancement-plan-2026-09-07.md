# OverKill Hill website advancement plan

September 7, 2026 UTC. This is the active assessment-derived plan for the OverKill-Hill clone and https://overkillhill.com/. It supersedes the September 5 plan as the starting queue, while preserving that report and its evidence. It does not declare all earlier work complete or commit the owner to every proposed enhancement.

Read the [Architect assessment](audit-comprehensive-website-2026-09-07.md), [visitor/content findings](audit-experience-content-2026-09-07.md), [engineering reconciliation](audit-engineering-2026-09-07.md), [validation record](audit-validation-2026-09-07.md), and [delivery/security report](audit-delivery-security-2026-09-07.md).

## Architectural direction

Retain authoritative English source fragments, deterministic generation, static HTML delivery, one shared stylesheet, vanilla browser interactions and the allowlisted GitHub Pages release. Preserve public URLs, the original manifesto, owner voice, deliberate prototype boundaries and accepted MurderBird artwork.

Invest in four outcomes: visitors can reach usable work; claims match the evidence; a release verifies every intended file; maintainers can tell what remains open. A framework migration, CMS, account system, service worker, chatbot or mandatory contact form has no demonstrated need in this assessment.

The preferred visitor path is: identify the problem you solve, choose a tool or inspect evidence, understand its current limits, then try it or contact you. Existing content can support that path without turning the portfolio into generic agency copy.

## Roles and working contract

The user requested Architect → Project Manager → Worker delegation. This assessment exercised that structure with one engineering PM and two Workers, while the Architect handled live experience, content and synthesis.

| Role | Responsibility | Completion evidence |
| --- | --- | --- |
| Project Architect | Priorities, scope, evidence adjudication, cross-surface integration and owner decisions | Current plan and accepted work packages; unresolved claims remain explicit |
| Engineering PM | Release/QA/operations packages; inspect Worker code and test results | Reproductions, independent review, exact changed paths and acceptance disposition |
| Experience/content PM | Proposed next role for retrieval, project truth, phone presentation and locales | Coherent visitor tasks and reviewed copy; one owner for shared runtime changes |
| Workers | Bounded changes with disjoint file ownership | Before/after evidence, tests, limitations and reviewable diff |
| Release integrator | Combined generation, validation, artifact and authorized publication | Exact candidate revision, digest inventory, CI and live readback |

Only the engineering PM and its two Workers have been launched in this assessment. The proposed experience PM is a future assignment, not an agent reported as already running. No messages were sent to GitHub Copilot, Replit or outside collaborators.

Code work starts from a named, reviewed baseline in an isolated branch/worktree. Preserve owner changes and recovery refs. One integrator owns generated HTML, search data, CSP output and cache fingerprints; workers change authoritative sources and return their generator requirements. Shared `app.js`/`theme.css` changes are serialized. Sibling propagation is a separate compatible-revision workflow, not a side effect of editing this clone.

## Work already delegated and completed locally

| Package | Outcome | Evidence and remaining boundary |
| --- | --- | --- |
| A01: release integrity | Implemented in `scripts/build-release.py` and `tests/test-release-package.py` | Schema 3 records SHA-256 and byte length for 370 payload files in the 371-file sample. Mutation formerly accepted is rejected. Nine release tests and nine live-edge unit regressions pass. The manifest itself is excluded from its own digest; it remains a trusted-workflow record, not an independent signature. |
| A02: active maintenance guidance | Implemented in `replit.md`, `docs/publishing.md`, `ROADMAP.md` | Replaced retired publication-helper advice, corrected immutable foundation-source selection and supported MTB flags, and distinguished historical SEO/backlog statements. No sync or publication ran. |

These are uncommitted local repairs. Production was observed at `ca38d5b9` with schema 2. No source/generated page, artwork, sibling repository, DNS or account setting was changed. The release-integrity change needs the normal integrated release process before it is a production capability.

## Prioritized execution queue

P1 means a concrete visitor-trust, task-completion or release/maintenance correction. P2 means important consistency, coverage or experience work. P3 means enhancement after evidence. These are work priorities, not vulnerability scores. S/M/L are relative effort bands for a bounded package, not delivery promises.

| ID | Priority / size | Worker scope and findings | Dependency | Acceptance |
| --- | --- | --- | --- | --- |
| A03 | P1 / M | Runtime: fail-open content visibility, X01 | Frozen shared-runtime owner | JS disabled, app.js blocked and initialization failure keep text, art and links visible; normal/reduced-motion tests pass; no sibling writes |
| A04 | P1 / M | Search interaction and parsed snippets, X02/X03 | A03 coordinated runtime ownership | Selected destination has accessible focus/state; nested markup produces clean text; loading/empty/error/query/category/Back/Enter/Escape regressions; current working list wrappers and Enter preserved |
| A05 | P1 / M | Skillz install journey, C01 | Real pinned public package selected | Complete directory including referenced resources, named-client path, clean-project install, no silent overwrite; structural verification separated from agent activation |
| A06 | P1 / M | Targeted content truth, C02/C04/C05/C06 | Dated public sources; owner judgment only for unsupported new claims | Workbench current/pending conflict removed without erasing history; three visible concept notices; license summary scoped; unproved success language qualified |
| A07 | P1 / M | Release artifact retry and freshness ordering, D02/V2 | A01 | Upload/deploy use matching attempt-specific artifact name; stale committed HTML/search rejected before regeneration; clean package passes; controlled authorized CI rerun evidence |
| A08 | P1 / M | Supported QA runtime, D03 | Existing dependencies unchanged | Supported Node LTS chosen from official release table; local/CI version contract explicit; clean install, relevant fixtures/browser suites pass; preview runtime assessed separately |
| A09 | P2 / M | Cross-platform review fixture, V1 | Preservation contract read | Default macOS temporary-root case and canonical-root case pass; add meaningful alias regression; prefer fixture normalization without altering archived builder bytes |
| A10 | P2 / M | All shipped-page coverage and explicit browser failures, V3/V4/V6 | A07/A08 | 56-route release inventory governs functional loops with named exceptions; sitemap remains indexing scope; missing browser fails explicitly; machine reports leave tracked source unchanged |
| A11 | P1 / L | Consistent project status registry, C03 | A06 source truth | All 14 detail pages inventoried; shelf exceptions named; separate editorial availability/software maturity/delivery evidence; same record drives cards/details/search where applicable; unknown proof stays unknown |
| A12 | P2 / S-M | Featured/latest and descriptions, X05/C08 | A06/A11 | Chronological claim agrees with metadata or is relabeled Featured; Vault and workbench previews match reality; no invented dates or unsupported schema claims |
| A13 | P2 / M | French interaction completion, X06 | A04 final strings; exact en-US → fr-FR skill | Search, selection/error/status/theme/language labels reviewed; fallback routes explained; linguistic review separate from hashes; regional noindex policy unchanged |
| A14 | P2 / M-L | Phone hierarchy, gutters and selected-work presentation, X04/X08 | A11/A12 | Two rendered proposals within current brand; owner-selected direction; consistent phone gutters, early practical choices, one primary action per card; task observations and full regression checks |
| A15 | P2 / M | Reader orientation/contact, X07/C07 | A11/A14 | Keep existing long-form jumps and original text; concise optional evidence route and inquiry prompts; stable anchors and keyboard history; no fictional service commitment |
| A16 | P2 / M | Measured asset/font/analytics economics | Actual network baseline | Fixed-condition cold/warm desktop/phone trials; optimize measured contributor; visual parity; retain source art; no claimed conversion/performance gain without before/after evidence |
| A17 | P2 / M | CI concurrency and status summaries, D07/D08 | A07/A08 | PR, rapid-push, dispatch/rerun paths retain required checks; content/edge/external states reported separately; repeated accepted warnings summarized |
| A18 | Conditional P1 / M | Preview/Replit exposure, D05 | Required before externally exposing that path | Loopback default or explicit intended bind; bounded report input/storage; allowlisted serving/publication; no source/dotfile/symlink escape; no changes to canonical hosting implied |
| A19 | Decision / M-L | Response-header host strategy, D06 | Owner chooses whether full edge control is needed | Compare accepted Pages limits with concrete edge/host adapter, cost/ops, staging headers, embeds and rollback; do not deploy raw oversized `_headers` |
| A20 | P2 / M | Independent task/accessibility acceptance | Candidate package | Real Safari/VoiceOver and, when available, NVDA/Firefox/phone sessions; five defined tasks; failures retained and retested; no conformance claim from automation alone |
| A21 | P1 release gate / M | Integrate and publish authorized candidate | Selected packages complete | Correct source ownership; all required combined checks; exact SHA/digests/artifact; authorized PR/merge/deploy; live bytes and tasks; rollback reference |

Any new dependency, large redesign or account/security policy change requires its own concrete justified scope. Current repository rules prohibit unsolicited dependencies. A future automated accessibility engine is therefore a proposal to evaluate, not an unapproved install instruction.

## Recommended sequence

**First release: reliability and trust.** Finish A03-A08, alongside A09 if its narrow fixture correction is ready. A01/A02 are already prepared locally. Add focused A20 acceptance and A21 integration. This release should make a reader's experience survive script failure, make retrieval usable, make installation real and make release checks honest.

**Second release: coherent project evidence.** A10-A13, plus A11 status work as soon as content truth is ready. A11 is high priority but has more editorial dependencies than the small initial corrections. Do not delay an independently useful reliability repair while waiting for every project owner fact.

**Third release: presentation.** A14-A16, followed by the broader A20 task review. Evaluate one homepage, one shelf, one long project page, one writing and Contact as a coherent journey. Keep two visual variants isolated until a direction is selected. Preserve the latest accepted MurderBird composition and original writing.

**Operations track.** A17 can run independently on workflow files after release-contract decisions settle. A18 becomes a prerequisite whenever externally reachable preview or Replit publication is actually used. A19 is an infrastructure choice; the current accepted Pages limitations need not block visitor improvements.

Do not quote a whole-program completion date before the first packages establish throughput and review effort. The first release contains bounded corrections; presentation and external infrastructure have wider uncertainty. Report progress by acceptance criteria, not number of agents or commits.

## Concrete Worker briefs

### Runtime Worker: A03

> Reproduce the current 1280×800 blank homepage with JavaScript disabled and app.js blocked. Read the canonical shared-runtime ADR and relevant CSS/JS. Implement fail-open visibility in authoritative runtime sources, enabling optional reveal only when its controller is ready. Do not simply add noscript CSS, remove all motion, or touch sibling copies. Preserve existing skip/hash focus and reduced-motion behavior. Test normal load, blocked script, unavailable observer and controller failure; ensure essential links remain usable. Return a small diff, reproduction, targeted browser tests and generator/cache requirements. Do not publish.

### Search Worker: A04

> Reproduce live `mermaid` results containing a closing-tag fragment and ArrowDown changing only data-active. Choose a complete focused-link or combobox model. Preserve existing listitem wrappers, dedicated-search Enter, query/category history, accents and safe text escaping. Fix section extraction at the generator, not by hiding one string in the renderer. Test nested markup, entities, empty index, failed fetch, loading, no results, input changes, selection bounds, Enter, Tab, Escape and focus return. Prepare final English interaction strings for A13. Return the coherent source/generated diff with relevant regression evidence; no sibling synchronization or publication.

### Content Worker: A05/A06

> Use only current public source evidence. Replace the Skillz flat-placeholder example with one reproducible complete package install at a pinned revision and named client. Test in an empty project and verify supporting references plus no-overwrite behavior; state whether client activation itself was tested. For the Mac journal, preserve historical evidence and explicitly distinguish old pending work from dated completions. Add visible concept notices to the three identified draft project pages. Correct Found-Ry's unqualified attribution sentence without changing the repository license or rights in exported artifacts. Keep protected manifesto/fiction untouched. Do not invent project status, benchmark success or customer claims. Run generation/freshness and affected-locale detection; translation review is separate.

### Release/QA Worker: A07-A10

> Begin from the reviewed A01 integrity repair. Keep the trusted-artifact and publication allowlist boundaries. Make artifact names agree across upload/deploy for retries. Prove that stale committed outputs fail before regeneration. Select a currently supported Node LTS using official documentation, preserve installed dependency scope, and test clean setup. Resolve the macOS alias fixture without altering hash-preserved archive material unless specifically necessary and authorized. Use the shipped release inventory for runtime checks and indexable inventory for sitemap checks. Missing browser execution must be an explicit failure or blocked result, never a passing static fallback. Return exact test evidence; CI rerun acceptance remains unverified until an authorized run occurs.

### Presentation Worker: A14/A15

> Build two local rendered alternatives using existing static templates, typography, Forge palette and accepted art. Make practical visitor choices easier to find on a phone, restore consistent gutters, and show a small selected-work set with evidence and maturity. Preserve the full archive, URLs, motto, punchy owner writing and currently working TOC behavior. Show homepage, shelf, one detail page and Contact at phone and desktop sizes. Mark new copy as proposed. Do not apply a live Replit design, migrate frameworks or overwrite the accepted artwork. Return rendered evidence, precise source scope and task questions for selection.

### Independent acceptance Worker: A20/A21

> Review a frozen integrated candidate against the original reproduced failures, not an implementer's summary. Recheck no-JS/blocked-script visibility, skip continuation, compact navigation, accessible search selection and clean excerpts, pinned full-package install, concept labels and status consistency. Execute the declared local checks and verify the exact all-file manifest. Name browser/assistive-tech environments and every unavailable check. Separate source success, CI success, staging and live deployment. Return accept-with-limits or reject with reproducible reasons. Do not modify the candidate while reviewing it or publish solely because tests pass.

## Validation and release acceptance

| Layer | Required evidence |
| --- | --- |
| Scope | Exact baseline and intended diff; no unrelated owner or sibling changes |
| Content | Availability, claim evidence, dates, rights and limitations agree across surfaces |
| Generation | Source HTML, search, universe, CSP and fingerprints current; no hand-merged generated conflicts |
| Locale | Changed English strings identified; exact-pair review as required; draft/index boundaries retained |
| Behavior | Fail-open content, keyboard tasks, search, theme, TOC, embeds and recovery |
| Responsive/accessibility | Shipped-route accounting; phone/short-height/zoom/reduced-motion evidence; named manual limitations |
| Performance | Source inventory and observed transfer distinguished; fixed-condition before/after tests for optimization |
| Release | Exact SHA, complete inventory/digests, trusted artifact, retry behavior and no publication escape |
| Operations | Content, delivered headers and external health reported separately; actionable failures |
| Post-deploy | Authorized release, intended live manifest, representative bytes and journeys, retained rollback reference |

At assessment close, a default macOS historical-review fixture failure remains unresolved. Local runtime differs from CI. Actual assistive-technology sessions, field metrics, full external-tool functionality, owner Analytics settings and alternate Replit exposure remain unverified. None can be promoted to PASS by filling out this plan.

## Decisions to bring to the owner only when concrete

1. Select between rendered presentation variants after A14 supplies the actual pages.
2. Supply or approve project facts only where A11 cannot substantiate maturity from public evidence.
3. Decide analytics value and policy after A16 explains observed costs and useful measures. Do not reinstate an old rejected consent idea by inference.
4. Choose edge enforcement only after A19 provides staging behavior, maintenance cost and rollback.
5. Approve the actual publication candidate through the established PR/release workflow.

The next engineering action is A03/A04, with A05/A06 independent on disjoint content files. The Architect should retain this plan as the active queue and record each package's evidence-based disposition instead of creating another competing completion narrative.
