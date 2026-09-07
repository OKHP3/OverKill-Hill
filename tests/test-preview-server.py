#!/usr/bin/env python3
"""Local HTTP regressions for the preview exposure boundary."""
import http.client
import importlib.util
import json
from pathlib import Path
import socket
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('preview', ROOT / 'server.py')
preview = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preview)


class QuietHandler(preview.NoCacheHandler):
    def log_message(self, format, *args):
        pass


class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for name in ('index.html', 'about/index.html', 'assets/js/app.js', '.secret', 'server.py'):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(name)
        self.server = preview.ThreadingServer(('127.0.0.1', 0), QuietHandler,
            root=self.root, public_files={'index.html', 'about/index.html', 'assets/js/app.js',
                                        'escape.html', 'linked/index.html', '.secret'}, collect_reports=True)
        self.worker = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.worker.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.worker.join()
        self.temp.cleanup()

    def request(self, path, method='GET', body=None, headers=None):
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=3)
        connection.request(method, path, body, headers or {})
        response = connection.getresponse()
        result = response.status, dict(response.getheaders()), response.read()
        connection.close()
        return result

    def test_public_routes_assets_head_and_redirect(self):
        for route in ('/', '/about/', '/assets/js/app.js?v=1'):
            self.assertEqual(self.request(route)[0], 200)
        self.assertEqual(self.request('/', 'HEAD')[2], b'')
        response = self.request('/about?q=1')
        self.assertEqual(response[0], 301)
        self.assertEqual(response[1]['Location'], '/about/?q=1')

    def test_source_dotfiles_traversal_and_listings_are_denied(self):
        for route in ('/server.py', '/site-src/pages/index.main.html', '/.git/config',
                      '/.secret', '/%2esecret', '/../index.html', '/%2e%2e/index.html',
                      '/assets/', '/assets/js/', '//server.py'):
            with self.subTest(route=route):
                self.assertEqual(self.request(route)[0], 404)

    def test_symlink_files_and_parents_are_denied(self):
        (self.root / 'escape.html').symlink_to(self.root / 'server.py')
        (self.root / 'linked').symlink_to(self.root / 'about', target_is_directory=True)
        for route in ('/escape.html', '/linked/'):
            self.assertEqual(self.request(route)[0], 404)
        original = self.root / 'assets/js/app.js'
        original.unlink()
        original.symlink_to(self.root / 'server.py')
        self.assertEqual(self.request('/assets/js/app.js')[0], 404)

    def test_report_bounds_and_schema(self):
        for length in ('-1', 'invalid', '0', str(preview.MAX_REPORT_BYTES + 1)):
            status = self.request('/__csp-report', 'POST', b'',
                {'Content-Length': length, 'Content-Type': 'application/csp-report'})[0]
            self.assertIn(status, (400, 413))
        self.assertEqual(self.request('/__csp-report', 'POST', b'[]',
            {'Content-Type': 'application/csp-report'})[0], 400)
        self.assertEqual(self.request('/__csp-report', 'POST', b'{}')[0], 415)
        self.assertEqual(self.request('/other', 'POST', b'{}')[0], 404)

    def test_report_storage_cap_and_disabled_collection(self):
        body = json.dumps({'csp-report': {'blocked-uri': 'x' * 200}}).encode()
        headers = {'Content-Type': 'application/csp-report'}
        self.server.report_limit = 500
        self.assertEqual(self.request('/__csp-report', 'POST', body, headers)[0], 204)
        self.assertEqual(self.request('/__csp-report', 'POST', body, headers)[0], 204)
        self.assertEqual(self.request('/__csp-report', 'POST', body, headers)[0], 507)
        self.assertLessEqual(self.server.reports.tell(), 500)
        self.server.collect_reports = False
        self.assertEqual(self.request('/__csp-report', 'POST', body, headers)[0], 404)

    def test_slow_report_times_out(self):
        self.server.request_timeout = 0.1
        with socket.create_connection(self.server.server_address, timeout=3) as client:
            client.sendall(b'POST /__csp-report HTTP/1.0\r\nContent-Type: application/json\r\n'
                           b'Content-Length: 20\r\n\r\n{')
            self.assertIn(b'408', client.recv(1024).split(b'\r\n')[0])

    def test_concurrent_reports_cannot_exceed_storage_cap(self):
        from concurrent.futures import ThreadPoolExecutor
        self.server.report_limit = 10
        def post(_):
            return self.request('/__csp-report', 'POST', b'{}',
                                {'Content-Type': 'application/json'})[0]
        with ThreadPoolExecutor(max_workers=8) as pool:
            statuses = list(pool.map(post, range(16)))
        self.assertEqual(statuses.count(204), 3)
        self.assertEqual(statuses.count(507), 13)
        self.assertEqual(self.server.reports.tell(), 9)

    def test_repository_allowlist_serves_every_selected_file(self):
        inventory = preview.public_inventory(ROOT)
        self.assertIn('index.html', inventory)
        self.assertIn('fr/index.html', inventory)
        for forbidden in ('server.py', 'AGENTS.md', '.replit', '.git/config',
                          'site-src/pages/index.main.html', 'assets/docs/remediation-a18-2026-09-07.md'):
            self.assertNotIn(forbidden, inventory)
        original_fd = self.server.root_fd
        try:
            self.server.root_fd = preview.os.open(ROOT, preview.os.O_RDONLY | preview.os.O_DIRECTORY)
            self.server.public_files = inventory
            for relative in sorted(inventory):
                with self.subTest(path=relative):
                    self.assertEqual(self.request('/' + relative, 'HEAD')[0], 200)
        finally:
            preview.os.close(self.server.root_fd)
            self.server.root_fd = original_fd

    def test_replit_has_explicit_preview_bind_and_no_root_publication(self):
        import tomllib
        config = tomllib.loads((ROOT / '.replit').read_text())
        self.assertNotIn('deployment', config)
        workflow = next(item for item in config['workflows']['workflow']
                        if item['name'] == 'Start application')
        self.assertEqual(workflow['tasks'][0]['args'], 'HOST=0.0.0.0 python3 server.py')

    def test_ambiguous_framing_and_short_body(self):
        for headers, body, expected in (
            ('Content-Length: 2\r\nContent-Length: 2', b'{}', 400),
            ('Content-Length: 2\r\nTransfer-Encoding: chunked', b'{}', 400),
            ('Content-Length: 20', b'{}', 400),
        ):
            with socket.create_connection(self.server.server_address, timeout=3) as client:
                client.sendall(('POST /__csp-report HTTP/1.0\r\nContent-Type: application/json\r\n'
                                + headers + '\r\n\r\n').encode() + body)
                client.shutdown(socket.SHUT_WR)
                self.assertIn(str(expected).encode(), client.recv(1024).split(b'\r\n')[0])


if __name__ == '__main__':
    unittest.main()
