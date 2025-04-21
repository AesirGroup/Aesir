from App.models import Recipe
from App.models import Ingredient
from App.models import RecipeIngredient
from App.database import db
from App.utils.validation import validate_name, validate_quantity
from .ingredient import get_ingredient_by_name
from sqlalchemy.sql import func, and_
from App.models import Inventory 


# CREATE
def create_recipe(user_id, name, description, ingredient_data_list):
    recipe = Recipe(user_id=user_id, name=name, description=description)
    db.session.add(recipe)
    db.session.flush()  # Ensure the recipe ID is available


    for item in ingredient_data_list:
        is_valid, error = validate_name(item.get("ingredient_name"))
        if not is_valid:
            raise ValueError(f"Ingredient name error: {error}")

        is_valid, error = validate_quantity(item.get("quantity"))
        if not is_valid:
            raise ValueError(f"Ingredient quantity error: {error}")
        
        is_valid, error = validate_name(item.get("unit"))
        if not is_valid:
            raise ValueError(f"Ingredient unit error: {error}")

        ingredient = get_ingredient_by_name(item["ingredient_name"])
        if ingredient:
            link = RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                quantity=item["quantity"],
                unit=item["unit"],
            )
            recipe.ingredients.append(link)

    db.session.commit()
    return recipe


# READ
def get_all_recipes(user):
    return Recipe.query.filter_by(user_id=user.id).all()


def get_recipe_by_id(user, recipe_id):
    return Recipe.query.filter_by(user_id=user.id, id=recipe_id).first()



# UPDATE
def update_recipe(
    user, recipe_id, name=None, description=None, ingredient_data_list=None
):
    recipe = get_recipe_by_id(user, recipe_id)
    if not recipe:
        return None

    # Validate name if provided
    if name is not None:
        is_valid, error = validate_name(name, max_length=100)
        if not is_valid:
            raise ValueError(error)
        recipe.name = name

    # Validate description if provided
    if description is not None:
        if len(description) > 4000:
            raise ValueError("Description must be 4000 characters or fewer.")
        recipe.description = description

    # Validate and update ingredients if provided
    if ingredient_data_list is not None:
        # Clear old links
        recipe.ingredients.clear()

        for item in ingredient_data_list:
            is_valid, error = validate_name(item.get("ingredient_name"))
            if not is_valid:
                raise ValueError(f"Ingredient name error: {error}")

            is_valid, error = validate_quantity(item.get("quantity"))
            if not is_valid:
                raise ValueError(f"Ingredient quantity error: {error}")
            
            is_valid, error = validate_name(item.get("unit"))
            if not is_valid:
                raise ValueError(f"Ingredient unit error: {error}")

            ingredient = get_ingredient_by_name(item["ingredient_name"])
            if ingredient:
                link = RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id,
                    quantity=item["quantity"],
                    unit=item["unit"],
                )
                recipe.ingredients.append(link)

    db.session.commit()
    return recipe


# DELETE
def delete_recipe(user, recipe_id):
    recipe = Recipe.query.filter_by(user_id=user.id, id=recipe_id).first()
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return True
    return False


def filter_recipes(user, filter_selection):

    # Query to find recipes where all required ingredients are available in sufficient quantity
    if filter_selection == "Possible":
        possible_recipes = (
            Recipe.query.join(RecipeIngredient, Recipe.id == RecipeIngredient.recipe_id)
            .outerjoin(
                Inventory,  # Join with the Inventory table
                and_(
                    Inventory.user_id == user.id,
                    Inventory.ingredient_id == RecipeIngredient.ingredient_id,
                ),
            )
            .group_by(Recipe.id)
            .having(
                func.count(RecipeIngredient.id)
                == func.sum(
                    and_(
                        Inventory.quantity >= RecipeIngredient.quantity,
                        Inventory.quantity.isnot(None),
                    )
                )
            )
            .all()
        )
        return possible_recipes

    # Query to find recipes where some ingredients are missing or insufficient
    elif filter_selection == "Missing Ingredients":
        impossible_recipes = (
            Recipe.query.join(RecipeIngredient, Recipe.id == RecipeIngredient.recipe_id)
            .outerjoin(
                Inventory,  # Join with the Inventory table
                and_(
                    Inventory.user_id == user.id,
                    Inventory.ingredient_id == RecipeIngredient.ingredient_id,
                ),
            )
            .group_by(Recipe.id)
            .having(
                func.count(RecipeIngredient.id)
                != func.sum(
                    and_(
                        Inventory.quantity >= RecipeIngredient.quantity,
                        Inventory.quantity.isnot(None),
                    )
                )
            )
            .all()
        )
        return impossible_recipes

    # Return all recipes if "All" is selected
    elif filter_selection == "All":
        return get_all_recipes(user)

    # Return an empty list for invalid filter selections
    return []
