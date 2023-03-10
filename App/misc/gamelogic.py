from App.database.tables import Player, Game, Account, Property, Utilities, Bus_stop, Email, Student_union, link_player_property, link_player_bus_stop, link_player_utilities, link_player_email, link_player_student_union
from flask_socketio import emit
from App.main import db, socketio, engine
from . import functions
import random
def show_player_options(player, game_code, session):
    pos = player.position

    all_properties = Property.query.all()
    all_utilities = Utilities.query.all()
    all_bus_stops = Bus_stop.query.all()
    all_emails = Email.query.all()
    all_student_unions = Student_union.query.all()
    
    index_of_properties = [i.position for i in all_properties]
    index_of_utilities = [i.position for i in all_utilities]
    index_of_bus_stops = [i.position for i in all_bus_stops]
    print(index_of_properties)
    if pos in index_of_properties:
        print("here1.5")
        buy_choice_active = player_landed_on_purchasable_card(player, game_code, session, all_properties[index_of_properties.index(pos)], link_player_property)
        return buy_choice_active

    elif pos in index_of_utilities:
        buy_choice_active = player_landed_on_purchasable_card(player, game_code, session, all_utilities[index_of_utilities.index(pos)], link_player_utilities)
        return buy_choice_active   

    elif pos in index_of_bus_stops:
        buy_choice_active = player_landed_on_purchasable_card(player, game_code, session, all_bus_stops[index_of_bus_stops.index(pos)], link_player_bus_stop)
        return buy_choice_active    
    
    pos_go_to_jail = 29
    pos_free_parking = 19
    pos_jail = 9
    pos_start = 0
    pos_emails = [7, 21]
    pos_student_unions = [16, 26]

    if pos == pos_go_to_jail:
        player_landed_on_go_to_jail(player, game_code, session)
    if pos == pos_jail:
        player_on_jail(player, game_code, session)
    if pos == pos_start:
        player_landed_on_start(player, game_code, session)
    if pos == pos_free_parking:
        player_landed_on_free_parking(player, game_code, session)
    if pos in pos_emails:
        player_landed_on_card(player, game_code, session, all_emails, link_player_email, True)
    if pos in pos_student_unions:
        player_landed_on_card(player, game_code, session, all_student_unions, link_player_student_union, False)
    # all_emails = Email.query.all()
    # index_of_emails = [i.position for i in all_emails]
    # if pos in index_of_emails:
    #     player_landed_on_card(player, game, session, all_emails[index_of_emails.index(pos)])
    
    # all_student_unions = Student_union.query.all()
    # index_of_student_unions = [i.position for i in all_student_unions]
    # if pos in index_of_student_unions:
    #     player_landed_on_card(player, game, session, all_student_unions[index_of_student_unions.index(pos)])

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
    player.turns_in_jail = max(0, player.turns_in_jail-1)
    db.session.commit()


def player_landed_on_go_to_jail(player, game_code, session):
    player.turns_in_jail += 3
    player.position = 9
    db.session.commit()
    emit('message', {'msg': player.username + str(player.position) + str(player.turns_in_jail) +' is sent to jail'}, room=game_code)


def player_landed_on_purchasable_card(player, game_code, session, card, link_table):

    emit('message', {'msg': player.username + ' landed on ' + card.name}, room=game_code)

    #selects the row in the table recording who owns what property with the id of the property that was landed on
    with engine.connect() as conn:
        query = link_table.select().where(link_table.c.card_id == card.id)
        card_row = conn.execute(query).fetchone()

        #nobody owns it
        if card_row == None:
            halt_player_turn(game_code)
            emit('buy property button change', {'operation':'show'}, session=session)
            emit('roll dice button change', {'operation':'hide'}, session=session)
            return True #to stop the next player getting to roll the dice

        #you own it
        elif card_row.player_id == player.id:
            return False
    
        #someone owns it and it isn't you so pay rent
        rent_amount, player_owed = get_rent_amount(player, game_code, session, card, link_table)
        print("rent_amount", rent_amount)
        print("player_owed", player_owed)
        functions.player1_owes_player2_money(player, rent_amount, player_owed)
        return False

#transforms the index of turn variable so that it applys to no player
def halt_player_turn(game_code):
    game= Game.query.filter_by(game_code=game_code).first()
    game.index_of_turn = -1 * game.index_of_turn - 1
    db.session.commit()

#returns the index of turn variable to its previous value
def resume_player_turn(game_code):
    game= Game.query.filter_by(game_code=game_code).first()
    game.index_of_turn = (game.index_of_turn + 1) * -1
    db.session.commit()

def update_position(game, game_code):
    positions = [[i, None] for i in range(40)]
    for i in game.players_connected:
        if positions[i.position][1] == None:
            positions[i.position][1] = i.username
        else:
            positions[i.position][1] = positions[i.position][1] + ',' + i.username
    positions = [i for i in positions if i[1]!= None]
    print(positions, game.game_code)
    emit('update player positions', {'positions': positions}, room=game_code) 

def get_rent_amount(player, game_code, session, card, link_table):
    ##get the rent required by the owner
    ##check the player has enough total money and property value
        ##if not make them lose
        ##return their properties to the game
        ##give the money they have and the morgage value of the properties to the renter

    ##get the money held by the player
    ##if enough to pay
        ##give them the money
    ##else
        ##wait until they have mortgaged their stuff
    with engine.connect() as conn:

        card_colour = Property.query.filter_by(id=card.id).first().colour
        cards_with_colour = Property.query.filter_by(colour=card_colour).all()
        card_ids_with_colour = [i.id for i in cards_with_colour]
        
        renter_id_query = link_table.select().where(link_table.c.card_id == card.id)
        card_row = conn.execute(renter_id_query).fetchone()
        renter_id = card_row.player_id
        no_of_houses = card_row.houses

        number_of_colour_owned = 0
        for card_id_with_colour in card_ids_with_colour:
            number_of_colour_owned_query = link_table.select().where(link_table.c.card_id==card_id_with_colour, link_table.c.player_id==renter_id)
            if conn.execute(number_of_colour_owned_query).fetchone() != None:
                number_of_colour_owned += 1

        player_owed = Player.query.filter_by(id=renter_id).first()

        if number_of_colour_owned < len(card_ids_with_colour):
            return int(card.rents.split(',')[0]), player_owed
        
        elif number_of_colour_owned == len(card_ids_with_colour):
            return int(card.rents.split(',')[1+no_of_houses]), player_owed
        

def get_cards(player):
    cards = []
    tables = [link_player_property, link_player_utilities, link_player_bus_stop]
    for i in tables:
        results = i.query.filter_by(player_id=player.player_id).all()
        cards = cards + [j.card_id.name for j in results]
    #temp
    cards = ["Duck.webp"]*9
    return cards

def player_landed_on_card(player, game_code, session, all_cards, link_player_card, is_email):
    emit('message', {'msg': player.username + ' landed on a pick up card square '}, room=game_code)
    card = random.choice(all_cards)
    if card.save_for_later:
        if True:
            insert_stmnt = link_player_card.insert().values(player_id=player.id, email_id=card.id)
        else:
            insert_stmnt = link_player_card.insert().values(player_id=player.id, student_union_id=card.id)
        db.session.execute(insert_stmnt)
        db.session.commit()
    emit('display card', {'text': card.text}, room=game_code)
