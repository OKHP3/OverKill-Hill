# Engineering assessment and implementation reconciliation

Assessment date: September 7, 2026. Repository: OverKill-Hill. Baseline: `ca38d5b9`, local `main`. This report is the Project Manager synthesis under the Project Architect. Two Workers independently own [validation](audit-validation-2026-09-07.md) and [delivery/security](audit-delivery-security-2026-09-07.md). Root owns visual, content, and integrated product recommendations.

## Decision

Keep the generated static architecture. Its allowlisted release, shared shell, generated search, CSP, and browser gates are appropriate foundations. Improve the contracts those mechanisms actually prove. A green structural gate does not prove complete project evidence, working failure states, or every released byte's integrity.

The September 5 advancement plan remains a useful hypothesis list, not a completed implementation ledger. The September 6 closeout records earlier accepted repairs and creative work. Its broad statements cannot close every later W01-W20 acceptance condition. Current source proves both real progress and surviving gaps.

Only this repository is in scope. No sibling source, account settings, published content, historical refs, or secrets were changed during baseline assessment. Two bounded local repairs were subsequently delegated; their results are separated below.

## Current evidence and consequential claims

| Claim | Tier | Evidence | Consequence if false | Next check |
| --- | --- | --- | --- | --- |
| Site remains 36 authoritative English page bodies, including 14 project detail routes; sitemap has 31 URLs | Confirmed | This session parsed `site-src/pages.json` and `sitemap.xml` | Wrong denominator for coverage and status rollout | Recompute on any route change |
| Status registry covers two projects, not the full project estate | Confirmed | `site-src/project-status.json`: Abrahamic Reference Engine and Skillz | A status gate could be mistaken for estate-wide editorial validation | Enumerate all registry consumers and unregistered cards before expansion |
| Status checker validates three hub surfaces, not all project detail claims or search maturity | Confirmed | `scripts/check-project-status.py:15`, `:59-72` | Contradictory detail/search claims can escape the gate | Add scoped consistency fixtures during registry implementation |
| Release verifier verifies SHA, exact inventory, and byte hashes for two generated artifacts only at baseline | Confirmed | `scripts/build-release.py:202-215`, `:254-267` | Workflow step name could imply complete byte verification | Worker reproduction and negative fixtures; see repair record |
| Active foundation-sync instructions contradict the implemented immutable-source contract | Confirmed | `replit.md:303-313` versus `scripts/sync-foundation-files.py:185-212` | Maintainer uses invalid commands or assumes timestamp winner selection | Narrow runbook correction and source/help comparison |
| Several deferred SEO statements describe already implemented article features | Confirmed | `replit.md:283` versus `writings/first-diagram-is-a-liar/index.html:24`, `:33`, `:104`, `:2864` | Repeated work and misleading audit scope | Rewrite as historical, or verify each feature's actual route coverage |
| Publishing runbook still references an archived PAT writer as an active command | Confirmed | `docs/publishing.md:18-25`; active script absent | Maintainer is sent toward an obsolete broad write path | Replace with current PR/Pages contract in a separate bounded docs task |
| Old anchor failure cannot be carried forward unchanged | Confirmed source change; behavior requires browser evidence | `assets/js/app.js:396-418` focuses target and updates hash | Duplicate repair could regress working navigation | Architect's current keyboard/history tests |
| Default reveal visibility still depends on JavaScript on larger screens | Confirmed source; visitor consequence tested by Architect | `assets/css/theme.css:1161-1167`; narrower-screen and reduced-motion exceptions elsewhere | Essential content may remain invisible after script failure | Disabled-JS and blocked-app.js desktop probes |
| Skillz installation example remains a flat placeholder download | Confirmed | `site-src/pages/projects/skillz/index.main.html:668-669` | Visitor cannot follow a reproducible complete-package install | Real pinned package and clean-project execution |
| Broad closeout is insufficient to close a detailed acceptance matrix | Inferred | Compare preceding current-source observations with `thread-implementation-closeout-2026-09-06.md` and `website-advancement-plan-2026-09-05.md` | New plan either repeats completed work or omits surviving defects | Attach evidence to individual package acceptance conditions |

## Reconcile earlier recommendations

| Earlier package | September 7 disposition | Required action |
| --- | --- | --- |
| W01 essential browsing | Partial: anchor focus/hash logic exists; reveal default remains unsafe in source | Verify anchors and fix only surviving failure-state behavior |
| W02 mobile navigation | Browser adjudication owned by Architect | Use current short-height and breakpoint measurements |
| W03 release integrity/retry | All-file byte verification still absent at baseline; retry naming separately remains for delivery Worker review | Bounded integrity repair delegated; keep retry acceptance separate |
| W04 search | Recent snippet and normalized highlight repairs are documented; does not establish complete keyboard semantics | Architect tests selected result, Enter, empty/error, Back, and focus return |
| W05 content/install | Earlier R06 fixed MTB package guidance; Skillz example still broken at source | Correct Skillz separately; do not claim all install guidance fixed |
| W06 estate-wide status | Partial: two registry entries among 14 detail pages | Establish source-supported status records for remaining pages without inventing maturity |
| W07 TOC motion | Recent dedicated TOC implementation and tests exist | Current reduced-motion/resize tests govern, not old finding text |
| W08 images | New art and archive/fallback work changed assets materially | Measure current initial delivery; preserve accepted original art |
| W09 runbooks | Partial: current PR contract exists, foundation sync instructions and the historical-only disclaimer on supported MTB checker flags still conflict with code | Narrow documentation repair delegated |
| W10 QA runtime/portability | Current workflow still selects Node 20; local verification belongs to Worker report | Select supported runtime and validate full suite in separate bounded package |
| W11 preview/Replit boundary | Conditional path, not proof of canonical Pages exposure | Determine whether alternate publication is in use before changing host config |
| W12 headers | Hosting limitation acknowledged in closeout | Preserve real delivered-header evidence; prepare concrete host decision if policy needed |
| W13 analytics | Existing accepted policy is not implicitly revoked by assessment | Define useful measures and revisit account policy only with owner direction |
| W14 locale operations | Four-route-per-locale pilot remains distinct from full-site language readiness | Exact-pair review for changed strings and transparent coverage |
| W15-W17 presentation/content/social | Design proposals, not blanket implementation duties | Architect orders after core reliability and content correctness |
| W18 operations | Separate validation, content delivery, header limitations, and external health | Avoid one green status concealing different contracts |
| W19 human validation | Automated suite cannot establish human task success or assistive-technology certification | Targeted VoiceOver/Safari and independent visitor tasks remain necessary |
| W20 release | Current production state assessed by delivery Worker | Local repairs require combined checks and explicit publication scope before release |

## Concrete next Worker packages

Severity labels here are implementation priorities. No critical exploit or active compromise was established.

| ID | Priority | Owner and scope | Acceptance |
| --- | --- | --- | --- |
| ENG-01 | P1 | Release Worker: `scripts/build-release.py`, release fixtures | Every released file except the manifest itself has digest and size; changed JS/CSS/HTML/data/vendor bytes fail; missing/added files and wrong SHA fail; untouched package passes; manifest boundary remains exact |
| ENG-02 | P1 | Documentation Worker: `replit.md`, `docs/publishing.md`, `ROADMAP.md` | Active commands match parser/help and immutable source selection; historical metadata clearly dated; supported checker flags remain documented accurately; no sibling or universal governance edits |
| ENG-03 | P1 | CI Worker after ENG-01 | Run committed generated freshness before mutating regeneration; deliberate stale HTML/index fixture fails; independently verify final rebuilt artifact; no weaker gate |
| ENG-04 | P1 | Runtime Worker scheduled by Architect | Essential desktop content remains visible with JS disabled and app.js blocked; retain brand, motion preference, anchors, mobile behavior; shared-file integration serialized |
| ENG-05 | P1 | Content Worker | Replace Skillz placeholder with real full-directory package at immutable public revision, tested clean install and repeat-install guard; no unsupported client claims |
| ENG-06 | P2 | Content-schema Worker | Inventory all 14 detail pages plus intentional shelf entries; evidence and unknowns preserved; add agreed statuses to authoritative registry and focused consumer fixtures |
| ENG-07 | P2 | QA/operations Worker | Supported Node runtime selected with primary release documentation; clean install and existing suite pass; investigate duplicate validation cancellation and retry behavior with exact run evidence |
| ENG-08 | P2 | Performance Worker | Capture current cold initial requests at fixed desktop/mobile conditions; optimize highest contributor with quality review; source budgets distinguish original archive size from delivered responsive bytes |

ENG-01 and ENG-02 are independently delegated local implementations under the Architect's authorization. ENG-03 onward are concrete proposals awaiting their scheduled implementation scope. Workers may independently inspect disjoint areas, but generated files and shared runtime have one integrator. Do not dispatch private notes to external agents or publish source merely because a report has a delegation brief.

## Validation and limitations

Workers run the project's declared gates and retain exact outcomes in their linked reports. The PM independently read the source contract and current audit/closeout documents, counted source/sitemap entries, inspected current Git branch/worktree state, and reviewed the specific code supporting this report. PM source observations are not a substitute for browser test results.

Historical preserved stashes/worktrees in earlier notes are not current inventory facts. This checkout reported only local `main` and one worktree in this session; delivery Worker verifies remote state separately. No deletion is recommended to make history look tidy.

Fresh validation evidence includes a macOS path-normalization failure in the historical review-boundary test; passing Linux deployment evidence does not make that local failure a pass. See the validation Worker report for exact reproduction and the remaining fixture scope.

Unknowns remain around real visitor task completion, full assistive-technology coverage, account-level analytics usefulness, external destination ownership state, and whether alternate Replit publication is actively used. Resolve each through its named task instead of presenting a static source scan as end-to-end certification.

## Local remediation results

ENG-01 implemented locally in `scripts/build-release.py` and `tests/test-release-package.py`. Schema 3 adds an exact integrity map of SHA-256 and byte length for every released file except the self-referential manifest. Existing live-edge artifact fields remain compatible. PM independently reviewed the diff and ran `python3 tests/test-release-package.py`: nine tests passed, including same-length and appended changes, inventory changes, bad integrity metadata, wrong commit, and legacy schema rejection. This is consistency against the trusted workflow manifest, not an independent signature against coordinated malicious manifest substitution.

ENG-02 completed locally in `replit.md`, `docs/publishing.md`, and `ROADMAP.md`. Active foundation selection and MTB command modes now match source; the PAT writer is clearly archived; current PR/Pages flow replaces the obsolete fallback; historical roadmap accomplishments and SEO observations remain labeled. PM reviewed the documentation diff and corrected the final release-integrity description to match schema 3. Worker checks verified command help, current MTB values, and generated HTML; `git diff --check` passes. PM independently reran the nine live-edge/hook regressions successfully. Baseline findings above remain explicitly tied to `ca38d5b9`; subsequent local changes are not claims of publication. Artifact retry naming remains open independently of ENG-01.
