from App.database import db

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Float, default=0)
    unit = db.Column(db.String(50))
    recipe = db.relationship('Recipe', back_populates='ingredients')
    ingredient = db.relationship('Ingredient', back_populates='recipe_links')

    __table_args__ = (db.UniqueConstraint('recipe_id', 'ingredient_id', name='_recipe_ingredient_uc'),)

    def __init__(self, recipe_id, ingredient_id, quantity=0, unit=None):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.quantity = quantity
        self.unit = unit

    def get_json(self):
        return {'id': self.id, 'recipe_id': self.recipe_id, 'ingredient_id': self.ingredient_id, 'quantity': self.quantity, 'unit': self.unit}

    def __repr__(self):
        return f"<RecipeIngredient recipe={self.recipe_id} ingredient={self.ingredient_id} qty={self.quantity} {self.unit!r}>"