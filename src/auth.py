import hashlib
import secrets
import json
import os


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
    password = input("Create a master password: ")

    salt = generate_salt()
    hashed_password = hash_password(password, salt)

    save_auth_data(username, salt, hashed_password)
    print("Master password created successfully")
