"""Flask-Admin Constructor"""
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from application.database import DB
from application.database.models import Project

ADMIN = Admin()

ADMIN.add_view(ModelView(Project, DB.session))
