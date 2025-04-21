import json
import os
from .user import create_user
from .ingredient import create_ingredient
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()

    # Create users
    bob = create_user("bob", "bobpass")
    alice = create_user("alice", "alicepass")

    # Load ingredients from extractedIngredients.json
    file_path = os.path.join(os.path.dirname(__file__), "extractedIngredients.json")
    with open(file_path, "r") as file:
        ingredients_data = json.load(file)

    # Create ingredients
    for ingredient in ingredients_data:
        name = ingredient.get("name")
        unit = ingredient.get("unit", "N/A")  # Default to "N/A" if unit is missing
        create_ingredient(name, unit)

    db.session.commit()
