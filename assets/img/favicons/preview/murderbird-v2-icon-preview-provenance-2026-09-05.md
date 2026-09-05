# MurderBird v2 Icon Preview Provenance

Status: candidate packaging preview only. This branch does not change live page sources, `assets/partials/head.html`, `site.webmanifest`, production favicon files, generated pages, or deployment configuration.

## Source

- Master: `context/threads/assets/murderbird-camera-series-2026-09-05/murderbird-v2-icon-head-master-draft-01.png`
- Supplied dimensions: 1254 x 1254
- Supplied mode: RGBA
- Verified SHA-256: `4808B3A99DAEBAB399B80BA781723352D72AF1FE507AAA1FD782784D6D70ED8C`
- Source status: exact imagery candidate; no artwork was regenerated or altered.

## Deterministic packaging

The preview derivatives were produced with Pillow using only resize, alpha compositing, opaque background compositing, ICO encoding, and contact-sheet drawing. The source master was copied unchanged. The safe-margin canvas is 1024 x 1024 with the source artwork resized to 720 x 720 and centered. Opaque platform previews use background `#2a2320`.

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

## Verification

- Master hash matches the supplied provenance record.
- Browser PNGs are exactly 16, 32, and 48 pixels and retain transparent corners.
- Opaque and maskable PNGs are exactly 180, 192, and 512 pixels as named and have opaque corners.
- ICO inspection reports 16, 32, and 48 pixel layers.
- Contact sheets show the master, safe-margin, light-surface, dark-surface, tiny browser, and mask-boundary evidence views.

## Not applied

This package does not authorize a manifest or HTML change. A later production change would need an explicit decision on `any` versus `maskable` declarations, canonical head links, browser-size policy, and live validation. The mask evidence is a review aid, not proof of final platform acceptance.
