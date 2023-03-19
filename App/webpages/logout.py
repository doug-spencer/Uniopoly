from App.main import app, db, engine
from App.database.tables import Player, Game
from flask import session, redirect, url_for, flash
from sqlalchemy import delete

@app.route('/logout')
def logout():
    session.clear()
    flash("You have successfully logged out")
    return redirect(url_for("login"))