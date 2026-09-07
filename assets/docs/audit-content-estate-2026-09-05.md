# Content, information architecture, localization, and Git estate assessment

Assessment date: September 5, 2026, America/Chicago. Remote observations were
made September 6 UTC. This is a recommendation report; no site content, refs,
worktrees, publication settings, or translations were changed.

## Assessment boundary

The owner checkout was clean when inspected at `897df5d3`. Remote `main` was
`40e18ee7916f4a54196cc407d60999ba1d786d11`. The parent audit acquired a separate
snapshot of that remote revision. Comparing the two revisions confirms that
the intervening change is CSP discovery/policy and related translation hash
metadata, not a change to the English editorial source fragments. The source
locators below therefore apply to both revisions. Runtime and hosted behavior
belong to the parent report; a published project description is not proof that
its external application implements every described capability.

Coverage includes all 36 English source page bodies and their page metadata,
the 14 project-detail records (11 indexable plus three noindex concepts), navigation and content hubs, retained concept
routes, localization manifests and detection code, public-safe planning and
editorial records, local refs/worktrees/stashes, live remote heads, and all 27
PR records returned by GitHub. The long article's historical prompts and
diagram artifacts were inventoried and inspected as historical material;
this assessment is not a scientific replication of its experiment or a
line-by-line fact check of every external claim in the archive.

The evidence-standard and i18n-page-sync skills informed classification and
freshness interpretation. Memory was used to locate previous decisions;
findings in this report were checked against current repository evidence.
Private editorial workspace identifiers and unpublished private source
content are intentionally absent.

Machine evidence:

- `assets/audit/comprehensive-2026-09-05/content-body-inventory.json`: text
  extracted from every English source body, excluding scripts/styles. Word
  counts include diagram source and code examples, so they are content-volume
  indicators, not reading-time estimates.
- `assets/audit/comprehensive-2026-09-05/i18n-current-check.json`: read-only
  detector results for the owner checkout.
- `assets/audit/comprehensive-2026-09-05/git-content-estate.json`: current refs,
  remote heads, divergence, worktree count, stash and open-PR observations.

## Judgment

The site has unusually substantial source material, a distinctive owner voice,
and several carefully bounded project pages. Its largest content weakness is
uneven truth maintenance: one section has a precise, dated limitation while
another section advertises the same thing as complete, automatic, or ready
for production. The engineering records are richer than the visitor-facing
status system.

Keep the static architecture and the writing. Advance the solution by making
status, evidence, entry paths, and maintenance ownership consistent. A new
framework or broad copy rewrite would not resolve these problems by itself.

Strong existing elements worth preserving:

- The homepage already offers task-oriented entry paths: use a tool, inspect
  the work, and discuss a project. Build on them instead of inventing a wholly
  new positioning scheme.
- Telling Forward explicitly distinguishes a static Author App prototype
  from API/database/authenticated service surfaces. LifeTrkr says
  pre-production. BPMN describes experimental pool/lane rendering and an
  unshipped Mermaid plugin path. These are good patterns for the rest of the
  shelf.
- Skillz separates contract maturity from evidence status and explicitly
  rejects a universal production-readiness claim. The distinction is valuable.
- The Diagram writing preserves unsuccessful results, uneven experimental
  conditions, thin audience polling, and a sample-specific interpretation.
  The project companion explicitly calls ROY a heuristic. Preserve these
  qualifications when shortening or featuring the material.
- The manifesto's original passage is deliberately protected. Its family
  narrative and language are owner-authored identity, not generic copy to
  replace. The September 4 editorial review records that decision.
- Concepts are generally excluded from search/sitemaps, and newer writing
  concepts visibly say they are unpublished. Regional drafts have explicit
  publication boundaries rather than pretending hash checks prove language
  quality.

## Prioritized findings

Priority meanings: P1 is a concrete trust or task-completion correction for the
next content release; P2 improves comprehension or sustained maintenance; P3
is a measured enhancement. These are not security severity scores.

### C01  --  P1: Skillz installation guidance teaches an incomplete package shape

**Confirmed.** `site-src/pages/projects/skillz/index.main.html:663` instructs a
visitor to install a skill by downloading its raw `SKILL.md`; line 668 writes
`.agents/skills/my-skill.md`. The example explicitly contains a placeholder
URL, so the placeholder itself is not a hidden broken live link. The deeper
problem is the flat destination and file-only procedure: it omits companion
scripts, references, and assets and does not establish discovery by a named
agent. Line 225 also describes the capability asset as one file.

The [Agent Skills specification](https://agentskills.io/specification) defines
a skill as a directory containing `SKILL.md`, potentially with supporting
resources. The site's own MTB page already demonstrates complete, versioned
package installation and destination checks. That is a reusable local model.

**Consequence:** the primary discovery-to-install journey can end in a file
that looks installed but lacks resources or is not automatically discovered.

**Proposal:** replace the generic curl example with a tested installation
path for an actual public package, pin its revision, copy the complete
directory, state which client location it targets, and link to other client
instructions. Treat manual context loading as a separately labeled mode.

**Acceptance:** a fresh temporary project can follow the displayed example,
find every relative resource, load the skill in the named agent, and complete
one bounded example. Repeat execution must not silently overwrite user work.
Do not claim universal agent compatibility from one successful client test.

### C02  --  P1: Workbench status contradicts itself within one page

**Confirmed.** `site-src/pages/projects/mac-studio-local-ai-workbench/index.main.html:130`
says RAG is deployed; line 131 says the six-model strict benchmark is complete;
the May 30 timeline at line 443 repeats the result. Yet line 670 says four of
those models are not benchmarked, and lines 1001–1009 present those benchmarks
and the RAG deployment as next work. The hero is a May 30 historical snapshot,
but lower sections mix historical and current language.

**Consequence:** a reader cannot tell whether this is a restorable historical
build, today's operating machine, or a plan. It undermines the very evidence
discipline the page sells.

**Proposal:** explicitly frame the article as the May 2026 build journal,
retain original dated test tables, add a clearly dated current-state summary,
and mark superseded next steps as completed or historical only after checking
their source records. Preserve the distinction between stored model inventory
and models with routing logic; `.agents/memory/project-page-stat-sources.md`
already explains why those counts differ.

**Acceptance:** no item appears both as currently shipped and currently
pending; every benchmark specifies date, model/runtime, prompt conditions,
result source, and limitation. A new full-machine audit is a separate task,
not implied by editing this website.

### C03  --  P1: Prototype boundaries disappear on the project shelf

**Confirmed.** `site-src/pages/projects/index.main.html:32` describes the whole
shelf as shipped and maintained. Its Telling Forward card (line 117) describes
the platform's intended behavior without the prototype qualification present
on its detail page. The LifeTrkr and BPMN cards likewise omit the prominent
maturity boundaries available after clicking. `site-src/project-status.json`
contains only Skillz and ARE; a second two-card status section is appended
below the larger shelf at line 161.

**Consequence:** the visitor must infer maturity from inconsistent prose or
open each project. The two-card proof section can suggest that only those two
have evidence, without explaining the selection rule.

**Proposal:** extend one project registry to all 14 detail records and the
intentional concept exceptions. Separate editorial availability, software
maturity, and delivery verification. Examples: `Published case study`,
`Prototype`, `Pre-production`, `Live tool`, `Concept`; a separate checked date
and evidence link describe what was actually verified. Render the same badges
on the shelf, hero, and relevant search result.

**Acceptance:** every listed project has an owner-approved status, primary
next action, reviewed date, and evidence/limitation. One registry change
updates all generated surfaces. Preserve explicit unknowns instead of
manufacturing missing dates or runtime proof.

### C04  --  P1: Three retained concept pages lack a visible draft boundary

**Confirmed.** `/projects/hometools/`, `/projects/pathscrib-r/`, and
`/projects/un-nocked-truth/` have `noindex, nofollow`, but their generated body
content has no visible draft/concept notice. Homestead-R and PathScrib-R
describe operational capabilities in present tense; Un-NOCKed Truth says
there are already several GPTs but supplies no direct launch/proof path.
The source fragments are respectively 108, 113, and 138 extracted words.
`/writings/biases-as-constants/` and `/writings/magnus-saga/` already show a
clear visible unpublished notice, so the inconsistency is avoidable.

**Consequence:** a direct-link visitor sees a product description without
knowing whether it is an idea, usable tool, or retired experiment. `noindex`
is crawler metadata, not a visitor explanation or access restriction.

**Proposal:** add a static, visible concept notice and a useful next step,
with capabilities labeled planned unless a real public destination supports
them. Preserve these routes and their history until an owner disposition.

**Acceptance:** with JavaScript disabled, each page identifies its current
state and provides a valid next action; metadata/search exclusion remains
intentional. No speculative GPT is invented to fill an empty button.

### C05  --  P1: A commercial-use FAQ oversimplifies Apache license obligations

**Confirmed.** `site-src/pages/projects/found-ry/index.main.html:619` says the
repository is Apache-2.0 licensed and that attribution is appreciated and not
required. The [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0)
includes redistribution obligations to retain relevant notices and provide
the license; a supplied NOTICE file also has requirements. A blanket sentence
about attribution can mislead a reader who is redistributing the repository.

**Proposal:** distinguish optional promotional credit from license/notice
retention and link directly to the repository license. Keep exported
specifications and third-party material separate from repository code rights.

**Acceptance:** the FAQ accurately summarizes the governing license without
claiming that all uses, dependencies, generated documents, or redistribution
conditions are identical. This is a content correction, not a legal opinion
on any particular visitor's use.

### C06  --  P1: Several automatic-success and influence claims exceed the evidence shown

**Confirmed wording, inferred trust risk.** Examples:

- BPMN line 348: valid first-try output and no syntax repair loops, despite an
  explicit prototype parser and experimental features elsewhere.
- MTB user guide: scaffolds produce on-brand results from the first
  generation with no follow-up styling cycles; the FAQ also says exports work
  anywhere Mermaid is used despite preceding renderer limitations.
- Prompt Forge anatomy says these elements distinguish prompts that work
  once from prompts that work every time. The GPT Interrogation section says
  self-description turns black-box assistants into auditable systems.
- BFS correctly identifies an independent public-information prototype, but
  still claims early teaching of a model wins influence and that the lens can
  secure a brand's story in the wider model ecosystem. A custom GPT's scoped
  knowledge does not, by itself, demonstrate that outcome elsewhere.
- The homepage describes every project as stress-tested and ready to plug
  into a daily stack (`site-src/pages/index.main.html:155`). This conflicts
  with the site's careful prototype and maturity disclosures.

**Proposal:** keep the author's confident, practical voice but bind outcomes
to conditions: designed to reduce repair cycles; test in the target renderer;
self-report is an audit input requiring corroboration; this prototype
demonstrates a controlled reference experience rather than proved influence
over unrelated systems. Preserve the BFS unofficial notice already added.

**Acceptance:** each measurable claim links to a versioned test or is clearly
labeled design intent, observation, or hypothesis. No unbounded guarantees
remain in cards, metadata, or FAQ where the detail page supplies a limitation.

### C07  --  P2: Homepage freshness is manually maintained and already inconsistent

**Confirmed.** `site-src/pages/index.main.html:103` labels Diagram v0.5 the
most recent thing to go public. `site-src/pages/writings/index.main.html:36`
features the newer MurderBird story, published September 5. The homepage's
selected-work review date and its separate latest-writing block have different
maintenance mechanisms.

**Proposal:** distinguish `Featured` from `Latest`. An editorial feature can
remain Diagram v0.5 indefinitely; a latest feed should derive ordering from
publication metadata. Add modified/reviewed dates only when their meanings
are explicit; do not rewrite historical publication dates to appear fresh.

**Acceptance:** one newly published writing updates the intended latest
surface, while an explicitly curated featured item stays stable. Shared
banners, titles, and version labels are consistent with the chosen release.

### C08  --  P2: Localization is mechanically stronger than its operating documentation

**Confirmed.** The configured detector reports all 12 fr/de/es route pairs in
sync, with zero missing/stale/baseline/orphan entries. The locale-link checker
passes. French is marked reviewed/indexable; German and Spain Spanish remain
drafted pending human review. en-GB and es-MX are separate AI-reviewed drafts
with four routes each, `noindex`, empty public search indexes, and no public
alternate cluster.

The regional routes are not in the page-sync configuration, but this is **not
an unmonitored freshness hole**: `scripts/check-regional-drafts.py` checks
normalized English source hashes and is wired into validation. Its separate
policy should be documented instead of replaced blindly.

`i18n/pilot/README.md` still says the shared runtime uses the English index
until locale search is decided. `assets/js/app.js:589` already selects the
French index. Search UI strings at lines 720–731 remain English even when
French results are used. German/Spanish fallbacks explicitly search English.
The README's three-locale operating scope also does not describe the newer
regional draft workflow. English and French head alternates include the
retained de/es noindex drafts, while the newer regional draft policy excludes
drafts from alternate clusters.

**Proposal:** document the actual two workflows, translate search controls,
status announcements, empty/error states, and scope labels for released
French, and deliberately converge alternate-cluster policy. Google requires
reciprocal alternate links; it does not make mixed draft/public policy a
substitute for a clear release decision. See [Google's localized-page
guidance](https://developers.google.com/search/docs/specialty/international/localized-versions).

**Acceptance:** the guide matches implementation; French has a complete
search microcopy journey; all 20 localized routes have named review and
freshness ownership; draft promotion is separate from hash adoption. Preserve
regional pair-specific review and no-native-certification boundaries.

### C09  --  P2: Project pages need a consistent short route through the evidence

**Confirmed structure; proposed UX change.** Project source bodies range from
108 to 4,601 extracted words. MTB, Skillz, Found-Ry, and the Mac journal contain
substantial detail; long-form content is appropriate but a new visitor must
work through many overlapping feature, scope, principles, origin, roadmap,
FAQ, and ecosystem sections. The project shelf offers 11 internal cards,
three external/library entries, and a repeated proof subsection. A user
trying a tool and a prospective collaborator need different reading depths.

**Proposal:** keep complete evidence under stable anchors, but standardize the
first viewport and summary: what it does, who it is for, current status, one
primary action, an example output, privacy/storage boundary, and known limits.
Provide secondary paths to evidence, build history, and related tools. Treat
long diagrams and archives as optional depth. The First Diagram writing
already has a detailed navigation structure; improve its reader orientation
before splitting it or moving URLs.

**Acceptance:** representative new visitors can identify a usable tool, tell
prototype from service, locate a result/example, and reach an inquiry path
without needing ecosystem vocabulary. Use task observation, not only click
counts or a stylistic opinion, to judge the revision.

### C10  --  P2: Maintenance documents do not identify supersession consistently

**Confirmed.** `ROADMAP.md:14` still proposes removing inline CSP patterns
superseded by current CSP generation; line 25 postpones analytics disclosure
already present in legal copy; line 24 proposes a public prompt library while
the Prompt Vault already offers a template. `i18n/pilot/README.md` contains
the search mismatch described above. Historical P3 and baseline/history
handoffs contain old unresolved checks and worktree counts, while the newer
infrastructure closeout records their dispositions.

**Proposal:** give active planning one small status index with last-verified
revision, owner, completed/pending/superseded disposition, and a link to the
evidence. Preserve historical reports intact with a pointer to their
successor. Do not let an agent treat an old pending sentence as a fresh defect
or re-open work already proved complete.

**Acceptance:** a reader can locate the current roadmap and release status in
one navigation step; finished work is no longer planned; historical records
remain recoverable. The parent infrastructure report should reconcile the
older Replit publication procedure with the current safe release contract.

### C11  --  P2: The private/prototype-to-public boundary needs an explicit editorial checklist

**Confirmed.** Telling Forward and Diagram companion pages carefully separate
public narrative, code, prototype services, and story rights. Prompt Forge
labels some systems internal or private enterprise patterns. The About
credentials have a dated owner-approved public-safe review in
`docs/editorial-review-2026-09-04.md`; they should not be replaced merely
because an auditor did not retrieve a private source. The Mac journal,
however, carries machine-specific paths and topology details that provide
little reuse value without context.

**Proposal:** require a short editorial preflight for public project updates:
availability, dates, evidence, rights, external service boundary, and whether
internal details improve the reader's task. Generalize implementation paths
in reusable guides, preserve source provenance in its proper private context,
and avoid claiming that a source archive is a service. Do not broaden this
into unsolicited deletion of the author's personal narrative.

**Acceptance:** public pages contain only intentionally shareable material;
every external-service CTA distinguishes live, intended, or unavailable;
privacy and license claims are scoped to the right surface.

### C12  --  P3: SEO polish should follow accuracy and user tasks

**Confirmed foundation:** the English page registry has specific titles,
descriptions, canonical paths, and explicit indexability decisions. Both
concept writings are appropriately excluded. Social image shapes are mixed,
including square assets and 1536×1024 images; a dedicated landscape social
card can improve composition, but a non-1200×630 image is not inherently a
standards defect. Search Console/Bing submission and actual query performance
were not verified here.

**Proposal:** first align metadata with actual maturity: the Mac description
says build complete; BPMN's description can be clearer that this is a
prototype/contribution proposal. Give Vault metadata the same one-download
plus-planned-materials boundary as its visible body. Then preview social cards
for the homepage and highest-value writing/project routes. Prune redundant
metadata only through the generator, after confirming it serves no current
consumer. Do not add structured-data claims for reviews, products, or
organization facts that the visible content cannot support.

**Acceptance:** metadata accurately represents the destination; canonical,
alternate, and sitemap checks pass; social titles remain readable in actual
platform previews; discoverability improvements have measured outcomes. A
technical SEO pass does not prove indexing or ranking.

## Complete route disposition

The following are source/content observations, not external application
certifications. Counts exclude shared navigation, scripts, and styles but
include code/diagram text. `Index` describes the English page registry.

| Route | Index | Content role / present state | Next editorial action |
| --- | --- | --- | --- |
| `/` | Yes | Orientation, featured work, two concept teasers; 697 words | C03/C06/C07; preserve task-oriented entry paths |
| `/about/` | Yes | Personal professional introduction; 524 words | Preserve approved credentials and first-person voice; add only verified public evidence links |
| `/contact/` | Yes | Direct email and creator support; 333 words | Keep inquiry and donation purposes visually distinct; concise optional inquiry prompts |
| `/legal/` | Yes | Privacy, terms, analytics, accessibility; 443 words | Keep claims synchronized with real runtime behavior; parent security review applies |
| `/manifesto/` | Yes | Living manifesto and protected origin; 5,312 words | Preserve original; improve reading/orientation only with owner-voice review |
| `/projects/` | Yes | Project shelf and duplicated two-card proof section; 531 words | C03/C09 |
| `/projects/abrahamic-reference-engine/` | Yes | Active v1.1 tool description, sources and external app; 1,176 words | Check external API/version claims at each project update; retain scope and text rights |
| `/projects/bfs-framing-intelligent-futures/` | Yes | Independent unofficial public-information GPT prototype; 1,444 words | C06; separate demonstrated lens behavior from broader market thesis |
| `/projects/bpmn-for-mermaid/` | Yes | Prototype parser/SVG playground, 15-skill suite, unshipped plugin path; 2,585 words | C03/C06; consistent shipped versus planned language |
| `/projects/first-diagram-is-a-liar/` | Yes | Writing companion, tutorial route explicitly unverified, evidence archive; 1,038 words | Verify route before upgrading delivery label; retain heuristic and rights boundaries |
| `/projects/found-ry/` | Yes | Described live design workbench, browser local storage; 3,244 words | C05/C09; distinguish rubric completion from tested GPT quality |
| `/projects/glee-fully-chai-chasers/` | Yes | Free browser game and multi-agent case study; 1,369 words | Preserve storage-partition notice, fictional-currency boundary, dated math evidence |
| `/projects/hometools/` | No | Homestead-R concept; 108 words | C04; name planned capabilities and useful next step |
| `/projects/kierans-lifetrkr/` | Yes | Pre-production v0.1.10, client-only app and optional integrations; 690 words | Preserve pre-production and fallback boundaries on cards |
| `/projects/mac-studio-local-ai-workbench/` | Yes | May 2026 build journal with conflicting current/pending state; 3,715 words | C02/C11 |
| `/projects/mermaid-theme-builder/` | Yes | Described shipped v0.6.1 workbench, renderer restrictions, full-package install; 4,601 words | Preserve install hardening; C06/C09; verify version drift before editing counts |
| `/projects/pathscrib-r/` | No | Narrative-suite concept without visible draft notice; 113 words | C04; decide relationship to Telling Forward without assuming replacement |
| `/projects/skillz/` | Yes | Live discovery app; contracts explicitly vary in maturity; 3,629 words | C01/C09; keep generated catalog and evidence status distinction |
| `/projects/telling-forward/` | Yes | Early concept/prototype; static app separate from services; 1,245 words | Carry the same boundary onto shelf and previews |
| `/projects/un-nocked-truth/` | No | Archery ecosystem concept, existence claims without launch links; 138 words | C04; do not invent safety/tool availability proof |
| `/prompt-forge/` | Yes | Six named methods, some internal/private, reusable public skeleton; 2,085 words | C06; make public-use versus conceptual paths explicit |
| `/vault/` | Yes | One downloadable protocol template plus planned resources; 293 words | Align metadata; add resources only when actually packaged |
| `/universe/` | Yes | Brand/ecosystem diagram and supporting explanation; 915 words | Keep an optional map, not a prerequisite to using the site; synchronize lifecycle labels |
| `/writings/` | Yes | Two released works and two visible concept cards; 194 words | Preserve separate fiction/research/status signals; C07 |
| `/writings/murderbird/` | Yes | Fictional origin story and visual record; 2,639 words | Keep fiction label and three-era structure; no requirement to turn fiction into technical claims |
| `/writings/first-diagram-is-a-liar/` | Yes | v0.5 argument, experiments, prompts, historical posts, diagrams; 18,481 extracted words | Preserve sample qualifications and original artifacts; offer a short guided entry |
| `/writings/first-diagram-is-a-liar/v03/v1-heat-a/` | Yes | Archived first-pass comparison, closed poll context; 1,300 words | Retain source/render pairs and experimental conditions |
| `/writings/first-diagram-is-a-liar/v03/v1-heat-b/` | Yes | Archived first-pass comparison; 879 words | Same; clear route back to current argument |
| `/writings/first-diagram-is-a-liar/v03/v2-heat-a/` | Yes | Revised comparison; 1,710 words | Same; preserve round and role boundaries |
| `/writings/first-diagram-is-a-liar/v03/v2-heat-b/` | Yes | Revised comparison; 1,746 words | Same; avoid reading rhetorical diagram text as validated research |
| `/writings/biases-as-constants/` | No | Visible research draft notice; 95 words | Preserve; add a real abstract/evidence packet only when ready |
| `/writings/magnus-saga/` | No | Visible unpublished fiction concept; 96 words | Preserve; publish intentional excerpts only after rights/editorial decisions |
| `/found-ry/` | No | Intentional moved-route redirect; 51 words | Preserve continuity and canonical destination |
| `/search/` | No | Search utility; 44 words | C08; preserve explicit scope and accessible error/empty handling |
| `/404.html` | No | Recovery utility; 142 words | Retain working recovery links; wording should identify a missing page clearly |
| `/under-construction.html` | No | Generic holding page; 140 words | Keep intentional utility status; do not use as proof that the whole site is unfinished |

## Git and historical work disposition

**Confirmed at inspection:** one live remote branch (`main`), zero open PRs,
two local worktrees, no stashes in this clone, and three local branches. The
27 returned PRs comprise 25 merged and two closed unmerged. The two closed
records are #14 (P1 correction work) and #16 (explicitly superseded regional
candidate); neither is an instruction to revive an abandoned branch.

| Local item | Observed relationship | Recommendation |
| --- | --- | --- |
| `main` at `897df5d3` | Behind live remote CSP closeout at `40e18ee7`; cached `origin/main` also old | Reconcile by a reviewed fast-forward during implementation, after preserving any audit files. Do not mistake cached parity for remote parity. |
| `backup/main-before-reconcile-2026-08-31` at `674376b2` | Ancestor of inspected local HEAD: 122 commits behind, zero ahead | Preserve recovery purpose; no product backlog inference from branch name. |
| `codex/repair-site-validation-i18n` at `50629090` | Clean linked worktree; two commits not ancestors of local main; PR #10 merged | Compare patch equivalence and record owner disposition before any cleanup. Squash integration can leave unique commit IDs without unique product work. |
| Cached `origin/codex/*` and Dependabot refs | Eight feature/bot refs remain cached although `ls-remote` returns only main | Refresh/prune only in a separately authorized maintenance action. Do not assess these as live unmerged branches. |

Older reports mention six stashes, many worktrees, preservation/archive refs,
and Windows cleanup. Those historical observations must not be transplanted
onto this Mac clone. No `refs/archive` entries were returned here. That does
not prove work was lost: machine, clone, and date boundaries differ. The
reports preserve context and should remain historical evidence.

Current author work has substantive value: the MurderBird story/assets are
now on main, regional variants have explicit draft status, and PR #28 repairs
release CSP discovery. An apparent pile of old refs is not a reason to merge,
squash, or delete content. No branch operation was performed in this audit.

## Execution packages

### Consequential claim ledger

| Claim | Tier | Evidence | Consequence if false | Next check |
| --- | --- | --- | --- | --- |
| C01: the displayed installation uses a flat, incomplete package shape | Confirmed source; discovery failure inferred | Skillz source lines 663-670; Agent Skills specification | An unnecessary installer rewrite could replace a supported client mode | Fresh-project install and named-agent activation test |
| C02: current and pending work conflict | Confirmed | Mac source lines 130-131, 443, 670, 1001-1009 | Historical evidence could be incorrectly overwritten | Reconcile dated source records; retain dated historical table |
| C03: registry covers two of fourteen detail pages and shelf hides some maturity boundaries | Confirmed | Project registry and shelf; prototype detail pages | A deliberately narrow featured registry could be expanded without need | Approve complete status model and determine whether to extend or rename registry |
| C04: three noindex concepts lack a visible status notice | Confirmed source | Both source and generated concept bodies | Duplicate notices could be added if runtime supplies one | Browser/no-JavaScript review of the three routes |
| C05: Apache FAQ wording is overly broad | Confirmed wording; editorial/legal interpretation | Found-Ry line 619 and Apache license section 4 | Replacement wording could imply obligations on unrelated exported content | Verify repository LICENSE/NOTICE and scope revised FAQ |
| C06: absolute success and influence language lacks linked evidence for those broad outcomes | Confirmed wording; trust impact inferred | Specific source examples in C06 | Intentional rhetoric could be stripped from owner voice | Owner review plus version-matched evidence for measurable claims |
| C07: latest homepage item differs from newer published writing | Confirmed | Homepage lines 103-114 and September 5 MurderBird page | Intended feature selection could be mistaken for chronological ordering | Choose Featured versus Latest label and test metadata ordering |
| C08: localization checks pass but operating guide and runtime diverge | Confirmed within checked snapshot | Detector JSON, checker result, guide, app.js 589 and 720-731 | Working policy could be replaced with weaker checks | Verify French interaction and map both locale workflows before edits |
| C09: shorter project entry paths would improve comprehension | Proposal | Content volumes and repeated section structure | Shortening could hide useful evidence or harm expert readers | Observe representative visitor tasks with current and proposed layouts |
| C10: active-looking planning documents contain completed work as future work | Confirmed | ROADMAP lines 14-25, legal source, current CSP, locale guide | Historical records could be falsely treated as actionable | Add current status index and supersession links, preserving history |
| C11: a public editorial preflight would reduce boundary drift | Proposal | Strong existing Telling Forward/Diagram examples and varied page detail | Overbroad rules could erase deliberately public personal writing | Owner-approved scope; review only new public-facing updates |
| C12: accurate metadata and social previews are worthwhile next SEO work | Proposal; indexing impact unknown | Page registry, mixed image shapes, no search-console retrieval | Effort might not improve real discovery | Inspect search performance and actual platform previews |
| Current remote has one branch and zero open PRs | Confirmed at retrieval | git-content-estate.json and GitHub PR query | Cleanup or backlog judgments could target stale state | Re-read remote immediately before any future maintenance action |
| External app functionality, native-language quality, and conversion gains are established | Unknown; not claimed | No comprehensive external-app audit, native-review observation, or analytics dataset in this subtask | False public reliability or business-success claims | Run the specific external, editorial, or measurement checks first |

Each package should start from the chosen current remote SHA in an isolated
checkout. One integrator owns generated outputs and merges them after source
reviews, avoiding repeated search-index and shared-shell conflicts.

| Package | Suggested owner | Inputs and scope | Required acceptance |
| --- | --- | --- | --- |
| E1: Correct visitor trust failures | Codex or Copilot, owner editorial review | C01, C02, C04, C05, bounded C06 source fragments | Complete install smoke test; no contradictory maturity; visible concept labels; license summary aligned; generated HTML/search/CSP/locale gates |
| E2: Complete status registry | Codex architecture pass, then Copilot implementation | C03; project schema, cards, detail summaries, search metadata | Every project represented; statuses distinguish editorial/software/delivery; no invented evidence; consistency fixture |
| E3: Reader and project entry design | Replit isolated visual proposal; owner selects | C07/C09, existing brand tokens, canonical sources, representative long pages | Task-based review on mobile/desktop; no path deletion; owner voice retained; accessible navigation and stable anchors |
| E4: French journey and locale governance | Exact-pair skill plus qualified reviewer; Codex shell integration | C08; runtime microcopy, two localization ledgers, alternate policy | Reviewed French strings and announced states; all locale gates; no draft promotion by hash adoption alone |
| E5: Maintenance and metadata reconciliation | Copilot bounded documentation/fixture PR | C10/C11/C12; active docs and generator metadata | Current versus historical records unambiguous; public-safe locators; accurate social/meta preview; no unsupported schema claims |
| E6: Measure whether the changes help | Owner plus Codex instrumentation review | Baseline inquiry/tool-launch/download paths and opt-in task sessions | Written metric definitions, privacy scope, reproducible before/after observations; no claimed conversion gain without data |

Order E1 before broad visual work. E2 and documentation preparation can run
in parallel on separate files; E3 consumes the settled status model. E4 must
follow final English copy for its four routes. One release integrator runs
the full structural/browser suite on the combined artifact and verifies the
deployed revision. A worker finishing its files is not release completion.

Unknowns that need evidence before stronger claims: real inquiry conversion,
search-query success and traffic, external project functional completeness,
current machine benchmark reproducibility, native-language review quality,
search-engine indexing, and whether a prospective visitor understands the
brand vocabulary. The next checks are task observation, source-specific
project verification, and owner-approved analytics review -- not speculative
replatforming or broad branch cleanup.
