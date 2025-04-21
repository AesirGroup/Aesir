# import os

# def load_config(app, overrides):
#     if os.path.exists(os.path.join('./App', 'custom_config.py')):
#         app.config.from_object('App.custom_config')
#     else:
#         app.config.from_object('App.default_config')
#     app.config.from_prefixed_env()

#     # Existing configurations
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['TEMPLATES_AUTO_RELOAD'] = True
#     app.config['PREFERRED_URL_SCHEME'] = 'https'
#     app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
#     app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
#     app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
#     app.config["JWT_COOKIE_SECURE"] = os.environ.get("JWT_COOKIE_SECURE", "True") == "True"  
#     app.config["JWT_COOKIE_SAMESITE"] = "None" 
#     app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  
#     app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Disable CSRF protection for JWT cookies in this setup
#     app.config['FLASK_ADMIN_SWATCH'] = 'darkly'

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
    
    # Updated JWT_COOKIE_SECURE to toggle based on environment
    app.config["JWT_COOKIE_SECURE"] = os.environ.get("FLASK_ENV", "production") != "development"
    app.config["JWT_COOKIE_SAMESITE"] = "None"  # Allow cross-origin requests
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Disable CSRF protection for simplicity
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    # Apply any overrides passed as arguments
    for key in overrides:
        app.config[key] = overrides[key]