#!/usr/bin/env python3
"""
scripts/lint-voice.py — Voice lint for overkillhill.com static site.

Flags AI-sounding / corporate-buzzword phrases and passive-heavy sentences
in HTML body copy.  All findings are WARNs — this check never fails the
build on its own.

Phrase patterns are sourced from the "User preferences" section of replit.md:
  - Conventional American English; avoid trendy/AI-sounding phrasing.
  - "custom GPT" must not appear as headline/lead technology.
  - Words like "utilize", "leverage", "delve" are AI-register red flags.

Skipped contexts (same logic as check_em_dashes in validate-site.py):
  - HTML comments
  - <script> blocks
  - <style> blocks
  - <pre> / <code> blocks  (code examples are not prose)

Run standalone:
    python3 scripts/lint-voice.py

Or called by validate-site.py (exits 0 always; findings are WARNs only).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"_replit", ".local", ".git", "node_modules", "attached_assets", "dist", "templates", ".agents"}

# ---------------------------------------------------------------------------
# Configurable phrase patterns
# Each entry: (label, compiled_regex, suggestion)
# Word-boundary anchors prevent partial matches (e.g. "utilization" catches
# "utiliz" but we want to flag it too, so some are prefix patterns).
# ---------------------------------------------------------------------------

# fmt: off
PHRASE_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    # --- AI-register verbs ---
    ("utilize",
     re.compile(r"\butiliz\w*\b", re.IGNORECASE),
     "use 'use' instead"),
    ("leverage (verb)",
     re.compile(r"\bleverag(e|es|ed|ing)\b", re.IGNORECASE),
     "be specific: 'use', 'apply', 'draw on'"),
    ("delve",
     re.compile(r"\bdelv(e|es|ed|ing)\b", re.IGNORECASE),
     "use 'explore', 'examine', 'look at'"),
    ("unlock (figurative)",
     re.compile(r"\bunlock(s|ed|ing)?\b", re.IGNORECASE),
     "say what specifically becomes possible"),
    # --- Hedging / throat-clearing ---
    ("it's worth noting",
     re.compile(r"\bit'?s worth noting\b", re.IGNORECASE),
     "say the thing directly, drop the preamble"),
    ("it is worth noting",
     re.compile(r"\bit is worth noting\b", re.IGNORECASE),
     "say the thing directly, drop the preamble"),
    ("it's important to note",
     re.compile(r"\bit'?s important to note\b", re.IGNORECASE),
     "say the thing directly"),
    ("it is important to note",
     re.compile(r"\bit is important to note\b", re.IGNORECASE),
     "say the thing directly"),
    ("note that",
     re.compile(r"\bnote that\b", re.IGNORECASE),
     "say the thing directly"),
    ("in order to",
     re.compile(r"\bin order to\b", re.IGNORECASE),
     "use plain 'to'"),
    # --- AI-positioning / headline tech ---
    ("custom GPT (lead copy)",
     re.compile(r"\bcustom\s+GPT\b", re.IGNORECASE),
     "lead copy must foreground protocol-first AI systems; 'custom GPT' only for factual past work"),
    # --- Corporate buzzwords ---
    ("going forward",
     re.compile(r"\bgoing forward\b", re.IGNORECASE),
     "use 'from now on', 'next', or be specific about the time frame"),
    ("touch base",
     re.compile(r"\btouch base\b", re.IGNORECASE),
     "use 'check in', 'follow up', 'talk'"),
    ("deep dive",
     re.compile(r"\bdeep[- ]dive?\b", re.IGNORECASE),
     "use 'close look', 'detailed examination', or just describe what you're doing"),
    ("synergy",
     re.compile(r"\bsynerg(y|ies|ize[sd]?|izing)\b", re.IGNORECASE),
     "describe the actual benefit"),
    ("robust",
     re.compile(r"\brobust\b", re.IGNORECASE),
     "say what specific quality you mean: reliable, thorough, detailed, etc."),
    ("seamless",
     re.compile(r"\bseamless(ly)?\b", re.IGNORECASE),
     "describe the actual experience"),
    ("cutting-edge",
     re.compile(r"\bcutting[- ]edge\b", re.IGNORECASE),
     "name the specific capability"),
    ("state-of-the-art",
     re.compile(r"\bstate[- ]of[- ]the[- ]art\b", re.IGNORECASE),
     "name the specific capability"),
    ("game changer",
     re.compile(r"\bgame[- ]changer?\b", re.IGNORECASE),
     "describe the actual impact"),
    ("pain point",
     re.compile(r"\bpain[- ]point\b", re.IGNORECASE),
     "name the actual problem"),
    ("revolutionize",
     re.compile(r"\brevolution(ize[sd]?|izing|ary)\b", re.IGNORECASE),
     "describe what actually changes"),
    ("transformative",
     re.compile(r"\btransformative\b", re.IGNORECASE),
     "describe what actually changes"),
]
# fmt: on

# ---------------------------------------------------------------------------
# Passive voice heuristic
# Pattern: be-verb + optional adverb(s) + past participle ending in -ed
# This catches the most common English passive constructions.
# Flags a line only when 2+ passive constructions appear (passive-heavy).
# ---------------------------------------------------------------------------

_BE_VERBS = r"(?:is|are|was|were|be|been|being)"
_OPT_ADV = r"(?:\s+\w+ly)?"  # optional single adverb (e.g. "was quickly built")
PASSIVE_RE = re.compile(
    rf"\b{_BE_VERBS}{_OPT_ADV}\s+([a-z]+ed)\b",
    re.IGNORECASE,
)

PASSIVE_PER_LINE_THRESHOLD = 2  # flag a line with this many passive hits


def find_html_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        parts = set(rel.parts)
        if parts & SKIP_DIRS:
            continue
        rel_posix = rel.as_posix()
        if rel_posix.startswith("assets/templates/"):
            continue
        files.append(path)
    return sorted(files)


def strip_tags(text: str) -> str:
    """Remove all HTML tags from a line, leaving only visible text."""
    return re.sub(r"<[^>]+>", " ", text)


def lint_file(path: Path) -> list[tuple[str, int, str]]:
    """
    Return a list of (severity, lineno, message) tuples for the file.
    All voice findings are 'WARN'.
    """
    rel = path.relative_to(ROOT).as_posix()
    raw = path.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()
    findings: list[tuple[str, int, str]] = []

    in_comment = False
    in_script = False
    in_pre = False
    in_style = False
    in_mermaid = False

    for lineno, line in enumerate(lines, 1):
        # ── update block-open state BEFORE evaluating ──────────────────────
        if not in_comment and "<!--" in line:
            in_comment = True
        if not in_script and re.search(r"<script[\s>]", line, re.IGNORECASE):
            in_script = True
        if not in_pre and re.search(r"<(?:pre|code)[\s>]", line, re.IGNORECASE):
            in_pre = True
        if not in_style and re.search(r"<style[\s>]", line, re.IGNORECASE):
            in_style = True
        if not in_mermaid and re.search(r'class="[^"]*\bmermaid\b', line, re.IGNORECASE):
            in_mermaid = True

        skip = in_comment or in_script or in_pre or in_style or in_mermaid

        if not skip:
            text = strip_tags(line)
            if not text.strip():
                pass  # nothing to check

            else:
                # ── phrase checks ─────────────────────────────────────────
                for label, pattern, suggestion in PHRASE_PATTERNS:
                    if pattern.search(text):
                        excerpt = text.strip()[:90]
                        findings.append((
                            "WARN", lineno,
                            f"{rel}:{lineno}: voice [{label}] — {suggestion} · …{excerpt}…",
                        ))

                # ── passive-heavy check ───────────────────────────────────
                passive_hits = PASSIVE_RE.findall(text)
                if len(passive_hits) >= PASSIVE_PER_LINE_THRESHOLD:
                    excerpt = text.strip()[:90]
                    findings.append((
                        "WARN", lineno,
                        f"{rel}:{lineno}: passive-heavy line ({len(passive_hits)} passive constructions) · …{excerpt}…",
                    ))

        # ── update block-close state AFTER evaluating ──────────────────────
        if in_comment and "-->" in line:
            in_comment = False
        if in_script and re.search(r"</script>", line, re.IGNORECASE):
            in_script = False
        if in_pre and re.search(r"</(?:pre|code)>", line, re.IGNORECASE):
            in_pre = False
        if in_style and re.search(r"</style>", line, re.IGNORECASE):
            in_style = False
        if in_mermaid and re.search(r"</(?:div|pre)>", line, re.IGNORECASE):
            in_mermaid = False

    return findings


def main() -> int:
    pages = find_html_files()
    all_findings: list[tuple[str, int, str]] = []
    for path in pages:
        all_findings.extend(lint_file(path))

    warnings = [f for f in all_findings if f[0] == "WARN"]

    if warnings:
        print(f"Voice lint — {len(warnings)} warning(s):")
        for _, _, msg in warnings:
            print(f"  ! {msg}")
    else:
        print("Voice lint — ✓ no voice warnings.")

    # Always exits 0: voice lint is advisory, never blocks the build.
    return 0


if __name__ == "__main__":
    sys.exit(main())
