from sqlalchemy import update, and_, select
from App.main import db
#from App.database.tables import link_player_student_union, link_player_email

def update_link_table(player_id, card_id, table, mortgaged, houses=None):
    if str(houses) != 'None':
        stmt = (
            update(table).
            where(table.c.player_id == player_id).
            where(table.c.card_id == card_id).
            values(houses=houses)
        )
    else:
        stmt = (
            update(table).
            where(table.c.player_id == player_id).
            where(table.c.card_id == card_id).
            values(mortgaged=mortgaged)
        )
    db.session.execute(stmt)
    db.session.commit()

'''
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
            where(link_player_bus_stop.c.card_id == secondary_id).
            values(mortgaged=mortgaged)
        )
        db.session.execute(stmt)
        db.session.commit()

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
            where(link_player_property.c.card_id == secondary_id).
            values(mortgaged=mortgage)
        )
        db.session.execute(stmt)
        db.session.commit()
    else:
        pass
        #sell houses
        #mortgage utilities
        #...
    db.session.commit()

def query_utilites(player_id, secondary_id, mortgaged):
    if str(mortgaged) !='None':
        stmt = (
            update(link_player_utilities).
            where(link_player_utilities.c.player_id == player_id).
            where(link_player_utilities.c.card_id == secondary_id).
            values(mortgaged=mortgaged)
        )
        db.session.execute(stmt)
        db.session.commit()
'''

'''
def query_link_table(player_id, card_id, table, houses=False):
    if not houses:
        result = table.query.filter_by(player_id=player_id, card_id=card_id).first()
        if result:
            return result.mortgaged
    else:
        result = table.query.filter_by(player_id=player_id, card_id=card_id).first()
        if result:
            return result.houses
'''
def query_link_table_with_two_id(player_id, card_id, table, houses=None):
    if str(houses) != 'None':
        stmt = select([
            table.columns.houses
        ]).where(and_(
            table.columns.player_id == player_id,
            table.columns.card_id == card_id
        ))
    else:
        stmt = select([
            table.columns.mortgaged
        ]).where(and_(
            table.columns.player_id == player_id,
            table.columns.card_id == card_id
        ))
    results = db.session.execute(stmt).fetchall()
    for i in results:
        print(i)
    return ''

def query_link_table_with_one_id(player_id, card_id, table, houses=None):
    if str(houses) != 'None':
        stmt = select((
            table.columns.player_id,
            table.columns.card_id,
            table.columns.houses
        )).where(and_(
    table.columns.player_id == player_id if player_id else table.columns.card_id == card_id
        ))
    else:
        stmt = select((
            table.columns.player_id,
            table.columns.card_id,
            table.columns.mortgaged
        )).where(and_(
    table.columns.player_id == player_id if player_id else table.columns.card_id == card_id
        ))
    results = db.session.execute(stmt).fetchall()
    for i in results:
        print(i)
    return ''