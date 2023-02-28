from flask import redirect, render_template, request, session, url_for
from App.main import app, db
from App.models.classes.main import Game, Player

@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    try:
        username = session['username']
    except:
        return False
    game_code = session['game_code']

    if request.method == 'GET':
        return render_template('lobby.html', game_code=game_code, session=session)

    game = Game.query.filter_by(game_code=game_code).first()
    player = Player.query.filter_by(username=username).first()
    #only runs if POST
    if request.form.get('leaveButton') == 'leave room':
        player.query.filter_by(username=username).delete()
        return redirect(url_for('menu'))
    elif request.form.get('startButton') == 'start game':
        if game.players_connected[0].username != username:
            #player isnt host
            return False
        game.game_started = True
        db.session.commit()
        return redirect(url_for('game_room'))

    return render_template('lobby.html', game_code=game_code, session=session)