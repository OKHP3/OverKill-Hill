#!/usr/bin/env python3
"""
wire-illustrations.py
Idempotent script: wires each tool-ette's SVG illustration into its HTML page.

For each of the 40 tool-ette pages it:
  1. Updates og:image (content, width→800, height→534, type→image/svg+xml)
     and og:image:alt to match the SVG aria-label description
  2. Updates twitter:image to match
  3. Updates JSON-LD "image" field if present
  4. Replaces the <div class="hero-visual"> GPT-PNG block with the SVG illustration,
     OR inserts a <figure class="tool-illustration"> after <p class="tool-helper">
     on older pages that use that pattern.
  5. Skip if already wired (idempotent guard: SVG path already in page).
"""
import os, re

BASE_URL = "https://glee-fully.tools"
SVG_BASE = "/assets/img/tool-ettes"
SVG_URL_BASE = BASE_URL + "/assets/img/tool-ettes"

# slug → (display name, aria-label description, page path)
TOOLS = {
    "01a-resume-builder": (
        "Resume Builder",
        "A retro-bright resume document with structured Contact, Summary, Experience, Education sections in a paper card layout",
        "toolbox/01-discovered-careers/01a-resume-builder/index.html",
    ),
    "01b-resume-customizer": (
        "Resume Customizer",
        "A retro-bright split-screen showing a job description matched against a tailored resume with keyword highlighting and match score",
        "toolbox/01-discovered-careers/01b-resume-customizer/index.html",
    ),
    "01c-career-fitness": (
        "Career Fitness",
        "A retro-bright career fitness dashboard showing a skills radar chart and professional development checklist",
        "toolbox/01-discovered-careers/01c-career-fitness/index.html",
    ),
    "01d-letter-composer": (
        "Letter Composer",
        "A retro-bright cover letter document editor with a personalized letter, structure prompts and tone meter",
        "toolbox/01-discovered-careers/01d-letter-composer/index.html",
    ),
    "01e-blinkin-tuner": (
        "Blinkin Tuner",
        "A retro-bright LinkedIn profile optimization dashboard showing profile strength meter, keyword density, and section improvement checklist",
        "toolbox/01-discovered-careers/01e-blinkin-tuner/index.html",
    ),
    "02a-personal-librarian": (
        "Personal Librarian",
        "A retro-bright bookshelf dashboard showing a reading list with status badges, genre filters, and a book recommendation panel",
        "toolbox/02-treasured-finds/02a-personal-librarian/index.html",
    ),
    "02b-decor-detective": (
        "Decor Detective",
        "A retro-bright home decor moodboard with room swatches, style cards and a product sourcing panel",
        "toolbox/02-treasured-finds/02b-decor-detective/index.html",
    ),
    "02c-present-hoarder": (
        "Present Hoarder",
        "A retro-bright gift tracking board with occasion cards, wishlist items, and a budget progress bar",
        "toolbox/02-treasured-finds/02c-present-hoarder/index.html",
    ),
    "02d-scentinal-journal": (
        "Scentinal Journal",
        "A retro-bright fragrance journal showing scent profile radar, notes cards and mood pairing wheel",
        "toolbox/02-treasured-finds/02d-scentinal-journal/index.html",
    ),
    "02e-spirited-journal": (
        "Spirited Journal",
        "A retro-bright drinks journal showing tasting notes, bottle rating cards and flavour wheel",
        "toolbox/02-treasured-finds/02e-spirited-journal/index.html",
    ),
    "02f-supply-haus": (
        "Supply Haus",
        "A retro-bright home inventory dashboard showing stock levels, low-alert badges and reorder list",
        "toolbox/02-treasured-finds/02f-supply-haus/index.html",
    ),
    "02g-bag-nabbit": (
        "Bag Nabbit",
        "A retro-bright packing list with categorised items, trip weather strip and tick-off progress bar",
        "toolbox/02-treasured-finds/02g-bag-nabbit/index.html",
    ),
    "03a-flavor-meister": (
        "Flavor Meister",
        "A retro-bright flavour profile card showing taste radar, ingredient pairing tiles and cuisine badge",
        "toolbox/03-tasty-tracker/03a-flavor-meister/index.html",
    ),
    "03c-wishful-tastes": (
        "Wishful Tastes",
        "A retro-bright restaurant wishlist with cards showing cuisine type, price band and neighbourhood tags",
        "toolbox/03-tasty-tracker/03c-wishful-tastes/index.html",
    ),
    "03d-pantry-shopper": (
        "Pantry Shopper",
        "A retro-bright pantry inventory grid with stock-level bars, aisle grouping and smart shopping list",
        "toolbox/03-tasty-tracker/03d-pantry-shopper/index.html",
    ),
    "03e-palatably-profiled": (
        "Palatably Profiled",
        "A retro-bright dietary profile card showing allergen badges, cuisine preferences and nutrition targets",
        "toolbox/03-tasty-tracker/03e-palatably-profiled/index.html",
    ),
    "04a-journey-diary": (
        "Journey Diary",
        "A retro-bright travel journal spread showing map pins, daily log entries and photo caption cards",
        "toolbox/04-travelers-guide/04a-journey-diary/index.html",
    ),
    "04b-itinerary-hacker": (
        "Itinerary Hacker",
        "A retro-bright trip itinerary timeline showing day-by-day activities, transit blocks and budget bar",
        "toolbox/04-travelers-guide/04b-itinerary-hacker/index.html",
    ),
    "04c-detour-discoverer": (
        "Detour Discoverer",
        "A retro-bright route map with off-the-beaten-track stop cards, distance labels and interest tags",
        "toolbox/04-travelers-guide/04c-detour-discoverer/index.html",
    ),
    "04d-dreamland-journeys": (
        "Dreamland Journeys",
        "A retro-bright travel wishlist with destination cards, bucket-list tags and savings progress bars",
        "toolbox/04-travelers-guide/04d-dreamland-journeys/index.html",
    ),
    "04e-memento-log": (
        "Memento Log",
        "A retro-bright souvenir and memory log showing item cards with origin tags, photo placeholders and story captions",
        "toolbox/04-travelers-guide/04e-memento-log/index.html",
    ),
    "05a-task-maestro": (
        "Task Maestro",
        "A retro-bright task board showing kanban columns for To Do, In Progress and Done with priority badges",
        "toolbox/05-organized-life/05a-task-maestro/index.html",
    ),
    "05b-thrifty-spender": (
        "Thrifty Spender",
        "A retro-bright personal budget dashboard with category spending bars, savings goal tracker and monthly summary",
        "toolbox/05-organized-life/05b-thrifty-spender/index.html",
    ),
    "05c-giftlist-helper": (
        "Giftlist Helper",
        "A retro-bright gift organizer showing a person-by-person gift list with budget tracking bars and smart suggestion panel",
        "toolbox/05-organized-life/05c-giftlist-helper/index.html",
    ),
    "05d-scheduling-wizard": (
        "Scheduling Wizard",
        "A retro-bright weekly calendar showing color-coded time blocks for work, personal and health events with conflict detector",
        "toolbox/05-organized-life/05d-scheduling-wizard/index.html",
    ),
    "05e-lifestyle-wallboard": (
        "Lifestyle Wallboard",
        "A retro-bright habit tracker wallboard with daily tick columns, streak counters and motivational progress rings",
        "toolbox/05-organized-life/05e-lifestyle-wallboard/index.html",
    ),
    "05f-neighborly-bazaar": (
        "Neighborly Bazaar",
        "A retro-bright neighbourhood marketplace board showing listing cards with price tags, category badges and location pins",
        "toolbox/05-organized-life/05f-neighborly-bazaar/index.html",
    ),
    "06a-care-check": (
        "Care Check",
        "A retro-bright self-care checklist with mood tracker, habit tick columns and weekly wellbeing score",
        "toolbox/06-healthy-bee-ing/06a-care-check/index.html",
    ),
    "06b-calm-keep": (
        "Calm Keep",
        "A retro-bright mindfulness log showing meditation timer, breathing exercise cards and calm-streak counter",
        "toolbox/06-healthy-bee-ing/06b-calm-keep/index.html",
    ),
    "06c-snappy-count": (
        "Snappy Count",
        "A retro-bright calorie and macro tracker showing daily intake bars, meal log cards and nutrition targets",
        "toolbox/06-healthy-bee-ing/06c-snappy-count/index.html",
    ),
    "06d-medi-minder": (
        "Medi Minder",
        "A retro-bright medication schedule showing pill cards with time slots, refill alerts and adherence progress bar",
        "toolbox/06-healthy-bee-ing/06d-medi-minder/index.html",
    ),
    "06e-moody-log": (
        "Moody Log",
        "A retro-bright mood journal showing daily emotion cards, color-coded calendar and trend chart",
        "toolbox/06-healthy-bee-ing/06e-moody-log/index.html",
    ),
    "06f-maven-wise": (
        "Maven Wise",
        "A retro-bright health knowledge dashboard with topic cards, source quality badges and personal notes panel",
        "toolbox/06-healthy-bee-ing/06f-maven-wise/index.html",
    ),
    "07a-critter-spotter": (
        "Critter Spotter",
        "A retro-bright wildlife observation log showing species cards, habitat tags, sighting map pins and identification tips",
        "toolbox/07-identity-known/07a-critter-spotter/index.html",
    ),
    "07b-roost-wrangler": (
        "Roost Wrangler",
        "A retro-bright bird watching log with species life-list, habitat filter badges and sighting count bars",
        "toolbox/07-identity-known/07b-roost-wrangler/index.html",
    ),
    "07c-sight-seeker": (
        "Sight Seeker",
        "A retro-bright astronomy observation log showing celestial object cards, sky condition ratings and equipment notes",
        "toolbox/07-identity-known/07c-sight-seeker/index.html",
    ),
    "07d-snap-decoder": (
        "Snap Decoder",
        "A retro-bright photo analysis panel showing scene identification cards, composition tips and subject recognition tags",
        "toolbox/07-identity-known/07d-snap-decoder/index.html",
    ),
    "07e-motif-muse": (
        "Motif Muse",
        "A retro-bright pattern and motif inspiration board with style cards, color palette chips and design origin notes",
        "toolbox/07-identity-known/07e-motif-muse/index.html",
    ),
    "07f-maker-matcher": (
        "Maker Matcher",
        "A retro-bright craft supply matcher showing material cards, project tags, skill level badges and tool checklist",
        "toolbox/07-identity-known/07f-maker-matcher/index.html",
    ),
    "07g-self-fixer": (
        "Self Fixer",
        "A retro-bright DIY repair guide showing a step-by-step fix-it flow with numbered instruction cards, tool list, difficulty rating and safety checklist",
        "toolbox/07-identity-known/07g-self-fixer/index.html",
    ),
}

# ── helpers ───────────────────────────────────────────────────────────────────

def svg_url_absolute(slug):
    return SVG_URL_BASE + "/" + slug + "-illustration.svg"

def svg_path_relative(slug):
    return SVG_BASE + "/" + slug + "-illustration.svg"

def update_og_image(html, slug, display_name, aria_label):
    """Replace og:image block (content + width + height) with SVG values."""
    abs_url = svg_url_absolute(slug)

    # Update og:image content
    html = re.sub(
        r'(<meta\s+property="og:image"\s+content=")[^"]*(")',
        r'\g<1>' + abs_url + r'\2',
        html
    )
    # Update og:image:width
    html = re.sub(
        r'(<meta\s+property="og:image:width"\s+content=")[^"]*(")',
        r'\g<1>800\2',
        html
    )
    # Update og:image:height
    html = re.sub(
        r'(<meta\s+property="og:image:height"\s+content=")[^"]*(")',
        r'\g<1>534\2',
        html
    )
    # Update og:image:alt
    html = re.sub(
        r'(<meta\s+property="og:image:alt"\s+content=")[^"]*(")',
        r'\g<1>' + display_name + " — illustration" + r'\2',
        html
    )
    # Remove og:image:type if present (will re-add as svg+xml)
    html = re.sub(r'\s*<meta\s+property="og:image:type"[^/]*/>\n?', '', html)
    # Inject og:image:type after og:image:height
    html = re.sub(
        r'(<meta\s+property="og:image:height"[^/]*/>)',
        r'\1\n    <meta property="og:image:type" content="image/svg+xml" />',
        html
    )
    return html

def update_twitter_image(html, slug):
    """Point twitter:image at the SVG."""
    abs_url = svg_url_absolute(slug)
    html = re.sub(
        r'(<meta\s+name="twitter:image"\s+content=")[^"]*(")',
        r'\g<1>' + abs_url + r'\2',
        html
    )
    return html

def update_jsonld_image(html, slug):
    """Update JSON-LD "image" field if it contains a .png reference."""
    abs_url = svg_url_absolute(slug)
    # Match "image": "..." patterns inside JSON-LD scripts
    html = re.sub(
        r'("image":\s*")https://glee-fully\.tools/assets/img/[^"]*\.png(")',
        r'\g<1>' + abs_url + r'\2',
        html
    )
    return html

def replace_hero_visual(html, slug, display_name, aria_label):
    """
    Replace the <div class="hero-visual"> block that contains a GPT PNG
    with the SVG illustration.
    """
    rel_path = svg_path_relative(slug)
    new_block = (
        '<div class="hero-visual reveal-on-scroll" aria-hidden="true">\n'
        '              <img\n'
        '                src="' + rel_path + '"\n'
        '                alt="' + display_name + ' — illustration"\n'
        '                class="glee-hero-img" width="800" height="534" loading="eager" decoding="async"\n'
        '               fetchpriority="high" />\n'
        '            </div>'
    )
    # Match the whole hero-visual div (non-greedy across lines)
    pattern = r'<div class="hero-visual[^"]*"[^>]*>.*?</div>'
    replaced, n = re.subn(pattern, new_block, html, count=1, flags=re.DOTALL)
    return replaced, n > 0

def insert_figure_after_tool_helper(html, slug, display_name, aria_label):
    """
    For older pages that have a <p class="tool-helper"> but no hero-visual,
    insert a <figure class="tool-illustration"> after it.
    """
    rel_path = svg_path_relative(slug)
    figure_block = (
        '\n\n      <figure class="tool-illustration">\n'
        '        <img src="' + rel_path + '"\n'
        '             alt="Illustration of ' + display_name + '" loading="lazy" decoding="async" width="800" height="534" >\n'
        '      </figure>'
    )
    # Insert after closing </p> that follows class="tool-helper"
    pattern = r'(<p class="tool-helper">.*?</p>)'
    replaced, n = re.subn(pattern, r'\1' + figure_block, html, count=1, flags=re.DOTALL)
    return replaced, n > 0

def replace_tool_hero_visual(html, slug, display_name, aria_label):
    """Replace <div class="tool-hero-visual"> block (blinkin-tuner pattern)."""
    rel_path = svg_path_relative(slug)
    new_block = (
        '<div class="tool-hero-visual">\n'
        '          <img\n'
        '            src="' + rel_path + '"\n'
        '            alt="' + display_name + ' — illustration"\n'
        '            loading="lazy"\n'
        '            width="800"\n'
        '            height="534"\n'
        '          />\n'
        '        </div>'
    )
    pattern = r'<div class="tool-hero-visual">.*?</div>'
    replaced, n = re.subn(pattern, new_block, html, count=1, flags=re.DOTALL)
    return replaced, n > 0

def replace_existing_figure(html, slug, display_name, aria_label):
    """
    Replace an existing <figure> that contains a PNG illustration placeholder.
    Handles: tool-ette-hero, tool-visual, tool-ette-illustration, tool-illustration variants.
    """
    rel_path = svg_path_relative(slug)
    # Match any figure with a class containing 'tool' that has a PNG src inside it
    pattern = r'(<figure\s+[^>]*class="(?:tool[^"]*)"[^>]*>)\s*(?:<!--[^>]*-->)?\s*<img[^>]+\.png[^>]*/?\s*>\s*(</figure>)'
    new_fig = (
        r'\1\n'
        '        <img src="' + rel_path + '"\n'
        '             alt="Illustration of ' + display_name + '" loading="lazy" decoding="async" width="800" height="534" >\n'
        '      ' + r'\2'
    )
    replaced, n = re.subn(pattern, new_fig, html, count=1, flags=re.DOTALL)
    return replaced, n > 0

def replace_existing_figure_with_section(html, slug, display_name, aria_label):
    """
    Replace a <section class="content-section tool-ette-visual"> that contains a figure/img.
    (memento-log pattern)
    """
    rel_path = svg_path_relative(slug)
    new_section = (
        '<!-- Illustration -->\n'
        '      <section class="content-section tool-ette-visual">\n'
        '        <div class="container">\n'
        '          <figure class="tool-illustration">\n'
        '            <img\n'
        '              src="' + rel_path + '"\n'
        '              alt="Illustration of ' + display_name + '"\n'
        '              loading="lazy" decoding="async" width="800" height="534" />\n'
        '          </figure>\n'
        '        </div>\n'
        '      </section>'
    )
    pattern = r'<!-- Illustration -->\s*<section class="content-section tool-ette-visual">.*?</section>'
    replaced, n = re.subn(pattern, new_section, html, count=1, flags=re.DOTALL)
    return replaced, n > 0

def insert_figure_before_content_block(html, slug, display_name, aria_label):
    """
    Fallback: insert illustration before the first <section class="content-block"
    or <section class="section content-section"> that follows the hero header.
    """
    rel_path = svg_path_relative(slug)
    figure_block = (
        '\n      <figure class="tool-illustration">\n'
        '        <img src="' + rel_path + '"\n'
        '             alt="Illustration of ' + display_name + '" loading="lazy" decoding="async" width="800" height="534" >\n'
        '      </figure>\n\n'
    )
    pattern = r'(<section class="(?:content-block|section content-section)")'
    replaced, n = re.subn(pattern, figure_block + r'\1', html, count=1, flags=re.DOTALL)
    return replaced, n > 0

def insert_figure_before_any_content_section(html, slug, display_name, aria_label):
    """
    Broader fallback: insert before any section that looks like main content.
    """
    rel_path = svg_path_relative(slug)
    figure_block = (
        '\n\n      <figure class="tool-illustration">\n'
        '        <img src="' + rel_path + '"\n'
        '             alt="Illustration of ' + display_name + '" loading="lazy" decoding="async" width="800" height="534" >\n'
        '      </figure>\n\n'
    )
    # Match first section after the hero that has content
    pattern = r'(<section(?:\s+class="[^"]*(?:content-section|tool-ette-section)[^"]*"|\s+aria-labelledby="[^"]*")[^>]*>)'
    replaced, n = re.subn(pattern, figure_block + r'\1', html, count=1, flags=re.DOTALL)
    return replaced, n > 0

# ── main ──────────────────────────────────────────────────────────────────────

updated = []
skipped = []
errors = []

for slug, (display_name, aria_label, page_path) in TOOLS.items():
    if not os.path.exists(page_path):
        errors.append(f"  ✗  {page_path} — FILE NOT FOUND")
        continue

    with open(page_path, encoding="utf-8") as f:
        html = f.read()

    # Idempotent guard: skip if SVG already wired
    if slug + "-illustration.svg" in html:
        skipped.append(f"  ·  {slug}  (already wired)")
        continue

    original = html

    # 1. Update meta tags
    html = update_og_image(html, slug, display_name, aria_label)
    html = update_twitter_image(html, slug)
    html = update_jsonld_image(html, slug)

    # 2. Wire illustration into page body
    wired = False
    if '<div class="hero-visual' in html:
        html, wired = replace_hero_visual(html, slug, display_name, aria_label)
    if not wired and '<div class="tool-hero-visual">' in html:
        html, wired = replace_tool_hero_visual(html, slug, display_name, aria_label)
    if not wired and '<!-- Illustration -->' in html and 'tool-ette-visual' in html:
        html, wired = replace_existing_figure_with_section(html, slug, display_name, aria_label)
    if not wired and 'class="tool-' in html and '.png' in html:
        html, wired = replace_existing_figure(html, slug, display_name, aria_label)
    if not wired and '<p class="tool-helper">' in html:
        html, wired = insert_figure_after_tool_helper(html, slug, display_name, aria_label)
    if not wired:
        html, wired = insert_figure_before_content_block(html, slug, display_name, aria_label)
    if not wired:
        html, wired = insert_figure_before_any_content_section(html, slug, display_name, aria_label)

    if not wired:
        errors.append(f"  ✗  {slug} — could not find insertion point in {page_path}")
        continue

    if html == original:
        skipped.append(f"  ·  {slug}  (no change)")
        continue

    with open(page_path, "w", encoding="utf-8") as f:
        f.write(html)
    updated.append(f"  ✓  {slug}")

print(f"\nUpdated  ({len(updated)}):")
for s in updated:
    print(s)
if skipped:
    print(f"\nSkipped  ({len(skipped)}) — already wired or no change:")
    for s in skipped:
        print(s)
if errors:
    print(f"\nErrors  ({len(errors)}):")
    for s in errors:
        print(s)
    raise SystemExit(1)

print(f"\n✅  Done. {len(updated)} pages updated, {len(skipped)} skipped.")
