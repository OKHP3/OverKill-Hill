"""Render a restrained 2D motion study with a fixed stand and planted feet.

Authoring tool only; requires Pillow, NumPy, and an explicit FFmpeg executable.
Uses the exact approved opening candidate rather than repairing generated
geometry. Output remains a source-only review candidate, not a release asset.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/img/library/murderbird-first-choice-opening-candidate-2026-09-06.png"
SOURCE_SHA = "c12874d1898dbee7617df22acaf39165b4453c5a9282091274c37ad6070ad5f6"
WIDTH, HEIGHT, FPS, SECONDS = 1280, 720, 24, 8
SCALE = WIDTH / 1672


def ease(t: float, start: float, end: float) -> float:
    value = min(1.0, max(0.0, (t - start) / (end - start)))
    return value * value * (3 - 2 * value)


def region(points: list[tuple[int, int]], blur: int) -> np.ndarray:
    mask = Image.new("L", (WIDTH, HEIGHT))
    ImageDraw.Draw(mask).polygon([(round(x * SCALE), round(y * SCALE)) for x, y in points], fill=255)
    # Blend only the margins of the motion field. No new scene content is generated.
    mask = mask.filter(ImageFilter.MaxFilter(19)).filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(mask, dtype=np.float32) / 255


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ffmpeg", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--contact-sheet", required=True, type=Path)
    args = parser.parse_args()
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA:
        raise SystemExit("Opening source differs from the reviewed reference")
    for path in (args.output, args.report, args.contact_sheet):
        if path.exists():
            raise SystemExit(f"Refusing to overwrite {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
    base = np.asarray(Image.open(SOURCE).convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS))
    yy, xx = np.mgrid[:HEIGHT, :WIDTH].astype(np.float32)
    body = region([(630, 220), (786, 223), (844, 290), (896, 411), (855, 520), (786, 569),
                   (803, 655), (806, 741), (764, 741), (729, 625), (675, 569), (618, 618),
                   (600, 720), (552, 720), (544, 590), (487, 509), (502, 368), (574, 283)], 12)
    head = region([(628, 181), (645, 89), (692, 45), (780, 23), (874, 49), (929, 107),
                   (955, 193), (940, 266), (895, 266), (843, 213), (783, 221), (751, 280),
                   (697, 284), (673, 233)], 12)
    saddle = region([(689, 493), (829, 493), (863, 463), (902, 470), (922, 503),
                     (917, 544), (890, 562), (852, 565), (723, 550)], 5)
    # Explicit immutable regions: both feet/floor, stand shaft/base, bench and CRT.
    fixed = (yy >= 752 * SCALE) | ((xx >= 929 * SCALE) & (yy >= 450 * SCALE)) | (xx <= 465 * SCALE)
    for mask in (body, head, saddle):
        mask[fixed] = 0
    encoder = subprocess.Popen([str(args.ffmpeg), "-v", "error", "-n", "-f", "rawvideo",
        "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "pipe:0",
        "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", str(args.output)], stdin=subprocess.PIPE)
    samples = []
    fixed_max_delta = 0
    try:
        for frame_index in range(FPS * SECONDS):
            t = frame_index / FPS
            settle = ease(t, 1.5, 2.35)
            shift = ease(t, 1.9, 3.3)
            dip = ease(t, 4.1, 6.7)
            # Inverse displacement fields: a small pad rotation, grounded torso
            # transfer, then head rotation around the neck. Never rotate the stand.
            tx, ty = -8 * SCALE * shift, -2 * SCALE * shift
            support_angle = math.radians(1.4) * settle
            head_angle = math.radians(8) * dip
            dx = -tx * np.maximum(body, head)
            dy = -ty * np.maximum(body, head)
            hx, hy = xx - 739 * SCALE, yy - 263 * SCALE
            dx += head * ((math.cos(head_angle) - 1) * hx + math.sin(head_angle) * hy)
            dy += head * (-math.sin(head_angle) * hx + (math.cos(head_angle) - 1) * hy)
            sx, sy = xx - 895 * SCALE, yy - 516 * SCALE
            dx += saddle * ((math.cos(support_angle) - 1) * sx + math.sin(support_angle) * sy)
            dy += saddle * (-math.sin(support_angle) * sx + (math.cos(support_angle) - 1) * sy)
            mx, my = np.clip(xx + dx, 0, WIDTH - 1), np.clip(yy + dy, 0, HEIGHT - 1)
            x0, y0 = mx.astype(np.int32), my.astype(np.int32)
            x1, y1 = np.minimum(x0 + 1, WIDTH - 1), np.minimum(y0 + 1, HEIGHT - 1)
            ax, ay = (mx - x0)[..., None], (my - y0)[..., None]
            frame = np.rint(base[y0, x0] * (1 - ax) * (1 - ay) + base[y0, x1] * ax * (1 - ay)
                            + base[y1, x0] * (1 - ax) * ay + base[y1, x1] * ax * ay).astype(np.uint8)
            fixed_max_delta = max(fixed_max_delta, int(np.abs(frame[fixed].astype(int) - base[fixed]).max()))
            encoder.stdin.write(frame.tobytes())
            if frame_index in (0, 36, 54, 78, 108, 132, 162, 191):
                sample = Image.fromarray(frame).resize((640, 360))
                ImageDraw.Draw(sample).text((12, 12), f"{t:.2f}s", fill="white", stroke_width=2, stroke_fill="black")
                samples.append(sample)
    finally:
        encoder.stdin.close()
        result = encoder.wait()
    if result:
        raise SystemExit(f"FFmpeg encoding failed: {result}")
    if fixed_max_delta != 0:
        raise SystemExit("A protected region moved")
    sheet = Image.new("RGB", (1280, 1440))
    for index, sample in enumerate(samples):
        sheet.paste(sample, ((index % 2) * 640, (index // 2) * 360))
    sheet.save(args.contact_sheet, quality=94)
    # A complete decode is distinct from the pre-encode invariant measurement.
    subprocess.run([str(args.ffmpeg), "-v", "error", "-i", str(args.output), "-f", "null", "-"], check=True)
    report = {"schema": 1, "status": "REVIEW_CANDIDATE", "method": "2d-controlled-motion-study",
              "source": SOURCE.relative_to(ROOT).as_posix(), "sourceSha256": SOURCE_SHA,
              "outputSha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
              "width": WIDTH, "height": HEIGHT, "fps": FPS, "frames": FPS * SECONDS,
              "seconds": SECONDS, "audio": False, "paidGenerationCredits": 0,
              "preEncodeProtectedRegionMaxChannelDelta": fixed_max_delta, "fullDecode": "PASS",
              "limitations": ["2D motion study, not a reconstructed 3D mechanism",
                  "Protected-region invariant is measured before lossy encoding",
                  "Human visual review and sound remain required before film acceptance"]}
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
