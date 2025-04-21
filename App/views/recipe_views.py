from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    flash,
    redirect,
    url_for,
)
from flask_jwt_extended import (
    jwt_required,
    current_user,
)
from App.controllers.recipe import (
    create_recipe,
    get_all_recipes,
    get_recipe_by_id,
    update_recipe,
    delete_recipe,
    filter_recipes,
    delete_recipe,
)

from App.controllers.ingredient import get_all_ingredients, get_ingredient_by_name

from App.utils.validation import validate_name, validate_quantity, validate_unit, validate_description

recipe_views = Blueprint("recipe_views", __name__, template_folder="../templates")


@recipe_views.route("/add-recipe", methods=["GET"])
@jwt_required()
def add_recipe_page():
    ingredients = get_all_ingredients()
    ingredients_json = [ingredient.get_json() for ingredient in ingredients]
    return render_template(
        "add-recipe.html", ingredients=ingredients, ingredients_json=ingredients_json
    )


@recipe_views.route("/add-recipe", methods=["POST"])
@jwt_required()
def add_recipe():
    recipe_name = request.form.get("recipe_name")
    recipe_description = request.form.get("recipe_description")
    recipe_ingredients = request.form.getlist("ingredient_names[]")
    recipe_quantities = request.form.getlist("ingredient_quantities[]")
    recipe_units = request.form.getlist("ingredient_units[]")

    # Validate recipe name
    is_valid, error = validate_name(recipe_name, max_length=100)
    if not is_valid:
        flash(error, "error")
        return redirect(url_for("recipe_views.add_recipe_page"))
    
    # Validate recipe description
    is_valid, error = validate_description(recipe_description, max_length=4000)
    if not is_valid:
        flash(error, "error")
        return redirect(url_for("recipe_views.add_recipe_page"))

    # Validate ingredients
    ingredient_data_list = []
    for name, quantity, unit in zip(recipe_ingredients, recipe_quantities, recipe_units):
        is_valid, error = validate_name(name)
        if not is_valid:
            flash(f"Ingredient name error: {error}", "error")
            return redirect(url_for("recipe_views.add_recipe_page"))

        is_valid, error = validate_quantity(quantity)
        if not is_valid:
            flash(f"Ingredient quantity error: {error}", "error")
            return redirect(url_for("recipe_views.add_recipe_page"))
        
        is_valid, error = validate_unit(unit)
        if not is_valid:
            flash(f"Ingredient unit error: {error}", "error")
            return redirect(url_for("recipe_views.add_recipe_page"))
        
        ingredient = get_ingredient_by_name(name)
        if not ingredient:
            flash(f"Ingredient '{name}' does not exist.", "error")
            return redirect(url_for("recipe_views.add_recipe_page"))

        # Append each ingredient to the list
        ingredient_data_list.append(
            {"ingredient_name": name, "quantity": quantity, "unit": unit}
        )


    recipe = create_recipe(
        current_user.id, recipe_name, recipe_description, ingredient_data_list
    )

    if recipe:
        flash("Recipe created successfully!", "success")
        print(recipe)
    else:
        flash("Failed to create recipe.", "danger")
    return redirect(url_for("recipe_views.add_recipe_page"))


@recipe_views.route("/manage-recipes", methods=["GET"])
@jwt_required()
def recipes_page():
    recipes = get_all_recipes(current_user)
    ingredients = get_all_ingredients()
    ingredients_json = [ingredient.get_json() for ingredient in ingredients]
    return render_template("manage-recipes.html", recipes=recipes, ingredients_json=ingredients_json)


@recipe_views.route("/manage-recipes/delete", methods=["POST"])
@jwt_required()
def delete_recipe_action():
    recipe_id = request.form.get("delete-recipe-id")
    recipe = delete_recipe(current_user, recipe_id)

    if recipe:
        flash("Recipe deleted successfully!", "success")
    else:
        flash("Failed to delete recipe.", "error")
    return redirect(url_for("recipe_views.recipes_page"))


@recipe_views.route("/manage-recipes/edit", methods=["POST"])
@jwt_required()
def edit_recipe():
    recipe_id = request.form.get("recipe_id")
    recipe_name = request.form.get("recipe_name")
    recipe_description = request.form.get("recipe_description")
    recipe_ingredients = request.form.getlist("ingredient_names[]")
    recipe_quantities = request.form.getlist("ingredient_quantities[]")
    recipe_units = request.form.getlist("ingredient_units[]")

    # Validate recipe name
    is_valid, error = validate_name(recipe_name, max_length=100)
    if not is_valid:
        flash(error, "error")
        return redirect(url_for("recipe_views.recipes_page"))
    
    # Validate recipe description
    is_valid, error = validate_description(recipe_description, max_length=4000)
    if not is_valid:
        flash(error, "error")
        return redirect(url_for("recipe_views.recipes_page"))

    ingredient_data_list = []
    for name, quantity, unit in zip(recipe_ingredients, recipe_quantities, recipe_units):
        is_valid, error = validate_name(name)
        if not is_valid:
            flash(f"Ingredient name error: {error}", "error")
            return redirect(url_for("recipe_views.recipes_page"))

        is_valid, error = validate_quantity(quantity)
        if not is_valid:
            flash(f"Ingredient quantity error: {error}", "error")
            return redirect(url_for("recipe_views.recipes_page"))
        
        is_valid, error = validate_unit(unit)
        if not is_valid:
            flash(f"Ingredient unit error: {error}", "error")
            return redirect(url_for("recipe_views.recipes_page"))
        
        ingredient = get_ingredient_by_name(name)
        if not ingredient:
            flash(f"Ingredient '{name}' does not exist.", "error")
            return redirect(url_for("recipe_views.recipes_page"))

        ingredient_data_list.append(
            {"ingredient_name": name, "quantity": quantity, "unit": unit}
        )

    print(ingredient_data_list)
    recipe = update_recipe(
        current_user, recipe_id, recipe_name, recipe_description, ingredient_data_list
    )
    if recipe:
        flash("Recipe updated successfully!", "success")
    else:
        flash("Failed to update recipe.", "danger")
    return redirect(url_for("recipe_views.recipes_page"))


@recipe_views.route("/manage-recipes/filter", methods=["GET", "POST"])
@jwt_required()
def filter_recipes_action():
    filter_selection = request.form.get("filter-dropdown")
    print(filter_selection)
    recipes = filter_recipes(current_user, filter_selection)
    ingredients = get_all_ingredients()
    ingredients_json = [ingredient.get_json() for ingredient in ingredients]
    return render_template(
        "manage-recipes.html",
        recipes=recipes,
        ingredients_json=ingredients_json,
        selected_filter=filter_selection,
    )
