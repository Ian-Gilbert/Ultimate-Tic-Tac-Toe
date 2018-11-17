import pygame
import sys
import boardclasses as bc


def get_lb_name(key):
    # Returns the name of the local board given lb_index as a key
    switcher = {
        0: "top left",
        1: "top center",
        2: "top right",
        3: "center left",
        4: "center board",
        5: "center right",
        6: "bottom left",
        7: "bottom center",
        8: "bottom right"
    }
    return switcher.get(key)


def get_next_board(old_row, old_col):
    """Use previous move to return the next local board"""
    new_lb_index = old_row * 3 + old_col
    new_lb = board.local_boards[new_lb_index]

    # If the next board has tic tac toe or is full
    if not new_lb.playable:
        for local_board in board.local_boards:
            local_board.focus = local_board.playable
        while not new_lb.focus:
            print(f"The {get_lb_name(lb_index)} board is not playable.")
            new_lb_index = int(input(f"Player {player}, please select your local board (1-9): ")) - 1
            new_lb = board.local_boards[new_lb_index]

    return new_lb_index, new_lb


board = bc.GlobalBoard()
player = 1

lb_index = int(input(f"Player {player}, please select your local board (1-9): ")) - 1
lb = board.local_boards[lb_index]

# TODO: reorganize logic so that board number is requested at the beginning of each turn, and the focus is updated at
# TODO: the end of the turn, to better match with how the GUI will work

while True:
    board.print_board()
    print(f"The {get_lb_name(lb_index)} board is in focus.")
    row = int(input(f"Player {player}, please enter the row (1-3): ")) - 1
    col = int(input(f"Player {player}, please enter the column (1-3): ")) - 1
    if lb.board[row][col] == 0:
        lb.board[row][col] = player

        if lb.has_tic_tac_toe():
            lb.playable = False
            board.mark_board(lb_index, player)
            if board.has_tic_tac_toe():
                print(f"Player {player} has won!")
                break
            elif board.is_full():
                print("The game is a draw.")
                break
        elif lb.is_full():
            lb.playable = False

        player = (player % 2) + 1
        lb_index, lb = get_next_board(row, col)
    else:
        print("That space has already been played.")
