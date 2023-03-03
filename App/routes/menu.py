from flask import flash, render_template, redirect, url_for, request, session
from re import search
from App.main import app, db
from App.database.tables import Game, Player, Account
from App.misc.functions import check_account
from random import randint

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    try:
        username = session['username']
    except: #player isnt in session (hasnt logged in)
        return False

    if request.method == 'GET':
        # temp code
        flash("current game codes:")
        for game in Game.query.all():
            flash(game.game_code)
        return render_template('menu.html')
    formType = request.form.get('button')

    if formType == "Join":
        code = request.form.get('code')
        if search("^\d{6}$", code):
            return join_game(code)
    else:
        return create_game(username)
    
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