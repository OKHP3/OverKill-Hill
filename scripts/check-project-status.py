#!/usr/bin/env python3
"""Validate the small public project-status registry."""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "site-src" / "project-status.json"
REQUIRED = {"id", "title", "purpose", "status", "surface_status", "reviewed", "route"}
SURFACES = (
    ROOT / "index.html",
    ROOT / "projects" / "index.html",
    ROOT / "universe" / "index.html",
)


def main() -> int:
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        records = data["projects"]
        assert isinstance(records, list) and records
        ids: set[str] = set()
        for record in records:
            missing = REQUIRED - record.keys()
            if missing:
                raise ValueError(f"{record.get('id', '<unknown>')}: missing {sorted(missing)}")
            if record["id"] in ids:
                raise ValueError(f"duplicate id: {record['id']}")
            ids.add(record["id"])
            if not isinstance(record["status"], str) or not record["status"].strip():
                raise ValueError(f"{record['id']}: status must be non-empty text")
            if not isinstance(record["surface_status"], str) or not record["surface_status"].strip():
                raise ValueError(f"{record['id']}: surface_status must be non-empty text")
            if "version" in record and (not isinstance(record["version"], str) or not record["version"].strip()):
                raise ValueError(f"{record['id']}: version must be non-empty text")
            date.fromisoformat(record["reviewed"])
            route = record["route"]
            if not route.startswith("/") or "?" in route or "#" in route:
                raise ValueError(f"{record['id']}: invalid route")
            target = ROOT / route.lstrip("/") / "index.html"
            if route == "/":
                target = ROOT / "index.html"
            if not target.is_file():
                raise ValueError(f"{record['id']}: route target missing: {route}")
            for optional in ("live", "source", "proof"):
                if optional in record:
                    parsed = urlparse(record[optional])
                    if optional == "proof" and record[optional].startswith("/"):
                        continue
                    if parsed.scheme != "https" or not parsed.netloc:
                        raise ValueError(f"{record['id']}: {optional} must be an https URL or local route")
        reviewed_date = date.fromisoformat(data["reviewed"])
        reviewed_label = reviewed_date.strftime("%B %d, %Y").replace(" 0", " ")
        rendered = {path: path.read_text(encoding="utf-8") for path in SURFACES}
        for path, content in rendered.items():
            soup = BeautifulSoup(content, "html.parser")
            cards = [str(card) for card in soup.find_all("article")]
            for record in records:
                matches = [card for card in cards if record["title"] in card and record["route"] in card]
                status_matches = [card for card in matches if record["surface_status"] in card]
                if record.get("version"):
                    status_matches = [card for card in status_matches if record["version"] in card]
                if not status_matches:
                    raise ValueError(f"{path.relative_to(ROOT)}: status card drift for {record['id']}")
            if reviewed_label not in content:
                raise ValueError(f"{path.relative_to(ROOT)}: missing registry review date")
        print(f"Project status registry valid: {len(records)} records")
        return 0
    except (AssertionError, KeyError, json.JSONDecodeError, OSError, ValueError) as exc:
        print(f"Project status registry invalid: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
