from App.main import app, db, engine
from App.database.tables import Player, Game
from flask import session, redirect, url_for
from sqlalchemy import delete

@app.route('/logout')
def logout():
    print("£££££££££££££££££££££££££££££££££££33")
    try:
        username = session['username']
    except:
        return redirect(url_for("login"))
    session.clear()
    return redirect(url_for("login"))