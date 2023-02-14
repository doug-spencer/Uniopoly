class Game(db.Model):
    game_code = db.Column(db.Integer, primary_key=True)
    index_of_turn = db.Column(db.Integer)
    game_started = db.Column(db.Boolean)
    #host_id = db.relationship('Player', lazy='select', uselist=False)#use=Flase for one to one 
    players_connected = db.relationship('Player', backref='game', lazy='select')
    #action for specific index