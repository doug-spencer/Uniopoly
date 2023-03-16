from flask import session
from flask_socketio import emit, join_room, leave_room
from App.main import db, socketio, engine
from App.misc.functions import check_in_game, player1_owes_player2_money
from random import randint
from sqlalchemy import update
from App.misc import gamelogic
from App.database.tables import link_player_property, link_player_bus_stop, link_player_utilities, Player, Game, Property, Bus_stop, Utilities
from App.database import link_table_updates

@socketio.on('join', namespace='/gameroom') #player joining room
def join(message):
    game_code = session.get('game_code')
    if game_code == None:
        return False
    join_room(game_code)
    players = Game.query.filter_by(game_code=game_code).first().players_connected
    players_arr = [[player.username, player.money] for player in players]
    emit('update leaderboard', {'players': players_arr}, room=game_code)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room = game_code)
    emit('buy property button change', {'operation':'hide'}, session=session)
    emit('get username', {'username': session.get('username')}, session=session)

@socketio.on('left', namespace='/gameroom') #leaving room
def left(message):
    game_code = session.get('game_code')
    username = session.get('username')
    leave_room(game_code)
    player = Player.query.filter_by(username = username, game_code=game_code).first()
    game= Game.query.filter_by(game_code=game_code).first()
    index_of_player = [i.id for i in game.players_connected].index(player.id)
    index = 0
    for i in game.players_connected:
        if index > index_of_player:
            game.players_connected[index].index_in_game = index - 1
        index += 1
    db.session.delete(player)
    db.session.commit()
    emit('status', {'msg': username + ' has left the room.'}, room = game_code)

@socketio.on('end turn', namespace='/gameroom') #when a players turn ends
def end_turn():
    game_code = session.get('game_code')
    username = session.get('username')
    game, player = check_in_game(game_code, username)

    if not game or not player:
        return False
    
    if player.money >= 0:
        resume_player_turn(game_code)
        update_index_of_turn()
    else:
        emit('message', {'msg': 'You need to clear your dept. Sell some houses or mortgage your cards'}, session = session)
    

@socketio.on('roll dice', namespace='/gameroom') #when a player rolls the dice
def roll_dice():
    game_code = session.get('game_code')
    username = session.get('username')
    game, player = check_in_game(game_code, username)

    if not game or not player:
        return False
    
    halt_player_turn(game_code)
    
    roll1 = randint(1,6)
    roll2 = randint(1,6)
    roll_value = roll1 + roll2
    current_value = player.position
    new_value = roll_value + current_value

    if new_value > 39:
        new_value -= 40
        player.money += 200
        emit('message', {'msg': player.username + ' passed go and collected 200'}, room=game_code)


    #only emits roll message and updates position if player is not in jail
    if player.turns_in_jail == 0:
        player.position = new_value
        emit('message', {'msg': player.username + ' rolled a ' + str(roll_value) + ' they are now at positon ' + str(new_value)}, room = game_code)
        emit('dice_roll', {'dice_value': roll_value, 'position': new_value}, session=session)
        gamelogic.update_position(game, game_code)
    db.session.commit()
    
    #performs action associated with board position
    buy_choice_active = gamelogic.show_player_options(player, game_code, session, roll_value)
    if not buy_choice_active:
        print("asdfasdfsdfghgblzvnjjvfij")
        emit('end turn button change', {'operation':'show'}, session=session)

    #emit('dice_roll', {'dice_value': roll_value, 'position': new_value}, session=session_id[player.id])

#increments the index of turn counter in the db
def update_index_of_turn():
    game_code = session.get('game_code')
    username = session.get('username')
    game, player = check_in_game(game_code, username)

    turn = game.index_of_turn

    if turn == len(game.players_connected) - 1:
        game.index_of_turn = 0
    else:
        game.index_of_turn = game.index_of_turn + 1
    db.session.commit()

#transforms the index of turn variable so that it applys to no player
def halt_player_turn(game_code):
    game= Game.query.filter_by(game_code=game_code).first()
    game.index_of_turn = -1 * game.index_of_turn - 1
    db.session.commit()

#returns the index of turn variable to its previous value
def resume_player_turn(game_code):
    game= Game.query.filter_by(game_code=game_code).first()
    game.index_of_turn = (game.index_of_turn + 1) * -1
    db.session.commit()

@socketio.on('get cards', namespace='/gameroom')
def get_cards():
    game_code = session.get('game_code')
    username = session.get('username')
    game, player = check_in_game(game_code, username)
    if not game and not player:
        return False
    unmortgaged_cards, mortgaged_cards,  unmortgaged_cards_id, mortgaged_cards_id= gamelogic.get_cards(player)
    print('cards:', unmortgaged_cards, mortgaged_cards)
    emit('cards', {
        'unmortgaged_cards': unmortgaged_cards, 
        'mortgaged_cards':mortgaged_cards, 
        'unmortgaged_cards_id':unmortgaged_cards_id, 
        'mortgaged_cards_id':mortgaged_cards_id}, 
        session=session
    )

@socketio.on('get houses', namespace='/gameroom')
def get_houses():
    game_code = session.get('game_code')
    username = session.get('username')
    game, player = check_in_game(game_code, username)
    if not game and not player:
        return False
    houses = gamelogic.get_houses(player)
    print(houses)
    emit('houses', {'houses': houses}, session=session)

@socketio.on('text', namespace='/gameroom') #sending text
def text(message):
    game_code = session.get('game_code')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room = game_code)

#check if its players turn yet (if roll dice button should be shown)
@socketio.on('update turn', namespace='/gameroom') 
def update_turn():
    game_code = session.get('game_code')
    username = session.get('username')
    game, player = check_in_game(game_code, username)
    if not game and not player:
        return False
    
    if game.index_of_turn == player.index_in_game:
        emit('roll dice button change', {'operation': 'show'}, session = session)
        emit('message', {'msg': 'It is ' + player.username + ' turn to roll the dice'}, room = game.game_code)
    else:
        emit('roll dice button change', {'operation': 'hide'}, session = session)

    players = [[player.username, player.money] for player in game.players_connected]

    emit('update leaderboard', {'players': players}, room=game_code)

@socketio.on('buy-property', namespace='/gameroom') #When player presses buy button
def buy_property():
    #Validation
    game_code = session.get('game_code')
    username = session.get('username')
    game, player = check_in_game(game_code, username)
    if not game and not player:
        return False
    
    #gathers the indeces of the respective cards on the board
    property_indices = [i.position for i in Property.query.all()]
    bus_stop_indices = [i.position for i in Bus_stop.query.all()]
    utility_indices = [i.position for i in Utilities.query.all()]

    #finds the card the player has landed on
    if player.position in property_indices:
        card = Property.query.filter_by(position=player.position).first()
        insert_stmnt = link_player_property.insert().values(player_id=player.id, card_id=card.id, houses=0)

    if player.position in utility_indices:
        card = Utilities.query.filter_by(position=player.position).first()
        insert_stmnt = link_player_utilities.insert().values(player_id=player.id, card_id=card.id)

    if player.position in bus_stop_indices:
        card = Bus_stop.query.filter_by(position=player.position).first()
        insert_stmnt = link_player_bus_stop.insert().values(player_id=player.id, card_id=card.id)

    card_price = card.buy_price

    #checks the player has enough money to buy the card
    if card_price > player.money:
        emit('message', {'msg':"you too broke to buy this"})
        emit('buy property button change', {'operation':'show'}, session=session)
        return

    #buys the card
    player.money -= card_price

    db.session.execute(insert_stmnt)
    db.session.commit()

    emit('message', {'msg': player.username + ' has bought ' + card.name + ' for ' + str(card_price)}, room=game_code)


    emit('buy property button change', {'operation': 'hide'}, session=session)
    emit('end turn button change', {'operation': 'show'}, session=session)
    #shows the roll dice button and updates the turn
    #gamelogic.resume_player_turn(game_code)
    #update_index_of_turn()


@socketio.on('dont-buy-property', namespace='/gameroom') #When player presses buy button
def dont_buy_property():
    #shows the roll dice button and updates the turn    
    game_code = session.get('game_code')

    emit('message', {'msg': 'card not bought'}, room=game_code)

    resume_player_turn(game_code)
    update_index_of_turn()

@socketio.on('sell house', namespace='/gameroom') 
def sell_house(data):
    print('sell house')
    game_code = session.get('game_code')
    username = session.get('username')
    game, player = check_in_game(game_code, username)
    if not game or not player:
        return False
    player = Player.query.filter_by(username = username, game_code=game_code).first()
    property = Property.query.filter_by(name=data['house']).first()
    houses = link_table_updates.query_link_table_with_two_id(player.id, property.id, link_player_property, True)[0][3]
    if houses == 0:
        emit('message', {'msg':"you don't have any houses on that property"}, session=session)
        return False
    amount = gamelogic.get_house_price(property.colour)
    if amount:
        link_table_updates.update_link_table(player.id, property.id, link_player_property, False, houses - 1)
        player = Player.query.filter_by(username = username, game_code=game_code).first()
        player.money += amount
        db.session.commit()
    else:
        emit('message', {'msg':"you don't have any houses on that property"}, session=session)

@socketio.on('buy house', namespace='/gameroom') 
def buy_house(data):
    print('buy house')
    game_code = session.get('game_code')
    username = session.get('username')
    game, player = check_in_game(game_code, username)
    if not game or not player:
        return False
    player = Player.query.filter_by(username = username, game_code=game_code).first()
    property = Property.query.filter_by(name=data['house']).first()
    houses = link_table_updates.query_link_table_with_two_id(player.id, property.id, link_player_property, True)[0][3]
    if houses == 5:
        emit('message', {'msg':"you already have a hotel on that property"}, session=session)
        return False
    amount = gamelogic.get_house_price(property.colour)
    if player.money >= amount:
        link_table_updates.update_link_table(player.id, property.id, link_player_property, False, houses + 1)
        player1_owes_player2_money(player, amount)
    else:
        emit('message', {'msg':"you don't have enough money to buy the house"}, session=session)



    

