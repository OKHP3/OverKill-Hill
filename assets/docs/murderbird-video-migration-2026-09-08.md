# MurderBird video source migration — September 8, 2026

Moved all 11 MP4 files from the owner's Downloads folder into
`assets/murderbird/production/video/` and renamed them using ASCII lowercase
kebab-case. The files contain nine unique SHA-256 hashes; both duplicate
copies remain present with a `copy-02` suffix. No video was transcoded or
overwritten. All 11 destination hashes matched the original inventory.

The exact original filenames, repository-relative destinations, byte counts,
and SHA-256 hashes are recorded in
[`murderbird-video-migration-2026-09-08.json`](../audit/murderbird-video-migration-2026-09-08.json).
For reversal, move each destination back to Downloads using its recorded
`originalName`, after checking that the original path is vacant.

## Production status

These are source and review artifacts, not accepted website media. The
release builder's runtime allowlist excludes `assets/murderbird/`.

- Seven unique legacy clips preserve the earlier six-scene sequence and
  vertical Sentinel experiment. They are not accepted for the revised film.
- First Choice pilot 01 remains on hold because the feet move and the cause
  of the bird's response is unclear.
- First Choice pilot 02 remains on hold because the entire stand moves
  instead of only its saddle pivot. Both new pilots contain no audio.

## Proposed motion correction

Anchor the stand's base and shaft. Animate only a small rotation at the saddle
pivot; keep both feet planted, then shift the torso and lower the head in
response. A controlled animation or composite is the proposed next approach.
This migration does not perform that correction or authorize another paid
generation.
