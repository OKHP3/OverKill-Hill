# A20 independent task and accessibility acceptance

September 7, 2026. **Prepared baseline evidence; final candidate acceptance pending.**
This report rejects the baseline for the unresolved task failures below. It does
not assess an integrated candidate or make an accessibility conformance claim.

## Identity and scope

- Clean starting revision: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`, including A01/A02.
- Isolated worktree: `/Users/okh/.codex/worktrees/0a49/OverKill-Hill`.
- Branch: `codex/a20-independent-acceptance`. The commit containing this report is
  the handoff revision; the baseline above remains the tested website revision.
- Read `AGENTS.md`, `replit.md`, the [advancement plan](website-advancement-plan-2026-09-07.md),
  its five assessment reports, and the Architect's resolved dispatch registry.
- A21 task: `01a07aaf-76a3-7d20-a26a-c29851127599`. A21 confirmed that it will supply
  a frozen candidate SHA, path and digest artifact after integration.
- No site source, generated HTML, runtime, artwork, indexing policy or workflow
  changed. No candidate edited, sibling synchronization, publication or message
  to an external contact occurred. No generator is required for these reports.

## Environments actually exercised

| Environment | Evidence and limit |
| --- | --- |
| macOS 26.6.2, build 25G83; Edge 152.0.4191.66 | Interactive local browser tasks through CUA; 1280 by 800 desktop and 390 by 844 compact viewport. Compact viewport is emulation, not a phone. |
| Node 26.0.0; locked Playwright 1.62.1 | Existing Chromium accessibility and tree suites. This does not establish A08's supported runtime or CI parity. |
| Default Python plus temporary pinned QA environment | Default and bundled Python lacked `bs4`; existing `requirements-qa.txt` installed into `/private/tmp/a20-qa-venv`, then HTML freshness passed. No dependency manifest changed. |
| Real Safari / VoiceOver | Safari was listed as running. Native `cua.getApp('com.apple.Safari')` failed with `timeoutReached` after 138.6818 seconds. No Safari navigation or VoiceOver task/speech session completed. |
| NVDA / Firefox / physical phone | No corresponding controlled session available in the enabled surfaces. Not tested. |

Preview used `python3 -m http.server 18220 --bind 127.0.0.1` from this isolated
worktree. It serves local static files, not production response headers. Browser
viewport, script-disabling and request-blocking overrides were restored; the
temporary browser tab was closed. Third-party availability was not assessed.

## Five declared visitor tasks and baseline observations

These tasks translate the Architect's proposed usable-tool, prototype, install,
reading and inquiry journeys into repeatable acceptance sessions. A task may
have passing substeps and still fail overall. No elapsed-time usability metric
or independent human-participant study was performed.

| Task | Procedure and completion criterion | Baseline result | Candidate retest |
| --- | --- | --- | --- |
| T1: Reach usable work despite an enhancement failure | At 1280 by 800 load `/` with JavaScript disabled, then with only `assets/js/app.js` blocked. Read heading/art/actions and follow a project link. Separately activate Skip to main, then Tab into main. | FAIL X01: screenshot showed an empty hero background; the `h1` ancestor `.container.hero-inner.reveal-on-scroll` had opacity `0` in both failure modes. With normal scripting, Skip updated `#main`; next Tab focused the `The Forge` link inside main. Project-link continuation under script failure was not completed. | Pending exact candidate. Repeat both failures plus missing observer, initialization failure, normal and reduced-motion cases; verify visible usable links, not merely DOM presence. |
| T2: Identify a concept or prototype before deciding to use it | Inspect the shelf, detail and search status for a prototype; directly visit Hometools, Pathscrib-r and Un-nocked Truth. Explain publication, maturity and delivery evidence separately. | FAIL C03/C04, source inspection only: `site-src/project-status.json` has two records; three concept main bodies have no visible concept notice. Full rendered cross-surface and spoken-status task not completed. | Pending A06/A11 integration. Check each visible notice and status consumer; retain noindex and named shelf exceptions. |
| T3: Install one complete Skillz package safely | Follow the page's exact pinned full-package example in an empty project for its named client. Resolve supporting references, repeat without overwriting, and attempt its documented activation separately. | FAIL C01: source steps 04/05 still direct a raw file to `.agents/skills/my-skill.md` with a placeholder `main/skills/family/SKILL.md` URL. No pinned complete package is specified. Placeholder download and client activation were not attempted. | Pending A05 candidate example. Independently run its commands and record revision, file inventory, reference resolution, no-overwrite result and client activation as separate results. |
| T4: Retrieve and read writing or evidence | Search `mermaid`; use ArrowDown/Up to identify the selected destination, Enter to follow, Escape to return focus. Inspect clean excerpts. Follow the article's argument/evidence jumps and use Back. Supplement with a story chapter task. | FAIL X02/X03: ArrowDown left focus in the search input, with no active-descendant relationship; selected link used only `data-active="true"`. Visible excerpts contained `</div` and `</di…`. Escape returned focus to the search button. Dedicated search `MurderBird` plus Enter opened the story; `Read the story` plus Enter updated the fragment and focus ID to `the-maker`. Article evidence jumps/Back were not run. | Pending A04. Retest original queries and article jumps, plus empty/loading/error states, category/query history, accents, bounds, Tab, Enter and focus return. Actual selected-result speech remains required. |
| T5: Prepare an inquiry from compact navigation | At 390 by 844 expand navigation, reach Contact, identify the email destination and information useful in an inquiry. Do not send. | PARTIAL: Enter on Toggle navigation expanded it and focused The Forge; clicking the exposed Contact link reached `/contact/`, heading `How to Reach The Hill`, and main email link `mailto:contact@overkillhill.com`. No email sent. Entire keyboard-only traversal and inquiry-prompt comprehension were not tested. | Pending candidate. Repeat entirely by keyboard and screen reader; include phone touch exploration, closing/reopening menu, Escape and focus recovery. |

Failure evidence above is retained as direct observed values and actions from
this A20 session, not copied from implementer summaries. The no-JavaScript
screenshot remains conversation evidence, not a committed image. Keep original
rows when retesting; append the candidate SHA, environment, outcome and artifact
for each failure. An unavailable retest remains pending, never resolved.

## Local check ledger

Every success below applies to the unchanged baseline website. Existing package
installation needed network permission after sandbox DNS failures. Both browser
suites initially failed at launch with macOS `MachPortRendezvousServer` permission
denial; the authorized retries completed with exit code zero.

| Result | Exact command / evidence |
| --- | --- |
| PASS with warnings | `python3 scripts/validate-site.py`: no errors, 32 warnings; MTB and banner checks pass; no new voice warnings beyond reviewed baseline. |
| BLOCKED initially; PASS after pinned setup | `/private/tmp/a20-qa-venv/bin/python scripts/build-site.py --check`: 36 generated pages current. |
| PASS | `python3 scripts/build-search-index.py --check`: current, 160 entries. |
| PASS | `python3 scripts/cache-bust.py --check`: 146 scanned HTML files, zero changes. |
| PASS | `python3 scripts/check-locale-links.py`: manifest check for fr, de, es. This is not linguistic review or all regional-policy acceptance. |
| PASS | `python3 tests/test-release-package.py`: nine tests. |
| PASS | `python3 scripts/build-release.py --output /private/tmp/a20-baseline-release --commit 98922aebf71d90b2b18ecc34c8b00a041fff51c7`, then same command with `--verify`: 56 HTML pages, 371 files. |
| PASS | Independent Python standard-library inventory/hash walk: exact file-set equality, schema 3, expected commit, integrity keys equal all payload paths excluding manifest, every byte length and SHA-256 matched. [Retained receipt](../audit/remediation-a20-2026-09-07/baseline-integrity.json). |
| PASS, narrow automation | `node scripts/accessibility-qa.mjs --base-url=http://127.0.0.1:18220`: four interaction samples and 31 sitemap routes. Original launch log `/private/tmp/a20-accessibility.log`; successful retry `/private/tmp/a20-accessibility-retry.log`. |
| PASS, tree structure only | `node scripts/screen-reader-tree-audit.mjs --base-url=http://127.0.0.1:18220`: six pages. Original launch log `/private/tmp/a20-tree.log`; successful retry `/private/tmp/a20-tree-retry.log`. |

Temporary log paths are diagnostic convenience, not durable artifacts. The
results and failure details are retained here. The tree script's preamble says
it is in Linux and can verify exactly what would be announced. Those statements
do not describe this macOS run and are not accepted as evidence of speech or
browser/assistive-technology interoperability. A21 should route that wording to
the QA owner; A20 did not edit shared QA code while reviewing it.

The baseline manifest SHA-256 is
`75369969469dba4445da8b32a44db29dc61a189dab809c02b778fc98614ed0fa`.
All 370 payload digests were independently matched. The manifest is excluded
from its own digest and is not a signature. Source completeness and delivered
production bytes are separate claims. Production SHA was not rechecked here.

## Frozen-candidate acceptance contract

A21 must provide the exact 40-character SHA, selected package scope, clean
candidate path, release artifact and manifest digest. Review that immutable
state without modifying it. Any fix creates a new candidate SHA and rerun scope.

1. Verify baseline-to-candidate scope and authoritative source ownership. Run
   committed freshness before any generation; use the candidate's current gates.
2. Verify the exact packaged file inventory and every payload digest independently.
   Account for all shipped HTML routes, with named exceptions; sitemap remains
   indexing scope. Baseline 56/31 counts are observations, not hardcoded targets.
3. Repeat T1-T5 and all original failures against the candidate. Keep accepted
   skip, search Enter and chapter-focus behavior. Confirm pinned installation,
   concept labels and status consistency from actual output.
4. Run real Safari/VoiceOver sessions and available NVDA/Firefox/phone sessions.
   Record OS/browser/AT versions, navigation mode, viewport or device, actions,
   actual announcements, expected result, observed result and evidence. Verify
   selected results, live statuses, landmarks, heading navigation, menus, focus,
   table/diagram alternatives and recovery. A tree snapshot cannot fill this row.
5. Keep source, local browser, CI, staging and live deployment dispositions
   separate. CI, full shipped-route regression, physical devices, real AT,
   full external-tool use, staging and live acceptance are NOT RUN in this A20
   baseline packet. Do not infer any of them from the existing automated passes.

Decision rule: reject reproduced task blockers; accept-with-limits only when
the tested scope passes and remaining unavailable checks are explicitly accepted
by the responsible release decision maker. A20's full requested acceptance
remains pending until real AT and frozen-candidate evidence exist. No publication
is authorized by this report or by passing tests.
