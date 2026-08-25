# i18n pilot scaffold

**Status: pilot-ready. The four pilot pages have supplied French copy and
remain limited to the routes listed below.**

## Decision

The first pilot locale is French (`fr`). The pilot is intentionally limited to
four evergreen pages:

1. `/` — the site orientation and value proposition
2. `/about/` — the organization and operating context
3. `/projects/` — the durable project index
4. `/contact/` — the path from discovery to inquiry

These pages are more suitable than the manifesto or long-form essays for a
translation pass because they contain less coined terminology,
model-specific prose, and rhetorical wordplay. French copy is supplied for
these four routes only. Any future copy changes must go through human
editorial review before release.

## Publishing contract

The supplied translations are placed as complete HTML pages under `/fr/` using
the route map in `manifest.json`. Each page must:

- use `<html lang="fr">`;
- use a locale-specific canonical URL such as
  `https://overkillhill.com/fr/about/`;
- link to its French siblings with `hreflang="fr"`;
- link to the English source with `hreflang="en"` and include an
  `hreflang="x-default"` link to the English source;
- be added to `sitemap.xml` only after human review and release QA.

The English pages gain reciprocal `fr` and `x-default` links in the same
release, and the four pilot routes are listed in the sitemap.

## Search index scaffold

The locale-aware generator reads the translated pages and writes the French
index:

```sh
python3 scripts/build-search-index.py --locale=fr
python3 scripts/build-search-index.py --locale=fr --check
```

It reads published-style pages from `/fr/` and writes
`assets/data/search-index.fr.json`. The English index remains unchanged.

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
- **Expansion gate:** do not expand beyond four pages until a human reviewer
  confirms meaning, tone, terminology, links, metadata, and mobile layout in
  the target locale.

The pilot is therefore technically feasible on the existing origin, but
translation quality and recurring editorial capacity are the decision gates
for expansion.