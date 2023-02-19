from sqlalchemy import Column, Integer, String
from App import db

class Account(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    # password = db.Column(db.String(100), nullable=False)
    total_played = db.Column(db.Integer)
    games_won = db.Column(db.Integer)
    game_instances = db.relationship('Player', backref='account', lazy='select')