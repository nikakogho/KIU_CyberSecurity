from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"""
        <html>
            <head><title>Port 80 Test</title></head>
            <body>
                <h1>Hello from Python on port 80!</h1>
                <p>If you see this, port 80 is open.</p>
            </body>
        </html>
        """)

server_address = ("0.0.0.0", 80)
httpd = HTTPServer(server_address, SimpleHandler)

print("Serving HTTP on port 80...")
httpd.serve_forever()
