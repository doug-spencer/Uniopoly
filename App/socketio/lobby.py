from flask import session
from flask_socketio import emit
from App.database.tables import Player, Game
from App.main import db, socketio

@socketio.on('check pregame status', namespace='/lobby') #player updating lobby screen
def check_pregame_status():
    try:
        username = session['username']
    except:
        print('INTRUDER')
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
        print('usrs: ', usernames)
        # emit('get username', {'username': username}, session=session)
        emit('player list', {'players': usernames, 'username': username}, session=session)

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

@socketio.on('leave lobby', namespace='/lobby') #player leaving lobby
def leave_lobby():
    try:
        session['username']
    except:
        return False
    # emit('message', {'msg':  session.get('username') + ' has left the room.'}, session=session)