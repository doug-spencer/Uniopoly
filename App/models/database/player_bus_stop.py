from sqlalchemy import Column, Integer
from App.main import db

link_player_bus_stop = db.Table('link_player_bus_stop',
        Column('username', Integer, db.Foreignkey('player.username'), primary_key=True),
        Column('bus_stop', Integer, db.ForeignKey('bus_stop.id'), primary_key=True)
        )