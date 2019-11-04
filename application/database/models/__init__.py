"""Project models"""

from .. import DB


class Project(DB.Model):
    """Project defines the projets being stored in this database"""

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<Project {self.id} - {self.name}>"
