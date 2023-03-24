from flask import session
from flask_socketio import emit, join_room, leave_room
from App.database.tables import Player, Game
from App.main import db, socketio

@socketio.on('check pregame status', namespace='/lobby') #player updating lobby screen
def check_pregame_status():
    try:
        username = session['username']
    except:
        return False
    game_code = session['game_code']
    game = Game.query.filter_by(game_code=game_code).first()
    if game.game_started:
        emit('game started', session=session)
    else: #updates list of players in game so far
        usernames = []
        for i in game.players_connected:
            usernames += [str(i.username)]
        if usernames == '':
            usernames = []
        # emit('get username', {'username': username}, session=session)
        emit('player list', {'players': usernames, 'username': username}, session=session)
    if len(game.players_connected) == 6:
        emit('flash function', {'msg': 'Lobby is full, waiting for host to start game!'})
    if username == game.players_connected[0].username:
        if len(game.players_connected) > 1:
            emit('start game avalible', session=session)
        else:
            emit('start game not avalible', session=session)

@socketio.on('remove', namespace='/lobby')
def remove(data):
    try:
        username = session['username']
    except:
        return False
    
    Player.query.filter_by(username = data['username']).delete()
    db.session.commit()
    game_code = session['game_code']
    leave_room(game_code)

@socketio.on('leave lobby', namespace='/lobby') #player leaving lobby
def leave_lobby():
    try:
        session['username']
    except:
        return False
    game_code = session['game_code']
    leave_room(game_code)
    # emit('status', {'msg':  session.get('username') + ' has left the room.'}, session=session)

@socketio.on('join', namespace='/lobby') #player leaving lobby
def join(data):
    game_code = session['game_code']
    game = Game.query.filter_by(game_code=game_code).first()
    join_room(game_code)
    usernames = []
    for i in game.players_connected:
        usernames += [str(i.username)]
        emit("flash function", {'msg': session.get('username')}, room=game_code)