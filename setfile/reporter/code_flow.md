# Code Flow Analysis

This document details the execution flow of the primary features: Organizing files and Reverting changes.

## 1. Organize Flow (`setfile organize`)

Triggered by the `@main.command() organize` function in `cli.py`.

1.  **Initialization**:
    -   The command accepts a `--path` argument (defaults to current directory).
    -   `Path` object is created for the target directory.

2.  **File Discovery**:
    -   Iterates through the directory using `folder_path.iterdir()`.
    -   collects all files into a list `files`.
    -   Logs found files and skipped directories.
    -   If no files are found, the process executes.

3.  **User Confirmation (Prediction)**:
    -   Asks "Do you want to run prediction".
    -   If yes, proceeds; otherwise aborts.

4.  **Prediction Phase**:
    -   Iterates through each file in `files`.
    -   **Read**: Calls `read_file(file)` from `utils.reader`.
        -   Checks extension (`.pdf`, `.docx`, `.txt`).
        -   Extracts text content.
    -   **Predict**: Calls `prediction(text)` from `core.prediction`.
        -   Loads `model/doc_classifier_svm.pkl`.
        -   Returns the predicted category (label).
    -   Stores result in a dictionary `result = {file_path: label}`.
    -   Catches and logs errors during this process.

5.  **User Confirmation (Organizing)**:
    -   Asks "Do You want to organize files into folder".
    -   If yes, proceeds; otherwise aborts.

6.  **Organization Phase**:
    -   Generates a `run_id` based on the current timestamp.
    -   Iterates through `result` items.
    -   **Create Folder**: Checks if a folder exists for the `label`. If not, creates it (`os.mkdir`).
    -   **Move File**: Moves the file to the label folder (`os.rename`).
    -   **Log Move**: Calls `log.moves(run_id, file_path, destination)` from `utils.logger` to record the move in `moves.log`.

## 2. Revert Flow (`setfile revert`)

Triggered by the `@main.command() revert` function in `cli.py`.

1.  **Read History**:
    -   Calls `log_reader()` from `utils/history.py`.
    -   Parses `moves.log` to get the last `run_id` and a list of `moves`.

2.  **Validation**:
    -   If no history is found, prints "No Files to revert" and exits.

3.  **User Confirmation**:
    -   Asks "Are You Sure you want to revert ?".

4.  **Revert Phase**:
    -   Iterates through `moves` in **reverse order**.
    -   Extracts `src` (original location) and `des` (current location).
    -   **Move Back**: Renames `destination` to `source`.
    -   **Cleanup**: Attempts to remove the parent folder (label folder) if it is empty (`Path.rmdir`).
    -   Logs the revert action.
