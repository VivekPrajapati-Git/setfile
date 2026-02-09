from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from pathlib import Path
import base64
import os
import keyring 
import json

email_file = Path(__file__).resolve().parent.parent/'session.txt'

if not email_file.exists():
    raise Exception("User is not logged in.")

with open(email_file, 'r') as f:
    email = f.read()

raw = keyring.get_password("gmail_cli",email)
if not raw: 
    raise Exception("User is not logged in.")

token_data = json.loads(raw)

if isinstance(token_data,str):
    token_data = json.loads(token_data)

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    creds = Credentials.from_authorized_user_info(token_data, SCOPES)
    return build("gmail", "v1", credentials=creds)

def list_messages(query="has:attachment"):
    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=20
    ).execute()

    return results.get("messages", [])

def get_message(message_id):
    service = get_gmail_service()

    return service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

def download_attachments(message, download_dir):
    service = get_gmail_service()
    os.makedirs(download_dir, exist_ok=True)

    def walk_parts(parts):
        for part in parts:
            if part.get("filename") and part.get("body", {}).get("attachmentId"):
                yield part
            if "parts" in part:
                yield from walk_parts(part["parts"])

    payload = message.get("payload", {})
    parts = payload.get("parts", [])

    for part in walk_parts(parts):
        att_id = part["body"]["attachmentId"]

        att = service.users().messages().attachments().get(
            userId="me",
            messageId=message["id"],
            id=att_id
        ).execute()

        data = base64.urlsafe_b64decode(att["data"].encode("UTF-8"))
        filename = part["filename"]

        filepath = os.path.join(download_dir, filename)
        with open(filepath, "wb") as f:
            f.write(data)

        print("Downloaded:", filename)