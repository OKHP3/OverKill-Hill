# Locale Translation Operating Guide

Verified against `98922aebf71d90b2b18ecc34c8b00a041fff51c7` on September 7,
2026. This guide describes existing interfaces; it grants no new review
approval or publication status.

## Scope and ownership

All five locale scopes cover `/`, `/about/`, `/projects/`, and `/contact/`.
English authoring inputs are `site-src/pages.json`, its content fragments,
and `assets/partials/`. `scripts/build-site.py` renders the English HTML
used by the detector and regional generator.

| Locale root | Exact-pair skill suffix after `okhp3-translation-en-us-` | Current boundary | Ledger/checker |
| --- | --- | --- | --- |
| `fr/` (fr-FR) | `fr-fr` | Released, indexable, in sitemap | `manifest.json`; site freshness failures block |
| `de/` (de-DE) | `de-de` | Draft, noindex, outside sitemap | `manifest.json`; source drift advisory |
| `es/` (es-ES) | `es-es` | Draft, noindex, outside sitemap | `manifest.json`; source drift advisory |
| `en-gb/` (en-GB) | `en-uk` | Regional draft, noindex, outside sitemap | `regional-drafts-manifest.json`; regional checker |
| `es-mx/` (es-MX) | `es-mx` | Regional draft, noindex, outside sitemap | `regional-drafts-manifest.json`; regional checker |

The two manifest paths above are relative to `i18n/pilot/`. Skill identifiers
retain `en-uk`; the corresponding site root and HTML language are `en-gb`
and `en-GB`. All five packages live under `.agents/skills/`.
Draft pages are publicly served; noindex does not provide access control.

`i18n/sync.config.json` configures only `fr`, `de`, and `es` for the portable
detector, with French as the blocking locale. `i18n/sync-state.json` records
those source/target baselines. Regional drafts use their own manifest and
source-hash checks; they are not additional configured detector locales.

## 1. Prepare source inputs and detect drift

Run commands from the repository root. First verify the generated inputs
without rewriting them:

```sh
python3 scripts/build-site.py --check
python3 scripts/build-search-index.py --check
python3 scripts/check-i18n-release.py --mode report --format json
python3 scripts/check-i18n-release.py --mode check --format json
```

If generation is stale, `python3 scripts/build-site.py` and
`python3 scripts/build-search-index.py` are write operations. The default
English index rebuild also refreshes the universe source and rendered HTML.
Coordinate generated-output reconciliation with the release integrator.

Both wrapper report/check modes are read-only. Report returns findings;
check exits 1 for French `missing`, `stale`, or `needs_baseline` findings.
German and Spain Spanish findings remain advisory. Configuration errors
exit 2. Neither mode drafts prose, records a baseline, or publishes pages.

For a portable diagnostic, these commands are also read-only:

```sh
python3 .agents/skills/okhp3-i18n-page-sync/scripts/i18n-page-sync.py --root . --mode report
python3 .agents/skills/okhp3-i18n-page-sync/scripts/i18n-page-sync.py --root . --mode check
```

The portable check exits 1 for missing/source-stale pages in **any configured
locale**, but does not fail for `needs_baseline` or `orphan`. It does not apply
this site's released-versus-draft severity policy. Use the wrapper for the
site gate. The detector reports the exact-pair skill for each flagged route.

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
An edit made only to those outputs can be overwritten. Inputs are:

- en-GB: current generated English HTML, plus
  `i18n/pilot/en-gb/dictionary.en-us-en-uk.json` and
  `i18n/pilot/en-gb/voice-profile.en-us.json`.
- es-MX: retained HTML in `i18n/pilot/es-mx/reviewed/` (`index.html`,
  `about-index.html`, `projects-index.html`, `contact-index.html`), plus
  current English shell inputs,
  `i18n/pilot/es-mx/dictionary.en-us-es-mx.json`, and
  `i18n/pilot/es-mx/voice-profile.en-us.json`. The generated `es/` or `es-mx/`
  pages are not translation inputs.
- Both: the generator's source guard currently reads
  `i18n/pilot/source-hashes-murderbird-stills-2026-09-06.json`.
  Keep earlier source records as history; do not substitute them by age.

The generator also applies its current shell and fixed-text adaptations.
These instructions describe its write path, not a new linguistic review.
T06 owns generator behavior changes; recheck inputs after that work lands.

## 3. Review and validate

Compare each draft against current English, record terminology/register
choices, and assign a review disposition in the owning review record.
Preserve the distinction between AI review and human/native approval.
Then run read-only structural and index-freshness checks:

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

The shared runtime in `assets/js/app.js` selects
`assets/data/search-index.fr.json` when the HTML language's base locale is
`fr`; every other locale falls back to `assets/data/search-index.json`.
This is already implemented. Do not treat locale-index existence as evidence
that every locale has language-specific search behavior.

## 4. Adopt a reviewed baseline

Use `scripts/check-i18n-release.py`, not direct portable adoption, for this
site. After review, the recipe is:

```sh
python3 scripts/check-i18n-release.py --mode adopt --locales fr --routes /about/ --provenance "$review_record"
```

Set `review_record` to the actual reviewed JSON record covering the selected
route and current file hashes. This is a recipe with an explicit input, not
a command to replay an old approval. Supply exactly one configured locale
(`fr`, `de`, or `es`) and only the reviewed routes. The wrapper requires the
matching language pair, locale, target path, accepted review status and route
disposition, and matching current source/target hashes. Its accepted statuses
are `ai-reviewed` or `approved`; accepted route dispositions are
`retained-ai-reviewed`, `approved`, or `no-semantic-delta-ai-reviewed`.
An `ai-reviewed` record cannot claim `native_or_human_approval: true`.

Adoption writes `i18n/sync-state.json`; it does not edit translated HTML or
change indexability. At this baseline, portable adoption updates only
`needs_baseline` and source-`stale` pairs, and detection does not compare
current target bytes with the recorded target hash. A target-only update is
therefore not a supported reviewed re-adoption path here. T02 owns that
pending integrity/adoption change. Revalidate this recipe against its merged
interface before handling target-only edits; do not invent a new flag or
claim target-integrity enforcement already exists.

## 5. Publication and policy boundary

Publication is a separate reviewed PR/release step through the existing
validation and Pages workflows. Passing structural checks or adopting hashes
does not grant publication approval, native-language certification, or a new
manifest status. Preserve the existing French release and all four draft
boundaries until the owning release decision explicitly changes them.

The canonical Skillz `okhp3-i18n-page-release` v1.1.0 policy uses an
indexable-only alternate cluster. This site retains its
`scripts/check-locale-links.py` adapter and regional checker for existing
draft alternates, noindex, sitemap exclusion, and index exclusion. Do not
replace that policy by copying portable examples or deleting manifests.
The manifest's `human-reviewed-required` field and individual AI-review
records remain distinct existing claims; this guide does not resolve their
policy vocabulary. T05 owns that proposed reconciliation.

## Evidence and distributed follow-up

Historical benchmarks, source hashes, and review records remain evidence of
their recorded revisions only. The `unpublished-scaffold` compatibility path
remains under separate review. No historical review claim changes here.

The local page-sync CLI help and SKILL examples use the actual `--mode`
interface. Follow up through the Skillz `language-mediation` source family:
compare the portable package with its canonical source and distributed site
copies, reconcile the documentation correction with their current versions,
and validate each consumer before promotion. This task does not write sibling
repositories or establish synchronized distribution. Keep generic detector
semantics portable and this site's provenance/severity policy in its wrapper.
