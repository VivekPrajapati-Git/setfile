from setfile.GoogleOAuth.gmail_functions import get_message, list_messages,download_attachments
import click
from pathlib import Path

download_dir = Path.home() / "Downloads/gmail-download"

def download():
    messages = list_messages()
    click.echo(messages)
    for message in messages:
        one = message
        id = one['id']
        full = get_message(id)
        download_attachments(full, download_dir)