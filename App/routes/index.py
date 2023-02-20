from flask import render_template, request, session, redirect, url_for
from App import app, db
# from App.models.auth import signup, login
from App.models.classes.main import Account

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if(request.method=='GET'):
#         return render_template('login.html')
#     elif(request.method=='POST'):
#         formSubmitted = request.form.get("button")

#         print(formSubmitted)

#         if formSubmitted == 'signup':
#             signup.signup()
#         elif formSubmitted == "login":
#             login.login()


@app.route('/', methods=['GET', 'POST'])
def index():
    def get_account_usernames():
        accounts = Account.Account.query.all()
        account_usernames = []
        for i in accounts:
            account_usernames.append(i.username)
        print(account_usernames)
        return account_usernames

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
                new_player = Account.Account(username=username)
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