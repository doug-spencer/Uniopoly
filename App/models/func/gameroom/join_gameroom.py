from flask import session
from flask_socketio import emit, join_room
from App.main import socketio

@socketio.on('join', namespace='/gameroom') #player joining room
def join(message):
    game_code = session.get('game_code')
    join_room(game_code)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room = game_code)