import os
from .reader import read_file
from .logger import logger
from setfile.core.prediction import prediction

EXTENSION_RULES = {
  ".exe": "installers",
  ".msi": "installers",
  ".zip": "archives",
  ".rar": "archives",
  ".7z": "archives",
  ".jpg": "images",
  ".jpeg": "images",
  ".png": "images",
  ".webp": "images",
  ".mp4": "videos",
  ".mp3": "audio"
}

supported_format = {
    '.pptx','.docx','.xlsx','.pdf','.txt'
}

def get_label(path):
    _, extension = os.path.splitext(str(path))
    extension = extension.lower()
    
    if extension in EXTENSION_RULES:
        return EXTENSION_RULES[extension]

    if extension not in supported_format:
        logger.info(f"{path} : Unsupported Binary File")
        return "others"
    
    try:
        text = read_file(path)
    except:
        logger.warning("Failed to read file content")
        return "others"
    
    try:
        predict = prediction(text)
        return predict[0]
    except:
        logger.warning("Model Failed to predict")
        return "others"