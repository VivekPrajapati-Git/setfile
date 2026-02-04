import click
import subprocess
import time
import webbrowser
import flask

def gmail_auth():
    click.echo("Starting Gmail Authentication Server...")
    subprocess.Popen([
        "python", "-m", "setfile.GoogleOAuth.auth_server"],
    )

    time.sleep(1.5)
    webbrowser.open("http://localhost:5000/")

    click.echo("Browser Opened for gmail connection..")
    click.echo("After Connection you can close the browser!")
