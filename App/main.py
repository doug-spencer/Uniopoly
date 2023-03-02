from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['SECRET'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
app.app_context().push()
socketio = SocketIO(app, cors_allowed_origins='*')
#socketio = SocketIO(app, logger=True, engineio_logger=True)
db = SQLAlchemy(app)
engine = create_engine('sqlite:///database.db', echo=False)

# if True:
#     try:
#         Game.__table__.drop(engine)
#         Player.__table__.drop(engine)
#     except Exception as e:
#         print(e)

db.session.commit()
from App.routes import index, lobby, menu, help, gameroom
from App.database import database_classes
db.create_all()
db.session.commit()