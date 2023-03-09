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

def player_on_jail(player, game_code, session):
    print("hellooooo")
    if player.turns_in_jail == 0:
        emit('message', {'msg': f'{player.username} is on jail'}, room=game_code)
    elif player.turns_in_jail == 1:
        emit('message', {'msg': f'{player.username} must pay 50 or use a get out of jail free card'}, room=game_code)
        player.turns_in_jail = 0  # fixed assignment here
    else:
        print("arfadsadsf")
        emit('message', {'msg': f'{player.username} has {player.turns_in_jail} turns left in jail'}, room=game_code)
    player.turns_in_jail = max(0, player.turns_in_jail-1)  # fixed assignment here
    db.session.commit()

def player_landed_on_start(player, game_code, session):
    emit('message', {'msg': player.username + ' passed go '}, room=game_code)

def player_landed_on_free_parking(player, game_code, session):
    emit('message', {'msg': player.username + ' is on free parking '}, room=game_code)

def player_landed_on_go_to_jail(player, game_code, session):
    player.turns_in_jail += 3
    player.position = 9
    db.session.commit()
    emit('message', {'msg': player.username + str(player.position) + str(player.turns_in_jail) +' is sent to jail'}, room=game_code)

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

def player_landed_on_bus_stop(player, game_code, session, bus_stop):
    
    emit('message', {'msg': player.username + ' landed on ' + bus_stop.name}, room=game_code)
    # Checks if bus stop is already owned
    b_link_player = db.session.query(link_player_bus_stop).all()
    b_owned = False
    for i in b_link_player:
        if i.bus_stop_id == bus_stop.id:
            b_owned = True
            owned_bus_stop = i
            break
    if b_owned: # If owned rent is paid and if cant pay players money is sent to other player and player_removed_from_game function called
         
        emit('message', {'msg': bus_stop.name + ' is owned by ' + owned_bus_stop.player.username}, room=game_code)
        rent_list = bus_stop.rents.split(',')
        rent = rent_list[owned_bus_stop.number_of_bus_stops_owned - 1]
        if player.money >= rent:
            emit('message', {'msg': player.username + ' owes ' + owned_bus_stop.player.username + ' §' + rent + ' as rent'}, room=game_code)
            player.money -= int(rent)
            owned_bus_stop.player.money += int(rent)
            db.session.commit()
        else:
            # emit message to player that they dont have enough money to pay and they will be removed from the game
            emit('message', {'msg': player.username + ' does not have enough money to pay rent and will be removed from the game'}, room=game_code)
            # send all money to owner of bus stop
            owned_bus_stop.player.money += player.money
            # remove player from game
            remove_player(player, owned_bus_stop, game_code, session)


            
        
        

    else: # If not owned, the option to buy the bus stop is given
        game_code = session.get('game_code')
        username = session.get('username')
        game, player = check_in_game(game_code, username)
        if not game and not player:
            return False
        
        emit('buy bus stop button change', {'operation': 'show'}, session=session)
        emit('message', {'msg': 'Click Buy to buy the bus stop for §' + str(bus_stop.buy_price)}, room=game.game_code)

# function that is called when a player has to be removed from the game because they have no money








