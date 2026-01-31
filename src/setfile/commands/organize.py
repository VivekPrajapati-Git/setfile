from pathlib import Path
from src.setfile.utils.file_rules import get_label
from datetime import datetime
from src.setfile.utils.logger import logger as log
import os
import click

def organize_files(path):
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