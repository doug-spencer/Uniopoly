from flask import flash, redirect, render_template, session, url_for
from App.main import db
from App.models.auth import check_account
from App.database.database_classes import Game, Player

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