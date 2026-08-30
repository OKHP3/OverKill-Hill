#!/usr/bin/env python3
"""inject-toolette-hub.py -- idempotent: injects/updates the AUTOGEN:TOOLETTE-HUB section
on all 7 branch pages with per-tool-ette icon cards.

Branch types:
  A (01, 02) -- already have individual cards; section replaced wholesale
  B (03, 04, 05, 06, 07) -- have list-style ecosystem section; new dedicated section injected
"""
import re
from pathlib import Path

ARROW = "\u2192"

BRANCHES = {
    "01": {
        "file": "toolbox/01-discovered-careers/index.html",
        "name": "Discovered Careers",
        "type": "A",
        "intro": "Six focused GPTs live on this branch. Each one owns a different part of your job\u2011search story.",
        "tools": [
            {"code": "01a", "name": "Resume Builder",
             "icon": "glee-fully-tools-gpt-icon-01a-resume-builder-background-retro-stripe-square-1024.png",
             "purpose": "Build or polish your core resume from scratch or an existing draft.",
             "bestfor": "Starting your job search or refreshing a resume for a new industry.",
             "url": "https://chatgpt.com/g/g-6855e58bf8d48191bf27795f6d5ec23c-resume-builder-by-glee-fully"},
            {"code": "01b", "name": "Resume Customizer",
             "icon": "glee-fully-tools-gpt-icon-01b-resume-customizer-background-retro-stripe-square-1024.png",
             "purpose": "Turn a general resume into a role-ready version for a specific job post.",
             "bestfor": "Tailoring your resume when applying to multiple jobs with different requirements.",
             "url": "https://chatgpt.com/g/g-685a97b415848191a6ad3aaa42a630f7-resume-customizer-by-glee-fully"},
            {"code": "01c", "name": "Career Fitness",
             "icon": "glee-fully-tools-gpt-icon-01c-career-fitness-background-retro-stripe-square-1024.png",
             "purpose": "Map your skills, benchmark salary ranges, and chart your growth path.",
             "bestfor": "When you\u2019re unsure what roles you qualify for or where to invest in new skills.",
             "url": "https://chatgpt.com/g/g-685a9c19ec2c8191a08945a385a23f4c-career-fitness-by-glee-fully"},
            {"code": "01d", "name": "Letter Composer",
             "icon": "glee-fully-tools-gpt-icon-01d-letter-composer-background-retro-stripe-square-1024.png",
             "purpose": "Draft cover letters that sound like you, not a template.",
             "bestfor": "Any application where a personalized cover letter gives you an edge.",
             "url": "https://chatgpt.com/g/g-685a9cee3a6481919a7cc5ee05065aae-letter-composer-by-glee-fully"},
            {"code": "01e", "name": "bLinkIn Tuner",
             "icon": "glee-fully-tools-gpt-icon-01e-b-link-in-tuner-background-retro-stripe-square-1024.png",
             "purpose": "Refresh your LinkedIn headline, About, and roles with keyword-rich clarity.",
             "bestfor": "When your profile isn\u2019t attracting recruiters or feels stale.",
             "url": "https://chatgpt.com/g/g-685aa123a3f4819188f2c80fe523d402-blinkn-tuner-by-glee-fully"},
            {"code": "01f", "name": "Career Seeker",
             "icon": "glee-fully-tools-gpt-icon-01f-career-seeker-background-retro-stripe-square-1024.png",
             "purpose": "Keep your whole job search organized in one trackable, living dashboard.",
             "bestfor": "Active job seekers juggling multiple applications, follow-ups, and interviews.",
             "url": "https://chatgpt.com/g/g-685aa234bfe88191b89b1c6949ced7f7-career-seeker-by-glee-fully"},
        ],
    },
    "02": {
        "file": "toolbox/02-treasured-finds/index.html",
        "name": "Treasured Finds",
        "type": "A",
        "intro": "Seven focused Tool\u2011ettes live on this branch, each tuned to a specific kind of treasure.",
        "tools": [
            {"code": "02a", "name": "Personal Librarian",
             "icon": "glee-fully-tools-gpt-icon-02a-personal-librarian-background-retro-stripe-square-1024.png",
             "purpose": "Track every book you\u2019ve read, own, or want \u2014 rated, tagged, and organized.",
             "bestfor": "Bibliophiles who want to remember what they\u2019ve read and plan their next reads.",
             "url": "https://chatgpt.com/g/g-68576b99c56c81918f1210a5442ab558-personal-librarian-by-glee-fully"},
            {"code": "02b", "name": "Decor Detective",
             "icon": "glee-fully-tools-gpt-icon-02b-decor-detective-background-retro-stripe-square-1024.png",
             "purpose": "Catalog holiday and seasonal d\u00e9cor by theme, room, and storage spot.",
             "bestfor": "Anyone who forgets what\u2019s in the bins until they\u2019re knee-deep in ornaments.",
             "url": "https://chatgpt.com/g/g-685aeec6991481918b003881d1da83ad-decor-detective-by-glee-fully"},
            {"code": "02c", "name": "Present Hoarder",
             "icon": "glee-fully-tools-gpt-icon-02c-present-hoarder-background-retro-stripe-square-1024.png",
             "purpose": "Log gifts by person, event, and hiding place so surprises stay surprising.",
             "bestfor": "Early shoppers and gift-stashers who need to track what\u2019s bought, wrapped, and where.",
             "url": "https://chatgpt.com/g/g-685af65a822881919690d7410a122984-present-hoarder-by-glee-fully"},
            {"code": "02d", "name": "Scentinal Journal",
             "icon": "glee-fully-tools-gpt-icon-02d-scentinal-journal-background-retro-stripe-square-1024.png",
             "purpose": "Log candles, wax melts, and diffusers with burn notes and reorder flags.",
             "bestfor": "Scent enthusiasts who want to remember what to reorder and what to skip.",
             "url": "https://chatgpt.com/g/g-685b052f31b481919fa71909e237fcf5-scentinal-journal-by-glee-fully"},
            {"code": "02e", "name": "Spirited Journal",
             "icon": "glee-fully-tools-gpt-icon-02e-spirited-journal-background-retro-stripe-square-1024.png",
             "purpose": "A story-first log for wine, whiskey, and spirits with tasting notes and gifting history.",
             "bestfor": "Collectors who want to remember what they opened, shared, and loved.",
             "url": "https://chatgpt.com/g/g-68588c7cfd3c8191ae826e1ca767f3ca-spirited-journal-by-glee-fully"},
            {"code": "02f", "name": "Supply Haus",
             "icon": "glee-fully-tools-gpt-icon-02f-supply-haus-background-retro-stripe-square-1024.png",
             "purpose": "Inventory your craft supplies by material, color, quantity, and project.",
             "bestfor": "Crafters who keep buying supplies they already own because they can\u2019t find what they have.",
             "url": "https://chatgpt.com/g/g-685b05275c788191afce321ffd49c523-supply-haus-by-glee-fully"},
            {"code": "02g", "name": "Bag Nabbit",
             "icon": "glee-fully-tools-gpt-icon-02g-bag-nabbit-background-retro-stripe-square-1024.png",
             "purpose": "Catalog handbags and totes by style, brand, color, and last-worn date.",
             "bestfor": "Bag lovers who want to rotate intentionally and track wishlist pieces.",
             "url": "https://chatgpt.com/g/g-685e94aa448c81918e8afa4b440bb9cd-bag-nabbit-by-glee-fully"},
        ],
    },
    "03": {
        "file": "toolbox/03-tasty-tracker/index.html",
        "name": "Tasty Tracker",
        "type": "B",
        "intro": "Five focused Tool\u2011ettes live on this branch, each tuned to a different layer of your food life.",
        "tools": [
            {"code": "03a", "name": "Flavor Meister",
             "icon": "glee-fully-tools-gpt-icon-03a-flavor-meister-background-retro-stripe-square-1024.png",
             "purpose": "Your joyful digital recipe box \u2014 log, rate, and remix meals you love.",
             "bestfor": "Adventurous eaters who want a searchable memory of every great meal.",
             "url": "https://chatgpt.com/g/g-685b061620b08191b61d5a2a0e9d87a1-flavor-meister-by-glee-fully"},
            {"code": "03b", "name": "Menu Conductor",
             "icon": "glee-fully-tools-gpt-icon-03b-menu-conductor-background-retro-stripe-square-1024.png",
             "purpose": "Build week-by-week menus and event-ready meal plans around your schedule.",
             "bestfor": "Anyone who dreads the \u2018what\u2019s for dinner?\u2019 question at 5pm every day.",
             "url": "https://chatgpt.com/g/g-685b061acda08191b2e43d4dd4f215a8-menu-conductor-by-glee-fully"},
            {"code": "03c", "name": "Wishful Tastes",
             "icon": "glee-fully-tools-gpt-icon-03c-wishful-tastes-background-retro-stripe-square-1024.png",
             "purpose": "Keep a running list of dream dishes, restaurants, and food events to try.",
             "bestfor": "People with a backlog of saved recommendations they never get around to visiting.",
             "url": "https://chatgpt.com/g/g-685b061efdf0819196e66e6b646da237-wishful-tastes-by-glee-fully"},
            {"code": "03d", "name": "Pantry Shopper",
             "icon": "glee-fully-tools-gpt-icon-03d-pantry-shopper-background-retro-stripe-square-1024.png",
             "purpose": "Turn your pantry inventory and meal plan into a smart grocery list.",
             "bestfor": "Households who want to stop over-buying and make the most of what\u2019s in the fridge.",
             "url": "https://chatgpt.com/g/g-685b06111ae881919036d78bed2af630-pantry-shopper-by-glee-fully"},
            {"code": "03e", "name": "Palatably Profiled",
             "icon": "glee-fully-tools-gpt-icon-03e-palatably-profiled-background-retro-stripe-square-1024.png",
             "purpose": "Build your flavor profile \u2014 dietary needs, preferences, and taste story.",
             "bestfor": "A one-time setup that makes every other Tasty Tracker tool smarter and more personal.",
             "url": "https://chatgpt.com/g/g-685b0623a28081919758078164db9957-palatably-profiled-by-glee-fully"},
        ],
    },
    "04": {
        "file": "toolbox/04-travelers-guide/index.html",
        "name": "Traveler\u2019s Guide",
        "type": "B",
        "intro": "Five focused Tool\u2011ettes live on this branch, each handling a different chapter of your journey.",
        "tools": [
            {"code": "04a", "name": "Journey Diary",
             "icon": "glee-fully-tools-gpt-icon-04a-journey-diary-background-retro-stripe-square-1024.png",
             "purpose": "Guided journaling for before, during, and after every trip.",
             "bestfor": "Travelers who want to remember the feeling of a trip, not just the itinerary.",
             "url": "https://chatgpt.com/g/g-685ef0500ee0819192d0981d558bf490-journey-diary-by-glee-fully"},
            {"code": "04b", "name": "Itinerary Hacker",
             "icon": "glee-fully-tools-gpt-icon-04b-itinerary-hacker-background-retro-stripe-square-1024.png",
             "purpose": "Turn your must-see list and constraints into a realistic day-by-day plan.",
             "bestfor": "Planners who need to balance too many priorities into one doable schedule.",
             "url": "https://chatgpt.com/g/g-685ef056f81481918c55e0b11cba406f-itinerary-hacker-by-glee-fully"},
            {"code": "04c", "name": "Detour Discoverer",
             "icon": "glee-fully-tools-gpt-icon-04c-detour-discoverer-background-retro-stripe-square-1024.png",
             "purpose": "Surface side-quests, layovers, and route-friendly surprises on your path.",
             "bestfor": "Road trippers and flexible travelers who want to find gems off the main path.",
             "url": "https://chatgpt.com/g/g-685ef05b00e881918b840db6cafbc643-detour-discoverer-by-glee-fully"},
            {"code": "04d", "name": "Dreamland Journeys",
             "icon": "glee-fully-tools-gpt-icon-04d-dreamland-journeys-background-retro-stripe-square-1024.png",
             "purpose": "Organize your \u2018someday trips\u2019 wishboard by vibe, season, or companions.",
             "bestfor": "Dreamers who want to turn travel inspiration into an actual plan.",
             "url": "https://chatgpt.com/g/g-685b072fccec8191a595b10991348f30-dreamland-journeys-by-glee-fully"},
            {"code": "04e", "name": "Memento Log",
             "icon": "glee-fully-tools-gpt-icon-04e-memento-log-background-retro-stripe-square-1024.png",
             "purpose": "Capture souvenirs, playlists, and tiny details organized by trip and timeline.",
             "bestfor": "Sentimental travelers who want trip memories that are searchable, not just photos.",
             "url": "https://chatgpt.com/g/g-685b072be58c8191ba386b00b33b93b8-memento-log-by-glee-fully"},
        ],
    },
    "05": {
        "file": "toolbox/05-organized-life/index.html",
        "name": "Organized Life",
        "type": "B",
        "intro": "Six focused Tool\u2011ettes live on this branch, each handling a different slice of everyday life admin.",
        "tools": [
            {"code": "05a", "name": "Task Maestro",
             "icon": "glee-fully-tools-gpt-icon-05a-task-maestro-background-retro-stripe-square-1024.png",
             "purpose": "Organize scattered to-dos into prioritized, printable checklists.",
             "bestfor": "People with tasks across apps and sticky notes who need one clear view.",
             "url": "/toolbox/05-organized-life/05a-task-maestro/"},
            {"code": "05b", "name": "Thrifty Spender",
             "icon": "glee-fully-tools-gpt-icon-05b-thrifty-spender-background-retro-stripe-square-1024.png",
             "purpose": "Map your spending to real-world plans and keep your budget honest.",
             "bestfor": "Anyone who wants to understand where money goes without building a spreadsheet.",
             "url": "/toolbox/05-organized-life/05b-thrifty-spender/"},
            {"code": "05c", "name": "Giftlist Helper",
             "icon": "glee-fully-tools-gpt-icon-05c-giftlist-helper-background-retro-stripe-square-1024.png",
             "purpose": "Track who you\u2019re gifting, what\u2019s bought, and what\u2019s still a maybe.",
             "bestfor": "Gift-givers juggling birthdays, holidays, and \u2018just because\u2019 moments for a long list.",
             "url": "/toolbox/05-organized-life/05c-giftlist-helper/"},
            {"code": "05d", "name": "Scheduling Wizard",
             "icon": "glee-fully-tools-gpt-icon-05d-scheduling-wizard-background-retro-stripe-square-1024.png",
             "purpose": "Turn your availability and events into a clean, conflict-free timeline.",
             "bestfor": "People coordinating multiple calendars who can\u2019t afford to drop the ball.",
             "url": "/toolbox/05-organized-life/05d-scheduling-wizard/"},
            {"code": "05e", "name": "Lifestyle Wallboard",
             "icon": "glee-fully-tools-gpt-icon-05e-lifestyle-wallboard-background-retro-stripe-square-1024.png",
             "purpose": "Build personal dashboards for goals, habits, and what matters this season.",
             "bestfor": "Visual thinkers who want a one-page view of life priorities, not a long list.",
             "url": "/toolbox/05-organized-life/05e-lifestyle-wallboard/"},
            {"code": "05f", "name": "Neighborly Bazaar",
             "icon": "glee-fully-tools-gpt-icon-05f-neighborly-bazaar-background-retro-stripe-square-1024.png",
             "purpose": "Plan what to sell, donate, or gift so your space and budget can breathe.",
             "bestfor": "Anyone doing a seasonal purge, estate clear-out, or too-much-stuff reset.",
             "url": "/toolbox/05-organized-life/05f-neighborly-bazaar/"},
        ],
    },
    "06": {
        "file": "toolbox/06-healthy-bee-ing/index.html",
        "name": "Healthy Bee\u2011ing",
        "type": "B",
        "intro": "Six focused Tool\u2011ettes live on this branch, each addressing a different layer of personal wellness.",
        "tools": [
            {"code": "06a", "name": "Care Check",
             "icon": "glee-fully-tools-gpt-icon-06a-care-check-background-retro-stripe-square-1024.png",
             "purpose": "Triage your symptoms with structured prompts to shape what you bring to a professional.",
             "bestfor": "Anyone heading into a medical appointment who wants to arrive organized, not scattered.",
             "url": "/toolbox/06-healthy-bee-ing/06a-care-check/"},
            {"code": "06b", "name": "Calm Keep",
             "icon": "glee-fully-tools-gpt-icon-06b-calm-keep-background-retro-stripe-square-1024.png",
             "purpose": "Check in on stress, sleep, and micro-movement to steady your day.",
             "bestfor": "People who want a gentle daily wellness rhythm without complex tracking apps.",
             "url": "/toolbox/06-healthy-bee-ing/06b-calm-keep/"},
            {"code": "06c", "name": "Snappy Count",
             "icon": "glee-fully-tools-gpt-icon-06c-snappy-count-background-retro-stripe-square-1024.png",
             "purpose": "Quick, honest nutrition awareness for \u2018what did I actually eat today?\u2019 moments.",
             "bestfor": "Anyone who wants a realistic food picture without obsessive calorie logging.",
             "url": "/toolbox/06-healthy-bee-ing/06c-snappy-count/"},
            {"code": "06d", "name": "Medi Minder",
             "icon": "glee-fully-tools-gpt-icon-06d-medi-minder-background-retro-stripe-square-1024.png",
             "purpose": "Light-touch medication, refill, and side-effect tracking so nothing slips.",
             "bestfor": "People managing multiple medications or new prescriptions who need simple reminders.",
             "url": "/toolbox/06-healthy-bee-ing/06d-medi-minder/"},
            {"code": "06e", "name": "Moody Log",
             "icon": "glee-fully-tools-gpt-icon-06e-moody-log-background-retro-stripe-square-1024.png",
             "purpose": "Track mood patterns across days and weeks to find what\u2019s driving how you feel.",
             "bestfor": "Anyone who wants to understand emotional cycles to share with a therapist or doctor.",
             "url": "/toolbox/06-healthy-bee-ing/06e-moody-log/"},
            {"code": "06f", "name": "Maven Wise",
             "icon": "glee-fully-tools-gpt-icon-06f-maven-wise-background-retro-stripe-square-1024.png",
             "purpose": "Turn complex health research into plain-language summaries you can act on.",
             "bestfor": "People who want to understand a diagnosis or treatment before their next appointment.",
             "url": "/toolbox/06-healthy-bee-ing/06f-maven-wise/"},
        ],
    },
    "07": {
        "file": "toolbox/07-identity-known/index.html",
        "name": "Identity Known",
        "type": "B",
        "intro": "Seven focused Tool\u2011ettes live on this branch, each specializing in a different kind of recognition.",
        "tools": [
            {"code": "07a", "name": "Critter Spotter",
             "icon": "glee-fully-tools-gpt-icon-07a-critter-spotter-background-retro-stripe-square-1024.png",
             "purpose": "ID animals, breeds, and wildlife from a photo with names, trivia, and habitat notes.",
             "bestfor": "Anyone who spots something in the backyard or on a trail and wants a fast answer.",
             "url": "https://chatgpt.com/g/g-68b4fccde1c08191a14ce69219dc8ab3-critter-spotter-by-glee-fully"},
            {"code": "07b", "name": "Roost Wrangler",
             "icon": "glee-fully-tools-gpt-icon-07b-roost-wrangler-background-retro-stripe-square-1024.png",
             "purpose": "Decode homes, furniture, and architecture styles from a photo with design context.",
             "bestfor": "Thrifters, decorators, and curious walkers who want to name what they see.",
             "url": "https://chatgpt.com/g/g-68b4fd1f885481919e71f55d6b2d5106-roost-wrangler-by-glee-fully"},
            {"code": "07c", "name": "Sight Seeker",
             "icon": "glee-fully-tools-gpt-icon-07c-sight-seeker-background-retro-stripe-square-1024.png",
             "purpose": "Recognize scenery, landmarks, and constellations from a photo.",
             "bestfor": "Travelers and stargazers who want to know exactly where \u2014 or what \u2014 they\u2019re looking at.",
             "url": "https://chatgpt.com/g/g-68b4fd573a74819186a27d60efca12ef-sight-seeker-by-glee-fully"},
            {"code": "07d", "name": "Snap Decoder",
             "icon": "glee-fully-tools-gpt-icon-07d-snap-decoder-background-retro-stripe-square-1024.png",
             "purpose": "Interpret screenshots, quotes, error messages, and mystery text.",
             "bestfor": "Anyone confused by a tech message, label, or document they can\u2019t decode alone.",
             "url": "https://chatgpt.com/g/g-68b4fda253c081919161af36ddc20260-snap-decoder-by-glee-fully"},
            {"code": "07e", "name": "Motif Muse",
             "icon": "glee-fully-tools-gpt-icon-07e-motif-muse-background-retro-stripe-square-1024.png",
             "purpose": "Extract color palettes, motifs, and design patterns from any image.",
             "bestfor": "Designers, crafters, and decorators seeking to name or replicate a visual style.",
             "url": "https://chatgpt.com/g/g-68b4fe189cac819189de192afa1854ad-motif-muse-by-glee-fully"},
            {"code": "07f", "name": "Maker Matcher",
             "icon": "glee-fully-tools-gpt-icon-07f-maker-matcher-background-retro-stripe-square-1024.png",
             "purpose": "Name crafts, tools, techniques, and creative hobbies from a photo or description.",
             "bestfor": "Curious makers who want to learn the name of something they spotted online.",
             "url": "https://chatgpt.com/g/g-68b4fe5ea5c88191a2f5f06aeb6fa169-maker-matcher-by-glee-fully"},
            {"code": "07g", "name": "Self Fixer",
             "icon": "glee-fully-tools-gpt-icon-07g-self-fixer-background-retro-stripe-square-1024.png",
             "purpose": "Identify mystery objects, broken parts, and DIY bits so you can fix or replace them.",
             "bestfor": "Handy folks who need to name a component before they can search for a replacement.",
             "url": "https://chatgpt.com/g/g-68b4fe9927c88191991b13e732347ad2-self-fixer-by-glee-fully"},
        ],
    },
}

MARKER_START = "<!-- AUTOGEN:TOOLETTE-HUB:START -->"
MARKER_END   = "<!-- AUTOGEN:TOOLETTE-HUB:END -->"


def make_card(t):
    is_external = t["url"].startswith("http")
    link_attrs  = ' target="_blank" rel="noopener"' if is_external else ""
    cta_label   = "Open in ChatGPT " + ARROW if is_external else "Explore " + t["name"] + " " + ARROW
    return (
        "          <!-- " + t["name"] + " -->\n"
        "          <article class=\"card card--tool-ette\">\n"
        "            <img\n"
        "              src=\"/assets/img/" + t["icon"] + "\"\n"
        "              alt=\"" + t["name"] + " icon\"\n"
        "              class=\"card__tool-icon\"\n"
        "              loading=\"lazy\"\n"
        "              decoding=\"async\"\n"
        "              width=\"80\"\n"
        "              height=\"80\"\n"
        "            />\n"
        "            <h3>#" + t["code"] + " \u2013 " + t["name"] + "</h3>\n"
        "            <p>" + t["purpose"] + "</p>\n"
        "            <p class=\"card__bestfor\"><strong>Best for:</strong> " + t["bestfor"] + "</p>\n"
        "            <p>\n"
        "              <a\n"
        "                href=\"" + t["url"] + "\"\n"
        "                class=\"btn btn-primary\"" + link_attrs + "\n"
        "                >" + cta_label + "</a\n"
        "              >\n"
        "            </p>\n"
        "          </article>"
    )


def make_hub_section(branch):
    cards = "\n\n".join(make_card(t) for t in branch["tools"])
    return (
        MARKER_START + "\n"
        "      <!-- Tool-ettes inside this branch -- visual routing hub -->\n"
        "      <section class=\"content-section container reveal-on-scroll\">\n"
        "        <header class=\"section-header\">\n"
        "          <h2>Tool\u2011ettes inside " + branch["name"] + "</h2>\n"
        "          <p>" + branch["intro"] + "</p>\n"
        "        </header>\n"
        "\n"
        "        <div class=\"grid grid-3\">\n"
        + cards + "\n"
        "        </div>\n"
        "      </section>\n"
        + MARKER_END
    )


def process_branch_a(bkey, branch):
    """Replace the existing Tool-ettes section (branches 01, 02) with hub section."""
    p = Path(branch["file"])
    text = p.read_text(encoding="utf-8")

    if MARKER_START in text:
        new_text = re.sub(
            re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
            make_hub_section(branch),
            text, flags=re.DOTALL
        )
        p.write_text(new_text, encoding="utf-8")
        print("  [" + bkey + "] Updated existing AUTOGEN hub section")
        return

    section_patterns = [
        r'[ \t]*<!-- TOOL-ETTES INSIDE THIS TOOL [*]+ -->.*?</section>',
        r'[ \t]*<!-- Tool-ettes inside this branch -->.*?</section>',
    ]
    matched = False
    for pat in section_patterns:
        m = re.search(pat, text, re.DOTALL)
        if m:
            new_text = text[:m.start()] + "\n" + make_hub_section(branch) + "\n" + text[m.end():]
            p.write_text(new_text, encoding="utf-8")
            print("  [" + bkey + "] Replaced existing tool-ette section with hub")
            matched = True
            break
    if not matched:
        print("  [" + bkey + "] WARNING: could not find existing tool-ette section")


def process_branch_b(bkey, branch):
    """Insert new hub section before the getting-started / HOW-TO section."""
    p = Path(branch["file"])
    text = p.read_text(encoding="utf-8")

    if MARKER_START in text:
        new_text = re.sub(
            re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
            make_hub_section(branch),
            text, flags=re.DOTALL
        )
        p.write_text(new_text, encoding="utf-8")
        print("  [" + bkey + "] Updated existing AUTOGEN hub section")
        return

    m = re.search(r'(\s*<!-- HOW TO USE IT|\s*<section[^>]+id=["\']getting-started["\'])', text)
    if m:
        insert_pos = m.start()
        new_text = (
            text[:insert_pos]
            + "\n\n" + make_hub_section(branch) + "\n"
            + text[insert_pos:]
        )
        p.write_text(new_text, encoding="utf-8")
        print("  [" + bkey + "] Injected new hub section before getting-started")
    else:
        print("  [" + bkey + "] WARNING: could not find insertion point")


def main():
    for bkey, branch in BRANCHES.items():
        print("Processing branch " + bkey + " (" + branch["name"] + ") -- type " + branch["type"] + " ...")
        if branch["type"] == "A":
            process_branch_a(bkey, branch)
        else:
            process_branch_b(bkey, branch)
    print("\nDone.")


if __name__ == "__main__":
    main()
