"""Routes that return their data as JSON"""
from flask import Blueprint

API = Blueprint('api', __name__)


@API.route('/')
def null():
    """Example API route"""

    return {
        'route': '/api/'
    }
