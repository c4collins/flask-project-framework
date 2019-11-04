"""Routes for the Database - probably for tests or stored procedures in development.
This blueprint should probably be disabled before going live."""

from flask import Blueprint
from application.database.models import Project

DATABASE = Blueprint('database', __name__)


@DATABASE.route('/test')
def db_test():
    """Test to check if projects are in database"""

    query = Project.query.all()

    return {'query': query}
