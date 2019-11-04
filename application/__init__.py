"""Flask application factory & configuration"""

import os

from flask import Flask

from .routes import API as api_routes
from .routes import WEB as web_routes
from .routes import DATABASE as database_routes

from .database import DB
from .database.models import Project


def register_blueprints(app):
    """Registers blueprints to the application

    @app: Flask application - application to attach these blueprints to
    """

    app.register_blueprint(web_routes)
    app.register_blueprint(api_routes, url_prefix="/api")
    app.register_blueprint(database_routes, url_prefix="/db")
    return app


def create_app(test_config=None):
    """Flask Application factory

    @config: object - Use a defined flask config rather than config.py
    """

    app = Flask(__name__, instance_relative_config=True)
    protocol = "sqlite"
    database_location = f"{protocol}:///{app.instance_path}/db.sqlite"
    print(database_location)
    app.config.from_mapping(
        SECRET_KEY="dev",
        # DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
        SQLALCHEMY_DATABASE_URI=database_location,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
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

    app = register_blueprints(app)

    return app


# if __name__ == "__main__":
#     app = create_app()
