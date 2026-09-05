import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("performance_budget", ROOT / "scripts" / "check-performance-budget.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class PerformanceBudgetTests(unittest.TestCase):
    def test_empty_route_config_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            config_path = Path(temporary) / "budget.json"
            config_path.write_text(json.dumps({"schema_version": 1, "routes": []}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "at least one route"):
                MODULE.load_config(config_path)

    def test_committed_budgets_cover_representative_routes(self) -> None:
        config = MODULE.load_config(ROOT / "assets/data/performance-budget.json")
        results, passed = MODULE.check(ROOT, config)
        self.assertTrue(passed, results)
        self.assertEqual([result["route"] for result in results], ["/", "/writings/first-diagram-is-a-liar/", "/projects/mermaid-theme-builder/"])
        self.assertTrue(all(result["files"] for result in results))

    def test_budget_failure_and_css_dependencies_are_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "assets").mkdir()
            (root / "index.html").write_text('<link rel="stylesheet" href="/assets/site.css"><img src="/assets/pixel.png"><img src="/assets/../assets/pixel.png"><img src="/assets/missing.png">', encoding="utf-8")
            (root / "assets/site.css").write_text('body { background: url("/assets/bg.svg"); mask: url("/assets/other.css") }', encoding="utf-8")
            (root / "assets/other.css").write_text('body { mask: url("/assets/../assets/site.css") }', encoding="utf-8")
            (root / "assets/pixel.png").write_bytes(b"png")
            (root / "assets/bg.svg").write_bytes(b"svg")
            config = {"schema_version": 1, "routes": [{"route": "/", "document": "index.html", "max_bytes": 1}]}
            results, passed = MODULE.check(root, config)
            self.assertFalse(passed)
            self.assertIn("assets/bg.svg", results[0]["files"])
            self.assertEqual(results[0]["files"].count("assets/pixel.png"), 1)
            self.assertIn("assets/other.css", results[0]["files"])
            self.assertLess(results[0]["headroom_bytes"], 0)
            self.assertEqual(results[0]["missing"], ["assets/missing.png"])

    def test_route_document_cannot_escape_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaisesRegex(ValueError, "route document escapes root"):
                MODULE.collect_route(root, "../outside.html")


if __name__ == "__main__":
    unittest.main()
