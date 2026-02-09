import os
import keyring
import pathlib
import json
import requests as r
from flask import Flask, session, redirect, request
from google_auth_oauthlib.flow import Flow

app = Flask("Google-Login App")
app.secret_key = "hello"
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

client_secret_file = pathlib.Path(__file__).resolve().parent.parent.parent.parent/"secret/gmail_auth.json"
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
]

@app.route("/login")
def login():
    flow = Flow.from_client_secrets_file(
        client_secret_file,
        scopes = SCOPES,
        redirect_uri = "http://localhost:5000/callback"
    )
    auth_url, state = flow.authorization_url(prompt="consent")
    session["state"] = state
    return redirect(auth_url)

@app.route("/callback")
def callback():
    flow = Flow.from_client_secrets_file(
        client_secret_file,
        scopes = SCOPES,
        redirect_uri = "http://localhost:5000/callback"
    )
    
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials

    user_info = r.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {credentials.token}"}
    ).json()

    email = user_info['email']

    keyring.set_password(
        "gmail_cli",
        email,
        json.dumps(credentials.to_json())
    )

    path = pathlib.Path(__file__).resolve().parent.parent/'session.txt'
    with open(path,'w',encoding='utf-8') as f:
        f.write(f'{email}')

    return "Login successful! You can close this tab."

@app.route('/')
def index():
    return "<button><a href='/login'>Login</a></button>"

if __name__ == "__main__":
    app.run(port=5000)
