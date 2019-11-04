"""Web-based (i.e. HTML-returning) routes for this application"""
from flask import Blueprint

WEB = Blueprint('web', __name__,
                # template_folder='templates'
                )


@WEB.route('/')
def null():
    """Home route"""

    return "/ route"
