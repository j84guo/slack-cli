import json

from config import conn, client_id, client_secret, redirect_uri
from urllib.parse import quote


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


def obtain_access_token(params):
    access_token_reqs(conn, params["code"])
    data = http_resp_json_body(conn)
    return get_slack_oauth_creds(data, params["code"])

def access_token_reqs(conn, code):
    path_query = access_token_path_query(code)
    conn.request("GET", path_query)

def access_token_path_query(code):
    path = "/api/oauth.access"
    return "{}?client_id={}&client_secret={}&code={}&redirect_uri={}".format(path, client_id, client_secret, code, redirect_uri)

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
