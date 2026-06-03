import json
from models import PasswordEntry
from crypto_utils import encrypt, decrypt, get_key, save_key, load_key
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Vault:
    def __init__(self, username):
        os.makedirs(os.path.join(BASE_DIR, "vaults"), exist_ok=True)

        self.username = username
        self.entries = []

        self.file_name = os.path.join(BASE_DIR, "vaults", f"{username}.dat")

        key = load_key()

        if not key:
            # Generates a new key and save it if no key is found
            key = get_key()
            save_key(key)

        self.key = key

    def add_entry(self, entry):
        # Adds a new entry to entries
        self.entries.append(entry)

    def remove_entry(self, service):
        # Removes specified entry from entries
        self.entries = [entry for entry in self.entries if entry.service != service]

    def get_entry(self, service):
        # Return the first entry that matches the service, or None if entry not found
        for entry in self.entries:
            if entry.service == service:
                return entry
        return None

    def list_entries(self):
        # Returns a list of all entries in the vault
        return self.entries

    def save_to_file(self):
        # Saves the vault entries to a file in encrypted format
        data = [entry.to_dict() for entry in self.entries]

        json_data = json.dumps(data).encode()

        encrypted = encrypt(json_data, self.key)

        with open(self.file_name, "wb") as file:
            file.write(encrypted)

    def load_from_file(self):
        # Loads vault entries from a file, decrypting the data and populating entries
        try:
            with open(self.file_name, "rb") as file:
                encrypted_data = file.read()

            decrypted = decrypt(encrypted_data, self.key)

            json_data = decrypted.decode()

            data = json.loads(json_data)

            self.entries = [PasswordEntry.from_dict(entry) for entry in data]

        except FileNotFoundError:
            # Starts with an empty vault if file does not exist
            self.entries = []
