import random

def roll_dice():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return dice1 + dice2

def move_player(player_position, dice_roll):
    player_position += dice_roll
    if player_position > 40:
        player_position -= 40
    return player_position

def check_space(player_position, player, board):
    space = board[player_position]
    if space == "Go":
        player["money"] += 200
    elif space == "Jail":
        player["jailed"] = True
    elif space == "Property":
        property_owner = board[player_position]["owner"]
        if property_owner is not None and property_owner != player["name"]:
            rent = board[player_position]["rent"]
            player["money"] -= rent
    return player

def send_to_jail(player):
    player["position"] = 10
    player["jailed"] = True
    return player

def get_out_of_jail(player):
    player["jailed"] = False
    return player

def pay_jail_fine(player):
    player["money"] -= 50
    return player

class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.properties = []
        
    def add_property(self, property):
        self.properties.append(property)
        
    def remove_property(self, property):
        self.properties.remove(property)
        
    def has_property(self, property):
        return property in self.properties

    def is_bankrupt(self, threshold=0):
        return self.money < threshold

class Property:
    def __init__(self, name, cost, owner=None):
        self.name = name
        self.cost = cost
        self.owner = owner
        
    def set_owner(self, owner):
        self.owner = owner
        
class Game:
    def __init__(self, players):
        self.players = players
        self.board = [
            "Go",
            Property("Mediterranean Avenue", 60),
            "Community Chest",
            Property("Baltic Avenue", 60),
            "Income Tax",
            Property("Reading Railroad", 200),
            Property("Oriental Avenue", 100),
            "Chance",
            Property("Vermont Avenue", 100),
            Property("Connecticut Avenue", 120),
            "Jail",
            Property("St. Charles Place", 140),
            "Electric Company",
            Property("States Avenue", 140),
            Property("Virginia Avenue", 160),
            Property("Pennsylvania Railroad", 200),
            Property("St. James Place", 180),
            "Community Chest",
            Property("Tennessee Avenue", 180),
            Property("New York Avenue", 200),
            "Free Parking",
            Property("Kentucky Avenue", 220),
            "Chance",
            Property("Indiana Avenue", 220),
            Property("Illinois Avenue", 240),
            Property("B. & O. Railroad", 200),
            Property("Atlantic Avenue", 260),
            Property("Ventnor Avenue", 260),
            "Water Works",
            Property("Marvin Gardens", 280),
            "Go to Jail",
            Property("Pacific Avenue", 300),
            Property("North Carolina Avenue", 300),
            "Community Chest",
            Property("Pennsylvania Avenue", 320),
            "Short Line",
            "Chance",
            Property("Park Place", 350),
            "Luxury Tax",
            Property("Boardwalk", 400)
        ]
        
    def play_turn(self, player):
        dice_roll = roll_dice()
        player.position = move_player(player.position, dice_roll)
        player = check_space(player, self.board)
        return player
        
    def trade(self, player1, player2, property1, property2, money1, money2):
        if property1 in player1.properties and property2 in player2.properties:
            if player1.money >= money1 and player2.money >= money2:
                player1.properties.remove(property1)
                player2.properties.append(property1)
                player2.properties.remove(property2)
                player1.properties.append(property2)
                player1.money -= money
                player2.money += money
                player2.money -= money2
                player1.money += money2

    

def main():
    # Create players
    player1 = Player("Player 1", 1500)
    player2 = Player("Player 2", 1500)
    players = [player1, player2]
    
    # Create a game
    game = Game(players)
    
    # Start playing the game
    while True:
        for player in game.players:
            if player.is_bankrupt():
                print(f"{player.name} has gone bankrupt and lost the game!")
                return
            else:
                player = game.play_turn(player)
                
if __name__ == "__main__":
    main()


                
    
'''Probably quite a few mistakes in here, was just brainstorming. Add anything or change if you see mistakes'''