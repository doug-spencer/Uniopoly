from flask import render_template, request
from App import app
from App.models.auth import login, signup

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