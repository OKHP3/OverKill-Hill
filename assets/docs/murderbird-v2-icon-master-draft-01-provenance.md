# MurderBird v2 icon master draft 01

Status: reviewable artwork candidate, not owner-approved or deployed.
Scope: one design plus one correction for painted-checkerboard defect. Platform derivatives belong to P2.

In this historical record, P2 means the website-remediation project-management task, not a priority rating. Its subsequent delivered work is recorded in [delivery status](murderbird-v2-delivery-status-2026-09-05.md).

## Artifact

Master: [murderbird-v2-icon-head-master-draft-01.png](../../context/threads/assets/murderbird-camera-series-2026-09-05/murderbird-v2-icon-head-master-draft-01.png)
1254 x 1254 RGBA PNG. Corner and sampled opening beneath beak have alpha zero.
SHA-256: 4808B3A99DAEBAB399B80BA781723352D72AF1FE507AAA1FD782784D6D70ED8C

Generated using the built-in image tool. No model selector, API fallback or added dependencies.
Brand skill profile v1.1.0 guided bronze, deep verdigris and concentrated orange optics. No typography or backdrop was applied.

## Reference and provenance

Owner-preferred July Image 2, inspected before generation:
[Owner-preferred July reference](../../context/threads/assets/murderbird-camera-series-2026-09-05/murderbird-owner-preferred-july-reference.png). Original generator identifier: `exec-7764b692-1ea2-4c96-b00a-7a21fb09eafc.png`.

Initial output: exec-0576e72d-143c-4b78-bc1c-1308d4091c3e.png. Rejected for painted checkerboard.
Corrected output: exec-75458b85-7131-4875-be79-eb9bcb4d552d.png in the same generated-images directory. Copied unchanged to the project master above.

## Design rationale and limits

Broad swept crown plates, a continuous hooked bill and orange optical disk carry recognition without relying on gears. The open negative space beneath the beak distinguishes the bill at reduced sizes. Cropped neck avoids shrinking a full body into an icon. The result is sculptural metal rather than a flat sports-mascot drawing.

The correction enlarged the head, changed texture and did not preserve the requested generous mask-safe margins. This is therefore artwork input, NOT a ready-to-ship maskable icon. P2 must center and scale the entire alpha silhouette into its verified mask-safe region when deriving app icons. Do not simply mark this master purpose=maskable.

Actual 16/32/48 px readability has not been verified here. P2 should inspect true-size previews against light and dark surfaces, with particular attention to dark crown separation, optic size and bill gap. Broad silhouette is intentional; high-frequency texture will not survive tiny sizes. Platform backgrounds, favicon framing, opaque Apple output and safe margins should be derived and reviewed by P2, not treated as already passed. No further artwork rounds in this task unless requested.

Existing favicon, website, manifesto and previous assets are unchanged.

## Exact generation prompt

```text
Use case: logo-brand.
Asset: ONE reviewable raster icon master for OverKill Hill P³ MurderBird v2, square.
Image 1: owner-preferred HEAD IDENTITY reference only, not a scene or full-body reference.
Create a purpose-designed head-only emblem of this ancient mechanical bird. Preserve the distinctive right-facing hooked bill, swept backward segmented crown, hostile heavy brow and one deep round ember-orange optic. Short cropped armored neck under the head. No body, computer or environment. No generic eagle sports mascot, cartoon, cute eye, literal dinosaur, lettering or border badge.
Simplify strongly for tiny favicon recognition: about five broad overlapping crown plates, bold continuous curved bill silhouette, one simple orange optical disk in a dark socket, three or four major bronze/verdigris metal planes. Omit tiny gears, filigree, screws and noise. Sculptural fabricated metal with restrained bevels and real weight, not glossy plastic and not a busy photoreal crop. Dark bottle-green patinated bronze, muted bronze edge accents, concentrated rust-orange/amber eye. Do not add neon or glowing halo.
Square 1024x1024 composition. Center the entire head inside an imaginary circle of diameter 72% of canvas. All bill tips, crown tips and neck inside that circle, with generous untouched margin for platform masks. Do not draw the circle. Strong recognizable profile with deep negative space under the hook.
Genuinely transparent background with real PNG alpha, no scenery, shadows outside silhouette, checkerboard illustration or white matte. Single isolated master, no mockup, no size sheet, no text or watermark.
```

## Exact defect-correction prompt

```text
Background extraction only: remove the painted checkerboard from this exact MurderBird head icon and return genuine RGBA PNG transparency. Preserve the artwork, position, square dimensions and margins unchanged. Make outside the silhouette and the opening beneath the beak fully alpha zero. No replacement scene, no checkerboard pattern, no white matte. Do not redesign the bird.
```
