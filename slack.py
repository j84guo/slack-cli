"""
Todo :
- understand slack api
- store slack data in local database
"""

import json

from http.client import HTTPSConnection

def get_user_conversations(oauth):
    conn = HTTPSConnection("slack.com")
    user_conversations_reqs(conn, oauth)
    return http_resp_json_body(conn)

def user_conversations_reqs(conn, oauth):
    headers = {
        "Authorization": "Bearer {}".format(oauth.access_token)
    }
    conn.request("GET", "/api/users.conversations", headers=headers)

def http_resp_json_body(conn):
    try:
        resp_obj = conn.getresponse()
        resp_bytes = resp_obj.read()
        resp_str = str(resp_bytes, "ascii")
        return json.loads(resp_str)

    except Exception as e:
        print("Error getting response from Slack API: {}".format(repr(e)))
