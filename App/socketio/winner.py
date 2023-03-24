from flask import session
from flask_socketio import emit, join_room, leave_room
from App.main import db, socketio, engine
from App.misc.functions import check_in_game, player1_owes_player2_money
from random import randint
from sqlalchemy import update, and_
from App.misc import gamelogic, functions
from App.database.tables import link_player_property, link_player_bus_stop, link_player_utilities, Player, Game, Property, Bus_stop, Utilities
from App.database import link_table_updates


@socketio.on('get winner', namespace='/winner')
def get_winner(data):
    game_code = session.get('game_code')
    game = Game.query.filter_by(game_code=game_code).first()
    if game != None:
        winner = False
        for player in game.players_connected:
            if player.money != -1000000:
                winner = player.username
    return winner
