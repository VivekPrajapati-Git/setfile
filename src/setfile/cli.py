import click
import os
from datetime import datetime
from  pathlib import Path
from .utils.reader import read_file
from .core.prediction import prediction
from .utils.logger import logger as log
from .utils.history import log_reader
from .utils.file_rules import get_label

# Making one single command
@click.group()
def main():
    pass

# Command for organizing
@main.command()
@click.option('--path',default = os.curdir)
def organize(path):
    # Reading files from folder i.e getting the count of folder
    folder_path = Path(path)

    # Printing the file name
    files = []
    click.echo("Following are the files in folder: ")
    log.info("Checking the folder")
    for file in folder_path.iterdir():
        if file.is_file():
            files.append(file)
            print(file.name)
            log.info(f"files found -> {file.name}")
        else:
            log.warning(f"Skipped files -> {file}")

    if files.count == 0:
        click.echo("No file found!")
        return

    # Asking User Permission for Predicting and Organizing
    if not click.confirm("Do you want to run prediction"):
        click.echo("Aborted")
        log.warning("User Aborted the prediction")
        return

    log.info("Making the Prediction")
    result = {}
    for file in files:
        try:
            predict = get_label(file)
            log.info(f"{file.name} -> {predict}")
            result.update({file : predict})
            print(file.name , ":" , predict)
        except Exception as e:
            log.error(f"Prediction failed for {file.name} : {e}")
            return

    log.info("Organizing the file")
    if not click.confirm("Do You want to organize files into folder"):
        click.echo("Aborted")
        log.warning("User aborted the organizing")
        return
    
    base = Path(path)
    now = datetime.now()
    run_id = now.strftime("%Y%m%d_%H%M%S")
    for file_path , label in result.items():
        try:
            folder_path = Path(label)
            label_folder = base / label
            if not os.path.isdir(label_folder):
                log.info(f"Making the directory of label -> {label_folder}")
                os.mkdir(label_folder)
            destination = label_folder / file_path.name
            os.rename(file_path, destination)
            log.info(f"Moved files : {file_path} -> {destination}")
            log.moves(run_id,file_path,destination)
        except Exception as e:
            log.error(f"Failed to organize {file_path.name} : {e}")
    click.echo("Files Organized !")
    
@main.command()
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
        
if __name__ == "__main__":
    main()