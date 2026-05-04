# Contributing

Thanks for your interest in **OverKill Hill P³™**.

This repository primarily contains public website source, writing artifacts, and brand-adjacent materials.

## Helpful contributions
- flagging broken links
- identifying rendering issues
- suggesting documentation clarifications
- proposing cleaner artifact organization for public pages and writings

## Please avoid
- large unsolicited brand rewrites
- structural changes that break live site continuity
- adding placeholder or experimental content to public-facing pages without alignment

## How to contribute
1. Be specific about the file, page, or artifact in question.
2. Describe the problem first, then the proposed improvement.
3. Keep suggestions practical, respectful, and public-artifact focused.

## Validation before you commit
This repo gates every push and PR through three Python validators (see `.github/workflows/validate.yml`). Run them locally first; CI will block merges that fail any of them.

```bash
python3 scripts/validate_site.py            # editorial + structural site validator (26 pages)
python3 scripts/extract_templates.py --check # template-conformance + drift detector (16 templates)
python3 scripts/build_search_index.py --check # search-index freshness + orphan detector
```

If you change content, run `python3 scripts/build_search_index.py` (without `--check`) to rebuild the search index. If you change a layout that has an extracted template, re-run `python3 scripts/extract_templates.py` so the template stays in sync. See `README.md` → "Build / maintenance scripts" for the full list.

## Maintainer
Jamie Hill / OverKill Hill P³™  
contact@overkillhill.com
