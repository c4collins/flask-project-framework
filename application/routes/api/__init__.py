"""Routes that return their data as JSON"""
from flask import Blueprint
from flask_security import login_required

API = Blueprint('api', __name__)


@API.route('/')
@login_required
def null():
    """Example API route"""

    return {
        'route': '/api/'
    }
