from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import json, cgi


class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        data = json.dumps({'hello': 'world', 'received': 'ok'})
        self.wfile.write(bytes(str(data).encode()))

    # POST echoes the message adding a JSON field
    def do_POST(self):
        # ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        content_len = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_len).decode('utf-8')
        print(post_body.strip().split())
        iter = int()
        for id, i in enumerate(post_body.split()):
            if 'name' in i:
                iter = id
            if id == iter + 1:
                print(i)
        # # refuse to receive non-json content
        #
        # # read the message and convert it into a python dictionary
        # length = int(self.headers.getheader('content-length'))
        # message = json.loads(self.rfile.read(length))
        # print(message)
        # add a property to the object, just to mess with data

        # # send the message back
        # self._set_headers()
        # self.wfile.write(json.dumps(message))


def run(server_class=HTTPServer, handler_class=Server, port=8080):
    host_name = socket.gethostbyname(socket.gethostname())
    server_address = (host_name, port)
    print(server_address)
    httpd = server_class(server_address, handler_class)

    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
