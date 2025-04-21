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

auth_views = Blueprint("auth_views", __name__, template_folder="../templates")


"""
Page/Action Routes
"""


@auth_views.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "" or password == "":
            flash("Please enter both username and password.", category="error")
            return render_template("login.html", title="Login")
        token = login(username, password)
        if token:
            response = redirect(url_for("index_views.index_page"))
            set_access_cookies(response, token)
            flash("Login Successful", category="success")
            return response
        else:
            flash("Invalid login credentials. Please try again.", category="error")
    return render_template("login.html", title="Login")


@auth_views.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        if password1 != password2:
            flash("Passwords do not match. Please try again.", category="error")
            return render_template("register.html", title="Register")
        user = register(username, password1)
        if user:
            flash("Registration Successful", category="success")
            return redirect(url_for("auth_views.login_page"))
        else:
            flash("Registration failed. Please try again.", category="error")
    return render_template("register.html", title="Register")


@auth_views.route("/logout", methods=["GET"])
def logout_action():
    response = redirect(url_for("index_views.index_page"))
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response


"""
API Routes
"""

# @auth_views.route('/api/login', methods=['POST'])
# def user_login_api():
#   data = request.json
#   token = login(data['username'], data['password'])
#   if not token:
#     return jsonify(message='bad username or password given'), 401
#   response = jsonify(access_token=token)
#   set_access_cookies(response, token)
#   return response

# @auth_views.route('/api/identify', methods=['GET'])
# @jwt_required()
# def identify_user():
#     return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

# @auth_views.route('/api/logout', methods=['GET'])
# def logout_api():
#     response = jsonify(message="Logged Out!")
#     unset_jwt_cookies(response)
#     return response
