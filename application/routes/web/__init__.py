from flask import Blueprint

web = Blueprint('web', __name__,
                # template_folder='templates'
                )


@web.route('/')
def null():
    return "/ route"
