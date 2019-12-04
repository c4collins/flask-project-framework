FLASK_APP=application flask db migrate &&
    FLASK_APP=application flask db upgrade
