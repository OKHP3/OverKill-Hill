#!/usr/bin/env python3
"""Inject a "Keep exploring" nav tray into all 42 Tool-ette pages.

Idempotent: presence of <!-- AUTOGEN:KEEP-EXPLORING --> marker skips the page.
Injects immediately before </main> on each tool-ette page.
"""
from pathlib import Path
import html as html_lib

ROOT = Path(__file__).parent.parent

# Branch metadata: (branch_slug, branch_display_name, [toolette_slugs])
BRANCHES = [
    ("01-discovered-careers", "Discovered Careers", [
        ("01a-resume-builder",      "Resume Builder"),
        ("01b-resume-customizer",   "Resume Customizer"),
        ("01c-career-fitness",      "Career Fitness"),
        ("01d-letter-composer",     "Letter Composer"),
        ("01e-blinkin-tuner",       "bLinkIn Tuner"),
        ("01f-career-seeker",       "Career Seeker"),
    ]),
    ("02-treasured-finds", "Treasured Finds", [
        ("02a-personal-librarian",  "Personal Librarian"),
        ("02b-decor-detective",     "Decor Detective"),
        ("02c-present-hoarder",     "Present Hoarder"),
        ("02d-scentinal-journal",   "Scentinal Journal"),
        ("02e-spirited-journal",    "Spirited Journal"),
        ("02f-supply-haus",         "Supply Haus"),
        ("02g-bag-nabbit",          "Bag Nabbit"),
    ]),
    ("03-tasty-tracker", "Tasty Tracker", [
        ("03a-flavor-meister",      "Flavor Meister"),
        ("03b-menu-conductor",      "Menu Conductor"),
        ("03c-wishful-tastes",      "Wishful Tastes"),
        ("03d-pantry-shopper",      "Pantry Shopper"),
        ("03e-palatably-profiled",  "Palatably Profiled"),
    ]),
    ("04-travelers-guide", "Traveler\u2019s Guide", [
        ("04a-journey-diary",       "Journey Diary"),
        ("04b-itinerary-hacker",    "Itinerary Hacker"),
        ("04c-detour-discoverer",   "Detour Discoverer"),
        ("04d-dreamland-journeys",  "Dreamland Journeys"),
        ("04e-memento-log",         "Memento Log"),
    ]),
    ("05-organized-life", "Organized Life", [
        ("05a-task-maestro",        "Task Maestro"),
        ("05b-thrifty-spender",     "Thrifty Spender"),
        ("05c-giftlist-helper",     "Giftlist Helper"),
        ("05d-scheduling-wizard",   "Scheduling Wizard"),
        ("05e-lifestyle-wallboard", "Lifestyle Wallboard"),
        ("05f-neighborly-bazaar",   "Neighborly Bazaar"),
    ]),
    ("06-healthy-bee-ing", "Healthy Bee\u2011ing", [
        ("06a-care-check",          "Care Check"),
        ("06b-calm-keep",           "Calm Keep"),
        ("06c-snappy-count",        "Snappy Count"),
        ("06d-medi-minder",         "Medi Minder"),
        ("06e-moody-log",           "Moody Log"),
        ("06f-maven-wise",          "Maven Wise"),
    ]),
    ("07-identity-known", "Identity Known", [
        ("07a-critter-spotter",     "Critter Spotter"),
        ("07b-roost-wrangler",      "Roost Wrangler"),
        ("07c-sight-seeker",        "Sight Seeker"),
        ("07d-snap-decoder",        "Snap Decoder"),
        ("07e-motif-muse",          "Motif Muse"),
        ("07f-maker-matcher",       "Maker Matcher"),
        ("07g-self-fixer",          "Self Fixer"),
    ]),
]

MARKER_START = "<!-- AUTOGEN:KEEP-EXPLORING -->"
MARKER_END   = "<!-- /AUTOGEN:KEEP-EXPLORING -->"
INSERT_BEFORE_OPTIONS = ["    </main>", "  </main>"]


def make_tray(branch_slug, branch_name, toolettes, current_idx):
    """Return the HTML block for the keep-exploring tray."""
    current_slug, current_name = toolettes[current_idx]
    prev_item = toolettes[current_idx - 1] if current_idx > 0 else None
    next_item = toolettes[current_idx + 1] if current_idx < len(toolettes) - 1 else None

    branch_url = f"/toolbox/{branch_slug}/"

    prev_html = ""
    if prev_item:
        prev_slug, prev_name = prev_item
        prev_html = (
            f'      <li class="keep-exploring__item keep-exploring__prev">\n'
            f'        <a href="/toolbox/{branch_slug}/{prev_slug}/" class="keep-exploring__link keep-exploring__link--prev">\n'
            f'          <span class="keep-exploring__dir" aria-hidden="true">&#8592;</span>\n'
            f'          <span class="keep-exploring__label">Previous</span>\n'
            f'          <span class="keep-exploring__name">{html_lib.escape(prev_name)}</span>\n'
            f'        </a>\n'
            f'      </li>\n'
        )

    next_html = ""
    if next_item:
        next_slug, next_name = next_item
        next_html = (
            f'      <li class="keep-exploring__item keep-exploring__next">\n'
            f'        <a href="/toolbox/{branch_slug}/{next_slug}/" class="keep-exploring__link keep-exploring__link--next">\n'
            f'          <span class="keep-exploring__dir" aria-hidden="true">&#8594;</span>\n'
            f'          <span class="keep-exploring__label">Next</span>\n'
            f'          <span class="keep-exploring__name">{html_lib.escape(next_name)}</span>\n'
            f'        </a>\n'
            f'      </li>\n'
        )

    return (
        f"      {MARKER_START}\n"
        f'      <nav class="keep-exploring" aria-label="Keep exploring">\n'
        f'        <div class="container">\n'
        f'          <p class="keep-exploring__heading">Keep exploring</p>\n'
        f'          <ul class="keep-exploring__list">\n'
        f'            <li class="keep-exploring__item keep-exploring__branch">\n'
        f'              <a href="{html_lib.escape(branch_url)}" class="keep-exploring__link keep-exploring__link--branch">\n'
        f'                <span class="keep-exploring__label">Branch</span>\n'
        f'                <span class="keep-exploring__name">{html_lib.escape(branch_name)}</span>\n'
        f'              </a>\n'
        f'            </li>\n'
        + (f'            {prev_html.strip()}\n' if prev_html else "")
        + (f'            {next_html.strip()}\n' if next_html else "")
        + f'            <li class="keep-exploring__item keep-exploring__toolbox">\n'
        f'              <a href="/toolbox/" class="keep-exploring__link keep-exploring__link--toolbox">\n'
        f'                <span class="keep-exploring__label">Hub</span>\n'
        f'                <span class="keep-exploring__name">The Toolbox</span>\n'
        f'              </a>\n'
        f'            </li>\n'
        f'            <li class="keep-exploring__item keep-exploring__search">\n'
        f'              <a href="/search/" class="keep-exploring__link keep-exploring__link--search">\n'
        f'                <span class="keep-exploring__label">Search</span>\n'
        f'                <span class="keep-exploring__name">All Tools</span>\n'
        f'              </a>\n'
        f'            </li>\n'
        f'          </ul>\n'
        f'        </div>\n'
        f'      </nav>\n'
        f"      {MARKER_END}\n"
    )


total_changed = 0
total_skipped = 0

for branch_slug, branch_name, toolettes in BRANCHES:
    for idx, (toolette_slug, toolette_name) in enumerate(toolettes):
        path = ROOT / "toolbox" / branch_slug / toolette_slug / "index.html"
        if not path.exists():
            print(f"  MISSING: {path}")
            continue

        raw = path.read_bytes()
        text = raw.decode("utf-8-sig")

        if MARKER_START in text:
            total_skipped += 1
            continue

        tray = make_tray(branch_slug, branch_name, toolettes, idx)

        insert_before = next((s for s in INSERT_BEFORE_OPTIONS if s in text), None)
        if insert_before is None:
            print(f"  WARN: </main> not found in {path.relative_to(ROOT)}")
            continue

        text = text.replace(insert_before, tray + insert_before)
        path.write_bytes(text.encode("utf-8"))
        total_changed += 1
        print(f"  INJECTED: {branch_slug}/{toolette_slug}")

print(f"\nDone. {total_changed} injected, {total_skipped} already had tray.")
