from App.database.tables import Player, Game, Account, Property, Utilities, Bus_stop, link_player_property
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
    print("hellooooo")
    if player.turns_in_jail == 0:
        emit('message', {'msg': f'{player.username} is on jail'}, room=game_code)
    elif player.turns_in_jail == 1:
        emit('message', {'msg': f'{player.username} must pay 50 or use a get out of jail free card'}, room=game_code)
        player.turns_in_jail == 0
    else:
        print("arfadsadsf")
        emit('message', {'msg': f'{player.username} has {player.turns_in_jail} turns left in jail'}, room=game_code)
    player.turns_in_jail -= 1
    player.turns_in_jail == max(0, player.turns_in_jail-1)
    db.session.commit()


def player_landed_on_go_to_jail(player, game_code, session):
    player.turns_in_jail += 3
    player.position = 9
    db.session.commit()
    emit('message', {'msg': player.username + str(player.position) + str(player.turns_in_jail) +' is sent to jail'}, room=game_code)

def player_landed_on_utility(player, game_code, session, utility):
    emit('message', {'msg': player.username + ' landed on ' + utility.name}, room=game_code)

def player_landed_on_property(player, game_code, session, property):
    emit('message', {'msg': player.username + ' landed on  the property: ' + property.name}, room=game_code)

def update_position(game, game_code):
    positions = [[i, None] for i in range(40)]
    for i in game.players_connected:
        if positions[i.position][1] == None:
            positions[i.position][1] = i.username
        else:
            positions[i.position][1] = positions[i.position][1] + ',' + i.username
    positions = [i for i in positions if i[1]!= None]
    print(positions, game.game_code)
    emit('update player positions', {'positions': positions}, room=game_code) 

def player_landed_on_bus_stop(player, game_code, session, bus_stop):
    emit('message', {'msg': player.username + ' landed on ' + bus_stop.name}, room=game_code)

def player_landed_on_card(player, game_code, session, card):
    emit('message', {'msg': player.username + ' landed on a pick up card square '}, room=game_code)