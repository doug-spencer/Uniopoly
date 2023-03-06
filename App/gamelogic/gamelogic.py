from App.database.tables import Game, Account, Property, Utilities, Bus_stop, link_player_property
from flask_socketio import emit
from App.main import db, socketio


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

def player_landed_on_start(player, game_code, session):
    emit('message', {'msg': player.username + ' passed go '}, room=game_code)

def player_landed_on_free_parking(player, game_code, session):
    emit('message', {'msg': player.username + ' is on free parking '}, room=game_code)

def player_on_jail(player, game_code, session):
    if player.turns_in_jail == 0:
        emit('message', {'msg': f'{player.username} is on jail'}, room=game_code)
    elif player.turns_in_jail == 1:
        emit('message', {'msg': f'{player.username} must pay 50 or use a get out of jail free card'}, room=game_code)
        player.turns_in_jail == 0
    else:
        emit('message', {'msg': f'{player.username} has {player.turns_in_jail} turns left in jail'}, room=game_code)
    player.turns_in_jail -= 1
    player.turns_in_jail == max(0, player.turns_in_jail-1)
    db.session.commit()


def player_landed_on_go_to_jail(player, game_code, session):
    player.turns_in_jail += 3
    player.position = 9
    db.session.commit()
    emit('message', {'msg': player.username + ' is sent to jail'}, room=game_code)

def player_landed_on_utility(player, game_code, session, utility):
    emit('message', {'msg': player.username + ' landed on ' + utility.name}, room=game_code)

def player_landed_on_property(player, game_code, session, property):
    @socketio.on('buy-property', namespace='/gameroom') #When player presses buy button
    def buy_property():
        game_code = session.get('game_code')
        username = session.get('username')
        game, player = check_in_game(game_code, username)
        if not game and not player:
            return False
        
        #Subtracts cost from money and adds new record of property ownership
        player.money -= property.buy_price
        insert_stmnt = link_player_property.insert().values(username=player.username, property_id=property.id, houses=0)
        db.session.execute(insert_stmnt)
        db.session.commit()

        emit('message', {'msg': property.name + ' has been purchased for ' + str(property.buy_price)}, room=game_code)

    emit('message', {'msg': player.username + ' landed on  the property: ' + property.name}, room=game_code)
    # Checks if property is already owned
    p_link_player = db.session.query(link_player_property).all()
    p_owned = False
    for i in p_link_player:
        if i.property_id == property.id:
            p_owned = True
            owned_property = i
            break
    if p_owned: # If owned rent is payed
        emit('message', {'msg':property.name + ' is owned by me'}, room=game_code)
        rent_list = property.rents.split(',')
        rent = rent_list[3]
        emit('message', {'msg': player.username + ' owes me §' + rent}, room=game_code)
        player.money -= int(rent)
        db.session.commit()
    else: # If not owned, the option to buy the property is given
        game_code = session.get('game_code')
        username = session.get('username')
        game, player = check_in_game(game_code, username)
        if not game and not player:
            return False
        
        emit('buy property button change', {'operation': 'show'}, session=session)
        emit('message', {'msg': 'Click Buy to buy the card for §' + str(property.buy_price)}, room=game.game_code)



def player_landed_on_bus_stop(player, game_code, session, bus_stop):
    emit('message', {'msg': player.username + ' landed on ' + bus_stop.name}, room=game_code)

def player_landed_on_card(player, game_code, session, card):
    emit('message', {'msg': player.username + ' landed on a pick up card square '}, room=game_code)