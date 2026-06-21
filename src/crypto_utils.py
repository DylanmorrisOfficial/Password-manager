import os
import hashlib
import base64
from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

KEY_FILE = os.path.join(DATA_DIR, "key.key")


def derive_key(password: str, salt: str):
    # Creates a hashed key using the master password and salt
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
    return base64.urlsafe_b64encode(key)


def encrypt(data: bytes, password: str, salt: str):
    # Encrypts the data with the derived key
    key = derive_key(password, salt)
    return Fernet(key).encrypt(data)


def decrypt(data: bytes, password: str, salt: str):
    # Decrytps the data with the derived key
    key = derive_key(password, salt)
    return Fernet(key).decrypt(data)
