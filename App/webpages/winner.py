from flask import redirect, render_template, request, session, url_for, flash
from App.main import app, db
from App.database.tables import Game, Player
from App.misc.functions import get_correct_location

@app.route('/winner', methods=['GET', 'POST'])
def winner():
    page, game_code = get_correct_location()

    # if page != 'winner':
    #     if game_code == None:
    #         flash('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    #         return redirect(url_for(page))
    #     return redirect(url_for(page, game_code=game_code))
    game_code = session['game_code']
    
    if request.method == 'GET':
        return render_template('winner.html', game_code=game_code, session=session)
    
    ##only runs if POST
    if request.form.get('returnToMenuButton') == 'Leave Room':
        return redirect(url_for('menu'))


    return render_template('winner.html', game_code=game_code, session=session)