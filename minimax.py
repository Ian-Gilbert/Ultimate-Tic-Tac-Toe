from math import inf
import random as rand
import copy
import boardclasses


COMP = 0
HUMAN = 0


def heuristic(state):
    # heuristic evaluation of the current board state
    if state.has_tic_tac_toe(COMP):
        score = 1
    elif state.has_tic_tac_toe(HUMAN):
        score = -1
    else:
        score = 0
    return score


def get_empty_cells(state):
    # Returns the coordinates of all the unclaimed spaces on the board
    cells = []
    for row_index, row in enumerate(state.board):
        for col_index, col in enumerate(row):
            if col == 0:
                cells.append([row_index, col_index])
    return cells


def minimax(state, depth, player):
    if player == COMP:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, inf]

    if depth == 0 or state.has_tic_tac_toe(COMP) or state.has_tic_tac_toe(HUMAN):
        score = heuristic(state)
        return [-1, -1, score]

    # print(get_empty_cells(state), depth)
    for cell in get_empty_cells(state):
        row, col = cell[0], cell[1]
        state.board[row][col] = player
        score = minimax(state, depth - 1, (player % 2) + 1)
        score[0], score[1] = row, col

        if player == COMP:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best


def bot_turn(global_board, bot):
    # Determine if the bot is player 1 or 2
    global COMP
    global HUMAN
    COMP = bot
    HUMAN = (bot % 2) + 1

    # If the next board is undetermined
    if all(lb.focus == lb.playable for lb in global_board.local_boards):
        # Use minimax on the global board to determine the next local board
        depth = len(get_empty_cells(global_board))
        if depth == 9:
            row = rand.choice([0, 1, 2])
            col = rand.choice([0, 1, 2])
        else:
            state = boardclasses.TicTacToeBoard()
            state.board = copy.deepcopy(global_board.board)
            row, col, _ = minimax(state, depth, COMP)

        local_board = global_board.local_boards[row * 3 + col]

    else:
        # Find the local board in focus
        for lb in global_board.local_boards:
            if lb.focus:
                local_board = lb
                break

    # local_board now defined. Use minimax to find row and col of next move
    depth = len(get_empty_cells(local_board))
    if depth == 9:
        row = rand.choice([0, 1, 2])
        col = rand.choice([0, 1, 2])
    else:
        state = boardclasses.TicTacToeBoard()
        state.board = copy.deepcopy(local_board.board)
        row, col, _ = minimax(state, depth, COMP)

    return local_board, row, col
