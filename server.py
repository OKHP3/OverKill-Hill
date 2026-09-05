#!/usr/bin/env python3
import http.server
import json
import os
import socketserver
from pathlib import Path

PORT = int(os.environ.get("PORT", "5000"))
HOST = os.environ.get("HOST", "0.0.0.0")

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/__csp-report":
            self.send_error(404)
            return
        try:
            length = min(int(self.headers.get("Content-Length", "0")), 64 * 1024)
            payload = json.loads(self.rfile.read(length)) if length else {}
            if not isinstance(payload, dict):
                raise ValueError("report must be an object")
        except (ValueError, json.JSONDecodeError):
            self.send_error(400, "invalid CSP report")
            return
        report_path = Path(os.environ.get("CSP_REPORT_FILE", "/tmp/overkill-hill-csp-reports.jsonl"))
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with report_path.open("a", encoding="utf-8") as reports:
            reports.write(json.dumps(payload, separators=(",", ":")) + "\n")
        self.send_response(204)
        self.end_headers()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

socketserver.TCPServer.allow_reuse_address = True

class ThreadingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    # Responsive QA opens eight browser pages in parallel, each requesting
    # several local assets. Keep the accept queue ahead of that burst so the
    # test server reports site behavior rather than transient refusals.
    request_queue_size = 128

with ThreadingServer((HOST, PORT), NoCacheHandler) as httpd:
    print(f"Serving {Path.cwd()} on http://{HOST}:{PORT} with no-cache headers")
    httpd.serve_forever()
