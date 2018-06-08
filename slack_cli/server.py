"""
Todo :
- handle access denial
- more elegant way to start server and signal between threads
"""

import os
import ssl
import time

from subprocess import call
from slack_cli.config import oauth_path, tls_path
from threading import Thread, Condition
from slack_cli.oauth import obtain_access_token, token_to_file
from http.server import HTTPServer, BaseHTTPRequestHandler


class HttpsServer(HTTPServer):

    def __init__(self, address, handler_cls, token_ready, tls_path):
        HTTPServer.__init__(self, address, handler_cls)
        self.token_ready = token_ready
        self.using_tls = False
        self.tls_path = tls_path

    def use_tls(self):
        if not os.path.isfile(self.tls_path):
            print("Creating self signed ssl certificate at {}".format(tls_path))
            command = "openssl req -new -x509 -keyout \"{}\" -out \"{}\" -days 365 -nodes -subj \"/C=CA/ST=Ontario/L=Toronto/O=Zero Gravity Labs/CN=localhost\" 2>/dev/null".format(self.tls_path, self.tls_path)
            call(command, shell=True)

        if not self.using_tls:
            self.secure_socket()
            self.using_tls = True

    def secure_socket(self):
        self.socket = ssl.wrap_socket(self.socket, certfile=self.tls_path, server_side=True)


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

            # acquire the underlying lock (this could be a critical section if
            # both threads try to access the resource concurrently)
            self.server.token_ready.acquire()

            # notify a waiting thread
            self.server.token_ready.notify()

            # release the underlying lock (allowing the thread to acquire the mutex)
            # in the event that in between this thread relasing the lock and the
            # waiting thread acquiring the lock, another thread acquires the lock
            # changes the shared resource, and then releases the lock
            # (spurious wakeup) the waiting thread will go back to sleep, since it's
            # coded to check the codition before proceeding
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


class HttpsThread(Thread):

    def __init__(self, server):
        Thread.__init__(self, daemon=True)
        self.server = server

    def run(self):
        self.server.use_tls()
        self.server.serve_forever()

def make_server(host, port):
    token_ready = Condition()
    server = HttpsServer((host, port), HttpsRequestHandler, token_ready, tls_path)
    return server, token_ready

def start_server(server):
    thread = HttpsThread(server)
    thread.start()

def shutdown_server(server):
    server.shutdown()
