from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import random
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)
db = SQLAlchemy(app)
engine = create_engine('sqlite:///database.db', echo=False)

@app.route('/')
def index():
    return render_template('index.html')

'''
@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('roll dice event')
def test_message():
    emit('my response', {'data': int(random.randint(1,6))}, broadcast=True)

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
'''

@app.route('/gameroom', methods=['GET', 'POST'])
def game_room():
    if(request.method=='POST'):
        username = request.form['username']
        room = request.form['room']
        #Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('game_room.html', session = session)
    else:
        if(session.get('username') is not None):
            return render_template('game_room.html', session = session)
        else:
            return redirect(url_for('index'))

@socketio.on('join', namespace='/gameroom')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)

@socketio.on('text', namespace='/gameroom')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)

@socketio.on('left', namespace='/gameroom')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)

if __name__ == '__main__':
    socketio.run(app)