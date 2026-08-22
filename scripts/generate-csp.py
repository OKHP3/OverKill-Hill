#!/usr/bin/env python3
"""Generate canonical CSP policies and apply them to every HTML page."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from csp import POLICY_FILE, ROOT, all_pages, build_edge_policy, build_policies, page_class, render_meta


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated output is stale")
    args = parser.parse_args(argv)
    policies = build_policies()
    output = json.dumps({"schema": 1, "policies": policies}, indent=2) + "\n"
    if args.check:
        if not POLICY_FILE.exists() or POLICY_FILE.read_text(encoding="utf-8") != output:
            print("CSP policy file is stale. Run: python3 scripts/generate-csp.py")
            return 1
    else:
        POLICY_FILE.parent.mkdir(parents=True, exist_ok=True)
        POLICY_FILE.write_text(output, encoding="utf-8")
        headers = ROOT / "_headers"
        header_source = headers.read_text(encoding="utf-8")
        header_pattern = re.compile(
            r"(?m)^\s*Content-Security-Policy(?:-Report-Only)?:\s*.*$"
        )
        header_line = "  Content-Security-Policy: " + build_edge_policy()
        updated_headers, count = header_pattern.subn(header_line, header_source, count=1)
        if count != 1:
            failures = ["_headers: expected one CSP header"]
        else:
            headers.write_text(updated_headers, encoding="utf-8")

    failures = locals().get("failures", [])
    meta_pattern = re.compile(
        r'<meta\s+http-equiv=["\']Content-Security-Policy["\']\s+content=(["\']).*?\1\s*/?>',
        re.IGNORECASE,
    )
    for page in all_pages():
        source = page.read_text(encoding="utf-8", errors="replace")
        expected = render_meta(policies[page_class(page)])
        if args.check:
            if source.count("http-equiv=\"Content-Security-Policy\"") != 1 or meta_policy(source) != policies[page_class(page)]:
                failures.append(f"{page}: CSP differs from {page_class(page)} canonical policy")
        else:
            updated, count = meta_pattern.subn(expected, source, count=1)
            if count != 1:
                failures.append(f"{page}: expected exactly one CSP meta tag")
            else:
                page.write_text(updated, encoding="utf-8", newline="")
    if failures:
        print("\n".join(failures))
        return 1
    print(f"CSP policies verified for {len(all_pages())} pages.")
    return 0


def meta_policy(source: str) -> str | None:
    match = re.search(
        r'<meta\s+http-equiv=["\']Content-Security-Policy["\']\s+content=(["\'])(.*?)\1',
        source,
        re.IGNORECASE,
    )
    return match.group(2) if match else None


if __name__ == "__main__":
    raise SystemExit(main())