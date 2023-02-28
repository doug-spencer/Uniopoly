from flask import redirect, render_template, request, session, url_for
from .account_check import check_account

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