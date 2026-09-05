# MurderBird v2 Icon Preview Provenance

Status: reviewable production-shaped candidate. This branch changes the shared icon references, manifest, generated HTML pages, root fallback ICO, and new unique runtime assets. It does not deploy or merge them.

## Source

- Master: `context/threads/assets/murderbird-camera-series-2026-09-05/murderbird-v2-icon-head-master-draft-01.png`
- Supplied dimensions: 1254 x 1254
- Supplied mode: RGBA
- Verified SHA-256: `4808B3A99DAEBAB399B80BA781723352D72AF1FE507AAA1FD782784D6D70ED8C`
- Source status: exact imagery candidate; no artwork was regenerated or altered.

## Deterministic packaging

The preview derivatives were produced with Pillow using only alpha-bounds cropping, resize, alpha compositing, opaque background compositing, ICO encoding, and contact-sheet drawing. The source master was copied unchanged. The safe-margin canvas is 1024 x 1024 with the source artwork resized to 720 x 720 and centered. Opaque platform previews use background `#2a2320`. Browser PNGs use the same master artwork cropped to its alpha bounds and fitted to a one-pixel transparent edge at each target size; this is separate from the wider PWA safe-margin treatment.

Generated files:

- `murderbird-v2-icon-safe-margin-preview-1024.png`
- `murderbird-v2-icon-browser-16.png`
- `murderbird-v2-icon-browser-32.png`
- `murderbird-v2-icon-browser-48.png`
- `murderbird-v2-icon-preview.ico` with 16, 32, and 48 layers
- `murderbird-v2-icon-opaque-180.png`
- `murderbird-v2-icon-opaque-192.png`
- `murderbird-v2-icon-opaque-512.png`
- `murderbird-v2-icon-maskable-192.png`
- `murderbird-v2-icon-maskable-512.png`
- `murderbird-v2-icon-contact-sheet-preview.png`
- `murderbird-v2-icon-mask-evidence-preview.png`
- `murderbird-v2-icon-native-size-contact-preview.png`

## Verification

- Master hash matches the supplied provenance record.
- Browser PNGs are exactly 16, 32, and 48 pixels and retain transparent corners.
- Opaque and maskable PNGs are exactly 180, 192, and 512 pixels as named and have opaque corners.
- ICO inspection reports 16, 32, and 48 pixel layers.
- Contact sheets show the master, safe-margin, light-surface, dark-surface, tiny browser, and mask-boundary evidence views.
- The browser contact view shows 16, 32, and 48 pixel icons at native size on light and dark surfaces.
- Browser derivatives were tightened after native-size review so the 16 pixel visible silhouette is not reduced by PWA padding; the ICO and root fallback were regenerated from those final browser derivatives.
- The root `/favicon.ico` now uses the MurderBird ICO package; the previous root file is preserved at `assets/img/favicons/archive/favicon-legacy-2026-09-05.ico`.
- Manifest entries use distinct `any` and `maskable` files with matching MIME types and declared sizes.

## Applied review scope

- `assets/partials/head.html` references the 16, 32, 48 browser PNGs, opaque 180 Apple touch icon, and MurderBird root ICO.
- `site.webmanifest` references separate opaque `any` entries and centered `maskable` entries at 192 and 512 pixels.
- Generated HTML pages were rebuilt so canonical and locale pages share the same icon head references.
- `index.html` and `site-src/pages/index.main.html` use the frontal homepage candidate and its WebP sources.
- The manifesto narrative artwork and metadata were not changed.

## Remaining gate

This remains a reviewable candidate, not a production release. PM/architect packaging and render acceptance, followed by CI and explicit merge authority, are still required. The mask evidence is a review aid, not proof of final platform acceptance.
