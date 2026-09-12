# T05: locale policy v2 proposal

Status: **PROPOSAL. Owner decision pending; no migration authorized by this document.**
Prepared September 7, 2026 against fetched `main` commit
`98922aebf71d90b2b18ecc34c8b00a041fff51c7` in the isolated T05 worktree.
This PR does not activate policy or change locale publication behavior. It
preserves the proposal, supporting evidence, a staging-only headers adapter,
and the focused contract test without changing production HTML, alternate
links, indexability, release behavior, ledgers, source writing, artwork, or
historical review records.

## Problem and intended result

One versioned site policy should define locale coverage and release rules without
making a review claim from a publication label. Keep review events and hash
observations separately versioned and linked to that policy. A page can be
released, AI-reviewed, without human/native approval, source-current, and
changed since review. Each fact must remain independently expressible.

The [September 5 T05 finding](../assets/docs/translation-workflow-cleanup-2026-09-05.md)
remains supported by current source. The
[September 7 plan](../assets/docs/website-advancement-plan-2026-09-07.md)
assigns French interactions to A13 and integration to A21. This proposal does
not repeat their implementation work or establish linguistic quality.

## Current authorities and exact migration mapping

All paths below refer to the recorded baseline. Current status is verified from
source and read-only checks, not inferred from an older audit.

| Current authority / fields | Actual behavior | Proposed v2 destination |
| --- | --- | --- |
| `i18n/sync.config.json`: `schema_version: 1.0`, `in_scope_routes`, `target_locales.*.{locale,root,skill}` | Four routes for fr/de/es only; exact language pairs differ from short route prefixes | `policy.locales[]` carries explicit locale ID, language tag, root, skill and route records; compatibility exporter retains the v1 detector input |
| Same: `blocking_locales: [fr]`, `search_index`, `state_file` | French source drift blocks; de/es drift is advisory; English search index supplies detector inventory | `checks.source_freshness` per locale plus explicit `detector` adapter paths |
| `i18n/pilot/manifest.json`: top-level `pilot-ready`, `translation_policy: human-reviewed-required` | Policy prose conflicts with narrower AI evidence; checker does not enforce that policy string | `legacy_claims` reference preserves exact old text; future `approval_requirement` needs owner decision, never an imported approval |
| Same: fr locale/page `translated` | Checker interprets `translated`, `published`, and `released` as published | fr `publication.state: released`; independent review and approval fields below |
| Same: de/es `drafted-pending-human-review` | Served noindex drafts, excluded from sitemap/search, but reciprocal alternates required | `publication.state: served-draft`; `alternates.profile: pilot-reciprocal`; old pending-human wording retained as history |
| Same: `pages`, `routes`, `target_locales`, `search_index.{command,output,status}` | Duplicate coverage; search `current` is a recorded label, not proof | One route list per locale; derived index adapter path; runtime freshness report recomputes status |
| `i18n/pilot/regional-drafts-manifest.json`: `ai-reviewed-draft`, `translation_policy`, `publication_gate` | en-gb/es-mx served noindex, empty search, no head alternates | Regional `served-draft`, separate AI review evidence, explicit false sitemap/search/indexability and `alternates.profile: none` |
| Regional `record`, `pages`, `search_index` | References historical translation records and four targets each | Route coverage plus immutable evidence references and adapter outputs |
| `i18n/sync-state.json`: `pages[route].targets[id].synced_source_sha256`, `target_sha256` | LF-normalized byte digests; detector scan compares source only, despite storing target hashes | Versioned observation baseline with separate source and reviewed-target digests; preserve algorithm ID and original JSON pointer |
| `i18n/pilot/{en-gb,es-mx}/translation-record.json`: object `language_pair`, `status: machine-drafted`, `review.complete: true`, `review.method: AI editorial review`, `review.native_or_human: false`, `review.release_accepted: false` | Draft production, AI review, and release acceptance are distinct; records have historical source revisions | `production.method: machine-drafted`; review event `method: ai`, `result: completed`; approval unestablished; publication authorization not granted by this record |
| Same: `native_review_required: false`, voice profile, dictionary, overrides, source/target paths | Historical pair settings; not a global publication waiver | Preserve settings and versioned resource references in evidence; do not override owner decision |
| `i18n/pilot/fr/review-record-2026-09-05.json` and dated fr/de/es review records | String pair, `review_status: ai-reviewed`, `native_or_human_approval: false`; route hashes/dispositions; semantic and cache-only scopes differ | Immutable review events with method, scope, original disposition, digest profile and exact route bindings; no automatic promotion to human/native approval |
| `i18n/pilot/source-hashes-murderbird-stills-2026-09-06.json`: `normalized_routes`, `source_revision`, `review_scope` | Active regional source-hash record; source revision includes descriptive suffix and is not a pure immutable SHA | Versioned regional source baseline with original revision text; parsed SHA only when actually verified; retain limitations |
| Other `source-hashes-*.json`, dated review/render records and es-MX `reviewed/*.html` | Earlier evidence plus active reviewed generator inputs | Keep original bytes/paths; evidence catalog records roles and explicit supersession, never filename-date winner selection |

Historical correction: the September 5 cleanup names
`source-hashes-release-0ee.json` as active. At this baseline both regional builder
and checker use `source-hashes-murderbird-stills-2026-09-06.json` instead. No
rename or repair of the older record is needed for T05. The old report stays
unchanged as dated evidence.

### Checker and generator contracts that must survive consolidation

| Consumer | Exact current rule to preserve or explicitly version |
| --- | --- |
| `scripts/check-i18n-release.py` | `load_results()` classifies `missing`, `stale`, `needs_baseline`; fr blocks, de/es advisory. `load_provenance()` accepts `ai-reviewed` or `approved`, rejects AI plus asserted human/native approval; accepted route dispositions are `retained-ai-reviewed`, `approved`, `no-semantic-delta-ai-reviewed`. `approved` alone does not identify the approving person or native competence. |
| Portable `i18n-page-sync.py` | `sha256_file()` replaces CRLF with LF only. `scan()` checks synced source, not reviewed target. Adoption visits missing-baseline/source-stale entries; T02 owns reviewed target-only adoption and integrity enforcement. |
| `scripts/check-locale-links.py` | `locale_specs()` supports legacy one-locale manifests. `unpublished-scaffold` requires absent targets. `validate_locale()` considers `published/released/translated` published; other extant statuses follow draft behavior. Both released and served pilot drafts require reciprocal en/x-default/locale links, self canonical and OG URL. HTML language is short fr/de/es, English is en. Published targets require sitemap and search coverage. |
| `scripts/check-regional-drafts.py` | Constants fix four routes, en-GB/es-MX tags, labels, noindex, no head alternates, zero search entries, canonical-source normalized hashes, preserved structural counts, and locale navigation/identity checks. Its manifest publication-gate fields are not a general policy interpreter. |
| `scripts/build-locale-drafts.py` | Canonical en-US input for each pair; en-GB dictionary adaptation, es-MX retained reviewed input plus English shell. Preserve dictionary, overrides and reviewed inputs. Generation is not approval. |
| Regional `normalized_translation_source()` | CRLF to LF, remove CSP meta tags, strip matching hexadecimal `?v=` fingerprints from asset href/src attributes. This is a different digest domain from detector LF hashes. Never compare the two as interchangeable. |

## Exact behavior matrix to import

Every locale covers `/`, `/about/`, `/projects/`, `/contact/`. For source route
`/`, the source path is `index.html`; otherwise it is
`<route without surrounding slashes>/index.html`. For locale ID `L`, target
route is `/L/` plus the source route without its leading slash; target path is
`L/` plus source path. These rules produce exactly 20 unique target pages.
Explicit path records must still validate against these rules.

| ID / language tag / HTML lang | Publication | Indexable / sitemap / search | Alternates | Source gate today | Reviewed-target gate today |
| --- | --- | --- | --- | --- | --- |
| fr / fr-FR / fr | released | true / true / true | pilot-reciprocal | blocking, LF profile | not enforced by detector scan |
| de / de-DE / de | served-draft | false / false / false | pilot-reciprocal | advisory, LF profile | not enforced by detector scan |
| es / es-ES / es | served-draft | false / false / false | pilot-reciprocal | advisory, LF profile | not enforced by detector scan |
| en-gb / en-GB / en-GB | served-draft | false / false / false | none | blocking regional checker, regional profile | no general reviewed-output digest comparison |
| es-mx / es-MX / es-MX | served-draft | false / false / false | none | blocking regional checker, regional profile | no general reviewed-output digest comparison |

Noindex drafts are publicly served. `served-draft` describes editorial lifecycle,
not confidentiality. `indexable` means declared eligibility, not confirmed
search-engine indexing. Alternate links and visible language-menu entries are
different surfaces; no automatic menu change follows from this matrix.

## Proposed versioned contract

Proposed future paths are `i18n/locale-policy.json`,
`i18n/locale-state.json`, and `i18n/review-events.json`. They are not created by
this PR. The policy declares `schema_version: "2.0.0"`; state and events declare
that same version and a `policy_sha256` binding. Unknown versions or fields
fail validation rather than falling through to a draft default. Minor versions
may add optional fields only; changed digest or approval semantics require a
major version. Keep legacy adapters versioned separately from the portable skill.

The following is a normative field specification, not an executable JSON Schema.
Objects reject unknown fields except the explicitly preserved `legacy_claims`.
All listed fields are required unless marked nullable. Paths are repository
relative, cannot escape the root through `..` or symlinks, and routes are unique,
slash-terminated site paths. Digests are lowercase 64-character hexadecimal.

| Object | Required fields and allowed values |
| --- | --- |
| Policy root | `schema_version`, `source_locale: en-US`, `source_registry: site-src/pages.json`, `approval_requirement`, `decision_ref` (nullable), `locales` (nonempty list), `legacy_claims` (list of original path/JSON-pointer/value references) |
| `approval_requirement` | `pending-owner-decision`, `ai-review-with-owner-release`, `human-review-with-owner-release`, or `native-review-with-owner-release`; pending forbids new publication transitions |
| Locale | `id`, `language_tag`, `html_lang`, `root`, `skill`, `routes`, `publication`, `alternates`, `checks`, `detector` (nullable), `generation` (nullable) |
| Route | `source_route`, `source_path`, `target_route`, `target_path`; all five current locale sets retain the four routes above |
| Publication | `state: absent-scaffold/served-draft/released`, boolean `indexable`, `sitemap`, `search`, `authorization_ref` (nullable), `basis: legacy-observed/explicit-owner-decision` |
| Alternates | `profile: pilot-reciprocal/none`; reciprocal means current short locale ID, en and x-default links both ways; no new tag normalization |
| Checks | Independent `source_freshness` and `target_integrity`, each `{severity: blocking/advisory/report-only, profile: digest-profile-id}`; migration initially preserves today's severity, then incorporates separately approved T02 behavior |
| Detector adapter | `config_schema: 1.0`, `search_index`, `state_file`; null for current regional generation |
| Generation adapter | `kind: regional-en-gb/regional-es-mx`, `source_baseline_ref`, `input_refs` (list); null for fr/de/es |
| State root | `schema_version`, `policy_sha256`, `observed_commit` (verified full SHA), `pages` (one record per locale/source route) |
| State page | `locale`, `source_route`, `baseline` (nullable), `observed_source`, `observed_target` (nullable if absent), `source_freshness: current/stale/unbaselined/missing-source`, `target_integrity: matches/changed/unbaselined/missing-target`, `review_event_refs` |
| Baseline | `source_digest`, `target_digest` (nullable for historical regional source-only evidence), `evidence_ref`; each digest is `{profile, sha256}` |
| Review event | `id`, `locale`, `source_route`, `source_digest`, `target_digest`, `method: ai/human/native/mixed/unknown`, `scope: semantic/interaction/generated-metadata/render/unknown`, `result: completed/rejected/incomplete/unknown`, `reviewer_ref` (nullable), `human_approval`, `native_approval`, `evidence_refs`, `supersedes` (list), `limitations` |
| Each approval | `{state: granted/not-established/denied, evidence_ref: nullable}`; granted/denied requires explicit evidence identifying authority, scope and reviewed bytes; AI method cannot grant either approval |

Evidence references contain the original repository path, JSON pointer when
applicable, and the digest of that evidence file. External source references
must be public-safe. Preserve original revision strings and unparsed legacy
fields; do not manufacture a commit or reviewer from prose. Every digest profile
must resolve to a pinned implementation/specification. Review events with
missing historical route hashes remain legacy evidence, not fabricated complete
v2 review events. A missing evidence path is reported as unavailable.

`sha256-lf-v1` means SHA-256 after CRLF-to-LF replacement only.
`sha256-regional-editorial-v1` pins the baseline regional normalization described
above. Current regional hashes cannot seed `sha256-lf-v1` target approval.
T02 must define any new target-integrity profile and negative fixtures before it
is referenced by an active policy. A digest match establishes byte integrity,
not semantic or native-language approval. No CSP/cache normalization may quietly
hide translated prose, alt text, links, or interaction-label edits.

### Before/after examples and invariants

- French `translated` plus AI evidence with `native_or_human_approval: false`
  becomes released with `basis: legacy-observed`, nullable authorization,
  AI review events, and both approvals `not-established`. This neither withdraws
  French nor invents an approval. Legacy publication is recorded, not retroactively
  justified by the new future requirement.
- de/es `drafted-pending-human-review` stays served-draft with reciprocal
  alternates. Import the exact historical policy claim; do not convert pending
  language into a completed human review.
- Regional `machine-drafted` plus completed AI review and
  `release_accepted: false` stays served-draft; AI review completion does not
  authorize release. `native_review_required: false` stays historical evidence.
- Fresh English plus edited French target yields `current` and `changed`, not
  a single `in_sync` claim. New review must bind the changed target and current
  source before target-only adoption. It cannot rewrite the earlier event.
- A metadata-only review supersedes the relevant byte baseline and points back
  to retained semantic evidence. It cannot expand the scope of linguistic review.
- No coverage import, successful check, schema upgrade or adoption mutates
  publication, sitemap/search eligibility, alternates, or approval.

## Validation fixture specification for implementation

These are required future fixtures, not tests claimed as implemented here.
Use disposable copies and distinct known source/target bytes. Assert structured
statuses, severity, exit codes, unchanged publication fields and no writes in
check mode. Suggested implementation location: `tests/fixtures/locale-policy/`.

| ID | Input or mutation | Required result |
| --- | --- | --- |
| V01 | Exact five-locale/four-route baseline | 20 unique targets; 4 released, 16 served drafts; matrix preserved |
| V02 | Unknown schema, extra field, duplicate route, root escape (four cases) | Each rejected before reading/writing outside fixture root |
| V03 | French AI review, no human/native evidence, legacy released | Import preserves release; approvals not established |
| V04 | New draft-to-released request with pending decision | Block transition; no index/alternate mutations |
| V05 | de/es versus regional draft alternates | Reciprocal pilot passes; regional alternates fail; missing pilot links fail |
| V06 | Change English only for fr, de, es | stale; fr blocking and de/es advisory under baseline policy |
| V07 | Change regional English editorial text | regional blocking stale; normalized comparison uses its own profile |
| V08 | Change French target only | source current, target changed; T02 policy determines blocking; no adoption |
| V09 | Valid reviewed target-only update | T02 adoption updates selected baseline only; old review remains accessible |
| V10 | Wrong pair, route, path, source hash or target hash (five cases) | Each rejected; no state write |
| V11 | CSP/cache-only change versus prose/alt/link/control changes | Profile-specific metadata result; every meaningful edit detected; no approval gained |
| V12 | Missing source, target, baseline or evidence (four cases) | Distinct missing/unbaselined/unavailable findings, never success by default |
| V13 | Same bytes under LF and regional digest labels | Cross-profile comparison rejected, even if hashes happen to match |
| V14 | Forged AI event asserting human/native approval | Reject; mechanical pass cannot supply evidence |
| V15 | Historical bare `approved` without identifiable approval scope | Preserve old claim; v2 approvals remain not established |
| V16 | Legacy one-locale manifest and absent scaffold | Adapter preserves coverage; scaffold requires no targets/index entries |
| V17 | Adapter round trip and two identical migrations | Exact semantic equivalence; second migration no-op; no history rewritten |
| V18 | Interrupted migration or checker failure | Atomic activation fails; prior policy/state remain usable |
| V19 | Rollback after later authorized review | Restore compatible readers/policy while retaining newer evidence files |
| V20 | A13 shared interaction strings change, page HTML unchanged | Review binds actual runtime resource revision/digest; page hash alone cannot claim reviewed interactions |

V20 requires review evidence to include shared runtime resources in
`evidence_refs`; semantic event scope and route-byte integrity remain separate.
A13 determines its exact interaction coverage. The eventual validator must not
claim those strings were reviewed solely from four unchanged HTML hashes.

## Migration and rollback sequence

1. A21 pins the actual integration SHA after T02 and A13 are settled. Re-run
   this inventory against it; record changed consumers and approved digest
   semantics. Preserve this baseline comparison as history.
2. Record the owner's future approval choice in a small decision record.
   Existing French remains observed legacy release; new locale releases and new
   semantic release updates follow the selected policy from its effective SHA.
3. Build a read-only importer and explicit v2 validator with V01-V20. Save a
   before-state inventory of all 20 targets, metadata, search/sitemap membership,
   source/state/evidence bytes, consumer versions and publication fields.
4. Produce v2 candidate files and legacy adapter outputs in an isolated staging
   directory. Missing/ambiguous review evidence remains unresolved. Compare all
   coverage and behavior; generate no translated prose or new approvals.
5. Run old and candidate readers on the same frozen fixture and checkout.
   Differences require a named T02/A13 decision, not a migration convenience.
   Regional blocking versus de/es advisory behavior must remain intentional.
6. In one separately reviewed implementation PR, activate compatible readers,
   policy and derived adapters atomically. Preserve existing evidence paths and
   hash records. Do not remove compatibility parsing until callers and legacy
   fixtures prove it unused. No dual hand-maintained policy authorities.
7. A21 runs combined structural, locale, freshness/integrity, search, generated
   HTML, CSP, regional and release checks before any separately authorized
   merge/deploy. Compare the before/after publication matrix and exact payload.
8. Rollback by reverting activation/readers and their derived adapter changes
   together to the pinned prior compatible commit. Retain append-only review
   evidence, including events created after activation. Do not blindly restore
   older state over newer approved target bytes; restore matching bytes/baselines
   as a reviewed set or keep release blocked. Validate again before publication.

## Smallest owner decision

For future semantic locale updates and first-time locale releases, may a
completed, hash-bound AI review plus explicit owner release authorization satisfy
the review requirement, or must a human/native reviewer approve the language?

Recommended proposal: `ai-review-with-owner-release`, with explicit limits and
no human/native claim. Alternatives distinguish ordinary human review from
native review rather than collapsing them. The owner chooses one requirement;
this PR does not make that choice. No retrospective withdrawal or inferred
approval of French is proposed. Generated-metadata-only updates would retain prior semantic evidence through
the proposed v2 evidence chain. T02 alone does not validate that chain or prove
the claimed metadata-only scope.

## Coordination and validation of this proposal

T02 owns executable target-integrity semantics, safe target-only adoption and
hash normalization. A13 owns French interaction strings, exact-pair linguistic
review and resource evidence. Neither needs to wait for a schema migration to
fix its bounded behavior. A21 owns integration, generated output reconciliation,
and any authorized release. T05 owns this document only. Coordination notices
were sent directly to A13 and T02. T02 confirmed compatibility and supplied
the bounded implementation details below; A13 feedback remains pending. The dispatch task
assigned PR publication sequencing to A21, so T05 first delivers a local commit.

Read-only baseline checks on September 7:

- `check-i18n-release.py --mode check --format text`: exit 0, four French pairs
  current, eight de/es source-stale advisories, no blocking items.
- `check-locale-links.py`: pass for fr/de/es, 12 target routes.
- `check-regional-drafts.py`: pass for en-gb/es-mx, eight target routes.

Document checks also verified two relative links, 20 unique manifest targets,
20 specified fixture groups, no em dashes and clean diff whitespace.

These are existing checker results, not a full review of translation quality,
new v2 tests, or proof that reviewed-target integrity is already enforced.
No live data migration, locale publication or linguistic approval occurred.

### T02 coordination update

T02 reports local commit `63e66fc911d9ae3653209d55ed07cab1daa411ef`. This is
coordination evidence, not a claim that it is merged or independently tested in
this worktree. It retains ledger v1 and CRLF-to-LF-only SHA-256 for both source
and target, including CSP and asset fingerprints. The site wrapper adds
independent `target_changed` findings (fr blocking, de/es advisory); portable
source `in_sync` lists retain their existing meaning. Explicit adoption accepts
the existing provenance labels with exact current source/target hashes and
updates only selected pairs. It does not hash shared runtime resources.

T02 does not establish semantic-evidence chaining, validate a metadata-only
scope claim, or automatically retain semantic approval. In particular, accepting
`no-semantic-delta-ai-reviewed` plus matching hashes does not independently
substantiate that review claim. Proposed v2 profile IDs and evidence links remain
future work. A21 should append verified integrated behavior to this baseline
comparison rather than relabel the portable scan as an integrity checker.
