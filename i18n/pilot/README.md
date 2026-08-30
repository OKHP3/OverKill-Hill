# i18n pilot scaffold

**Status: pilot-ready for French. German (`de`) and Spanish (`es`) copy has
been drafted for the same four routes and is live on `/de/` and `/es/`, but
is pending human editorial review before it is added to `sitemap.xml` (see
Publishing contract below). Treat `de`/`es` as a draft pilot, not a released
one, until that review happens.**

## Decision

The first pilot locale is French (`fr`), later extended to German (`de`) and
Spanish (`es`) on the same four routes. The pilot is intentionally limited to
four evergreen pages:

1. `/` — the site orientation and value proposition
2. `/about/` — the organization and operating context
3. `/projects/` — the durable project index
4. `/contact/` — the path from discovery to inquiry

These pages are more suitable than the manifesto or long-form essays for a
translation pass because they contain less coined terminology,
model-specific prose, and rhetorical wordplay. Copy is supplied for these
four routes only, in French, German, and Spanish. Any future copy changes
must go through human editorial review before release. The German and
Spanish copy was AI-drafted (adapted, not literal, matching the French
pilot's approach) and has not yet had the human editorial pass the French
pilot received before its own release; it should get that same review
before being treated as final.

## Publishing contract

The supplied translations are placed as complete HTML pages under `/fr/`,
`/de/`, and `/es/` using the route map in `manifest.json`. Each page must:

- use `<html lang="fr">`, `lang="de"`, or `lang="es"` as appropriate;
- use a locale-specific canonical URL such as
  `https://overkillhill.com/fr/about/`, `.../de/about/`, or `.../es/about/`;
- link to its sibling pages in every other pilot locale (`hreflang="fr"`,
  `"de"`, `"es"`) plus the English source (`hreflang="en"`) and an
  `hreflang="x-default"` link to the English source;
- be added to `sitemap.xml` only after human review and release QA.

The English pages, and every pilot-locale page, gain reciprocal `hreflang`
links to all four locales in the same release. French is listed in the
sitemap because it has been through that review; German and Spanish are not
yet listed -- add their eight URLs to `sitemap.xml` once reviewed.

## Search index scaffold

The locale-aware generator reads the translated pages and writes a
locale-specific index; the `--locale` flag accepts any two-letter code with a
matching top-level directory, so `fr`, `de`, and `es` all work unchanged:

```sh
python3 scripts/build-search-index.py --locale=fr
python3 scripts/build-search-index.py --locale=de
python3 scripts/build-search-index.py --locale=es
python3 scripts/build-search-index.py --locale=fr --check
```

It reads published-style pages from `/fr/`, `/de/`, or `/es/` and writes
`assets/data/search-index.<locale>.json`. The English index remains
unchanged.

## Effort and maintenance assessment

This is a pre-pilot estimate, not evidence that translation has already been
performed. Based on the current static site and the four selected pages:

- **Human translation:** approximately 2–4 working days for a first pass,
  terminology review, and editorial QA. The range assumes a translator who
  can preserve the site's technical meaning without machine-only output.
- **Engineering and release work:** approximately 0.5–1 day for locale page
  wiring, reciprocal hreflang, sitemap inclusion, index generation, and
  responsive/accessibility checks.
- **Ongoing burden:** every source-page edit requires a translation decision,
  terminology review, and a second release check. A practical planning
  assumption is 10–25% additional editorial effort on changes touching these
  pages, with a larger cost when brand terminology changes.
- **Expansion gate:** do not expand beyond four pages, in any locale, until
  a human reviewer confirms meaning, tone, terminology, links, metadata, and
  mobile layout in that locale. This gate applied to French before its
  release and applies to the drafted German and Spanish copy now.

The pilot is therefore technically feasible on the existing origin, but
translation quality and recurring editorial capacity are the decision gates
for expansion.