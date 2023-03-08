from flask import render_template, request, session, redirect, url_for, flash
from App.main import db, app
from App.database.tables import Account, Game
from App.misc.functions import check_account, get_correct_location

@app.route('/', methods=['GET', 'POST'])
def login():
    if(request.method=='GET'):
        '''
        try:
            username = session['username']
        except: #user isnt logged in
            return render_template('login.html')
        try:
            gamename = session['game_name']
        except: #user isnt in a game
            return redirect(url_for('menu'))
        game = Game.query.filter_by(gamename=gamename)
        if game == None:
            flash("game you were in has ended")
            return render_template("menu")
        print([i.username for i in game.players_connected])
        if username not in [i.username for i in game.players_connected]:
            flash("your not in the game anymore my friend")
            return render_template("menu")
        return render_template("gameroom")
        '''
        page, game_code = get_correct_location()
        if page == 'login':
            return render_template("login.html")
        if game_code == None:
            return redirect(url_for(page))
        return redirect(url_for(page, game_code=game_code))
    elif(request.method=='POST'):
        formSubmitted = request.form.get("button")
        if formSubmitted == 'signup':
            return signup()
        elif formSubmitted == "login":
            return login()
        
def login():
    username = request.form.get("loginname")
    account = check_account(username)
    if account:
        print("You can log in")
        session['username'] = username
        return redirect(url_for('menu'))
    else:
        print("Account doesn't exist")
        return render_template('login.html')

def signup():
    username = request.form.get("signupname")
    account = check_account(username)
    if account:
        print("Account taken")
        return render_template('login.html')
    else:
        new_account = Account(username=username)
        db.session.add(new_account)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('menu'))