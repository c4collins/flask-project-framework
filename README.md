# Flask Project Skeleton

## Notes:

- Use pipenv locally, but save a requirements.txt for Docker
- Uses Flask-Migrate for db migrations; follow the instructions here:
  - [from](https://flask-migrate.readthedocs.io/en/latest/)
    - `flask db init` To start fresh after deleting db or in new location
    - `flask db migrate -m "Migration message"` review the file generated for accuracy
    - `flask db upgrade` to confirm and apply the migration to the db

## Development Startup Instructions

1. Close the repo and `cd` into the folder
1. Create a `.env` file containing:

   - `FLASK_APP=` # application; always
   - `FLASK_ENV=` # development; or anything else for prod mode
   - `MAIL_USERNAME=` # Email account to login to server as not necessarily the sendmail address
   - `MAIL_PASSWORD=` # Password for that user

1. Check that the settings in `settings/{dev,prod}.cfg` are acceptable - `prod` overwrites `dev` when not in 'development' mode, but most of the settings don't need to be overwritten
   - FLASK_ADMIN_SWATCH choices available [here](https://bootswatch.com/3/)
1. Run `pipenv shell` to create or join the the virtuaenv
1. `pipenv install`
1. Run locally with `flask run --host 0.0.0.0 --port 5000`

## Production/Server Startup instructions

1. `pipenv lock --requirements > requirements.txt`
1. `docker-compose up --build -d`
