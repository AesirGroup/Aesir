from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    flash,
    send_from_directory,
    flash,
    redirect,
    url_for,
)
from flask_jwt_extended import (
    jwt_required,
    current_user,
    unset_jwt_cookies,
    set_access_cookies,
)

from .index_views import index_views

from App.controllers import login, register

from App.utils.validation import (
    validate_username,
    validate_password,
    compare_passwords,
)

auth_views = Blueprint("auth_views", __name__, template_folder="../templates")


"""
Page/Action Routes
"""


@auth_views.route("/login", methods=["GET", "POST"])
def login_page():
    errorsDict = {
        "username_error": None,
        "password_error": None,
    }

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Validate inputs
        is_valid, error = validate_username(username)
        if not is_valid:
            errorsDict["username_error"] = error
        is_valid, error = validate_password(password)
        if not is_valid:
            errorsDict["password_error"] = error

        if any(errorsDict.values()):
            return render_template("login.html", title="Login", errorsDict=errorsDict)

        # Proceed with login if no errors
        token = login(username, password)
        if token:
            response = redirect(url_for("index_views.index_page"))
            set_access_cookies(response, token)
            flash("Login Successful", category="success")
            return response
        else:
            flash("Invalid login credentials. Please try again.", category="error")
    return render_template("login.html", title="Login", errorsDict=errorsDict)


@auth_views.route("/register", methods=["GET", "POST"])
def register_page():
    errorsDict = {
        "username_error": None,
        "password1_error": None,
        "password2_error": None,
    }

    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Validate inputs
        is_valid, error = validate_username(username)
        if not is_valid:
            errorsDict["username_error"] = error

        is_valid, error = validate_password(password1)
        if not is_valid:
            errorsDict["password1_error"] = error

        is_valid, error = validate_password(password2)
        if not is_valid:
            errorsDict["password2_error"] = error

        is_valid, error = compare_passwords(password1, password2)
        if not is_valid:
            errorsDict["password2_error"] = error

        if any(errorsDict.values()):
            return render_template(
                "register.html", title="Register", errorsDict=errorsDict
            )

        # Proceed with registration if no errors
        user = register(username, password1)
        if user:
            flash("Registration Successful", category="success")
            return redirect(url_for("auth_views.login_page"))
        else:
            flash("Registration failed. Please try again.", category="error")

    return render_template("register.html", title="Register", errorsDict=errorsDict)


@auth_views.route("/logout", methods=["GET"])
def logout_action():
    response = redirect(url_for("index_views.index_page"))
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response
