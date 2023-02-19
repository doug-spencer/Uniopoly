from sqlalchemy import Column, Integer
from App import db

link_player_utilities = db.Table('link_player_utilities',
        Column('username', Integer, db.ForeignKey('player.username'), primary_key=True),
        Column('utilities_id', Integer, db.ForeignKey('utilities.id'), primary_key=True)
        )