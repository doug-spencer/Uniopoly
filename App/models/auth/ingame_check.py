from App.models.classes.main import Account, Game

def check_in_game(game_name, username): #verification fucntion
    game = Game.query.filter_by(game_name = game_name).first()
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