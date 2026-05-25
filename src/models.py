class PasswordEntry:
    def __init__(self, service, username, password, notes):
        self.service = service
        self.username = username
        self.password = password
        self.notes = notes

    def to_dict(self):
        # Converts the PasswordEntry to a dictionary
        return {
            "service": self.service,
            "username": self.username,
            "password": self.password,
            "notes": self.notes,
        }

    @staticmethod
    def from_dict(data):
        # Converts a dictionary back to a PasswordEntry
        return PasswordEntry(
            data["service"], data["username"], data["password"], data["notes"]
        )
