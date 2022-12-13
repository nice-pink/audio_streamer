from http_receiver.http_server import HttpServer
from http.server import HTTPServer
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please define host_ip and port as argument.')
        sys.exit(1)
    host_ip: str = sys.argv[1]
    port: int = int(sys.argv[2])
    httpd = HTTPServer((host_ip, port), HttpServer)
    httpd.serve_forever()
