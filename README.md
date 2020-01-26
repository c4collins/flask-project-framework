# Flask Project Skeleton

- Use pipenv locally, but save a requirements.txt for Docker
- Run locally with `FLASK_APP=application FLASK_ENV=development flask run --host 0.0.0.0 --port 5000`
- Uses Flask-Migrate for db migrations; follow the instructions here:
    - from: https://flask-migrate.readthedocs.io/en/latest/
        - `flask db init` To start fresh after deleting db or in new location
        - `flask db migrate -m "Migration message"` review the file generated for accuracy
        - `flask db upgrade` to confirm and apply the migration to the db