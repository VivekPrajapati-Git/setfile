import os
import click
import webbrowser
import subprocess
import time
from src.setfile.commands.organize import organize_files
from src.setfile.commands.revert import revert
from src.setfile.commands.gmail_auth import gmail_auth

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
def gmailauth():
    gmail_auth()

@main.command()
def gmailorg():
    pass

if __name__ == "__main__":
    main()