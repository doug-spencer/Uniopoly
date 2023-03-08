from sqlalchemy import update
from App.main import db
from App.database.tables import link_player_bus_stop, link_player_property, link_player_utilities, link_player_student_union, link_player_email

def query_property(player_id, secondary_id, mortgage, houses):
    if str(houses) !='None':
        stmt = (
            update(link_player_property).
            where(link_player_property.c.player_id == player_id).
            where(link_player_property.c.property_id == secondary_id).
            values(houses=houses)
        )
        db.session.execute(stmt)
        db.session.commit()
    if str(mortgage) != 'None':
        stmt = (
            update(link_player_property).
            where(link_player_property.c.player_id == player_id).
            where(link_player_property.c.property_id == secondary_id).
            values(mortgaged=mortgage)
        )
        db.session.execute(stmt)
        db.session.commit()

def query_utilites(player_id, secondary_id, mortgaged):
    if str(mortgaged) !='None':
        stmt = (
            update(link_player_utilities).
            where(link_player_utilities.c.player_id == player_id).
            where(link_player_utilities.c.utilities_id == secondary_id).
            values(mortgaged=mortgaged)
        )
        db.session.execute(stmt)
        db.session.commit()

def query_student_union(player_id, secondary_id, mortgaged):
    if str(mortgaged) !='None':
        stmt = (
            update(link_player_student_union).
            where(link_player_student_union.c.player_id == player_id).
            where(link_player_student_union.c.student_union_id == secondary_id).
            values(mortgaged=mortgaged)
        )
        db.session.execute(stmt)
        db.session.commit()

def query_email(player_id, secondary_id, mortgaged):
    if str(mortgaged) !='None':
        stmt = (
            update(link_player_email).
            where(link_player_email.c.player_id == player_id).
            where(link_player_email.c.email_id == secondary_id).
            values(mortgaged=mortgaged)
        )
        db.session.execute(stmt)
        db.session.commit()

def query_bus_stop(player_id, secondary_id, mortgaged):
    if str(mortgaged) !='None':
        stmt = (
            update(link_player_bus_stop).
            where(link_player_bus_stop.c.player_id == player_id).
            where(link_player_bus_stop.c.bus_stop_id == secondary_id).
            values(mortgaged=mortgaged)
        )
        db.session.execute(stmt)
        db.session.commit()