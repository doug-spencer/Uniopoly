from sqlalchemy import Boolean, Column, Integer
from App import db

class Game(db.Model):
    game_code = Column(Integer, primary_key=True)
    index_of_turn = Column(Integer)
    game_started = Column(Boolean)
    #host_id = db.relationship('Player', lazy='select', uselist=False)#use=Flase for one to one 
    players_connected = db.relationship('Player', backref='game', lazy='select')
    #action for specific index