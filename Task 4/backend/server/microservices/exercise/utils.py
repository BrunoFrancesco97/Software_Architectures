import re
from difflib import SequenceMatcher
import base64

ALLOWED_EXTENSIONS=['pdf','py','c','cpp','java']

def whitespaces_remover(text: str):
    return re.sub(' +', '', text)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def encode(a : str) -> str:
    return (base64.b64encode(bytes(a,'UTF-8'))).decode(encoding='UTF-8')

def decode(a : str):
    bytes_decoded = bytes(a,'UTF-8')
    return (base64.b64decode(bytes_decoded)).decode(encoding='UTF-8')
