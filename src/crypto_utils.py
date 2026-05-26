from cryptography.fernet import Fernet

KEY_FILE = "key.key"


def generate_key():
    return Fernet.generate_key()


def save_key(key: bytes):
    with open(KEY_FILE, "wb") as f:
        f.write(key)


def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()


def get_key():
    # Try to load existing key, if not found, generate a new one and save it
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
