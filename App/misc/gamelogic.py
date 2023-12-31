from App.database.tables import Player, Game, Account, Property, Utilities, Bus_stop, Student_union, Email, link_player_property, link_player_bus_stop, link_player_utilities, link_player_email, link_player_student_union
from flask_socketio import emit
import random
from App.main import db, socketio, engine
from App.database import link_table_updates
from . import functions

def show_player_options(player, game_code, session, roll_value):
    pos = player.position
    all_properties = Property.query.all()
    all_utilities = Utilities.query.all()
    all_bus_stops = Bus_stop.query.all()
    
    index_of_properties = [i.position for i in all_properties]
    index_of_utilities = [i.position for i in all_utilities]
    index_of_bus_stops = [i.position for i in all_bus_stops]
    
    if pos in index_of_properties:
        buy_choice_active= player_landed_on_purchasable_card(player, game_code, session, all_properties[index_of_properties.index(pos)], link_player_property, "property")
        return buy_choice_active

    elif pos in index_of_utilities:
        buy_choice_active= player_landed_on_purchasable_card(player, game_code, session, all_utilities[index_of_utilities.index(pos)], link_player_utilities, "utility", roll_value)
        return buy_choice_active

    elif pos in index_of_bus_stops:
        buy_choice_active= player_landed_on_purchasable_card(player, game_code, session, all_bus_stops[index_of_bus_stops.index(pos)], link_player_bus_stop, "bus")
        return buy_choice_active 
    
    pos_email = [7, 17, 28, 36]
    pos_student_union = [2, 12, 22, 33]
    pos_go_to_jail = 30
    pos_free_parking = 20
    pos_jail = 10
    pos_start = 0

    if pos == pos_go_to_jail:
        player_landed_on_go_to_jail(player, game_code, pos_jail, session)
    elif pos == pos_jail:
        player_on_jail(player, game_code, session)
    elif pos == pos_start:
        player_landed_on_start(player, game_code, session)
    elif pos == pos_free_parking:
        player_landed_on_free_parking(player, game_code, session)
    elif pos in pos_email:
        card_table = Email.query.all()
        card_type = "Email"
        player_landed_on_money_card(player, game_code,  card_table, card_type, session)
    elif pos in pos_student_union:
        card_table = Student_union.query.all()
        card_type = "Student Union"
        player_landed_on_money_card(player, game_code,  card_table, card_type, session)

    return False    

def player_landed_on_start(player, game_code, session):
    player.money = player.money + 200
    db.session.commit()
    emit('message', {'msg': f'{player.username} landed on go.'}, room=game_code)
    emit('display text', {'text': f'You landed on go.'}, session=session)
    

def player_landed_on_free_parking(player, game_code, session):
    emit('message', {'msg': f'{player.username} landed on free parking.'}, room=game_code)
    emit('display text', {'text': f'You landed on free parking.'}, session=session)

def player_on_jail(player, game_code, session):
    if player.turns_in_jail == 0:
        emit('message', {'msg': f'{player.username} is just visiting Oak House.'}, room=game_code)
        emit('display text', {'text': f'You are just visiting Oak House.'}, session=session)
    elif player.turns_in_jail == 1:
        emit('message', {'msg': f'{player.username} has 1 turn left in Oak House. They {player.username} must pay §50 to get out.'}, room=game_code)
        emit('display text', {'text': f'You have 1 turn left in Oak House. You must pay §50 to get out.'}, session=session)
        functions.player1_owes_player2_money(player, 50)     
    else:
        emit('message', {'msg': f'{player.username} has {player.turns_in_jail} turns left in Oak House.'}, room=game_code)
        emit('display text', {'text': f'You have {player.turns_in_jail} turns left in Oak House.'}, session=session)
    
    player.turns_in_jail = max(0, player.turns_in_jail-1)
    if player.turns_in_jail == 0:
        functions.player1_owes_player2_money(player, 50)
    db.session.commit()

    return False


def player_landed_on_go_to_jail(player, game_code, pos_jail, session):
    player.turns_in_jail += 3
    player.position = pos_jail
    db.session.commit()
    emit('message', {'msg': f'{player.username} is sent to Oak House.'}, room=game_code)
    emit('flash function', session=session)
    emit('display text', {'text': f'You are sent to Oak House.'}, session=session)


def player_landed_on_purchasable_card(player, game_code, session, card, link_table, type, roll_value=None):
    #returns true to show buy button and false otherwise
    emit('message', {'msg': f'{player.username} landed on {card.name}.'}, room=game_code)
    emit('display text', {'text': f'You landed on {card.name}.'}, session=session)

    #selects the row in the table recording who owns what property with the id of the property that was landed on
    with engine.connect() as conn:
        players_in_game = Player.query.filter_by(game_code=game_code).all()
        player_ids_in_game = [i.id for i in players_in_game]
        
        #creates row_ingame_with card which is the card from the link table that the player landed on in current game
        query = link_table.select().where(link_table.c.card_id == card.id)
        rows_with_card = conn.execute(query).fetchall()
        row_ingame_with_card = None
        for row in rows_with_card:
            if row.player_id in player_ids_in_game:
                row_ingame_with_card = row
                break

        ##if that card hasnt been purchased yet
        if row_ingame_with_card == None:
            emit('display text', {'text': f' You can buy it for §{card.buy_price}'})
            emit('buy property button change', {'operation':'show'}, session=session)
            return True

        #you own the card
        elif row_ingame_with_card.player_id == player.id:
            emit('display text', {'text': 'You already own this square'}, session=session)
            return False
    
        #someone owns it and it isn't you so get the rent you need to pay and who needs paying
        if type == "property":
            rent_amount, player_owed = get_property_rent_amount(card, link_table, player_ids_in_game)
        elif type == "utility":
            rent_amount, player_owed = get_bus_or_utility_rent_amount(card, link_table, player_ids_in_game, type, roll_value)
        elif type == "bus":
            rent_amount, player_owed = get_bus_or_utility_rent_amount(card, link_table, player_ids_in_game, type)
        
        #pays the rent to the player owed
        emit('message', {'msg':f'{player.username} owes §{str(rent_amount)} to {player_owed.username}'}, room=game_code)
        emit('display text', {'text': f'You owe §{str(rent_amount)} to {player_owed.username}'}, session=session)
        functions.player1_owes_player2_money(player, rent_amount, player_owed)
        return False
    
def player_landed_on_money_card(player, game_code, card_table, card_type, session):
    money_card = random.choice(card_table)
    if money_card.amount != 0:
        player.money += money_card.amount
    elif money_card.amount == 0:
        player.position = money_card.go_to
        if money_card.go_to == 10:
            player.turns_in_jail = 3

        game_code = session.get('game_code')
        username = session.get('username')
        game, player123 = functions.check_in_game(game_code, username)
        
        update_position(game, game_code)

    db.session.commit()
    emit('message', {'msg': f'{player.username} landed on {card_type.lower()}'}, room=game_code)
    text = money_card.text.replace('Â', '')
    emit('display text', {'text': text}, session=session)
    
def update_position(game, game_code):
    players = [[i, None, None, 0] for i in range(40)]
    for i in game.players_connected:
        if players[i.position][1] == None:
            players[i.position][1] = i.username
            players[i.position][2] = str(i.symbol)
            players[i.position][3] = str(i.turns_in_jail)
        else:
            players[i.position][1] = players[i.position][1] + ',' + i.username
            players[i.position][2] = players[i.position][2] + ',' + str(i.symbol)
            players[i.position][3] = players[i.position][3] + ',' + str(i.turns_in_jail)
    players = [i for i in players if i[1]!= None]
    emit('update player positions', {'players': players}, room=game_code) 

def get_property_rent_amount(card, link_table, player_ids_in_game):
    with engine.connect() as conn:
        ##finds the ids of the cards that are the same colour as the card that was landed on
        card_colour = Property.query.filter_by(id=card.id).first().colour
        cards_with_colour = Property.query.filter_by(colour=card_colour).all()
        card_ids_with_colour = [i.id for i in cards_with_colour]
        
        ##finds the ids that own this landed on card in the link table
        renter_id_query = link_table.select().where(link_table.c.card_id == card.id)
        card_rows = conn.execute(renter_id_query).fetchall()

        ##chooses the owner specific to this game
        for card_row in card_rows:
            if card_row.player_id in player_ids_in_game:
                renter_id = card_row.player_id
                break
        no_of_houses = card_row.houses

        ##finds the number of the properties of the select colour that the renter owns
        number_of_colour_owned = 0
        for card_id_with_colour in card_ids_with_colour:
            number_of_colour_owned_query = link_table.select().where(link_table.c.card_id==card_id_with_colour, link_table.c.player_id==renter_id)
            if conn.execute(number_of_colour_owned_query).fetchone() != None:
                number_of_colour_owned += 1

        player_owed = Player.query.filter_by(id=renter_id).first()

        ##returns the first rent amount if the renter does not own the set 
        if number_of_colour_owned < len(card_ids_with_colour):
            return int(card.rents.split(',')[0]), player_owed
        
        ##returns the rent amount associated with the set and the number of houses owned by the renter
        elif number_of_colour_owned == len(card_ids_with_colour):
            return int(card.rents.split(',')[1+no_of_houses]), player_owed
        


def get_bus_or_utility_rent_amount(card, link_table, player_ids_in_game, type, roll_value=None):
    with engine.connect() as conn:
        ##finds the ids that own this landed on card in the link table
        renter_id_query = link_table.select().where(link_table.c.card_id == card.id)
        card_rows = conn.execute(renter_id_query).fetchall()

        ##chooses the owner specific to this game
        for card_row in card_rows:
            if card_row.player_id in player_ids_in_game:
                renter_id = card_row.player_id
                break

        ##finds the number of bus stops/utilities owned by the renter
        no_owned = 0
        if type == "utility":
            ids_of_cards = [1,2]
        elif type == "bus":
            ids_of_cards = [1,4]
        
        for id_of_card in ids_of_cards:
            no_owned_query = link_table.select().where(link_table.c.card_id==id_of_card, link_table.c.player_id==renter_id)
            if conn.execute(no_owned_query).fetchone() != None:
                no_owned += 1

        ##returns the rent amount associated with the number of bus stops or utilities owned by the renter and the renter
        if type == "bus": 
            bus_rents = [25, 50, 100, 200]
            rent = bus_rents[no_owned-1]
        elif type == "utility":
            if no_owned == 1:
                rent = roll_value * 4
            elif no_owned == 2:
                rent = roll_value * 10


        player_owed = Player.query.filter_by(id=renter_id).first()
        return rent, player_owed

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
                card = i[1].query.filter_by(id=card[1]).first()
                unmortgaged_cards.append(card.photo)
                unmortgaged_cards_id.append(card.id)
            query = i[0].select().where(i[0].c.player_id == player.id, i[0].c.mortgaged == True)
            card_row = conn.execute(query).fetchall()
            for card in card_row:
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

def check_if_mortgaged(player_id, photo):
    card = Property.query.filter_by(photo=photo).first()
    table = link_player_property
    if not card:
        card = Bus_stop.query.filter_by(photo=photo).first()
        table = link_player_bus_stop
    if not card:
        card = Utilities.query.filter_by(photo=photo).first()
        table = link_player_utilities
    
    card_id = card.id
    amount = card.morgage_value

    result = link_table_updates.query_link_table_with_two_id(player_id, card_id, table, True)
    return amount, table, result
# def eliminate_players(game):
#     for player in game.players_connected:
#         if player.money  <= 0:
#             tables = [link_player_property, link_player_utilities, link_player_bus_stop]
#             broke = True
#             for table in tables:
#                 results = link_table_updates.query_link_table_with_one_id(player.id, False, table)
#                 for result in results:
#                     if result[2] == False:#hasnt been mortgaged
#                         broke = False
#                         break

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