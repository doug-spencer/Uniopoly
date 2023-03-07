from App.database.tables import Account, Game, Player
from flask import render_template, request, session, redirect, url_for, flash
from App.main import db

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
        db.session.commit()
        return True
    return False