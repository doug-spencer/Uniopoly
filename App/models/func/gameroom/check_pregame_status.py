from flask import session
from flask_socketio import emit
from App import socketio
from App.models.classes.main import Game, Player

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
        usernames = ''
        for i in game.players_connected:
            usernames += str(i.username) + ', '
        if usernames == '':
            usernames = 'None'
        print('usrs: ', usernames)
        emit('player list', {'players': usernames}, session=session)