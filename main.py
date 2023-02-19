from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, Boolean, String
import random
from datetime import timedelta
from re import search

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['SECRET'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
app.app_context().push()
socketio = SocketIO(app, cors_allowed_origins='*')
#socketio = SocketIO(app, logger=True, engineio_logger=True)
db = SQLAlchemy(app)
engine = create_engine('sqlite:///instace/database.db', echo=False)

#global session_id
#session_id = {}


'''
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
'''
        
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
    '''
    utilities = db.relationship('Utilities', secondary=link_player_utilities, backref='player', lazy='select')
    properties = db.relationship('Property', secondary=link_player_property, backref='player', lazy='select')
    bus_stop = db.relationship('Bus_stop', secondary=link_player_bus_stop, backref='player', lazy='select')
    student_union = db.relationship('Student_union', secondary=link_player_student_union, backref='player', lazy='select')
    email = db.relationship('Email', secondary=link_player_email, backref='player', lazy='select')
    '''

class Account(db.Model):
    username = db.Column(db.String(100), primary_key=True)
#    password = db.Column(db.String(100), nullable=False)
    total_played = db.Column(db.Integer)
    games_won = db.Column(db.Integer)
    game_instances = db.relationship('Player', backref='account', lazy='select')

'''
class Utilities(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    text = Column(String(300))
    photo = Column(String(200))
    position = Column(Integer)
    morgage_value = Column(Integer)
    players = db.relationship('players', secondary=link_player_property, backref='utilities', lazy='select')
    
class Property(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    colour = Column(String(20))
    photo = Column(String(200))
    position = Column(Integer)
    morgage_value = Column(Integer)
    rents = Column(String(200))
    players = db.relationship('players', secondary=link_player_property, backref='property', lazy='select')

class Bus_stop(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    position = Column(Integer)
    players = db.relationship('players', secondary=link_player_property, backref='bus_stop', lazy='select')

class Student_union(db.Model):
    id = Column(Integer, primary_key=True)
    text = Column(String(500))
    amount = Column(Integer)
    save_for_later = Column(Boolean)
    players = db.relationship('players', secondary=link_player_property, backref='student_union', lazy='select')

class Email(db.Model):
    id = Column(Integer, primary_key=True)
    text = Column(String(500))
    amount = Column(Integer)
    save_for_later = Column(Boolean)
    players = db.relationship('players', secondary=link_player_property, backref='email', lazy='select')
'''

#admin1 = Account(username='jacob')
#db.session.add(admin1)
#db.session.add(Game(game_name='wooga'))
if True:
    try:
        Game.__table__.drop(engine)
        Player.__table__.drop(engine)
    except Exception as e:
        print(e)

db.create_all()
db.session.commit()

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

@app.route('/', methods=['GET', 'POST'])
def index():
    def get_account_usernames():
        accounts = Account.query.all()
        account_usernames = []
        for i in accounts:
            account_usernames.append(i.username)
        print(account_usernames)
        return account_usernames

    if(request.method=='GET'):
        return render_template('login.html')
        
    elif(request.method=='POST'):
        account_usernames = get_account_usernames()
        formSubmitted = request.form.get("button")
        print(formSubmitted)

        if formSubmitted == "signup":
            ##render menu once it has been made
            username = request.form.get("signupname")
            session['username'] = username            
            if username not in account_usernames:
                new_player = Account(username=username)
                db.session.add(new_player)
                db.create_all()
                db.session.commit()
                print("success i think")
                return redirect(url_for('menu'))
            else:
                print("account taken")
                return render_template('login.html')

        elif formSubmitted == "login":
            #render menu once it has been made
            username = request.form.get("loginname")
            if username in account_usernames:
                print("you can log in")
                session['username'] = username
                return redirect(url_for('menu'))
            else:
                print("account doesnt exist")
                return render_template('login.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    try:
        username = session['username']
    except: #player isnt in session (hasnt logged in)
        return False
    if request.method == 'GET':
        # temp code
        flash("current game codes:")
        for game in Game.query.all():
            flash(game.game_code)
        return render_template('menu.html')
    formType = request.form.get('button')
    games = Game.query.all()
    if formType == "Join":
        code = request.form.get('code')
        if search("^\d{6}$", code):
            for game in games:
                if game.game_code == int(code):
                    account = Account.query.filter_by(username=username).first()
                    player = Player(position=0, index_in_game=len(game.players_connected), money=7)
                    account.game_instances.append(player)
                    game.players_connected.append(player)
                    db.session.add(player)
                    db.session.commit()
                    flash("Game joined!")
                    session['game_code'] = code 
                    return redirect(url_for('lobby'))
        flash("Code was not valid")
        return render_template('menu.html')
    else:
        new_id = ""
        unique = False
        while not unique:
            unique = True
            new_id = ""
            for i in range(6):
                new_id += str(random.randint(0, 9))
            for game in games:
                if game.game_code == int(new_id):
                    unique = False
        game = Game(game_code=int(new_id), index_of_turn=0, game_started=False)
        account = Account.query.filter_by(username=username).first()
        player = Player(position=0, index_in_game=0, money=7)
        account.game_instances.append(player)
        game.players_connected.append(player)
        db.session.add(player)
        db.session.add(game)
        db.session.commit()
        session['game_code'] = new_id 
        flash("Game created with code " + new_id)
        return redirect(url_for('lobby'))


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
@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    try:
        username = session['username']
    except:
        return False
    game_code = session['game_code']

    if request.method == 'GET':
        return render_template('lobby.html', game_code=game_code, session=session)

    game = Game.query.filter_by(game_code=game_code).first()
    player = Player.query.filter_by(username=username).first()
    #only runs if POST
    if request.form.get('leaveButton') == 'leave room':
        Player.query.filter_by(username=username).delete()
        return redirect(url_for('menu'))
    elif request.form.get('startButton') == 'start game':
        if game.players_connected[0].username != username:
            #player isnt host
            return False
        game.game_started = True
        db.session.commit()
        return redirect(url_for('game_room'))

    return render_template('lobby.html', game_code=game_code, session=session)

@socketio.on('remove', namespace='/lobby')
def remove(data):
    try:
        username = session['username']
    except:
        print('INTRUDER')
        return False
    
    Player.query.filter_by(username=data['username']).delete()
    db.session.commit()
    print(data['username'])


       


     

@socketio.on('check pregame status', namespace='/lobby') #player updating lobby screen
def check_pregame_status():
    try:
        username = session['username']
    except:
        print('INTRUDER')
        return False
    player = Player.query.filter_by(username=username).first()
    if player == None:
        print(2345678765432)
        #players been removed from game
        emit('player not in game', session=session)
        return False
    game = Game.query.filter_by(game_code=player.game_code).first()
    if game.game_started:
        emit('game started', session=session)
    else: #updates list of players in game so far
        usernames = []
        for i in game.players_connected:
            usernames.append(str(i.username))
        
        print('usrs: ', usernames)
        emit('player list', {'players': usernames}, session=session)

@socketio.on('leave lobby', namespace='/lobby') #player leaving lobby
def leave_lobby():
    try:
        session['username']
    except:
        return False
    #emit('status', {'msg':  session.get('username') + ' has entered the room.'}, session=session)

@app.route('/gameroom', methods=['GET', 'POST'])
def game_room():
    if(request.method=='POST'): #player has made a game or is joining one
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
            game = Game(game_name=game_name, index_of_turn=0, game_started=False)
            db.session.add(game)
        else: #joining game
            game_name = choice
            game=Game.query.filter_by(game_name=choice).first()
        game.players_connected.append(player)#adds player to game    
        player.index_in_game = len(game.players_connected) - 1
        db.session.commit()
        #Store the data in session
        session['username'] = username
        session['game_name'] = game_name
        #session_id[player.id] = session.get('session_id') 
        return render_template('game_room.html', session = session)
    else: 
        if(session.get('username') is not None): #player is already in a session
            return render_template('game_room.html', session = session)
        else: #if not logged in
            games = Game.query.all()
            game_names = []
            for i in games:
                game_names.append(i.game_name)
            return redirect(url_for('index'), games = game_names)

@socketio.on('join', namespace='/gameroom') #player joining room
def join(message):
    game_name = session.get('game_name')
    join_room(game_name)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=game_name)

@socketio.on('roll dice', namespace='/gameroom') #when a player rolls the dice
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
    turn = game.index_of_turn
    if turn == len(game.players_connected) - 1:
        game.index_of_turn = 0
    else:
        game.index_of_turn = game.index_of_turn + 1
    db.session.commit()
    emit('message', {'msg': player.username + ' rolled a ' + str(roll_value) + ' they are now at possiton ' + str(new_value)}, room=game_name)
    emit('dice_roll', {'dice_value': roll_value, 'position': new_value}, session=session)
    #emit('dice_roll', {'dice_value': roll_value, 'position': new_value}, session=session_id[player.id])

@socketio.on('update turn', namespace='/gameroom') #check if its players turn yet (if roll dice button should be shown)
def update_turn():
    game_name = session.get('game_name')
    username = session.get('username')
    game, player = check_in_game(game_name, username)
    if not game and not player:
        return False
    if game.index_of_turn == player.index_in_game:
        #emit('roll dice button change', {'operation': 'show'}, session=session_id[player.id])
        emit('roll dice button change', {'operation': 'show'}, session=session)
        emit('message', {'msg': 'It is ' + player.username + ' turn to roll the dice'}, room=game.game_name)
    else:
        #emit('roll dice button change', {'operation': 'hide'}, session=session_id[player.id])
        emit('roll dice button change', {'operation': 'hide'}, session=session)

'''
def players_turn_to_roll(game_name):
    game = Game.query.filter_by(game_name=game_name).first()
    if not game:
        return False
    index = game.index_of_turn
    for i in game.players_connected:
        if i.index_in_game == index:
            emit('roll dice button change', {'operation': 'show'}, session=session_id[i.id])
            emit('message', {'msg': 'It is ' + i.username + ' turn to roll the dice'}, room=game.game_name)
        else:
            emit('roll dice button change', {'operation': 'hide'}, session=session_id[i.id])
'''

@socketio.on('text', namespace='/gameroom') #sending text
def text(message):
    game_name = session.get('game_name')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=game_name)

@socketio.on('left', namespace='/gameroom') #leaving room
def left(message):
    game_name = session.get('game_name')
    username = session.get('username')
    leave_room(game_name)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=game_name)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')