from flask import session, request, render_template, url_for, redirect
from flask_socketio import emit, join_room, leave_room
import random
from App import app, socketio, db
from App.models.classes.main import Account, Game, Player
from App.models.auth import check_in_game

@socketio.on('check pregame status', namespace='/lobby') #player updating lobby screen
def check_pregame_status():
    try:
        username = session['username']
    except:
        print('INTRUDER')
        return False
    player = Player.Player.query.filter_by(username=username).first()
    game = Game.Game.query.filter_by(game_code=player.game_code).first()
    if game.game_started:
        emit('game started', session=session)
    else: #updates list of players in game so far
        usernames = ''
        for i in game.players_connected:
            usernames += str(i.username) + ', '
        if usernames == '':
            usernames = 'None'
        print('usrs: ', usernames)
        emit('player list', {'players': usernames}, session=session)

@socketio.on('leave lobby', namespace='/lobby') #player leaving lobby
def leave_lobby():
    try:
        session['username']
    except:
        return False
    #emit('status', {'msg':  session.get('username') + ' has entered the room.'}, session=session)

@app.route('/gameroom', methods=['GET', 'POST'])
def game_room():
    if(request.method=='POST'): #player has made a game or is joining one
        username = request.form['username']
        choice = request.form['choice'] #if the made a game or the name of the game they joined
        account = Account.Account.query.filter_by(username=username).first()
        if not account: #player doesnt have account
            account = Account.Account(username=username)
            db.session.add(account)
        player = Player.Player(position=0)
        db.session.add(player)
        account.game_instances.append(player) #links account with the player in the new game
        if choice == 'make': #imaking a game
            game_name = request.form['game_name']
            game = Game.Game(game_name=game_name, index_of_turn=0, game_started=False)
            db.session.add(game)
        else: #joining game
            game_name = choice
            game=Game.Game.query.filter_by(game_name=choice).first()
        game.players_connected.append(player)#adds player to game    
        player.index_in_game = len(game.players_connected) - 1
        db.session.commit()
        #Store the data in session
        session['username'] = username
        session['game_name'] = game_name
        #session_id[player.id] = session.get('session_id') 
        return render_template('game_room.html', session = session)
    else: 
        if(session.get('username') is not None): #player is already in a session
            return render_template('game_room.html', session = session)
        else: #if not logged in
            games = Game.Game.query.all()
            game_names = []
            for i in games:
                game_names.append(i.game_name)
            return redirect(url_for('index'), games = game_names)

@socketio.on('join', namespace='/gameroom') #player joining room
def join(message):
    game_name = session.get('game_name')
    join_room(game_name)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=game_name)

@socketio.on('roll dice', namespace='/gameroom') #when a player rolls the dice
def roll_dice():
    game_name = session.get('game_name')
    username = session.get('username')
    game, player = check_in_game.check_in_game(game_name, username)
    if not game and not player:
        return False
    roll_value = random.randint(1,6)
    current_value = player.position
    new_value = roll_value + current_value
    if new_value > 39:
        new_value -= 40
    player.position = new_value
    turn = game.index_of_turn
    if turn == len(game.players_connected) - 1:
        game.index_of_turn = 0
    else:
        game.index_of_turn = game.index_of_turn + 1
    db.session.commit()
    emit('message', {'msg': player.username + ' rolled a ' + str(roll_value) + ' they are now at possiton ' + str(new_value)}, room=game_name)
    emit('dice_roll', {'dice_value': roll_value, 'position': new_value}, session=session)
    #emit('dice_roll', {'dice_value': roll_value, 'position': new_value}, session=session_id[player.id])

@socketio.on('update turn', namespace='/gameroom') #check if its players turn yet (if roll dice button should be shown)
def update_turn():
    game_name = session.get('game_name')
    username = session.get('username')
    game, player = check_in_game.check_in_game(game_name, username)
    if not game and not player:
        return False
    if game.index_of_turn == player.index_in_game:
        #emit('roll dice button change', {'operation': 'show'}, session=session_id[player.id])
        emit('roll dice button change', {'operation': 'show'}, session=session)
        emit('message', {'msg': 'It is ' + player.username + ' turn to roll the dice'}, room=game.game_name)
    else:
        #emit('roll dice button change', {'operation': 'hide'}, session=session_id[player.id])
        emit('roll dice button change', {'operation': 'hide'}, session=session)

'''
def players_turn_to_roll(game_name):
    game = Game.query.filter_by(game_name=game_name).first()
    if not game:
        return False
    index = game.index_of_turn
    for i in game.players_connected:
        if i.index_in_game == index:
            emit('roll dice button change', {'operation': 'show'}, session=session_id[i.id])
            emit('message', {'msg': 'It is ' + i.username + ' turn to roll the dice'}, room=game.game_name)
        else:
            emit('roll dice button change', {'operation': 'hide'}, session=session_id[i.id])
'''

@socketio.on('text', namespace='/gameroom') #sending text
def text(message):
    game_name = session.get('game_name')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=game_name)

@socketio.on('left', namespace='/gameroom') #leaving room
def left(message):
    game_name = session.get('game_name')
    username = session.get('username')
    leave_room(game_name)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=game_name)