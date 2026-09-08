# A15 reader orientation and contact handoff

Prepared September 7; validated September 8, 2026. **PREPARED PENDING INTEGRATION AND ACCEPTANCE.** New copy is proposed, not an approved service offer or a deployed change.

## Baseline and source scope

Actual baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`. Branch: `codex/a15-reader-orientation`. On September 8, fetched `origin/main` was `f4a353c323fc1caa848e03f6f0aa1ea1e520210c`, 23 commits ahead of the baseline. Both affected source fragments still exactly match the baseline there before these additions. This is a source comparison, not a production-SHA observation.

- `site-src/pages/contact/index.main.html`: optional problem, current process, desired result, and constraints checklist after the existing email/location block. The email remains selectable text and a mailto link. Creator support remains in its original separate section. No form, response-time promise, availability claim, or service commitment.
- `site-src/pages/writings/first-diagram-is-a-liar/index.main.html`: optional route through existing prompts, first-pass diagrams, revisions, scoring, and self-interviews. Existing jump menu, all original anchors and full article/archive remain intact. No manifesto, fiction, image, shared runtime, or project status edits.
- `tests/a15-reader-navigation.mjs`: local preview check and reproducible captures of two proposed treatments. No new dependency.

Reproduction: Contact had a working direct email but no inquiry prompts; the article had four working jump links but no annotated sequence for inspecting the experiment. Removing only the two A15-marked additions reproduces both original source files byte for byte.

## Two rendered treatments

Expanded is the source proposal: inquiry prompts remain visible; a separate article evidence card follows the existing jump menu. Compact uses the same copy in native, initially closed details disclosures. The browser check constructs compact only in memory, preserving source and URLs. The expanded treatment makes the guidance discoverable; compact reduces the added distance to the original prose. Neither has owner approval. A14 owns the homepage/shelf/detail/Contact layout alternatives; this package supplies the bounded Contact/article copy comparison without duplicating its layout work.

Eight local captures are reproducible under `.local/a15/`: `{expanded,compact}-{contact,article}-{390,1280}.png`. These generated review images are not committed. Visual inspection covered expanded phone Contact and article plus compact desktop article. Existing typography/palette and art were retained. External fonts were blocked in this deterministic run, so these captures do not certify final font appearance.

Owner task questions: Should the optional guide be visible immediately or opened on request? Does the inquiry checklist help explain a real problem without feeling like a required form? A14 must carry the chosen treatment into its selected coherent journey.

## Validation

PASS on generated proposal overlay:

- Existing source text preserved byte for byte after removing the marked additions.
- `scripts/build-site.py --check`: 36 pages.
- `scripts/build-search-index.py --check`: 161 entries. The additional article heading is discovered by the existing generator.
- `scripts/validate-site.py`: 56 pages, no errors; 32 existing locale metadata warnings and reviewed voice warnings remain.
- `scripts/check-locale-links.py`: configured French/German/Spanish structure passes.
- `git diff --check`.
- `tests/a15-reader-navigation.mjs`: Chromium 151.0.7922.34, Node 26.0.0, reduced motion, 390x844 and 1280x844, both treatments. Checks existing jump links, Enter moving focus to prompts, subsequent Tab continuing into article content, Back/Forward fragment history, unchanged mailto destination without sending, no horizontal page overflow, and keyboard expansion of compact disclosures. Eight rendered page/treatment/viewport combinations.

Initial checks were blocked by system Python missing Beautiful Soup and sandboxed browser/server startup. Generation then passed using the existing pinned QA environment; browser/server ran with approved local execution. Two early test assumptions were corrected: the footer also contains the email link, and the next keyboard control in the prompts section need not be an anchor. Final assertions scope email to main and verify document-order keyboard continuation.

Locale drift report flags Contact for fr-FR, de-DE, and es-ES; German/Spanish also have unrelated baseline drift. All five locale Contact copies require consideration after owner copy selection, including en-GB/es-MX outside that report's configuration. No locale bytes or indexing policy changed. Article translation is not part of the current four-route pilot.

NOT RUN: normal-motion regression of final integrated runtime; 320px/zoom matrix; dark-mode comparison; actual Safari/VoiceOver, NVDA/Firefox, physical phone or independent user session; external fonts/embeds; GitHub CI for a merged candidate; live deployment checks. No accessibility-conformance or user-task-success claim.

## Integration contract and remaining work

This commit intentionally carries authoritative source only, plus review tooling and this handoff. Generated HTML/search used for testing were restored to baseline afterward. Therefore freshness will intentionally fail until A21 regenerates the selected source candidate. Do not merge this branch directly or hand-merge generated files.

1. Resolved September 8: the owner selected A14 Option A, Forge front door, in the A14 task. Selection is recorded at `366fc258`; the selected implementation is `d31d55075bbe4885f38658b16a12ac305094cfe2` on `codex/a14-original-proposals-preserved`. This resolves the A14 direction dependency. It does not select an unrelated proposal also labeled A. A21 should use the visible A15 source treatment as the prepared integration default and keep the compact treatment as a reviewed alternative; neither is a separate release approval. A11 status records are on current main. Reviewed upstream content and the selected layout have not been incorporated in this A15 baseline.
2. A21 applies the selected authoritative sources on its reconciled candidate, then runs `python scripts/build-site.py` and `python scripts/build-search-index.py`. Run HTML/search/universe/CSP/cache freshness and required combined gates. No runtime fingerprint or CSP source change originates here.
3. Translate the selected Contact additions with the applicable exact-pair skills; preserve regional noindex policy.
4. Run the selected journey with A14 and final shared runtime, then A20 independent acceptance. Review actual rendered fonts and phone/zoom/dark-mode behavior.
5. Complete the authorized GitHub integration and release through A21. A source proposal on GitHub does not close these dependencies or prove deployment.

Reproduce browser review after generation with the existing Playwright dependency and a loopback preview on port 5155: `node tests/a15-reader-navigation.mjs`. Optional environment variables: `A15_BASE_URL` (include trailing slash), `A15_OUTPUT`, and `PLAYWRIGHT_MODULE` for an already installed dependency outside the worktree. The test blocks external network requests and never follows mailto.

## September 8 coordination update

A15 proposal `865025f4e6e38011a5d13396cdd0ed474e518cf0` was pushed and verified on GitHub. The owner selection above was verified from the actual A14 task message. A21 owns selected-source integration and A20 acceptance coordination. No further A14 direction choice is required from the owner; remaining work is integration, locale treatment, final validation, and the established release process.
