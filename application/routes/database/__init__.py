"""Routes for the Database - probably for tests or stored procedures in development.
This blueprint should probably be disabled before going live."""

from flask import Blueprint
from application.database.models import Game

DATABASE = Blueprint('database', __name__)


@DATABASE.route('/test')
def db_test():
    """Test to check if games are in database"""

    query = Game.query.all()

    return {'query': query}
