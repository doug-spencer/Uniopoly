import os
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['SECRET'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_TYPE'] =\
#     'sqlite:///' + os.path.join(basedir, 'database.db')
app.app_context().push()
socketio = SocketIO(app, cors_allowed_origins='*')
db = SQLAlchemy(app)
#print('sqlite:///' + os.path.join(basedir, 'database.db'))
engine = create_engine('sqlite:///instance/database.db', echo=False)

db.session.commit()

from App.webpages import login, menu, lobby, gameroom, help, logout
from App.database import tables, load_static_files
from App.socketio import gameroom, lobby


if False:
    from App.database.tables import Game, Player
    try:
        Game.__table__.drop(engine)
        Player.__table__.drop(engine)
    except Exception as e:
        print(e)

db.create_all()
db.session.commit()

if False:
    load_static_files.load_static_files()
