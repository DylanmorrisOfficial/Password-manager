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
