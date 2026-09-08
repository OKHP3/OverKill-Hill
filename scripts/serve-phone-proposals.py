#!/usr/bin/env python3
"""Serve a dedicated A14 artifact tree on loopback; never serve the checkout."""
import argparse
import json
import mimetypes
import shutil
import subprocess
import sys
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PROPOSALS = ('index.html', 'projects/index.html', 'projects/skillz/index.html', 'contact/index.html')


def safe_file(root, relative):
    """Reject links and Windows reparse points at every path component."""
    try:
        root_stat = root.lstat()
    except OSError:
        return None
    if root.is_symlink() or getattr(root_stat, 'st_file_attributes', 0) & 0x400:
        return None
    path = root
    for component in Path(relative).parts:
        path = path / component
        try:
            stat = path.lstat()
        except OSError:
            return None
        if path.is_symlink() or getattr(stat, 'st_file_attributes', 0) & 0x400:
            return None
    if not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
        return None
    return path


def prepare_tree():
    previews = ROOT / '.local/a14'
    required = [f'{variant}/{route}' for variant in ('a', 'b') for route in PROPOSALS] + ['proposal.css']
    if any(safe_file(previews, name) is None for name in required):
        raise ValueError('Build the phone proposals before starting this server')
    staging = Path(tempfile.mkdtemp(prefix='preview-', dir=previews)) / 'site'
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    subprocess.run([sys.executable, str(ROOT / 'scripts/build-release.py'), '--output', str(staging), '--commit', commit], cwd=ROOT, check=True)
    manifest = json.loads((staging / 'assets/audit/release-manifest.json').read_text(encoding='utf-8'))
    allowed = set(manifest['files'])
    for name in required:
        destination = staging / 'proposals' / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(safe_file(previews, name), destination)
        allowed.add('proposals/' + name)
    # This inventory sits outside the HTTP root and is not served.
    (staging.parent / 'allowlist.json').write_text(json.dumps(sorted(allowed), indent=2), encoding='utf-8')
    return staging, frozenset(allowed)


def make_handler(root, allowed):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.respond()

        def do_HEAD(self):
            self.respond(head=True)

        def respond(self, head=False):
            if self.headers.get('Host') not in (f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'):
                self.send_error(403)
                return
            try:
                path = unquote(urlsplit(self.path).path, errors='strict')
            except (ValueError, UnicodeError):
                self.send_error(404)
                return
            parts = path.split('/')
            if not path.startswith('/') or path.startswith('//') or any(p.startswith('.') for p in parts) or '\\' in path or ':' in path or '%' in path:
                self.send_error(404)
                return
            relative = path.lstrip('/') + ('index.html' if path.endswith('/') else '')
            target = safe_file(root, relative) if relative in allowed else None
            if target is None:
                self.send_error(404)
                return
            data = target.read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', mimetypes.guess_type(target.name)[0] or 'application/octet-stream')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('X-Robots-Tag', 'noindex, nofollow')
            self.end_headers()
            if not head:
                self.wfile.write(data)

        def log_message(self, *_):
            pass

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=5145)
    args = parser.parse_args()
    root, allowed = prepare_tree()
    with ThreadingHTTPServer(('127.0.0.1', args.port), make_handler(root, allowed)) as server:
        print(f'A14 only: http://127.0.0.1:{server.server_port}/proposals/a/ and /proposals/b/', flush=True)
        print(f'Explicit preview tree: {root}', flush=True)
        server.serve_forever()


if __name__ == '__main__':
    main()
