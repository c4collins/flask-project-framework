"""Manages user authentication and authorization"""
from flask_security import Security, SQLAlchemyUserDatastore, login_required
from flask_admin.contrib.sqla import ModelView

from application.database import DB

from application.auth.models import User, Role


class Auth:
    """Flask-Security: Controls user auth for the application"""
    def __init__(self):
        self.user_datastore = SQLAlchemyUserDatastore(DB, User, Role)

    def init_app(self, app):
        """Sets up user management for the Flask app

        init_app(self, Flask) -> Security
            Flask => flask application
        """
        return Security(app, self.user_datastore)
