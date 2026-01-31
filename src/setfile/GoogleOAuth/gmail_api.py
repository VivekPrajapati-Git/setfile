from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from pathlib import Path
import base64
import os

TOKEN_FILE = Path(__file__).parent / "secrets" / "gmail_token.json"

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
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

    for part in message["payload"]["parts"]:
        if part.get("filename") and part.get("body", {}).get("attachmentId"):
            att_id = part["body"]["attachmentId"]

            att = service.users().messages().attachments().get(
                userId="me",
                messageId=message["id"],
                id=att_id
            ).execute()

            data = base64.urlsafe_b64decode(att["data"].encode("UTF-8"))

            filepath = os.path.join(download_dir, part["filename"])

            with open(filepath, "wb") as f:
                f.write(data)

            print("Downloaded:", part["filename"])
