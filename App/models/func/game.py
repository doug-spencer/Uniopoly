from flask import flash, redirect, render_template, session, url_for
from App.main import db
from App.database.database_classes import Game, Account, Player
from App.models.auth import check_account
from random import randint

def create_game(username):
    new_id = ""
    unique = False
    while not unique:
        unique = True
        new_id = ""
        for i in range(6):
            new_id += str(randint(0, 9))
        if Game.query.filter_by(game_code=int(new_id)).first():
            unique = False
    account = Account.query.filter_by(username=username).first()
    game = Game(game_code=int(new_id), index_of_turn=0, game_started=False)
    player = Player(position=0, index_in_game=len(game.players_connected), money=7)
    account.game_instances.append(player)
    game.players_connected.append(player)
    db.session.add(player)
    db.session.add(game)
    db.session.commit()
    session['game_code'] = new_id 
    flash("Game created with code " + new_id)
    return redirect(url_for('lobby'))

def join_game(code):
    game = Game.query.filter_by(game_code=code).first()
    if not game:
        flash("Code was not valid")
        return render_template('menu.html')

    account = check_account(session['username'])
    player = Player(position=0, index_in_game=len(game.players_connected), money=7)
    account.game_instances.append(player)
    game.players_connected.append(player)
    db.session.add(player)
    db.session.commit()
    flash("Game joined!")
    session['game_code'] = code 
    return redirect(url_for('lobby'))