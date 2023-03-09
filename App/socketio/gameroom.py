from flask import session
from flask_socketio import emit, join_room, leave_room
from App.main import db, socketio
from App.misc.functions import check_in_game
from random import randint
from App.gamelogic import gamelogic
from App.database.tables import link_player_property, Player, Game, Property

@socketio.on('join', namespace='/gameroom') #player joining room
def join(message):
    game_code = session.get('game_code')
    if game_code == None:
        return False
    join_room(game_code)
    players = Game.query.filter_by(game_code=game_code).first().players_connected
    player_usernames = [player.username for player in players]
    player_money = [player.money for player in players]
    emit('init leaderboard', {'username': player_usernames, 'money': player_money})
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room = game_code)

@socketio.on('left', namespace='/gameroom') #leaving room
def left(message):
    game_code = session.get('game_code')
    username = session.get('username')
    leave_room(game_code)
    player = Player.query.filter_by(username = username, game_code=game_code).first()
    db.session.delete(player)
    db.session.commit()
    game= Game.query.filter_by(game_code=game_code).first()
    for i in game.players_connected:
        print(i.username)
    emit('status', {'msg': username + ' has left the room.'}, room = game_code)

@socketio.on('roll dice', namespace='/gameroom') #when a player rolls the dice
def roll_dice():
    game_code = session.get('game_code')
    username = session.get('username')
    game, player = check_in_game(game_code, username)

    if not game or not player:
        return False
    
    roll1 = randint(1,6)
    roll2 = randint(1,6)
    roll_value = roll1 + roll2
    current_value = player.position
    new_value = roll_value + current_value

    if new_value > 39:
        new_value -= 40

    turn = game.index_of_turn

    if turn == len(game.players_connected) - 1:
        game.index_of_turn = 0
    else:
        game.index_of_turn = game.index_of_turn + 1

    #only emits roll message and updates position if player is not in jail
    if player.turns_in_jail == 0:
        player.position = new_value
        emit('message', {'msg': player.username + ' rolled a ' + str(roll_value) + ' they are now at positon ' + str(new_value)}, room = game_code)
        emit('dice_roll', {'dice_value': roll_value, 'position': new_value}, session=session)   
        gamelogic.update_position(game, game_code)
    db.session.commit()
    
    #performs action associated with board position
    gamelogic.show_player_options(player, game_code, session)
    
    #emit('dice_roll', {'dice_value': roll_value, 'position': new_value}, session=session_id[player.id])##dougs not sure what this is

@socketio.on('text', namespace='/gameroom') #sending text
def text(message):
    game_code = session.get('game_code')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room = game_code)

@socketio.on('update turn', namespace='/gameroom') #check if its players turn yet (if roll dice button should be shown)
def update_turn():
    game_code = session.get('game_code')
    username = session.get('username')
    game, player = check_in_game(game_code, username)
    if not game and not player:
        return False
    if game.index_of_turn == player.index_in_game:
        #emit('roll dice button change', {'operation': 'show'}, session=session_id[player.id])
        emit('roll dice button change', {'operation': 'show'}, session = session)
        emit('message', {'msg': 'It is ' + player.username + ' turn to roll the dice'}, room = game.game_code)
    else:
        #emit('roll dice button change', {'operation': 'hide'}, session=session_id[player.id])
        emit('roll dice button change', {'operation': 'hide'}, session = session)

@socketio.on('buy-property', namespace='/gameroom') #When player presses buy button
def buy_property():
    game_code = session.get('game_code')
    username = session.get('username')
    game, player = check_in_game(game_code, username)
    if not game and not player:
        return False
    pos = player.position
    all_properties = Property.query.all()
    index_of_properties = [i.position for i in all_properties]
    property = all_properties[index_of_properties.index(pos)]
    # Subtracts cost from money and adds new record of property ownership
    player.money -= property.buy_price
    insert_stmnt = link_player_property.insert().values(username=player.username, property_id=property.id, houses=0)
    db.session.execute(insert_stmnt)
    db.session.commit()

    emit('message', {'msg': property.name + ' has been purchased for ' + str(property.buy_price)}, room=game_code)
