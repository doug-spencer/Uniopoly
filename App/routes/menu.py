from flask import flash, render_template, request, session
from re import search
from App.main import app
from App.database.database_classes import Game
from App.models.func import create_game, join_game

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