from flask import redirect, url_for, render_template, request, session, flash
from re import search
import random
from App import app, db
from .models import Account, Game, Player, get_account_usernames

@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method=='GET'):
        return render_template('login.html')
        
    elif(request.method=='POST'):
        account_usernames = get_account_usernames()
        formSubmitted = request.form.get("button")
        print(formSubmitted)

        if formSubmitted == "signup":
            ##render menu once it has been made
            username = request.form.get("signupname")
            session['username'] = username            
            if username not in account_usernames:
                new_player = Account(username=username)
                db.session.add(new_player)
                db.create_all()
                db.session.commit()
                print("success i think")
                return redirect(url_for('menu'))
            else:
                print("account taken")
                return render_template('login.html')

        elif formSubmitted == "login":
            #render menu once it has been made
            username = request.form.get("loginname")
            if username in account_usernames:
                print("you can log in")
                session['username'] = username
                return redirect(url_for('menu'))
            else:
                print("account doesnt exist")
                return render_template('login.html')

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
    games = Game.query.all()
    if formType == "Join":
        code = request.form.get('code')
        if search("^\d{6}$", code):
            for game in games:
                if game.game_code == int(code):
                    account = Account.query.filter_by(username=username).first()
                    player = Player(position=0, index_in_game=len(game.players_connected), money=7)
                    account.game_instances.append(player)
                    game.players_connected.append(player)
                    db.session.add(player)
                    db.session.commit()
                    flash("Game joined!")
                    return redirect(url_for('lobby'))
        flash("Code was not valid")
        return render_template('menu.html')
    else:
        new_id = ""
        unique = False
        while not unique:
            unique = True
            new_id = ""
            for i in range(6):
                new_id += str(random.randint(0, 9))
            for game in games:
                if game.game_code == int(new_id):
                    unique = False
        game = Game(game_code=int(new_id), index_of_turn=0, game_started=False)
        account = Account.query.filter_by(username=username).first()
        player = Player(position=0, index_in_game=0, money=7)
        account.game_instances.append(player)
        game.players_connected.append(player)
        db.session.add(player)
        db.session.add(game)
        db.session.commit()
        flash("Game created with code " + new_id)
        return redirect(url_for('lobby'))

@app.route('/lobby')
def lobby():
    try:
        username = session['username']
    except:
        return False
    #get room code
    return render_template('lobby.html',room_code='i will get that later' , session=session)


