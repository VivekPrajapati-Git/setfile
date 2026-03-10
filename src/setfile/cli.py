import os
import click

# Making one single command
@click.group()
def main():
    pass

# Command for organizing
@main.command(help="Organize the files")
@click.option('--path',default = os.curdir)
def organize(path):
    from setfile.commands.organize import organize_files
    organize_files(path)
    
@main.command(help="Revert the changes")
def revert():
    from setfile.commands.revert import revert
    revert()

@main.command(help="Used for authenticating gmail")
def gmailauth():
    from setfile.commands.gmail_auth import gmail_auth
    gmail_auth()

@main.command(help="Used for downloading mail attachments")
def gmail_download():
    from setfile.commands.gmail_download import download
    download()

@main.command(help = "Suggest unused files")
@click.option("--days", type=int)
@click.option("--path", default=os.curdir)
@click.option("--delete", is_flag=True, help="Delete Unused Files")
def suggest_unused(days,path, delete):
    from setfile.commands.suggest import suggest
    suggest(path,days,delete)        

if __name__ == "__main__":
    main()