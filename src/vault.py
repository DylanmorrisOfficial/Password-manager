import json
from models import PasswordEntry


class Vault:
    def __init__(self):
        self.entries = []

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
        # Return a list of all entries in the vault
        return self.entries

    def save_to_file(self, filename="vault.json"):
        # Save entries to a JSON file
        data = [entry.to_dict() for entry in self.entries]

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_from_file(self, filename="vault.json"):
        # Load entries from a JSON file
        try:
            with open(filename, "r") as file:
                data = json.load(file)

                self.entries = [PasswordEntry.from_dict(entry) for entry in data]

        except FileNotFoundError:
            self.entries = []
