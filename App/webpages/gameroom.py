from flask import session, request, render_template, url_for, redirect
from App.main import app, db
from App.database.tables import Account, Game

@app.route('/gameroom', methods=['GET', 'POST'])
def game_room():
    if(request.method=='POST'): #player has made a game or is joining one
        username = request.form['username']
        choice = request.form['choice'] #if the made a game or the name of the game they joined
        account = Account.query.filter_by(username=username).first()
        if not account: #player doesnt have account
            account = Account(username=username)
            db.session.add(account)
        player = player.Player(position=0)
        db.session.add(player)
        account.game_instances.append(player) #links account with the player in the new game
        if choice == 'make': #imaking a game
            game_name = request.form['game_name']
            game = Game(game_name=game_name, index_of_turn=0, game_started=False)
            db.session.add(game)
        else: #joining game
            game_name = choice
            game=Game.query.filter_by(game_name=choice).first()
        game.players_connected.append(player)#adds player to game    
        player.index_in_game = len(game.players_connected) - 1
        db.session.commit()
        #Store the data in session
        session['username'] = username
        session['game_name'] = game_name
        #session_id[player.id] = session.get('session_id') 
        return render_template('game_room.html', session = session)
    else: 
        return render_template('game_room.html', session = session)