# ADR-0001: Strictly Identical Cross-Site Foundation Runtime

## Status

Accepted — 2026-09-02

## Context

OverKill Hill, Glee-fully Tools, and AskJamie publish the same three foundation
files:

- `assets/css/theme.css`
- `assets/js/app.js`
- `assets/js/mermaid-init.js`

The live `main` branches had drifted into three different implementations. The
differences were not all the same kind of change:

| Area | Classification | Compatibility requirement |
| --- | --- | --- |
| Theme CSS | Shared structure with intentional body-class scopes (`.glee-main`, `.askjamie-main`, and the OKH default) | One byte-identical superset |
| Reading progress, year stamps, header controls, search, and reduced-motion behavior | Shared behavior | One implementation |
| Mobile navigation | Shared behavior; OKH had the strongest keyboard and inert-state handling | Keep the accessible implementation |
| OKH theme selector | OKH-specific interaction | Run only on unbranded OKH pages |
| Glee/AskJamie color-scheme selector | Shared compatibility behavior for brand-locked pages | Keep `data-theme="light"` for shared light rules and use `data-color-scheme` for the optional dark scheme |
| Construction overlay | Shared capability; actively used by Glee | Keep the accessible overlay behavior and no-op when absent |
| Sticky TOC follow and scrollspy | Shared behavior | Keep the wide-screen lerp follow and existing scrollspy |
| Search index fallback and result announcements | Shared defensive/accessibility behavior | Prefer `entries`, accept legacy `pages`, and re-announce through the live region |
| Mermaid source labeling and color resolution | Shared behavior required by OKH diagrams | Keep the pre-render accessible alternative and semantic-token color mapping |
| Mermaid click handling | Site/page-specific security policy | Strict by default; allow only the existing explicitly opted-in heat pages and exact target allowlist |
| Service worker, sparkle loader, and site analytics IDs | Site-specific or obsolete for the foundation | Do not place them in the shared runtime |

The sibling runtime copies were compared from their current `main` branches on
2026-09-02. The differences were substantial enough that “newest file wins”
would discard working behavior. The smallest safe design is therefore a single
byte-identical foundation superset whose site-specific behavior is selected by
existing DOM hooks and page data attributes, not by separate runtime copies.

## Decision

The three foundation files must be byte-identical across all three repositories.
The synchronization tool continues to enforce exact-content grouping and
reports a three-way conflict instead of choosing a winner.

`app.js` will use one shared bootstrap with these compatibility rules:

1. OKH pages (no `.glee-main` or `.askjamie-main`) receive the three-state
   `system`/`light`/`dark` theme control and `data-theme` updates on `<html>`.
2. Brand-locked pages always retain `data-theme="light"` for the shared CSS
   baseline, while their `auto`/`light`/`dark` control uses
   `data-color-scheme` and a site-specific storage key.
3. All storage access is failure-safe so private browsing or disabled storage
   cannot break navigation or search initialization.
4. Search and overlay strings remain neutral and derive the current brand from
   body classes; no site-specific analytics or offline code is added.

`mermaid-init.js` will initialize Mermaid with `strict` security by default.
Pages that explicitly opt in with `data-mermaid-security="loose"` receive the
existing exact click-target allowlist. Link attributes are normalized after
rendering so generated links cannot create an unsafe focus or opener path.

`theme.css` remains one superset. New site-specific CSS belongs in its existing
brand scopes; it is not split into per-site files.

## Consequences

### Positive

- A foundation change has one reviewable implementation and one content
  fingerprint for all three sites.
- Each site keeps its required visual theme and page-specific behavior through
  stable DOM hooks rather than hidden file divergence.
- The sync tool can distinguish a safe two-way propagation from a genuine
  three-way conflict.
- Mermaid security and cache fingerprints have a single source of behavior.

### Negative

- A shared runtime release must be smoke-tested against all three markup
  dialects, including Glee's construction overlay and the two brand-locked
  color-scheme controls.
- The shared file contains inert code for features not used on every site.
- A future site-specific behavior must be expressed as a hook/configuration
  contract or remain outside these foundation files.

## Validation contract

Before a foundation release is accepted:

1. `scripts/sync-foundation-files.py` dry-run reports no unresolved conflict.
2. Every sibling copy has the same normalized-content fingerprint and every
   generated page points at the current cache fingerprint.
3. Site validation covers navigation, search, Mermaid security, CSP alignment,
   and the site's existing responsive/accessibility checks.