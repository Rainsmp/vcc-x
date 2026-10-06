from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict


class ApiHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        routes = {
            "/api/v1/health": {"status": "ok", "uptime": "healthy"},
            "/api/v1/servers": {"servers": [{"hostname": "node-01", "status": "online"}]},
            "/api/v1/jobs": {"jobs": [{"id": "JOB-1001", "status": "completed"}]},
            "/api/v1/backups": {"backups": [{"name": "nightly", "status": "successful"}]},
            "/api/v1/incidents": {"incidents": []},
            "/api/v1/audit": {"audit": [{"event": "server.online", "request_id": "REQ-TEST"}]},
            "/api/v1/cloudflare": {"cloudflare": {"status": "not_configured"}},
            "/api/v1/pterodactyl": {"pterodactyl": {"status": "not_configured"}},
        }
        payload = routes.get(self.path)
        if payload is None:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "not_found"}).encode("utf-8"))
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload, sort_keys=True).encode("utf-8"))

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return


def start_api_server(host: str = "127.0.0.1", port: int = 8080) -> None:
    server = ThreadingHTTPServer((host, port), ApiHandler)
    print(f"Starting VCC-X API on http://{host}:{port}")
    server.serve_forever()
