from flask import render_template, request, session, redirect, url_for, flash
from App.main import db, app
from App.database.tables import Account, Game
from App.misc.functions import check_account, check_username, get_correct_location
from re import search
import hashlib

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
    password = hashlib.sha256(request.form.get("loginpassword").encode()).hexdigest()
    if not check_username(username):
        flash("Account doesn't exist")
        return render_template('login.html')

    if not check_account(username, password):
        flash("Incorrect password")
        return render_template('login.html')

    session['username'] = username
    flash("You have successfully logged in")
    return redirect(url_for('menu'))

def signup():
    username = request.form.get("loginname")
    password = hashlib.sha256(request.form.get("loginpassword").encode()).hexdigest()
    if search(r'\d', username):
        flash('Username cannot contain numbers')
        return render_template('login.html')
    if check_username(username):
        flash("Username taken")
        return render_template('login.html')
    
    new_account = Account(username=username, password=password)
    db.session.add(new_account)
    db.session.commit()
    session['username'] = username
    flash("You have successfully signed up")
    return redirect(url_for('menu'))