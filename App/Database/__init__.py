from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import Account, Game, Player
import Controller

db = SQLAlchemy(app)
engine = create_engine('sqlite:///database.db', echo=False)

#admin1 = Account(username='jacob')
#db.session.add(admin1)
#db.session.add(Game(game_name='wooga'))
db.create_all()
db.session.commit()