from urllib.parse import quote
from http.client import HTTPSConnection

conn = HTTPSConnection("slack.com")
client_id = "361449430741.360777286161"
client_secret = "afe16e3a4e570987c8f04a122c385c2a"
redirect_uri = quote("https://localhost:8443/slack-cli/authorize", safe="")
