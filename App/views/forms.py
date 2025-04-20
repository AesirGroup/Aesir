from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from App.models import User


class RegisterForm(FlaskForm):
    username = StringField(
        label="Username:", validators=[Length(min=2, max=30), DataRequired()]
    )
    password1 = PasswordField(
        label="Password:", validators=[Length(min=8, max=64), DataRequired()]
    )
    password2 = PasswordField(
        label="Confirm Password:", validators=[EqualTo("password1"), DataRequired()]
    )
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    username = StringField(label="Username:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label="Log in")
