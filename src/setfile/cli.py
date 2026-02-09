import os
import click

# Making one single command
@click.group()
def main():
    pass

# Command for organizing
@main.command()
@click.option('--path',default = os.curdir)
def organize(path):
    from setfile.commands.organize import organize_files
    organize_files(path)
    
@main.command()
def revert():
    from setfile.commands.revert import revert
    revert()

@main.command()
def gmailauth():
    from setfile.commands.gmail_auth import gmail_auth
    gmail_auth()

@main.command()
def gmail_download():
    from setfile.commands.gmail_download import download
    download()

if __name__ == "__main__":
    main()