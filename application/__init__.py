"""Flask application factory & configuration"""

from pathlib import Path
import logging
import os
import uuid

from dotenv import load_dotenv
from flask import Flask, url_for, send_from_directory, request
from flask_admin import helpers as admin_helpers
from flask_assets import Environment, Bundle
from flask_security import SQLAlchemyUserDatastore, utils

from application.helpers import try_except

from application.admin import ADMIN
from application.auth import AUTH
from application.auth.models import User, Role
from application.database import DB, MIGRATE
from application.mail import MAIL
from application.routes import API as api_routes
from application.routes import DATABASE as database_routes
from application.routes import WEB as web_routes
from application.routes.web import web_context_processors


load_dotenv()

FLASK_ENV = try_except('FLASK_ENV', 'development')
SECRET_KEY = try_except('SECRET_KEY', 'dev')
DEBUG = try_except('DEBUG', False)
MAIL_DEBUG = int(DEBUG is True)  # Flask-Mail has some issues with bools
DOMAIN = try_except('DOMAIN', 'connomation.ca')
ADMIN_EMAIL = try_except('ADMIN_EMAIL', f'connor@{DOMAIN}')
ADMIN_PASSWORD = try_except('ADMIN_PASSWORD', 'Pa55w0rD!')
SECURITY_PASSWORD_SALT = try_except(
    'SECURITY_PASSWORD_SALT',
    str(uuid.uuid5(uuid.NAMESPACE_DNS, DOMAIN))
)
MAIL_DEFAULT_SENDER = try_except(
    'MAIL_DEFAULT_SENDER', f"notifications@{DOMAIN}")
DB_PROTOCOL = try_except('DB_PROTOCOL', 'sqlite')
INSTANCE_PATH = Path(os.path.dirname(__file__), '..', 'instance')
SQLALCHEMY_DATABASE_URI = f"{DB_PROTOCOL}:///{INSTANCE_PATH}/db.sqlite"

def register_blueprints(app):
    """Registers blueprints to the application

    register_blueprints(app:Flask) -> Flask
        app => Flask application to attach these blueprints to
    """
    logger = logging.getLogger(__name__)
    logger.info('Loading blueprints')
    app.register_blueprint(web_routes)
    app.register_blueprint(api_routes, url_prefix="/api")
    # TODO: This blueprint (database_routes) should probably be disabled before going live.
    app.register_blueprint(database_routes, url_prefix="/db")
    web_context_processors(app, domain=DOMAIN)
    return app


def create_default_user_and_roles(user_datastore):
    """Creates roles + an admin user if none exist"""
    logger = logging.getLogger(__name__)
    if Role.query.filter_by(name='admin').count() == 0:
        logger.info('Creating admin role')
        user_datastore.find_or_create_role(
            name='admin', description='Administrator')

    if Role.query.filter_by(name='end-user').count() == 0:
        logger.info('Creating end-user role')
        user_datastore.find_or_create_role(
            name='end-user', description='End user')

    if User.query.filter_by(email=ADMIN_EMAIL).count() == 0:
        logger.info('Creating admin user')
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
    logger = logging.getLogger(__name__)
    app = Flask(
        __name__,
        instance_path=INSTANCE_PATH,
        instance_relative_config=True,
    )
    assets = Environment(app)

    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
    )

    if test_config is None:
        settings_path = Path(os.path.dirname(__file__), '..', 'settings')
        app.config.from_pyfile(Path(settings_path, 'dev.cfg'))
        if FLASK_ENV != 'development':
            app.config.from_pyfile(Path(settings_path, 'prod.cfg'))
    else:
        app.config.from_mapping(test_config)

    main_css = Bundle('css/main.scss', filters='pyscss', output='gen/main.css')
    assets.register('main_css', main_css)

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

    # @app.after_request
    # def after_request(response):
    #    timestamp = strftime('[%Y-%b-%d %H:%M]')
    #    logger.error(
    #       '%s %s %s %s %s %s',
    #       timestamp,
    #       request.remote_addr,
    #       request.method,
    #       request.scheme,
    #       request.full_path,
    #       response.status
    #   )
    #    return response

    logger.debug('app loaded')
    return app
