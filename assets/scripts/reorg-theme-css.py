#!/usr/bin/env python3
"""
Reorganize assets/css/theme.css into the canonical structure:
    GLOBAL  →  OVERKILL HILL  →  GLEE-FULLY  →  ASKJAMIE

Each top-level rule is parsed, classified by selector, and re-emitted
in the new order. Original relative order WITHIN each brand is preserved
so cascade behavior stays intact.

Usage:
    python3 assets/scripts/reorg-theme-css.py            # in-place reorg
    python3 assets/scripts/reorg-theme-css.py --dry-run  # report only
"""
from __future__ import annotations
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

SRC = Path("assets/css/theme.css")


# ─── Tokenizer ──────────────────────────────────────────────────────────────

def tokenize(text: str):
    """Return list of (kind, content) tokens.
    kind in {'ws', 'comment', 'rule'}.
    'rule' = a complete top-level CSS rule (selector + balanced { ... }) or
             a top-level at-rule (e.g. @media { ... }, @keyframes { ... }).
    """
    out = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        # Whitespace run
        if ch.isspace():
            j = i
            while j < n and text[j].isspace():
                j += 1
            out.append(('ws', text[i:j]))
            i = j
            continue
        # Comment /* ... */
        if ch == '/' and i + 1 < n and text[i + 1] == '*':
            end = text.find('*/', i + 2)
            if end == -1:
                raise ValueError(f"Unterminated comment at byte {i}")
            end += 2
            out.append(('comment', text[i:end]))
            i = end
            continue
        # Otherwise: start of a rule. Walk to its matching closing brace.
        j = i
        depth = 0
        started_brace = False
        while j < n:
            c = text[j]
            # Skip nested comments
            if c == '/' and j + 1 < n and text[j + 1] == '*':
                k = text.find('*/', j + 2)
                if k == -1:
                    raise ValueError(f"Unterminated comment in rule at byte {j}")
                j = k + 2
                continue
            # Skip strings
            if c in ('"', "'"):
                q = c
                k = j + 1
                while k < n:
                    if text[k] == '\\':
                        k += 2
                        continue
                    if text[k] == q:
                        break
                    k += 1
                j = k + 1
                continue
            if c == '{':
                depth += 1
                started_brace = True
                j += 1
                continue
            if c == '}':
                depth -= 1
                j += 1
                if depth == 0 and started_brace:
                    break
                continue
            j += 1
        out.append(('rule', text[i:j]))
        i = j
    return out


# ─── Block builder ──────────────────────────────────────────────────────────

# Fingerprints for canonical banners we emit. We strip these from any block's
# leading text so the script is idempotent — re-running it does not accumulate
# duplicate banners. If you change a banner's wording, also update these patterns.
CANONICAL_BANNER_PATTERNS = [
    re.compile(r'OverKill Hill P\u00b3 \u2014 Industrial Blueprint Theme'),  # top file header
    re.compile(r'STRUCTURE \(canonical order'),                              # top file header (alt fingerprint)
    re.compile(r'SECTION \u00b7 GLOBAL'),                                    # section banners
    re.compile(r'SECTION \u00b7 OKH'),
    re.compile(r'SECTION \u00b7 GLEE'),
    re.compile(r'SECTION \u00b7 ASKJAMIE'),
]


def is_canonical_banner(comment_text: str) -> bool:
    """True if this comment matches one of the banners THIS SCRIPT emits.
    Used to drop stale banners during re-runs (idempotency)."""
    return any(p.search(comment_text) for p in CANONICAL_BANNER_PATTERNS)


def build_blocks(tokens):
    """Group tokens into blocks. A block = leading whitespace+comments + one rule.
    Canonical banner comments (the ones THIS script emits) are stripped from the
    leading text so the script is idempotent. Whitespace on BOTH sides of a
    stripped banner is also collapsed so we don't accumulate blank lines on
    re-run — the emit step adds its own blank-line separators."""
    blocks = []
    buf = []
    skip_ws = False  # set after a stripped banner so trailing ws is also dropped
    for kind, content in tokens:
        if kind == 'comment' and is_canonical_banner(content):
            # Drop banner + any whitespace immediately preceding it…
            while buf and buf[-1][0] == 'ws':
                buf.pop()
            # …and any whitespace immediately following it.
            skip_ws = True
            continue
        if skip_ws and kind == 'ws':
            continue
        skip_ws = False
        if kind in ('ws', 'comment'):
            buf.append((kind, content))
        else:  # rule
            leading = ''.join(c for _, c in buf)
            blocks.append({'leading': leading, 'rule': content})
            buf = []
    tail = ''.join(c for _, c in buf)
    return blocks, tail


# ─── Classifier ─────────────────────────────────────────────────────────────

GLEE_PAT = re.compile(
    r'\.glee-main\b|'
    r'\.glee-(?:hero|mermaid|wip|glow|fully)|'
    r'\bgleeSweep\b|'
    r'--glee\b'                     # BEM brand modifier suffix (e.g. .brand-stripes--glee, .site-specials--glee)
)
ASKJAMIE_PAT = re.compile(
    r'\.askjamie(?:-main)?\b|'
    r'\.askjamie-(?:hero|mermaid|paper|avatar|under|breadcrumb|logo|system)|'
    r'--jamie\b|--askjamie\b'       # BEM brand modifier suffix (e.g. .brand-stripes--jamie)
)
OKH_EXPLICIT_PAT = re.compile(
    r'body:not\(\.glee-main\):not\(\.askjamie-main\)|'
    r'body:not\(\.askjamie-main\):not\(\.glee-main\)'
)
OKH_COMPONENT_PAT = re.compile(
    r'\.article-(?!hero \.brand-stripes)|'  # article-* classes (not the shared brand-stripes inside)
    r'\.bracket-heats|\.heat-(?:guide|competitors|actions|poll-box)|'
    r'\.scorecard|\.scoring-lane|'
    r'\.diagram-(?:card|grid|shell|section|caption|header|label|links|gallery|gallery-note|embed-wrap|external-link|source-link|live-render|static-img)|'
    r'\.bfs-hero|\.gpt-hero|'
    r'\.bullet-list|\.artifact-(?:stack|card|copy)|'
    r'\.code-drop|\.inline-code-example|'
    r'\.formula-block|'
    r'\.council-(?:card|pill|table|name|role|members)|'
    r'\.pull-quote|\.protoform-notice|'
    r'\.sidebar-(?:widget|links|section|diagram|tool|widget-desc)|'
    r'\.toc-list|'
    r'\.download-(?:options|format|links)|'
    r'\.mermaid-(?:cta|referral-link)|'
    r'\.brand-stripes--okh|'
    r'\.hero-blueprint-bg|\.hero-forge-card|'
    r'\.latest-(?:image|pill|block|card|submenu)|'
    r'\.text-amber|\.link-amber|'
    r'\.series-badge|'
    r'#404\b|@keyframes blueprintShift'
)


def classify(rule_text: str, leading_text: str = '') -> str:
    """Classify a CSS block by priority:
       1. OKH-explicit (body:not(.glee-main):not(.askjamie-main) ...) → OKH
       2. Selector contains .glee-main as a positive scope → GLEE
       3. Selector contains .askjamie-main as a positive scope → ASKJAMIE
       4. Selector contains --glee / --jamie BEM modifier → that brand
       5. OKH-only component class (.article-*, .heat-*, .diagram-*, etc.) → OKH
       6. Otherwise → GLOBAL.
       Rule: positive brand scopes win over component classes.
       :not() clauses are stripped before the GLEE/ASKJAMIE checks so an
       OKH-explicit selector isn't double-claimed by the brands it excludes.
    """
    # Strip comments
    cleaned = re.sub(r'/\*.*?\*/', '', rule_text, flags=re.S)

    # 1. OKH-explicit takes priority — it positively scopes to "neither subsite".
    if OKH_EXPLICIT_PAT.search(cleaned):
        return 'OKH'

    # Strip :not() clauses so the brand patterns only match POSITIVE scopes.
    # Without this, `.foo:not(.glee-main)` would falsely look GLEE-positive.
    positive = re.sub(r':not\([^)]*\)', '', cleaned)

    has_glee = bool(GLEE_PAT.search(positive))
    has_askjamie = bool(ASKJAMIE_PAT.search(positive))

    # 2-4. Brand scope wins over component class.
    if has_glee and not has_askjamie:
        return 'GLEE'
    if has_askjamie and not has_glee:
        return 'ASKJAMIE'
    if has_glee and has_askjamie:
        # Multi-brand selector list (e.g. ".glee-main .x, .askjamie-main .x")
        # — neither brand owns this exclusively, so it's a shared override.
        return 'GLOBAL'

    # 5. OKH-only component class.
    if OKH_COMPONENT_PAT.search(cleaned):
        return 'OKH'

    # 6. Truly brand-agnostic.
    return 'GLOBAL'


# ─── Banner emitters ────────────────────────────────────────────────────────

def banner(title: str, body: str = '') -> str:
    bar = '═' * 76
    lines = [
        f'/* ╔{bar}╗',
        f'   ║  {title.ljust(72)}  ║',
    ]
    for ln in body.splitlines():
        lines.append(f'   ║  {ln.ljust(72)}  ║')
    lines.append(f'   ╚{bar}╝ */')
    return '\n'.join(lines) + '\n'


# ─── Main ───────────────────────────────────────────────────────────────────

def main(argv):
    dry_run = '--dry-run' in argv
    text = SRC.read_text()
    tokens = tokenize(text)
    blocks, tail = build_blocks(tokens)
    print(f'Parsed {len(blocks)} top-level blocks (+ {len(tail)} bytes tail)')

    by_cls = OrderedDict([('GLOBAL', []), ('OKH', []), ('GLEE', []), ('ASKJAMIE', [])])
    for b in blocks:
        c = classify(b['rule'], b['leading'])
        b['cls'] = c
        by_cls[c].append(b)

    print('Classification counts:')
    for k, v in by_cls.items():
        print(f'  {k:10s} {len(v):4d} blocks')

    if dry_run:
        print('\n--- Sample of first 3 blocks per category ---')
        for k, v in by_cls.items():
            print(f'\n[{k}] (showing first 3 of {len(v)})')
            for b in v[:3]:
                # Print first selector line
                first_rule_line = b['rule'].splitlines()[0] if b['rule'] else '(empty)'
                first_lead = b['leading'].strip().splitlines()[-1][:80] if b['leading'].strip() else ''
                print(f'  rule:    {first_rule_line[:90]}')
                if first_lead:
                    print(f'  comment: {first_lead}')

        # Sanity check: warn about GLOBAL blocks that mention brand tokens.
        # Catches future regressions where a brand-specific selector is
        # accidentally routed to GLOBAL because no matcher claimed it.
        print('\n--- GLOBAL blocks mentioning brand tokens (review for misclassification) ---')
        brand_mention = re.compile(r'\b(?:glee|jamie|askjamie)\b', re.I)
        flagged = 0
        for b in by_cls['GLOBAL']:
            cleaned = re.sub(r'/\*.*?\*/', '', b['rule'], flags=re.S)
            if brand_mention.search(cleaned):
                first = b['rule'].splitlines()[0][:90]
                print(f'  ⚠ GLOBAL: {first}')
                flagged += 1
        if flagged == 0:
            print('  ✓ none — every GLOBAL block is brand-agnostic at the selector level')
        else:
            print(f'  → {flagged} block(s) flagged. Either (a) extend GLEE_PAT/ASKJAMIE_PAT '
                  f'to claim them, or (b) leave them in GLOBAL if they are intentionally '
                  f'multi-brand variants (e.g. brand-stripes that bundles all 3 brand colors).')
        return 0

    # Emit reorganized file
    parts = []
    parts.append(
        '/* OverKill Hill P³ — Industrial Blueprint Theme\n'
        '   Shared layout + motion across overkillhill.com, glee-fully.tools, and askjamie.bot.\n'
        '\n'
        '   ┌────────────────────────────────────────────────────────────────┐\n'
        '   │  STRUCTURE (canonical order — mirror this in sibling repos)    │\n'
        '   │   1. GLOBAL        tokens, reset, base, shared utilities,      │\n'
        '   │                    components used by all three sites          │\n'
        '   │   2. OVERKILL HILL site-specific (default)                     │\n'
        '   │   3. GLEE-FULLY    `.glee-main`-scoped overrides               │\n'
        '   │   4. ASKJAMIE      `.askjamie-main`-scoped overrides           │\n'
        '   │                                                                │\n'
        '   │  Maintenance: edit here, then run                              │\n'
        '   │    python3 assets/scripts/reorg-theme-css.py --dry-run         │\n'
        '   │  to verify the section a new rule lands in.                    │\n'
        '   └────────────────────────────────────────────────────────────────┘\n'
        '*/\n\n'
    )

    for cls, descr in [
        ('GLOBAL',   'Tokens, reset, base, shared utilities + components'),
        ('OKH',      'Default brand: scoped via body:not(.glee-main):not(.askjamie-main)\nor uses OKH-only component classes (.article-*, .heat-*, .diagram-*, etc.)'),
        ('GLEE',     'glee-fully.tools — scoped via .glee-main'),
        ('ASKJAMIE', 'askjamie.bot — scoped via .askjamie-main'),
    ]:
        parts.append('\n')
        parts.append(banner(f'SECTION · {cls}', descr))
        parts.append('\n')
        for b in by_cls[cls]:
            parts.append(b['leading'] if b['leading'] else '\n')
            parts.append(b['rule'])
        parts.append('\n')
    parts.append(tail)

    new_text = ''.join(parts)
    # Normalize trailing whitespace to exactly one \n so re-runs are byte-stable.
    # (The per-section emit appends a trailing \n which combines with the
    # original file's trailing newline → one extra byte per run otherwise.)
    new_text = new_text.rstrip() + '\n'
    SRC.write_text(new_text)
    print(f'\nWrote {SRC} ({len(new_text)} bytes)')

    # Verify brace balance
    cleaned = re.sub(r'/\*.*?\*/', lambda m: '\n' * m.group(0).count('\n'), new_text, flags=re.S)
    depth = 0
    issues = 0
    line = 1
    for ch in cleaned:
        if ch == '\n':
            line += 1
        elif ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth < 0:
                issues += 1
                depth = 0
    print(f'Brace verification: final_depth={depth}, negative_depth_events={issues}')
    if depth != 0 or issues > 0:
        print('  ⚠ CSS NOT BALANCED — restore from /tmp/theme.css.backup')
        return 1
    print('  ✓ CSS balanced')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
