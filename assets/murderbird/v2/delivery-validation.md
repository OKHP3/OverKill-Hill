# Delivery validation

Validated 2026-09-06 after the corrected Heart and First Choice masters replaced their initial versions.

- Eight masters, 48 delivery encodings (three widths in WebP/JPEG), and eight 1200 × 630 PNG social cards.
- All 64 manifest image SHA-256 values verified against files on disk. Exact prompt provenance exists for all eight masters; both modern scale correction prompts are included.
- These 64 image files total 31,620,361 bytes (about 30.2 MiB). The 960-pixel WebP previews range from 48,978 to 128,336 bytes; social PNGs range from 727,020 to 1,091,484 bytes.
- Browser checks verified all eight social cards are exactly 1200 × 630, use loaded images with `object-fit: contain`, and have no footer overflow.
- Gallery checked at 1440-pixel desktop and 390-pixel mobile widths. All eight images load with nonempty alt text and uncropped proportional dimensions. Mobile document width equals viewport width; no horizontal overflow.
- Visually inspected the mobile gallery and the Maker, corrected Heart, and corrected First Choice social raster layouts. Typography fits and full compositions remain visible.
- Browser screenshots: repository-local `output/playwright/murderbird-library-desktop.png` and `murderbird-library-mobile.png` (ignored review evidence).
- The local server returns a harmless 404 for an unprovided favicon; no gallery image failed to load.

These checks validate delivery packaging, not historical accuracy, exact anatomical consistency, mechanics, or approval to publish. See `independent-visual-review.md` and `ART-DIRECTION.md` for creative limits and outstanding canon decisions.
