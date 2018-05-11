#!/usr/bin/env python3

import os
import ssl

from subprocess import call
from threading import Thread
from oauth import obtain_access_token
from http.server import HTTPServer, BaseHTTPRequestHandler


class HttpsServer(HTTPServer):

    def use_tls(self, tls_path):
        if not os.path.isfile(tls_path):
            command = "openssl req -new -x509 -keyout {} -out {} -days 365 -nodes -subj \"/C=CA/ST=Ontario/L=Toronto/O=Zero Gravity Labs/CN=localhost\" 2>/dev/null".format(tls_path, tls_path)
            call(command, shell=True)
        self.secure_socket(tls_path)

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
            print(oauth)
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
        Thread.__init__(self, daemon=False)
        self.server = server

    def run(self):
        self.server.use_tls("server.pem")
        self.server.serve_forever()


def start_server(host, port):
    server = HttpsServer((host, port), HttpsRequestHandler)
    thread = HttpsThread(server)
    thread.start()
    return server


if __name__ == "__main__":

    authorization_url = "https://slack.com/oauth/authorize?client_id=361449430741.360777286161&scope=channels%3Aread%2Cchannels%3Awrite&redirect_uri=https%3A%2F%2Flocalhost%3A8443%2Fslack-cli%2Fauthorize"
    print("Please authorize slack-cli at: {}".format(authorization_url))

    host, port = "127.0.0.1", 8443
    print("Server starting on {}:{}".format(host, port))

    server = start_server(host, port)
    # server.shutdown()
