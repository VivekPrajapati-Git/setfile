# Directory and Structure Analysis

The project follows a modular structure, separating the CLI interface, core logic, utilities, and data models.

## Root Directory
- **`cli.py`**: The main entry point of the application. It uses the `click` library to define command-line interfaces for `organize` and `revert` commands.
- **`README.md`**: Basic documentation explaining the folder structure and flow.
- **`pyproject.toml` / `requirements.txt`**: Dependency management files.
- **`logs/`**: Directory where application logs (`setfile.log`, `error.log`, `moves.log`) are stored.

## Source Code (`src/setfile`)
### `core/`
Contains the core business logic of the application.
- **`prediction.py`**: Handles the loading of the Machine Learning model (`doc_classifier_svm.pkl`) and provides a `prediction` function to classify text content.

### `utils/`
Contains helper modules for file operations and logging.
- **`reader.py`**: Provides functionality to read text content from different file formats (`.pdf`, `.docx`, `.txt`). It handles file extension detection and uses appropriate libraries (`PyPDF2`, `docxpy`) to extract text.
- **`logger.py`**: a custom `Logger` class that manages writing to different log files. It specifically handles "MOVE" events to track file relocations for the revert feature.
- **`history.py`**: Contains `log_reader`, which parses the `moves.log` to retrieve the history of file moves, enabling the revert functionality.

### `model/`
- **`doc_classifier_svm.pkl`**: The serialized Scikit-learn SVM model used for document classification.

## Data Flow Summary
1.  **Input**: User executes a command via `cli.py`.
2.  **Processing**:
    -   Files are read using `utils/reader.py`.
    -   Content is classified using `core/prediction.py`.
3.  **Action**:
    -   Files are moved to labeled directories.
    -   Actions are logged via `utils/logger.py`.
4.  **Revert**:
    -   History is read via `utils/history.py`.
    -   Files are moved back based on logs.
