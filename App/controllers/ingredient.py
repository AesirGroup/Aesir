from App.models import Ingredient
from App.database import db
from App.utils.validation import validate_name, validate_quantity, validate_unit


def create_ingredient(name, unit):
    existing = get_ingredient_by_name(name)
    if existing:
        raise ValueError("Ingredient already exists.")
    ingredient = Ingredient(name=name, unit=unit)
    db.session.add(ingredient)
    db.session.commit()
    return ingredient


def get_all_ingredients():
    return Ingredient.query.all()

def get_ingredient_by_id(ingredient_id):
    return Ingredient.query.filter_by(id=ingredient_id).first()

def get_ingredient_by_name(name):
    return Ingredient.query.filter_by(name=name).first()


def update_ingredient(ingredient_id, name=None, unit=None):
    ingredient = get_ingredient_by_id(ingredient_id)
    if not ingredient:
        return None

    # Validate name if provided
    if name is not None:
        is_valid, error = validate_name(name)
        if not is_valid:
            raise ValueError(error)
        ingredient.name = name

    # Validate unit if provided
    if unit is not None:
        is_valid, error = validate_unit(unit)
        if not is_valid:
            raise ValueError(error)
        ingredient.unit = unit

    db.session.commit()
    return ingredient


def delete_ingredient(ingredient_id):
    ingredient = get_ingredient_by_id(ingredient_id)
    if ingredient:
        db.session.delete(ingredient)
        db.session.commit()
        return True
    return False
