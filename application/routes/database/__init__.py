"""Routes for the Database - probably for tests or stored procedures in development."""

from flask import Blueprint
from application.auth.models import User, Role
from application.database.models import Project

DATABASE = Blueprint('database', __name__)


@DATABASE.route('/test')
def db_test():
    """Test to check if projects are in database"""

    user_query = User.query.all()
    role_query = Role.query.all()
    project_query = Project.query.all()

    return {
        'users': [str(user) for user in user_query],
        'roles': [str(role) for role in role_query],
        'projects': project_query
    }
