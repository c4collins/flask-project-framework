"""Flask application factory & configuration"""

import os
import uuid

from flask import Flask, url_for
from flask_admin import helpers as admin_helpers
from flask_migrate import Migrate
from flask_security import SQLAlchemyUserDatastore, utils
from dotenv import load_dotenv

from application.routes import API as api_routes
from application.routes import WEB as web_routes
from application.routes import DATABASE as database_routes

from application.database import DB

from application.admin import ADMIN

from application.auth import AUTH
from application.auth.models import User, Role

load_dotenv()  # Added for Windows because I couldn't figure out how powershell env vars worked


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
    ADMIN_PASSWORD = 'password'  # FIXME: Set a better password


def register_blueprints(app):
    """Registers blueprints to the application

    register_blueprints(app:Flask) -> Flask
        app => Flask application to attach these blueprints to
    """

    app.register_blueprint(web_routes)
    app.register_blueprint(api_routes, url_prefix="/api")
    app.register_blueprint(database_routes, url_prefix="/db")
    return app


def create_default_user_and_roles(security):
    """Creates roles + an admin user if none exist"""

    if Role.query.filter_by(name='admin').count() == 0:
        security.user_datastore.find_or_create_role(
            name='admin', description='Administrator')

    if Role.query.filter_by(name='end-user').count() == 0:
        security.user_datastore.find_or_create_role(
            name='end-user', description='End user')

    if User.query.filter_by(email=ADMIN_EMAIL).count() == 0:
        # DB.create_all()
        security.user_datastore.create_user(
            email=ADMIN_EMAIL,
            password=utils.encrypt_password(ADMIN_PASSWORD)
        )
        DB.session.commit()
        security.user_datastore.add_role_to_user(ADMIN_EMAIL, 'admin')

    DB.session.commit()


def create_app(test_config=None):
    """Flask application factory

    create_app(test_config:object) -> Flask
        test_config => Use a defined flask config rather than config.py
    """

    app = Flask(__name__, instance_relative_config=True)
    protocol = "sqlite"

    app.config.from_mapping(
        SECRET_KEY="dev",
        DEBUG=True,
        # Flask Admin
        FLASK_ADMIN_SWATCH="cerulean",
        # SQLAlchemy
        SQLALCHEMY_DATABASE_URI=f"{protocol}:///{app.instance_path}/db.sqlite",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # Flask Security
        SECURITY_PASSWORD_SALT=str(uuid.uuid5(
            uuid.NAMESPACE_DNS, DOMAIN)),  # FIXME: Insecure
        SECURITY_CONFIRMABLE=False,  # TODO: Maybe set this up later, post flask-mail setup
        SECURITY_TRACKABLE=True,
        SECURITY_REGISTERABLE=True,
        SECURITY_RECOVERABLE=True,
        SECURITY_CHANGEABLE=True,
        # Flask-Security URLs, overridden because they don't put a / at the end
        SECURITY_LOGIN_URL="/login/",
        SECURITY_LOGOUT_URL="/logout/",
        SECURITY_REGISTER_URL="/register/",
        SECURITY_POST_LOGIN_VIEW="/",
        SECURITY_POST_LOGOUT_VIEW="/",
        SECURITY_POST_REGISTER_VIEW="/",
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
    Migrate(app, DB)

    user_datastore = SQLAlchemyUserDatastore(DB, User, Role)
    security = AUTH.init_app(app, user_datastore)

    app = register_blueprints(app)

    ADMIN.init_app(app)

    with app.test_request_context():
        DB.create_all()
        create_default_user_and_roles(security)

    return app
