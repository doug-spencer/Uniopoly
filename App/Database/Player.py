class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    index_in_game = db.Column(db.Integer) #order of players
    symbol = db.Column(db.Integer)
    money = db.Column(db.Integer)
    game_code = db.Column(db.Integer, db.ForeignKey('game.game_code'))
    username = db.Column(db.Integer, db.ForeignKey('account.username'))