from sqlalchemy import Column, Integer, Boolean, String
from App import db
from App.models.database import link_player_property

class Email(db.Model):
    id = Column(Integer, primary_key=True)
    text = Column(String(500))
    amount = Column(Integer)
    save_for_later = Column(Boolean)
    players = db.relationship('players', secondary=link_player_property, backref='email', lazy='select')