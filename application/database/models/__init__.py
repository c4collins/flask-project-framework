"""Table tennis models"""
from datetime import datetime

from .. import DB


class Player(DB.Model):
    """Player represents a player of table tennis"""
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(255), nullable=False)
    display_name = DB.Column(DB.String(255), nullable=True)
    date_created = DB.Column(DB.DateTime, default=datetime.now, nullable=False)
    date_modified = DB.Column(
        DB.DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False)
    game_id = DB.Column(DB.Integer, DB.ForeignKey("game.id"))

    def __repr__(self):
        return f"P#{self.id}-{self.display_name}"


class Game(DB.Model):
    """Game represents the status of a single game, during as well as pre- and post-"""

    id = DB.Column(DB.Integer, primary_key=True)
    players = DB.relationship(
        'Player',
        lazy=True)
    is_finished = DB.Column(DB.Boolean, default=False, nullable=False)
    is_happening = DB.Column(DB.Boolean, default=False, nullable=False)
    date_created = DB.Column(DB.DateTime, default=datetime.now, nullable=False)
    date_modified = DB.Column(
        DB.DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False)
    tournament_id = DB.Column(DB.Integer, DB.ForeignKey("tournament.id"))

    def __repr__(self):
        return f"G#{self.id}"


class Tournament(DB.Model):
    """Tournament represents a collection of games for an event"""
    id = DB.Column(DB.Integer, primary_key=True)
    games = DB.relationship(
        'Game',
        backref="tournament",
        lazy=True)
    name = DB.Column(DB.String(255))
    date_created = DB.Column(DB.DateTime, default=datetime.now, nullable=False)
    date_modified = DB.Column(
        DB.DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False)

    def __repr__(self):
        if self.name:
            return f"{self.name} Tournament"
        return f"T#{self.id}"
