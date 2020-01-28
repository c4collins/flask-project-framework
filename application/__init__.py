"""Flask application factory & configuration"""

import os
import uuid
import logging
from time import strftime

from dotenv import load_dotenv
from flask import Flask, url_for, send_from_directory, request
from flask_admin import helpers as admin_helpers
from flask_assets import Environment, Bundle
from flask_security import SQLAlchemyUserDatastore, utils

from application.admin import ADMIN
from application.auth import AUTH
from application.auth.models import User, Role
from application.database import DB, MIGRATE
from application.mail import MAIL
from application.routes import API as api_routes
from application.routes import DATABASE as database_routes
from application.routes import WEB as web_routes
from application.routes.web import web_context_processors

load_dotenv()  # Added for Windows because I couldn't figure out how powershell env vars worked

logger = logging.getLogger(__name__)


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
    ADMIN_PASSWORD = 'Pa55w0rD!'

try:
    SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT']
except KeyError:
    SECURITY_PASSWORD_SALT = str(uuid.uuid5(uuid.NAMESPACE_DNS, DOMAIN))

try:
    MAIL_DEFAULT_SENDER = os.environ['MAIL_DEFAULT_SENDER']
except KeyError:
    MAIL_DEFAULT_SENDER = f"notifications@{DOMAIN}"

def register_blueprints(app):
    """Registers blueprints to the application

    register_blueprints(app:Flask) -> Flask
        app => Flask application to attach these blueprints to
    """

    app.register_blueprint(web_routes)
    app.register_blueprint(api_routes, url_prefix="/api")
    # TODO: This blueprint (database_routes) should probably be disabled before going live.
    app.register_blueprint(database_routes, url_prefix="/db")
    web_context_processors(app, domain=DOMAIN)
    return app


def create_default_user_and_roles(user_datastore):
    """Creates roles + an admin user if none exist"""

    if Role.query.filter_by(name='admin').count() == 0:
        user_datastore.find_or_create_role(
            name='admin', description='Administrator')

    if Role.query.filter_by(name='end-user').count() == 0:
        user_datastore.find_or_create_role(
            name='end-user', description='End user')

    if User.query.filter_by(email=ADMIN_EMAIL).count() == 0:
        # DB.create_all()
        user_datastore.create_user(
            email=ADMIN_EMAIL,
            password=utils.encrypt_password(ADMIN_PASSWORD)
        )
        DB.session.commit()
        user_datastore.add_role_to_user(ADMIN_EMAIL, 'admin')

    DB.session.commit()


def create_app(test_config=None):
    """Flask application factory

    create_app(test_config:object) -> Flask
        test_config => Use a defined flask config rather than config.py
    """
    db_protocol = "sqlite"

    app = Flask(__name__, instance_relative_config=True)
    assets = Environment(app)

    main_css = Bundle('css/main.scss', filters='pyscss', output='gen/main.css')
    assets.register('main_css', main_css)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DEBUG=True,
        # Flask Admin
        FLASK_ADMIN_SWATCH="cerulean",
        # SQLAlchemy
        SQLALCHEMY_DATABASE_URI=f"{db_protocol}:///{app.instance_path}/db.sqlite",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # Flask Security
        SECURITY_PASSWORD_SALT=SECURITY_PASSWORD_SALT,
        SECURITY_CONFIRMABLE=False,
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
        # Flask Mail
        MAIL_SERVER="smtp-relay.gmail.com",
        MAIL_PORT=465,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True,
        MAIL_USERNAME=os.environ['MAIL_USERNAME'],
        MAIL_PASSWORD=os.environ['MAIL_PASSWORD'],
        MAIL_DEFAULT_SENDER=MAIL_DEFAULT_SENDER,
        MAIL_MAX_EMAILS=2000,
        MAIL_ASCII_ATTACHMENTS=False,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True) # TODO Create config file for prod
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    DB.init_app(app)
    MIGRATE.init_app(app, DB)

    MAIL.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(DB, User, Role)
    AUTH.init_app(app, user_datastore)

    app = register_blueprints(app)

    ADMIN.init_app(app)

    with app.test_request_context():
        DB.create_all()
        create_default_user_and_roles(user_datastore)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.after_request
    def after_request(response):
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
        return response

    return app
