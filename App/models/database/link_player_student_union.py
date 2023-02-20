from sqlalchemy import Column, Integer
from app import db

link_player_student_union = db.Table('link_player_student_union',
        Column('username', Integer, db.ForeignKey('player.username'), primary_key=True),
        Column('student_union', Integer, db.ForeignKey('student_union.id'), primary_key=True)
        )