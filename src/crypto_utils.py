import os
from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

KEY_FILE = os.path.join(DATA_DIR, "key.key")


def generate_key():
    return Fernet.generate_key()


def save_key(key: bytes):
    with open(KEY_FILE, "wb") as f:
        f.write(key)


def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()


def get_key():
    # Tries to load existing key file or generates a new key if file not found
    try:
        return load_key()
    except FileNotFoundError:
        key = generate_key()
        save_key(key)
        return key


def encrypt(data: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data)


def decrypt(data: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(data)
