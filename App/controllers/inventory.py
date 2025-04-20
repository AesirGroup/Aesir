from App.models import Inventory
from App.database import db

def add_inventory_item(user_id, ingredient_id, quantity, unit):
    # Check if the user already has this ingredient in their inventory
    existing_item = Inventory.query.filter_by(user_id=user_id, ingredient_id=ingredient_id).first()
    if existing_item:
        return None  # Item already exists in inventory
    inventory_item = Inventory(user_id=user_id, ingredient_id=ingredient_id, quantity=quantity, unit=unit)
    db.session.add(inventory_item)
    db.session.commit()
    return inventory_item

def get_inventory_items(user_id):
    return Inventory.query.filter_by(user_id=user_id).all()

def get_inventory_item(user_id, inventory_item_id):
    return Inventory.query.filter_by(user_id=user_id, id=inventory_item_id).first()

def update_inventory_item(user_id, inventory_item_id, quantity=None, unit=None):
    inventory_item = get_inventory_item(user_id, inventory_item_id)
    if not inventory_item:
        return None

    if quantity is not None:
        inventory_item.quantity = quantity

    if unit is not None:
        inventory_item.unit = unit

    db.session.commit()
    return inventory_item

def delete_inventory_item(user_id, inventory_item_id):
    inventory_item = get_inventory_item(user_id, inventory_item_id)
    if inventory_item:
        db.session.delete(inventory_item)
        db.session.commit()
        return True
    return False