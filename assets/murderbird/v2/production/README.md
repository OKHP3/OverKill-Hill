# MurderBird production scale stage

Editable Blender 5.2.1 LTS scene: `murderbird-scale-stage.blend`.

This is measured **previsualization only**, not a finished MurderBird model, animation rig, historical reconstruction, or certification of mechanical feasibility. The 1.8 m bird height is the current working design proposal, not an established measurement in the story.

## Dimensions and use

- Scene units are metres at scale 1.
- Bird envelope: 0.85 m wide, 0.9 m deep, 1.8 m high.
- Abstract adult mannequin: 1.8 m overall height, beside the bird on the same depth plane.
- Bench upper surface: 0.9 m above ground.
- Ordinary CRT placeholder: 0.45 m wide, 0.42 m deep, 0.4 m high; supported by bench.
- Floor cradle base: 0.12 m high; separate from the standing bird.
- Perspective, front orthographic, and side orthographic cameras are provided.
- The concept reference is packed into the blend as a non-rendering image empty. **It is not dimensionally calibrated** and must not override measured stage objects.

Use the orthographic view to check overall height and floor contact. Use the perspective view to plan consistent human/furniture scale cues. Proxy cubes deliberately avoid implying that character geometry, foot articulation or load capacity has been solved.

## Rebuild and verify

Run in PowerShell from this folder:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --factory-startup --python './build-scale-stage.py'
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --factory-startup --python './verify-scale-stage.py'
```

The build script saves beside itself. Its optional source-reference path points to Jamie's original production folder; if absent, scene construction still works, but the packed-reference verification check will fail until a reference is provided. The supplied blend already contains the packed image and opens independently.

`scale-stage-manifest.json` records all mesh locations/dimensions. `scale-stage-verification.json` records a separate-process reopening check of units, heights, cameras and the packed reference. All seven checks passed on creation.

No renders, website edits, or master-image replacements are performed by these scripts.

