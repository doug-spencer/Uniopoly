from flask import session
from App.main import db, socketio

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