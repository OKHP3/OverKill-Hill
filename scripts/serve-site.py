#!/usr/bin/env python3
"""Dev server with no-cache headers so browsers always fetch fresh assets."""
import http.server, socketserver, os, sys

PORT = int(os.environ.get("PORT", 5000))

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass  # silence per-request noise; errors still show via exception

socketserver.TCPServer.allow_reuse_address = True
with http.server.ThreadingHTTPServer(("0.0.0.0", PORT), NoCacheHandler) as httpd:
    print(f"Serving on http://0.0.0.0:{PORT}", flush=True)
    httpd.serve_forever()
