from sqlalchemy import Column, Integer, String
from App import db
from App.models.database import link_player_property

class Bus_stop(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    position = Column(Integer)
    # players = db.relationship('players', secondary=link_player_property, backref='bus_stop', lazy='select')