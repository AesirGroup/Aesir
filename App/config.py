import os

def load_config(app, overrides):
    if os.path.exists(os.path.join('./App', 'custom_config.py')):
        app.config.from_object('App.custom_config')
    else:
        app.config.from_object('App.default_config')
    app.config.from_prefixed_env()

    # Existing configurations
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
    app.config["JWT_COOKIE_SECURE"] = os.environ.get("JWT_COOKIE_SECURE", "True") == "True"  # Use Secure cookies if True
    app.config["JWT_COOKIE_SAMESITE"] = "None"  # Allow cookies in cross-origin requests
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # 1 hour expiration for JWT tokens
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Disable CSRF protection for JWT cookies in this setup
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'

    # Apply any overrides passed as arguments
    for key in overrides:
        app.config[key] = overrides[key]