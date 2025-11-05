# Image Asset Guidelines

This directory contains all image assets used across the OverKill Hill P³ site.

## Sizes & Formats

- **Logo icon**: Provide square PNGs at 512px and 192px for Android / PWA icons and an SVG for the favicon. The `OverKill Hill P³ Square Icon.png` file is used for the header and favicon fallback.
- **Banner image**: Use a high‑resolution image (~2400×1350) to ensure crispness on large screens. The file `OverKill Hill P³ Banner.png` is used on the home hero.
- **Square feature image**: Use a 1200×1200 PNG for cards and previews (`OverKill Hill P³ Square.png`).
- **Social previews**: When creating Open Graph cards, target 1200×630 JPG dimensions.
- **Blueprint background**: Rather than embedding an image, the blueprint grid is rendered via CSS using the `.stripe-bg` class and background gradients. If pattern artwork is needed, create an SVG or PNG at 800×800 and tile it with 8–12% opacity.
- **Alt text**: Each image must include a concise, descriptive `alt` attribute. For decorative images, leave alt empty (`alt=""`) and specify role="presentation".

## Usage

Images are referenced relative to `assets/img/` from HTML files. Keep file names descriptive. Avoid embedding text within images; instead use HTML/CSS for live, accessible text.
