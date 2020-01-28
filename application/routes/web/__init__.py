"""Web-based (i.e. HTML-returning) routes for this application"""
from os import environ
from flask import Blueprint, render_template

WEB = Blueprint('web', __name__)

def web_context_processors(app, domain):
    """Adds context processors for the web routes"""
    @app.context_processor
    def add_site_info():
        return {
            'domain': domain
        }

@WEB.route('/')
def null():
    """Home route"""

    return render_template("null.html")
