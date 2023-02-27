from flask import session
from flask_socketio import emit, leave_room
from App.main import socketio

@socketio.on('left', namespace='/gameroom') #leaving room
def left(message):
    game_code = session.get('game_code')
    username = session.get('username')
    leave_room(game_code)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room = game_code)