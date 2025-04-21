import re


def validate_name(name, max_length=100):
    if not name or len(name) > max_length:
        return False, f"Name must be between 1 and {max_length} characters."
    if not re.match("^[a-zA-Z0-9, \-/()%]+$", name):
        return (
            False,
            "Name can only contain letters, numbers, spaces, commas, dashes (-), slashes (/), percent signs (%), and brackets ().",
        )
    return True, None


def validate_username(username, min_length=3, max_length=20):
    if not username or len(username) < min_length or len(username) > max_length:
        return (
            False,
            f"Username must be between {min_length} and {max_length} characters.",
        )
    if not re.match("^[a-zA-Z0-9_]+$", username):
        return (
            False,
            "Username can only contain letters, numbers, and underscores.",
        )
    return True, None


def validate_password(password, min_length=7, max_length=64):
    if not password or len(password) < min_length or len(password) > max_length:
        return (
            False,
            f"Password must be between {min_length} and {max_length} characters.",
        )
    if not re.match("^[a-zA-Z0-9!@#$%^&*()_+={}:;\"'<>?,./\\|`~]+$", password):
        return (
            False,
            "Password can only contain letters, numbers, and special characters.",
        )
    return True, None


def compare_passwords(password1, password2):
    if password1 != password2:
        return False, "Passwords do not match."
    return True, None


def validate_quantity(quantity):
    try:
        quantity = float(quantity)
        if quantity <= 0:
            return False, "Quantity must be greater than 0."
        return True, None
    except ValueError:
        return False, "Quantity must be a valid number."


def validate_unit(unit, max_length=20):
    if not unit or len(unit) > max_length:
        return False, f"Unit must be between 1 and {max_length} characters."
    return True, None


def validate_description(description, max_length=4000):
    if not description or len(description) > max_length:
        return False, f"Description must be between 1 and {max_length} characters."
    return True, None