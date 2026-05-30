import vault
import models
import auth


class Main:
    def __init__(self):
        self.vault = vault.Vault()
        self.vault.load_from_file()

    def run_menu(self):
        self.login()

        # Main loop for menu options
        while True:
            print("\n--- Menu ---")
            print("1. Add entry")
            print("2. Delete entry")
            print("3. Get entry")
            print("4. List entries")
            print("5. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                self.add_entry()

            elif choice == "2":
                self.delete_entry()

            elif choice == "3":
                self.get_entry()

            elif choice == "4":
                self.list_entries()

            elif choice == "5":
                print("Goodbye!")
                self.vault.save_to_file()
                break

            else:
                print("Invalid option")

    def add_entry(self):
        # Prompts user for entry details and add to vault
        service = self.get_non_empty("Enter service name: ")
        username = self.get_non_empty("Enter username: ")

        # Asks user if they want to use a random password or enter their own
        use_random_password = input("Use random password? (y/n): ").lower() == "y"
        if use_random_password:
            # Generates a random password using the password generator
            password = self.generate_random_password()
        else:
            # Prompts user for password and ensure it is not empty
            password = self.get_non_empty("Enter password: ")

        notes = input("Enter notes (optional): ")

        # Creates a new PasswordEntry and add it to the vault
        entry = models.PasswordEntry(service, username, password, notes)
        self.vault.add_entry(entry)
        print(f"Entry for {service} added successfully")

    def delete_entry(self):
        # Prompts user for service name and delete entry from vault
        service = input("Enter service name: ")
        self.vault.remove_entry(service)
        print(f"Entry for {service} deleted successfully")

    def get_entry(self):
        # Prompts user for service name and display entry details
        service = input("Enter service name: ")

        entry = self.vault.get_entry(service)
        if entry:
            self.print_entry(entry)
        else:
            # Prints message if entry not found
            print("Entry not found")

    def list_entries(self):
        # Lists all entries in the vault
        entries = self.vault.list_entries()
        if entries:
            for entry in entries:
                print(f"Service: {entry.service}, Username: {entry.username}")
        else:
            # Prints message if no entries found
            print("No entries found")

    # Helper method to get non-empty input from user
    def get_non_empty(self, prompt):
        while True:
            value = input(prompt).strip()
            if value == "":
                print("This field cannot be empty. Try again.")
            else:
                return value

    def print_entry(self, entry):
        # Prints entry details with password hidden, then prompts user if they want to reveal the password
        self._print(entry, revealed=False)

        choice = input("Reveal password? (y/n): ").lower()

        if choice == "y":
            self._print(entry, revealed=True)

        return

    def _print(self, entry, revealed):
        # Helper method to print entry details, showing password if revealed is True
        print("\n===================")
        print(entry.service.upper())
        print("-------------------")
        print(f"Username: {entry.username}")

        if revealed:
            print(f"Password: {entry.password}")
        else:
            print(f"Password: {'*' * len(entry.password)}")

        print(f"Notes: {entry.notes}")
        print("===================")

    def generate_random_password(self):
        # Generates a random password using the password generator
        from password_generator import generate_password

        return generate_password()

    def login(self):
        # Checks if authentication data exists, prompts user to create master password if not found
        if not auth.auth_exists():
            print("No master password found.")
            auth.create_master_password()
        else:
            print("Login required.")

        # keep looping until correct password
        while True:
            if auth.login():
                print("Login successful!")
                return  # exit function when success
            else:
                print("Incorrect username or password. Try again.\n")


# Main entry point
if __name__ == "__main__":
    main = Main()
    main.run_menu()
