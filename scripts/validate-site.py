#!/usr/bin/env python3
"""
OverKill Hill P³™ — static site validation harness.

Phase 16 of the AUDIT_OVERKILL_HILL_REPLIT_PASS pipeline.

Checks every production HTML page for:
  - <title> present
  - meta description present
  - canonical link present
  - single <h1>
  - JSON-LD structured data present
   - sitemap inventory and inclusion (for non-noindex pages)
  - broken internal links (relative or /-rooted hrefs that resolve to no file)
  - broken asset references (CSS/JS/images)
  - external target="_blank" links missing rel="noopener" / "noreferrer"
  - placeholder hrefs ("#", "javascript:void(0)", empty href)
  - "P3" without superscript inside <title> or <meta> (brand violation)
  - old tagline "Precision. Power. Presence." anywhere (brand regression)
  - current content-hashed references to shared CSS and JavaScript

Exits 0 if no errors. Exits 1 if any errors. Warnings do not fail the build.
Run from repo root:  python3 scripts/validate-site.py
"""

from __future__ import annotations

import os
import hashlib
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

from csp import build_policies, page_class, sha256_source

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"_replit", ".local", ".git", ".pr-head", "node_modules", "attached_assets", "dist", "templates", ".agents", "site-src"}
SITEMAP = ROOT / "sitemap.xml"
SITE_ORIGIN = "https://overkillhill.com"
THEME_STYLESHEET_PATH = "/assets/css/theme.css"
THEME_STYLESHEET = ROOT / THEME_STYLESHEET_PATH.lstrip("/")
APP_SCRIPT_PATH = "/assets/js/app.js"
MERMAID_INIT_SCRIPT_PATH = "/assets/js/mermaid-init.js"
SHARED_SCRIPT_PATHS = (APP_SCRIPT_PATH, MERMAID_INIT_SCRIPT_PATH)
MERMAID_VENDOR_ROOT = ROOT / "assets/vendor/mermaid"
MERMAID_VENDOR_ENTRY = MERMAID_VENDOR_ROOT / "mermaid.esm.min.mjs"
MERMAID_VERSION_FILE = MERMAID_VENDOR_ROOT / "VERSION"
INLINE_CSP_SOURCE_ROUTES = {"projects/telling-forward/index.html"}
MERMAID_LOOSE_ROUTES = {
    "universe/index.html",
    "writings/first-diagram-is-a-liar/v03/v2-heat-a/index.html",
    "writings/first-diagram-is-a-liar/v03/v2-heat-b/index.html",
}
MERMAID_HEAT_ROUTES = {
    "writings/first-diagram-is-a-liar/v03/v2-heat-a/index.html",
    "writings/first-diagram-is-a-liar/v03/v2-heat-b/index.html",
}
MERMAID_HEAT_TARGETS = {
    ("https://mermaidchart.cello.so", "/UhVlNtC2MlS"),
    ("https://replit.com", "/refer/overkillhillp3"),
    ("https://overkillhill.com", "/writings/first-diagram-is-a-liar/"),
    ("https://overkillhill.com", "/"),
    ("https://www.linkedin.com", "/company/overkillhillp3"),
    ("https://ko-fi.com", "/T6T71HCY6A"),
}

# Em dash in all three forms: literal U+2014, named entity, numeric entity
EM_DASH_RE = re.compile(r"\u2014|&mdash;|&#8212;")


class TagCounter(HTMLParser):
    """Collect everything we need for one HTML page in a single pass."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title: str | None = None
        self._in_title = False
        self._title_buf: list[str] = []
        self.h1_count = 0
        self.has_meta_description = False
        self.has_canonical = False
        self.has_jsonld = False
        self.is_noindex = False
        self.anchors: list[dict[str, str]] = []
        self.asset_refs: list[str] = []  # src/href for css/js/img/link
        self.stylesheet_refs: list[str] = []
        self.script_refs: list[str] = []

    def handle_starttag(self, tag: str, attrs_list):
        attrs = {k: (v or "") for k, v in attrs_list}
        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta":
            name = attrs.get("name", "").lower()
            content = attrs.get("content", "")
            if name == "description" and content.strip():
                self.has_meta_description = True
            if name == "robots" and "noindex" in content.lower():
                self.is_noindex = True
        elif tag == "link":
            rel = attrs.get("rel", "").lower()
            href = attrs.get("href", "")
            if rel == "canonical" and href:
                self.has_canonical = True
            if "stylesheet" in rel.split() and href:
                self.stylesheet_refs.append(href)
                self.asset_refs.append(href)
            elif rel in ("icon", "apple-touch-icon", "manifest") and href:
                self.asset_refs.append(href)
        elif tag == "script":
            t = attrs.get("type", "").lower()
            src = attrs.get("src", "")
            if t == "application/ld+json":
                self.has_jsonld = True
            if src:
                self.asset_refs.append(src)
                self.script_refs.append(src)
        elif tag == "img":
            src = attrs.get("src", "")
            if src:
                self.asset_refs.append(src)
        elif tag == "a":
            href = attrs.get("href", "")
            if href is not None:
                self.anchors.append(
                    {
                        "href": href,
                        "target": attrs.get("target", ""),
                        "rel": attrs.get("rel", ""),
                    }
                )

    def handle_endtag(self, tag: str):
        if tag == "title":
            self._in_title = False
            self.title = "".join(self._title_buf).strip()
            self._title_buf = []

    def handle_data(self, data: str):
        if self._in_title:
            self._title_buf.append(data)


def find_html_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        parts = set(rel.parts)
        if parts & SKIP_DIRS:
            continue
        # /assets/templates/ holds stripped template scaffolds with [PLACEHOLDER]
        # tokens — not live pages. They're parsed separately by extract-templates.py.
        rel_posix = rel.as_posix()
        if rel_posix.startswith(("assets/templates/", "assets/partials/")):
            continue
        files.append(path)
    return sorted(files)


def load_sitemap_urls() -> set[str]:
    if not SITEMAP.exists():
        return set()
    text = SITEMAP.read_text(encoding="utf-8")
    return set(re.findall(r"<loc>([^<]+)</loc>", text))


def validate_sitemap_inventory(sitemap_urls: set[str]) -> list[Finding]:
    """Ensure every sitemap entry resolves to a production HTML page."""
    findings: list[Finding] = []
    for url in sorted(sitemap_urls):
        parsed = urlparse(url)
        if parsed.netloc and parsed.netloc != urlparse(SITE_ORIGIN).netloc:
            findings.append(Finding("ERROR", "sitemap.xml", f"non-production URL in sitemap.xml: {url}"))
            continue
        route = parsed.path or "/"
        target = ROOT / route.lstrip("/")
        if route == "/":
            target = ROOT / "index.html"
        elif route.endswith("/"):
            target = target / "index.html"
        if not target.is_file():
            findings.append(Finding("ERROR", "sitemap.xml", f"sitemap URL has no HTML page: {url}"))
    return findings


def html_to_route(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def current_content_hashed_url(asset_path: str) -> str | None:
    """Return the canonical content-hashed URL for a shared asset."""
    asset = ROOT / asset_path.lstrip("/")
    if not asset.is_file():
        return None
    canonical = asset.read_bytes().replace(b"\r\n", b"\n")
    fingerprint = hashlib.sha256(canonical).hexdigest()[:8]
    return f"{asset_path}?v={fingerprint}"


def is_asset_ref(ref: str, asset_path: str) -> bool:
    """Identify an asset whether a page used the canonical URL or a legacy form."""
    return urlparse(ref).path.lstrip("/") == asset_path.lstrip("/")


def resolve_internal(href: str, source: Path) -> Path | None:
    """Map a /-rooted or relative href back to a filesystem path. Returns None if not local."""
    parsed = urlparse(href)
    if parsed.scheme in ("http", "https", "mailto", "tel", "javascript"):
        return None
    if not parsed.path:
        return None  # pure fragment like "#protocols"
    p = unquote(parsed.path)
    if p.startswith("/"):
        target = ROOT / p.lstrip("/")
    else:
        target = source.parent / p
    return target


def target_exists(target: Path) -> bool:
    if target.exists():
        if target.is_dir():
            return (target / "index.html").exists()
        return True
    # tolerate trailing-slash directory references
    if str(target).endswith("/") and (target / "index.html").exists():
        return True
    return False


def _csp_script_hashes(policy: str | None) -> set[str]:
    """Extract script hashes from a serialized CSP policy."""
    if not policy:
        return set()
    match = re.search(r"(?:^|;\s*)script-src\s+([^;]+)", policy)
    if not match:
        return set()
    return {
        token for token in match.group(1).split()
        if token.startswith("'sha256-") and token.endswith("'")
    }


def _csp_meta_policy(raw: str) -> str | None:
    """Read a CSP meta tag regardless of HTML attribute ordering."""
    match = re.search(
        r'<meta\b(?=[^>]*\bhttp-equiv=["\']Content-Security-Policy["\'])'
        r'(?=[^>]*\bcontent=(["\']))[^>]*\bcontent=\1(.*?)\1',
        raw,
        re.IGNORECASE,
    )
    return match.group(2) if match else None


def _source_inline_script_hashes(page: Path) -> set[str]:
    """Return hashes for inline scripts in a page's source fragments."""
    rel = page.relative_to(ROOT).as_posix()
    stem = ROOT / "site-src" / "pages" / rel
    hashes: set[str] = set()
    for suffix in (".main.html", ".extras.html"):
        source = stem.with_suffix(suffix)
        if not source.is_file():
            continue
        text = source.read_text(encoding="utf-8", errors="replace")
        hashes.update(
            sha256_source(match.group(1))
            for match in re.finditer(
                r"<script\b(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>",
                text,
                re.IGNORECASE,
            )
            if match.group(1).strip()
        )
    return hashes


def validate_csp_hashes(pages: list[Path]) -> list[Finding]:
    """Ensure the telling-forward source script and generated CSP stay aligned."""
    findings: list[Finding] = []
    policies = build_policies()

    for page in pages:
        rel = page.relative_to(ROOT).as_posix()
        if rel not in INLINE_CSP_SOURCE_ROUTES:
            continue
        raw = page.read_text(encoding="utf-8", errors="replace")
        actual = _csp_meta_policy(raw)
        expected = policies[page_class(page)]
        if actual != expected:
            findings.append(Finding(
                "ERROR", rel,
                "CSP policy or inline script hash list is stale; run "
                "python3 scripts/generate-csp.py",
            ))
            continue

        actual_hashes = _csp_script_hashes(actual)
        source_hashes = _source_inline_script_hashes(page)
        missing = sorted(source_hashes - actual_hashes)
        if missing:
            findings.append(Finding(
                "ERROR", rel,
                "CSP is missing inline script hash(es) from site-src: "
                + ", ".join(missing),
            ))

    return findings


def _mermaid_imports(text: str) -> list[str]:
    """Return import specifiers from static and dynamic ESM imports."""
    pattern = re.compile(
        r"""(?:\bimport\s*\(\s*|\b(?:import|export)\b[^;]*?\bfrom\s*)["']([^"']+)["']"""
    )
    return [match.group(1) for match in pattern.finditer(text)]


def _mermaid_target_is_allowed(route: str, target: str) -> bool:
    try:
        parsed = urlparse(target)
    except ValueError:
        return False
    origin = f"{parsed.scheme}://{parsed.netloc}"
    if parsed.scheme != "https" or parsed.query or parsed.fragment:
        return False
    if route in MERMAID_HEAT_ROUTES:
        return (origin, parsed.path) in MERMAID_HEAT_TARGETS
    if route == "universe/index.html":
        if origin == "https://glee-fully.tools":
            return parsed.path == "/" or parsed.path.startswith("/toolbox/")
        if origin == "https://askjamie.bot":
            return parsed.path == "/" or parsed.path.startswith("/lens-system/")
        if origin == "https://overkillhill.com":
            return (
                parsed.path == "/"
                or parsed.path.startswith("/projects/")
                or parsed.path.startswith("/writings/")
            )
    return False


def validate_mermaid_runtime(pages: list[Path]) -> list[Finding]:
    """Check the vendored graph, Mermaid sources, security, and click policies."""
    findings: list[Finding] = []

    if not MERMAID_VENDOR_ENTRY.is_file():
        findings.append(Finding("ERROR", str(MERMAID_VENDOR_ENTRY.relative_to(ROOT)),
                                "vendored Mermaid entry module is missing"))
    elif not MERMAID_VENDOR_ROOT.is_dir():
        findings.append(Finding("ERROR", "assets/vendor/mermaid",
                                "vendored Mermaid directory is missing"))

    # Every relative import in the entry module and its chunks must resolve.
    if MERMAID_VENDOR_ROOT.is_dir():
        for module in sorted(MERMAID_VENDOR_ROOT.rglob("*.mjs")):
            text = module.read_text(encoding="utf-8", errors="replace")
            for specifier in _mermaid_imports(text):
                if specifier.startswith("."):
                    target = (module.parent / specifier).resolve()
                    if not target.is_file():
                        findings.append(Finding(
                            "ERROR", module.relative_to(ROOT).as_posix(),
                            f"missing local Mermaid import: {specifier}",
                        ))
                elif specifier.startswith("/assets/vendor/mermaid/"):
                    target = ROOT / specifier.split("?", 1)[0].lstrip("/")
                    if not target.is_file():
                        findings.append(Finding(
                            "ERROR", module.relative_to(ROOT).as_posix(),
                            f"missing local Mermaid import: {specifier}",
                        ))

    # Inspect checked-in HTML/JS sources as well as generated production pages.
    source_files = [
        path for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".html", ".js", ".mjs"}
        and not (set(path.relative_to(ROOT).parts) & SKIP_DIRS)
    ]
    for path in sorted(source_files):
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for specifier in _mermaid_imports(text):
            if "mermaid" in specifier.lower() and urlparse(specifier).scheme in ("http", "https"):
                findings.append(Finding("ERROR", rel,
                                        f"external Mermaid import is not allowed: {specifier}"))
            if specifier.startswith("/assets/vendor/mermaid/"):
                target = ROOT / specifier.split("?", 1)[0].lstrip("/")
                if not target.is_file():
                    findings.append(Finding("ERROR", rel,
                                            f"missing local Mermaid import: {specifier}"))
        for specifier in re.findall(r"""<script\b[^>]*\bsrc=["']([^"']+)["']""", text, re.I):
            if "mermaid" in specifier.lower() and urlparse(specifier).scheme in ("http", "https"):
                findings.append(Finding("ERROR", rel,
                                        f"external Mermaid script is not allowed: {specifier}"))

    for path in pages:
        rel = path.relative_to(ROOT).as_posix()
        raw = path.read_text(encoding="utf-8", errors="replace")
        has_loose = bool(re.search(
            r"""data-mermaid-security\s*=\s*["']loose["']|securityLevel\s*:\s*["']loose["']""",
            raw, re.I,
        ))
        if has_loose and rel not in MERMAID_LOOSE_ROUTES:
            findings.append(Finding("ERROR", rel,
                                    "Mermaid loose security is not approved for this page"))

        click_targets = re.findall(
            r"""^\s*click\s+\S+\s+"([^"]+)""", raw, re.MULTILINE
        )
        if click_targets and rel not in MERMAID_LOOSE_ROUTES:
            findings.append(Finding("ERROR", rel,
                                    "Mermaid click targets are only approved on the documented pages"))
        for target in click_targets:
            if not _mermaid_target_is_allowed(rel, target):
                findings.append(Finding("ERROR", rel,
                                        f"Mermaid click target is outside its allowlist: {target}"))

    return findings


def validate_mermaid_version_pin(pages: list[Path]) -> list[Finding]:
    """Confirm the pinned VERSION file matches the vendored runtime bundle.

    This does not check npm for a newer release -- that is the job of the
    scheduled "mermaid-version-watch" GitHub Action, which needs network
    access this local validator does not assume. This check only confirms
    internal consistency: the version this repo claims to be running is the
    version actually sitting in assets/vendor/mermaid/, so a partial or
    forgotten re-vendor step cannot silently pass validation.
    """
    findings: list[Finding] = []
    rel_version_file = MERMAID_VERSION_FILE.relative_to(ROOT).as_posix()

    if not MERMAID_VERSION_FILE.is_file():
        findings.append(Finding(
            "ERROR", rel_version_file,
            "Mermaid VERSION pin file is missing; create it with the vendored "
            "release number (see README 'Mermaid runtime trust decision')",
        ))
        return findings

    pinned = MERMAID_VERSION_FILE.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", pinned):
        findings.append(Finding(
            "ERROR", rel_version_file,
            f"Mermaid VERSION pin {pinned!r} is not a plain semver string (X.Y.Z)",
        ))
        return findings

    if not MERMAID_VENDOR_ENTRY.is_file():
        # Already reported by validate_mermaid_runtime(); avoid duplicating.
        return findings

    bundle_text = MERMAID_VENDOR_ENTRY.read_text(encoding="utf-8", errors="replace")
    if pinned not in bundle_text:
        findings.append(Finding(
            "ERROR", rel_version_file,
            f"Mermaid VERSION pin ({pinned}) was not found inside "
            f"{MERMAID_VENDOR_ENTRY.relative_to(ROOT).as_posix()}; the pin file "
            "and the vendored runtime have drifted out of sync",
        ))

    return findings


def _page_renders_mermaid(raw: str) -> bool:
    return bool(re.search(r"""class=["\'][^"\']*\bmermaid\b""", raw, re.IGNORECASE))


def validate_mermaid_csp_alignment(pages: list[Path]) -> list[Finding]:
    """Flag pages whose CSP class cannot legally style Mermaid's own output.

    Mermaid renders inline style="..." attributes and <style> blocks at
    runtime, per diagram, per page load. scripts/csp.py computes the
    style-src / style-src-attr hash allowlists by statically scanning built
    HTML, so a hash allowlist can never cover output Mermaid only generates
    in the browser. Until a page class carries 'unsafe-inline' for style
    directives (or diagrams are pre-rendered at build time instead), Mermaid
    diagrams on that page class will lose their theme styling and the
    browser console will show real CSP violations -- even though the
    diagram still parses correctly and the vendored bundle is current.

    This is WARN, not ERROR: it is a known, open architecture decision, not
    a regression this validator should block commits over by itself.
    Promote the affected branch to ERROR once a fix lands and is the
    intended permanent state.
    """
    findings: list[Finding] = []
    policies = build_policies()
    for path in pages:
        raw = path.read_text(encoding="utf-8", errors="replace")
        if not _page_renders_mermaid(raw):
            continue
        rel = path.relative_to(ROOT).as_posix()
        kind = page_class(path)
        policy = policies.get(kind, "")
        style_attr_directive = next(
            (part.strip() for part in policy.split(";")
             if part.strip().startswith("style-src-attr")),
            "",
        )
        if "unsafe-inline" not in style_attr_directive:
            findings.append(Finding(
                "WARN", rel,
                f"page renders live Mermaid diagrams under the {kind!r} CSP "
                "class, which only allow-lists static style hashes; Mermaid's "
                "runtime-generated inline styles will be blocked and diagrams "
                "will render without theme styling (open architecture "
                "decision, not yet fixed)",
            ))
    return findings


# Single class for all findings; severity drives behavior.
class Finding:
    __slots__ = ("severity", "page", "msg")

    def __init__(self, severity: str, page: str, msg: str):
        self.severity = severity
        self.page = page
        self.msg = msg


def check_em_dashes(path: Path, raw: str) -> list[Finding]:
    """
    Scan for em dashes (U+2014, &mdash;, &#8212;) outside allowed contexts.

    Allowed contexts (no finding raised):
      - HTML comments          (<!-- ... -->)
      - <script> blocks        (code / JS comments are not user-facing copy)
      - <style> blocks
      - <pre> blocks
      - <div class="mermaid"> / <pre class="mermaid"> blocks
      - Lines containing an <h1>–<h6> tag  (heading separator is brand-approved)
      - Lines containing a <title> tag
      - Lines with og:title / twitter:title / og:image:alt / twitter:image:alt
      - Lines containing the builder-sig class
    """
    rel = path.relative_to(ROOT).as_posix()
    findings: list[Finding] = []
    lines = raw.splitlines()

    in_comment = False
    in_script = False
    in_pre = False
    in_style = False
    in_mermaid = False

    for lineno, line in enumerate(lines, 1):
        # Update block-open state BEFORE evaluating the line so that the
        # opening tag line itself is treated as part of the block.
        if not in_comment and "<!--" in line:
            in_comment = True
        if not in_script and re.search(r"<script[\s>]", line, re.IGNORECASE):
            in_script = True
        if not in_pre and re.search(r"<pre[\s>]", line, re.IGNORECASE):
            in_pre = True
        if not in_style and re.search(r"<style[\s>]", line, re.IGNORECASE):
            in_style = True
        if not in_mermaid and re.search(r'class="[^"]*\bmermaid\b', line, re.IGNORECASE):
            in_mermaid = True

        # Is this line inside a block where em dashes are structurally expected?
        in_block = in_comment or in_script or in_pre or in_style or in_mermaid

        # Per-line tag patterns that permit an em dash regardless of block state
        line_allowed = (
            in_block
            or re.search(r"</?h[1-6][\s>]", line, re.IGNORECASE)
            or re.search(r"<title[\s>]", line, re.IGNORECASE)
            or re.search(
                r'property="og:title"|property="twitter:title"'
                r'|name="twitter:title"'
                r'|property="og:image:alt"|name="og:image:alt"'
                r'|property="twitter:image:alt"|name="twitter:image:alt"',
                line, re.IGNORECASE,
            )
            or "builder-sig" in line
        )

        if not line_allowed and EM_DASH_RE.search(line):
            findings.append(
                Finding(
                    "ERROR", rel,
                    f"em dash in body copy at line {lineno}: {line.strip()[:100]}",
                )
            )

        # Update block-close state AFTER evaluating the line
        if in_comment and "-->" in line:
            in_comment = False
        if in_script and re.search(r"</script>", line, re.IGNORECASE):
            in_script = False
        if in_pre and re.search(r"</pre>", line, re.IGNORECASE):
            in_pre = False
        if in_style and re.search(r"</style>", line, re.IGNORECASE):
            in_style = False
        if in_mermaid and re.search(r"</div>|</pre>", line, re.IGNORECASE):
            in_mermaid = False

    return findings


def validate_page(
    path: Path,
    sitemap_urls: set[str],
    expected_theme_url: str | None,
    expected_script_urls: dict[str, str | None],
) -> list[Finding]:
    findings: list[Finding] = []
    rel = path.relative_to(ROOT).as_posix()
    raw = path.read_text(encoding="utf-8", errors="replace")

    # --- raw-string brand checks (don't need parsed DOM) ---
    if "Precision. Power. Presence" in raw or "Precision · Power · Presence" in raw:
        findings.append(Finding("ERROR", rel, "old tagline 'Power. Presence.' found — must be 'Precision · Protocol · Promptcraft'"))

    # A malformed closing annotation such as `</div> /container` is parsed as
    # visible body text. Keep these template labels inside HTML comments.
    for match in re.finditer(
        r"</[a-z][\w:-]*>\s+/(?:[.#])?[A-Za-z][\w.-]*(?=\s|$)",
        raw,
        re.IGNORECASE,
    ):
        findings.append(
            Finding(
                "ERROR",
                rel,
                f"leaked closing annotation rendered as body text: {match.group(0).strip()!r}",
            )
        )

    # A malformed section-marker comment such as `</section>\nLABEL TEXT\n<section`
    # is parsed as visible orphaned body text between sections (the opening-side
    # counterpart to the closing-annotation check above -- same root cause,
    # different flavor: `<!-- LABEL -->` losing its comment delimiters). Keep
    # these template labels inside HTML comments.
    for match in re.finditer(
        r"</section>\s*\n[ \t]*([^\s<][^\n]*?)[ \t]*\n\s*<",
        raw,
    ):
        findings.append(
            Finding(
                "ERROR",
                rel,
                f"leaked section-marker annotation rendered as body text: {match.group(1)!r}",
            )
        )

    # P3 (no superscript) inside <title> or <meta ...>
    for m in re.finditer(r"<(title|meta)[^>]*>", raw):
        chunk = m.group(0)
        if re.search(r"\bP3\b", chunk) and "P³" not in chunk:
            # ignore github.com/OKHP3 path occurrences (legitimate org handle)
            if "github.com/OKHP3" not in chunk and "OKHP3" not in chunk:
                findings.append(Finding("ERROR", rel, f"'P3' without superscript in {m.group(1)} tag — brand violation"))

    # footer brand name: must be OverKill&nbsp;Hill&nbsp;P³™ (not missing ™ or prefixed with "The ")
    if re.search(r"<h3>OverKill&nbsp;Hill&nbsp;P³</h3>", raw):
        findings.append(Finding("ERROR", rel, "footer brand name missing ™ — should be 'OverKill&nbsp;Hill&nbsp;P³™'"))
    if re.search(r"<h3>The OverKill&nbsp;Hill&nbsp;P³", raw):
        findings.append(Finding("WARN", rel, "footer brand name has 'The ' prefix — canonical form has no 'The'"))

    # GA4 tag presence
    if "G-VJ1BKXS27H" not in raw:
        findings.append(Finding("WARN", rel, "GA4 tag (G-VJ1BKXS27H) not found"))

    # og:title comma-separator (brand standard is middot · or pipe |, not comma)
    m_og = re.search(r'property="og:title"\s+content="([^"]+)"', raw)
    if m_og:
        og_val = m_og.group(1)
        # only flag if it looks like the middot terms but uses comma between them
        if re.search(r"Precision,\s*Protocol", og_val):
            findings.append(Finding("ERROR", rel, f"og:title uses comma between brand terms — use middot · (found: {og_val!r})"))

    # placeholder hrefs
    for m in re.finditer(r'href="(#|javascript:[^"]*|)"', raw):
        # bare "#" anchor used as a placeholder (not a real fragment) — flag.
        # but allow href="#main" / href="#protocols" etc (fragments to real ids)
        href = m.group(1)
        if href in ("", "#"):
            findings.append(Finding("WARN", rel, f"placeholder href={href!r}"))
        elif href.startswith("javascript:"):
            findings.append(Finding("ERROR", rel, f"javascript: href found ({href!r})"))

    # --- em dash voice check ---
    findings.extend(check_em_dashes(path, raw))

    # --- parsed DOM checks ---
    parser = TagCounter()
    try:
        parser.feed(raw)
    except Exception as exc:  # html.parser is forgiving but be defensive
        findings.append(Finding("WARN", rel, f"HTML parser exception: {exc}"))
        return findings

    if not parser.title:
        findings.append(Finding("ERROR", rel, "missing <title>"))
    if not parser.has_meta_description:
        findings.append(Finding("ERROR", rel, "missing meta description"))
    if not parser.has_canonical:
        findings.append(Finding("WARN", rel, "missing canonical link"))
    if parser.h1_count == 0:
        findings.append(Finding("ERROR", rel, "no <h1> found"))
    elif parser.h1_count > 1:
        findings.append(Finding("WARN", rel, f"{parser.h1_count} <h1> elements (should be 1)"))
    if not parser.has_jsonld:
        findings.append(Finding("WARN", rel, "no JSON-LD structured data"))

    # Shared stylesheet cache-busting. A content hash changes whenever theme.css
    # changes, making browsers request the responsive rules released with it.
    theme_refs = [href for href in parser.stylesheet_refs if is_asset_ref(href, THEME_STYLESHEET_PATH)]
    if expected_theme_url is None:
        findings.append(Finding("ERROR", rel, "shared stylesheet file is missing"))
    elif len(theme_refs) != 1:
        findings.append(
            Finding(
                "ERROR",
                rel,
                f"expected exactly one shared stylesheet reference, found {len(theme_refs)}",
            )
        )
    elif theme_refs[0] != expected_theme_url:
        findings.append(
            Finding(
                "ERROR",
                rel,
                f"stale stylesheet reference {theme_refs[0]!r}; expected {expected_theme_url!r}",
            )
        )

    # Shared script cache-busting. app.js is site-wide and must have exactly
    # one current reference on every page. Mermaid is loaded only on diagram
    # pages, but any reference must likewise use its current content hash.
    for script_path in SHARED_SCRIPT_PATHS:
        script_refs = [
            src for src in parser.script_refs if is_asset_ref(src, script_path)
        ]
        expected_script_url = expected_script_urls[script_path]
        script_name = Path(script_path).name

        if expected_script_url is None:
            findings.append(Finding("ERROR", rel, f"shared script file is missing: {script_name}"))
        elif script_path == APP_SCRIPT_PATH and len(script_refs) != 1:
            findings.append(
                Finding(
                    "ERROR",
                    rel,
                    f"expected exactly one shared app.js reference, found {len(script_refs)}",
                )
            )
        elif len(script_refs) > 1:
            findings.append(
                Finding(
                    "ERROR",
                    rel,
                    f"expected at most one shared {script_name} reference, found {len(script_refs)}",
                )
            )
        elif script_refs and script_refs[0] != expected_script_url:
            findings.append(
                Finding(
                    "ERROR",
                    rel,
                    f"stale shared script reference {script_refs[0]!r}; expected {expected_script_url!r}",
                )
            )

    # sitemap inclusion (non-noindex, non-utility pages only)
    canonical_url = SITE_ORIGIN + html_to_route(path)
    if not parser.is_noindex and rel not in ("404.html", "under-construction.html"):
        if canonical_url not in sitemap_urls:
            findings.append(Finding("ERROR", rel, f"missing from sitemap.xml ({canonical_url})"))

    # noindex pages must NOT be in sitemap
    if parser.is_noindex and canonical_url in sitemap_urls:
        findings.append(Finding("ERROR", rel, f"noindex page listed in sitemap.xml — remove it ({canonical_url})"))

    # internal link + asset existence
    for ref in parser.asset_refs:
        target = resolve_internal(ref, path)
        if target is not None and not target_exists(target):
            findings.append(Finding("ERROR", rel, f"broken asset reference: {ref}"))

    for a in parser.anchors:
        href = a["href"]
        target = resolve_internal(href, path)
        if target is not None and not target_exists(target):
            # ignore pure-fragment hrefs (no path)
            if not href.startswith("#"):
                findings.append(Finding("ERROR", rel, f"broken internal link: {href}"))

        # external target=_blank must carry rel=noopener (or noreferrer)
        parsed = urlparse(href)
        if parsed.scheme in ("http", "https") and "overkillhill.com" not in parsed.netloc:
            if a["target"] == "_blank" and "noopener" not in a["rel"]:
                findings.append(Finding("ERROR", rel, f"external target=_blank without rel=noopener: {href}"))

    return findings


def run_mtb_version_check() -> int:
    """Run check-mtb-version.py and stream its output. Returns its exit code."""
    script = Path(__file__).resolve().parent / "check-mtb-version.py"
    print("── MTB Version Check ──────────────────────────────────────────────")
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")
    return result.returncode


def run_banner_check() -> int:
    """Run check-banner.py and stream its output. Returns its exit code."""
    script = Path(__file__).resolve().parent / "check-banner.py"
    print("\u2500\u2500 Banner Consistency Check \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")
    return result.returncode



def run_voice_lint() -> int:
    """Run the voice-lint baseline gate and stream its output."""
    script = Path(__file__).resolve().parent / "lint-voice.py"
    baseline = Path(__file__).resolve().parent / "voice-lint-baseline.json"
    print("\u2500\u2500 Voice Lint \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
    result = subprocess.run(
        [sys.executable, str(script), "--baseline", str(baseline)],
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")
    return result.returncode

def main() -> int:
    sitemap_urls = load_sitemap_urls()
    if not sitemap_urls:
        print("WARN: sitemap.xml not found or empty.")

    pages = find_html_files()
    print(f"Validating {len(pages)} HTML pages…\n")

    all_findings: list[Finding] = []
    all_findings.extend(validate_sitemap_inventory(sitemap_urls))
    all_findings.extend(validate_csp_hashes(pages))
    all_findings.extend(validate_mermaid_runtime(pages))
    all_findings.extend(validate_mermaid_version_pin(pages))
    all_findings.extend(validate_mermaid_csp_alignment(pages))
    expected_theme_url = current_content_hashed_url(THEME_STYLESHEET_PATH)
    expected_script_urls = {
        script_path: current_content_hashed_url(script_path)
        for script_path in SHARED_SCRIPT_PATHS
    }
    if expected_theme_url is None:
        all_findings.append(
            Finding(
                "ERROR",
                "assets/css/theme.css",
                "shared stylesheet is missing; cannot validate cache fingerprint",
            )
        )
    for script_path, expected_script_url in expected_script_urls.items():
        if expected_script_url is None:
            all_findings.append(
                Finding(
                    "ERROR",
                    script_path.lstrip("/"),
                    "shared script is missing; cannot validate cache fingerprint",
                )
            )
    for path in pages:
        all_findings.extend(
            validate_page(path, sitemap_urls, expected_theme_url, expected_script_urls)
        )

    errors = [f for f in all_findings if f.severity == "ERROR"]
    warnings = [f for f in all_findings if f.severity == "WARN"]

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for f in errors:
            print(f"  ✖ {f.page}: {f.msg}")
        print()
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for f in warnings:
            print(f"  ! {f.page}: {f.msg}")
        print()

    if not errors and not warnings:
        print("✓ all clean.")
    elif not errors:
        print(f"✓ no errors ({len(warnings)} warnings).")
    else:
        print(f"✖ {len(errors)} error(s), {len(warnings)} warning(s).")

    print()
    mtb_exit = run_mtb_version_check()

    print()
    banner_exit = run_banner_check()

    print()
    voice_exit = run_voice_lint()

    return 1 if (errors or mtb_exit != 0 or banner_exit != 0 or voice_exit != 0) else 0


if __name__ == "__main__":
    sys.exit(main())
