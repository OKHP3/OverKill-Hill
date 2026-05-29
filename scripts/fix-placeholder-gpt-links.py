#!/usr/bin/env python3
"""Fix placeholder GPT links in tool-ette pages.

Idempotent: skips pages where the real URL is already present.
Real URLs sourced from branch index pages and confirmed by site owner.

History:
  2026-05-26 — original 3 fixes (02c, 04d, 04e)
  2026-05-27 — added 4 Healthy Bee-ing fixes (06a wrong URL, 06b, 06c, 06d)
               06a had a copy-paste error (Lifestyle Wallboard URL); 06d had
               YOUR-GPT-ID-HERE placeholder; 06b had Lifestyle Wallboard URL.
"""
from pathlib import Path
import re

FIXES = [
    {
        "page": "toolbox/02-treasured-finds/02c-present-hoarder/index.html",
        "real_url": "https://chatgpt.com/g/g-685af65a822881919690d7410a122984-present-hoarder-by-glee-fully",
        "placeholder_patterns": [
            r'href="https://chatgpt\.com"\s',
            r'href="https://chatgpt\.com"',
        ],
        "cta_text_old": 'Launch "Present Hoarder" in ChatGPT',
        "cta_text_new": 'Open Present Hoarder in ChatGPT',
        "todo_comment": "<!-- TODO: replace href with the specific Present Hoarder GPT URL once finalized -->",
    },
    {
        "page": "toolbox/04-travelers-guide/04d-dreamland-journeys/index.html",
        "real_url": "https://chatgpt.com/g/g-685b072fccec8191a595b10991348f30-dreamland-journeys-by-glee-fully",
        "placeholder_patterns": [
            r'href="https://chat\.openai\.com/"',
        ],
        "cta_text_old": "Launch Dreamland Journeys",
        "cta_text_new": "Open Dreamland Journeys in ChatGPT",
        "todo_comment": "<!-- TODO: swap href for the live Dreamland Journeys GPT link when ready -->",
    },
    {
        "page": "toolbox/04-travelers-guide/04e-memento-log/index.html",
        "real_url": "https://chatgpt.com/g/g-685b072be58c8191ba386b00b33b93b8-memento-log-by-glee-fully",
        "placeholder_patterns": [
            r'href="https://chatgpt\.com/g/REPLACE_WITH_MEMENTO_LOG_GPT_ID"',
        ],
        "cta_text_old": 'Launch "Memento Log" in ChatGPT',
        "cta_text_new": "Open Memento Log in ChatGPT",
        "todo_comment": "<!-- TODO: replace href with the real GPT URL for Memento Log -->",
    },
]

HEALTHY_BEEING_FIXES = [
    {
        "page": "toolbox/06-healthy-bee-ing/06a-care-check/index.html",
        "real_url": "https://chatgpt.com/g/g-68b505526b9c8191a6d2a804e45c7741-care-check-by-glee-fully",
        "wrong_urls": [
            "https://chatgpt.com/g/g-685b073a236481919de38600d5ebdcbb",
        ],
    },
    {
        "page": "toolbox/06-healthy-bee-ing/06b-calm-keep/index.html",
        "real_url": "https://chatgpt.com/g/g-68b50556eca08191b5101eaa06d7253a-calm-keep-by-glee-fully",
        "wrong_urls": [
            "https://chatgpt.com/g/g-685b073a236481919de38600d5ebdcbb-lifestyle-wallboard-by-glee-fully",
        ],
    },
    {
        "page": "toolbox/06-healthy-bee-ing/06d-medi-minder/index.html",
        "real_url": "https://chatgpt.com/g/g-68b5055fd2748191b794f98ec9025844-medi-minder-by-glee-fully",
        "wrong_urls": [
            "https://chatgpt.com/g/YOUR-GPT-ID-HERE",
        ],
    },
]

ROOT = Path(__file__).parent.parent
changed = 0

# Apply Healthy Bee-ing wrong-URL fixes (simple string replacement)
for fix in HEALTHY_BEEING_FIXES:
    path = ROOT / fix["page"]
    if not path.exists():
        print(f"  SKIP (not found): {fix['page']}")
        continue
    text = path.read_text(encoding="utf-8")
    if fix["real_url"] in text:
        print(f"  SKIP (already fixed): {fix['page']}")
        continue
    original = text
    for wrong in fix["wrong_urls"]:
        text = text.replace(wrong, fix["real_url"])
    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"  FIXED: {fix['page']}")
        changed += 1
    else:
        print(f"  WARN: no change made to {fix['page']} — check wrong_urls")

for fix in FIXES:
    path = ROOT / fix["page"]
    if not path.exists():
        print(f"  SKIP (not found): {fix['page']}")
        continue

    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")

    if fix["real_url"] in text:
        print(f"  SKIP (already fixed): {fix['page']}")
        continue

    original = text

    # Remove TODO comment
    if fix["todo_comment"] in text:
        text = text.replace(fix["todo_comment"], "")

    # Replace placeholder href with real URL (try each pattern)
    for pat in fix["placeholder_patterns"]:
        text = re.sub(pat, f'href="{fix["real_url"]}"', text)

    # Update CTA text if needed
    if fix["cta_text_old"] in text:
        text = text.replace(fix["cta_text_old"], fix["cta_text_new"])

    if text != original:
        path.write_bytes(text.encode("utf-8"))
        print(f"  FIXED: {fix['page']}")
        changed += 1
    else:
        print(f"  WARN: no change made to {fix['page']} — check patterns")

print(f"\nDone. {changed} file(s) updated.")
