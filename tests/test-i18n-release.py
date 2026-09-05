import importlib.util
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check-i18n-release.py"
SPEC = importlib.util.spec_from_file_location("check_i18n_release", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

DETECTOR = ROOT / ".agents" / "skills" / "okhp3-i18n-page-sync" / "scripts" / "i18n-page-sync.py"
DETECTOR_SPEC = importlib.util.spec_from_file_location("i18n_page_sync", DETECTOR)
DETECTOR_MODULE = importlib.util.module_from_spec(DETECTOR_SPEC)
assert DETECTOR_SPEC.loader is not None
DETECTOR_SPEC.loader.exec_module(DETECTOR_MODULE)


class I18nReleaseTests(unittest.TestCase):
    def test_detector_hash_is_stable_across_checkout_line_endings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lf = root / "lf.html"
            crlf = root / "crlf.html"
            lf.write_bytes(b"<p>stable</p>\n")
            crlf.write_bytes(b"<p>stable</p>\r\n")
            self.assertEqual(DETECTOR_MODULE.sha256_file(lf), DETECTOR_MODULE.sha256_file(crlf))

    def test_full_report_preserves_all_pairs_and_blocks_only_french(self):
        report = {
            "missing": [{"route": f"/missing-{index}/", "locale": "fr"} for index in range(4)]
            + [{"route": f"/missing-{index}/", "locale": "de"} for index in range(4)],
            "stale": [{"route": f"/stale-{index}/", "locale": "es"} for index in range(4)],
            "needs_baseline": [],
            "in_sync": [],
            "orphan": [],
        }
        config = MODULE.load_site_config()
        with patch.object(MODULE, "run_detector", return_value=report):
            result = MODULE.load_results(config)
        self.assertEqual(12, sum(len(result[key]) for key in ("missing", "stale", "needs_baseline")))
        self.assertEqual({"fr"}, {item["locale"] for item in result["policy"]["blocking_items"]})
        self.assertEqual({"de", "es"}, {item["locale"] for item in result["policy"]["advisory_items"]})
        self.assertEqual(4, len(result["policy"]["blocking_items"]))
        self.assertEqual(8, len(result["policy"]["advisory_items"]))

    def test_all_current_blocking_locale_is_not_blocked(self):
        report = {
            "missing": [],
            "stale": [{"route": "/", "locale": "de"}, {"route": "/", "locale": "es"}],
            "needs_baseline": [],
            "in_sync": [],
            "orphan": [],
        }
        config = MODULE.load_site_config()
        with patch.object(MODULE, "run_detector", return_value=report):
            result = MODULE.load_results(config)
        self.assertEqual([], result["policy"]["blocking_items"])
        self.assertEqual(2, len(result["policy"]["advisory_items"]))

    def test_invalid_blocking_locale_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "i18n").mkdir()
            (root / "i18n" / "sync.config.json").write_text(
                json.dumps({"schema_version": "1.0", "target_locales": {"fr": {}}, "blocking_locales": ["de"]}),
                encoding="utf-8",
            )
            with patch.object(MODULE, "ROOT", root):
                with self.assertRaises(ValueError):
                    MODULE.load_site_config()

    def test_malformed_portable_report_fails_closed(self):
        with patch.object(MODULE.subprocess, "run", return_value=MODULE.subprocess.CompletedProcess([], 0, "not json", "")):
            with self.assertRaises(ValueError):
                MODULE.run_detector(Path("missing-config.json"))

    def test_real_adoption_updates_only_french_ledger_entries(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "i18n").mkdir()
            (root / "assets" / "data").mkdir(parents=True)
            (root / "fr").mkdir()
            (root / "de").mkdir()
            (root / "es").mkdir()
            (root / "index.html").write_text("<html>current source</html>", encoding="utf-8")
            (root / "about").mkdir()
            (root / "about" / "index.html").write_text("<html>about source</html>", encoding="utf-8")
            for locale in ("fr", "de", "es"):
                (root / locale / "index.html").write_text(f"<html>{locale}</html>", encoding="utf-8")
                (root / locale / "about").mkdir()
                (root / locale / "about" / "index.html").write_text(f"<html>{locale} about</html>", encoding="utf-8")
            (root / "assets" / "data" / "search-index.json").write_text(
                json.dumps({"entries": [{"url": "/"}, {"url": "/about/"}]}), encoding="utf-8"
            )
            config = {
                "schema_version": "1.0",
                "search_index": "assets/data/search-index.json",
                "state_file": "i18n/sync-state.json",
                "in_scope_routes": ["/", "/about/"],
                "blocking_locales": ["fr"],
                "target_locales": {
                    key: {"locale": f"{key}-FR" if key == "fr" else key, "root": key, "skill": "pair"}
                    for key in ("fr", "de", "es")
                },
            }
            original = {
                "schema_version": "1.0",
                "pages": {
                    route: {"targets": {
                        key: {"synced_source_sha256": f"old-{key}-{route}", "target_sha256": f"target-{key}-{route}"}
                        for key in ("fr", "de", "es")
                    }}
                    for route in ("/", "/about/")
                },
            }
            (root / "i18n" / "sync-state.json").write_text(json.dumps(original), encoding="utf-8")
            provenance = root / "review.json"
            provenance.write_text(json.dumps({
                "language_pair": "en-US -> fr-FR",
                "review_status": "ai-reviewed",
                "native_or_human_approval": False,
                "routes": [{
                    "route": "/", "locale": "fr", "target_path": "fr/index.html",
                    "source_sha256": hashlib.sha256((root / "index.html").read_bytes()).hexdigest(),
                    "target_sha256": hashlib.sha256((root / "fr" / "index.html").read_bytes()).hexdigest(),
                    "disposition": "no-semantic-delta-ai-reviewed",
                }],
            }), encoding="utf-8")
            with patch.object(MODULE, "ROOT", root):
                bad_hash = json.loads(provenance.read_text(encoding="utf-8"))
                bad_hash["routes"][0]["target_sha256"] = "wrong-target-hash"
                provenance.write_text(json.dumps(bad_hash), encoding="utf-8")
                with self.assertRaises(ValueError):
                    MODULE.adopt(["fr"], ["/"], provenance, config)
                bad_source = json.loads(provenance.read_text(encoding="utf-8"))
                bad_source["routes"][0]["source_sha256"] = "wrong-source-hash"
                bad_source["routes"][0]["target_sha256"] = hashlib.sha256((root / "fr" / "index.html").read_bytes()).hexdigest()
                provenance.write_text(json.dumps(bad_source), encoding="utf-8")
                with self.assertRaises(ValueError):
                    MODULE.adopt(["fr"], ["/"], provenance, config)
                bad_locale = json.loads(provenance.read_text(encoding="utf-8"))
                bad_locale["routes"][0]["target_sha256"] = hashlib.sha256((root / "fr" / "index.html").read_bytes()).hexdigest()
                bad_locale["routes"][0]["locale"] = "de"
                provenance.write_text(json.dumps(bad_locale), encoding="utf-8")
                with self.assertRaises(ValueError):
                    MODULE.adopt(["fr"], ["/"], provenance, config)
                provenance.write_text(json.dumps({
                    "language_pair": "en-US -> fr-FR",
                    "review_status": "ai-reviewed",
                    "native_or_human_approval": False,
                    "routes": [{
                        "route": "/", "locale": "fr", "target_path": "fr/index.html",
                        "source_sha256": hashlib.sha256((root / "index.html").read_bytes()).hexdigest(),
                        "target_sha256": hashlib.sha256((root / "fr" / "index.html").read_bytes()).hexdigest(),
                        "disposition": "no-semantic-delta-ai-reviewed",
                    }],
                }), encoding="utf-8")
                self.assertEqual(0, MODULE.adopt(["fr"], ["/"], provenance, config))
            updated = json.loads((root / "i18n" / "sync-state.json").read_text(encoding="utf-8"))
            self.assertEqual(original["pages"]["/"]["targets"]["de"], updated["pages"]["/"]["targets"]["de"])
            self.assertEqual(original["pages"]["/"]["targets"]["es"], updated["pages"]["/"]["targets"]["es"])
            self.assertNotEqual(original["pages"]["/"]["targets"]["fr"], updated["pages"]["/"]["targets"]["fr"])
            for locale in ("fr", "de", "es"):
                self.assertEqual(
                    original["pages"]["/about/"]["targets"][locale],
                    updated["pages"]["/about/"]["targets"][locale],
                )


if __name__ == "__main__":
    unittest.main()
