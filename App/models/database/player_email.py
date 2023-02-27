from sqlalchemy import Column, Integer
from App.main import db

link_player_email = db.Table('link_player_email',
        Column('username', Integer, db.ForeignKey('player.username'), primary_key=True),
        Column('email', Integer, db.ForeignKey('email.id'), primary_key=True)
        )