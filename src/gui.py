import tkinter as tk
from tkinter import messagebox
import auth
import models
import vault
import ttkbootstrap as ttk


class PasswordManagerGUI:
    def __init__(self):
        # Initializes the main window of the application with a dark theme, sets the title and size, and initializes variables for the current user and vault. It also defines font styles for the title, headings, and text in the application.
        self.window = ttk.Window(themename="darkly")
        self.window.title("Password Manager")
        self.window.geometry("600x400")

        self.current_user = None
        self.current_vault = None

        # Defines font styles for the title, headings, and text in the application
        self.TITLE_FONT = ("Segoe UI", 24, "bold")
        self.HEADING_FONT = ("Segoe UI", 14)
        self.TEXT_FONT = ("Segoe UI", 11)

        # Shows the login screen when the application starts
        self.show_login_screen()

        self.vault = None

    def clear_screen(self):
        # Clears all widgets from the current screen to prepare for the next screen
        for widget in self.window.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        # Clears the screen and sets up the login screen with entry fields for username and password, a message label for feedback, and buttons for login and account creation
        self.clear_screen()

        self.title = ttk.Label(
            self.window, text="Password Manager", font=self.TITLE_FONT
        )
        self.title.pack(pady=20)

        ttk.Label(self.window, text="Username", font=self.HEADING_FONT).pack()
        self.username_entry = ttk.Entry(self.window, font=self.TEXT_FONT)
        self.username_entry.pack(pady=5)

        ttk.Label(self.window, text="Password", font=self.HEADING_FONT).pack()
        self.password_entry = ttk.Entry(self.window, show="*", font=self.TEXT_FONT)
        self.password_entry.pack(pady=5)

        self.message_label = ttk.Label(self.window, text="", font=self.TEXT_FONT)
        self.message_label.pack(pady=5)

        self.login_button = ttk.Button(self.window, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        # Button to navigate to the account creation screen
        self.create_account_button = ttk.Button(
            self.window, text="Create Account", command=self.create_account
        )
        self.create_account_button.pack(pady=10)

    def login(self):
        # Retrieves username and password from the entry fields and attempts to log in using the auth module, if login is successful, shows the vault screen, otherwise displays a login failed message
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.current_user = auth.login(username, password)

        if self.current_user:
            # Clears the screen, initializes the vault for the logged-in user, loads the vault from file, and shows the vault screen
            self.clear_screen()
            self.vault = vault.Vault(self.current_user)
            self.vault.load_from_file()
            self.show_vault_screen()
        else:
            # Displays login failed message
            self.message_label.config(text="Login failed")

    def show_vault_screen(self):
        # Updates the title to welcome the logged-in user
        self.clear_screen()

        self.title = ttk.Label(
            self.window, text=f"Welcome {self.current_user}", font=self.TITLE_FONT
        )
        self.title.pack(pady=20)

        self.add_entry_button = ttk.Button(
            self.window, text="Add Entry", command=self.add_entry
        )
        self.add_entry_button.pack(pady=10)

        self.delete_entry_button = ttk.Button(
            self.window, text="Delete Entry", command=self.delete_entry
        )
        self.delete_entry_button.pack(pady=10)

        self.get_entry_button = ttk.Button(
            self.window, text="Get Entry", command=self.get_entry
        )
        self.get_entry_button.pack(pady=10)

        self.list_entries_button = ttk.Button(
            self.window, text="List Entries", command=self.list_entries
        )
        self.list_entries_button.pack(pady=10)

        self.logout_button = ttk.Button(self.window, text="Logout", command=self.logout)
        self.logout_button.pack(pady=10)

    def add_entry(self):
        # Clears the screen and sets up the add entry screen with entry fields for service name, username, password, and notes, a checkbox to generate a random password, and a button to save the new entry
        self.clear_screen()

        ttk.Label(self.window, text="Service Name", font=self.HEADING_FONT).pack()
        self.service_entry = ttk.Entry(self.window, font=self.TEXT_FONT)
        self.service_entry.pack(pady=5)

        ttk.Label(self.window, text="Username", font=self.HEADING_FONT).pack()
        self.username_entry = ttk.Entry(self.window, font=self.TEXT_FONT)
        self.username_entry.pack(pady=5)

        self.generate_var = tk.BooleanVar()

        ttk.Label(self.window, text="Password", font=self.HEADING_FONT).pack()
        self.password_entry = ttk.Entry(self.window, show="*", font=self.TEXT_FONT)
        self.password_entry.pack(pady=5)

        ttk.Checkbutton(
            self.window, text="Generate Random Password", variable=self.generate_var
        ).pack(pady=5)

        ttk.Label(self.window, text="Notes", font=self.HEADING_FONT).pack()
        self.notes_text = tk.Text(self.window, height=4, width=30, font=self.TEXT_FONT)
        self.notes_text.pack(pady=5)

        ttk.Button(self.window, text="Save Entry", command=self.save_entry).pack(
            pady=10
        )

        ttk.Button(
            self.window, text="Return to Vault", command=self.show_vault_screen
        ).pack(pady=10)

    def save_entry(self):
        # Retrieves service name, username, password, and notes from the entry fields, checks if service and username are provided, generates a random password if the checkbox is selected, creates a new PasswordEntry object, adds it to the vault, and displays a success message
        service = self.service_entry.get().strip()
        username = self.username_entry.get().strip()

        if not service:
            # Displays an error message if the service name is not provided and prompts user to try again
            messagebox.showerror("Error", "Service required")
            return

        if not username:
            # Displays an error message if the username is not provided and prompts user to try again
            messagebox.showerror("Error", "Username required")
            return

        if self.generate_var.get():
            # Generates a random password if the checkbox is selected
            password = self.generate_random_password()
        else:
            # Retrieves the password from the entry field and strips any leading/trailing whitespace
            password = self.password_entry.get().strip()

        # Retrieves notes from the text field and strips any leading/trailing whitespace
        notes = self.notes_text.get("1.0", tk.END).strip()

        # Creates a new PasswordEntry object with the provided service, username, password, and notes, adds it to the vault, and displays a success message
        entry = models.PasswordEntry(service, username, password, notes)

        # Adds the new entry to the vault and displays a success message
        self.vault.add_entry(entry)

        messagebox.showinfo("Success", f"Entry for {service} added")

    def generate_random_password(self):
        # Generates a random password using the password generator
        from password_generator import generate_password

        return generate_password()

    def delete_entry(self):
        # Clears the screen and sets up the delete entry screen with an entry field for service name, a button to confirm deletion, and a button to return to the vault screen
        self.clear_screen()

        ttk.Label(self.window, text="Service Name", font=self.HEADING_FONT).pack(pady=5)

        self.service_entry = ttk.Entry(self.window, font=self.TEXT_FONT)
        self.service_entry.pack(pady=5)

        ttk.Button(self.window, text="Delete Entry", command=self.confirm_delete).pack(
            pady=10
        )

        ttk.Button(
            self.window, text="Return to Vault", command=self.show_vault_screen
        ).pack(pady=10)

    def confirm_delete(self):
        # Retrieves the service name from the entry field, checks if it is provided, removes the entry from the vault, displays a success message, and returns to the vault screen
        service = self.service_entry.get().strip()

        if not service:
            # Displays an error message if the service name is not provided and prompts user to try again
            messagebox.showerror("Error", "Please enter a service name")
            return

        # Removes the entry for the specified service from the vault and displays a success message
        self.vault.remove_entry(service)

        messagebox.showinfo("Success", f"Entry for {service} removed")

    def get_entry(self):
        # Clears the screen and sets up the get entry screen with an entry field for service name, a button to retrieve the entry, and a button to return to the vault screen
        self.clear_screen()

        ttk.Label(self.window, text="Service Name", font=self.HEADING_FONT).pack(pady=5)
        self.service_entry = ttk.Entry(self.window, font=self.TEXT_FONT)
        self.service_entry.pack(pady=5)

        ttk.Button(self.window, text="Get Entry", command=self.show_entry).pack(pady=10)

        ttk.Button(
            self.window, text="Return to Vault", command=self.show_vault_screen
        ).pack(pady=10)

    def show_entry(self):
        # Retrieves the service name from the entry field, checks if it is provided, retrieves the entry from the vault, and displays the entry details or an error message if the entry is not found
        service = self.service_entry.get().strip()

        if not service:
            # Displays an error message if the service name is not provided and prompts user to try again
            messagebox.showerror("Error", "Please enter a service name")
            return

        # Retrieves the entry for the specified service from the vault
        entry = self.vault.get_entry(service)

        if not entry:
            # Displays an error message if the entry is not found and prompts user to try again
            messagebox.showerror("Error", "Entry not found")
            return

        # Displays the entry details using the print_entry method
        self.print_entry(entry)

    def print_entry(self, entry):
        # Clears the screen and displays the entry details, including service name, username, password (hidden by default), and notes, with a button to toggle password visibility and a button to return to the vault screen
        self.clear_screen()

        ttk.Label(self.window, text=entry.service.upper(), font=self.HEADING_FONT).pack(
            pady=5
        )

        ttk.Label(
            self.window, text=f"Username: {entry.username}", font=self.TEXT_FONT
        ).pack(pady=5)

        self.password_visible = False
        self.entry = entry

        self.password_label = ttk.Label(
            self.window,
            text=f"Password: {'*' * len(entry.password)}",
            font=self.TEXT_FONT,
        )
        self.password_label.pack(pady=5)

        ttk.Label(self.window, text=f"Notes: {entry.notes}", font=self.TEXT_FONT).pack(
            pady=5
        )

        self.password_button = ttk.Button(
            self.window, text="Show Password", command=self.toggle_password
        )
        self.password_button.pack(pady=10)

        ttk.Button(
            self.window, text="Return to Vault", command=self.show_vault_screen
        ).pack(pady=10)

    def toggle_password(self):
        # Toggles the visibility of the password in the entry details, updating the password label and button text accordingly
        if self.password_visible:
            # Hides the password
            self.password_label.config(
                text=f"Password: {'*' * len(self.entry.password)}"
            )
            self.password_button.config(text="Show Password")
            self.password_visible = False

        else:
            # Shows the password
            self.password_label.config(text=f"Password: {self.entry.password}")
            self.password_button.config(text="Hide Password")
            self.password_visible = True

    def list_entries(self):
        # Clears the screen and displays a list of all entries in the vault, showing service names and usernames, with a button to return to the vault screen
        self.clear_screen()

        entries = self.vault.list_entries()

        if entries:
            # Displays each entry's service name and username in the list
            for entry in entries:
                ttk.Label(self.window, text=f"Service: {entry.service}").pack(pady=5)

                ttk.Label(self.window, text=f"Username: {entry.username}").pack(pady=5)

                ttk.Label(self.window, text="────────────────────").pack(pady=5)
        else:
            # Displays a message if no entries are found in the vault
            ttk.Label(self.window, text="No entries found").pack(pady=5)

        ttk.Button(
            self.window, text="Return to Vault", command=self.show_vault_screen
        ).pack(pady=10)

    def logout(self):
        # Logs out the current user, clears the screen, and shows the login screen
        self.current_user = None
        self.vault.save_to_file()
        self.clear_screen()
        self.show_login_screen()

    def create_account(self):
        # Clears the screen and sets up the account creation screen with entry fields for username, password, and password confirmation, a message label for feedback, and a button to save the new account
        self.clear_screen()

        self.title = ttk.Label(
            self.window, text="Create Account", font=self.HEADING_FONT
        )
        self.title.pack(pady=20)

        ttk.Label(self.window, text="Username", font=self.HEADING_FONT).pack(pady=5)
        self.username_entry = ttk.Entry(self.window, font=self.TEXT_FONT)
        self.username_entry.pack(pady=5)

        ttk.Label(self.window, text="Password", font=self.HEADING_FONT).pack(pady=5)
        self.password_entry = ttk.Entry(self.window, show="*", font=self.TEXT_FONT)
        self.password_entry.pack(pady=5)

        ttk.Label(self.window, text="Confirm Password", font=self.HEADING_FONT).pack(
            pady=5
        )
        self.confirm_password_entry = ttk.Entry(
            self.window, show="*", font=self.TEXT_FONT
        )
        self.confirm_password_entry.pack(pady=5)

        self.create_message_label = ttk.Label(self.window, text="", font=self.TEXT_FONT)
        self.create_message_label.pack(pady=5)

        # Button to save the new account and navigate back to the login screen if account creation is successful
        self.create_account_button = ttk.Button(
            self.window,
            text="Create Account",
            command=lambda: self.save_account(),
        )
        self.create_account_button.pack(pady=10)

        ttk.Button(
            self.window, text="Return to Login", command=self.show_login_screen
        ).pack(pady=10)

    def save_account(
        self,
    ):
        # Retrieves username, password, and password confirmation from the entry fields, checks if the passwords match, if they do, attempts to register the new account using the auth module, if registration is successful, shows the login screen, otherwise displays error messages
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_password_entry.get()

        if password != confirm:
            # Displays message if passwords do not match and prompts user to try again
            self.create_message_label.config(text="Passwords do not match")
            return

        success, message = auth.register(username, password)

        if success:
            # Clears the screen and shows the login screen after successful account creation
            self.show_login_screen()
        else:
            # Displays error messages if account creation failed and prompts user to try again
            self.create_message_label.config(text=message)


# Main entry point to start the application
app = PasswordManagerGUI()
app.window.mainloop()
