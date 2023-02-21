from flask import redirect, render_template, request, url_for
from App import app

@app.route('/help', methods=['GET', 'POST'])
def help():
    if(request.method=='POST'):
        return redirect(url_for('menu'))
    return render_template('help.html')