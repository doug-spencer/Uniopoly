from flask import session
from flask_socketio import emit
from App import socketio

@socketio.on('text', namespace='/gameroom') #sending text
def text(message):
    game_name = session.get('game_name')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=game_name)