from flask import session
from flask_socketio import emit, join_room, leave_room
from App.database.database_classes import Player, Game
from App.main import db, socketio
from App.models.auth import check_in_game
from random import randint

@socketio.on('check pregame status', namespace='/lobby') #player updating lobby screen
def check_pregame_status():
    try:
        username = session['username']
    except:
        print('INTRUDER')
        return False
    player = Player.query.filter_by(username=username).first()
    game = Game.query.filter_by(game_code=player.game_code).first()
    if game.game_started:
        emit('game started', session=session)
    else: #updates list of players in game so far
        usernames = []
        for i in game.players_connected:
            usernames += [str(i.username)]
        if usernames == '':
            usernames = []
        print('usrs: ', usernames)
        emit('player list', {'players': usernames}, session=session)

@socketio.on('join', namespace='/gameroom') #player joining room
def join(message):
    game_code = session.get('game_code')
    join_room(game_code)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room = game_code)

@socketio.on('leave lobby', namespace='/lobby') #player leaving lobby
def leave_lobby():
    try:
        session['username']
    except:
        return False
    #emit('status', {'msg':  session.get('username') + ' has entered the room.'}, session=session)

@socketio.on('left', namespace='/gameroom') #leaving room
def left(message):
    game_code = session.get('game_code')
    username = session.get('username')
    leave_room(game_code)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room = game_code)

@socketio.on('remove', namespace='/lobby')
def remove(data):
    try:
        username = session['username']
    except:
        print('INTRUDER')
        return False
    
    Player.query.filter_by(username = data['username']).delete()
    db.session.commit()
    print(data['username'])

@socketio.on('roll dice', namespace='/gameroom') #when a player rolls the dice
def roll_dice():
    game_code = session.get('game_code')
    username = session.get('username')
    game, player = check_in_game(game_code, username)
    if not game and not player:
        return False
    roll_value = randint(1,6)
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
    emit('message', {'msg': player.username + ' rolled a ' + str(roll_value) + ' they are now at possiton ' + str(new_value)}, room = game_code)
    emit('dice_roll', {'dice_value': roll_value, 'position': new_value}, session=session)
    #emit('dice_roll', {'dice_value': roll_value, 'position': new_value}, session=session_id[player.id])

@socketio.on('text', namespace='/gameroom') #sending text
def text(message):
    game_code = session.get('game_code')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room = game_code)

@socketio.on('update turn', namespace='/gameroom') #check if its players turn yet (if roll dice button should be shown)
def update_turn():
    game_code = session.get('game_code')
    username = session.get('username')
    game, player = check_in_game(game_code, username)
    if not game and not player:
        return False
    if game.index_of_turn == player.index_in_game:
        #emit('roll dice button change', {'operation': 'show'}, session=session_id[player.id])
        emit('roll dice button change', {'operation': 'show'}, session = session)
        emit('message', {'msg': 'It is ' + player.username + ' turn to roll the dice'}, room = game.game_code)
    else:
        #emit('roll dice button change', {'operation': 'hide'}, session=session_id[player.id])
        emit('roll dice button change', {'operation': 'hide'}, session = session)