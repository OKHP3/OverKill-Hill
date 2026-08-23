#!/usr/bin/env python3
"""Read-only post-deploy verifier for a static site live edge.

The base URL is intentionally required.  This helper never publishes, mutates
the repository, or uses credentials.  It checks the repository's sitemap,
representative noindex boundaries, security headers, generated search index,
and content-hashed CSS/JS responses.

Usage:
    python3 scripts/verify-live-edge.py --base https://example.com
    python3 scripts/verify-live-edge.py --base https://example.com \
        --expected-commit "$GITHUB_SHA" \
        --report assets/audit/live-edge-report.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SITEMAP = ROOT / "sitemap.xml"
SEARCH_INDEX = ROOT / "assets" / "data" / "search-index.json"
RELEASE_MANIFEST = "/assets/audit/release-manifest.json"
TIMEOUT = 10.0
USER_AGENT = "OKHP3-live-edge-verifier/1.0 (read-only)"
GITHUB_PAGES_POLICY_NOTE = (
    "GitHub Pages serves this response but does not apply repository _headers; "
    "configure the custom edge proxy before treating this policy as enforced"
)
SECURITY_HEADERS = {
    "x-content-type-options": "nosniff",
    "x-frame-options": "SAMEORIGIN",
    "referrer-policy": "strict-origin-when-cross-origin",
    "permissions-policy": "accelerometer=(), ambient-light-sensor=(), autoplay=(), battery=(), camera=(), display-capture=(), document-domain=(), encrypted-media=(), fullscreen=(self), gamepad=(), geolocation=(), gyroscope=(), hid=(), idle-detection=(), interest-cohort=(), magnetometer=(), microphone=(), midi=(), payment=(), picture-in-picture=(self), publickey-credentials-get=(), screen-wake-lock=(), serial=(), sync-xhr=(), usb=(), web-share=(self), xr-spatial-tracking=()",
    "strict-transport-security": "max-age=63072000; includeSubDomains; preload",
    "cross-origin-opener-policy": "same-origin",
    "cross-origin-resource-policy": "same-origin",
    "origin-agent-cluster": "?1",
    "content-security-policy-report-only": "default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' data: https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https://www.google-analytics.com https://www.googletagmanager.com https://cdn.jsdelivr.net; frame-ancestors 'self'; base-uri 'self'; form-action 'self'; object-src 'none'; manifest-src 'self'; upgrade-insecure-requests",
}
HTML_CACHE_RE = re.compile(r"max-age=300\b", re.I)
REVALIDATE_RE = re.compile(r"\bmust-revalidate\b", re.I)
IMMUTABLE_RE = re.compile(r"\bimmutable\b", re.I)
FINGERPRINT_RE = re.compile(r"(?:^|&)v=([0-9a-f]{8})(?:&|$)", re.I)
ASSET_RE = re.compile(
    r"""(?:href|src)=(['"])(?P<url>/assets/(?:css|js)/[^'"?#]+(?:\?[^'"#]*)?)\1""",
    re.I,
)
ROBOTS_RE = re.compile(
    r"""<meta\b[^>]*\bname=["']robots["'][^>]*\bcontent=["']([^"']+)["']""",
    re.I,
)


def canonical_text_bytes(path: Path) -> bytes:
    """Match GitHub Pages' LF text bytes from Windows CRLF checkouts."""
    return path.read_bytes().replace(b"\r\n", b"\n")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def result(check: str, status: str, evidence: str, **extra: Any) -> dict[str, Any]:
    item = {"check": check, "status": status, "evidence": evidence}
    item.update(extra)
    return item


def transport_status(response: dict[str, Any]) -> str:
    """Keep network/timeout limits distinct from an HTTP deployment failure."""
    return "BLOCKED" if response.get("status") is None else "FAIL"


def fetch(base: str, path: str, timeout: float = TIMEOUT) -> dict[str, Any]:
    url = urllib.parse.urljoin(base.rstrip("/") + "/", path.lstrip("/"))
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"}
    )
    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            headers = {k.lower(): v.strip() for k, v in response.headers.items()}
            return {
                "ok": True,
                "url": response.geturl(),
                "status": response.status,
                "headers": headers,
                "body": body,
                "elapsed_ms": round((time.monotonic() - started) * 1000),
            }
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as exc:
        headers = {}
        body = b""
        status = getattr(exc, "code", None)
        if isinstance(exc, urllib.error.HTTPError):
            headers = {k.lower(): v.strip() for k, v in exc.headers.items()}
            try:
                body = exc.read()
            except OSError:
                pass
        return {
            "ok": False,
            "url": url,
            "status": status,
            "headers": headers,
            "body": body,
            "error": f"{type(exc).__name__}: {exc}",
            "elapsed_ms": round((time.monotonic() - started) * 1000),
        }


def path_from_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    path = parsed.path or "/"
    return path if path.endswith("/") or path.rsplit("/", 1)[-1].find(".") >= 0 else path + "/"


def load_routes() -> tuple[list[str], str | None]:
    if not SITEMAP.is_file():
        return [], "sitemap.xml is missing"
    try:
        root = ET.fromstring(SITEMAP.read_bytes())
    except (ET.ParseError, OSError) as exc:
        return [], f"sitemap.xml is unreadable: {exc}"
    routes: list[str] = []
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1] == "loc" and node.text:
            routes.append(path_from_url(node.text.strip()))
    duplicate = sorted({route for route in routes if routes.count(route) > 1})
    if not routes:
        return [], "sitemap.xml contains no routes"
    if duplicate:
        return [], f"sitemap.xml contains duplicate routes: {', '.join(duplicate)}"
    return routes, None


def check_headers(
    report: list[dict[str, Any]], label: str, response: dict[str, Any], hosting: str
) -> None:
    if not response.get("ok"):
        return
    headers = response["headers"]
    for name, expected in SECURITY_HEADERS.items():
        value = headers.get(name)
        if hosting == "github-pages":
            report.append(result(f"{label} security header {name}", "BLOCKED", GITHUB_PAGES_POLICY_NOTE))
            continue
        if not value:
            report.append(result(f"{label} security header {name}", "FAIL", "header absent"))
        elif expected and value.lower() != expected.lower():
            report.append(
                result(
                    f"{label} security header {name}",
                    "FAIL",
                    f"expected {expected!r}, received {value!r}",
                )
            )
        else:
            report.append(result(f"{label} security header {name}", "PASS", value))


def check_page(
    report: list[dict[str, Any]],
    base: str,
    path: str,
    expected_indexable: bool,
    timeout: float,
    hosting: str,
) -> tuple[dict[str, Any] | None, str]:
    response = fetch(base, path, timeout)
    label = f"route {path}"
    status = response.get("status")
    if not response.get("ok") or status != 200:
        report.append(
            result(label, transport_status(response), response.get("error", f"HTTP {status}"), http_status=status)
        )
        return None, ""
    content_type = response["headers"].get("content-type", "")
    body = response["body"].decode("utf-8", errors="replace")
    if "text/html" not in content_type.lower():
        report.append(
            result(
                label,
                "FAIL",
                f"content-type is {content_type!r}",
                http_status=status,
                response_headers=dict(sorted(response["headers"].items())),
            )
        )
    else:
        report.append(
            result(
                label,
                "PASS",
                f"HTTP 200; {content_type}",
                http_status=status,
                response_headers=dict(sorted(response["headers"].items())),
            )
        )
    robots_match = ROBOTS_RE.search(body)
    robots = robots_match.group(1).lower() if robots_match else ""
    has_noindex = "noindex" in robots
    if has_noindex == expected_indexable:
        wanted = "indexable" if expected_indexable else "noindex"
        report.append(result(f"{label} robots boundary", "FAIL", f"expected {wanted}, received {robots or 'none'}"))
    else:
        wanted = "indexable" if expected_indexable else "noindex"
        report.append(result(f"{label} robots boundary", "PASS", f"{wanted}; {robots or 'no robots meta'}"))
    cache = response["headers"].get("cache-control", "")
    cache_passed = bool(HTML_CACHE_RE.search(cache)) and bool(REVALIDATE_RE.search(cache))
    cache_status = "PASS" if cache_passed else "FAIL"
    if hosting == "github-pages":
        cache_status = "BLOCKED"
    report.append(result(f"{label} cache policy", cache_status,
                         GITHUB_PAGES_POLICY_NOTE if hosting == "github-pages" else (cache or "Cache-Control absent")))
    check_headers(report, label, response, hosting)
    return response, body


def check_release_manifest(
    report: list[dict[str, Any]],
    base: str,
    expected_commit: str,
    timeout: float,
) -> None:
    """Require the live edge to identify the commit whose files were validated."""
    response = fetch(base, RELEASE_MANIFEST, timeout)
    label = "release manifest"
    if not response.get("ok") or response.get("status") != 200:
        report.append(
            result(
                label,
                transport_status(response),
                response.get("error", f"HTTP {response.get('status')}"),
            )
        )
        return

    try:
        manifest = json.loads(response["body"])
    except (ValueError, UnicodeDecodeError) as exc:
        report.append(result(label, "FAIL", f"invalid JSON: {exc}"))
        return

    if not isinstance(manifest, dict):
        report.append(result(label, "FAIL", "expected a JSON object"))
        return
    commit = manifest.get("commit")
    artifacts = manifest.get("artifacts")
    if commit != expected_commit:
        report.append(
            result(
                label,
                "FAIL",
                f"expected validated commit {expected_commit}, received {commit!r}",
            )
        )
    elif not isinstance(artifacts, dict):
        report.append(result(label, "FAIL", "artifacts map is missing"))
    else:
        report.append(result(label, "PASS", f"validated commit {commit}"))

    expected_artifacts = {
        "/sitemap.xml": SITEMAP,
        "/assets/data/search-index.json": SEARCH_INDEX,
    }
    if not isinstance(artifacts, dict):
        return
    for public_path, local_path in expected_artifacts.items():
        entry = artifacts.get(public_path)
        manifest_hash = entry.get("sha256") if isinstance(entry, dict) else None
        local_hash = (
            hashlib.sha256(canonical_text_bytes(local_path)).hexdigest()
            if local_path.is_file()
            else None
        )
        if not manifest_hash:
            report.append(
                result(
                    f"release manifest {public_path}",
                    "FAIL",
                    "artifact SHA-256 is missing",
                )
            )
        elif local_hash is None:
            report.append(
                result(
                    f"release manifest {public_path}",
                    "FAIL",
                    f"local artifact missing: {local_path}",
                )
            )
        elif manifest_hash != local_hash:
            report.append(
                result(
                    f"release manifest {public_path}",
                    "FAIL",
                    f"manifest SHA-256 {manifest_hash[:12]} differs from local {local_hash[:12]}",
                )
            )
        else:
            report.append(
                result(
                    f"release manifest {public_path}",
                    "PASS",
                    f"SHA-256 {manifest_hash[:12]} matches validated files",
                )
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="Explicit deployed origin, e.g. https://overkillhill.com")
    parser.add_argument("--timeout", type=float, default=TIMEOUT, help=f"Per-request timeout in seconds (default: {TIMEOUT:g})")
    parser.add_argument("--report", type=Path, help="Write the JSON report to this path")
    parser.add_argument(
        "--expected-commit",
        help="Require the deployed release manifest to identify this validated commit",
    )
    parser.add_argument(
        "--hosting",
        choices=("strict", "github-pages"),
        default="strict",
        help="Hosting policy to verify; GitHub Pages cannot apply repository _headers",
    )
    parser.add_argument(
        "--accept-blocked",
        action="store_true",
        help="Return success when only hosting limitations are BLOCKED",
    )
    parser.add_argument("--noindex-route", action="append", default=["/404.html", "/found-ry/"],
                        help="Additional utility/noindex route (repeatable)")
    args = parser.parse_args()
    parsed_base = urllib.parse.urlparse(args.base)
    if parsed_base.scheme not in {"http", "https"} or not parsed_base.netloc:
        parser.error("--base must be an explicit http(s) origin")
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    report: list[dict[str, Any]] = []
    if args.expected_commit:
        check_release_manifest(report, args.base, args.expected_commit, args.timeout)
    routes, sitemap_error = load_routes()
    if sitemap_error:
        report.append(result("local sitemap inventory", "FAIL", sitemap_error))
    else:
        report.append(result("local sitemap inventory", "PASS", f"{len(routes)} unique routes"))

    responses: dict[str, dict[str, Any]] = {}
    bodies: dict[str, str] = {}
    for route in routes:
        response, body = check_page(report, args.base, route, True, args.timeout, args.hosting)
        if response:
            responses[route] = response
            bodies[route] = body

    for route in dict.fromkeys(args.noindex_route):
        if route in responses:
            continue
        response, body = check_page(report, args.base, route, False, args.timeout, args.hosting)
        if response:
            responses[route] = response
            bodies[route] = body

    # Verify the two generated public artifacts against the checked-out release.
    for path, local_path, kind in [
        ("/sitemap.xml", SITEMAP, "sitemap"),
        ("/assets/data/search-index.json", SEARCH_INDEX, "search index"),
    ]:
        response = fetch(args.base, path, args.timeout)
        if not response.get("ok") or response.get("status") != 200:
            report.append(result(f"generated {kind}", transport_status(response),
                                 response.get("error", f"HTTP {response.get('status')}")))
            continue
        remote_hash = hashlib.sha256(response["body"]).hexdigest()
        local_hash = (
            hashlib.sha256(canonical_text_bytes(local_path)).hexdigest()
            if local_path.is_file()
            else None
        )
        if local_hash is None:
            report.append(
                result(
                    f"generated {kind}",
                    "FAIL",
                    f"local artifact missing: {local_path}",
                    remote_sha256=remote_hash,
                )
            )
        elif remote_hash != local_hash:
            report.append(
                result(
                    f"generated {kind}",
                    "FAIL",
                    f"live SHA-256 {remote_hash[:12]} differs from local {local_hash[:12]}",
                    remote_sha256=remote_hash,
                    local_sha256=local_hash,
                )
            )
        else:
            report.append(
                result(
                    f"generated {kind}",
                    "PASS",
                    f"HTTP 200; SHA-256 {remote_hash[:12]}",
                    remote_sha256=remote_hash,
                    local_sha256=local_hash,
                )
            )
        if kind == "search index":
            try:
                parsed = json.loads(response["body"])
                count = parsed.get("count") if isinstance(parsed, dict) else None
                if not isinstance(parsed, dict) or not isinstance(count, int) or count <= 0:
                    report.append(result("search index shape", "FAIL", "expected a JSON object with positive integer count"))
                else:
                    report.append(result("search index shape", "PASS", f"{count} indexed pages"))
            except (ValueError, UnicodeDecodeError) as exc:
                report.append(result("search index shape", "FAIL", f"invalid JSON: {exc}"))
        cache = response["headers"].get("cache-control", "")
        if kind == "search index":
            passed = bool(cache) and not IMMUTABLE_RE.search(cache) and bool(re.search(r"max-age=(?:[0-9]|[1-2][0-9]{1,2}|300)\b", cache, re.I))
            cache_status = "PASS" if passed else "FAIL"
            if args.hosting == "github-pages":
                cache_status = "BLOCKED"
            report.append(result("search index cache policy", cache_status, GITHUB_PAGES_POLICY_NOTE if args.hosting == "github-pages" else (cache or "Cache-Control absent")))
        else:
            cache_status = "PASS" if HTML_CACHE_RE.search(cache) and REVALIDATE_RE.search(cache) else "FAIL"
            if args.hosting == "github-pages":
                cache_status = "BLOCKED"
            report.append(result("sitemap cache policy", cache_status, GITHUB_PAGES_POLICY_NOTE if args.hosting == "github-pages" else (cache or "Cache-Control absent")))
        check_headers(report, f"generated {kind}", response, args.hosting)

    # Every shared CSS/JS asset referenced by fetched HTML must carry its
    # content hash and be served immutable at the live edge.
    assets: dict[str, str] = {}
    for body in bodies.values():
        for match in ASSET_RE.finditer(body):
            assets[match.group("url").split("#", 1)[0]] = match.group("url")
    if not assets:
        report.append(result("fingerprinted shared assets", "FAIL", "no CSS/JS references found in fetched HTML"))
    for asset_url in sorted(assets):
        parsed = urllib.parse.urlparse(asset_url)
        fingerprint = FINGERPRINT_RE.search(parsed.query)
        path = parsed.path
        local_path = ROOT / path.lstrip("/")
        expected_hash = (
            hashlib.sha256(canonical_text_bytes(local_path)).hexdigest()[:8]
            if local_path.is_file()
            else None
        )
        response = fetch(args.base, asset_url, args.timeout)
        if not fingerprint:
            report.append(result(f"asset {path}", "FAIL", "missing 8-character ?v= fingerprint"))
            continue
        if expected_hash and fingerprint.group(1).lower() != expected_hash.lower():
            report.append(result(f"asset {path}", "FAIL", f"URL fingerprint {fingerprint.group(1)} != local {expected_hash}"))
        elif not response.get("ok") or response.get("status") != 200:
            report.append(result(f"asset {path}", transport_status(response),
                                 response.get("error", f"HTTP {response.get('status')}")))
        else:
            cache = response["headers"].get("cache-control", "")
            passed = bool(IMMUTABLE_RE.search(cache)) and bool(re.search(r"max-age=(?:[0-9]{8,}|31536000)\b", cache, re.I))
            asset_status = "PASS" if passed else "FAIL"
            if args.hosting == "github-pages":
                asset_status = "BLOCKED"
            report.append(result(f"asset {path}", asset_status, GITHUB_PAGES_POLICY_NOTE if args.hosting == "github-pages" else f"HTTP 200; {cache or 'Cache-Control absent'}"))

    failures = sum(item["status"] == "FAIL" for item in report)
    blocked = sum(item["status"] == "BLOCKED" for item in report)
    payload = {
        "verifier": "verify-live-edge.py",
        "run_at": now(),
        "base": args.base.rstrip("/"),
        "timeout_seconds": args.timeout,
        "expected_commit": args.expected_commit,
        "hosting": args.hosting,
        "status": "FAILED" if failures else ("PARTIAL" if blocked else "PASS"),
        "summary": {"checks": len(report), "failures": failures, "blocked": blocked},
        "checks": report,
    }
    encoded = json.dumps(payload, indent=2, sort_keys=False) + "\n"
    print(encoded, end="")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(encoded, encoding="utf-8")
    return 1 if failures or (blocked and not args.accept_blocked) or not routes else 0


if __name__ == "__main__":
    sys.exit(main())
