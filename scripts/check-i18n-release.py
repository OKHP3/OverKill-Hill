#!/usr/bin/env python3
"""Apply this site's published-locale gate around the portable i18n detector."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
DETECTOR_PATH = ROOT / ".agents" / "skills" / "okhp3-i18n-page-sync" / "scripts" / "i18n-page-sync.py"
SOURCE_HASHES_PATH = ROOT / "i18n" / "pilot" / "source-hashes-release-0ee.json"
CSP_META_RE = re.compile(
    rb'<meta\b(?=[^>]*\bhttp-equiv=["\']Content-Security-Policy["\'])[^>]*>',
    re.I,
)
ASSET_FINGERPRINT_RE = re.compile(
    rb'(\b(?:href|src)=["\'][^"\']*/assets/[^"\']*?)\?v=[0-9a-f]{8,64}(?=["\'])',
    re.I,
)


def load_site_config() -> Dict[str, Any]:
    path = ROOT / "i18n" / "sync.config.json"
    if not path.is_file():
        raise ValueError(f"missing site i18n policy: {path}")
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid site i18n policy: {exc}") from exc
    if not isinstance(config, dict) or config.get("schema_version") != "1.0":
        raise ValueError("site i18n policy must declare schema_version 1.0")
    blocking = config.get("blocking_locales")
    targets = config.get("target_locales", {})
    if not isinstance(blocking, list) or not blocking or not all(isinstance(item, str) for item in blocking):
        raise ValueError("blocking_locales must be a non-empty list")
    unknown = sorted(set(blocking) - set(targets))
    if unknown:
        raise ValueError(f"blocking_locales contains unconfigured locales: {unknown}")
    return config


def run_detector(config_path: Path, mode: str = "report") -> Dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(DETECTOR_PATH), "--root", str(ROOT), "--config", str(config_path), "--mode", mode, "--format", "json"],
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise ValueError(f"portable i18n detector failed ({completed.returncode}): {completed.stderr.strip()}")
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(f"portable i18n detector returned malformed JSON: {exc}") from exc
    if mode == "report" and (not isinstance(result, dict) or not all(key in result for key in ("missing", "stale", "needs_baseline", "in_sync", "orphan"))):
        raise ValueError("portable i18n detector returned an incomplete report")
    return result


def normalized_translation_hash(path: Path) -> str:
    """Hash editorial source while excluding generated release metadata."""
    content = path.read_bytes().replace(b"\r\n", b"\n")
    content = CSP_META_RE.sub(b"", content)
    content = ASSET_FINGERPRINT_RE.sub(rb"\1", content)
    return hashlib.sha256(content).hexdigest()


def generated_metadata_only(route: str) -> bool:
    """Return true when detector drift is only CSP or asset fingerprints."""
    if not SOURCE_HASHES_PATH.is_file():
        return False
    expected = json.loads(SOURCE_HASHES_PATH.read_text(encoding="utf-8"))
    release_hash = expected.get("normalized_routes", {}).get(route)
    source_rel = "index.html" if route == "/" else f"{route.strip('/')}/index.html"
    source_path = ROOT / source_rel
    return bool(release_hash and source_path.is_file() and normalized_translation_hash(source_path) == release_hash)


def load_results(config: Dict[str, Any]) -> Dict[str, Any]:
    config_path = ROOT / "i18n" / "sync.config.json"
    results = run_detector(config_path)
    blocking = set(config["blocking_locales"])
    blocking_items: List[Dict[str, Any]] = []
    advisory_items: List[Dict[str, Any]] = []
    metadata_only: List[Dict[str, Any]] = []
    retained_stale: List[Dict[str, Any]] = []
    for item in results["stale"]:
        if generated_metadata_only(item["route"]):
            metadata_only.append(item)
        else:
            retained_stale.append(item)
    results["stale"] = retained_stale
    for status in ("missing", "stale", "needs_baseline"):
        for item in results[status]:
            (blocking_items if item["locale"] in blocking else advisory_items).append(
                {"status": status, **item}
            )
    return {
        **results,
        "generated_metadata_only": metadata_only,
        "policy": {
            "blocking_locales": sorted(blocking),
            "blocking_items": blocking_items,
            "advisory_items": advisory_items,
        },
    }


def load_provenance(path: Path, locales: List[str], routes: List[str], config: Dict[str, Any]) -> None:
    if not path.is_file():
        raise ValueError(f"reviewed provenance is missing: {path}")
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid reviewed provenance: {exc}") from exc
    if len(locales) != 1:
        raise ValueError("adoption requires exactly one selected locale per provenance record")
    selected_locale = locales[0]
    configured = set(config["target_locales"])
    if not set(locales) <= configured:
        raise ValueError("adoption locales must be configured target locales")
    expected_pair = f"en-US -> {config['target_locales'][selected_locale]['locale']}"
    if record.get("language_pair") != expected_pair:
        raise ValueError(f"reviewed provenance must declare {expected_pair}")
    if record.get("review_status") not in {"ai-reviewed", "approved"}:
        raise ValueError("reviewed provenance must be ai-reviewed or approved")
    if record.get("native_or_human_approval") is True and record.get("review_status") == "ai-reviewed":
        raise ValueError("ai-reviewed provenance cannot claim human or native approval")
    entries = {item.get("route"): item for item in record.get("routes", []) if isinstance(item, dict)}
    for route in routes:
        entry = entries.get(route)
        expected_target = f"{config['target_locales'][selected_locale]['root'].strip('/')}/{route.strip('/')}/index.html" if route.strip('/') else f"{config['target_locales'][selected_locale]['root'].strip('/')}/index.html"
        if entry is None or entry.get("locale") != selected_locale or entry.get("target_path") != expected_target:
            raise ValueError(f"reviewed provenance does not cover selected locale route: {route}")
        if entry.get("disposition") not in {"retained-ai-reviewed", "approved", "no-semantic-delta-ai-reviewed"}:
            raise ValueError(f"reviewed provenance does not cover route: {route}")


def adopt(locales: List[str], routes: List[str], provenance: Path, config: Dict[str, Any]) -> int:
    if not locales or not routes:
        raise ValueError("adoption requires explicit --locales and --routes")
    load_provenance(provenance, locales, routes, config)
    reduced = dict(config)
    reduced["target_locales"] = {key: config["target_locales"][key] for key in locales}
    with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_state = temp_dir_path / "sync-state.json"
        reduced["state_file"] = str(temp_state)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
            json.dump(reduced, handle, indent=2, ensure_ascii=False)
            temp_config = Path(handle.name)
        try:
            run_detector(temp_config, mode="adopt")
            record = json.loads(provenance.read_text(encoding="utf-8"))
            by_route = {item["route"]: item for item in record["routes"]}
            state = json.loads(temp_state.read_text(encoding="utf-8"))
            for route in routes:
                adopted = state["pages"][route]["targets"][locales[0]]
                entry = by_route[route]
                if entry.get("source_sha256") != adopted.get("synced_source_sha256") or entry.get("target_sha256") != adopted.get("target_sha256"):
                    raise ValueError(f"reviewed provenance hashes do not match current files: {route}")
        finally:
            temp_config.unlink(missing_ok=True)
    reduced["state_file"] = config.get("state_file", "i18n/sync-state.json")
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
        json.dump(reduced, handle, indent=2, ensure_ascii=False)
        temp_config = Path(handle.name)
    try:
        command = [
            sys.executable,
            str(DETECTOR_PATH),
            "--root",
            str(ROOT),
            "--config",
            str(temp_config),
            "--mode",
            "adopt",
            "--format",
            "json",
            "--routes",
            *routes,
        ]
        completed = subprocess.run(command, text=True, capture_output=True, encoding="utf-8")
        if completed.returncode != 0:
            raise ValueError(f"portable i18n adoption failed ({completed.returncode}): {completed.stderr.strip()}")
        try:
            adoption_result = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise ValueError(f"portable i18n adoption returned malformed JSON: {exc}") from exc
        if not isinstance(adoption_result, dict) or "adopted" not in adoption_result:
            raise ValueError("portable i18n adoption returned an incomplete result")
        if completed.stdout:
            print(json.dumps(adoption_result, ensure_ascii=False))
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        return completed.returncode
    finally:
        temp_config.unlink(missing_ok=True)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("report", "check", "adopt"), default="report")
    parser.add_argument("--format", choices=("json", "text"), default="json")
    parser.add_argument("--locales", nargs="*", default=None)
    parser.add_argument("--routes", nargs="*", default=None)
    parser.add_argument("--provenance", type=Path)
    args = parser.parse_args(argv)
    try:
        config = load_site_config()
        if args.mode == "adopt":
            if args.provenance is None:
                raise ValueError("--provenance is required for adoption")
            return adopt(args.locales or [], args.routes or [], args.provenance.resolve(), config)
        results = load_results(config)
        if args.format == "json":
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print(f"i18n release policy: blocking locales={','.join(results['policy']['blocking_locales'])}")
            for status in ("missing", "stale", "needs_baseline"):
                for item in results[status]:
                    label = "BLOCKING" if item["locale"] in config["blocking_locales"] else "ADVISORY"
                    print(f"{label:9} {status:14} {item['route']:20} -> {item['locale']}")
        if args.mode == "check" and results["policy"]["blocking_items"]:
            return 1
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
