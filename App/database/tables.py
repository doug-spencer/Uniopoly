from App.main import db

link_player_property = db.Table('link_player_property',
        db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
        db.Column('card_id', db.Integer, db.ForeignKey('property.id'), primary_key=True),
        db.Column('mortgaged', db.Boolean),
        db.Column('houses', db.Integer)
        )


link_player_utilities = db.Table('link_player_utilities',
        db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
        db.Column('card_id', db.Integer, db.ForeignKey('utilities.id'), primary_key=True),
        db.Column('mortgaged', db.Boolean)
        )


link_player_student_union = db.Table('link_player_student_union',
        db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
        db.Column('student_union_id', db.Integer, db.ForeignKey('student_union.id'), primary_key=True)
        )


link_player_email = db.Table('link_player_email',
        db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
        db.Column('email_id', db.Integer, db.ForeignKey('email.id'), primary_key=True)
        )


link_player_bus_stop = db.Table('link_player_bus_stop',
        db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
        db.Column('card_id', db.Integer, db.ForeignKey('bus_stop.id'), primary_key=True),
        db.Column('mortgaged', db.Boolean)
        )
        

class Game(db.Model):
    game_code = db.Column(db.Integer, primary_key=True)
    index_of_turn = db.Column(db.Integer)
    game_started = db.Column(db.Boolean)
    #host_id = db.relationship('Player', lazy='select', uselist=False)#use=Flase for one to one 
    players_connected = db.relationship('Player', backref='game', lazy='select')
    #action for specific index


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    index_in_game = db.Column(db.Integer) #order of players
    symbol = db.Column(db.Integer)
    money = db.Column(db.Integer)
    game_code = db.Column(db.Integer, db.ForeignKey('game.game_code'))
    username = db.Column(db.Integer, db.ForeignKey('account.username'))
    turns_in_jail = db.Column(db.Integer)
    utilities = db.relationship('Utilities', secondary=link_player_utilities, backref='player', lazy='select')
    properties = db.relationship('Property', secondary=link_player_property, backref='player', lazy='select')
    bus_stop = db.relationship('Bus_stop', secondary=link_player_bus_stop, backref='player', lazy='select')
    student_union = db.relationship('Student_union', secondary=link_player_student_union, backref='player', lazy='select')
    email = db.relationship('Email', secondary=link_player_email, backref='player', lazy='select')


class Account(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    total_played = db.Column(db.Integer)
    games_won = db.Column(db.Integer)
    game_instances = db.relationship('Player', backref='account', lazy='select')


class Utilities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    text = db.Column(db.String(300))
    photo = db.Column(db.String(200))
    position = db.Column(db.Integer)
    buy_price = db.Column(db.Integer)
    morgage_value = db.Column(db.Integer)
    

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    colour = db.Column(db.String(20))
    photo = db.Column(db.String(200))
    position = db.Column(db.Integer)
    buy_price = db.Column(db.Integer)
    morgage_value = db.Column(db.Integer)
    rents = db.Column(db.String(200))


class Bus_stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    photo = db.Column(db.String(200))
    position = db.Column(db.Integer)
    # rents = {'0': 0, '1': 25, '2': 50, '3': 100, '4': 200}
    # owner = db.Column(db.String(100))
    # morgage_value = db.Column(db.Integer)
    # is_owned = db.Column(db.Boolean, default=False)
    buy_price = db.Column(db.Integer)
    morgage_value = db.Column(db.Integer)


class Student_union(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    amount = db.Column(db.Integer)
    go_to = db.Column(db.Integer)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    amount = db.Column(db.Integer)
    go_to = db.Column(db.Integer)