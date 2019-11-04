"""Project models"""

from .. import db


class Project(db.Model):
    """Project defines the projets being stored in this database"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<Project {self.id} - {self.name}>"
