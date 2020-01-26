"""Flask application factory & configuration"""

import os
import uuid

from flask import Flask
from dotenv import load_dotenv

from .routes import API as api_routes
from .routes import WEB as web_routes
from .routes import DATABASE as database_routes

from .database import DB
from .database.models import Project

from .admin import ADMIN

from .auth import Auth
from .auth.models import User

load_dotenv()  # Added for Windows because I couldn't figure out how powershell env vars worked

AUTH = Auth()

try:
    DOMAIN = os.environ['DOMAIN']
except KeyError:
    DOMAIN = 'connomation.ca'

try:
    ADMIN_EMAIL = os.environ['ADMIN_EMAIL']
except KeyError:
    ADMIN_EMAIL = f'connor@{DOMAIN}'

try:
    ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']
except KeyError:
    ADMIN_PASSWORD = 'password' # FIXME: Set a better password


def register_blueprints(app):
    """Registers blueprints to the application

    register_blueprints(app:Flask) -> Flask
        app => Flask application to attach these blueprints to
    """

    app.register_blueprint(web_routes)
    app.register_blueprint(api_routes, url_prefix="/api")
    app.register_blueprint(database_routes, url_prefix="/db")
    return app


def create_app(test_config=None):
    """Flask application factory

    create_app(test_config:object) -> Flask
        test_config => Use a defined flask config rather than config.py
    """

    app = Flask(__name__, instance_relative_config=True)
    protocol = "sqlite"
    database_location = f"{protocol}:///{app.instance_path}/db.sqlite"

    app.config.from_mapping(
        SECRET_KEY="dev",
        DEBUG=True,
        # Flask Admin
        FLASK_ADMIN_SWATCH="cerulean",
        # SQLAlchemy
        SQLALCHEMY_DATABASE_URI=database_location,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # Flask Security
        SECURITY_PASSWORD_SALT=str(uuid.uuid5(
            uuid.NAMESPACE_DNS, DOMAIN)) # FIXME: Insecure
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    DB.init_app(app)
    with app.test_request_context():
        DB.create_all()

    AUTH.init_app(app)

    app = register_blueprints(app)

    ADMIN.init_app(app)

    @app.before_first_request
    def create_default_user():
        if User.query.filter_by(email=ADMIN_EMAIL).count() == 0:
            AUTH.user_datastore.create_user(
                email=ADMIN_EMAIL, password=ADMIN_PASSWORD)
            DB.session.commit()

    return app
