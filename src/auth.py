import hashlib
import secrets
import json
import os
import getpass
import string

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

AUTH_FILE = os.path.join(DATA_DIR, "auth_data.json")


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
    # Loads existing authentication data, updates it with the new username, salt, and hashed password, and saves it back to the JSON file
    auth_data = load_auth_data()

    auth_data[username] = {"salt": salt, "hashed_password": hashed_password}

    with open(AUTH_FILE, "w") as file:
        json.dump(auth_data, file)


def create_master_password():
    # Prompts user to create a master password and saves the authentication data
    username = input("Create a username: ")

    auth_data = load_auth_data()

    if username in auth_data:
        print("Username already exists. Please choose a different username.")
        return

    password = confirm_password()

    salt = generate_salt()
    hashed_password = hash_password(password, salt)

    save_auth_data(username, salt, hashed_password)


def auth_exists():
    # Checks if the authentication data file exists
    return os.path.exists(AUTH_FILE)


def load_auth_data():
    # Loads the authentication data from the JSON file, returns an empty dictionary if file not found
    if not os.path.exists(AUTH_FILE):
        return {}

    with open(AUTH_FILE, "r") as file:
        return json.load(file)


def verify_password(username, password):
    # Loads the authentication data, checks if the username exists, and verifies the entered password by hashing it with the stored salt and comparing it to the stored hash
    auth_data = load_auth_data()

    if username not in auth_data:
        return False

    # Extracts salt and stored hash from the authentication data for the given username
    salt = auth_data[username]["salt"]
    stored_hash = auth_data[username]["hashed_password"]

    # Hashes the entered password with the stored salt and compares it to the stored hash
    entered_hash = hash_password(password, salt)

    return entered_hash == stored_hash


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


def register(username, password):
    # Registers a new user by checking if the username already exists, validating the password, and saving the authentication data if registration is successful, otherwise returns an error message
    auth_data = load_auth_data()

    # Checks if the entered username already exists in the authentication data, if it does, returns an error message
    if username in auth_data:
        return False, "Username already exists"

    errors = validate_password(password)

    # Validates the entered password against the defined requirements, if there are errors, returns a message containing the errors
    if errors:
        return False, "\n".join(errors)

    # Generates a salt, hashes the password, saves the authentication data, and returns a success message
    salt = generate_salt()
    hashed_password = hash_password(password, salt)

    save_auth_data(username, salt, hashed_password)

    return True, ""


def login(username, password):
    # Verifies the entered username and password, if verification is successful, returns the username, otherwise returns None
    if verify_password(username, password):
        return username

    return None
