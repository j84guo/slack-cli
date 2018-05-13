#!/usr/bin/env python3

"""
Todo :
- authorize oauth after ensuring the command is valid
- format output
- sort output by newest/unseen
- provide an "index" integer to output objects
- provide option for history length
- handle rate limit
- interactive mode, with 2 way communication
- python wheel structure
"""

import os
import sys

from threading import Condition
from oauth import token_from_file
from slack import list_channels, list_instant_messages, channels_history, instant_messages_history, post_message
from config import authorization_url, oauth_path, tls_path
from server import start_server, shutdown_server, HttpsServer, HttpsRequestHandler


def process_command(oauth):
    command = sys.argv[1]

    if command == "oauth":
        print(oauth)
    elif command == "ch":
        data = list_channels(oauth)
        print(data)
    elif command == "im":
        data = list_instant_messages(oauth)
        print(data)
    elif command == "ch_h":
        if len(sys.argv) <= 2:
            sys.exit(usage_text())
        data = channels_history(oauth, sys.argv[2])
        print(data)
    elif command == "im_h":
        if len(sys.argv) <= 2:
            sys.exit(usage_text())
        data = instant_messages_history(oauth, sys.argv[2])
        print(data)
    elif command == "im_p" or command == "ch_p":
        if len(sys.argv) <= 3:
            sys.exit(usage_text())
        data = post_message(oauth, sys.argv[2], sys.argv[3])
        print(data)
    else:
        print(usage_text())


def usage_text():
    out = []

    out.append("usage: slk [--version] [--help]\n\t<command> [<args>]\n\n")
    out.append("These are common slack-cli commands:\n\n")
    out.append("update local slack database:\n\tpull\n\n")
    out.append("list channels:\n\tch\n\n")
    out.append("list instant messages:\n\tim\n\n")
    out.append("instant messages history:\n\tim_h <id>\n\n")
    out.append("channels history:\n\tch_h <id>")

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
        server = HttpsServer((host, port), HttpsRequestHandler, token_ready, tls_path)
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
