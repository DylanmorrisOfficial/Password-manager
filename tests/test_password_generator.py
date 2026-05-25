import sys
import os
import pytest
import string

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from password_generator import generate_password


def test_default_length():
    password = generate_password()
    assert len(password) == 16


def test_custom_length():
    password = generate_password(20)
    assert len(password) == 20


def test_minimum_length():
    password = generate_password(8)
    assert len(password) == 8


def test_too_short_raises_error():
    with pytest.raises(ValueError):
        generate_password(4)


def test_contains_uppercase():
    password = generate_password(20)
    assert any(char.isupper() for char in password)


def test_contains_lowercase():
    password = generate_password(20)
    assert any(char.islower() for char in password)


def test_contains_digits():
    password = generate_password(20)
    assert any(char.isdigit() for char in password)


def test_contains_punctuation():
    password = generate_password(20)
    assert any(char in string.punctuation for char in password)


def test_passwords_are_random():
    password1 = generate_password()
    password2 = generate_password()

    assert password1 != password2
