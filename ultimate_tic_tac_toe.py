import random as rand
import sys
from boardclasses import GlobalBoard
import minimax
from gui.pyg_init import *  # contains pygame import
from gui import pyg_util

"""PyGame Initialization"""
pygame.init()

# define the main screen
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Ultimate Tic Tac Toe")

rules = pyg_util.RulesScreen()

# menu items
textarea = pyg_util.TextArea()

rulesbutton = pyg_util.Button((GLOBALBOARDSIZE + BOARDERSIZE, BOARDERSIZE + int(1.75 * SQUARESIZE),
                               LOCALBOARDSIZE, SQUARESIZE), 'Show Rules', colorfamily=BLUE_FAMILY, textcolor=LIGHT_GRAY)
newgamebutton = pyg_util.Button((GLOBALBOARDSIZE + BOARDERSIZE, SCREENHEIGHT - BOARDERSIZE - int(2.75 * SQUARESIZE),
                                 LOCALBOARDSIZE, SQUARESIZE), 'New Game', colorfamily=GREEN_FAMILY)
quitbutton = pyg_util.Button((GLOBALBOARDSIZE + BOARDERSIZE, SCREENHEIGHT - BOARDERSIZE - int(1.25 * SQUARESIZE),
                              LOCALBOARDSIZE, SQUARESIZE), 'Quit Game', colorfamily=RED_FAMILY)
alg_options = pyg_util.GameOptions((GLOBALBOARDSIZE + BOARDERSIZE, LOCALBOARDSIZE + WHITESPACE), 'Very Easy',
                                   '2 Player', 'Very Easy', 'Easy', 'Medium', 'Hard')
order_options = pyg_util.GameOptions(
    (GLOBALBOARDSIZE + BOARDERSIZE + int(.55 * LOCALBOARDSIZE), LOCALBOARDSIZE + WHITESPACE), 'Random', 'Random',
    'First', 'Second')
"""End PyGame Initialization"""


def init_variables():
    """Initializes the game variables to their defaults."""
    global global_board, player, bot, bot_alg, game_over, reset

    # Global board
    global_board = GlobalBoard()

    player = 1  # player will always be 1 or 2. 1 -> 'X' and 2 -> 'O'

    bot_alg = alg_options.get_option()
    mode = order_options.get_option()

    # Decide whether the bot goes first or second
    if bot_alg == '2 Player':
        bot = 0
    elif mode == 'Random':
        bot = rand.randint(1, 2)
    elif mode == 'First':
        bot = 2
    elif mode == 'Second':
        bot = 1

    game_over = False  # break out of the game loop when the game ends
    reset = False  # after the game, you are stuck in keep_alive() until reset == True

    # global_board.print_board()  # command line
    draw_board()  # GUI
    draw_menu()  # GUI
    pygame.display.flip()


def draw_menu():
    """Draws the menu area on the right side of the GUI"""
    pygame.draw.rect(screen, DARK_GRAY, MENUAREA)

    # text box
    update_text()

    # Display Buttons
    rulesbutton.draw(screen, False)
    newgamebutton.draw(screen, False)
    quitbutton.draw(screen, False)

    alg_options.draw(screen)
    order_options.draw(screen)


def update_text():
    """Updates the text displayed on the TextArea"""
    if not game_over:
        if player != bot:
            if player == 1:
                textarea.set_text("Player X:", "Make your move", screen, color=BLUE)
            else:
                textarea.set_text("Player O:", "Make your move", screen, color=RED)
    else:
        if player == 0:
            textarea.set_text("The game is", "a draw.", screen)
        elif player == 1:
            textarea.set_text("Player X", "has won!", screen, color=BLUE)
        else:
            textarea.set_text("Player O", "has won!", screen, color=RED)


def draw_board(update=True):
    """Displays the full global and local boards in the GUI. Does not update the menu"""
    pygame.draw.rect(screen, LIGHT_GRAY, GLOBALBOARDAREA)

    # For each local board
    for outer_x in range(3):
        for outer_y in range(3):
            # Get the current local board
            local_board = global_board.local_boards[outer_y * 3 + outer_x]

            # Top left coordinate of the current local board
            board_origin_x = BOARDERSIZE + ((LOCALBOARDSIZE + WHITESPACE) * outer_x)
            board_origin_y = BOARDERSIZE + ((LOCALBOARDSIZE + WHITESPACE) * outer_y)

            # Color the board accordingly if it is won by X or O, or if it is in focus
            if local_board.focus and not game_over:  # if the game is over, nothing is in focus
                pygame.draw.rect(screen, WHITE, (board_origin_x, board_origin_y, LOCALBOARDSIZE, LOCALBOARDSIZE))
            elif global_board.board[outer_y][outer_x] == 1:
                pygame.draw.rect(screen, LIGHT_BLUE, (board_origin_x, board_origin_y, LOCALBOARDSIZE, LOCALBOARDSIZE))
            elif global_board.board[outer_y][outer_x] == 2:
                pygame.draw.rect(screen, LIGHT_RED, (board_origin_x, board_origin_y, LOCALBOARDSIZE, LOCALBOARDSIZE))

            # Draw the grid lines for the local board
            for i in range(4):
                # Vertical Grid Lines
                start_x = board_origin_x + (SQUARESIZE * i)
                start_y = board_origin_y
                pygame.draw.line(screen, BLACK, (start_x, start_y), (start_x, start_y + LOCALBOARDSIZE))

                # Horizontal Grid Lines
                start_x = board_origin_x
                start_y = board_origin_y + (SQUARESIZE * i)
                pygame.draw.line(screen, BLACK, (start_x, start_y), (start_x + LOCALBOARDSIZE, start_y))

            # For each square in the local board
            for inner_x in range(3):
                for inner_y in range(3):
                    # Get the center of the square
                    center_x = board_origin_x + (SQUARESIZE * inner_x) + SQUARESIZE // 2
                    center_y = board_origin_y + (SQUARESIZE * inner_y) + SQUARESIZE // 2
                    center = (center_x, center_y)

                    # Draw an 'X' or 'O' if appropriate
                    if local_board.board[inner_y][inner_x] == 1:
                        draw_x(center, screen)
                    elif local_board.board[inner_y][inner_x] == 2:
                        pygame.draw.circle(screen, RED, center, DIFF, 4)

    if update:
        pygame.display.update(GLOBALBOARDAREA)


# def get_lb_name(local_board):
#     # Returns the physical location of the local board given lb as a key (for the command line)
#     switcher = {
#         0: "top left",
#         1: "top center",
#         2: "top right",
#         3: "center left",
#         4: "center board",
#         5: "center right",
#         6: "bottom left",
#         7: "bottom center",
#         8: "bottom right"
#     }
#     return switcher.get(local_board.index)


def get_inputs():
    """Gets the current position of the mouse and returns the local board, as well as row and column coordinates of the
    square that the mouse is currently in. If the mouse is not in a square, then local_board will return None."""

    x_pos, y_pos = pygame.mouse.get_pos()  # current x and y coordinates of the mouse
    local_board = None  # default value for local_board

    # For each local board
    for x in range(3):
        for y in range(3):
            # Top left coordinate of the current local board
            board_origin_x = BOARDERSIZE + ((LOCALBOARDSIZE + WHITESPACE) * x)
            board_origin_y = BOARDERSIZE + ((LOCALBOARDSIZE + WHITESPACE) * y)

            # If the mouse is over one of the boards, set local_board accordingly
            if board_origin_x < x_pos < board_origin_x + LOCALBOARDSIZE and \
                    board_origin_y < y_pos < board_origin_y + LOCALBOARDSIZE:
                local_board = global_board.local_boards[y * 3 + x]
                break
        # How to break out of nested for loops in python:
        else:  # if the inner loop does not break, continue
            continue
        break  # if the inner loop does break, then break out of the outer loop too

    # row and col will be nonsense if the mouse is not over a board. Need to ensure local_board is not None before using
    row_pos = (y_pos - board_origin_y) // SQUARESIZE
    col_pos = (x_pos - board_origin_x) // SQUARESIZE

    return local_board, row_pos, col_pos


# def get_next_move():
#     # Request local board and row and col coordinates from the player (for the command line)
#     # DO NOT RUN WHILE USING THE GUI
#     while True:
#         next_lb_index = int(input(f"Player {player}, please select your local board (1-9): ")) - 1
#         next_lb = board.local_boards[next_lb_index]
#         if next_lb.focus:
#             print(f"The {get_lb_name(next_lb.index)} board is in focus.")
#             next_row = int(input(f"Player {player}, please enter the row (1-3): ")) - 1
#             next_col = int(input(f"Player {player}, please enter the column (1-3): ")) - 1
#
#             if next_lb.board[next_row][next_col] == 0:
#                 return next_lb, next_row, next_col
#             else:
#                 print("That space has already been played.")
#         else:
#             print(f"The {get_lb_name(next_lb.index)} board is not playable.")


def update_focus(old_row, old_col):
    """Use the previous move to set the focus of the local boards for the next turn"""

    # Local board in the same position as the previous guess. May or may not be playable
    next_lb = global_board.local_boards[old_row * 3 + old_col]

    # if the board is playable, set focus to True, and all others to False
    if next_lb.playable:
        for local_board in global_board.local_boards:
            local_board.focus = False
        next_lb.focus = True
    # if the board is not playable, set all playable boards in focus, and all non-playable boards out of focus
    else:
        for local_board in global_board.local_boards:
            local_board.focus = local_board.playable


def make_move(local_board, row_pos, col_pos):
    """Takes a local board and the coordinates of a space on the board, and marks the space for the current player"""

    global player, game_over

    local_board.board[row_pos][col_pos] = player  # set space to player

    # Check if this move determines the outcome of the local board (win, lose, draw)
    if local_board.has_tic_tac_toe(player):
        # if local board has been won, set playable to False, then mark the global board
        local_board.playable = False
        global_board.mark_global_board(local_board, player)

        # Now check if this determines the outcome of the global board. If so, the game is over
        if global_board.has_tic_tac_toe(player):
            game_over = True
        elif global_board.is_full():
            game_over = True
            player = 0

    # if the local board is a draw
    elif local_board.is_full():
        local_board.playable = False
        global_board.mark_global_board(local_board, -1)

        if global_board.is_full():
            game_over = True

    # update the focus of the local boards for the next turn
    update_focus(row_pos, col_pos)

    # global_board.print_board()  # Command Line
    draw_board()  # GUI

    # switch player 1 <-> 2
    if not game_over:
        player = (player % 2) + 1

    update_text()


def main():
    """The main game loop. Initializes the global variables, then plays one game of ultimate tic tac toe"""
    global reset

    init_variables()

    # Game loop
    while not game_over:
        # Bot turn
        if player == bot:
            if bot_alg == 'Very Easy':
                lb, row, col = minimax.bot_turn(global_board, bot)  # get the bot's move
            make_move(lb, row, col)  # record the move and update the GUI
        else:
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()

                # New Game Button
                if newgamebutton.is_button_event(event, mouse):
                    newgamebutton.draw(screen)
                    if event.type == pygame.MOUSEBUTTONUP:
                        reset = True
                        return

                # Show Rules Button
                elif rulesbutton.is_button_event(event, mouse):
                    rulesbutton.draw(screen)
                    if event.type == pygame.MOUSEBUTTONUP:
                        rules.show_rules(screen)
                        draw_board()
                        rulesbutton.mode = 'normal'
                        draw_menu()
                        pygame.display.flip()

                # Quit Button
                elif quitbutton.is_button_event(event, mouse):  # Custom quit button
                    quitbutton.draw(screen)
                    if event.type == pygame.MOUSEBUTTONUP:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.QUIT:  # Standard quit button
                    pygame.quit()
                    sys.exit()

                elif alg_options.is_event(event, mouse, screen) or order_options.is_event(event, mouse, screen):
                    pass

                # Human Turn
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Get lb, and row and col coordinates from get_inputs(). Check if lb is None
                    lb, row, col = get_inputs()
                    if lb is not None:
                        # Check if selected space has already been played
                        if lb.focus and lb.board[row][col] == 0:
                            make_move(lb, row, col)

                # If the mouse has been moved and is within the global board, draw a trail that displays an X or O
                # depending on the turn
                elif event.type == pygame.MOUSEMOTION and mouse[0] < GLOBALBOARDSIZE - int(1.1 * DIFF):
                    # draw an 'X' or 'O' where the mouse is pointed
                    if player == 1:
                        draw_x(mouse, screen)
                    else:
                        pygame.draw.circle(screen, RED, mouse, DIFF, 4)

                    # after the display is updated, redraw the board so that the 'X' or 'O' will disappear the next
                    # time the display is updated
                    mousebox = pygame.Rect(mouse[0] - (DIFF // 2), mouse[1] - (DIFF // 2), DIFF,
                                           DIFF)
                    pygame.display.update(mousebox)
                    draw_board(False)


def keep_alive():
    """Keep the screen up after the game ends until the user quits or resets"""
    global reset
    while not reset:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()

            # New Game Button
            if newgamebutton.is_button_event(event, mouse):
                newgamebutton.draw(screen)
                if event.type == pygame.MOUSEBUTTONUP:
                    reset = True
                    return

            # Show Rules Button
            elif rulesbutton.is_button_event(event, mouse):
                rulesbutton.draw(screen)
                if event.type == pygame.MOUSEBUTTONUP:
                    rules.show_rules(screen)
                    draw_board()
                    rulesbutton.mode = 'normal'
                    draw_menu()
                    pygame.display.flip()

            # Quit Button
            elif quitbutton.is_button_event(event, mouse):
                quitbutton.draw(screen)
                if event.type == pygame.MOUSEBUTTONUP:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif alg_options.is_event(event, mouse, screen) or order_options.is_event(event, mouse, screen):
                pass


if __name__ == '__main__':
    """After main(), the program will be stuck in keep_alive() until the game is reset or quit. If the user quits,
    sys.exit() is called and the program will quit. If the user resets, the program will simply exit keep_alive(), and
    the loop will start over."""
    while True:
        main()
        keep_alive()
