# Project Overview

## Introduction
Use `setfile` to clean up your messy directories. It is an intelligent file organizer that analyzes the content of your files and moves them into appropriate folders based on their category.

## Purpose
The main purpose of this project is to automate the process of file organization. Instead of relying on file extensions or manual sorting, `setfile` reads the actual content of documents (PDF, DOCX, TXT), uses a pre-trained Machine Learning model to predict the document type, and organizes the files accordingly.

## Key Features
- **Content-Based Classification**: Uses a Machine Learning model (SVM) to classify documents based on text content.
- **Multiple File Support**: Supports reading from `.pdf`, `.docx`, and `.txt` files.
- **Automated Organization**: Moves files into labeled directories automatically.
- **Safety Mechanism**: Includes a `revert` command to undo the last organization operation, restoring files to their original locations.
- **Logging**: Maintains detailed logs of operations and moves to ensure traceability and enable the revert functionality.
