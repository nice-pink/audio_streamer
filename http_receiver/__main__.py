from http_receiver.http_server import HttpServer
from http.server import HTTPServer

if __name__ == '__main__':
    httpd = HTTPServer(('127.0.0.1', 8000), HttpServer)
    httpd.serve_forever()
