from App.database.tables import Account, Game, Player
from flask import render_template, request, session, redirect, url_for, flash

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

def take_to_right_page():
    try:
        username = session['username']
        player = Player.query.filter_by(username=username).first()
    except: #user isnt logged in
        return redirect(url_for("game_room"))
    if not player:
        return redirect(url_for("game_room"))
    print(player.game_code)
    game = Game.query.filter_by(game_code=player.game_code).first()
    if game == None:
        flash("your not in any games")
        return render_template("menu")
    if game.game_started:
        return redirect(url_for("game_room"))
    return redirect(url_for("lobby", game_code=game.game_code))
