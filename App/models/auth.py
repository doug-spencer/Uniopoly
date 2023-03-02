from App.database.database_classes import Account, Game
from flask import redirect, render_template, request, session, url_for
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

def login():
    username = request.form.get("loginname")
    account = check_account(username)
    if account:
        print("You can log in")
        session['username'] = username
        return redirect(url_for('menu'))
    else:
        print("Account doesn't exist")
        return render_template('login.html')

def signup():
    username = request.form.get("signupname")
    account = check_account(username)
    if account:
        print("Account taken")
        return render_template('login.html')
    else:
        new_account = Account(username=username)
        db.session.add(new_account)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('menu'))