
from http.server import BaseHTTPRequestHandler, HTTPServer

class HelloHandler(BaseHTTPRequestHandler):
    def _send_response(self, message):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(message.encode())

    def do_GET(self):
        if self.path == "/":
            message = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Alon-bot</title>
            </head>
            <body>
                <h1>Hello, I'm Alon-bot</h1>
            </body>
            </html>
            """
            self._send_response(message)
        else:
            self.send_error(404, "Not Found")

if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, HelloHandler)
    print("Alon-bot server is running on port 8080")
    httpd.serve_forever()
