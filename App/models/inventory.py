from App.database import db

class Inventory(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Float, default=0)
    unit = db.Column(db.String(50))
    user = db.relationship('User', back_populates='inventory_items')
    ingredient = db.relationship('Ingredient', back_populates='inventory_items')

    __table_args__ = (db.UniqueConstraint('user_id', 'ingredient_id', name='_user_ingredient_uc'),)

    def __init__(self, user_id, ingredient_id, quantity=0, unit=None):
        self.user_id = user_id
        self.ingredient_id = ingredient_id
        self.quantity = quantity
        self.unit = unit

    def get_json(self):
        return {'id': self.id, 'user_id': self.user_id, 'ingredient_id': self.ingredient_id, 'quantity': self.quantity, 'unit': self.unit}

    def __repr__(self):
        return f"<Inventory user={self.user_id!r} ingredient={self.ingredient_id} qty={self.quantity} {self.unit!r}>"