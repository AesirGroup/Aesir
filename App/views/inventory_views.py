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
from App.controllers.ingredient import (
    get_ingredient_by_name,
)

from App.controllers.inventory import (
    add_inventory_item,
    update_inventory_item,
    delete_inventory_item,
)

from App.controllers.ingredient import get_all_ingredients

from App.utils.validation import (
    validate_name,
    validate_quantity,
    validate_unit,
)


from App.models import Inventory

inventory_views = Blueprint("inventory_views", __name__, template_folder="../templates")

"""
    Inventory management views
"""


@inventory_views.route("/inventory", methods=["GET"])
@jwt_required()
def inventory_page():
    inventory_items = Inventory.query.filter_by(user_id=current_user.id).all()
    ingredients = get_all_ingredients()
    ingredients_json = [ingredient.get_json() for ingredient in ingredients]
    return render_template("manage-inventory.html", inventory_items=inventory_items, ingredients_json=ingredients_json)


@inventory_views.route("/inventory/add", methods=["GET", "POST"])
@jwt_required()
def add_ingredient_action():
    ingredient_name = request.form.get("add_name")
    quantity = request.form.get("add_quantity")
    unit = request.form.get("add_unit")

    # Validate inputs
    is_valid, error = validate_name(ingredient_name)
    if not is_valid:
        flash(error, "error")
        return redirect(url_for("inventory_views.inventory_page"))
    is_valid, error = validate_quantity(quantity)
    if not is_valid:
        flash(error, "error")
        return redirect(url_for("inventory_views.inventory_page"))
    is_valid, error = validate_unit(unit)
    if not is_valid:
        flash(error, "error")
        return redirect(url_for("inventory_views.inventory_page"))

    ingredient = get_ingredient_by_name(ingredient_name)
    if not ingredient:
        flash(f"Ingredient {ingredient_name} does not exist!", "error")
        return redirect(url_for("inventory_views.inventory_page"))
    new_ingredient = add_inventory_item(current_user.id, ingredient.id, quantity, unit)
    if not new_ingredient:
        flash(f"Ingredient {ingredient_name} already exists!", "error")
    else:
        flash(f"Ingredient {ingredient_name} added successfully!", "success")
    return redirect(url_for("inventory_views.inventory_page"))


@inventory_views.route("/inventory/edit", methods=["GET", "POST"])
@jwt_required()
def edit_ingredient_action():
    ingredient_id = request.form.get("inventory_id")
    ingredient_name = request.form.get("inventory_name")
    quantity = request.form.get("quantity")
    unit = request.form.get("unit")

    # Validate inputs
    is_valid, error = validate_name(ingredient_name)
    if not is_valid:
        flash(error, "error")
        return redirect(url_for("inventory_views.inventory_page"))
    is_valid, error = validate_quantity(quantity)
    if not is_valid:
        flash(error, "error")
        return redirect(url_for("inventory_views.inventory_page"))
    is_valid, error = validate_unit(unit)
    if not is_valid:
        flash(error, "error")
        return redirect(url_for("inventory_views.inventory_page"))

    updated_ingredient = update_inventory_item(
        current_user.id, ingredient_id, quantity, unit
    )

    if not updated_ingredient:
        flash(f"Ingredient update unsuccessful.", "error")
    else:
        flash(f"Ingredient {ingredient_name} updated successfully!", "success")
    return redirect(url_for("inventory_views.inventory_page"))


@inventory_views.route("/inventory/delete", methods=["GET", "POST"])
@jwt_required()
def delete_ingredient_action():
    ingredient_id = request.form.get("delete_inventory_id")
    print(ingredient_id)
    deleted_ingredient = delete_inventory_item(current_user.id, ingredient_id)
    if deleted_ingredient:
        flash(f"Ingredient deleted successfully!", "success")
    else:
        flash(f"Ingredient deletion unsuccessful.", "error")
    return redirect(url_for("inventory_views.inventory_page"))
