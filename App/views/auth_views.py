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
from App.views.forms import RegisterForm, LoginForm

from .index_views import index_views

from App.controllers import login, register

auth_views = Blueprint("auth_views", __name__, template_folder="../templates")


"""
Page/Action Routes
"""


@auth_views.route("/login", methods=["GET", "POST"])
def login_page():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        token = login(username, password)
        if token:
            response = redirect(url_for("index_views.index_page"))
            set_access_cookies(response, token)
            flash("Login Successful", category="success")
            return response
        else:
            flash("Invalid login credentials. Please try again.", category="error")
    return render_template("login.html", title="Login", login_form=login_form)


@auth_views.route("/register", methods=["GET", "POST"])
def register_page():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        password = register_form.password1.data
        user = register(username, password)
        if user:
            flash("Registration Successful")
            return redirect(url_for("auth_views.login_page"))
        else:
            flash("Registration failed. Please try again.")
    return render_template(
        "register.html", title="Register", register_form=register_form
    )


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
