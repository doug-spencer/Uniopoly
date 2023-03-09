from App.database.tables import Game, Account, Property, Utilities, Bus_stop, link_player_property, link_player_bus_stop
from flask_socketio import emit
from App.main import db, socketio

def check_in_game(game_code, username):
    game = Game.query.filter_by(game_code=game_code).first()
    if not game:
        raise ValueError(f"No game found with game code {game_code}")
    account = Account.query.filter_by(username=username).first()
    if not account:
        raise ValueError(f"No account found with username {username}")
    player = next((p for p in game.players_connected if p.username == username), None)
    if not player:
        raise ValueError(f"Player {username} not found in game {game_code}")
    return game, player

def check_in_game(game_code, username): #verification fucntion
    game = Game.query.filter_by(game_code = game_code).first()
    if not game:
        return False, False
    account = Account.query.filter_by(username=username).first()
    if not account:
        return False, False
    player = False
    for i in game.players_connected:
        if i.username == username:
            player = i
    if not player:
        return False, False
    return game, player

def show_player_options(player, game_code, session):
    #return False #while db is empty
    pos = player.position

    all_properties = Property.query.all()
    index_of_properties = [i.position for i in all_properties]
    print(index_of_properties)
    if pos in index_of_properties:
        player_landed_on_property(player, game_code, session, all_properties[index_of_properties.index(pos)])
    
    all_utilities = Utilities.query.all()
    index_of_utilities = [i.position for i in all_utilities]
    if pos in index_of_utilities:
        player_landed_on_utility(player, game_code, session, all_utilities[index_of_utilities.index(pos)])
    
    all_bus_stops = Bus_stop.query.all()
    index_of_bus_stops = [i.position for i in all_bus_stops]
    if pos in index_of_bus_stops:
        player_landed_on_bus_stop(player, game_code, session, all_bus_stops[index_of_bus_stops.index(pos)])
    
    # all_emails = Email.query.all()
    # index_of_emails = [i.position for i in all_emails]
    # if pos in index_of_emails:
    #     player_landed_on_card(player, game, session, all_emails[index_of_emails.index(pos)])
    
    # all_student_unions = Student_union.query.all()
    # index_of_student_unions = [i.position for i in all_student_unions]
    # if pos in index_of_student_unions:
    #     player_landed_on_card(player, game, session, all_student_unions[index_of_student_unions.index(pos)])
    
    pos_go_to_jail = 29
    pos_free_parking = 19
    pos_jail = 9
    pos_start = 0
    if pos == pos_go_to_jail:
        player_landed_on_go_to_jail(player, game_code, session)
    if pos == pos_jail:
        player_on_jail(player, game_code, session)
    if pos == pos_start:
        player_landed_on_start(player, game_code, session)
    if pos == pos_free_parking:
        player_landed_on_free_parking(player, game_code, session)

def player_landed_on_property(player, game_code, session, property):
    emit('message', {'msg': f"{player.username} landed on the property: {property.name}"}, room=game_code)
    # # check who owns the property
    # link = link_player_property.query.filter_by(property_id=property.id).first()
    # if not link:
    #     # property is not owned
    #     buy_property(player, property, game, session, game_code)
    # else:
    #     # property is owned
    #     pay_rent(player, link, property, game_code)

    # chek if property is owned by someone 
    link = link_player_property.query.filter_by(property_id=property.id).first()
    if not link:
        # property is not owned
        buy_property(player, property, game, session, game_code)
    else:
        # property is owned
        pay_rent(player, link, property, game_code)
    

        



   

    


  

def pay_rent(player, link, property, game_code):
    emit('message', {'msg': f"{property.name} is owned by {link.player.username}"}, room=game_code)
    rent_list = property.rents.split(',')
    rent = rent_list[3]
    emit('message', {'msg': f"{player.username} owes {link.player.username} §{rent}"}, room=game_code)
    if player.money >= int(rent):
        player.money -= int(rent)
        link.player.money += int(rent)
        db.session.commit()
    else:
        remove_player(player, link, game_code, session)

def buy_property(player, property, game, session, game_code):
    emit('buy property button change', {'operation': 'show'}, session=session)
    emit('message', {'msg': f"Click Buy to buy the card for §{property.buy_price}"}, room=game_code)

def remove_player(player, link, game_code, session):
    link.player.money += player.money
    player.money = 0
    db.session.commit()
    player_removed_from_game(player, game_code, session)

#  add function that allows player to mortgage property
# 1. check if player owns property
# 2. if player owns property, check if property is mortgaged
# 3. if property is not mortgaged, mortgage property
# 4. if property is mortgaged, unmortgage property
def mortgage(player, property, game_code, session):
    link = link_player_property.query.filter_by(property_id=property.id).first()
    if not link:
        emit('message', {'msg': f"{player.username} does not own {property.name}"}, room=game_code)
    else:
        if link.mortgaged == False:
            link.mortgaged = True
            player.money += property.mortgage_price
            db.session.commit()
            emit('message', {'msg': f"{player.username} mortgaged {property.name}"}, room=game_code)
        else:
            link.mortgaged = False
            player.money -= property.mortgage_price
            db.session.commit()
            emit('message', {'msg': f"{player.username} unmortgaged {property.name}"}, room=game_code)






