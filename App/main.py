from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['SECRET'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
app.app_context().push()
socketio = SocketIO(app, cors_allowed_origins='*')
db = SQLAlchemy(app)
engine = create_engine('sqlite:///database.db', echo=False)

# if True:
#     try:
#         Game.__table__.drop(engine)
#         Player.__table__.drop(engine)
#     except Exception as e:
#         print(e)

db.session.commit()

from App.webpages import login, menu, lobby, gameroom, help, logout
from App.database import tables
from App.socketio import gameroom, lobby

db.create_all()
db.session.commit()