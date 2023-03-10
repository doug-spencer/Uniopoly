from App.database.tables import Player, Game, Account, Property, Utilities, Bus_stop, link_player_property, link_player_bus_stop, link_player_utilities
from App.database.link_table_updates import query_link_table_with_one_id
from flask_socketio import emit
from App.main import db, socketio, engine


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

    if pos == pos_go_to_jail:
        player_landed_on_go_to_jail(player, game_code, session)
    if pos == pos_jail:
        player_on_jail(player, game_code, session)
    if pos == pos_start:
        player_landed_on_start(player, game_code, session)
    if pos == pos_free_parking:
        player_landed_on_free_parking(player, game_code, session)

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
        query = link_table.select().where(link_table.c.card_id == card.id)##########ERROR
        card_row = conn.execute(query).fetchone()

        #nobody owns it
        print("here2")

        if card_row == None:
            print("here3")
            halt_player_turn(game_code)
            emit('buy property button change', {'operation':'show'}, session=session)
            emit('roll dice button change', {'operation':'hide'}, session=session)
            return True #to stop the next player getting to roll the dice

        #you own it
        elif card_row.player_id == player.id:
            return False
    
        #someone owns it and it isn't you so pay rent
        pay_rent()
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

def pay_rent():
    pass

def get_cards(player):
    unmortgaged_cards = []
    mortgaged_cards = []
    tables = [[link_player_property, Property], [link_player_utilities, Utilities], [link_player_bus_stop, Bus_stop]]
    with engine.connect() as conn:
        for i in tables:
            query = i[0].select().where(i[0].c.player_id == player.id, i[0].c.mortgaged == False)
            card_row = conn.execute(query).fetchall()
            for card in card_row:
                print(card_row)
                card = i[1].query.filter_by(id=card[1]).first()
                unmortgaged_cards.append(card.photo)
            query = i[0].select().where(i[0].c.player_id == player.id, i[0].c.mortgaged == True)
            card_row = conn.execute(query).fetchall()
            for card in card_row:
                print(card_row)
                card = i[1].query.filter_by(id=card[1]).first()
                mortgaged_cards.append(card.photo)
    return unmortgaged_cards, mortgaged_cards

def get_houses(player):
    property = []
    colour_sets = []
    colour_count = {}
    with engine.connect() as conn:
        query = link_player_property.select().where(link_player_property.c.player_id == player.id)
        card_row = conn.execute(query).fetchall()
    for card in card_row:
        card = Property.query.filter_by(id=card[1]).first()
        if card.colour not in colour_sets:
            colour_sets.append(card.colour)
            colour_count[card.colour] = 1
        property.append([card.name, card.colour])
    for key in colour_count:
        if colour_count[key] >= 3:
            pass


def player_landed_on_card(player, game_code, session, card):
    emit('message', {'msg': player.username + ' landed on a pick up card square '}, room=game_code)