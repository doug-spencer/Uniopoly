from flask import redirect, render_template, request, session, url_for
from App.main import app, db
from App.database.tables import Game, Player
from App.misc.functions import check_account, get_correct_location

@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    page, game_code = get_correct_location()
    if page != 'lobby':
        if game_code == None:
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            return redirect(url_for(page))
        print(page, game_code)
        return redirect(url_for(page, game_code=game_code))
    game_code = session['game_code']
    username = session['username']
    if request.method == 'GET':
        return render_template('lobby.html', game_code=game_code, session=session)

    game = Game.query.filter_by(game_code=game_code).first()
    player = Player.query.filter_by(username=username).first()
    #only runs if POST
    if request.form.get('leaveButton') == 'Leave Room':
        player.query.filter_by(username=username).delete()
        return redirect(url_for('menu'))
    elif request.form.get('startButton') == 'Start Game':
        if game.players_connected[0].username != username:
            #player isnt host
            return False
        game.game_started = True
        db.session.commit()
        return redirect(url_for('game_room'))

    return render_template('lobby.html', game_code=game_code, session=session)