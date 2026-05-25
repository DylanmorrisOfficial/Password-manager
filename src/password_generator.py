import secrets
import string


def generate_password(length=16):
    # Ensure the password is of a reasonable length
    if length < 8:
        raise ValueError("Password length should be at least 8 characters.")

    alphabet = string.ascii_letters + string.digits + string.punctuation

    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))

        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in string.punctuation for c in password)

        if has_lower and has_upper and has_digit and has_symbol:
            return password
