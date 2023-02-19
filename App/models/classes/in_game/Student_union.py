from sqlalchemy import Column, Integer, String, Boolean
from App import db
from database import link_player_property

class Student_union(db.Model):
    id = Column(Integer, primary_key=True)
    text = Column(String(500))
    amount = Column(Integer)
    save_for_later = Column(Boolean)
    players = db.relationship('players', secondary=link_player_property, backref='student_union', lazy='select')