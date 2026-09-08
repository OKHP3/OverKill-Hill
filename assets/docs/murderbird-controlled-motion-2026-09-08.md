# MurderBird controlled motion correction

## Delivered correction

After two generative pilots failed support continuity, the September 8 owner
instruction to apply the proposed fixes authorized a controlled animation.
`assets/murderbird/production/video/murderbird-first-choice-controlled-pilot-03.mp4`
is an eight-second, 1280 × 720, 24 fps, silent 2D motion study derived from the
existing opening candidate. No Firefly generation or paid credits were used.
Both earlier pilots remain intact.

The stand shaft, base, feet, floor, bench, and CRT are protected from animation.
Only local motion fields around the saddle, torso, and head are animated:

| Time | Motion |
| --- | --- |
| 0–1.5 seconds | Hold the opening pose. |
| 1.5–2.35 seconds | Rotate the saddle region slightly around its seated pivot. |
| 1.9–3.3 seconds | Shift the torso slightly while keeping the feet fixed. |
| 4.1–6.7 seconds | Lower the head with a restrained eight-degree rotation. |
| 6.7–8 seconds | Hold the resulting pose. |

## Evidence and limits

The renderer checks the source SHA-256, refuses to overwrite outputs, and
measures protected pixels on all 192 frames. Maximum channel difference from
the opening frame in those regions was **zero before encoding**. H.264 is
lossy, so this is not a claim of byte-identical decoded regions. The resulting
MP4 passed a complete FFmpeg decode. The machine record is
[`murderbird-controlled-pilot-03.json`](../audit/murderbird-controlled-pilot-03.json).

This corrects the floating-stand failure in a controlled study. It does not
reconstruct a three-dimensional mechanism, supply typing animation, establish
that the gaze lands precisely on the fastener, or complete the soundtrack and
30–45-second film. The head movement is deliberately small. Local image
deformation can still be distinguishable from articulated 3D motion.

Disposition: **review candidate, not accepted final film**. No website media
references or release allowlists were changed. `assets/murderbird/` remains
outside the published release package.

A separate visual reviewer inspected eight sampled frames and the machine
report. The reviewer confirmed no obvious stand movement or foot lift and no
catastrophic silhouette break, while noting minor contour variation at the
neck, shoulder, and wing edges. That sampled review supports the controlled
study; it is not a full-speed or final-film acceptance review.

## Reproduction

Run `scripts/render-murderbird-first-choice.py` with Python, NumPy, and Pillow.
Supply `--ffmpeg` pointing to an FFmpeg build with `libx264`, plus vacant paths
for `--output`, `--report`, and `--contact-sheet`. Use a source-only output path.
The initial Studio encoder lacked H.264 support and produced no candidate;
the successful run used the executable bundled with imageio-ffmpeg 0.6.0.

Review the exported motion at normal speed and close-up before promoting it
beyond a controlled study. Add sound and integrate into the longer sequence
only after the motion is accepted for that use.

## Owner acceptance for the story page

Later on September 8, the owner reviewed the delivered study and explicitly
approved incorporating it into the MurderBird story page. This supersedes the
publication hold for this exact clip, SHA-256
`635f0e1552bac61699c03c8406157207f6230ea817bb1ecaeb3adbb3a7bf8613`.

The publication copy is `assets/video/murderbird-first-choice-635f0e15.mp4`,
placed at `/writings/murderbird/#media-first-choice` with native controls,
a first-frame poster, and an adjacent visual description. Playback is manual;
the eight-second clip is identified as silent. The longer film and the earlier
rejected clips are not included in this acceptance.
