import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from bridge.core import build_report

class BridgeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))
            return
            
        if self.path == "/report":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            report = build_report()
            self.wfile.write(json.dumps(report, indent=2).encode("utf-8"))
            return
            
        self.send_response(404)
        self.end_headers()

def serve(port=8780):
    server = HTTPServer(("127.0.0.1", port), BridgeHandler)
    print(f"Bridge command nexus active at http://127.0.0.1:{port}")
    server.serve_forever()