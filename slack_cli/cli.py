#!/usr/bin/env python3

"""
Todo :
- format output
- sort output by newest/unseen
- provide an "index" integer to output objects
- provide option for history length
- handle rate limit
- interactive/streaming mode, with two way communication
- python wheel structure
"""

import os
import sys

from slack_cli.slack_service import SlackService
from slack_cli.slack_viewer import SlackViewer
from slack_cli.oauth import token_from_file
from slack_cli.config import oauth_path, authorization_url, slack_cli_path
from slack_cli.server import make_server, start_server, shutdown_server

def valid_args(args):
    if len(args) < 2:
        return False
    elif args[1] not in ("oauth", "ch", "im", "ch_h", "im_h", "ch_p", "im_p"):
        return False
    elif args[1].endswith("_h") and len(args) < 3:
        return False
    elif args[1].endswith("_p") and len(args) < 4:
        return False
    else:
        return True

def usage_text():
    out = []
    out.append("usage: slk [--version] [--help]\n\t<command> [<args>]\n\n")
    out.append("These are common slack-cli commands:\n\n")
    out.append("local database:\n\tpull\n\n")
    out.append("channels:\n\tch\n\tch_h <id>\n\n")
    out.append("instant messages:\n\tim\n\tim_h <id>")

    return "".join(out)

def process_command(service, viewer):
    command = sys.argv[1]

    if command == "oauth":
        out = str(oauth)
    elif command == "ch":
        channels = service.list_channels()
        out = viewer.view_channels(channels)
    elif command == "im":
        instant_messages = service.list_instant_messages()
        out = viewer.view_instant_messages(instant_messages)
    elif command == "ch_h":
        history = service.channels_history(sys.argv[2])
        out = viewer.view_history(history)
    elif command == "im_h":
        history = service.instant_messages_history(sys.argv[2])
        out = viewer.view_history(history)
    elif command == "im_p" or command == "ch_p":
        out = service.post_message(sys.argv[2], sys.argv[3])
    else:
        out = ""

    print(out)

def authorize_slack_cli():
    print("Please authorize slack-cli at {}".format(authorization_url))
    server, token_ready = make_server("127.0.0.1", 8443)
    start_server(server)

    # acquires the shared resource lock (means no producer is accessing the resource)
    # checks the codition (oauth_path existence)
    # sleeps if the condition is not true
    # upon waking, we check the codition once more, to handle
    # spurious wakeups
    token_ready.acquire()
    while not os.path.exists(oauth_path):
        token_ready.wait()

    shutdown_server(server)

    # at this point the lock should be released
    token_ready.release();

def main():

    if not valid_args(sys.argv):
        sys.exit(usage_text())

    if not os.path.exists(slack_cli_path):
        os.mkdir(slack_cli_path)

    if not os.path.exists(oauth_path):
        authorize_slack_cli()

    print("Loading oauth access token...")
    oauth = token_from_file(oauth_path)
    service = SlackService(oauth)
    viewer = SlackViewer()

    print("Processing command...")
    process_command(service, viewer)
