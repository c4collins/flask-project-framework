# Flask Project Skeleton

## Notes:
- Use pipenv locally, but save a requirements.txt for Docker
- Uses Flask-Migrate for db migrations; follow the instructions here:
    - from: https://flask-migrate.readthedocs.io/en/latest/
        - `flask db init` To start fresh after deleting db or in new location
        - `flask db migrate -m "Migration message"` review the file generated for accuracy
        - `flask db upgrade` to confirm and apply the migration to the db

## Development Startup Instructions
1. Close the repo and `cd` into the folder
1. Create a `.env` file containing:
    - `FLASK_APP=application` # Shouldn't change, probably doesn't need to be variable but ¯\\_(ツ)_/¯
    - `FLASK_ENV=development` # or `production`
    - `DOMAIN=` # the domain this site will run on; defaults to `connomation.ca`
    - `ADMIN_EMAIL=` # email address for admin account; defaults to `connor@{DOMAIN}`
    - `ADMIN_PASSWORD=` # password for said admin account; defaults to `Pa55w0rD!`
    - `SECURITY_PASSWORD_SALT=` # Salt for user passwords; defaults to an insecure uuid5 which lets you share dbs between environments for development
    - `MAIL_USERNAME` # Username for gmail account that can authorize sending emails (i.e. G Suite admin account)
    - `MAIL_PASSWORD` # Password for said gmail account
    - `MAIL_DEFAULT_SENDER` # email address to actually use for sending; defaults to notifications@{DOMAIN} - make sure you can receive mail or have an undeliverable reply for this address for marketing purposes
    
    #\ if you want to use something other than G Suite you'll have to mess with the code
1. Run `pipenv shell` to create or join the 
1. `pipenv install`
1. Run locally with `flask run --host 0.0.0.0 --port 5000`