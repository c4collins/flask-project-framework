from flask import Blueprint

api = Blueprint('api', __name__,
                # template_folder='templates'
                )


@api.route('/')
def null():
    return {
        'route': '/api/'
    }
