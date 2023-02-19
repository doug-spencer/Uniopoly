from sqlalchemy import Column, Integer
from App import db

link_player_bus_stop = db.Table('link_player_bus_stop',
        Column('username', Integer, db.ForeignKey('player.username'), primary_key=True),
        Column('bus_stop', Integer, db.ForeignKey('bus_stop.id'), primary_key=True)
        )