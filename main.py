from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import random
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
app.app_context().push()
socketio = SocketIO(app)
db = SQLAlchemy(app)
engine = create_engine('sqlite:///database.db', echo=False)

class Game(db.Model):
    game_name = db.Column(db.String(100), primary_key=True)
    host_username = db.Column(db.String(100))
    players_connected = db.relationship('Player', backref='game', lazy='select')
    #index of turn
    #action for specific index

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    symbol = db.Column(db.Integer)
    money = db.Column(db.Integer)
    game_id = db.Column(db.Integer, db.ForeignKey('game.game_name'))
    username = db.Column(db.Integer, db.ForeignKey('account.username'))

class Account(db.Model):
    username = db.Column(db.String(100), primary_key=True)
#    password = db.Column(db.String(100), nullable=False)
    total_played = db.Column(db.Integer)
    games_won = db.Column(db.Integer)
    game_instances = db.relationship('Player', backref='account', lazy='select')

#admin1 = Account(username='jacob')
#db.session.add(admin1)
#db.session.add(Game(game_name='wooga'))
db.create_all()
db.session.commit()

def check_in_game(game_name, username):
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

@app.route('/')
def index():
    games = Game.query.all()
    game_names = []
    for i in games:
        print(i.game_name)
        game_names.append(i.game_name)
    return render_template('index.html', games = game_names)

'''
@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('roll dice event')
def test_message():
    emit('my response', {'data': int(random.randint(1,6))}, broadcast=True)

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
'''

@app.route('/gameroom', methods=['GET', 'POST'])
def game_room():
    if(request.method=='POST'):
        username = request.form['username']
        choice = request.form['choice'] #if the made a game or the name of the game they joined
        account = Account.query.filter_by(username=username).first()
        if not account: #player doesnt have account
            account = Account(username=username)
            db.session.add(account)
        player = Player(position=0)
        db.session.add(player)
        account.game_instances.append(player) #links account with the player in the new game
        if choice == 'make': #imaking a game
            game_name = request.form['game_name']
            game = Game(game_name=game_name)
            db.session.add(game)
        else: #joining game
            game_name = choice
            game=Game.query.filter_by(game_name=choice).first()
        game.players_connected.append(player)#adds player to game    
        db.session.commit()
        #Store the data in session
        session['username'] = username
        session['game_name'] = game_name
        return render_template('game_room.html', session = session)
    else:
        if(session.get('username') is not None):
            return render_template('game_room.html', session = session)
        else: #if not logged in
            games = Game.query.all()
            game_names = []
            for i in games:
                game_names.append(i.game_name)
            return redirect(url_for('index'), games = game_names)

@socketio.on('join', namespace='/gameroom')
def join(message):
    game_name = session.get('game_name')
    join_room(game_name)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=game_name)

@socketio.on('roll dice', namespace='/gameroom')
def roll_dice():
    game_name = session.get('game_name')
    username = session.get('username')
    game, player = check_in_game(game_name, username)
    if not game and not player:
        return False
    roll_value = random.randint(1,6)
    current_value = player.position
    new_value = roll_value + current_value
    if new_value > 39:
        new_value -= 40
    player.position = new_value
    db.session.commit()
    emit('dice_roll', {'dice_value': roll_value, 'position': new_value}, room=game_name)

@socketio.on('text', namespace='/gameroom')
def text(message):
    game_name = session.get('game_name')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=game_name)

@socketio.on('left', namespace='/gameroom')
def left(message):
    game_name = session.get('game_name')
    username = session.get('username')
    leave_room(game_name)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=game_name)

if __name__ == '__main__':
    socketio.run(app)