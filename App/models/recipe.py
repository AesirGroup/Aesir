from App.database import db

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    user = db.relationship('User', back_populates='recipes')
    ingredients = db.relationship('RecipeIngredient', back_populates='recipe', cascade='all, delete-orphan')

    def __init__(self, user_id, name, description=None):
        self.user_id = user_id
        self.name = name
        self.description = description

    def get_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'ingredients': [
                {
                    'id': assoc.id,
                    'ingredient_id': assoc.ingredient_id,
                    'name': assoc.ingredient.name,
                    'quantity': assoc.quantity,
                    'unit': assoc.unit
                } for assoc in self.ingredients
            ]
        }

    def __repr__(self):
        return f"<Recipe {self.name!r}>"
