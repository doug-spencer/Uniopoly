from sqlalchemy import Column, Integer, String
from App import db
from App.models.database import link_player_property

class Utilities(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    text = Column(String(300))
    photo = Column(String(200))
    position = Column(Integer)
    morgage_value = Column(Integer)
    # players = db.relationship('players', secondary=link_player_property, backref='utilities', lazy='select')