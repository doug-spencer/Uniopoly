def jump_spaces(current_position, spaces_to_jump):
    """
    This function takes two parameters:
    current_position: the current position of the player on the board
    spaces_to_jump: the number of spaces the player needs to jump
    """
    final_position = (current_position + spaces_to_jump) % 40
    if final_position == 30:
        # Player lands on "Go to Jail" square
        return 10
    elif final_position in [2, 17, 33]:
        # Player lands on Community Chest square
        # You can randomly choose to move the player to a specific square or keep them on the same square
        return final_position
    elif final_position in [7, 22, 36]:
        # Player lands on Chance square
        # You can randomly choose to move the player to a specific square or keep them on the same square
        return final_position
    else:
        return final_position


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

def go_back_spaces(current_position, spaces_to_move_back):
    updated_position = current_position - spaces_to_move_back
    if updated_position < 0:
        # To make sure the updated position is not negative
        updated_position = 0
    return updated_position

def pause_page():
    print("The game is paused.")
    while True:
        choice = input("Do you want to resume or quit the game? (r/q)").lower()
        if choice == "r":
            break
        elif choice == "q":
            quit()
        else:
            print("Invalid choice. Please enter 'r' to resume or 'q' to quit.")




'''Just a list of functions that could be used.'''