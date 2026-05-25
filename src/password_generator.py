import secrets
import string


def generate_password(length=16):
    # Ensure the password is of a reasonable length
    if length < 8:
        raise ValueError("Password length should be at least 8 characters.")

    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(alphabet) for _ in range(length))

    if (
        password.count(string.ascii_lowercase) == 0
        or password.count(string.ascii_uppercase) == 0
        or password.count(string.digits) == 0
        or password.count(string.punctuation) == 0
    ):
        # Generate a new password the password does not contain all character types
        return generate_password(length)

    return password
