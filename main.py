from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, Boolean, String
import random
from datetime import timedelta
from re import search

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['SECRET'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
app.app_context().push()
socketio = SocketIO(app, cors_allowed_origins='*')
#socketio = SocketIO(app, logger=True, engineio_logger=True)
db = SQLAlchemy(app)
engine = create_engine('sqlite:///instace/database.db', echo=False)

#global session_id
#session_id = {}


link_player_property = db.Table('link_player_property',
        Column('username', Integer, db.ForeignKey('player.username'), primary_key=True),
        Column('property_id', Integer, db.ForeignKey('property.id'), primary_key=True),
        Column('houses', Integer)
        )

link_player_utilities = db.Table('link_player_utilities',
        Column('username', Integer, db.ForeignKey('player.username'), primary_key=True),
        Column('utilities_id', Integer, db.ForeignKey('utilities.id'), primary_key=True)
        )

link_player_student_union = db.Table('link_player_student_union',
        Column('username', Integer, db.ForeignKey('player.username'), primary_key=True),
        Column('student_union', Integer, db.ForeignKey('student_union.id'), primary_key=True)
        )

link_player_email = db.Table('link_player_email',
        Column('username', Integer, db.ForeignKey('player.username'), primary_key=True),
        Column('email', Integer, db.ForeignKey('email.id'), primary_key=True)
        )

link_player_bus_stop = db.Table('link_player_bus_stop',
        Column('username', Integer, db.ForeignKey('player.username'), primary_key=True),
        Column('bus_stop', Integer, db.ForeignKey('bus_stop.id'), primary_key=True)
        )

        
class Game(db.Model):
    game_code = Column(Integer, primary_key=True)
    index_of_turn = Column(Integer)
    game_started = Column(Boolean)
    

    #host_id = db.relationship('Player', lazy='select', uselist=False)#use=Flase for one to one 
    players_connected = db.relationship('Player', backref='game', lazy='select')
    #action for specific index

class Player(db.Model):
    id = Column(Integer, primary_key=True)
    position = Column(Integer)
    index_in_game = Column(Integer) #order of players
    symbol = Column(Integer)
    money = Column(Integer)
    game_code = Column(Integer, db.ForeignKey('game.game_code'))
    username = Column(Integer, db.ForeignKey('account.username'))
    turns_in_jail = Column(Integer)
    utilities = db.relationship('Utilities', secondary=link_player_utilities, backref='player', lazy='select')
    properties = db.relationship('Property', secondary=link_player_property, backref='player', lazy='select')
    bus_stop = db.relationship('Bus_stop', secondary=link_player_bus_stop, backref='player', lazy='select')
    student_union = db.relationship('Student_union', secondary=link_player_student_union, backref='player', lazy='select')
    email = db.relationship('Email', secondary=link_player_email, backref='player', lazy='select')


class Account(db.Model):
    username = db.Column(db.String(100), primary_key=True)
#    password = db.Column(db.String(100), nullable=False)
    total_played = db.Column(db.Integer)
    games_won = db.Column(db.Integer)
    game_instances = db.relationship('Player', backref='account', lazy='select')


class Utilities(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    text = Column(String(300))
    photo = Column(String(200))
    position = Column(Integer)
    buy_price = Column(Integer)
    morgage_value = Column(Integer)
    #players = db.relationship('players', secondary=link_player_property, backref='utilities', lazy='select')
    
class Property(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    colour = Column(String(20))
    photo = Column(String(200))
    position = Column(Integer)
    buy_price = Column(Integer)
    morgage_value = Column(Integer)
    rents = Column(String(200))
    #players = db.relationship('players', secondary=link_player_property, backref='property', lazy='select')

class Bus_stop(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    photo = Column(String(200))
    position = Column(Integer)
    #rents = {'0': 0, '1': 25, '2': 50, '3': 100, '4': 200}
    # owner = Column(String(100))
    # morgage_value = Column(Integer)
    # is_owned = Column(Boolean, default=False)
    buy_price = Column(Integer)
    morgage_value = Column(Integer)


    #players = db.relationship('players', secondary=link_player_property, backref='bus_stop', lazy='select')

class Student_union(db.Model):
    id = Column(Integer, primary_key=True)
    text = Column(String(500))
    amount = Column(Integer)
    save_for_later = Column(Boolean)
    #players = db.relationship('players', secondary=link_player_property, backref='student_union', lazy='select')

class Email(db.Model):
    id = Column(Integer, primary_key=True)
    text = Column(String(500))
    amount = Column(Integer)
    save_for_later = Column(Boolean)
    #players = db.relationship('players', secondary=link_player_property, backref='email', lazy='select')

'''
# create community chest and chace card class
# create card class
class Card(db.Model):
    id = Column(Integer, primary_key=True)
    text = Column(String(500))
    amount = Column(Integer)
    save_for_later = Column(Boolean)
    #players = db.relationship('players', secondary=link_player_property, backref='email', lazy='select')
    instruction = Column(String(100))
    #method to return the card face down to bottom of deck
    card_bottom_deck = Column(Boolean, default=False)
    #method to return the card face up to top of deck
    card_top_deck = Column(Boolean, default=False)
    #method to return the card to the player
    card_to_player = Column(Boolean, default=False)
'''





    
    
    











#admin1 = Account(username='jacob')
#db.session.add(admin1)
#db.session.add(Game(game_code='wooga'))
if True:
    try:
        Game.__table__.drop(engine)
        Player.__table__.drop(engine)
    except Exception as e:
        print(e)

db.create_all()
db.session.commit()

def load_static_files():
    with open('db_static_files.txt') as file:
        lines = [i for i in file.readlines()]
        index = 0
        current_line = lines[index]

        #Properties
        while current_line != '\n':
            details = current_line.split(';')
            print(details)
            db.session.add(Property(
                name=details[0],
                colour=details[1],
                photo=details[2],
                position=int(details[3]),
                buy_price=int(details[4]),
                morgage_value=int(details[5]),
                rents=details[6][0:len(details[6]) - 1]
                ))
            index += 1
            current_line = lines[index]
            print(index,current_line)
            db.session.commit()
        index += 1
        current_line = lines[index]
        

        #Utilites
        while current_line != '\n':
            details = current_line.split(';')
            print(details)
            db.session.add(Utilities(
                name=details[0],
                text=details[1],
                photo=details[2],
                position=int(details[3]),
                buy_price=int(details[4]),
                morgage_value=int(details[5][0:len(details[5]) - 1])
                ))
            index += 1
            current_line = lines[index]
            print(index,current_line)
        index += 1
        current_line = lines[index]   

        #Bus stop     
        while current_line != '\n':
            details = current_line.split(';')
            print(details)
            db.session.add(Bus_stop(
                name=details[0],
                photo=details[1],
                position=int(details[2]),
                buy_price=int(details[3]),
                morgage_value=int(details[4][0:len(details[4]) - 1])
                ))
            index += 1
            current_line = lines[index]
            print(index,current_line)
        index += 1
        current_line = lines[index]  

        #Student union
        while current_line != '\n':
            details = current_line.split(';')
            print(details)
            db.session.add(Student_union(
                text=details[0],
                amount=int(details[1]),
                save_for_later=bool(details[2][0:len(details[2]) - 1])
                ))
            index += 1
            current_line = lines[index]
            print(index,current_line)
        index += 1
        current_line = lines[index] 

        #Email       
        while current_line != '\n':
            details = current_line.split(';')
            print(details)
            db.session.add(Email(
                text=details[0],
                amount=int(details[1]),
                save_for_later=bool(details[2][0:len(details[2]) - 1])
                ))
            try:
                index += 1
                current_line = lines[index]
            except:
                current_line = '\n'
            print(index,current_line)
    db.session.commit()

load_static_files()


def check_in_game(game_code, username): #verification fucntion
    game = Game.query.filter_by(game_code = game_code).first()
    if not game:
        return False, False
    account = Account.query.filter_by(username=username).first()
    if not account:
        return False, False
    player = False
    for i in game.players_connected:
        if i.username == username:
            player = i
    if not player:
        return False, False
    return game, player

def show_player_options(player, game_code, session):
    #return False #while db is empty
    pos = player.position

    all_properties = Property.query.all()
    index_of_properties = [i.position for i in all_properties]
    if pos in index_of_properties:
        player_landed_on_property(player, game_code, session, all_properties[index_of_properties.index(pos)])
    
    all_utilities = Utilities.query.all()
    index_of_utilities = [i.position for i in all_utilities]
    if pos in index_of_utilities:
        player_landed_on_utility(player, game_code, session, all_utilities[index_of_utilities.index(pos)])
    
    all_bus_stops = Bus_stop.query.all()
    index_of_bus_stops = [i.position for i in all_bus_stops]
    if pos in index_of_bus_stops:
        player_landed_on_bus_stop(player, game_code, session, all_bus_stops[index_of_bus_stops.index(pos)])
    
    all_emails = Email.query.all()
    index_of_emails = [i.postion for i in all_emails]
    if pos in index_of_emails:
        return player_landed_on_card(player, game, session, all_emails[index_of_emails.index(pos)])
    
    # all_student_unions = Student_union.query.all()
    # index_of_student_unions = [i.position for i in all_student_unions]
    # if pos in index_of_student_unions:
    #     player_landed_on_card(player, game, session, all_student_unions[index_of_student_unions.index(pos)])
    
    pos_go_to_jail = 29
    pos_free_parking = 19
    pos_jail = 9
    pos_start = 0
    if pos == pos_go_to_jail:
        player_landed_on_go_to_jail(player, game_code, session)
    if pos == pos_jail:
        player_on_jail(player, game_code, session)
    if pos == pos_start:
        player_landed_on_start(player, game_code, session)
    if pos == pos_free_parking:
        player_landed_on_free_parking(player, game_code, session)

def player_landed_on_start(player, game_code, session):
    emit('message', {'msg': player.username + ' passed go '}, room=game_code)

def player_landed_on_free_parking(player, game_code, session):
    emit('message', {'msg': player.username + ' is on free parking '}, room=game_code)

def player_on_jail(player, game_code, session):
    if player.turns_in_jail == 0:
        emit('message', {'msg': f'{player.username} is on jail'}, room=game_code)
    elif player.turns_in_jail == 1:
        emit('message', {'msg': f'{player.username} must pay 50 or use a get out of jail free card'}, room=game_code)
        player.turns_in_jail == 0
    else:
        emit('message', {'msg': f'{player.username} has {player.turns_in_jail} turns left in jail'}, room=game_code)
    player.turns_in_jail -= 1
    player.turns_in_jail == max(0, player.turns_in_jail-1)
    db.session.commit()


def player_landed_on_go_to_jail(player, game_code, session):
    player.turns_in_jail += 3
    player.position = 9
    db.session.commit()
    emit('message', {'msg': player.username + ' is sent to jail'}, room=game_code)

def player_landed_on_utility(player, game_code, session, utility):
    emit('message', {'msg': player.username + ' landed on ' + utility.name}, room=game_code)

def player_landed_on_property(player, game_code, session, property):
    @socketio.on('buy-property', namespace='/gameroom') #When player presses buy button
    def buy_property():
        game_code = session.get('game_code')
        username = session.get('username')
        game, player = check_in_game(game_code, username)
        if not game and not player:
            return False
        
        #Subtracts cost from money and adds new record of property ownership
        player.money -= property.buy_price
        insert_stmnt = link_player_property.insert().values(username=player.username, property_id=property.id, houses=0)
        db.session.execute(insert_stmnt)
        db.session.commit()

        emit('message', {'msg': property.name + ' has been purchased for ' + str(property.buy_price)}, room=game_code)

    emit('message', {'msg': player.username + ' landed on  the property: ' + property.name}, room=game_code)
    # Checks if property is already owned
    p_link_player = db.session.query(link_player_property).all()
    p_owned = False
    for i in p_link_player:
        if i.property_id == property.id:
            p_owned = True
            owned_property = i
            break
    if p_owned: # If owned rent is payed
        emit('message', {'msg':property.name + ' is owned by me'}, room=game_code)
        rent_list = property.rents.split(',')
        rent = rent_list[3]
        emit('message', {'msg': player.username + ' owes me §' + rent}, room=game_code)
        player.money -= int(rent)
        db.session.commit()
    else: # If not owned, the option to buy the property is given
        game_code = session.get('game_code')
        username = session.get('username')
        game, player = check_in_game(game_code, username)
        if not game and not player:
            return False
        
        emit('buy property button change', {'operation': 'show'}, session=session)
        emit('message', {'msg': 'Click Buy to buy the card for §' + str(property.buy_price)}, room=game.game_code)



def player_landed_on_bus_stop(player, game, session, bus_stop):

    # Check if the player owns the bus stop

    '''Player landed on Bus stop'''
    # Check if the player owns the bus stop
    if player == bus_stop.owner:
    # If they do, do nothing   
        emit('message', {'msg': player.username + ' landed on their own bus stop '}, room=game.game_code) 
    # If they don't, check who owns the bus stop
    else:
        # If no one owns the bus stop, the player can buy it
        if not bus_stop.owner:
            emit('message', {'msg': player.username + ' landed on an unowned bus stop '}, room=game.game_code)
            emit('message', {'msg': player.username + ' can buy the bus stop '}, room=game.game_code)
            emit('message', {'msg': 'The bus stop costs ' + str(bus_stop.cost) + ' '}, room=game.game_code)
            emit('message', {'msg': 'The player has ' + str(player.money) + ' '}, room=game.game_code)
            if player.money >= bus_stop.cost:
                emit('message', {'msg': player.username + ' has enough money to buy the bus stop '}, room=game.game_code)
                emit('message', {'msg': player.username + ' buys the bus stop '}, room=game.game_code)
                bus_stop.owner = player
                player.money -= bus_stop.cost
                emit('message', {'msg': 'The player now has ' + str(player.money) + ' '}, room=game.game_code)
                emit('message', {'msg': 'The bus stop is now owned by ' + str(bus_stop.owner.username) + ' '}, room=game.game_code)
            else:
                emit('message', {'msg': player.username + ' does not have enough money to buy the bus stop '}, room=game.game_code)
                emit('message', {'msg': player.username + ' does not buy the bus stop '}, room=game.game_code)
        # If someone owns the bus stop, the player has to pay rent, for each bus they own they pay a different amount

        else:
            emit('message', {'msg': player.username + ' landed on a bus stop owned by ' + str(bus_stop.owner.username) + ' '}, room=game.game_code)
            emit('message', {'msg': player.username + ' has to pay rent '}, room=game.game_code)
            emit('message', {'msg': 'The player has ' + str(player.money) + ' '}, room=game.game_code)
            emit('message', {'msg': 'The bus stop owner has ' + str(bus_stop.owner.money) + ' '}, room=game.game_code)
            if player.money >= bus_stop.rent:
                emit('message', {'msg': player.username + ' has enough money to pay the rent '}, room=game.game_code)
                emit('message', {'msg': player.username + ' pays the rent '}, room=game.game_code)
                player.money -= bus_stop.rent
                bus_stop.owner.money += bus_stop.rent
                emit('message', {'msg': 'The player now has ' + str(player.money) + ' '}, room=game.game_code)
                emit('message', {'msg': 'The bus stop owner now has ' + str(bus_stop.owner.money) + ' '}, room=game.game_code)
            else:
                emit('message', {'msg': player.username + ' does not have enough money to pay the rent '}, room=game.game_code)
                emit('message', {'msg': player.username + ' goes bankrupt '}, room=game.game_code)
                emit('message', {'msg': 'The player now has ' + str(player.money) + ' '}, room=game.game_code)
                emit('message', {'msg': 'The bus stop owner now has ' + str(bus_stop.owner.money) + ' '}, room=game.game_code)
                player.money = 0
                emit('message', {'msg': player.username + ' is removed from the game '}, room=game.game_code)
                game.players.remove(player)
                session.commit()

        db.session.commit()

 
def player_landed_on_card(player, game, session, card):

    # if player lands on card emit message to client
    
    emit('message', {'msg': player.username + ' landed on a card '}, room=game.game_code)
    emit('message', {'msg': 'The card is ' + str(card.type) + ' '}, room=game.game_code)
    emit('message', {'msg': 'The card says ' + str(card.instructions) + ' '}, room=game.game_code)
    #if card is chance then do chance card instrucitons and is instance of card class
    if card.type == "Chance":
        game.chance_cards.remove(card)
        

        # Do the chance card instructions
        game.chance_cards.append(card)
        
    #if card is community chest then do community chest instructions
    elif card.type == "Community Chest":
        game.community_chest_cards.remove(card)
        # Do the community chest card instructions
        game.community_chest_cards.append(card)
    
        
    

  
    
    db.session.commit()

 
   






           


@app.route('/', methods=['GET', 'POST'])
def index():
    def get_account_usernames():
        accounts = Account.query.all()
        account_usernames = []
        for i in accounts:
            account_usernames.append(i.username)
        print(account_usernames)
        return account_usernames

    if(request.method=='GET'):
        return render_template('login.html')
        
    elif(request.method=='POST'):
        login_message = ""
        account_usernames = get_account_usernames()
        formSubmitted = request.form.get("button")
        print(formSubmitted)

        if formSubmitted == "signup":
            ##render menu once it has been made
            username = request.form.get("signupname")
            session['username'] = username            
            if username not in account_usernames:
                new_account = Account(username=username)
                db.session.add(new_account)
                db.create_all()
                db.session.commit()
                return redirect(url_for('menu'))
            else:
                login_message = "account taken"
                return render_template('login.html', login_message=login_message)

        elif formSubmitted == "login":
            #render menu once it has been made
            username = request.form.get("loginname")
            if username in account_usernames:
                print("you can log in")
                session['username'] = username
                return redirect(url_for('menu'))
            else:
                login_message = "account doesnt exist"
                return render_template('login.html', login_message=login_message)

@app.route('/help', methods=['GET', 'POST'])
def help():
    if(request.method=='POST'):
        return redirect(url_for('menu'))
    return render_template('help.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    try:
        username = session['username']
    except: #player isnt in session (hasnt logged in)
        return False
    if request.method == 'GET':
        # temp code
        flash("current game codes:")
        for game in Game.query.all():
            flash(game.game_code)
        return render_template('menu.html')
    formType = request.form.get('button')
    games = Game.query.all()
    if formType == "Join":
        code = request.form.get('code')
        if search("^\d{6}$", code):
            for game in games:
                if game.game_code == int(code):
                    account = Account.query.filter_by(username=username).first()
                    player = Player(position=0, index_in_game=len(game.players_connected), money=7)
                    account.game_instances.append(player)
                    game.players_connected.append(player)
                    db.session.add(player)
                    db.session.commit()
                    flash("Game joined!")
                    session['game_code'] = code 
                    return redirect(url_for('lobby'))
        flash("Code was not valid")
        return render_template('menu.html')
    elif formType == "Help Page":
        return redirect(url_for('help'))
    else:
        new_id = ""
        unique = False
        while not unique:
            unique = True
            new_id = ""
            for i in range(6):
                new_id += str(random.randint(0, 9))
            for game in games:
                if game.game_code == int(new_id):
                    unique = False
        game = Game(game_code=int(new_id), index_of_turn=0, game_started=False)
        account = Account.query.filter_by(username=username).first()
        player = Player(position=0, index_in_game=0, money=7, turns_in_jail=0)
        account.game_instances.append(player)
        game.players_connected.append(player)
        db.session.add(player)
        db.session.add(game)
        db.session.commit()
        session['game_code'] = new_id 
        flash("Game created with code " + new_id)
        return redirect(url_for('lobby'))


'''
@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('roll dice event')
def test_message():
    emit('my response', {'data': int(random.randint(1,6))}, broadcast=True)

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
'''
@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    try:
        username = session['username']
    except:
        return False
    game_code = session['game_code']

    if request.method == 'GET':
        return render_template('lobby.html',game_code=game_code, session=session)

    game = Game.query.filter_by(game_code=game_code).first()
    player = Player.query.filter_by(username=username).first()
    #only runs if POST
    if request.form.get('leaveButton') == 'leave room':
        Player.query.filter_by(username=username).delete()
        return redirect(url_for('menu'))
    elif request.form.get('startButton') == 'start game':
        if game.players_connected[0].username != username:
            #player isnt host
            return False
        game.game_started = True
        db.session.commit()
        return redirect(url_for('game_room'))

    return render_template('lobby.html',game_code=game_code, session=session)

@socketio.on('remove', namespace='/lobby')
def remove(data):
    try:
        username = session['username']
    except:
        print('INTRUDER')
        return False
    
    Player.query.filter_by(username=data['username']).delete()
    db.session.commit()
    print(data['username']) 

@socketio.on('check pregame status', namespace='/lobby') #player updating lobby screen
def check_pregame_status():
    try:
        username = session['username']
    except:
        print('INTRUDER')
        return False
    player = Player.query.filter_by(username=username).first()
    if player == None:
        print(2345678765432)
        #players been removed from game
        emit('player not in game', session=session)
        return False
    game = Game.query.filter_by(game_code=player.game_code).first()
    if game.game_started:
        emit('game started', session=session)
    else: #updates list of players in game so far
        usernames = []
        for i in game.players_connected:
            usernames.append(str(i.username))
        
        print('usrs: ', usernames)
        emit('player list', {'players': usernames}, session=session)

@socketio.on('leave lobby', namespace='/lobby') #player leaving lobby
def leave_lobby():
    try:
        session['username']
    except:
        return False
    #emit('status', {'msg':  session.get('username') + ' has entered the room.'}, session=session)

@app.route('/gameroom', methods=['GET', 'POST'])
def game_room():
    if(request.method=='POST') and False: #player has made a game or is joining one
        ### not used any more
        username = request.form['username']
        choice = request.form['choice'] #if the made a game or the name of the game they joined
        account = Account.query.filter_by(username=username).first()
        if not account: #player doesnt have account
            account = Account(username=username)
            db.session.add(account)
        player = Player(position=0)
        db.session.add(player)
        account.game_instances.append(player) #links account with the player in the new game
        if choice == 'make': #imaking a game
            game_code = request.form['game_code']
            game = Game(game_code=game_code, index_of_turn=0, game_started=False)
            db.session.add(game)
        else: #joining game
            game_code = choice
            game=Game.query.filter_by(game_code=choice).first()
        game.players_connected.append(player)#adds player to game    
        player.index_in_game = len(game.players_connected) - 1
        db.session.commit()
        #Store the data in session
        session['username'] = username
        session['game_code'] = game_code
        #session_id[player.id] = session.get('session_id') 
        return render_template('game_room.html', session = session)
    else:
        if(session.get('username') is not None): #player is already in a session
            return render_template('game_room.html', session = session)
        else: #if not logged in
            games = Game.query.all()
            game_codes = []
            for i in games:
                game_codes.append(i.game_code)
            return redirect(url_for(''))

@socketio.on('join', namespace='/gameroom') #player joining room
def join(message):
    game_code = session.get('game_code')
    join_room(game_code)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=game_code)
    emit('buy property button change', {'operation': 'hide'}, session=session)

@socketio.on('roll dice', namespace='/gameroom') #when a player rolls the dice
def roll_dice():
    game_code = session.get('game_code')
    username = session.get('username')
    game, player = check_in_game(game_code, username)
    if not game and not player:
        return False
    
    if player.turns_in_jail == 0:
        roll_value = random.randint(1,6)
        current_value = player.position
        new_value = roll_value + current_value
        
        if new_value > 39:
            new_value -= 40
        
        player.position = new_value
        
        turn = game.index_of_turn
        if turn == len(game.players_connected) - 1:
            game.index_of_turn = 0
        else:
            game.index_of_turn += 1
        db.session.commit()
        emit('message', {'msg': player.username + ' rolled a ' + str(roll_value) + ' they are now at positon ' + str(new_value)}, room=game_code)
        emit('dice_roll', {'dice_value': roll_value, 'position': new_value}, session=session)
    show_player_options(player, game_code, session)
    #emit('dice_roll', {'dice_value': roll_value, 'position': new_value}, session=session_id[player.id])

@socketio.on('update turn', namespace='/gameroom') #check if its players turn yet (if roll dice button should be shown)
def update_turn():
    game_code = session.get('game_code')
    username = session.get('username')
    game, player = check_in_game(game_code, username)
    if not game and not player:
        return False
    if game.index_of_turn == player.index_in_game:
        #emit('roll dice button change', {'operation': 'show'}, session=session_id[player.id])
        emit('roll dice button change', {'operation': 'show'}, session=session)
        emit('message', {'msg': 'It is ' + player.username + ' turn to roll the dice'}, room=game.game_code)
    else:
        #emit('roll dice button change', {'operation': 'hide'}, session=session_id[player.id])
        emit('roll dice button change', {'operation': 'hide'}, session=session)


def player_landed_on_bus(player, game, session, bus_stop):
    print('player landed on bus')
    # if player.money < 200:
    #     emit('message', {'msg': 'You do not have enough money to buy this property'}, session=session)
    #     return False
    # player.money -= 200
    # player.properties.append(Property.query.filter_by(name='bus').first())
    # db.session.commit()
    # emit('message', {'msg': player.username + ' has bought the bus for $200'}, room=game.game_code)
    # show_player_options(player, game, session)

    if player in bus_stop.players:
        # If player does own the bus stop, do nothing
        return 
    else:
        # Check who owns the bus stop
        owner = None
        for p in bus_stop.players:
            # owner = p
            if p == player:
                owner = p
                break
        
            if owner:
                # If the bus stop is owned by another player, check how many bus stops they own
                count = 0
                for bs in Bus_stop.query.all():
                    if owner in bs.players:
                        count += 1
                
                # Calculate the rent based on the number of bus stops owned
                rent = bus_stop.rents[count]
                
                # If the player doesn't have enough money, all of their money goes to the owner
                if player.money < rent:
                    owner.money += player.money
                    player.money = 0
                    
                    # If the player goes bankrupt, remove them from the game and auction their cards
                    game.players_connected.remove(player)
                    flash('You went bankrupt and were removed from the game!')
                    # Auction player's cards here
                else:
                    # If the player has enough money, deduct the rent and give it to the owner
                    player.money -= rent
                    owner.money += rent
        else:
            # If the bus stop is unowned, give the player the option to buy it
            # Code to present buy option to player here
            player_wants_to_buy = input("Do you want to buy this property? (y/n) ")
            if player_wants_to_buy.upper == "Y":
                player_wants_to_buy = True
            else:
                player_wants_to_buy = False
                                        
            if player_wants_to_buy:
                # Add the property to the table and link it with the player
                player.bus_stop.append(bus_stop)
                bus_stop.players.append(player)
                player.money -= bus_stop.price
            else:
                pass
                # Put the property up for sale to other players
                # Code to handle property auction here
    return False

'''
def players_turn_to_roll(game_code):
    game = Game.query.filter_by(game_code=game_code).first()
    if not game:
        return False
    index = game.index_of_turn
    for i in game.players_connected:
        if i.index_in_game == index:
            emit('roll dice button change', {'operation': 'show'}, session=session_id[i.id])
            emit('message', {'msg': 'It is ' + i.username + ' turn to roll the dice'}, room=game.game_code)
        else:
            emit('roll dice button change', {'operation': 'hide'}, session=session_id[i.id])
'''

@socketio.on('text', namespace='/gameroom') #sending text
def text(message):
    game_code = session.get('game_code')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=game_code)

@socketio.on('left', namespace='/gameroom') #leaving room
def left(message):
    game_code = session.get('game_code')
    username = session.get('username')
    leave_room(game_code)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=game_code)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')