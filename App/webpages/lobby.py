from flask import redirect, render_template, request, session, url_for, flash
from App.main import app, db
from App.database.tables import Game, Player
from App.misc.functions import get_correct_location

@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    page, game_code = get_correct_location()
    if page != 'lobby':
        if game_code == None:
            flash('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            return redirect(url_for(page))
        return redirect(url_for(page, game_code=game_code))
    game_code = session['game_code']
    username = session['username']
    if request.method == 'GET':
        return render_template('lobby.html', game_code=game_code, session=session)

    game = Game.query.filter_by(game_code=game_code).first()
    player = Player.query.filter_by(username=username, game_code=game_code).first()
    #only runs if POST
    if request.form.get('leaveButton') == 'Leave Room':
        db.session.delete(player)
        db.session.commit()
        username = session['username']
        session.clear()
        session['username'] = username
        flash("You have successfully left the game")
        return redirect(url_for('menu'))
    elif request.form.get('startButton') == 'Start Game':
        if game.players_connected[0].username != username:
            #player isnt host
            return False
        game.game_started = True
        db.session.commit()
        return redirect(url_for('game_room'))
    return render_template('lobby.html', game_code=game_code, session=session)