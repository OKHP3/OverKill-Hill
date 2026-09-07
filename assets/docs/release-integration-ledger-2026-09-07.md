# A21 release integration ledger

## Baseline and authority

Confirmed September 7, 2026: this isolated checkout began clean at
`98922aebf71d90b2b18ecc34c8b00a041fff51c7`, matching freshly fetched
`origin/main`. Integration branch: `codex/a21-release-integration`.
A01/A02 are in this baseline. The advancement plan's descriptions of them as
uncommitted are historical. No open pull requests were returned at intake.

This ledger implements the existing [advancement plan](website-advancement-plan-2026-09-07.md).
It does not replace its priorities. A21 is the sole integrator. Workers retain
their own isolated checkouts. No sibling writes or canonical-checkout changes
are authorized here. Preserve source branches and worktrees for recovery.

## Dependency and ownership ledger

Task IDs are confirmed by coordinator handoff below. The disposition log below
supersedes initial NOT RECEIVED states. Ownership below identifies package scope;
exact touched paths must accompany each package before integration.

| Package | Source ownership | Required upstream contract | Acceptance boundary |
| --- | --- | --- | --- |
| A03 | Shared reveal CSS/JS and targeted fixtures | Baseline shared-runtime compatibility | Fail-open failure modes; hand off runtime diff to A04 |
| A04 | Shared search JS/CSS; search extraction and fixtures | Reviewed A03 runtime diff | Accessible selection, clean snippets, final English strings |
| A05 | Skillz English install instructions and install fixture | Verified pinned complete public package | Clean install, no overwrite; activation separately evidenced |
| A06 | Targeted English claim corrections | Dated public evidence | Concept notices, history, rights, qualified claims |
| A07 | Validation/Pages artifact and freshness workflow | Baseline A01 | Attempt identity, stale-input rejection, actual rerun evidence |
| A08 | Existing QA runtime declaration/setup | Official supported runtime selection | Lockfile scope preserved; setup and browser evidence |
| A09 | Historical-review fixture | Preservation receipt | Alias/default/canonical-root evidence; archived bytes preserved |
| A10 | Shipped-route browser coverage/reporting | Reviewed A07/A08 contracts | Every shipped route accounted; missing browser fails |
| A11 | Project status source registry and consumers | Reviewed A06 facts | All detail pages, named exceptions, unknown proof retained |
| A12 | Featured/latest labels and descriptions | Reviewed A06/A11 | Metadata and visible previews agree |
| A13 | French interaction copy and relevant runtime hooks | A04 final English strings | Exact-pair linguistic review; noindex boundaries retained |
| A14 | Isolated presentation proposals, then selected sources | A11/A12; explicit owner selection | Two rendered proposals; elapsed time is not selection |
| A15 | Reader orientation and Contact sources | A11/A14 selected contract | Original text, URLs, anchors, keyboard history preserved |
| A16 | Measured asset/font/analytics changes | Fixed-condition network baseline | Before/after evidence and visual parity; policy decisions explicit |
| A17 | Workflow concurrency and status reporting | Reviewed A07/A08 workflow/runtime | PR, rapid-push, dispatch/rerun required checks retained |
| A18 | Preview server and publication boundary fixtures | Required before external preview exposure | Loopback/bounded input/storage/allowlist/escape evidence |
| A19 | Host strategy decision evidence | Explicit owner host choice for implementation | Staging, cost, operations, rollback; no inferred approval |
| A20 | Independent acceptance report only | Frozen integrated candidate SHA | Named actual devices/AT, five tasks, retained failures |
| A21 | Combined generated HTML/search/universe/CSP/fingerprints; release evidence | Reviewed selected packages and A20 disposition | Exact SHA/digests/artifact/CI/live evidence and rollback |

Serialize shared `assets/js/app.js` and `assets/css/theme.css` contributions:
A03 before A04, then A13 and any selected presentation/performance changes.
Review shared-runtime compatibility against the existing ADR; do not copy
changes to siblings. Serialize `.github/workflows/validate.yml` contributions:
A07 and A08 contract reconciliation before A10/A17 integration. Do not resolve
these overlaps by taking one worker's entire file over another's changes.

English authoring remains in `site-src/`. A21 regenerates outputs from accepted
sources. Worker-generated files can demonstrate intent but are never the
authority for hand-merging output conflicts. A11/A12/A14 may share page metadata
and shelf sources; require exact source-path manifests before combining them.

## Package intake and review contract

Each handoff must contain package ID, task ID, immutable commit SHA, baseline,
exact changed paths, prerequisites and their accepted revisions, before/after
reproduction, commands and results, generated-output requirements, locale
impact, reviewer disposition and unresolved evidence. Missing fields remain
pending. A branch name or passing worker summary alone is not review acceptance.

Record each package's state as NOT RECEIVED, RECEIVED, REVIEWED READY, REJECTED,
INTEGRATED or DEFERRED. Record the reviewing task and reviewed SHA. An already
fixed finding may close with current-source evidence and no duplicate patch.
Do not integrate unresolved dependency-sensitive edits. Source review and
combined candidate acceptance are distinct gates.

## Candidate and release sequence

1. Select an independently useful batch from reviewed ready packages. The plan
   recommends A03-A08 and ready A09 first, with focused A20 acceptance. Do not
   interpret all later packages as prerequisites or silently mark them complete.
2. Recheck origin, working-tree inventory and baseline divergence. Record the
   pre-integration SHA as recovery evidence. Integrate only the named reviewed
   commits into this branch; preserve all concurrent work.
3. Review combined authoritative source conflicts. Run the required generators
   in their current supported order, including HTML, CSP, fingerprints, search
   and universe. Recheck every generated family after the final mutation;
   generation success alone cannot prove committed freshness.
4. Commit coherent generated outputs, then run committed freshness before any
   mutator. Run all required checks in the reconciled validation workflow, plus
   each accepted package's regressions. Record environment and report paths.
   Audit outputs must leave tracked sources unchanged.
5. Freeze the candidate SHA and all-file manifest. A20 reviews that exact SHA
   without modifying it. Missing Safari/VoiceOver, NVDA/Firefox or phone
   sessions remain unavailable evidence. Automated checks cannot establish
   human acceptance or WCAG conformance.
6. Only a reviewed candidate can enter the authorized normal PR/merge/deploy
   flow. Read the publishing skill at that point. Record PR, exact tested SHA,
   required checks, artifact run/attempt identity, digest inventory and review
   disposition. Draft PRs must name unmet dependencies. Never bypass protection.
7. Verify the deployed artifact and live manifest against the intended release,
   compare delivered bytes and rerun representative visitor tasks. Record
   content, host headers and external availability separately. Preserve the
   prior accepted deployment SHA/artifact as the rollback target; a source
   baseline alone is not proof of the previous live deployment.

Owner presentation, host-policy and human acceptance gates require their actual
evidence. No timeout, elapsed wait, source test or CI pass supplies approval.
No publication candidate is ready at intake.

## Current evidence

All intake checks below address baseline
`98922aebf71d90b2b18ecc34c8b00a041fff51c7` on Windows with
Python `3.14.0rc1` and Node `24.11.1`. This is not claimed as A08 runtime parity.

| Status | Command | Evidence |
| --- | --- | --- |
| PASS | `git status --short --branch` | Clean detached intake; named integration branch subsequently created |
| PASS | `git fetch origin main` and revision comparison | HEAD and origin/main match specified baseline |
| PASS | `py -3 -X utf8 scripts/build-site.py --check` | 36 generated pages current |
| PASS | `py -3 -X utf8 scripts/build-search-index.py --check` | 160 current entries |
| PASS | `py -3 -X utf8 scripts/cache-bust.py --check` | 146 scanned files; zero changes |
| PASS | `py -3 -X utf8 scripts/generate-csp.py --check` | 56 page policies current |
| PASS | `py -3 -X utf8 scripts/sync-universe-map.py --check` | Universe map current |
| PASS | `py -3 -X utf8 tests/test-release-package.py` | 9 regressions |
| PASS | `py -3 -X utf8 -m unittest tests/test_verify_live_edge.py` | 9 regressions |
| NOT RUN | Integrated browser/AT/CI/deployment acceptance | No reviewed candidate exists yet |

The counts are this intake's observed results, not fixed future route gates.
Cross-machine architect alignment remains UNKNOWN: architect01a07281 is
inaccessible from this host. No second-machine confirmation has been supplied.

## Confirmed task routing

| Package | Task ID |
| --- | --- |
| A03 | `01a07ab0-c2a4-7e20-ae8f-a21c61751116` |
| A04 | `01a07ab0-c280-7de3-9e69-abb308c94306` |
| A05 | `01a07ab0-c2ad-7f42-9a31-58aa21d16735` |
| A06 | `01a07ab0-c2a4-7e20-ae8f-a1ff5726a7dd` |
| A07 | `01a07ab1-0899-7ca2-8c1a-b7dc3b0817c8` |
| A08 | `01a07ab1-087d-73a0-95e3-5f93e302efa8` |
| A09 | `01a07ab1-0880-7591-85f0-df1d1616b1b9` |
| A10 | `01a07ab1-087e-7de0-ac07-39d978a7a613` |
| A11 | `01a07ab1-087f-7f30-af45-7c7db61578bb` |
| A12 | `01a07ab1-089a-7da1-8c8d-978e098bb529` |
| A13 | `01a07ab1-1bed-7273-97e0-ce92c4bae23b` |
| A14 | `01a07ab1-32ce-7663-9fea-337d1ef55967` |
| A15 | `01a07ab1-5e65-7c73-acbd-75017460f60d` |
| A16 | `01a07ab1-64cb-7860-9831-27022e797c2f` |
| A17 | `01a07ab1-7e00-79f3-bbaa-48f164c012b3` |
| A18 | `01a07ab1-8b18-7183-b066-bdd181039eac` |
| A19 | `01a07ab1-8b16-7d63-b1d8-e01a488f12ad` |
| A20 | `01a07ab1-ae00-7a01-bee3-e676f260e3cb` |
| A21 | `01a07ab1-ae09-76d3-8384-f669b18f7f21` |

## Integration disposition log

A21 performed source review before the following cherry-picks. These are source
integration decisions, not release approval. No combined candidate is frozen.

| Package | Worker SHA | Integration SHA | Disposition and evidence |
| --- | --- | --- | --- |
| A03 | `6a0a6aaea1ae9adafc5fdc146b55ed785814d813` | `778608ae` | INTEGRATED: disjoint reveal block reviewed; independent `node tests/test-reveal-browser.mjs` passes all 10 scenarios. Added standalone test to combined CI. Combined cache regeneration pending A04. |
| A07 | `7f4aa0b15c5c676c1a1babb113c30428c85158bf` | `3928a42d` | INTEGRATED: producer output, empty guard, matching Pages names and pre-mutation freshness reviewed. Independent combined regression rerun pending. Actual full/deploy-only CI retries NOT RUN. |
| A08 | `f524d7fc31303d18fca826394746c031cba9418e` | `61060cd7` | INTEGRATED: only root engine metadata added to dependency graph; two workflow selectors use .nvmrc. Local Node 24.11.1. Ubuntu/latest patch CI and connected Replit NOT RUN. |
| A09 | `c9fa89490c4e7477f5ef1b09a10dec3f942884af` | `42af4220` | INTEGRATED: fixture resolves its patched root just as archived builder resolves __file__; no archive edits. Independent three-case test PASS, including Windows junction. Native macOS and POSIX run remain NOT RUN. |
| A19 | `547f31143a425632777edc73e0211bf61fe5c66b` | `904eceb7` | INTEGRATED as decision evidence only: source/observation scope reviewed. No host implementation, provider staging or owner selection accepted. |

Native macOS pending command: `python3 tests/test-murderbird-review-boundary.py`
at worker candidate `c9fa89490c4e7477f5ef1b09a10dec3f942884af`. Coordinator
confirmed the second-machine task remains inaccessible. That unavailable check
does not block unrelated fixes or become PASS. Final selected release scope
must account for the unresolved A09 acceptance condition.

Received preparation only, not implementation completion: A11 inventory
`39bc5c2c2bede18f99d7a9121fbc024254d6c641`; A13 audit
`d220902e8f8b4212ee2d69ee1a67955c6b4369fa`; A15 proposal
`e9154af71eb8248cad2efcf2d44fa5d06bd0ad06`. These are not integrated at this
checkpoint. A12 source subset `2074a969825e81e742d728b6816fb0adb364b445`
is reviewed but awaits its A06/C08 completion disposition before intake.

A04 received reviewed A03 contract. A10/A17 received reviewed A07/A08 contracts
and instructions to resume dependent implementation. A06 was asked to deliver
its immutable factual contract directly to A11/A12. A20 is preparing baseline
evidence and awaits an exact frozen combined SHA for independent acceptance.
