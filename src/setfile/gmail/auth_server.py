from flask import Flask, session, abort, redirect, request
from google_auth_oauthlib.flow import Flow
import os
import pathlib

app = Flask("Google-Login App")
app.secret_key = "hello"
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

client_secret_file = pathlib.Path(__file__).resolve().parent.parent.parent.parent/"secret/google_oauth.json"
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

flow = Flow.from_client_secrets_file(
    client_secret_file,
    scopes = SCOPES,
    redirect_uri = "http://localhost:5000/callback"
)

def login_is_required(function):
    def wrapper(*args,**kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function(*args,**kwargs)
    return wrapper

@app.route("/login")
def login():
    auth_url, state = flow.authorization_url(prompt="consent")
    session["state"] = state
    return redirect(auth_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials

    with open("gmail_token.json", "w") as f:
        f.write(credentials.to_json())

    return "Login successful! You can close this tab."

@app.route('/')
def index():
    return "<button><a href='/login'>Login</a></button>"

@app.route('/protected_area')
@login_is_required
def protected_area():
    return "protected area <button><a href = '/logout'>Logout</a></button>" 

if __name__ == "__main__":
    app.run(debug=True)