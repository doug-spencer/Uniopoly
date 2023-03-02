from sqlalchemy import Column, Integer, String, Boolean
from App.main import db

link_player_property = db.Table('link_player_property',
        Column('username', Integer, db.ForeignKey('player.username'), primary_key=True),
        Column('property_id', Integer, db.ForeignKey('property.id'), primary_key=True),
        Column('houses', Integer)
        )

link_player_utilities = db.Table('link_player_utilities',
        Column('username', Integer, db.ForeignKey('player.username'), primary_key=True),
        Column('utilities_id', Integer, db.ForeignKey('utilities.id'), primary_key=True)
        )

link_player_student_union = db.Table('link_player_student_union',
        Column('username', Integer, db.ForeignKey('player.username'), primary_key=True),
        Column('student_union', Integer, db.ForeignKey('student_union.id'), primary_key=True)
        )

link_player_email = db.Table('link_player_email',
        Column('username', Integer, db.ForeignKey('player.username'), primary_key=True),
        Column('email', Integer, db.ForeignKey('email.id'), primary_key=True)
        )

link_player_bus_stop = db.Table('link_player_bus_stop',
        Column('username', Integer, db.ForeignKey('player.username'), primary_key=True),
        Column('bus_stop', Integer, db.ForeignKey('bus_stop.id'), primary_key=True)
        )

        
class Game(db.Model):
    game_code = Column(Integer, primary_key=True)
    index_of_turn = Column(Integer)
    game_started = Column(Boolean)
    

    #host_id = db.relationship('Player', lazy='select', uselist=False)#use=Flase for one to one 
    players_connected = db.relationship('Player', backref='game', lazy='select')
    #action for specific index

class Player(db.Model):
    id = Column(Integer, primary_key=True)
    position = Column(Integer)
    index_in_game = Column(Integer) #order of players
    symbol = Column(Integer)
    money = Column(Integer)
    game_code = Column(Integer, db.ForeignKey('game.game_code'))
    username = Column(Integer, db.ForeignKey('account.username'))
    turns_in_jail = Column(Integer)
    utilities = db.relationship('Utilities', secondary=link_player_utilities, backref='player', lazy='select')
    properties = db.relationship('Property', secondary=link_player_property, backref='player', lazy='select')
    bus_stop = db.relationship('Bus_stop', secondary=link_player_bus_stop, backref='player', lazy='select')
    student_union = db.relationship('Student_union', secondary=link_player_student_union, backref='player', lazy='select')
    email = db.relationship('Email', secondary=link_player_email, backref='player', lazy='select')


class Account(db.Model):
    username = db.Column(db.String(100), primary_key=True)
#    password = db.Column(db.String(100), nullable=False)
    total_played = db.Column(db.Integer)
    games_won = db.Column(db.Integer)
    game_instances = db.relationship('Player', backref='account', lazy='select')


class Utilities(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    text = Column(String(300))
    photo = Column(String(200))
    position = Column(Integer)
    buy_price = Column(Integer)
    morgage_value = Column(Integer)
    #players = db.relationship('players', secondary=link_player_property, backref='utilities', lazy='select')
    
class Property(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    colour = Column(String(20))
    photo = Column(String(200))
    position = Column(Integer)
    buy_price = Column(Integer)
    morgage_value = Column(Integer)
    rents = Column(String(200))
    #players = db.relationship('players', secondary=link_player_property, backref='property', lazy='select')

class Bus_stop(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    photo = Column(String(200))
    position = Column(Integer)
    #rents = {'0': 0, '1': 25, '2': 50, '3': 100, '4': 200}
    # owner = Column(String(100))
    # morgage_value = Column(Integer)
    # is_owned = Column(Boolean, default=False)
    buy_price = Column(Integer)
    morgage_value = Column(Integer)


    #players = db.relationship('players', secondary=link_player_property, backref='bus_stop', lazy='select')

class Student_union(db.Model):
    id = Column(Integer, primary_key=True)
    text = Column(String(500))
    amount = Column(Integer)
    save_for_later = Column(Boolean)
    #players = db.relationship('players', secondary=link_player_property, backref='student_union', lazy='select')

class Email(db.Model):
    id = Column(Integer, primary_key=True)
    text = Column(String(500))
    amount = Column(Integer)
    save_for_later = Column(Boolean)
    #players = db.relationship('players', secondary=link_player_property, backref='email', lazy='select')

