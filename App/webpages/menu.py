from flask import flash, render_template, redirect, url_for, request, session
from re import search
from App.main import app, db
from App.database.tables import Game, Player, Account
from App.misc.functions import get_correct_location
from random import randint
from flask_socketio import emit

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    page, game_code = get_correct_location()
    if page != 'menu':
        if game_code == None:
            return redirect(url_for(page))
        return redirect(url_for(page, game_code=game_code))
    
    if request.method == 'GET':
        return render_template('menu.html')
    
    formType = request.form.get('button')
    if formType == "Join":
        code = request.form.get('code')
        if search("^\d{6}$", code):
            return join_game(code)
        else:
            flash("Code was not valid")
            return render_template('menu.html')
    else:
        username = session['username']
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
    player = Player(position=0, index_in_game=0, money=1000, turns_in_jail=0, symbol=randint(0,7))
    account.game_instances.append(player)
    game.players_connected.append(player)
    db.session.add(player)
    db.session.add(game)
    db.session.commit()
    if True:
        from App.misc.functions import load_test_data
        load_test_data(player)
    session['game_code'] = new_id
    return redirect(url_for('lobby'))

def join_game(code):
    game = Game.query.filter_by(game_code=code).first()
    if not game:
        flash("Code was not valid")
        return render_template('menu.html')
    
    if game.game_started:
        flash("Game has already started, please pick on the list!!")
        return render_template('menu.html')
    
    account = Account.query.filter_by(username=session['username']).first()
    usernames_in_game = [i.username for i in game.players_connected]
    if account.username in usernames_in_game:
        flash("You are already in this game")
        return render_template('menu.html')
    
    # If there are fewer than 8 players, the index of a random unused sprite is chosen
    players_symbols = [i.symbol for i in game.players_connected]
    if len(players_symbols) < 7:
        symbol = randint(0,6)
        while symbol in players_symbols:
            symbol = randint(0,6)

    player = Player(position=0, index_in_game=len(game.players_connected), symbol=symbol, money=1000, turns_in_jail=0)
    account.game_instances.append(player)
    game.players_connected.append(player)
    db.session.add(player)
    db.session.commit()
    session['game_code'] = code
    flash("Game joined!")

    

    return redirect(url_for('lobby'))