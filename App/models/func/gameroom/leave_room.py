from flask import session
from flask_socketio import emit, leave_room
from App import socketio

@socketio.on('left', namespace='/gameroom') #leaving room
def left(message):
    game_name = session.get('game_name')
    username = session.get('username')
    leave_room(game_name)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=game_name)