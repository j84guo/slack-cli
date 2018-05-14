"""
Todo :
-
- store slack data in local database
- determine whether message is seen/unseen
"""

import json

from http.client import HTTPSConnection
from slack_models import SlackChannel, SlackInstantMessage, SlackMessage, SlackFile


class SlackService(object):

    def __init__(self, oauth):
        self.oauth = oauth
        self.conn = HTTPSConnection("slack.com")

    def oauth_header(self):
        headers = {"Authorization": "Bearer {}".format(self.oauth.access_token)}
        return headers

    def http_resp_json_body(self, conn):
        try:
            resp_obj = conn.getresponse()
            resp_bytes = resp_obj.read()
            resp_str = str(resp_bytes, "ascii")
            return json.loads(resp_str)

        except Exception as e:
            print("Error getting response from Slack API: {}".format(repr(e)))

    def list_channels(self):
        self.list_channels_reqs(self.conn)
        body = self.http_resp_json_body(self.conn)
        return self.build_channels(body)

    def list_channels_reqs(self, conn):
        headers = self.oauth_header()
        conn.request("GET", "/api/channels.list", headers=headers)

    def build_channels(self, body):
        channels = []
        for c in body["channels"]:
            channels.append(SlackChannel(c["id"], c["created"], c["name"], c["topic"], c["purpose"], c["num_members"]))
        return channels

    def channels_history(self, id):
        self.channels_history_reqs(self.conn, id)
        body = self.http_resp_json_body(self.conn)
        return self.build_channels_history(body)

    def build_channels_history(self, body):
        history = []
        for m in body["messages"]:
            history.append(self.build_message(m))
        return history

    def build_message(self, m):
        if "subtype" in m and m["subtype"] == "file_share":
            message = SlackMessage(m["type"], m["text"], m["ts"]
            ).set_subtype(m["subtype"]
            ).set_file(self.build_file(m["file"])
            ).set_upload(m["upload"]
            ).set_username(m["username"])
        else:
            message = SlackMessage(m["type"], m["text"], m["ts"])

        return message

    def build_file(self, f):
        file = SlackFile(f["id"], f["created"], f["name"], f["filetype"], f["user"])
        return file

    def channels_history_reqs(self, conn, id):
        headers = self.oauth_header()
        conn.request("GET", "/api/channels.history?channel={}".format(id), headers=headers)

    def list_instant_messages(self):
        self.list_instant_messages_reqs(self.conn)
        body = self.http_resp_json_body(self.conn)
        return self.build_instant_messages(body)

    def build_instant_messages_history(self, body):
        history = []
        for m in body["messages"]:
            history.append(self.build_message(m))
        return history

    def list_instant_messages_reqs(self, conn):
        headers = self.oauth_header()
        conn.request("GET", "/api/im.list", headers=headers)

    def build_instant_messages(self, body):
        instant_messages = []
        for i in body["ims"]:
            instant_messages.append(SlackInstantMessage(i["id"], i["created"], i["user"]))
        return instant_messages

    def instant_messages_history(self, id):
        self.instant_messages_history_reqs(self.conn, id)
        body = self.http_resp_json_body(self.conn)
        return self.build_instant_messages_history(body)

    def instant_messages_history_reqs(self, conn, id):
        headers = self.oauth_header()
        conn.request("GET", "/api/im.history?channel={}".format(id), headers=headers)

    def post_message(self, id, text):
        self.post_message_reqs(self.conn, id, text)
        return self.http_resp_json_body(self.conn)

    def post_message_reqs(self, conn, id, text):
        headers = self.oauth_header()
        headers["Content-Type"] = "application/json"
        body = {
            "channel": id,
            "text": text,
            "as_user": "true"
        }
        conn.request("POST", "/api/chat.postMessage", headers=headers, body=json.dumps(body))
