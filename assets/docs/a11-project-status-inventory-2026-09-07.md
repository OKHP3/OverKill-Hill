# A11 project status inventory

Source inspection: September 7, 2026. Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`.

Disposition: inventory complete; registry implementation held for A06 truth reconciliation. This is a dated audit, not a second status authority. No published status, source fragment, metadata, or generated output was changed. A01/A02 are committed in this baseline; the advancement plan's earlier uncommitted description is historical.

## Reproduced finding

`site-src/project-status.json` contains two records, Skillz and Abrahamic Reference Engine. `scripts/check-project-status.py` passes with `Project status registry valid: 2 records`. It checks matching cards on the homepage, Projects, and Universe, but does not require coverage of detail pages or shelf exceptions. It does not check software maturity separately from page availability or delivery evidence.

Neither `scripts/build-site.py` nor `scripts/build-search-index.py` reads that registry. Source fragments repeat the two status cards manually. Search uses HTML metadata and extracted text. A passing checker therefore proves consistency of the two selected cards only. `scripts/build-site.py --check` passes for 36 English generated pages at this baseline.

## All 14 detail pages

Every row below is CONFIRMED as a source observation, not confirmation that an external application works today. Source paths are relative to the repository. For each slug, inspect `site-src/pages/projects/<slug>/index.main.html`; indexing is read from `projects/<slug>/index.html`. "Shelf" means a card in the main Built at the Hill section of `site-src/pages/projects/index.main.html`.

| Detail slug | Page availability in committed HTML | Shelf | Current source label or limitation | Delivery evidence boundary / next check |
| --- | --- | --- | --- | --- |
| abrahamic-reference-engine | Indexable detail | Yes | v1.1 Active | Source and launch links exist; fresh functional delivery UNKNOWN. Reconcile dated release evidence before treating Active as maturity. |
| bfs-framing-intelligent-futures | Indexable detail | No | Independent prototype; evolved into AskJamie BrandGuard; not an official corporate product | Public-information prototype, not a client-delivery claim. Preserve affiliation limits; verify any external delivery claim separately. |
| bpmn-for-mermaid | Indexable detail | Yes | Active; hand-written prototype parser; not a production Mermaid plugin | Playground link is not proof of production-plugin maturity. A06 must qualify outcome language; retain experimental rendering limits. |
| first-diagram-is-a-liar | Indexable detail | Yes | Writing Companion; Interactive Tutorial; Evidence Archive | Public narrative and tutorial are different surfaces. Test the tutorial separately from the existence of the writing/archive. |
| found-ry | Indexable detail | Yes | Live; Browser-Only | Launch/source links and capability prose exist; current tool function UNKNOWN. A06 owns rights and outcome qualification. |
| glee-fully-chai-chasers | Indexable detail | Yes | Current build; Zero Backend | Play/source/governance links exist; current game function UNKNOWN. A link or build label alone is not acceptance. |
| hometools | Noindex, nofollow detail | No | Homestead-R capability prose; no visible concept label | A06 must supply visible concept notice and planned wording. Public product delivery UNKNOWN. |
| kierans-lifetrkr | Indexable detail | Yes | Pre-production / v0.1.10; external integration and handoff gates still being verified | Shelf omits pre-production qualification. Current integration acceptance UNKNOWN; retain explicit limit. |
| mac-studio-local-ai-workbench | Indexable journal | Yes | Baseline complete May 12; updated May 30; complete and pending statements coexist | A06 must reconcile dated completion and historical pending work. Journal availability does not establish current workstation health. |
| mermaid-theme-builder | Indexable detail | Yes | v0.6.1 Shipped; Agent Skill Family Shipped | Source labels describe release claims; fresh app and skill-family acceptance UNKNOWN. Preserve separate artifact scope. |
| pathscrib-r | Noindex, nofollow detail | No | PathScrib-R capability prose; no visible concept label | A06 must supply visible concept notice and planned wording. Public product delivery UNKNOWN. |
| skillz | Indexable detail | Yes | Skillz Forge Live; Active Build | Catalog availability differs from individual package maturity and client activation. A05 install evidence is a further input for any installation proof claim. |
| telling-forward | Indexable detail | Yes | Prototype Seed; Active Build; static Author App; API/database/authenticated writes remain separate | Shelf omits static-prototype/service boundary. Do not label the complete platform shipped from the static deployment. |
| un-nocked-truth | Noindex, nofollow detail | No | Early-stage capability prose; no visible concept label | A06 must supply visible concept notice and planned wording. Public product delivery UNKNOWN. |

Counts: 14 detail pages, 11 indexable, three noindex; 10 details represented on the main shelf, four absent. These counts describe this baseline, not constants for future validation.

## Shelf exceptions

The shelf contains 14 cards across Built at the Hill and External Tools & Platforms, plus two repeated Status and proof cards. Its four entries without a `/projects/<slug>/` detail are intentional route/type exceptions:

| Entry | Target | Treatment proposed for the registry |
| --- | --- | --- |
| Prompt Forge | `/prompt-forge/` | Local workshop/resource hub; no invented software release maturity. |
| Glee-fully Personalizable Tools | `https://glee-fully.tools/` | External sibling site; availability and acceptance require separate evidence. No sibling writes. |
| AskJamie | `https://askjamie.bot/` | External sibling site; availability and acceptance require separate evidence. No sibling writes. |
| Protocol Libraries | `mailto:contact@overkillhill.com` | Access inquiry, not a public application or verified downloadable library. |

The four detail exclusions are BFS, Homestead-R, PathScrib-R, and Un-NOCKed Truth. Preserve their existing URLs and visibility decisions. Record exclusions explicitly rather than automatically promoting them onto the shelf. Do not equate noindex with access control.

## Proposed implementation contract after A06

Extend the existing `site-src/project-status.json`, with explicit schema migration, rather than adding another registry. Separate editorial availability, software/artifact maturity, and delivery evidence. Each evidence claim should carry a source, observed date, scope, and tier; unknown evidence stays explicit. Existing version labels are claims to reconcile, not automatically verified current release versions. A review date must identify what was actually reviewed.

Have the generator render compact detail summaries and applicable shelf cards from that record. Use explicit markers so repeated generation is idempotent. Preserve narrative history and anchors. Replace the broad shelf assertion that all entries are shipped and maintained with wording supported by the reconciled records. Do not turn long-form historical claims into current status facts.

Search should receive the same applicable availability/maturity wording through generation or registry-aware metadata, while retaining current noindex exclusions. Coordinate its generator changes with A04 and preview metadata with A12. Universe contains the existing two status cards as well as generated index-driven navigation; preserve its owning generator and canonical skill package.

Replace substring-only coverage with validation that inventories actual detail routes and declared shelf exceptions, checks unique IDs/routes, validates evidence references and explicit unknowns, and verifies generated summaries agree with the records. Meaningful regressions should reject a missing detail, duplicate route, undeclared shelf exception, unsupported proof state, and a stale card/detail/search summary. Do not infer runtime delivery from registry validation.

## Evidence and remaining gates

| Claim | Tier | Evidence | Consequence if false | Next check |
| --- | --- | --- | --- | --- |
| Existing registry covers only two projects | CONFIRMED | `site-src/project-status.json`; passing checker output | Coverage work could be redundant | Recheck after upstream reconciliation. |
| Fourteen details and four shelf-only entries exist | CONFIRMED | Parsed source fragments, generated robots metadata, Projects shelf | Missing records or accidental publication | Add dynamic coverage tests when implementing. |
| Registry is not a build/search input | CONFIRMED | `scripts/build-site.py`, `scripts/build-search-index.py`, registry-reference search | A second rendering path could be introduced | Extend existing generation entry points. |
| Proposed separated fields will resolve C03 | PROPOSAL | Consumer inventory above | New labels could repeat unsupported claims | Review A06 facts, then implement and test against all consumers. |
| A06 truth reconciliation is ready | UNKNOWN | No verified upstream commit supplied during this inventory | Implementation could publish conflicting status | Obtain A06 commit, inspect source diff and its evidence before dependent edits. |
| External applications are currently usable | UNKNOWN | External functional tests did not run | Visitors could receive false delivery assurance | Perform scoped dated checks only for claims selected for registry inclusion. |

No browser, locale, external functional, CI, deployment, or live-byte acceptance is claimed. This documentation-only checkpoint needs no generated-file refresh. A21 remains the sole integration/publication owner. Resume A11 with the verified A06 contract; A11 is not complete at this checkpoint.
