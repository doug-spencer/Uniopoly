from App.database.tables import Account, Game, Player, Property, Utilities, Bus_stop, link_player_bus_stop, link_player_property, link_player_utilities
from flask import render_template, request, session, redirect, url_for, flash
from App.main import db
from App.database.link_table_updates import update_link_table


def check_account(username):
    account = Account.query.filter_by(username=username).first()
    if not account:
        return False
    return account

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
    elif True:
        player1.money = 0
    else:
        pass
        #sell houses
        #mortgage utilities
        #...
    db.session.commit()

def load_test_data(player):
    return
    for i in range(3): #add all light blue
        property = Property.query.filter_by(id=i+4).first()
        print(property.name)
        player.properties.append(property)
        db.session.commit()
        query_property(player.id,  property.id, False, 0)
    for i in range(2): #add all utilites
        utility = Utilities.query.filter_by(id=i+1).first()
        print(utility.name)
        player.utilities.append(utility)
        db.session.commit()
        query_utilites(player.id,  utility.id, 0)
    for i in range(2): #add the first 2 bus stops
        bus_stop = Bus_stop.query.filter_by(id=i+1).first()
        print(bus_stop.name)
        player.bus_stop.append(bus_stop)
        db.session.commit()
        query_bus_stop(player.id, bus_stop.id, 0)