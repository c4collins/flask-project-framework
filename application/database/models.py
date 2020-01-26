"""Project models"""
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user

from application.database import DB

# NOTE: Make sure to make a ______Admin ModelView


class Project(DB.Model):
    """Project defines the projets being stored in this database"""

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<Project {self.id} - {self.name}>"
    def __str__(self):
        return f"Project {self.id} - {self.name}"


class ProjectAdmin(ModelView):
    """Flask-admin ModelView for the Project model"""
    def is_accessible(self):
        """Make sure only admins can see this"""
        return current_user.has_role('admin')
