from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import time
from urllib.parse import urlparse, parse_qs

class Handler(BaseHTTPRequestHandler):
    def _send_json(self, obj, status=200):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = urlparse(self.path)
        qs = parse_qs(url.query)

        if url.path == "/health":
            self._send_json({"ok": True, "time": time.time()})
            return

        if url.path == "/work":
            # Simulate controllable CPU work (small by default)
            ms = int(qs.get("ms", ["50"])[0])  # target work time in milliseconds
            ms = max(0, min(ms, 5000))         # clamp 0..5000ms
            end = time.perf_counter() + (ms / 1000.0)
            x = 0
            while time.perf_counter() < end:
                x = (x * 1103515245 + 12345) & 0x7fffffff  # tiny CPU loop
            self._send_json({"worked_ms": ms, "result": x})
            return

        if url.path == "/":
            self.send_response(200)
            body = (
                "OK. Try:\n"
                "  /health\n"
                "  /work?ms=50   (or ms=200, 500, 1000)\n"
            ).encode("utf-8")
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self._send_json({"error": "not found", "path": url.path}, status=404)

    def log_message(self, fmt, *args):
        # Reduce console spam
        return

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Serving on http://{host}:{port}")
    print("Endpoints: / , /health , /work?ms=50")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("Server stopped.")
