# OverKill Hill comprehensive website assessment

September 7, 2026 UTC. Project Architect assessment for the local `OKHP3/OverKill-Hill` clone and https://overkillhill.com/. Baseline: `ca38d5b9fc46746ea8b41e2ba32e39685c53f511` on `main`, initially clean.

## Architect's verdict

**Keep the architecture and identity. Correct the remaining reliability and truth-maintenance gaps before another broad design pass.** The site contains useful tools, substantial evidence and a distinctive voice. Its current weakness is the distance between what some visitor-facing claims imply and what the underlying records and checks actually establish.

The site is successfully deployed. Its structural, generated-source, internal-link and broad Chromium checks pass. That is meaningful progress. It is also possible to get those results while a desktop visitor sees an empty homepage after JavaScript fails, keyboard search selection is not exposed to assistive technology, or a new user follows an incomplete installation example. The existing gates need to include those tasks.

There is no evidence here that a React/Vite migration, CMS, backend, login, chatbot or PWA would solve the important problems. The next investment should be a usable tool/evidence/contact journey, consistent project status, complete release verification and clearer current operating instructions.

**Disposition: NEEDS INPUT for strategic presentation/hosting decisions; CLEAR for the bounded corrective packages already identified.** No critical exploit or active compromise was established. Full accessibility conformance, external product readiness and visitor conversion gains remain unverified.

## Assessment packet

| Artifact | Purpose |
| --- | --- |
| [Advancement plan](website-advancement-plan-2026-09-07.md) | Active priorities, sequence, ownership, exact Worker briefs and acceptance criteria |
| [Experience and content](audit-experience-content-2026-09-07.md) | Live desktop/phone/search/locale findings, route-by-route content disposition and source ledger |
| [Engineering reconciliation](audit-engineering-2026-09-07.md) | Project Manager synthesis and individual W01-W20 status reconciliation |
| [Validation record](audit-validation-2026-09-07.md) | Exact checks, environment, route coverage, failures and retained log locations |
| [Delivery and security](audit-delivery-security-2026-09-07.md) | Current GitHub/Pages state, live policy evidence and scoped repairs |
| [Content inventory](../audit/assessment-2026-09-07/content-inventory.json) | Current hashes, headings, links, volumes and comparison with prior source |

The September 5 audit was substantive. Thirty-two of 36 current main-body source files remain identical to its source snapshot; the changed bodies are homepage, MTB, Universe and MurderBird. Earlier reports were used as hypotheses and compared with current source, checks and browser behavior. A broad September 6 closeout is not proof that every acceptance condition in the separate September 5 advancement plan was delivered.

## What exists today

| Surface | Confirmed state and implication |
| --- | --- |
| Authoring | 36 English main-body sources with registry/shell generation; 14 project detail routes. Generated HTML is current. |
| Published inventory | 56 HTML pages in the allowlisted release, including 20 locale pages. Sitemap contains 31 indexable routes. These counts describe different boundaries. |
| Retrieval | Generated index has 160 entries, including section links. Search freshness passes; some excerpt/selection behavior still needs correction. |
| Runtime | Static HTML, canonical shared CSS, vanilla JS and selected Mermaid rendering/embeds. The Python preview server is not the production application server. |
| Deployment | Protected `main`, workflow-based Pages, canonical domain and HTTPS enabled. [Pages run 34084298158](https://github.com/OKHP3/OverKill-Hill/actions/runs/34084298158) succeeded at baseline. |
| Source history | One local worktree, local main, no stashes and one observed remote branch; no open PRs. Four archive refs remain. Older other-machine worktree/stash descriptions are historical, not current cleanup targets. |
| Identity | Forge palette/type, MurderBird, original manifesto, protocol-first positioning and deliberate fiction/research distinctions. Preserve these. |
| Privacy boundary | No first-party account/checkout application; email, analytics, fonts and embedded/linked tools introduce their own boundaries. Account settings were not audited. |

The release allowlist excludes sampled source and governance routes on the live domain. Public repository availability is separate from website publication. No inference that GitHub Pages exposes the checkout root should be made from a local preview server's configuration.

## Highest-value corrections

| Priority | Finding | Why it matters | Disposition |
| --- | --- | --- | --- |
| P1 | Essential homepage visibility depends on JavaScript | A static site should retain readable content if an enhancement fails. Live desktop failure reproduced. | A03, next runtime Worker |
| P1 | Search selection is visual-only; snippets contain HTML fragments | Retrieval reaches useful work, but keyboard users lack equivalent selected-result information and excerpts look broken. | A04; current Enter/list-wrapper fixes retained |
| P1 | Skillz install example uses an incomplete flat package shape | The flagship discovery-to-install journey can fail at its central task. | A05; real pinned complete-package example |
| P1 | Project summaries lose maturity limits; journal contains contradictory current/pending work | Visitors should distinguish prototype, case study and usable tool without comparing several pages. | A06/A11; source-backed claims and registry |
| P1 | Baseline release manifest hashes only two generated files | An altered copied JS file passed the custom verifier. This was a validation gap, not demonstrated compromise. | A01 repaired locally, not deployed |
| P1 | Retry naming, obsolete QA runtime and retired publication guidance | Maintenance should be reproducible across reruns and hosts. | Guidance repaired locally; A07/A08 remain |
| P2 | QA inventory/freshness semantics do not cover all claimed boundaries | Some checks run only indexable routes; generation precedes freshness checks; responsive runner can fall back to static mode. | A07/A10; keep publication and indexing separate |
| P2 | Phone hero has no gutter and practical choices arrive late | At 390×844, task section starts about 1581px down, selected work about 2351px down. | A14 rendered proposals after truth/reliability work |
| P2 | Featured/latest, French controls and some metadata disagree with destination | Presentation should not undermine otherwise careful content. | A12/A13, focused editorial work |
| Conditional | Preview exposure and full response-header control | Local/Replit publication and direct Pages have different controls and risks. | A18 before affected exposure; A19 owner infrastructure choice |

The detailed reports distinguish confirmed source/browser behavior, inference, proposals and unknowns. Priorities above are delivery priorities, not CVSS scores.

## What is working and should remain intact

- Generated-source, sitemap, internal-link, CSP and locale boundaries have substantive checks. They should be extended with missing tasks rather than replaced by another stack.
- Skip-link focus and hash behavior work in the current live test. The next Tab enters main content. Dedicated-search Enter follows the first result. MurderBird chapter links move focus and update the URL.
- The Universe now derives from the search inventory, provides an HTML outline and distinguishes a published page from a finished project. This is stronger than hand-maintained lifecycle claims in a diagram.
- Current TOC testing accounts for 56 shipped pages and all 14 matching menus, including legacy media-query behavior. Preserve the chosen follow behavior and accessibility adjustments.
- Telling Forward's service boundary, LifeTrkr's pre-production label, BPMN's experimental/plugin limits and Skillz's maturity-versus-evidence distinction are useful models for the project shelf.
- The newer writing and accepted art have deliberate provenance, preserved source boundaries, responsive derivatives and PNG fallback tests. Keep the archive and improve delivered assets only against real measurements.
- Historical experiment failures and protected personal writing have value. Polishing this site does not require turning its voice into generic corporate language or erasing evidence of prototypes.

## Validation results and their limits

| Evidence | Result | What it establishes |
| --- | --- | --- |
| Structural/generated/index/CSP/cache/locale/project gates | PASS after installing existing pinned Python QA requirements in an ignored venv | Current source and generated artifacts satisfy the named local checks; project-status coverage is only two records |
| Internal links | PASS: zero broken internal links among 2,369 inspected; 1,354 external links inventoried | Internal navigation validity; external-link count does not mean all external destinations were requested successfully |
| Responsive Chromium | PASS: 31 routes × 10 viewports, 310 rows | Existing layout assertions across indexable routes |
| Phone overflow | PASS: 31 routes at 320×800 | Existing horizontal-overflow assertions, not all usability/reflow criteria |
| Accessibility/CSP runtime | PASS within declared deterministic limits | Four focused interaction samples; basic route-wide ARIA; 21 rendered Mermaid diagrams; external services controlled separately |
| Search/embed/Mermaid/CSP regressions | PASS: 20 Node tests | Existing fixture behaviors, not all live user journeys |
| TOC / Universe | PASS | 14 menus across shipped inventory; five Universe diagrams, links, two widths and no-JS fallback |
| macOS historical-review boundary fixture | FAIL under default temporary-directory aliases | `/var` versus `/private/var` path portability defect; canonical temp-root diagnostic rerun passes; no claim of broken deployed routes |
| Live delivery | PARTIAL: 428 checks, 0 failures, 39 blocked, 315 warnings | First-party content checks pass within accepted direct-Pages limitations; missing header/cache policy is not enforced |
| Local integrity repair | PASS: 9 release tests; 9 live-edge unit regressions | Every payload file is now checked against recorded digest/size in a trusted manifest; mutation reproduction rejected |

Local environment was Python 3.14.5, Node 26 and Chromium 151; CI uses Python 3.11 and Node 20. This is not full environment parity. Node 20's support issue is documented against the current [official release table](https://nodejs.org/en/about/previous-releases) in the delivery report. Browser installation is an execution prerequisite, not an optional reason to call static lint a browser pass.

The live verifier's exit zero in accepted-Pages mode is not blanket security clearance. Source `_headers` does not establish actual response headers, and CSP meta cannot supply every response-level control. Keep content availability, header policy and external health as separate statuses.

## Performance and design investment

Do not describe the roughly 5.45 MB source-budget inventory as a visitor download. It includes candidate assets and ignores caching/compression/external costs. A cache-disabled live desktop observation measured 433,582 site/third-party encoded bytes, including 192,076 first-party bytes. The selected hero WebP was about 75 KB; Google tag JavaScript was about 174 KB. Browser-extension traffic was excluded.

This one existing-profile, unthrottled observation is not a Core Web Vitals assessment. Use fixed-condition cold/warm phone and desktop measurements before optimization, and field evidence before claiming real-user improvements. [Google's Web Vitals guidance](https://web.dev/articles/vitals) explains the experience measures that source totals cannot provide.

The proposed visual direction is restrained: consistent mobile spacing, practical choices near the beginning, one selected-work section with maturity and evidence, a distinct featured-writing choice, optional depth for the archive, and an obvious inquiry path. Preserve the art and personality. Test it with tasks such as finding a usable tool, identifying a prototype, installing one skill, reading the argument/evidence and preparing a useful inquiry. No conversion uplift has been measured.

## Delegation and changes completed

The Architect delegated to `assessment_pm`, which spawned validation and delivery/security Workers. Workers investigated independently, then received bounded corrective assignments. The PM reviewed the resulting code and evidence before reporting completion.

Changed tracked files:

- `scripts/build-release.py`: manifest schema 3 records and verifies SHA-256 plus byte length for every payload file, retaining the legacy artifact fields needed by live monitoring.
- `tests/test-release-package.py`: negative cases for same-size/re-sized mutations, multiple asset types, missing/extra entries, wrong SHA/schema and inventory changes.
- `replit.md`, `docs/publishing.md`, `ROADMAP.md`: correct active commands and source-selection rules; distinguish historical evidence and proposals.

New assessment reports and machine evidence are linked above. No public page source, generated page, accepted artwork or sibling file changed. No commit, push, PR, merge, deployment or account change was performed. Production remains the observed baseline until a later authorized release.

The repair checks accidental or transport alteration against a trusted manifest; it is not independent cryptographic signing against an attacker able to replace both manifest and payload. Retry naming and committed-freshness ordering are separate open tasks.

Final artifact review: the Architect independently reran all nine release-package tests and nine live-edge unit tests successfully. `git diff --check` passed, and all relative file references across the six assessment documents resolve. The PM independently checked the Architect assessment, experience/content report and advancement plan against its engineering evidence and found no concrete contradictions. These checks validate the assessment packet and bounded repairs; they do not clear the unresolved acceptance limits above.

## Scope not established

This assessment does not establish full Safari/Firefox/physical-device behavior, VoiceOver/NVDA task completion, all external application functionality, actual search-engine indexing/ranking, Analytics retention/advertising settings, field performance, native-language quality, private project facts or live Replit exposure. It does not turn displayed project claims into production proof. Those unknowns have concrete next checks in the advancement plan.

The referenced older Codex thread was not readable from this host; the pasted brief and repository's retained audit/closeout artifacts supplied the available context. That limitation did not prevent fresh source, GitHub, live delivery and browser verification.

Next action: execute the first reliability/trust release in the [advancement plan](website-advancement-plan-2026-09-07.md), keeping A01/A02's prepared changes separate from the remaining candidate work. Bring only concrete presentation, unsupported project facts, hosting strategy and publication decisions to the owner.
