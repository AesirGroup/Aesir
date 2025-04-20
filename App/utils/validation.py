import re

# Added


def validate_name(name, max_length=100):
    if not name or len(name) > max_length:
        return False, f"Name must be between 1 and {max_length} characters."
    if not re.match("^[a-zA-Z0-9, \-/()%]+$", name):
        return False, "Name can only contain letters, numbers, spaces, commas, dashes (-), slashes (/), percent signs (%), and brackets ()."
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
