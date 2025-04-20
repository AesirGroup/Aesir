from App.database import db

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    inventory_items = db.relationship('Inventory', back_populates='ingredient', cascade='all, delete-orphan')
    recipe_links = db.relationship('RecipeIngredient', back_populates='ingredient', cascade='all, delete-orphan')

    def __init__(self, name, unit):
        self.name = name
        self.unit = unit

    def get_json(self):
        return {'id': self.id, 'name': self.name, 'unit': self.unit}

    def __repr__(self):
        return f"<Ingredient {self.name!r}>"
