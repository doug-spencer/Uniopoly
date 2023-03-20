from App.database.tables import Account, Game, Player, Property, Utilities, Bus_stop, link_player_bus_stop, link_player_property, link_player_utilities
from flask import render_template, request, session, redirect, url_for, flash
from App.main import db
from App.database.link_table_updates import update_link_table, query_link_table_with_one_id, query_link_table_with_two_id
from flask_socketio import emit, leave_room
from App.misc import gamelogic


def check_account(username, password):
    account = Account.query.filter_by(username=username, password=password).first()
    if not account:
        return False
    return account

def check_username(username):
    account = Account.query.filter_by(username=username).first()
    if not account:
        return False
    return True

def get_account_usernames():
    accounts = Account.query.all()
    account_usernames = []
    for i in accounts:
        account_usernames.append(i.username)
    print(account_usernames)
    return account_usernames

def check_in_game(game_name, username): #verification fucntion
    game = Game.query.filter_by(game_code = game_name).first()
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

def get_correct_location():
    try:
        username = session['username']
        player = Player.query.filter_by(username=username).first()
    except: #user isnt logged in
        print(1)
        return "login", None
    if player == None:
        print(2)
        return "menu", None
    try:
        game_code = session['game_code']
    except:
        return "menu", None
    game = Game.query.filter_by(game_code=game_code).first()
    if game == None:
        flash("your not in any games")
        print(3)
        return "menu", None
    if game.game_started:
        print(4)
        return "game_room", None
    print(5)
    return "lobby", game.game_code

def player1_owes_player2_money(player1, amount, player2=False):
    if player1.money >= amount:
        player1.money -= amount
        if player2:
            player2.money += amount
            emit('message', {'msg': player1.username + " payed " + player2.username + " " + str(amount)}, session=session)
        db.session.commit()
        return "debt paid"

    else:
        total_money = player1.money
        house_price = 0
        #get worth of all houses
        property = query_link_table_with_one_id(player1.id, None, link_player_property, None)
        for i in property:
            card = Property.query.filter_by(id=i[1]).first()
            house_price += gamelogic.get_house_price(card.colour)
            total_money += house_price * i[3]

        #add up unmortgaged cards
        utilities =  query_link_table_with_one_id(player1.id, None, link_player_utilities, None)
        bus_stop = query_link_table_with_one_id(player1.id, None, link_player_bus_stop, None)
        all_cards = [[property, Property], [utilities, Utilities], [bus_stop, Bus_stop]]
        for i in all_cards:
            for j in i[0]:
                if not j[2]: #unmortgaged
                    card = i[1].query.filter_by(id=j[1]).first()
                    total_money += card.morgage_value
        if total_money >= amount:
            need_to_free_up = amount - player1.money
            emit('message', {'msg': player1.username + "needs to sell things to free up " + str(need_to_free_up)}, session=session)
            return "debt not paid"
        else:
            bankrupt_player(player1)
            return "bankrupt"
        
def load_test_data(player):
    for i in range(8): #add all light blue
        property = Property.query.filter_by(id=i+3).first()
        print(property.name)
        player.properties.append(property)
        db.session.commit()
        update_link_table(player.id,  property.id, link_player_property, False)
        update_link_table(player.id,  property.id, link_player_property, None, 0)
    for i in range(2): #add all utilites
        utility = Utilities.query.filter_by(id=i+1).first()
        print(utility.name)
        player.utilities.append(utility)
        db.session.commit()
        update_link_table(player.id,  property.id, link_player_utilities, False)
    for i in range(2): #add the first 2 bus stops
        bus_stop = Bus_stop.query.filter_by(id=i+1).first()
        print(bus_stop.name) 
        player.bus_stop.append(bus_stop)
        db.session.commit()
        update_link_table(player.id,  property.id, link_player_bus_stop, False)

def bankrupt_player(player):
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
    session.pop('game_code', None)
