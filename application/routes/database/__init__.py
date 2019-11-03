from flask import Blueprint
from application.database.models import Project

database = Blueprint('database', __name__,
                     # template_folder='templates'
                     )


@database.route('/test')
def db_test():
    q = Project.query.all()

    return {'query': q}
