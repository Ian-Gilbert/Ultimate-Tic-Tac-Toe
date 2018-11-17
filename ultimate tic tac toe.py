import pygame
import sys
import boardclasses as bc


def get_sb_name(key):
    # Returns the name of the small board given sb_index as a key
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
    """Use previous move to return the next small board"""
    new_sb_index = old_row * 3 + old_col
    new_sb = board.small_boards[new_sb_index]

    # If the next board has tic tac toe or is full
    if not new_sb.playable:
        for small_board in board.small_boards:
            small_board.focus = small_board.playable
        while not new_sb.focus:
            print(f"The {get_sb_name(sb_index)} board is not playable.")
            new_sb_index = int(input(f"Player {player}, please select your small board (1-9): ")) - 1
            new_sb = board.small_boards[new_sb_index]

    return new_sb_index, new_sb


board = bc.BigBoard()
player = 1

sb_index = int(input(f"Player {player}, please select your small board (1-9): ")) - 1
sb = board.small_boards[sb_index]

while True:
    board.print_board()
    print(f"The {get_sb_name(sb_index)} board is in focus.")
    row = int(input(f"Player {player}, please enter the row (1-3): ")) - 1
    col = int(input(f"Player {player}, please enter the column (1-3): ")) - 1
    if sb.board[row][col] == 0:
        sb.board[row][col] = player

        if sb.has_tic_tac_toe():
            sb.playable = False
            board.mark_board(sb_index, player)
            if board.has_tic_tac_toe():
                print(f"Player {player} has won!")
                break
            elif board.is_full():
                print("The game is a draw.")
                break
        elif sb.is_full():
            sb.playable = False

        player = (player % 2) + 1
        sb_index, sb = get_next_board(row, col)
    else:
        print("That space has already been played.")
