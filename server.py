"""
Todo :
- handle access denial
- more elegant way to start server and signal between threads
"""

import os
import ssl
import time

from config import oauth_path
from subprocess import call
from threading import Thread
from oauth import obtain_access_token, token_to_file
from http.server import HTTPServer, BaseHTTPRequestHandler


class HttpsServer(HTTPServer):

    def __init__(self, address, handler_cls, token_ready):
        HTTPServer.__init__(self, address, handler_cls)
        self.token_ready = token_ready
        self.using_tls = False

    def use_tls(self, tls_path):
        if not os.path.isfile(tls_path):
            command = "openssl req -new -x509 -keyout {} -out {} -days 365 -nodes -subj \"/C=CA/ST=Ontario/L=Toronto/O=Zero Gravity Labs/CN=localhost\" 2>/dev/null".format(tls_path, tls_path)
            call(command, shell=True)

        if not self.using_tls:
            self.secure_socket(tls_path)
            self.using_tls = True

    def secure_socket(self, tls_path):
        self.socket = ssl.wrap_socket(self.socket, certfile=tls_path, server_side=True)


class HttpsRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        params = self.query_params(self.path)

        if "code" in params:
            status = 200
            headers = {"Content-Type": "text/plain"}
            body = "Obtained authorization code."

            oauth = obtain_access_token(params)
            if oauth is not None:
                token_to_file(oauth_path, oauth)

            self.server.token_ready.acquire()
            self.server.token_ready.notify()
            self.server.token_ready.release()
        else:
            status = 400
            headers = {"Content-Type": "text/plain"}
            body = "Could not obtain authorization code."

        self.do_response(status, headers, body)

    def do_response(self, status, headers, body):
        self.send_response(status)
        self.send_headers(headers)
        self.wfile.write(bytes(body, "ascii"))

    def send_headers(self, headers):
        for k in headers:
            self.send_header(k, headers[k])
        self.end_headers()

    def query_params(self, path_query):
        if "?" not in path_query:
            return dict()

        query = path_query.split("?")[-1]

        if query.startswith("&"):
            query = query_string[1:]

        if query.endswith("&"):
            query = query[:-1]

        params = dict()
        for pair in query.split("&"):
            if "=" in pair:
                kv = pair.split("=")
                params[kv[0]] = kv[1]

        return params


class HttpRequest(object):

    def __init__(self, verb, path, params, headers, body):
        self.verb = verb
        self.path = path
        self.params = params
        self.headers = headers
        self.body = body

    def __str__(self):
        return "<HttpRequest object verb:{}, path:{}, params:{}, headers:{}, body:{}".format(verb, path, params, headers, body)

    def __repr__(self):
        return self.__str__()


class HttpResponse(object):

    def __init__(self, status, headers, body):
        self.status = status
        self.headers = headers
        self.body = body

    def __str__(self):
        return "<HttpResponse object status:{}, headers:{}, body:{}".format(status, headers, body)

    def __repr__(self):
        return self.__str__()


class HttpsThread(Thread):

    def __init__(self, server):
        Thread.__init__(self, daemon=True)
        self.server = server

    def run(self):
        self.server.use_tls("server.pem")
        self.server.serve_forever()


def start_server(server):
    thread = HttpsThread(server)
    thread.start()

def shutdown_server(server):
    server.shutdown()
