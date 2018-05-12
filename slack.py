"""
Todo :
- understand slack api
- break functionality into im's, channels
- store slack data in local database
- determine whether message is seen/unseen
"""

import json

from http.client import HTTPSConnection

def list_channels(oauth):
    conn = HTTPSConnection("slack.com")
    list_channels_reqs(conn, oauth)
    return http_resp_json_body(conn)

def list_channels_reqs(conn, oauth):
    headers = oauth_header(oauth)
    conn.request("GET", "/api/channels.list", headers=headers)

def channels_history(oauth, id):
    conn = HTTPSConnection("slack.com")
    channels_history_reqs(conn, oauth, id)
    return http_resp_json_body(conn)

def channels_history_reqs(conn, oauth, id):
    headers = oauth_header(oauth)
    conn.request("GET", "/api/channels.history?channel={}".format(id), headers=headers)

def list_instant_messages(oauth):
    conn = HTTPSConnection("slack.com")
    list_instant_messages_reqs(conn, oauth)
    return http_resp_json_body(conn)

def list_instant_messages_reqs(conn, oauth):
    headers = oauth_header(oauth)
    conn.request("GET", "/api/im.list", headers=headers)

def instant_messages_history(oauth, id):
    conn = HTTPSConnection("slack.com")
    instant_messages_history_reqs(conn, oauth, id)
    return http_resp_json_body(conn)

def instant_messages_history_reqs(conn, oauth, id):
    headers = oauth_header(oauth)
    conn.request("GET", "/api/im.history?channel={}".format(id), headers=headers)

def post_message(oauth, id, text):
    conn = HTTPSConnection("slack.com")
    post_message_reqs(conn, oauth, id, text)
    return http_resp_json_body(conn)

def post_message_reqs(conn, oauth, id, text):
    headers = oauth_header(oauth)
    headers["Content-Type"] = "application/json"
    body = {
        "channel": id,
        "text": text,
        "as_user":"true"
    }
    conn.request("POST", "/api/chat.postMessage", headers=headers, body=json.dumps(body))

def oauth_header(oauth):
    headers = {"Authorization": "Bearer {}".format(oauth.access_token)}
    return headers

def http_resp_json_body(conn):
    try:
        resp_obj = conn.getresponse()
        resp_bytes = resp_obj.read()
        resp_str = str(resp_bytes, "ascii")
        return json.loads(resp_str)

    except Exception as e:
        print("Error getting response from Slack API: {}".format(repr(e)))
