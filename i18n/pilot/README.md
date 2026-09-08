# Locale Translation Operating Guide

This guide describes the current repository interfaces and release boundaries;
it grants no new review approval, translation certification, or publication
status.

## Scope and ownership

All five locale scopes cover `/`, `/about/`, `/projects/`, and `/contact/`.
English authoring inputs are `site-src/pages.json`, its content fragments, and
`assets/partials/`. `scripts/build-site.py` renders the English HTML used by
the detector and regional generator.

| Locale root | Exact-pair skill suffix | Current boundary | Ledger/checker |
| --- | --- | --- | --- |
| `fr/` (`fr-FR`) | `fr-fr` | Released, indexable, in sitemap | `manifest.json`; freshness failures block |
| `de/` (`de-DE`) | `de-de` | Draft, noindex, outside sitemap | `manifest.json`; source drift advisory |
| `es/` (`es-ES`) | `es-es` | Draft, noindex, outside sitemap | `manifest.json`; source drift advisory |
| `en-gb/` (`en-GB`) | `en-uk` | Regional draft, noindex, outside sitemap | `regional-drafts-manifest.json`; regional checker |
| `es-mx/` (`es-MX`) | `es-mx` | Regional draft, noindex, outside sitemap | `regional-drafts-manifest.json`; regional checker |

The manifest paths above are relative to `i18n/pilot/`. The skill identifier
retains `en-uk`; the site root and HTML language are `en-gb` and `en-GB`. All
five packages live under `.agents/skills/`. Draft pages are publicly served;
`noindex` is a search directive, not access control.

`i18n/sync.config.json` configures `fr`, `de`, and `es` for the portable
detector, with French as the blocking locale. `i18n/sync-state.json` records
those source/target baselines. Regional drafts use their own manifest and
source-hash checks; they are not additional configured detector locales.

## 1. Prepare source inputs and detect drift

Run commands from the repository root. First verify generated inputs without
rewriting them:

```sh
python3 scripts/build-site.py --check
python3 scripts/build-search-index.py --check
python3 scripts/check-i18n-release.py --mode report --format json
python3 scripts/check-i18n-release.py --mode check --format json
```

The release wrapper is the site policy boundary. Its report and check modes
are read-only. Report returns blocking and advisory findings; check exits 1
when French has `missing`, `stale`, or `needs_baseline` findings. German and
Spain Spanish findings remain advisory. Configuration or malformed policy
inputs exit 2. Neither mode drafts prose, records a baseline, or publishes
pages.

If generation is stale, the build and index commands without `--check` are
write operations. Coordinate generated-output reconciliation with the release
integrator before committing those outputs.

For a portable diagnostic, use the skill-owned detector directly:

```sh
python3 .agents/skills/okhp3-i18n-page-sync/scripts/i18n-page-sync.py --root . --mode report --format json
python3 .agents/skills/okhp3-i18n-page-sync/scripts/i18n-page-sync.py --root . --mode check --format json
```

The portable check exits 1 for missing or source-stale pages in any configured
locale, but does not apply this site's blocking-versus-advisory policy. Use the
wrapper for the site gate. The detector reports the exact-pair skill for each
flagged route.

## 2. Produce or update drafts

Use the named exact-pair skill, applying register mediation and terminology
decisions before regional translation. Skill instructions and deterministic
helpers do not themselves invoke an automatic translation model.

Regional generation is a separate write operation:

```sh
python3 scripts/build-locale-drafts.py --locale en-gb
python3 scripts/build-locale-drafts.py --locale es-mx
```

Each command regenerates four output pages under its selected locale root.
Edits made only to those outputs can be overwritten. Inputs are:

- en-GB: current generated English HTML, plus
  `i18n/pilot/en-gb/dictionary.en-us-en-uk.json` and
  `i18n/pilot/en-gb/voice-profile.en-us.json`.
- es-MX: retained HTML in `i18n/pilot/es-mx/reviewed/` (`index.html`,
  `about-index.html`, `projects-index.html`, and `contact-index.html`), plus
  current English shell inputs, `i18n/pilot/es-mx/dictionary.en-us-es-mx.json`,
  and `i18n/pilot/es-mx/voice-profile.en-us.json`. Generated `es/` and
  `es-mx/` pages are not translation inputs.
- Both: the generator's source guard currently reads
  `i18n/pilot/source-hashes-murderbird-stills-2026-09-06.json`. Keep earlier
  source records as history; do not substitute them by age.

## 3. Review and validate

Compare each draft against current English, record terminology and register
choices, and assign a review disposition in the owning review record. Preserve
the distinction between AI review and human/native approval. Then run the
read-only structural and index-freshness checks:

```sh
python3 scripts/check-locale-links.py
python3 scripts/check-regional-drafts.py
python3 scripts/build-search-index.py --locale=fr --check
python3 scripts/build-search-index.py --locale=de --check
python3 scripts/build-search-index.py --locale=es --check
python3 scripts/build-search-index.py --locale=en-gb --check
python3 scripts/build-search-index.py --locale=es-mx --check
```

Omitting `--check` from a locale index command writes
`assets/data/search-index.<locale>.json`. Draft indexes remain empty because
noindex pages are excluded; generating an index does not publish a locale.

## Page and release contract

Each in-scope locale page must use its locale HTML language, locale-specific
canonical URL, reciprocal `hreflang` links to English and the configured
locales, and the correct indexability state. French is released and listed in
the sitemap. German and Spanish remain drafts, `noindex`, and absent from the
sitemap. Locale indexes are generated separately as
`assets/data/search-index.<locale>.json`.

Useful commands:

```sh
python3 scripts/build-site.py --check
python3 scripts/build-search-index.py
python3 scripts/build-search-index.py --locale=fr
python3 scripts/build-search-index.py --locale=de
python3 scripts/build-search-index.py --locale=es
python3 scripts/check-locale-links.py
python3 scripts/check-regional-drafts.py
python3 scripts/check-i18n-release.py --mode report --format json
python3 scripts/check-i18n-release.py --mode check --format json
python3 .agents/skills/okhp3-i18n-page-sync/scripts/i18n-page-sync.py --root . --mode report --format json
python3 .agents/skills/okhp3-i18n-page-sync/scripts/i18n-page-sync.py --root . --mode check --format json
```

## 4. Adopt a reviewed baseline

Use `scripts/check-i18n-release.py`, not direct portable adoption, for this
site. After review, the recipe is:

```sh
python3 scripts/check-i18n-release.py --mode adopt --locales fr --routes /about/ --provenance "$review_record"
```

Set `review_record` to the actual reviewed JSON record covering the selected
route and current file hashes. This is an explicit-input recipe, not a command
to replay an old approval. Supply exactly one configured locale (`fr`, `de`, or
`es`) and only reviewed routes. The wrapper requires the matching language
pair, locale, target path, accepted review status and route disposition, plus
matching current source and target SHA-256 values. Accepted review statuses
are `ai-reviewed` and `approved`; accepted route dispositions are
`retained-ai-reviewed`, `approved`, and `no-semantic-delta-ai-reviewed`. An
`ai-reviewed` record cannot claim `native_or_human_approval: true`.

Adoption writes `i18n/sync-state.json`; it does not edit translated HTML or
change indexability. Target-only edits require the reviewed-target integrity
and adoption interface owned by T02. Revalidate this recipe against the
merged T02 interface before handling target-only changes; do not invent a flag
or claim target-integrity enforcement that has not been verified in the
checked-out wrapper and tests.

## 5. Publication and policy boundary

Publication is a separate reviewed PR and release step through the existing
validation and Pages workflows. Passing structural checks or adopting hashes
does not grant publication approval, native-language certification, or a new
manifest status. Preserve the existing French release and all four draft
boundaries until the owning release decision explicitly changes them.

The canonical Skillz `okhp3-i18n-page-release` v1.1.0 policy uses an
indexable-only alternate cluster. This site keeps the existing
`scripts/check-locale-links.py` adapter because it also verifies retained
German/Spanish draft pages, their `noindex` state, sitemap exclusion, and
locale-index exclusion. Do not install a second checker or delete the pilot
manifest to make drift pass. Any future policy change must map these checks
and preserve the meaning of the current state ledger first. `noindex` and draft
flags are not access control, so do not put private content in draft routes.

The shared runtime currently uses the English search index constant. Locale
indexes remain active generated artifacts until the language-specific search
behavior is decided and tested with the shared-runtime owner. Do not edit
`assets/js/app.js` in this migration cleanup.

## Evidence and history

Historical benchmarks, source hashes, and review records remain evidence of
their recorded revisions only. Their presence does not imply that the current
site has used every package or approved every locale.
The `unpublished-scaffold` compatibility branch in the locale checker remains
under separate review because it is compatibility behavior, not confirmed
dead code. No historical review claim changes here.

The local page-sync CLI help and skill examples use the actual `--mode`,
`--format`, `--locales`, `--routes`, and `--provenance` interfaces where the
site wrapper supports them. Follow up through the Skillz language-mediation
source family by comparing the portable package with its canonical source and
distributed site copies before promotion. This task does not write sibling
repositories or establish synchronized distribution. Keep generic detector
semantics portable and this site's provenance and severity policy in its
wrapper.
