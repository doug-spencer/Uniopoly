from flask import redirect, render_template, request, session, url_for, flash
from App.main import app, db
from App.database.tables import Game, Player
from App.misc.functions import get_correct_location

@app.route('/winner', methods=['GET', 'POST'])
def winner():
    #page, game_code = get_correct_location()

    # if page != 'winner':
    #     if game_code == None:
    #         flash('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    #         return redirect(url_for(page))
    #     return redirect(url_for(page, game_code=game_code))
    
    if request.method == 'GET':
        game_code = session['game_code']
        game = Game.query.filter_by(game_code=game_code).first()
        if game != None:
            winner = False
            for player in game.players_connected:
                if player.money != -1000000:
                    winner = player.username
        return render_template('winner.html', winner=winner)
        return render_template('winner.html', game_code=game_code, session=session)
    
    ##only runs if POST
    else:
        username = session['username']
        player = Player.query.filter_by(username=username).first()
        db.session.delete(player)
        session.pop('game_code', None)
        return redirect(url_for('menu'))