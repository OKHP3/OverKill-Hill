"""Dedicated A14 HTTP boundary regressions; no production server changes."""
import http.client
import importlib.util
import tempfile
import threading
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from http.server import ThreadingHTTPServer
from pathlib import Path

spec = importlib.util.spec_from_file_location('proposal_server', Path(__file__).resolve().parents[1] / 'scripts/serve-phone-proposals.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        (self.root / 'proposals/a').mkdir(parents=True)
        (self.root / 'proposals/a/index.html').write_text('proposal')
        (self.root / 'private.txt').write_text('private')
        self.allowed = {'proposals/a/index.html', 'linked.txt'}
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), module.make_handler(self.root, self.allowed))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.directory.cleanup()

    def request(self, path, method='GET', headers=None):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port)
        connection.request(method, path, headers=headers or {})
        response = connection.getresponse()
        result = response.status, response.read(), dict(response.getheaders())
        connection.close()
        return result

    def test_exact_page_and_query(self):
        status, data, headers = self.request('/proposals/a/?review=1')
        self.assertEqual((status, data), (200, b'proposal'))
        self.assertEqual(headers['X-Robots-Tag'], 'noindex, nofollow')

    def test_no_directory_listing_or_unlisted_files(self):
        for path in ('/proposals/', '/private.txt', '/scripts/serve-phone-proposals.py'):
            self.assertEqual(self.request(path)[0], 404)

    def test_private_and_traversal_paths(self):
        for path in ('/.local/a14/a/', '/.git/config', '/proposals/a/../../private.txt', '/%2e%2e/private.txt', '/%252e%252e/private.txt', '/proposals%5ca/index.html'):
            self.assertEqual(self.request(path)[0], 404)

    def test_untrusted_host(self):
        self.assertEqual(self.request('/proposals/a/', headers={'Host': 'example.org'})[0], 403)

    def test_no_post(self):
        self.assertEqual(self.request('/__csp-report', method='POST')[0], 501)

    def test_head(self):
        self.assertEqual(self.request('/proposals/a/', method='HEAD')[:2], (200, b''))

    def test_symlink_even_when_allowlisted(self):
        try:
            (self.root / 'linked.txt').symlink_to(self.root / 'private.txt')
        except OSError as exc:
            self.skipTest(f'Symlink creation unavailable: {exc}')
        self.assertEqual(self.request('/linked.txt')[0], 404)

    def test_link_guard_without_symlink_privileges(self):
        (self.root / 'linked.txt').write_text('hidden')
        with patch.object(Path, 'is_symlink', autospec=True, side_effect=lambda path: path.name == 'linked.txt'):
            self.assertIsNone(module.safe_file(self.root, 'linked.txt'))

    def test_windows_reparse_guard(self):
        (self.root / 'linked.txt').write_text('hidden')
        original = Path.lstat
        def stat(path):
            result = original(path)
            if path.name == 'linked.txt':
                return SimpleNamespace(st_mode=result.st_mode, st_file_attributes=0x400)
            return result
        with patch.object(Path, 'lstat', stat):
            self.assertIsNone(module.safe_file(self.root, 'linked.txt'))


if __name__ == '__main__':
    unittest.main()
