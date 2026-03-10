import click
import subprocess
import time
import webbrowser
from pathlib import Path

def gmail_auth():
    path = Path(__file__).resolve().parent.parent/'session.txt'
    if path.is_file():
        click.echo("You are already logged in!")
        return 

    click.echo("Starting Gmail Authentication Server...")
    subprocess.Popen([
        "python", "-m", "setfile.GoogleOAuth.gmail_auth"],
    )

    time.sleep(1.5)
    webbrowser.open("http://localhost:5000/")

    click.echo("Browser Opened for gmail connection..")
    click.echo("After Connection you can close the browser!")
