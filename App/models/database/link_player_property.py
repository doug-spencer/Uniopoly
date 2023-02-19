from sqlalchemy import Column, Integer
from App import db

link_player_property = db.Table('link_player_property',
        Column('username', Integer, db.ForeignKey('player.username'), primary_key=True),
        Column('property_id', Integer, db.ForeignKey('property.id'), primary_key=True),
        Column('houses', Integer)
        )