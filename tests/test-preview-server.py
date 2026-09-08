#!/usr/bin/env python3
"""HTTP regressions for local preview exposure boundaries."""
import concurrent.futures
import http.client
import importlib.util
import json
import os
import subprocess
import socket
import sys
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("preview", ROOT / "server.py")
preview = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preview)


class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        for name in ("index.html", "about/index.html", "assets/js/app.js", "private.txt", ".well-known/security.txt"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("fixture", encoding="utf-8")
        self.allowed = {"index.html", "about/index.html", "assets/js/app.js", ".well-known/security.txt", "linked.html", "linked/index.html"}
        with patch.object(preview, "public_files", return_value=self.allowed):
            self.server = preview.ThreadingServer(("127.0.0.1", 0), root=self.root)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()
        self.temp.cleanup()

    def request(self, path, method="GET", body=None, headers=None):
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=7)
        try:
            connection.request(method, path, body=body, headers=headers or {})
            response = connection.getresponse()
            data = response.read()
            return response.status, data, response.getheader("Cache-Control")
        finally:
            connection.close()

    def test_public_get_head_redirect_and_private_routes(self):
        for path in ("/", "/about/", "/assets/js/app.js?v=1", "/.well-known/security.txt"):
            for method in ("GET", "HEAD"):
                with self.subTest(path=path, method=method):
                    status, body, cache = self.request(path, method)
                    self.assertEqual(status, 200)
                    self.assertIn("no-store", cache)
                    if method == "HEAD":
                        self.assertEqual(body, b"")
        self.assertEqual(self.request("/about")[0], 301)
        for path in ("/private.txt", "/server.py", "/.git/config", "/site-src/pages.json", "/assets/js/", "/%2e%2e/private.txt", "/assets/%2e%2e/private.txt", "/assets%5cjs/app.js", "/index.html:stream", "/%00"):
            with self.subTest(path=path):
                self.assertEqual(self.request(path)[0], 404)

    def test_bind_default_and_explicit_override(self):
        env = dict(os.environ)
        env.pop("HOST", None)
        code = "import runpy,sys; print(runpy.run_path(sys.argv[1])['HOST'])"
        for requested, expected in ((None, "127.0.0.1"), ("0.0.0.0", "0.0.0.0")):
            if requested is not None:
                env["HOST"] = requested
            result = subprocess.run([sys.executable, "-c", code, str(ROOT / "server.py")], cwd=self.root, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), expected)

    def test_release_allowlist(self):
        paths = preview.public_files(ROOT)
        self.assertIn("index.html", paths)
        self.assertIn("assets/js/app.js", paths)
        self.assertIn(".well-known/security.txt", paths)
        for private in ("server.py", "AGENTS.md", "site-src/pages.json", "assets/templates/template--homepage.html"):
            self.assertNotIn(private, paths)

    def test_symlinks_inside_and_outside_and_parent(self):
        link = self.root / "linked.html"
        try:
            link.symlink_to(self.root / "private.txt")
        except OSError as exc:
            self.skipTest(f"symlink creation unavailable: {exc}")
        self.assertEqual(self.request("/linked.html")[0], 404)
        link.unlink()
        link.symlink_to(ROOT / "server.py")
        self.assertEqual(self.request("/linked.html")[0], 404)
        (self.root / "linked").symlink_to(self.root / "about", target_is_directory=True)
        self.assertEqual(self.request("/linked/")[0], 404)

    def test_publication_hidden_file_and_junction_rejected(self):
        spec = importlib.util.spec_from_file_location("release", ROOT / "scripts/build-release.py")
        release = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(release)
        output = self.root / "output"
        hidden = self.root / "assets/downloads/.private"
        hidden.parent.mkdir(parents=True)
        hidden.write_text("private")
        with self.assertRaises(SystemExit):
            release.copy_runtime_assets(self.root, output, set())
        self.assertFalse((output / "assets/downloads/.private").exists())
        with self.assertRaises(SystemExit):
            release.copy_file(self.root, output, Path("../outside.txt"))
        link = self.root / "linked"
        if os.name == "nt":
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(self.root / "about")], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            link.symlink_to(self.root / "about", target_is_directory=True)
        try:
            with self.assertRaises(SystemExit):
                release.copy_file(self.root, output, Path("linked/index.html"))
            self.assertFalse((output / "linked/index.html").exists())
        finally:
            if os.name == "nt":
                link.rmdir()
            else:
                link.unlink()

    def test_windows_junction(self):
        if os.name != "nt":
            self.skipTest("Windows junction test")
        link = self.root / "linked"
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(self.root / "about")], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        try:
            self.assertEqual(self.request("/linked/")[0], 404)
        finally:
            link.rmdir()

    def test_missing_duplicate_and_truncated_lengths(self):
        for headers, body in ((b"", b""), (b"Content-Length: 2\r\nContent-Length: 2\r\n", b"{}"), (b"Content-Length: 10\r\n", b"{}")):
            with socket.create_connection(self.server.server_address, timeout=7) as connection:
                connection.sendall(b"POST /__csp-report HTTP/1.0\r\n" + headers + b"\r\n" + body)
                connection.shutdown(socket.SHUT_WR)
                self.assertIn(b" 400 ", connection.recv(4096).split(b"\r\n")[0])
        self.assertEqual(self.server.report_bytes, 0)

    def test_invalid_report_lengths_and_payloads(self):
        for length in ("-1", "0", "65537", "abc", "1, 1"):
            with self.subTest(length=length):
                self.assertIn(self.request("/__csp-report", "POST", b"", {"Content-Length": length})[0], (400, 413))
        self.assertEqual(self.request("/__csp-report", "POST", b"{}", {"Transfer-Encoding": "chunked"})[0], 400)
        for body in (b"[]", b"broken", b"\xff", b"[" * 2000):
            self.assertEqual(self.request("/__csp-report", "POST", body)[0], 400)
        self.assertEqual(self.request("/elsewhere", "POST", b"{}")[0], 404)
        self.assertEqual(self.server.report_bytes, 0)

    def test_report_storage_bound_under_concurrent_requests(self):
        body = json.dumps({"csp-report": {"document-uri": "/"}}).encode()
        self.assertEqual(self.request("/__csp-report", "POST", body)[0], 204)
        self.server.reports.seek(0)
        self.assertEqual(json.loads(self.server.reports.readline()), json.loads(body))
        self.server.reports.seek(0, 2)
        with patch.object(preview, "MAX_STORAGE_BYTES", self.server.report_bytes + 40):
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                statuses = list(pool.map(lambda _: self.request("/__csp-report", "POST", body)[0], range(12)))
            self.assertIn(507, statuses)
            self.assertLessEqual(self.server.report_bytes, preview.MAX_STORAGE_BYTES)
            self.assertEqual(self.server.reports.tell(), self.server.report_bytes)


if __name__ == "__main__":
    unittest.main()
