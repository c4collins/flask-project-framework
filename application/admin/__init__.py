"""Flask-Admin Constructor"""
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from application.database import DB
from application.database.models import Game, Player, Tournament

ADMIN = Admin()

ADMIN.add_view(ModelView(Game, DB.session))
ADMIN.add_view(ModelView(Player, DB.session))
ADMIN.add_view(ModelView(Tournament, DB.session))
