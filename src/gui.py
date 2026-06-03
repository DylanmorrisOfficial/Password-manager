import tkinter as tk
from tkinter import ttk
import auth


def login():
    # Retrieves username and password from the entry fields and attempts to log in using the auth module, if login is successful, shows the vault screen, otherwise displays a login failed message
    username = username_entry.get()
    password = password_entry.get()

    logged_in_user = auth.login(username, password)

    if logged_in_user:
        # Displays login successful message, destroys login widgets, and shows the vault screen
        message_label.config(text="Login successful")
        destroy_login_widgets()
        show_vault_screen(logged_in_user)
    else:
        # Displays login failed message
        message_label.config(text="Login failed")


def destroy_login_widgets():
    # Destroys all login-related widgets to clear the screen for the vault interface
    username_label.destroy()
    username_entry.destroy()
    password_label.destroy()
    password_entry.destroy()
    login_button.destroy()
    message_label.destroy()


def show_vault_screen(username):
    # Updates the title to welcome the logged-in user
    title.config(text=f"Welcome {username}")


# Main application window setup
window = tk.Tk()

window.title("Password Manager")
window.geometry("600x400")

title = tk.Label(window, text="Password Manager", font=("Arial", 24, "bold"))

title.pack(pady=20)

username_label = tk.Label(window, text="Username")

username_label.pack()

username_entry = tk.Entry(window)

username_entry.pack()

password_label = tk.Label(window, text="Password")

password_label.pack()

password_entry = tk.Entry(window, show="*")

password_entry.pack()

login_button = ttk.Button(window, text="Login", command=login)

login_button.pack(pady=10)

message_label = tk.Label(window, text="")
message_label.pack(pady=5)

window.mainloop()
