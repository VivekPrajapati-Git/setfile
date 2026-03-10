import os
import click
from src.setfile.utils.unused import unused

def suggest(path,days,delete):
    files = unused(path,days)
    click.echo("Following are the files")
    for name,age in files:
        print(f"{name} - last used {age} days ago")
        if delete:
            if not click.confirm("Are you sure you want to delete: "):
                click.echo("Aborted")
                return
            os.remove(f'{path}/{name}')
            print(f"Deleted {name}")