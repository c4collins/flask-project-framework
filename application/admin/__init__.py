"""Flask-Admin Constructor"""
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from application.database import DB
from application.database.models import Project, ProjectAdmin

from application.auth.models import User, UserAdmin, Role, RoleAdmin

ADMIN = Admin(template_mode="bootstrap3")

# Default
ADMIN.add_view(ProjectAdmin(Project, DB.session))

# Security / Auth
## User admin
ADMIN.add_view(RoleAdmin(Role, DB.session))
ADMIN.add_view(UserAdmin(User, DB.session))
# ADMIN.add_view(ModelView(Role, DB.session)) # Insecure
# ADMIN.add_view(ModelView(User, DB.session)) # Insecure
