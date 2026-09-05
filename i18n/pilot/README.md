# Locale Translation Operating Guide

**Status:** active four-route translation scope. French (`fr`) is the reviewed
locale. German (`de`) and Spanish (`es`) are drafted, retained as `noindex`,
and pending human editorial review. This directory records the route contract;
it is not a translation service or a publication queue.

## Scope and ownership

The current scope is limited to these evergreen English routes:

1. `/` -- site orientation and value proposition
2. `/about/` -- organization and operating context
3. `/projects/` -- durable project index
4. `/contact/` -- discovery-to-inquiry path

English source truth is `site-src/pages.json` and its content fragments and
partials. Locale pages are maintained separately under `/fr/`, `/de/`, and
`/es/`. The route and locale status ledger is
`i18n/pilot/manifest.json`; source/target hash state is
`i18n/sync-state.json`; configured detector inputs are
`i18n/sync.config.json`.

## Operating sequence

1. Run the English build and regenerate the English search index.
2. Run the page-sync detector in report/check mode. It compares the generated
   English index with the persisted source hashes and names the exact
   `okhp3-translation-en-us-<pair>` skill for each stale route.
3. Use the named exact-pair skill for the draft. Apply register mediation and
   terminology decisions before regional translation; do not treat a hash
   update as translation-quality evidence.
4. Compare the draft with the current English source, record terminology and
   register decisions, and assign a review disposition in the owning handoff
   or release record.
5. Run locale search-index generation and `scripts/check-locale-links.py`.
   Keep German and Spanish `noindex` and outside the sitemap until human
   editorial review is complete.
6. Only after review and release QA, update the relevant manifest status and
   adopt the source baseline with the page-sync tool. Adoption records
   freshness; it does not certify native-language quality.

## Page and release contract

Each in-scope locale page must use its locale HTML language, locale-specific
canonical URL, reciprocal `hreflang` links to English and the configured
locales, and the correct indexability state. French is released and listed in
the sitemap. German and Spanish remain drafts, `noindex`, and absent from the
sitemap. Locale indexes are generated separately as
`assets/data/search-index.<locale>.json`.

Useful commands:

```sh
python3 scripts/build-search-index.py
python3 scripts/build-search-index.py --locale=fr
python3 scripts/build-search-index.py --locale=de
python3 scripts/build-search-index.py --locale=es
python3 scripts/check-locale-links.py
python3 .agents/skills/okhp3-i18n-page-sync/scripts/i18n-page-sync.py --root . --mode report
python3 .agents/skills/okhp3-i18n-page-sync/scripts/i18n-page-sync.py --root . --mode check
```

## Policy boundary

The canonical Skillz `okhp3-i18n-page-release` v1.1.0 policy uses an
indexable-only alternate cluster. This site keeps the existing
`scripts/check-locale-links.py` adapter because it also verifies retained
German/Spanish draft pages, their `noindex` state, sitemap exclusion, and
locale-index exclusion. Do not install a second checker or delete the pilot
manifest to make drift pass. Any future policy change must map these checks
and preserve the meaning of the current state ledger first.

The shared runtime currently uses the English search index constant. Locale
indexes remain active generated artifacts until the language-specific search
behavior is decided and tested with the shared-runtime owner. Do not edit
`assets/js/app.js` in this migration cleanup.

## Evidence and history

Historical skill benchmarks and extra exact-pair packages remain preserved;
their presence does not imply that the current site has used every package.
The `unpublished-scaffold` compatibility branch in the locale checker remains
under separate review because it is compatibility behavior, not confirmed
dead code. No new language publication or native-language approval is implied
by structural or hash validation.
