"""
Todo :
- duplicate function http_resp_json_body()
- more elegant way to persist user credentials
"""

import json

from http.client import HTTPSConnection
from slack_cli.config import client_id, client_secret, redirect_url


class SlackOauthCredentials(object):

    def __init__(self, code, access_token, scope, user_id, team_name, team_id):
        self.code = code
        self.access_token = access_token
        self.scope = scope
        self.user_id = user_id
        self.team_name = team_name
        self.team_id = team_id

    def __str__(self):
        return "<OauthCredentials object code:{}, access_token: {}, scope: {}, user_id={}, team_name={}, team_id={}>".format(
            self.code, self.access_token, self.scope, self.user_id, self.team_name, self.team_id)

    def __repr__(self):
        return self.__str__()

def token_to_file(token_path, oauth):
    payload = {
        "code": oauth.code,
        "access_token": oauth.access_token,
        "scope": oauth.scope,
        "user_id": oauth.user_id,
        "team_name": oauth.team_name,
        "team_id": oauth.team_id
    }
    f = open(token_path, "w")
    f.write(json.dumps(payload))
    f.close()

def token_from_file(token_path):
    try:
        f = open(token_path, "r")
        payload = json.loads(f.read())
        return SlackOauthCredentials(payload["code"], payload["access_token"], payload["scope"], payload["user_id"], payload["team_name"], payload["team_id"])
    except Exception as e:
        print("Error loading token from file: {}".format(e))

def obtain_access_token(params):
    conn = HTTPSConnection("slack.com")
    access_token_reqs(conn, params["code"])
    data = http_resp_json_body(conn)
    return get_slack_oauth_creds(data, params["code"])

def access_token_reqs(conn, code):
    path_query = access_token_path_query(code)
    conn.request("GET", path_query)

def access_token_path_query(code):
    path = "/api/oauth.access"
    return "{}?client_id={}&client_secret={}&code={}&redirect_uri={}".format(path, client_id, client_secret, code, redirect_url)

def http_resp_json_body(conn):
    try:
        resp_obj = conn.getresponse()
        resp_bytes = resp_obj.read()
        resp_str = str(resp_bytes, "ascii")
        return json.loads(resp_str)

    except Exception as e:
        print("Error getting response from Slack API: {}".format(repr(e)))

def get_slack_oauth_creds(data, code=None):
    try:
        access_token = data["access_token"]
        scope = data["scope"]
        user_id = data["user_id"]
        team_name = data["team_name"]
        team_id = data["team_id"]
        return SlackOauthCredentials(code, access_token, scope, user_id, team_name, team_id)

    except Exception as e:
        print("Error extracting oauth credentials: {}, response body {}".format(repr(e), data))
