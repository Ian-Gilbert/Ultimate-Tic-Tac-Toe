"""
This is a modified version of the minimax algorithm for Tic Tac Toe from the following source:
Link: https://github.com/Cledersonbc/tic-tac-toe-minimax

An implementation of Minimax AI Algorithm in Tic Tac Toe, using Python.
This software is available under GPL license.
Author: Clederson Cruz
Year: 2017
License: GNU GENERAL PUBLIC LICENSE (GPL)
"""


from typing import Tuple, List, Optional
from math import inf
from random import choice
from copy import deepcopy
from src.boardclasses import TicTacToeBoard, LocalBoard, GlobalBoard


COMP: int
HUMAN: int


def heuristic(state: TicTacToeBoard, depth: int) -> int:
    """
    Heuristic evaluation of the current board state
    :param state: the current board state
    :param depth: the number of empty spaces left on the board. Preference is given for faster wins and slower losses.
    """
    if state.has_tic_tac_toe(COMP):
        score = depth + 1
    elif state.has_tic_tac_toe(HUMAN):
        score = -(depth + 1)
    else:  # draw/undetermined outcome
        score = 0
    return score


def get_empty_cells(state: TicTacToeBoard) -> List[Tuple[int, int]]:
    """
    Returns the coordinates of all the unclaimed spaces on the board
    :param state: the current board state
    :return: The coordinates of all the empty cells left on the board
    """
    cells = []
    for row_index, row in enumerate(state.board):
        for col_index, cell in enumerate(row):
            if cell == 0:
                cells.append((row_index, col_index))
    return cells


def minimax(state: TicTacToeBoard, depth: int, player: int) -> List[int]:
    """
    The minimax algorithm itself. Returns a random move if the depth is 9, otherwise the first move would always be the
    top left corner.
    :param state: the current board state
    :param depth: the number of empty spaces left on the board
    :param player: who makes the next move (1 or 2)
    :return: coordinates of the best move for the current branch at the current depth, along with the score of that
    move, defined by the heuristic function
    """
    if depth == 9:
        row = choice([0, 1, 2])
        col = choice([0, 1, 2])
        return [row, col, 0]

    if player == COMP:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, inf]

    if depth == 0 or state.has_tic_tac_toe(COMP) or state.has_tic_tac_toe(HUMAN):
        score = heuristic(state, depth)
        return [-1, -1, score]

    for row, col in get_empty_cells(state):  # iterate through list of available moves
        state.board[row][col] = player  # mark current available move for current player
        result = minimax(state, depth - 1, (player % 2) + 1)  # search through branch until it terminates
        state.board[row][col] = 0  # undo move for future iterations
        result[0], result[1] = row, col  # set result to current move

        # If COMP move is better than previous best move, make this the new best
        if player == COMP:
            if result[2] > best[2]:
                best = result
        # Same for HUMAN move, but reversed. We want most negative move, because that is good for the human
        else:
            if result[2] < best[2]:
                best = result

    return best


def bot_turn(global_board: GlobalBoard, bot: int):
    """
    Finds the next local board to play on. If undefined, it uses the minimax algorithm to decide which board to play on.
    Then uses the minimax algorithm again to decide where to play on that board.
    :param global_board: The entire global board of the game
    :param bot: is the bot player 1 or 2?
    :return: local_board and coordinates of the bot's next move
    """
    # Determine if the bot is player 1 or 2
    global COMP
    global HUMAN
    COMP = bot
    HUMAN = (bot % 2) + 1
    local_board: Optional[LocalBoard] = None

    # If the next board is undetermined
    if all(lb.focus == lb.playable for lb in global_board.local_board_list):
        # Use minimax on the global board to determine the next local board
        depth = len(get_empty_cells(global_board))
        state = TicTacToeBoard()
        state.board = deepcopy(global_board.board)
        row, col, _ = minimax(state, depth, COMP)

        local_board = global_board.local_board_list[row * 3 + col]

    else:
        # Find the local board in focus
        for lb in global_board.local_board_list:
            if lb.focus:
                local_board = lb
                break

    assert local_board is not None

    # local_board now defined. Now use minimax to find row and col of next move
    depth = len(get_empty_cells(local_board))
    state = TicTacToeBoard()
    state.board = deepcopy(local_board.board)
    row, col, _ = minimax(state, depth, COMP)

    return local_board, row, col
