from flask import flash, redirect, render_template, request, session, url_for
from App import db
from App.models.classes.main import Account
from . import check_account

def signup():
    username = request.form.get("signupname")
    account = check_account.check_account(username)
    if account:
        print("Account taken")
        return render_template('login.html')
    else:
        new_account = Account.Account(username=username)
        db.session.add(new_account)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('menu'))