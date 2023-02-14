from App import db

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

class Account(db.Model):
    username = db.Column(db.String(100), primary_key=True)
#    password = db.Column(db.String(100), nullable=False)
    total_played = db.Column(db.Integer)
    games_won = db.Column(db.Integer)
    game_instances = db.relationship('Player', backref='account', lazy='select')

def check_in_game(game_name, username): #verification fucntion
    game = Game.query.filter_by(game_name = game_name).first()
    if not game:
        return False, False
    account = Account.query.filter_by(username=username).first()
    if not account:
        return False, False
    player = False
    for i in game.players_connected:
        if i.username == username:
            player = i
    if not player:
        return False, False
    return game, player

def get_account_usernames():
    accounts = Account.query.all()
    account_usernames = []
    for i in accounts:
        account_usernames.append(i.username)
    print(account_usernames)
    return account_usernames