"""Manages user authentication and authorization"""
from flask_security import Security, SQLAlchemyUserDatastore

from application.database import DB

from .models import User, Role


class Auth:
    def __init__(self):
        self.user_datastore = SQLAlchemyUserDatastore(DB, User, Role)

    def init_app(self, app):
        """Takes the flask_app and manages user auth for it"""
        Security(app, self.user_datastore)
