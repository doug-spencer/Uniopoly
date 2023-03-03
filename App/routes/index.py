from flask import render_template, request, session, redirect, url_for
from App.main import db, app
from App.database.tables import Account
from App.misc.functions import check_account

@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method=='GET'):
        return render_template('login.html')
    elif(request.method=='POST'):
        formSubmitted = request.form.get("button")
        print(formSubmitted)

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