from urllib.parse import quote

client_id = "361449430741.360777286161"
client_secret = "afe16e3a4e570987c8f04a122c385c2a"
scope = quote("channels:read,chat:write:user,team:read,usergroups:read,users:read,groups:read,channels:history,groups:history,mpim:history,mpim:read,im:history,im:read", safe="")
redirect_url = quote("https://localhost:8443/slack-cli/authorize", safe="")
authorization_url = "https://slack.com/oauth/authorize?client_id={}&scope={}&redirect_uri={}".format(client_id, scope, redirect_url)
oauth_path = "oauth.json"
tls_path = "server.pem"
