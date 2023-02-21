from flask import Flask, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import random
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


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
engine = create_engine('sqlite:///database.db', echo=False)

# if True:
#     try:
#         Game.__table__.drop(engine)
#         Player.__table__.drop(engine)
#     except Exception as e:
#         print(e)

db.create_all()
db.session.commit()



from App.routes import index, lobby, menu, help, gameroom
from App.models.func.gameroom import roll_dice
# from App.models.classes.main import Player, Account, Game
# from App.models.auth import check_in_game

# @socketio.on('remove', namespace='/lobby')
# def remove(data):
#     try:
#         username = session['username']
#     except:
#         print('INTRUDER')
#         return False
    
#     Player.query.filter_by(username=data['username']).delete()
#     db.session.commit()
#     print(data['username'])  

# @socketio.on('check pregame status', namespace='/lobby') #player updating lobby screen
# def check_pregame_status():
#     try:
#         username = session['username']
#     except:
#         print('INTRUDER')
#         return False
#     player = Player.query.filter_by(username=username).first()
#     if player == None:
#         print(2345678765432)
#         #players been removed from game
#         emit('player not in game', session=session)
#         return False
#     game = Game.query.filter_by(game_code=player.game_code).first()
#     if game.game_started:
#         emit('game started', session=session)
#     else: #updates list of players in game so far
#         usernames = []
#         for i in game.players_connected:
#             usernames.append(str(i.username))
        
#         print('usrs: ', usernames)
#         emit('player list', {'players': usernames}, session=session)

# @socketio.on('leave lobby', namespace='/lobby') #player leaving lobby
# def leave_lobby():
#     try:
#         session['username']
#     except:
#         return False
#     #emit('status', {'msg':  session.get('username') + ' has entered the room.'}, session=session)

# @socketio.on('join', namespace='/gameroom') #player joining room
# def join(message):
#     game_code = session.get('game_code')
#     join_room(game_code)
#     emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=game_code)

# @socketio.on('roll dice', namespace='/gameroom') #when a player rolls the dice
# def roll_dice():
#     game_code = session.get('game_code')
#     username = session.get('username')
#     game, player = check_in_game(game_code, username)
#     if not game and not player:
#         return False
#     roll_value = random.randint(1,6)
#     current_value = player.position
#     new_value = roll_value + current_value
#     if new_value > 39:
#         new_value -= 40
#     player.position = new_value
#     turn = game.index_of_turn
#     if turn == len(game.players_connected) - 1:
#         game.index_of_turn = 0
#     else:
#         game.index_of_turn = game.index_of_turn + 1
#     db.session.commit()
#     emit('message', {'msg': player.username + ' rolled a ' + str(roll_value) + ' they are now at possiton ' + str(new_value)}, room=game_code)
#     emit('dice_roll', {'dice_value': roll_value, 'position': new_value}, session=session)
#     #emit('dice_roll', {'dice_value': roll_value, 'position': new_value}, session=session_id[player.id])

# @socketio.on('update turn', namespace='/gameroom') #check if its players turn yet (if roll dice button should be shown)
# def update_turn():
#     game_code = session.get('game_code')
#     username = session.get('username')
#     game, player = check_in_game(game_code, username)
#     if not game and not player:
#         return False
#     if game.index_of_turn == player.index_in_game:
#         #emit('roll dice button change', {'operation': 'show'}, session=session_id[player.id])
#         emit('roll dice button change', {'operation': 'show'}, session=session)
#         emit('message', {'msg': 'It is ' + player.username + ' turn to roll the dice'}, room=game.game_code)
#     else:
#         #emit('roll dice button change', {'operation': 'hide'}, session=session_id[player.id])
#         emit('roll dice button change', {'operation': 'hide'}, session=session)

# @socketio.on('text', namespace='/gameroom') #sending text
# def text(message):
#     game_code = session.get('game_code')
#     emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=game_code)

# @socketio.on('left', namespace='/gameroom') #leaving room
# def left(message):
#     game_code = session.get('game_code')
#     username = session.get('username')
#     leave_room(game_code)
#     session.clear()
#     emit('status', {'msg': username + ' has left the room.'}, room=game_code)