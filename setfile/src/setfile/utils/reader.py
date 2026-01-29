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
    elif extension in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
        return f"This is a video file format {extension[1:]} movie clip recording."
    elif extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']:
        return f"This is an image file format {extension[1:]} photo picture graphic."
    elif extension in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']:
        return f"This is an audio file format {extension[1:]} sound music recording song."
    else:
        return ""