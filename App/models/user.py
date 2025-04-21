from werkzeug.security import check_password_hash, generate_password_hash
from uuid import uuid4
from App.database import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(), primary_key=True, default=lambda: str(uuid4()))
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    inventory_items = db.relationship(
        "Inventory", back_populates="user", cascade="all, delete-orphan"
    )

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_json(self):
        return {"id": self.id, "username": self.username}

    def __repr__(self):
        return f"<User {self.username!r}>"
