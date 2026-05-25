import vault
import models


class Main:
    def __init__(self):
        self.vault = vault.Vault()

    def run_menu(self):
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
                break

            else:
                print("Invalid option")

    def add_entry(self):
        service = input("Enter service name: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        notes = input("Enter notes (optional): ")

        entry = models.PasswordEntry(service, username, password, notes)
        self.vault.add_entry(entry)
        print(f"Entry for {service} added successfully")

    def delete_entry(self):
        service = input("Enter service name: ")
        self.vault.remove_entry(service)
        print(f"Entry for {service} deleted successfully")

    def get_entry(self):
        service = input("Enter service name: ")
        entry = self.vault.get_entry(service)
        if entry:
            print(f"Service: {entry.service}")
            print(f"Username: {entry.username}")
            print(f"Password: {entry.password}")
            print(f"Notes: {entry.notes}")
        else:
            print("Entry not found")

    def list_entries(self):
        entries = self.vault.list_entries()
        if entries:
            for entry in entries:
                print(f"Service: {entry.service}, Username: {entry.username}")
        else:
            print("No entries found")


if __name__ == "__main__":
    main = Main()
    main.run_menu()
