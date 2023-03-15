from App.database.tables import Player, Game, Account, Property, Utilities, Bus_stop, Student_union, Email, link_player_property, link_player_bus_stop, link_player_utilities
from flask_socketio import emit
import random
from App.main import db, socketio, engine
from App.database import link_table_updates
from . import functions

def show_player_options(player, game_code, session):
    pos = player.position

    all_properties = Property.query.all()
    all_utilities = Utilities.query.all()
    all_bus_stops = Bus_stop.query.all()
    
    index_of_properties = [i.position for i in all_properties]
    index_of_utilities = [i.position for i in all_utilities]
    index_of_bus_stops = [i.position for i in all_bus_stops]
    print(index_of_properties)
    if pos in index_of_properties:
        buy_choice_active = player_landed_on_purchasable_card(player, game_code, session, all_properties[index_of_properties.index(pos)], link_player_property)
        return buy_choice_active

    elif pos in index_of_utilities:
        buy_choice_active = player_landed_on_purchasable_card(player, game_code, session, all_utilities[index_of_utilities.index(pos)], link_player_utilities)
        return buy_choice_active   

    elif pos in index_of_bus_stops:
        buy_choice_active = player_landed_on_purchasable_card(player, game_code, session, all_bus_stops[index_of_bus_stops.index(pos)], link_player_bus_stop)
        return buy_choice_active    
    
    pos_email = 7
    pos_student_union = 16
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
    if pos == pos_email:
        player_landed_on_email(player, game_code)
    if pos == pos_student_union:
        player_landed_on_student_union(player, game_code)     

    # all_emails = Email.query.all()
    # index_of_emails = [i.position for i in all_emails]
    # if pos in index_of_emails:
    #     player_landed_on_card(player, game, session, all_emails[index_of_emails.index(pos)])
    
    # all_student_unions = Student_union.query.all()
    # index_of_student_unions = [i.position for i in all_student_unions]
    # if pos in index_of_student_unions:
    #     player_landed_on_card(player, game, session, all_student_unions[index_of_student_unions.index(pos)])

def player_landed_on_start(player, game_code, session):
    emit('message', {'msg': player.username + ' landed on go '}, room=game_code)

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

        if card_row == None:
            emit('buy property button change', {'operation':'show'}, session=session)
            return True #to stop the next player getting to roll the dice

        #you own it
        elif card_row.player_id == player.id:
            return False
    
        #someone owns it and it isn't you so pay rent
        rent_amount, player_owed = get_rent_amount(card, link_table)
        functions.player1_owes_player2_money(player, rent_amount, player_owed)
        return False

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

def get_rent_amount(card, link_table):
    with engine.connect() as conn:

        ##finds the ids of the cards that are the same colour as the card that was landed on
        card_colour = Property.query.filter_by(id=card.id).first().colour
        cards_with_colour = Property.query.filter_by(colour=card_colour).all()
        card_ids_with_colour = [i.id for i in cards_with_colour]
        
        ##finds the renter id and the number of houses on the card that was landed on
        renter_id_query = link_table.select().where(link_table.c.card_id == card.id)
        card_row = conn.execute(renter_id_query).fetchone()
        renter_id = card_row.player_id
        no_of_houses = card_row.houses

        ##finds the number of the houses of the select colour that the renter owns
        number_of_colour_owned = 0
        for card_id_with_colour in card_ids_with_colour:
            number_of_colour_owned_query = link_table.select().where(link_table.c.card_id==card_id_with_colour, link_table.c.player_id==renter_id)
            if conn.execute(number_of_colour_owned_query).fetchone() != None:
                number_of_colour_owned += 1

        ##finds the player that is owed
        player_owed = Player.query.filter_by(id=renter_id).first()

        ##returns the first rent amount if the renter does not own the set 
        if number_of_colour_owned < len(card_ids_with_colour):
            return int(card.rents.split(',')[0]), player_owed
        
        ##returns the rent amount associated with the set and the number of houses owned by the renter
        elif number_of_colour_owned == len(card_ids_with_colour):
            return int(card.rents.split(',')[1+no_of_houses]), player_owed

def get_cards(player):
    unmortgaged_cards = []
    mortgaged_cards = []
    unmortgaged_cards_id = []
    mortgaged_cards_id = []
    tables = [[link_player_property, Property], [link_player_utilities, Utilities], [link_player_bus_stop, Bus_stop]]
    with engine.connect() as conn:
        for i in tables:
            query = i[0].select().where(i[0].c.player_id == player.id, i[0].c.mortgaged == False)
            card_row = conn.execute(query).fetchall()
            for card in card_row:
                print(card_row)
                card = i[1].query.filter_by(id=card[1]).first()
                unmortgaged_cards.append(card.photo)
                unmortgaged_cards_id.append(card.id)
            query = i[0].select().where(i[0].c.player_id == player.id, i[0].c.mortgaged == True)
            card_row = conn.execute(query).fetchall()
            for card in card_row:
                print(card_row)
                card = i[1].query.filter_by(id=card[1]).first()
                mortgaged_cards.append(card.photo)
                mortgaged_cards_id.append(card.id)
    return unmortgaged_cards, mortgaged_cards, unmortgaged_cards_id, mortgaged_cards_id

def get_houses(player):
    property = []
    colours = []
    colour_count = {}
    with engine.connect() as conn:
        query = link_player_property.select().where(link_player_property.c.player_id == player.id)
        card_row = conn.execute(query).fetchall()
    for card in card_row:
        property_card = Property.query.filter_by(id=card[1]).first()
        if property_card.colour not in colour_count:
            colour_count[property_card.colour] = 1
        else:
            colour_count[property_card.colour] += 1
        property.append([property_card.name, property_card.colour, card[3]])
    for key in colour_count:
        if colour_count[key] == 3:
            colours.append(key)
    split_property_by_colour = []
    for colour in colours:
        split_property_by_colour.append([i for i in property if i[1] == colour])
    return split_property_by_colour

def get_house_price(colour):
    if int(colour[3]) < 3:
        return 50
    if int(colour[3]) < 5:
        return 100
    if int(colour[3]) < 7:
        return 150
    else:
        return 200
    
def player_landed_on_email(player, game_code):
    email = random.choice(Email.query.all())
    player.money += email.amount
    emit('message', {'msg': player.username + ' landed on email'}, room=game_code)
    emit('message', {'msg': email.text}, room=game_code)

def player_landed_on_student_union(player, game_code):
    student_union = random.choice(Student_union.query.all())
    player.money += student_union.amount
    emit('message', {'msg': player.username + ' landed on student union'}, room=game_code)
    emit('message', {'msg': student_union.text}, room=game_code)

# def player_landed_on_card(player, game_code, session, card):
#     emit('message', {'msg': player.username + ' landed on a pick up card square '}, room=game_code)

def eliminate_players(game):
    for player in game.players_connected:
        if player.money  <= 0:
            tables = [link_player_property, link_player_utilities, link_player_bus_stop]
            broke = True
            for table in tables:
                results = link_table_updates.query_link_table_with_one_id(player.id, False, table)
                for result in results:
                    if result[2] == False:#hasnt been mortgaged
                        broke = False
                        break