# Analytics purpose and visitor-choice decision memo

September 7, 2026. **NEEDS INPUT for policy; documentation-only proposal.**
Scope: W13 / SD-09. Starting HEAD and fetched `origin/main` both resolved to
`98922aebf71d90b2b18ecc34c8b00a041fff51c7`. Branch:
`codex/w13-analytics-decision`. No analytics, account, disclosure, consent UI,
locale, or deployment behavior changes are authorized by this memo.

## Decision context

Which measurements support an actual owner decision, and what collection and
visitor-choice behavior should support them? The [September 7 plan](website-advancement-plan-2026-09-07.md)
requires A16 cost evidence before the owner chooses analytics policy. A16 owns
performance trials and optimization; this package owns purposes, data boundaries,
unknown settings, and options. A21 owns integration. Coordination messages were
sent to both tasks on September 7. A16's planned handoff is
`assets/docs/remediation-a16-2026-09-07.md`; its final results were not available
when this memo was prepared. Do not use the earlier single-load byte count as a
controlled performance result.

The [September 5 plan](website-advancement-plan-2026-09-05.md) explicitly records
a previously rejected consent UI. The September 7 plan preserves that decision.
The original rejection wording and rationale were not recovered from the scoped
repository search. Its continued force is clear; no banner is proposed for
implementation without an explicit new owner decision. SD-09 is a product
decision, not an established legal violation.

**Already addressed:** analytics and cookie disclosure exist in
[the authoring source](../../site-src/pages/legal/index.main.html) and
[generated Legal page](../../legal/index.html). Commit
[`931771a1`](https://github.com/OKHP3/OverKill-Hill/commit/931771a15c037192f0ad80bc46df763afe7e29af)
records the legal trust-surface work. Do not recreate a missing-disclosure repair.
Current disclosure describes aggregate visits, referrals, device/browser
categories, engagement, possible cookies/identifiers, and browser/extension
controls. It states that analytics is not used to sell personal information or
make decisions about visitors. Those are published owner statements, not an
account audit. No retention duration or first-party withdrawal mechanism is stated.

## Verified boundaries and consequences

| Claim | Tier and evidence | Consequence if false; next check |
| --- | --- | --- |
| Initialization is in the shared head, not app.js | CONFIRMED: [head partial](../../assets/partials/head.html), lines 97-103, asynchronously loads Google tag and queues `js` then `config`; [app.js](../../assets/js/app.js), lines 66-75, dispatches markup-defined events | Editing only app.js would leave collection initialization; recheck final generated head |
| No first-party consent/default-denied or disable gate was found in these runtime sources | CONFIRMED source scan and nine browser fixtures below | A newly added gate would change the option baseline; repeat source/probe checks after integration |
| Homepage coverage differs by locale | CONFIRMED fixtures: English and en-GB initialize; fr/de/es/es-MX do not | Cross-locale visit comparisons would be biased; inventory all released routes before using such a report |
| Search input can enter analytics page-location data | INFERRED from `/search/?q=`, app.js URL handling, unchanged tag config, and S1; optional enhanced search recognizes `q` under S2 | Do not promise local-only search privacy merely because matching is client-side; inspect stream redaction/enhanced settings and a separately authorized payload capture |
| Actual collection, retention, sharing, advertising, and receipt are unknown | UNKNOWN: no GA4 connector or supplied account export was available; no account session was inspected | A source-only policy statement could be inaccurate; obtain bounded read-only settings evidence |
| No live analytics telemetry was sent by these probes | CONFIRMED method: all external requests aborted; same-origin requests fulfilled from checkout files | Live behavior remains unverified; future live testing needs explicit authorization and exclusion from real reporting |

### Data-flow map

1. Browser obtains the page from the host. Host request logging is a separate
   boundary whose retention was not inspected.
2. The English head attempts `www.googletagmanager.com/gtag/js`. The local
   `dataLayer` queues configuration even if that request is blocked. When loaded,
   the vendor library can send measurement to Google Analytics; the site's CSP
   permits Google Analytics collection origins. Permission in CSP is not proof
   that a particular request was sent or received.
3. S1 documents a default page view, full page location, referrer, title, language,
   and screen resolution. The site does not override those configuration fields.
   Query data can therefore reach measurement independently of a custom search
   event. A referrer header policy does not sanitize JavaScript event parameters.
4. Skillz markup has 23 event-bearing controls. One synthetic click queued
   `skillz_live_app_open` with category `cta` and label `hero`. This proves local
   dispatch, not receipt or a completed app task. Optional enhanced outbound or
   download measurement could overlap custom events; actual settings are unknown.
5. S3 documents first-party `_ga` and `_ga_<container-id>` cookies with two-year
   defaults, subject to browser limits and configuration. Cookie lifetime is
   distinct from account retention. Cookie blocking alone does not guarantee
   no transmission. No live cookie values were read or retained.
6. Fonts and embedded tools remain separate recipients even if analytics is
   removed. The Skillz fixture also attempted its external iframe and project
   summary request. Email begins only through the visitor's mail workflow;
   message content is not an approved metric. No form or email was submitted.

French remains released; other retained locale drafts remain noindex under
their existing policy. Noindex is not a collection or access-control switch.
These homepage observations do not justify adding tags to currently untagged
locales or changing their release state. The [translation workflow assessment](translation-workflow-cleanup-2026-09-05.md)
governs the distinct translation follow-up.

## Proposed minimum measurement contract

No metric has been established as necessary by an owner decision or account
usage evidence. These are candidates for approval, not new instrumentation.

| Owner decision | Smallest useful measure | Boundary and review |
| --- | --- | --- |
| Which published work merits maintenance? | Monthly page-view totals by canonical path | Exclude query/fragment and internal trials; views do not establish reader understanding |
| Which public referral channels merit effort? | Monthly aggregate source/channel | Prefer coarse source categories; do not retain raw referral queries or visitor profiles |
| Are project entry links used? | Counts of allowlisted outbound actions by project and placement | Reuse verified event names where useful; deduplicate enhanced/custom counts; a click is not successful tool use |
| Which device layouts deserve testing? | Coarse device/browser proportions | Optional; combine with actual task failures, not individual-device tracking |
| Does search help readers? | Moderated synthetic task completion initially | No raw visitor queries needed; any later aggregate result-count/outcome event needs a separate schema decision |

Proposal: owner reviews the approved aggregate report monthly for two cycles.
If it changes no concrete editorial or maintenance decision, revisit removal.
Do not add advertising, demographics, persistent identity, inquiry text, or raw
search terms to satisfy this contract. A16 should attach measured costs before
the owner weighs usefulness against burden.

## Account evidence still needed

Read-only evidence should record the observation date, verified property/stream
match, and settings without credentials, visitor rows, cookie values, or raw URLs
in this public repository. All following values are currently **UNKNOWN**:

| Settings to inspect | Decision they resolve |
| --- | --- |
| Property/stream identity; extra tag destinations; cross-domain configuration | Whether the public tag reaches only the intended property and how sibling/embedded visits are treated |
| Event/user retention and reset-on-activity; cookie expiration/update overrides | Actual persistence; S4 explains that aggregate standard reports are not governed by the same retention setting |
| Enhanced measurement, especially search, history page views, outbound links and downloads; query/email redaction | Actual automatic event exposure and duplicate counting |
| Google signals; advertising personalization; Ads/product links; user-provided data; account data-sharing settings | Whether collection exceeds the proposed purpose |
| Internal/developer filters, reporting identity, exports and access roles | Whether trials distort results, additional copies persist, and access is proportionate |
| Existing reports actually reviewed by the owner | Whether measurement has demonstrated value |

Do not infer an off setting from absence of configuration in Git. Do not change
settings while collecting evidence. S4's retention options and deletion behavior
must not be described as this property's settings or as deletion of all copies.

## Narrow options for owner selection

| Option | Concrete scope after approval | Tradeoff and acceptance |
| --- | --- | --- |
| A. Retain current behavior pending evidence | No runtime change; obtain settings and A16 report, then confirm or revise disclosure | Preserves current decision but leaves first-party visitor choice absent; record an explicit review point, not a claim of compliance |
| B. Remove first-party GA4 | Remove active tag/config and analytics resource hint from authoritative inputs; remove or inert custom dispatch; reconcile generated outputs and notice | Loses browser analytics; fresh/reload/navigation/event fixtures must show zero first-party GA tag/collection attempts. Inventory existing GA cookie cleanup separately; do not delete account history implicitly |
| C. Retain GA4 with data minimization, no new UI | Approve canonical-path-only page locations, referrer minimization, allowlisted events, and separately reviewed account settings | Still makes analytics requests and may use identifiers. Test every event field, initial/history page views, query strings and fragments; disabling enhanced search alone is insufficient |
| D. Explicitly reopen visitor choice | Separate owner-approved design for a persistent Analytics control, with either default-off basic loading or clearly disclosed default-on opt-out | Changes the preserved choice policy. Must specify the default and meet the state contract below before implementation |

Recommendation: make the owner decision after the bounded settings readback and
A16 evidence. B is the simplest technical option if no useful metric is approved;
C is a candidate if aggregate measures justify continued collection. Neither is
selected here. Advanced consent mode is not a shortcut to a no-request promise:
S5 explains that denied storage can still send cookieless measurements. No need
for such modeling has been demonstrated in this portfolio's proposed measures.

### State contract if D is selected

| State | Proposed default-off/basic contract | Default-on opt-out difference |
| --- | --- | --- |
| Fresh or invalid/unreadable stored choice | Do not load GA or queue replayable analytics events; no analytics resource hint | Collection occurs before choice; this must be explicit in the notice |
| Accept | Persist versioned choice locally; load/configure once; start prospective allowed events only | Continue permitted collection without duplicate configuration |
| Reject | Persist denial; no GA load/collection; retain working navigation, search, theme and content | Stop future dispatch and prevent loading on the next page; initial collection cannot be undone |
| Withdraw after accepting | Immediately stop dispatch, persist denial, clear only identified first-party GA cookies with correct domain/path scope, and reload if needed to remove the loaded library | Same prospective stop; verify no queued or unload event escapes during transition |
| Return visit, another tab, expiry, unavailable storage | Reapply before configuration; synchronize withdrawal between tabs; fall back to off on unreadable choice | Owner must explicitly choose whether this also falls back to off |

Use an accessible permanent control with equally reachable choices and an
owner-selected persistence duration. Do not queue rejected activity for later
replay. Withdrawal cannot retract already transmitted data or promise account
deletion. Scope the guarantee to this site's analytics; independently inspect
embeds if a broader promise is desired. Test fresh/accept/reject/withdraw/return,
history navigation, two tabs, storage failure, keyboard access, and blocked
vendor script. These are future acceptance criteria, not passing tests today.

## Evidence and validation

[Machine observation record](../audit/analytics-boundary-2026-09-07.json): nine
fresh Chromium 151.0.7922.34 contexts, four English routes and five locale
homepages. All nine returned 200 and one h1; five attempted a GA script and
queued `js`/`config`; four did neither. One synthetic Skillz click queued the
expected named event and two static labels. Zero cookies in these blocked-script
contexts is expected and does **not** establish cookieless live behavior.

Reproduction: use isolated Playwright contexts with service workers blocked;
intercept every request before navigation; fulfill same-origin paths from this
SHA's files and abort all other origins. Visit the nine routes in the JSON;
record tag elements, sanitized dataLayer commands, cookie names, and external
origin/path only. On Skillz, prevent navigation and click the first event-bearing
control. Never retain query identifiers or let the real Google script execute.

No live tag execution, collection payload, account receipt/settings, legal
jurisdiction analysis, accepted/rejected/withdrawn implementation, or whole-site
functional test was performed. The document and JSON are the only tracked
changes. No generators were run in write mode; A21 owns final reconciliation.

Validation at handoff: all eight relative document links resolve; JSON parses;
the nine fixture outcomes, five tag initializations, and one synthetic payload
match the observations above. `git diff --check` passes. Search-index check
passes with 160 entries. Generated-HTML freshness is **NOT RUN**: both the
default and bundled Python attempts stopped at missing `bs4` before checking
outputs. No dependency was installed. Full release/browser QA is not claimed
for this documentation change; A21 must run the final candidate's required gates.

## Authoritative source ledger

All retrieved September 7, 2026. Google is the primary authority for its tag
and Analytics mechanics; these sources establish product behavior, not this
owner's configured values or legal obligations.

| ID | Publisher and title | Supported claims |
| --- | --- | --- |
| S1 | Google Developers, [GA4 Configuration](https://developers.google.com/analytics/devguides/collection/ga4/reference/config) | Default page view, page location/referrer/title and device-related fields; overridable configuration |
| S2 | Google Analytics Help, [Enhanced measurement events](https://support.google.com/analytics/answer/9216061?hl=en) | Optional search measurement recognizes `q`; automatic outbound and download events |
| S3 | Google Analytics Help, [Cookie usage on websites](https://support.google.com/analytics/answer/11397207?hl=en) | Cookie names, default lifetime, overrides, transmission without cookies |
| S4 | Google Analytics Help, [Data retention](https://support.google.com/analytics/answer/7667196?hl=en) | User/event retention and reset behavior; aggregate-report distinction |
| S5 | Google Developers, [Consent mode overview](https://developers.google.com/tag-platform/security/concepts/consent-mode) | Basic blocking versus advanced cookieless measurements; consent is not a UI supplied by the tag |

**Next action:** owner reviews the proposed metric contract alongside A16's cost
report and supplies or authorizes the bounded settings readback. Record the
selected option and any changed consent-UI decision before a separate
implementation PR. Merging this memo approves no policy or account change.
