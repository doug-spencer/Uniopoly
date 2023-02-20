from sqlalchemy import Column, Integer
from App import db
# from models.database import link_player_utilities, link_player_student_union, link_player_bus_stop, link_player_email, link_player_property

class Player(db.Model):
    id = Column(Integer, primary_key=True)
    position = Column(Integer)
    index_in_game = Column(Integer) #order of players
    symbol = Column(Integer)
    money = Column(Integer)
    game_code = Column(Integer, db.ForeignKey('game.game_code'))
    username = Column(Integer, db.ForeignKey('account.username'))
    # utilities = db.relationship('Utilities', secondary=link_player_utilities, backref='player', lazy='select')
    # properties = db.relationship('Property', secondary=link_player_property, backref='player', lazy='select')
    # bus_stop = db.relationship('Bus_stop', secondary=link_player_bus_stop, backref='player', lazy='select')
    # student_union = db.relationship('Student_union', secondary=link_player_student_union, backref='player', lazy='select')
    # email = db.relationship('Email', secondary=link_player_email, backref='player', lazy='select')