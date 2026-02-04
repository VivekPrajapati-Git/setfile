import os
import pathlib
import requests as r
from flask import Flask, session, redirect, request
from google_auth_oauthlib.flow import Flow
from setfile.GoogleOAuth.db import get_db, init_db
import threading

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

    google_id = user_info['id']
    email = user_info['email']

    expires_at = credentials.expiry.isoformat() if credentials.expiry else None
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (google_id, email, access_token , refresh_token , expires_at) VALUES (?, ?, ?, ?, ?)", (google_id, email, credentials.token, credentials.refresh_token or "", expires_at))
    db.commit()
    db.close()

    path = pathlib.Path(__file__).resolve().parent.parent/'session.json'
    with open(path,'w') as f:
        f.write(f'{user_info}')

    print("Callback Received",flush=True)
    return "Login successful! You can close this tab."

@app.route('/')
def index():
    return "<button><a href='/login'>Login</a></button>"

if __name__ == "__main__":
    init_db()
    app.run(port=5000)
