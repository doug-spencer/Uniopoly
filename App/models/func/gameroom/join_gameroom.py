from flask import session
from flask_socketio import emit, join_room
from App import socketio

@socketio.on('join', namespace='/gameroom') #player joining room
def join(message):
    game_name = session.get('game_name')
    join_room(game_name)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=game_name)