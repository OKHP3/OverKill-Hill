#!/usr/bin/env python3
"""Refresh the universe authoring block from the current search index."""
import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site-src/pages/universe/index.main.html"
START = "<!-- AUTOGEN:UNIVERSE-MAP -->"
END = "<!-- /AUTOGEN:UNIVERSE-MAP -->"
PATTERN = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)


def render():
    script = ROOT / ".agents/skills/okhp3-universe-map/scripts/build-universe-map.py"
    spec = importlib.util.spec_from_file_location("universe_generator", script)
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    outputs = generator.build(ROOT / "universe-map.config.json")
    fragment = outputs["universe-map.html-fragment"]
    # Strict rendering deliberately ignores Mermaid click directives. The browser
    # adds validated links from the ordinary outline after rendering.
    fragment = re.sub(r"^\s*click [^\n]*\n", "", fragment, flags=re.M)
    fragment = fragment.replace('class="mermaid"', 'class="universe-diagram"')
    fragment = fragment.replace('<details>', '<details class="content-block">')
    fragment = fragment.replace('<section aria-label="Universe map">', '<section class="universe-generated" aria-label="Published page map">')
    fragment = fragment.replace('href="https://overkillhill.com/', 'href="/')
    fragment = fragment.replace('<details class="content-block">', '<details class="content-block" open>', 1)
    report = json.loads(outputs["universe-map.json"])
    included = {node["id"] for node in report["nodes"]}
    covered = {node for diagram in report["diagrams"] for node in diagram["nodes"]}
    if included != covered:
        raise ValueError("Generated universe map does not cover its inventory")
    return fragment.strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = SOURCE.read_text(encoding="utf-8")
    if content.count(START) != 1 or content.count(END) != 1:
        raise ValueError("Expected exactly one owned universe map block")
    expected = PATTERN.sub(lambda _: render(), content)
    if expected != content:
        if args.check:
            print("Universe map is stale. Run scripts/build-search-index.py.")
            return 1
        SOURCE.write_bytes(expected.encode("utf-8"))
        print("Updated universe map authoring source")
    else:
        print("Universe map is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
