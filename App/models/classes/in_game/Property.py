from sqlalchemy import Column, Integer, String
from App import db
from App.models.database import link_player_property

class Property(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    colour = Column(String(20))
    photo = Column(String(200))
    position = Column(Integer)
    morgage_value = Column(Integer)
    rents = Column(String(200))
    players = db.relationship('players', secondary=link_player_property, backref='property', lazy='select')