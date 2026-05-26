import vault
import models


class Main:
    def __init__(self):
        self.vault = vault.Vault()
        self.vault.load_from_file()

    def run_menu(self):
        # Main loop for menu options
        while True:
            print("--- Menu ---")
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
        # Prompt user for entry details and add to vault
        service = self.get_non_empty("Enter service name: ")
        username = self.get_non_empty("Enter username: ")

        # Ask user if they want to use a random password or enter their own
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
        # Prompt user for service name and delete entry from vault
        service = input("Enter service name: ")
        self.vault.remove_entry(service)
        print(f"Entry for {service} deleted successfully")

    def get_entry(self):
        # Prompt user for service name and display entry details
        service = input("Enter service name: ")

        entry = self.vault.get_entry(service)
        if entry:
            self.print_entry(entry)
        else:
            # Print message if entry not found
            print("Entry not found")

    def list_entries(self):
        # List all entries in the vault
        entries = self.vault.list_entries()
        if entries:
            for entry in entries:
                print(f"Service: {entry.service}, Username: {entry.username}")
        else:
            # Print message if no entries found
            print("No entries found")

    # Helper method to get non-empty input from user
    def get_non_empty(self, prompt):
        while True:
            value = input(prompt).strip()
            if value == "":
                print("This field cannot be empty. Try again.")
            else:
                return value

    # Prints entries in a formatted way
    def print_entry(self, entry):
        print("\n===================")
        print(entry.service.upper())
        print("-------------------")
        print(f"Username: {entry.username}")
        print(f"Password: {entry.password}")
        print(f"Notes: {entry.notes}")
        print("===================")

    def generate_random_password(self):
        # Generate a random password using the password generator
        from password_generator import generate_password

        return generate_password()


# Main entry point
if __name__ == "__main__":
    main = Main()
    main.run_menu()
