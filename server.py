#!/usr/bin/env python3
"""Local, allowlisted static preview with bounded temporary CSP reports."""
import http.server
import importlib.util
import json
import os
import re
import socket
import socketserver
import tempfile
import threading
from pathlib import Path
from urllib.parse import unquote, urlsplit

PORT = int(os.environ.get("PORT", "5000"))
HOST = os.environ.get("HOST", "127.0.0.1")
ROOT = Path(__file__).resolve().parent
MAX_REPORT_BYTES = 64 * 1024
MAX_STORAGE_BYTES = 1024 * 1024


def public_files(root):
    """Reuse the release contract without copying or regenerating the checkout."""
    spec = importlib.util.spec_from_file_location("preview_release", ROOT / "scripts/build-release.py")
    release = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(release)
    paths = set(release.load_public_pages(root))
    paths.update(Path(value) for value in release.ROOT_FILES)
    archived = release.load_archived_library_paths(root)
    for directory, extensions in release.RUNTIME_ASSET_RULES:
        for path in (root / directory).rglob("*"):
            if path.is_file() and (extensions is None or path.suffix.lower() in extensions):
                paths.add(path.relative_to(root))
    return {p.as_posix() for p in paths - archived}


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server, **kwargs):
        super().__init__(request, client_address, server, directory=str(server.root), **kwargs)

    def setup(self):
        super().setup()
        self.connection.settimeout(5)

    def send_head(self):
        try:
            route = unquote(urlsplit(self.path).path, errors="strict")
            parts = route.lstrip("/").split("/")
            if any(p in (".", "..") or "\\" in p or ":" in p or "\x00" in p
                   or (p.startswith(".") and not (i == 0 and p == ".well-known"))
                   for i, p in enumerate(parts)):
                raise ValueError("unsafe path")
            relative = Path(*parts)
            candidate = self.server.root / relative
            if candidate.is_dir():
                relative /= "index.html"
                candidate /= "index.html"
            if relative.as_posix() not in self.server.allowed:
                raise ValueError("not public")
            # Reject links to internal files too, including directory junctions.
            current = self.server.root
            for part in relative.parts:
                current /= part
                if current.is_symlink() or (hasattr(current, "is_junction") and current.is_junction()):
                    raise ValueError("linked path")
            if candidate.resolve() != candidate or not candidate.is_file():
                raise ValueError("noncanonical path")
        except (ValueError, OSError, RuntimeError):
            self.send_error(404)
            return None
        return super().send_head()

    def list_directory(self, path):
        self.send_error(404)
        return None

    def do_POST(self):
        self.close_connection = True
        if self.path != "/__csp-report":
            self.send_error(404)
            return
        lengths = self.headers.get_all("Content-Length", [])
        if self.headers.get("Transfer-Encoding") or len(lengths) != 1 or not re.fullmatch(r"[0-9]{1,10}", lengths[0]):
            self.send_error(400, "invalid report length")
            return
        length = int(lengths[0])
        if not 0 < length <= MAX_REPORT_BYTES:
            self.send_error(413, "report size outside limits")
            return
        try:
            raw = self.rfile.read(length)
            if len(raw) != length:
                raise ValueError("truncated report")
            payload = json.loads(raw)
            if not isinstance(payload, dict):
                raise ValueError("report must be an object")
            encoded = (json.dumps(payload, separators=(",", ":")) + "\n").encode("utf-8")
            if len(encoded) > MAX_REPORT_BYTES:
                raise ValueError("encoded report exceeds limit")
        except (ValueError, RecursionError, socket.timeout):
            self.send_error(400, "invalid CSP report")
            return
        with self.server.report_lock:
            if self.server.report_bytes + len(encoded) > MAX_STORAGE_BYTES:
                self.send_error(507, "temporary report storage is full")
                return
            self.server.reports.write(encoded)
            self.server.reports.flush()
            self.server.report_bytes += len(encoded)
        self.send_response(204)
        self.end_headers()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


class ThreadingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True
    request_queue_size = 128

    def __init__(self, address, handler=NoCacheHandler, root=ROOT):
        self.root = Path(root).resolve()
        self.allowed = public_files(self.root)
        self.report_lock = threading.Lock()
        self.report_bytes = 0
        self.reports = tempfile.TemporaryFile(mode="w+b")
        try:
            super().__init__(address, handler)
        except BaseException:
            self.reports.close()
            raise

    def server_close(self):
        super().server_close()
        self.reports.close()


if __name__ == "__main__":
    with ThreadingServer((HOST, PORT)) as httpd:
        print(f"Serving allowlisted preview from {ROOT} on {HOST}:{PORT}; temporary reports capped at 1 MiB", flush=True)
        httpd.serve_forever()
