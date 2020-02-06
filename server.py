from io import BytesIO
from urllib import parse
import logging

from http.server import HTTPServer, BaseHTTPRequestHandler

all_users = [
    {
        "username": "user1", "password" : "pass1"
    },
    {
        "username": "user2", "password" : "pass2"
    }
]

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info(f" POST {self.path} Data: {post_data.decode('utf-8')}")
        data = parse.parse_qs(post_data.decode('utf-8'))
        self.send_response(200)
        self.end_headers()
        user_found = [ user for user in all_users if user['username'] == data['username'][0] and user['password'] == data['password'][0] ]
        if user_found:
            response = BytesIO()
            response.write(b"True")
            self.wfile.write(response.getvalue())
            logging.info(f" User({data['username'][0]}) is valid.")
        else:
            response = BytesIO()
            response.write(b"False")
            self.wfile.write(response.getvalue())
            logging.info(f" Invalid Credentials.  Username: {data['username'][0]} Password: {data['password'][0]}")

if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    logging.basicConfig(level=logging.INFO)
    logging.info(f'Starting Server at {host}:{port}')

    httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
    httpd.serve_forever()