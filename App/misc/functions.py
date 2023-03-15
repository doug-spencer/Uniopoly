from App.database.tables import Account, Game, Player, Property, Utilities, Bus_stop, link_player_bus_stop, link_player_property, link_player_utilities
from flask import render_template, request, session, redirect, url_for, flash
from App.main import db
from App.database.link_table_updates import update_link_table, query_link_table_with_one_id, query_link_table_with_two_id
from flask_socketio import emit
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
    else:
        total_money = 0
        total_money += player1.money

        #get worth of all houses
        property = query_link_table_with_one_id(player1.id, None, Property, None)
        for i in property:
            card = Property.query.filter_by(property_id=i[1]).all()
            house_price += gamelogic.get_house_price(i.colour)
            total_money += house_price * i[3]

        #add up unmortgaged cards
        utilities =  query_link_table_with_one_id(player1.id, None, Utilities, None)
        bus_stop = query_link_table_with_one_id(player1.id, None, Bus_stop, None)
        all_cards = [[property, Property], [utilities, Utilities], [bus_stop, Bus_stop]]
        for i in all_cards:
            if not i[0][2]: #unmortgaged
                card = i[1].query.filter_by(id=i[0][1]).first()
                total_money += card.mortgage_value
        if total_money >= amount:
            total_money -= amount
        else:
            #bankrupt dem
            pass
    db.session.commit()

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
