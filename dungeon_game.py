import random
from subprocess import call

CELLS = [(0, 0), (0, 1), (0, 2)
       , (1, 0), (1, 1), (1, 2)
       , (2, 0), (2, 1), (2, 2)]

def get_starting_positions(cells):
    player_start = random.choice(cells)
    door_placement = random.choice(cells)
    monster_start = random.choice(cells)

    while door_placement == player_start:
        door_placement = random.choice(cells)

    while (monster_start == player_start or 
        monster_start == door_placement):
        monster_start = random.choice(cells)

    return player_start, door_placement, monster_start

def valid_moves(player_position):
    valid_movements = ["left", "right", "up", "down"]

    if player_position[1] == 0:
        valid_movements.remove("left")
    if player_position[1] == 2:
        valid_movements.remove("right")
    if player_position[0] == 0:
        valid_movements.remove("up")
    if player_position[0] == 2:
        valid_movements.remove("down")

    return valid_movements

def valid_monster_moves(monster_position, door_position):
    valid_movements = ["left", "right", "up", "down", "no_move"]

    new_placement_if_monster_moves_left = (monster_position[0], monster_position[1] - 1)
    new_placement_if_monster_moves_right = (monster_position[0], monster_position[1] + 1)
    new_placement_if_monster_moves_up = (monster_position[0] - 1, monster_position[1])
    new_placement_if_monster_moves_down = (monster_position[0] + 1, monster_position[1])

    if monster_position[1] == 0 or new_placement_if_monster_moves_left == door_position:
        valid_movements.remove("left")
    if monster_position[1] == 2 or new_placement_if_monster_moves_right == door_position:
        valid_movements.remove("right")
    if monster_position[0] == 0 or new_placement_if_monster_moves_up == door_position:
        valid_movements.remove("up")
    if monster_position[0] == 2 or new_placement_if_monster_moves_down == door_position:
        valid_movements.remove("down")

    return valid_movements

def show_current_grid(piece_positions, cells):
    grid_picture = []
    for idx, cell in enumerate(cells):
        if piece_positions[0] == cell:
            grid_picture.append('[P]')
        elif piece_positions[1] == cell:
            grid_picture.append('[D]')
        elif piece_positions[2] == cell:
            grid_picture.append('[M]')
        else:
            grid_picture.append('[ ]')

        if idx > 0 and (idx + 1) % 3 == 0:
            grid_picture.append('\n')

    return ''.join(grid_picture)

def list_contains(item, list):
    for list_item in list:
        if item == list_item:
            return True
    return False

def move_piece(direction, piece_position):
    if direction == 'left':
        return piece_position[0], piece_position[1] - 1
    elif direction == 'right':
        return piece_position[0], piece_position[1] + 1
    elif direction == 'up':
        return piece_position[0] - 1, piece_position[1]
    elif direction == 'down':
        return piece_position[0] + 1, piece_position[1]
    else:
        return piece_position

def move_monster(valid_directions, monster_position):
    return move_piece(random.choice(valid_directions), monster_position)

player, door, monster = get_starting_positions(CELLS)

call(['clear'])
print("Welcome to the dungeon! Try to move your player (P) to the door (D) before the monster (M) catches you\n" +
    "Type 'quit' to quit game. Otherwise try your luck with 'left', 'right', 'up', and 'down'; Good Luck!")

while True:
    print("Here's what the current situation is:\n{}".format(show_current_grid((player, door, monster), CELLS)))
    print("Here are your valid movement commands: {}".format(', '.join(valid_moves(player)).upper()))
    user_input = input("> ").lower()

    if user_input == "quit":
        print("See you later, quitter!")
        break
    elif list_contains(user_input, valid_moves(player)):
        player = move_piece(user_input, player)
        monster = move_monster(valid_monster_moves(monster, door), monster)
        if player == door:
            print("You made it out alive, this time. You Win!")
            break;
        if player == monster:
            print("The monster ate your flesh. You Lose!")
            break;
        continue
    else:
        print("Invalid command!")
        continue