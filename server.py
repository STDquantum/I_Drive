import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import mimetypes

class CustomRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('.js'):
            self.send_response(200)
            self.send_header("Content-type", "application/javascript")
            self.end_headers()
            with open(os.getcwd() + self.path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            super().do_GET()

    def end_headers(self):
        self.send_my_headers()
        super().end_headers()

    def send_my_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")

def run(server_class=HTTPServer, handler_class=CustomRequestHandler, port=410):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting HTTP server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()