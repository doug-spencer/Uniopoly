from flask import flash, redirect, render_template, request, session, url_for
from App import app, db
from re import search
import random
from App.models.classes.main import Account, Game, Player
from . import check_account

def login():
    username = request.form.get("loginname")
    account = check_account.check_account(username)
    if account:
        print("You can log in")
        session['username'] = username
        return redirect(url_for('menu'))
    else:
        print("Account doesn't exist")
        return render_template('login.html')

# @app.route('/menu', methods=['GET', 'POST'])
# def menu():
#     try:
#         username = session['username']
#     except: #player isnt in session (hasnt logged in)
#         return False
#     if request.method == 'GET':
#         # temp code
#         flash("current game codes:")
#         for game in Game.Game.query.all():
#             flash(game.game_code)
#         return render_template('menu.html')
#     formType = request.form.get('button')
#     games = Game.Game.query.all()
#     if formType == "Join":
#         code = request.form.get('code')
#         if search("^\d{6}$", code):
#             for game in games:
#                 if game.game_code == int(code):
#                     account = Account.Account.query.filter_by(username=username).first()
#                     player = Player.Player(position=0, index_in_game=len(game.players_connected), money=7)
#                     account.game_instances.append(player)
#                     game.players_connected.append(player)
#                     db.session.add(player)
#                     db.session.commit()
#                     flash("Game joined!")
#                     return redirect(url_for('lobby'))
#         flash("Code was not valid")
#         return render_template('menu.html')
#     else:
#         new_id = ""
#         unique = False
#         while not unique:
#             unique = True
#             new_id = ""
#             for i in range(6):
#                 new_id += str(random.randint(0, 9))
#             for game in games:
#                 if game.game_code == int(new_id):
#                     unique = False
#         game = Game(game_code=int(new_id), index_of_turn=0, game_started=False)
#         account = Account.query.filter_by(username=username).first()
#         player = Player(position=0, index_in_game=0, money=7)
#         account.game_instances.append(player)
#         game.players_connected.append(player)
#         db.session.add(player)
#         db.session.add(game)
#         db.session.commit()
#         flash("Game created with code " + new_id)
#         return redirect(url_for('lobby'))