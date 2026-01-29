import os
from PyPDF2 import PdfReader
import docxpy

def read_file(path):
    # file_name = path.split('/')
    # file_name = file_name[-1]

    _,extension = os.path.splitext(path)

    if extension == '.pdf':
        reader = PdfReader(path)
        text = reader.pages[0]
        text = text.extract_text()
        return text
    elif extension == '.docx':
        text = docxpy.process(path)
        return text
    elif extension == '.pptx':
        pass
    elif extension == '.txt':
        with open(path, "r") as f:
            content = f.read()
            return content
    else:
        return ""