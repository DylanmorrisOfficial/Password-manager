import hashlib
import secrets
import json
import os
import getpass
import string


def generate_salt():
    # Generates a random salt using the secrets module
    return secrets.token_hex(16)


def hash_password(password, salt):
    password_bytes = password.encode()
    salt_bytes = salt.encode()

    # Hashes the password using PBKDF2 HMAC with SHA-256 and 100,000 iterations
    hashed = hashlib.pbkdf2_hmac("sha256", password_bytes, salt_bytes, 100000)
    return hashed.hex()


def save_auth_data(username, salt, hashed_password):
    # Saves the authentication data to a JSON file
    auth_data = {"username": username, "salt": salt, "hashed_password": hashed_password}

    with open("auth_data.json", "w") as file:
        json.dump(auth_data, file)


def create_master_password():
    # Prompts user to create a master password and saves the authentication data
    username = input("Create a username: ")
    password = confirm_password()

    salt = generate_salt()
    hashed_password = hash_password(password, salt)

    save_auth_data(username, salt, hashed_password)


def auth_exists():
    # Checks if the authentication data file exists
    return os.path.exists("auth_data.json")


def load_auth_data():
    # Loads the authentication data from the JSON file
    with open("auth_data.json", "r") as file:
        return json.load(file)


def verify_password(password):
    # loads the authentication data
    auth_data = load_auth_data()

    # Extracts salt and stored hash from the authentication data
    salt = auth_data["salt"]
    stored_hash = auth_data["hashed_password"]

    # Hashes the entered password with the stored salt and compares it to the stored hash
    entered_hash = hash_password(password, salt)

    return entered_hash == stored_hash


def verify_username(username):
    # Loads the authentication data and compares the entered username to the stored username
    auth_data = load_auth_data()
    stored_username = auth_data["username"]

    return username == stored_username


def confirm_password():
    # Prompts user to create a master password, confirming it by asking for the password twice and ensuring they match
    while True:
        password = getpass.getpass("Create a master password: ")

        # Validates the entered password against the defined requirements, if there are errors, prints them and prompts user to try again
        errors = validate_password(password)
        if errors:
            print("Password does not meet the requirements:")
            for error in errors:
                print(f" - {error}")
            continue

        confirm = getpass.getpass("Confirm password: ")

        # Checks if the entered password and confirmation match, if they do, returns the password, otherwise prompts user to try again
        if password == confirm:
            print("Password set!")
            return password
        else:
            print("Passwords do not match. Try again.\n")


def validate_password(password, min_length=8):
    # Validates the password against defined requirements and returns a list of error messages for any requirements that are not met
    errors = []

    if len(password) < min_length:
        errors.append("Must be at least 8 characters")

    if not any(c.islower() for c in password):
        errors.append("Must contain a lowercase letter")

    if not any(c.isupper() for c in password):
        errors.append("Must contain an uppercase letter")

    if not any(c.isdigit() for c in password):
        errors.append("Must contain a number")

    if not any(c in string.punctuation for c in password):
        errors.append("Must contain a symbol")

    return errors


def login():
    # Prompts user for master password and verifies it against stored authentication data
    username = input("\nEnter username: ")
    password = getpass.getpass("Enter password: ")

    # Verifies the entered username and password, returns True if both are correct, otherwise returns False
    if verify_username(username) and verify_password(password):
        return True
    else:
        return False
