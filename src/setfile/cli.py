import click
from src.setfile.commands.organize import organize_files
from src.setfile.commands.revert import revert
import os

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
@click.option('--email', required=True)
def gmail_auth(email):
    pass

@main.command()
def gmail_org():
    pass

if __name__ == "__main__":
    main()