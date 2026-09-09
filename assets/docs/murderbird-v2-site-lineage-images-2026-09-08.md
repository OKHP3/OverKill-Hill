# MurderBird v2 site-lineage images

## Request and status

Jamie requested new v2 images that retain visual lineage to the existing page illustrations after the sitewide image-era audit. Five source images were generated with the built-in imagegen tool on September 8, 2026. These are new review candidates, not owner-approved replacements or a deployment. No existing page, image, historical gallery, or sharing metadata was overwritten.

Sources are saved under `assets/murderbird/production/images/`, outside the Pages release allowlist. The original generator outputs remain preserved in the task's Codex generated-images directory. This is a generation receipt, not a replacement for the established asset register.

## Shared character reference

`assets/img/library/murderbird-unified-master-candidate-03-2026-09-06.png` supplied the authoritative character/material reference for all five generations: hooked terror-bird bill, segmented metal crown, orange circular optic, dark patinated bronze with restrained verdigris, brass bearings, Victorian articulation, and a physically supported body. Older artwork supplied composition and role, not character anatomy. These are independently generated interpretations; exact geometric identity is not certified.

## Delivered files and retained lineage

All paths below are relative to `assets/murderbird/production/images/`.

| File | Size and format | Earlier composition retained |
|---|---|---|
| `murderbird-v2-legal-guardian-square-1254-2026-09-08.png` | 1254 × 1254, RGBA | Waiting Sentinel: centered, quiet standing guardian, compact wings, whole-body square cutout |
| `murderbird-v2-contact-warning-square-1254-2026-09-08.png` | 1254 × 1254, RGBA | Attacking Sentinel: right-facing open bill, raised foot, spread armor panels, energetic square silhouette |
| `murderbird-v2-under-construction-wide-1536-2026-09-08.png` | 1536 × 1024, RGB | Bird Patrol construction: hanging sign, conveyor, gears and pipes; bird now stands beside the conveyor on the floor |
| `murderbird-v2-technical-difficulties-wide-1536-2026-09-08.png` | 1536 × 1024, RGB | Bird Patrol error: startled bird, steam, loose mechanical parts; blank lower area for accessible page text |
| `murderbird-v2-crt-sharing-background-wide-1536-2026-09-08.png` | 1536 × 1024, RGB | Title-left/computer-right sharing composition, horizontal color bands and blueprint grid; added v2 head medallion |

Composition references were respectively the existing `over-kill-hill-p3-sentinel-waiting-square-1024.png`, `over-kill-hill-p3-sentinel-attacking-square-1024.png`, `over-kill-hill-p3-bird-patrol-comp-left-under-construction-wide-1536.png`, `over-kill-hill-p3-bird-patrol-comp-left-error-explosion-wide-1536.png`, and `assets/img/library/over-kill-hill-p3-title-left-comp-right-wide-1536.png`.

## Validation and integration notes

- All five copied files were SHA256-compared with their generator outputs and decoded successfully with Pillow.
- Both cutouts have actual RGBA alpha ranging from 0 to 255. The first Legal generation had a painted checkerboard; it was rejected and regenerated using imagegen background extraction. Only the corrected output is selected here.
- Visual inspection confirmed the main silhouettes, intact feet, bronze material family, readable construction lettering, and composition lineage. The Contact image is a stylized gesture with broader raised panels than the folded-wing story master; it is not a new canonical anatomy sheet.
- The sharing image is a background, not a finished social card. Add real typeset brand text and compose the required social dimensions before publication. Keep error copy in HTML. Preserve translated copy and accurate alternative text during integration.
- WebP derivatives, page swaps, localized parity, browser checks, owner art acceptance, and release verification have not been performed for these new files. No claim that this resolves the live image-era audit is made.

## Generator outputs

### Error illustration revision 04: moderated neck length

Jamie found revision 03's neck too long. Revision 04 shortens that neck toward a midpoint between revisions 02 and 03, retaining upright posture and the 404 disassembly scene. Saved `assets/murderbird/production/images/murderbird-v2-404-reassembly-revision-04-wide-1536-2026-09-08.png` from generator output `exec-3e00f026-2b3a-4ff0-9e3c-74aac65251c0.png`. Visual review confirms a lower head and shorter exposed neck than revision 03; exact percentage reduction and unchanged surrounding pixels are not certified. 1536 × 1024 RGB, decoded and copy hash verified. Earlier revisions remain preserved. Candidate for review, not deployed.

### Error illustration revision 03: neck proportions

Jamie requested a longer neck in the 404 revision. Saved `assets/murderbird/production/images/murderbird-v2-404-reassembly-revision-03-wide-1536-2026-09-08.png` from `exec-734478cb-fd37-481a-b8d6-ae9005ffce72.png`. The visible articulated neck is longer and more upright, with increased separation between head and shoulders. Master03 supplied the anatomy reference. The disassembly, falling parts, workshop, and 404 CRT remain recognizable; generated changes to proportions and positioning are not pixel-identical preservation. 1536 × 1024 RGB, decoded successfully, source/copy SHA256 matched. Earlier revisions preserved. Review candidate only, not deployed.

### Construction anatomy revision 02

Jamie identified oversized wings/tail and a short eagle-like neck in the first construction candidate. Revision `assets/murderbird/production/images/murderbird-v2-under-construction-revision-02-wide-1536-2026-09-08.png` uses master03 as its anatomy reference: visibly longer upright neck, small rounded folded wing armor, and no projecting tail fan. Workshop composition, conveyor, lighting family, and readable construction sign remain recognizable, with minor generated framing changes. Visual review confirms the requested silhouette changes, not pixel-identical environment preservation or exact geometric identity. Source `exec-ebf7e68f-fff5-45fa-bd53-e40bb488e9bd.png`; 1536 × 1024 RGB, decoded successfully and copy SHA256 matched. Original preserved. Revision is a review candidate, not owner-approved or deployed.

### Legal guardian frontal alternate

**REJECTED BY OWNER — do not integrate or publish.** Jamie scrapped the dead-on design because it looks goofy. This rejection applies to both `exec-9b89ef51-fab2-4dab-9d42-3cf53ffee283.png` and its transparent derivative `exec-c8a2b3cc-69d1-4943-9ccd-870e2653aa45.png`, including the project copy named below. Files remain only as historical production sources outside the Pages release allowlist. The earlier three-quarter guardian is unaffected. This disposition supersedes the creation-time review-candidate status below.

Jamie requested a dead-on alternate of the Legal guardian. Saved `assets/murderbird/production/images/murderbird-v2-legal-guardian-frontal-alternate-square-1254-2026-09-08.png`, 1254 × 1254 RGBA with verified alpha range 0–255. Head and torso face the viewer, with both orange optics visible and symmetrical planted feet. Original three-quarter guardian remains preserved. Generation source: `exec-c8a2b3cc-69d1-4943-9ccd-870e2653aa45.png`; the first frontal output (`exec-9b89ef51-fab2-4dab-9d42-3cf53ffee283.png`) had a painted checkerboard and was superseded by the transparent cutout. This is an alternate review candidate, not a deployed image or an exact geometric reconstruction.

### Error illustration revision 02

Jamie requested a clearer 404 problem in the bird itself, visible disassembly, and closer leg/foot correspondence to the masters. New review candidate: `assets/murderbird/production/images/murderbird-v2-404-reassembly-revision-02-wide-1536-2026-09-08.png` (1536 × 1024 RGB). Generator source: `exec-566f5b34-9fe6-4511-a73d-aa8dd3db0bbb.png`. Copy hash matched and image decoding passed.

The revised scene contains a readable CRT message, `404 / PAGE NOT FOUND / REASSEMBLY REQUIRED`, detached breast armor, exposed gearing, sparks, and falling fasteners from the bird. Heavy segmented legs and compact wings were referenced to master03 and the accepted unified Sentinel scene. The requested foot arrangement is four talons per foot, three forward and one rear. This is an inferred interpretation of the reference, not an established written canon rule. Toe overlap prevents a definitive independent visual count on both feet in this view; do not claim exact anatomy validation. The original scene remains preserved; revision 02 is not owner-approved or deployed.

### Contact anatomy revision 02

Jamie identified oversized wings and tail and requested beak consistency. Comparison against the accepted master03 and unified Sentinel scene confirmed that the first Contact candidate inherited too much of the older spread-wing silhouette. It is superseded for review by `assets/murderbird/production/images/murderbird-v2-contact-warning-revision-02-square-1254-2026-09-08.png`.

Revision 02 retains the raised-foot gesture but replaces the raised flight-like wings with compact folded body armor, removes the projecting tail fan, and closes the exaggerated lower jaw beneath a heavy hooked upper bill. Visual review finds substantially closer correspondence to both references; exact geometric identity is not certified. The output is 1254 × 1254 RGBA with verified alpha range 0–255. Two intermediate outputs had painted checkerboards and were rejected. Selected generator output: `exec-e0c2ac4c-47c7-428f-bede-26419b477804.png`. Original candidate and intermediate generator files remain preserved. This revision is not yet owner-approved or deployed.

Original directory: `C:/Users/jamie/.codex/generated_images/01a07924-14ac-7030-a52f-0f0d826f7aa0/`.

- Legal selected: `exec-b335a1bb-80ab-4fff-a7fa-f845f4ec4c40.png`; rejected checkerboard source: `exec-6059d6c2-a8e9-4ac5-9770-402c6731db04.png`.
- Contact: `exec-bbbc14d5-b916-432d-a75f-aca1aa718bf1.png`.
- Construction: `exec-9c6f0f57-2fcd-4f93-ac23-57e3b2390c4e.png`.
- Error: `exec-a9e44152-cccf-49fe-be12-f2497ca641d1.png`.
- Sharing background: `exec-81d91c31-ce47-4587-8ba0-043c7572653b.png`.
