from src.setfile.utils.history import log_reader
from src.setfile.utils.logger import logger as log
from pathlib import Path
import click
import os

def revert():
    run_id , moves = log_reader()
    if not run_id:
        click.echo("No Files to revert")
        return

    if not click.confirm("Are You Sure you want to revert ?"):
        click.echo("Aborted")
        log.warning("User Aborted the Revert Changes")
        return

    log.info("Reverting the changes")
    for move in reversed(moves):
        src = move['src']
        des = move['des']
        source = Path(src.strip())
        destination = Path(des.strip())
        os.rename(destination,source)
        log.info(f"Reverted Files : {destination} -> {source}")
        
        label_folder = destination.resolve().parent
        try:
            Path.rmdir(label_folder)
            log.warning(f"Removing the Parent Folder -> {label_folder}")
        except OSError:
            pass
    click.echo("Files reverted Successfully")
