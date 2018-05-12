#!/usr/bin/env python3

"""
Todo :
- authorize oauth after ensuring the command is valid
"""

import os
import sys

from threading import Condition
from oauth import token_from_file
from slack import get_user_conversations
from config import authorization_url, oauth_path
from server import start_server, shutdown_server, HttpsServer, HttpsRequestHandler


def process_command(oauth):
    command = sys.argv[1]

    if command == "oauth":
        print(oauth)
    elif command == "conv":
        data = get_user_conversations(oauth)
        print(data)
    else:
        print("Unknown: {}".format(command))


def usage_text():
    out = []
    
    out.append("usage: slk [--version] [--help]\n\t<command> [<args>]\n\n")
    out.append("These are common slack-cli commands:\n\n")
    out.append("update local slack database:\n\tpull\n\n")
    out.append("get slack channels:\n\tchan\n\n")
    out.append("get slack conversations:\n\tconv")

    return "".join(out)


if __name__ == "__main__":

    if len(sys.argv) <= 1:
        sys.exit(usage_text())

    authorized = os.path.exists(oauth_path)

    if not authorized:
        print("Please authorize slack-cli at {}".format(authorization_url))

        host, port = "127.0.0.1", 8443
        print("Server starting at {}:{}".format(host, port))

        token_ready = Condition()
        server = HttpsServer((host, port), HttpsRequestHandler, token_ready)
        start_server(server)

        token_ready.acquire()
        token_ready.wait()

    print("Loading oauth access token...")
    oauth = token_from_file(oauth_path)

    if not authorized:
        authorized = True

        print("Shutting down server...")
        shutdown_server(server)

    print("Processing command...")
    process_command(oauth)
