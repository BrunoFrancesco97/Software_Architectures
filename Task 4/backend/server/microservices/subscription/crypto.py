import hashlib
from random import choice
from string import ascii_uppercase, digits


def generate_salt():
    return ''.join(choice(ascii_uppercase + digits) for i in range(30))


def sha256_basic(text: str):
    return hashlib.sha256(str(text).encode('utf-8')).hexdigest()

    
def sha256_encode(text: str):
    salt = generate_salt()
    return hashlib.sha256(str(text + salt).encode('utf-8')).hexdigest(), salt

def sha256_encode_salt(text: str, salt : str):
    return hashlib.sha256(str(text + salt).encode('utf-8')).hexdigest()


