import os
import click
import webbrowser
import subprocess
import time
from src.setfile.commands.organize import organize_files
from src.setfile.commands.revert import revert

# Making one single command
@click.group()
def main():
    pass

# Command for organizing
@main.command()
@click.option('--path',default = os.curdir)
def organize(path):
    organize_files(path)
    
@main.command()
def revert():
    revert()

@main.command()
def gmail_auth():
    click.echo("Starting Gmail Authentication Server...")
    subprocess.Popen(["python", "-m", "setfile.GoogleOAuth.auth_server"])
    time.sleep(1.5)

    webbrowser.open("http://localhost:5000/")
    click.echo("Browser Opened for gmail connection..")
    click.echo("After Connection you can close the browser!")

@main.command()
def gmail_org():
    pass

if __name__ == "__main__":
    main()