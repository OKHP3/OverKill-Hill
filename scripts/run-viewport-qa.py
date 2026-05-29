#!/usr/bin/env python3
"""
run-viewport-qa.py — Full browser viewport QA runner
=====================================================
Sets up the required environment (libgbm stub + Playwright flags) and
runs the complete 26-page × 8-viewport Playwright test suite.

Usage:
    python3 scripts/run-viewport-qa.py
    python3 scripts/run-viewport-qa.py --all-screenshots

Output:
    assets/audit/viewport-qa-2026-05-26.json   (machine-readable results)
    assets/audit/screenshots/2026-05-26/        (failure screenshots; all if --all-screenshots)
"""
import os
import sys
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── Environment setup ─────────────────────────────────────────────────────────
# libgbm.so.1 stub compiled from scripts/libgbm_stub.c
# Required because Playwright's bundled Chromium needs libgbm.so.1 which is
# not in the standard Nix library path in this environment.
STUB_DIR = "/tmp/stublibs"
STUB_LIB = os.path.join(STUB_DIR, "libgbm.so.1")

STUB_SRC = r"""
/* Minimal libgbm.so.1 stub — returns null/zero for all calls.
   Headless Chrome with --disable-gpu never invokes GBM functions. */
#include <stddef.h>
#include <stdint.h>
typedef struct gbm_device  gbm_device;
typedef struct gbm_bo      gbm_bo;
typedef struct gbm_surface gbm_surface;
union gbm_bo_handle { void *ptr; int32_t s32; uint32_t u32; int64_t s64; uint64_t u64; };
gbm_device*  gbm_create_device(int fd)                          { return NULL; }
void         gbm_device_destroy(gbm_device *g)                  {}
int          gbm_device_get_fd(gbm_device *g)                   { return -1; }
const char*  gbm_device_get_backend_name(gbm_device *g)         { return "stub"; }
int          gbm_device_is_format_supported(gbm_device *g, uint32_t f, uint32_t u) { return 0; }
int          gbm_device_get_format_modifier_plane_count(gbm_device *g, uint32_t f, uint64_t m) { return 0; }
gbm_bo*      gbm_bo_create(gbm_device *g, uint32_t w, uint32_t h, uint32_t f, uint32_t fl) { return NULL; }
gbm_bo*      gbm_bo_create_with_modifiers(gbm_device *g, uint32_t w, uint32_t h, uint32_t f, const uint64_t *m, unsigned c) { return NULL; }
gbm_bo*      gbm_bo_create_with_modifiers2(gbm_device *g, uint32_t w, uint32_t h, uint32_t f, const uint64_t *m, unsigned c, uint32_t fl) { return NULL; }
gbm_bo*      gbm_bo_import(gbm_device *g, uint32_t t, void *b, uint32_t fl)   { return NULL; }
void         gbm_bo_destroy(gbm_bo *b)                          {}
uint32_t     gbm_bo_get_width(gbm_bo *b)                        { return 0; }
uint32_t     gbm_bo_get_height(gbm_bo *b)                       { return 0; }
uint32_t     gbm_bo_get_stride(gbm_bo *b)                       { return 0; }
uint32_t     gbm_bo_get_stride_for_plane(gbm_bo *b, int p)      { return 0; }
uint32_t     gbm_bo_get_format(gbm_bo *b)                       { return 0; }
uint64_t     gbm_bo_get_modifier(gbm_bo *b)                     { return 0; }
int          gbm_bo_get_plane_count(gbm_bo *b)                  { return 0; }
union gbm_bo_handle gbm_bo_get_handle(gbm_bo *b)               { union gbm_bo_handle h; h.u64=0; return h; }
union gbm_bo_handle gbm_bo_get_handle_for_plane(gbm_bo *b, int p) { union gbm_bo_handle h; h.u64=0; return h; }
int          gbm_bo_get_fd(gbm_bo *b)                           { return -1; }
int          gbm_bo_get_fd_for_plane(gbm_bo *b, int p)          { return -1; }
int          gbm_bo_get_offset(gbm_bo *b, int p)                { return 0; }
gbm_device*  gbm_bo_get_device(gbm_bo *b)                       { return NULL; }
void*        gbm_bo_map(gbm_bo *b, uint32_t x, uint32_t y, uint32_t w, uint32_t h, uint32_t fl, uint32_t *st, void **md) { return NULL; }
void         gbm_bo_unmap(gbm_bo *b, void *md)                  {}
int          gbm_bo_set_user_data(gbm_bo *b, void *d, void(*fn)(gbm_bo*,void*)) { return 0; }
void*        gbm_bo_get_user_data(gbm_bo *b)                    { return NULL; }
gbm_surface* gbm_surface_create(gbm_device *g, uint32_t w, uint32_t h, uint32_t f, uint32_t fl) { return NULL; }
gbm_surface* gbm_surface_create_with_modifiers(gbm_device *g, uint32_t w, uint32_t h, uint32_t f, const uint64_t *m, unsigned c) { return NULL; }
gbm_surface* gbm_surface_create_with_modifiers2(gbm_device *g, uint32_t w, uint32_t h, uint32_t f, const uint64_t *m, unsigned c, uint32_t fl) { return NULL; }
gbm_bo*      gbm_surface_lock_front_buffer(gbm_surface *s)      { return NULL; }
void         gbm_surface_release_buffer(gbm_surface *s, gbm_bo *b) {}
int          gbm_surface_has_free_buffers(gbm_surface *s)       { return 0; }
void         gbm_surface_destroy(gbm_surface *s)                {}
"""

def ensure_stub():
    """Compile the libgbm stub if not already present."""
    Path(STUB_DIR).mkdir(parents=True, exist_ok=True)
    if not Path(STUB_LIB).exists():
        src = Path("/tmp/libgbm_stub.c")
        src.write_text(STUB_SRC)
        ret = os.system(
            f"gcc -shared -fPIC -Wl,-soname,libgbm.so.1 -o {STUB_LIB} {src} 2>/dev/null"
        )
        if ret != 0:
            print("ERROR: failed to compile libgbm stub. Install gcc first.", file=sys.stderr)
            sys.exit(1)
        print(f"  compiled libgbm stub → {STUB_LIB}")
    # Inject into LD_LIBRARY_PATH
    existing = os.environ.get("LD_LIBRARY_PATH", "")
    if STUB_DIR not in existing:
        os.environ["LD_LIBRARY_PATH"] = f"{STUB_DIR}:{existing}" if existing else STUB_DIR
    # Skip Playwright host validation (we supply the missing lib ourselves)
    os.environ["PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS"] = "1"


VIEWPORTS = [
    {"name": "320",  "width": 320,  "height": 568},
    {"name": "375",  "width": 375,  "height": 812},
    {"name": "390",  "width": 390,  "height": 844},
    {"name": "414",  "width": 414,  "height": 896},
    {"name": "768",  "width": 768,  "height": 1024},
    {"name": "1024", "width": 1024, "height": 768},
    {"name": "1280", "width": 1280, "height": 800},
    {"name": "1440", "width": 1440, "height": 900},
]

# Pages: (slug, path) — all 59 published pages verified 2026-05-27
# 10 core + 7 branch hubs + 42 tool-ettes = 59 total
PAGES = [
    # ── Core pages (10) ──────────────────────────────────────────────────────
    ("home",               "/"),
    ("toolbox",            "/toolbox/"),
    ("ecosystem",          "/ecosystem/"),
    ("universe",           "/universe/"),
    ("search",             "/search/"),
    ("about",              "/about/"),
    ("contact",            "/contact/"),
    ("legal",              "/legal/"),
    ("persona",            "/persona/"),
    ("showcase",           "/showcase/"),
    # ── 7 branch hubs ────────────────────────────────────────────────────────
    ("branch-01",          "/toolbox/01-discovered-careers/"),
    ("branch-02",          "/toolbox/02-treasured-finds/"),
    ("branch-03",          "/toolbox/03-tasty-tracker/"),
    ("branch-04",          "/toolbox/04-travelers-guide/"),
    ("branch-05",          "/toolbox/05-organized-life/"),
    ("branch-06",          "/toolbox/06-healthy-bee-ing/"),
    ("branch-07",          "/toolbox/07-identity-known/"),
    # ── Branch 01 — Discovered Careers (6 tool-ettes) ────────────────────────
    ("tool-01a",           "/toolbox/01-discovered-careers/01a-resume-builder/"),
    ("tool-01b",           "/toolbox/01-discovered-careers/01b-resume-customizer/"),
    ("tool-01c",           "/toolbox/01-discovered-careers/01c-career-fitness/"),
    ("tool-01d",           "/toolbox/01-discovered-careers/01d-letter-composer/"),
    ("tool-01e",           "/toolbox/01-discovered-careers/01e-blinkin-tuner/"),
    ("tool-01f",           "/toolbox/01-discovered-careers/01f-career-seeker/"),
    # ── Branch 02 — Treasured Finds (7 tool-ettes) ───────────────────────────
    ("tool-02a",           "/toolbox/02-treasured-finds/02a-personal-librarian/"),
    ("tool-02b",           "/toolbox/02-treasured-finds/02b-decor-detective/"),
    ("tool-02c",           "/toolbox/02-treasured-finds/02c-present-hoarder/"),
    ("tool-02d",           "/toolbox/02-treasured-finds/02d-scentinal-journal/"),
    ("tool-02e",           "/toolbox/02-treasured-finds/02e-spirited-journal/"),
    ("tool-02f",           "/toolbox/02-treasured-finds/02f-supply-haus/"),
    ("tool-02g",           "/toolbox/02-treasured-finds/02g-bag-nabbit/"),
    # ── Branch 03 — Tasty Tracker (5 tool-ettes) ─────────────────────────────
    ("tool-03a",           "/toolbox/03-tasty-tracker/03a-flavor-meister/"),
    ("tool-03b",           "/toolbox/03-tasty-tracker/03b-menu-conductor/"),
    ("tool-03c",           "/toolbox/03-tasty-tracker/03c-wishful-tastes/"),
    ("tool-03d",           "/toolbox/03-tasty-tracker/03d-pantry-shopper/"),
    ("tool-03e",           "/toolbox/03-tasty-tracker/03e-palatably-profiled/"),
    # ── Branch 04 — Traveler's Guide (5 tool-ettes) ──────────────────────────
    ("tool-04a",           "/toolbox/04-travelers-guide/04a-journey-diary/"),
    ("tool-04b",           "/toolbox/04-travelers-guide/04b-itinerary-hacker/"),
    ("tool-04c",           "/toolbox/04-travelers-guide/04c-detour-discoverer/"),
    ("tool-04d",           "/toolbox/04-travelers-guide/04d-dreamland-journeys/"),
    ("tool-04e",           "/toolbox/04-travelers-guide/04e-memento-log/"),
    # ── Branch 05 — Organized Life (6 tool-ettes) ────────────────────────────
    ("tool-05a",           "/toolbox/05-organized-life/05a-task-maestro/"),
    ("tool-05b",           "/toolbox/05-organized-life/05b-thrifty-spender/"),
    ("tool-05c",           "/toolbox/05-organized-life/05c-giftlist-helper/"),
    ("tool-05d",           "/toolbox/05-organized-life/05d-scheduling-wizard/"),
    ("tool-05e",           "/toolbox/05-organized-life/05e-lifestyle-wallboard/"),
    ("tool-05f",           "/toolbox/05-organized-life/05f-neighborly-bazaar/"),
    # ── Branch 06 — Healthy Bee-ing (6 tool-ettes) ───────────────────────────
    ("tool-06a",           "/toolbox/06-healthy-bee-ing/06a-care-check/"),
    ("tool-06b",           "/toolbox/06-healthy-bee-ing/06b-calm-keep/"),
    ("tool-06c",           "/toolbox/06-healthy-bee-ing/06c-snappy-count/"),
    ("tool-06d",           "/toolbox/06-healthy-bee-ing/06d-medi-minder/"),
    ("tool-06e",           "/toolbox/06-healthy-bee-ing/06e-moody-log/"),
    ("tool-06f",           "/toolbox/06-healthy-bee-ing/06f-maven-wise/"),
    # ── Branch 07 — Identity Known (7 tool-ettes) ────────────────────────────
    ("tool-07a",           "/toolbox/07-identity-known/07a-critter-spotter/"),
    ("tool-07b",           "/toolbox/07-identity-known/07b-roost-wrangler/"),
    ("tool-07c",           "/toolbox/07-identity-known/07c-sight-seeker/"),
    ("tool-07d",           "/toolbox/07-identity-known/07d-snap-decoder/"),
    ("tool-07e",           "/toolbox/07-identity-known/07e-motif-muse/"),
    ("tool-07f",           "/toolbox/07-identity-known/07f-maker-matcher/"),
    ("tool-07g",           "/toolbox/07-identity-known/07g-self-fixer/"),
]

BASE_URL = "http://localhost:5000"
SCREENSHOTS_ALL = "--all-screenshots" in sys.argv
import datetime as _dt
import argparse as _ap
_TODAY = _dt.date.today().isoformat()
SCREENSHOTS_DIR = ROOT / "assets" / "audit" / "screenshots" / _TODAY

def _parse_args():
    p = _ap.ArgumentParser(add_help=False)
    p.add_argument("--start", type=int, default=0)
    p.add_argument("--end",   type=int, default=len(PAGES))
    p.add_argument("--batch", type=str, default=None,
                   help="Suffix for partial output filename (e.g. '0', '1', …)")
    p.add_argument("--all-screenshots", action="store_true")
    args, _ = p.parse_known_args()
    return args

LAUNCH_ARGS = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-software-rasterizer",
    "--disable-dbus",
    "--disable-infobars",
    "--disable-extensions",
    "--disable-translate",
    "--disable-sync",
    "--disable-background-networking",
    "--metrics-recording-only",
    "--no-first-run",
    "--safebrowsing-disable-auto-update",
    "--mute-audio",
]


def run_qa(base_url: str = BASE_URL, pages_slice=None, batch_suffix=None):
    from playwright.sync_api import sync_playwright

    pages = PAGES[pages_slice] if pages_slice else PAGES
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    total_issues = 0
    total_warnings = 0

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=LAUNCH_ARGS)

        for page_slug, page_path in pages:
            url = base_url + page_path
            page_result = {
                "page": page_path,
                "slug": page_slug,
                "url": url,
                "viewports": [],
            }

            for vp in VIEWPORTS:
                ctx = browser.new_context(
                    viewport={"width": vp["width"], "height": vp["height"]},
                    device_scale_factor=1,
                )
                page = ctx.new_page()
                issues = []
                warnings = []

                try:
                    resp = page.goto(url, wait_until="domcontentloaded", timeout=15000)
                    time.sleep(0.15)

                    http_status = resp.status if resp else 0
                    if http_status >= 400:
                        issues.append(f"HTTP {http_status}")

                    # ── Check 1: Horizontal overflow ─────────────────────────
                    ov = page.evaluate("""() => {
                        const vw = window.innerWidth;
                        const maxW = Math.max(document.body.scrollWidth,
                                               document.documentElement.scrollWidth);
                        const offenders = [];
                        if (maxW > vw + 4) {
                            for (const el of document.querySelectorAll('*')) {
                                const r = el.getBoundingClientRect();
                                if (r.right > vw + 4) {
                                    offenders.push({
                                        tag: el.tagName.toLowerCase(),
                                        cls: (typeof el.className === 'string'
                                              ? el.className : '').slice(0,50),
                                        id:  el.id.slice(0,20),
                                        right: Math.round(r.right),
                                    });
                                    if (offenders.length >= 4) break;
                                }
                            }
                        }
                        return { maxW, vw, offenders };
                    }""")
                    if ov["maxW"] > ov["vw"] + 4:
                        overflow_px = ov["maxW"] - ov["vw"]
                        top3 = ov["offenders"][:3]
                        who = "; ".join(
                            f"{o['tag']}{'#'+o['id'] if o['id'] else ''}"
                            f"{'.' + o['cls'].split()[0] if o['cls'] else ''}"
                            for o in top3
                        ) or "unknown"
                        issues.append(
                            f"horizontal-overflow +{overflow_px}px (offenders: {who})"
                        )

                    # ── Check 2: Nav toggle at mobile ────────────────────────
                    if vp["width"] < 768:
                        tog = page.query_selector(".nav-toggle")
                        if not tog:
                            warnings.append("no .nav-toggle element found")
                        elif not tog.is_visible():
                            issues.append("nav-toggle present but not visible at mobile width")

                    # ── Check 3: H1 not overflowing ──────────────────────────
                    h1 = page.query_selector("h1")
                    if h1:
                        box = h1.bounding_box()
                        if box and box["x"] + box["width"] > vp["width"] + 4:
                            issues.append("h1 overflows right viewport edge")

                    # ── Check 4: Images not wider than viewport ───────────────
                    img_issues = page.evaluate("""() => {
                        const problems = [];
                        const vw = window.innerWidth;
                        for (const img of document.querySelectorAll('img')) {
                            const r = img.getBoundingClientRect();
                            if (r.width > vw + 8 && r.width > 50) {
                                problems.push({
                                    src: img.src.split('/').pop().slice(0,30),
                                    w: Math.round(r.width),
                                });
                                if (problems.length >= 2) break;
                            }
                        }
                        return problems;
                    }""")
                    for ip in img_issues:
                        issues.append(
                            f"img '{ip['src']}' rendered at {ip['w']}px > viewport"
                        )

                    # ── Check 5: Minimum font size ────────────────────────────
                    tiny = page.evaluate("""() => {
                        const items = [];
                        for (const el of document.querySelectorAll('p, li, td, span')) {
                            const fs = parseFloat(window.getComputedStyle(el).fontSize);
                            if (fs > 0 && fs < 12) {
                                items.push({ fs: Math.round(fs*10)/10,
                                             txt: el.textContent.trim().slice(0,30) });
                                if (items.length >= 2) break;
                            }
                        }
                        return items;
                    }""")
                    for t in tiny:
                        warnings.append(f"text at {t['fs']}px (<12px): '{t['txt']}'")

                    # Screenshot on any issue (or always if --all-screenshots)
                    if issues or SCREENSHOTS_ALL:
                        shot = SCREENSHOTS_DIR / f"{page_slug}-{vp['name']}.png"
                        try:
                            page.screenshot(path=str(shot), full_page=False)
                        except Exception:
                            pass

                except Exception as exc:
                    issues.append(f"playwright-error: {str(exc)[:120]}")

                finally:
                    ctx.close()

                total_issues += len(issues)
                total_warnings += len(warnings)

                sym = "✗" if issues else ("△" if warnings else "✓")
                detail = ("  ".join(issues[:2]) if issues
                          else ("  ".join(warnings[:1]) if warnings else "ok"))
                print(f"  {sym} {page_slug:<24} {vp['name']:>5}px  {detail}")

                page_result["viewports"].append({
                    "viewport": vp["name"],
                    "width": vp["width"],
                    "issues": issues,
                    "warnings": warnings,
                })

            results.append(page_result)

        browser.close()

    # Write JSON report
    out_dir = ROOT / "assets" / "audit"
    out_dir.mkdir(exist_ok=True)
    suffix = f"-batch{batch_suffix}" if batch_suffix is not None else ""
    report_path = out_dir / f"viewport-qa-full{suffix}-{_TODAY}.json"
    report = {
        "date": _TODAY,
        "base_url": base_url,
        "viewports_tested": [v["name"] for v in VIEWPORTS],
        "pages_tested": len(pages),
        "total_combinations": len(pages) * len(VIEWPORTS),
        "total_issues": total_issues,
        "total_warnings": total_warnings,
        "screenshots_dir": str(SCREENSHOTS_DIR.relative_to(ROOT)),
        "environment_note": (
            "libgbm.so.1 stub compiled from scripts/run-viewport-qa.py embedded source. "
            "All Chrome system deps installed via Nix. --disable-gpu mode; "
            "GPU/GBM code paths not exercised."
        ),
        "results": results,
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"Pages tested:        {len(pages)}")
    print(f"Viewports per page:  {len(VIEWPORTS)}")
    print(f"Total combinations:  {len(pages) * len(VIEWPORTS)}")
    print(f"Total issues:        {total_issues}")
    print(f"Total warnings:      {total_warnings}")
    print(f"Report:              {report_path.relative_to(ROOT)}")
    print(f"Screenshots:         {SCREENSHOTS_DIR.relative_to(ROOT)}/")

    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    _args = _parse_args()
    _start = _args.start
    _end   = _args.end
    _batch = _args.batch
    print("Setting up libgbm stub…")
    ensure_stub()
    _page_slice = slice(_start, _end)
    _n = len(PAGES[_page_slice])
    print(f"Starting Playwright QA: {_n} pages (indices {_start}–{_end-1}) × {len(VIEWPORTS)} viewports\n")
    sys.exit(run_qa(pages_slice=_page_slice, batch_suffix=_batch))
