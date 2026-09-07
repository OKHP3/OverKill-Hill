#!/usr/bin/env python3
"""Local allowlisted preview. Replit must explicitly opt into a network bind."""
import argparse
import http.server
import importlib.util
import json
import mimetypes
import os
from pathlib import Path
import re
import shutil
import socketserver
import stat
import tempfile
import threading
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parent
HOST = os.environ.get('HOST', '127.0.0.1')
PORT = int(os.environ.get('PORT', '5000'))
MAX_REPORT_BYTES = 64 * 1024
MAX_REPORT_STORAGE = 1024 * 1024


def safe_parts(relative):
    parts = relative.split('/')
    return bool(parts) and all(part and part not in ('.', '..') and '\\' not in part
        and '\x00' not in part and (not part.startswith('.') or
        (i == 0 and part == '.well-known')) for i, part in enumerate(parts))


def public_inventory(root):
    """Reuse the release builder's routes, asset rules and artwork exclusions."""
    spec = importlib.util.spec_from_file_location('release', ROOT / 'scripts/build-release.py')
    release = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(release)
    paths = set(release.load_public_pages(root))
    paths.update(Path(path) for path in release.ROOT_FILES)
    archived = release.load_archived_library_paths(root)
    for directory, extensions in release.RUNTIME_ASSET_RULES:
        paths.update(path.relative_to(root) for path in (root / directory).rglob('*')
                     if path.is_file() and (extensions is None or path.suffix.lower() in extensions))
    return {path.as_posix() for path in paths - archived if safe_parts(path.as_posix())}


class NoCacheHandler(http.server.BaseHTTPRequestHandler):
    def setup(self):
        self.request.settimeout(self.server.request_timeout)
        super().setup()

    def open_public(self, relative):
        if relative not in self.server.public_files or not safe_parts(relative):
            raise FileNotFoundError(relative)
        # Open each component relative to an already-open directory. O_NOFOLLOW
        # prevents both ordinary symlinks and replacement between check and open.
        directory = os.dup(self.server.root_fd)
        try:
            parts = relative.split('/')
            for component in parts[:-1]:
                child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                dir_fd=directory)
                os.close(directory)
                directory = child
            fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                os.close(fd)
                raise FileNotFoundError(relative)
            return os.fdopen(fd, 'rb')
        finally:
            os.close(directory)

    def serve_file(self, head=False):
        try:
            parsed = urlsplit(self.path)
            path = unquote(parsed.path, errors='strict')
            if parsed.scheme or parsed.netloc or not path.startswith('/'):
                raise ValueError('invalid path')
            relative = path[1:]
            if not relative or relative.endswith('/'):
                relative += 'index.html'
            redirect = False
            if relative not in self.server.public_files and not path.endswith('/'):
                relative += '/index.html'
                redirect = True
            with self.open_public(relative) as content:
                if redirect:
                    self.send_response(301)
                    self.send_header('Location', quote(path, safe='/') + '/' +
                                     ('?' + parsed.query if parsed.query else ''))
                    self.send_header('Content-Length', '0')
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header('Content-Type', mimetypes.guess_type(relative)[0] or 'application/octet-stream')
                self.send_header('Content-Length', str(os.fstat(content.fileno()).st_size))
                self.end_headers()
                if not head:
                    shutil.copyfileobj(content, self.wfile)
        except (OSError, ValueError):
            self.send_error(404)

    def do_GET(self):
        self.serve_file()

    def do_HEAD(self):
        self.serve_file(head=True)

    def do_POST(self):
        if self.path != '/__csp-report' or not self.server.collect_reports:
            self.send_error(404)
            return
        lengths = self.headers.get_all('Content-Length', [])
        if (self.headers.get_all('Transfer-Encoding') or len(lengths) != 1
                or not re.fullmatch(r'[0-9]{1,10}', lengths[0])):
            self.send_error(400, 'invalid report length')
            return
        length = int(lengths[0])
        if not 0 < length <= MAX_REPORT_BYTES:
            self.send_error(413 if length > MAX_REPORT_BYTES else 400)
            return
        if self.headers.get_content_type() not in ('application/json', 'application/csp-report'):
            self.send_error(415)
            return
        try:
            body = self.rfile.read(length)
            if len(body) != length:
                raise ValueError('incomplete report')
            payload = json.loads(body)
            if not isinstance(payload, dict):
                raise ValueError('report must be an object')
            data = (json.dumps(payload, separators=(',', ':')) + '\n').encode()
        except (ValueError, UnicodeError, RecursionError):
            self.send_error(400, 'invalid CSP report')
            return
        except TimeoutError:
            self.send_error(408)
            return
        with self.server.report_lock:
            if self.server.reports.tell() + len(data) > self.server.report_limit:
                self.send_error(507, 'preview report storage full')
                return
            self.server.reports.write(data)
            self.server.reports.flush()
        self.send_response(204)
        self.end_headers()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()


class ThreadingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True
    request_queue_size = 128
    request_timeout = 5

    def __init__(self, address, handler, *, root, public_files, collect_reports=False):
        self.public_files = frozenset(public_files)
        self.root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        self.collect_reports = collect_reports
        self.reports = tempfile.TemporaryFile(mode='w+b')
        self.report_limit = MAX_REPORT_STORAGE
        self.report_lock = threading.Lock()
        self.slots = threading.BoundedSemaphore(32)
        super().__init__(address, handler)

    def process_request(self, request, client_address):
        if not self.slots.acquire(blocking=False):
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except Exception:
            self.slots.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self.slots.release()

    def server_close(self):
        super().server_close()
        self.reports.close()
        os.close(self.root_fd)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--collect-csp-reports', action='store_true',
                        help='accept up to 1 MiB in private temporary session storage')
    args = parser.parse_args()
    if not HOST:
        parser.error('HOST must explicitly name an intended bind address')
    with ThreadingServer((HOST, PORT), NoCacheHandler, root=ROOT,
                         public_files=public_inventory(ROOT),
                         collect_reports=args.collect_csp_reports) as httpd:
        print(f'Serving allowlisted preview on {HOST}:{PORT}; restart after adding files', flush=True)
        httpd.serve_forever()


if __name__ == '__main__':
    main()
