import re
from difflib import SequenceMatcher

ALLOWED_EXTENSIONS=['pdf','py','c','cpp','java']

def whitespaces_remover(text: str):
    return re.sub(' +', '', text)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

