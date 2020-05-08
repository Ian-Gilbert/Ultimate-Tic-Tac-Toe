from typing import Optional  # also Tuple from src.gui.pyg_init
import random as rand
import sys
from src.boardclasses import GlobalBoard, LocalBoard
from src import minimax
from src.gui.pyg_init import *  # contains pygame import
from src.gui import pyg_util


"""Game Setup Constants"""

# Opponent setting
TWO_PLAYER = "2 Player"
BEGINNER = "Beginner"
MCTS = "MCTS"
FOO1 = "Foo 1"
FOO2 = "Foo 2"
FOO3 = "Foo 3"

# Turn order
RANDOM_ORDER = "Random"
PLAYER_FIRST = "First"
PLAYER_SECOND = "Second"


"""PyGame Initialization"""
pygame.init()

# Define the main screen
screen: pygame.display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Ultimate Tic Tac Toe")

rules = pyg_util.RulesScreen()

# menu items
textarea = pyg_util.TextArea()  # Displays who's turn it is and game outcome

rulesbutton = pyg_util.Button(  # Show game rules
    (GLOBALBOARDSIZE + BOARDERSIZE, BOARDERSIZE + int(1.75 * SQUARESIZE)),
    'Show Rules',
    colorfamily=BLUE_FAMILY,
    textcolor=LIGHT_GRAY
)

newgamebutton = pyg_util.Button(  # Start new game
    (GLOBALBOARDSIZE + BOARDERSIZE, SCREENHEIGHT - BOARDERSIZE - int(2.75 * SQUARESIZE)),
    'New Game',
    colorfamily=GREEN_FAMILY
)

quitbutton = pyg_util.Button(  # Quit game
    (GLOBALBOARDSIZE + BOARDERSIZE, SCREENHEIGHT - BOARDERSIZE - int(1.25 * SQUARESIZE)),
    'Quit Game',
    colorfamily=RED_FAMILY
)

alg_options = pyg_util.GameOptions(  # Opponent settings
    (GLOBALBOARDSIZE + BOARDERSIZE, LOCALBOARDSIZE + WHITESPACE),
    BEGINNER,  # default value
    TWO_PLAYER,
    BEGINNER,
    FOO1,
    FOO2,
    FOO3
)

order_options = pyg_util.GameOptions(  # Turn order settings
    (GLOBALBOARDSIZE + BOARDERSIZE + int(0.55 * LOCALBOARDSIZE), LOCALBOARDSIZE + WHITESPACE),
    RANDOM_ORDER,  # default value
    RANDOM_ORDER,
    PLAYER_FIRST,
    PLAYER_SECOND
)

"""End PyGame Initialization"""


class GlobalVariables:
    def __init__(self) -> None:
        self.global_board: GlobalBoard = GlobalBoard()
        self.player: int = 1  # player will always be 1 or 2. 1 -> 'X' and 2 -> 'O'
        self.bot_alg: str = alg_options.get_option()
        order: str = order_options.get_option()
        self.bot: int

        # Decide whether the bot goes first or second
        if self.bot_alg == TWO_PLAYER:
            self.bot = 0
        elif order == RANDOM_ORDER:
            self.bot = rand.randint(1, 2)
        elif order == PLAYER_FIRST:
            self.bot = 2
        elif order == PLAYER_SECOND:
            self.bot = 1

        self.game_over: bool = False  # break out of the game loop when the game ends
        self.reset: bool = False  # after the game, you are stuck in keep_alive() until reset == True


GLOBALS = GlobalVariables()


def draw_menu() -> None:
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


def update_text() -> None:
    """Updates the text displayed on the TextArea"""
    if not GLOBALS.game_over:
        if GLOBALS.bot_alg != 'minimax' or GLOBALS.player != GLOBALS.bot:
            if GLOBALS.player == 1:
                textarea.set_text("Player X:", "Make your move", screen, color=BLUE)
            else:
                textarea.set_text("Player O:", "Make your move", screen, color=RED)
    else:
        if GLOBALS.player == 0:
            textarea.set_text("The game is", "a draw.", screen)
        elif GLOBALS.player == 1:
            textarea.set_text("Player X", "has won!", screen, color=BLUE)
        else:
            textarea.set_text("Player O", "has won!", screen, color=RED)


def draw_board(update: bool = True) -> None:
    """Displays the full global and local boards in the GUI. Does not update the menu."""
    pygame.draw.rect(screen, LIGHT_GRAY, GLOBALBOARDAREA)

    # For each local board
    for outer_x in range(3):
        for outer_y in range(3):
            # Get the current local board
            local_board = GLOBALS.global_board.local_board_list[outer_y * 3 + outer_x]

            # Top left coordinate of the current local board
            board_origin_x = BOARDERSIZE + ((LOCALBOARDSIZE + WHITESPACE) * outer_x)
            board_origin_y = BOARDERSIZE + ((LOCALBOARDSIZE + WHITESPACE) * outer_y)

            # Color the board accordingly if it is won by X or O, or if it is in focus
            if local_board.focus and not GLOBALS.game_over:  # if the game is over, nothing is in focus
                pygame.draw.rect(screen, WHITE, (board_origin_x, board_origin_y, LOCALBOARDSIZE, LOCALBOARDSIZE))
            elif GLOBALS.global_board.board[outer_y][outer_x] == 1:
                pygame.draw.rect(screen, LIGHT_BLUE, (board_origin_x, board_origin_y, LOCALBOARDSIZE, LOCALBOARDSIZE))
            elif GLOBALS.global_board.board[outer_y][outer_x] == 2:
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


def get_inputs(mouse: Tuple[int, int]) -> Optional[Tuple[LocalBoard, int, int]]:
    """Gets the current position of the mouse and returns the local board, as well as row and column coordinates of the
    square that the mouse is currently in. If the mouse is not in a square, then local_board will return None."""

    x_pos, y_pos = mouse  # current x and y coordinates of the mouse

    # For each local board
    for x in range(3):
        for y in range(3):
            # Top left coordinate of the current local board
            board_origin_x = BOARDERSIZE + ((LOCALBOARDSIZE + WHITESPACE) * x)
            board_origin_y = BOARDERSIZE + ((LOCALBOARDSIZE + WHITESPACE) * y)

            # If the mouse is over the current local_board area, return local_board, row, and col
            if 0 < x_pos - board_origin_x < LOCALBOARDSIZE and 0 < y_pos - board_origin_y < LOCALBOARDSIZE:
                local_board = GLOBALS.global_board.local_board_list[y * 3 + x]
                row = (y_pos - board_origin_y) // SQUARESIZE
                col = (x_pos - board_origin_x) // SQUARESIZE
                return local_board, row, col

    # If the mouse was not over a local board, return None
    return None


def make_move(local_board: LocalBoard, row: int, col: int) -> None:
    """Takes a local board and the coordinates of a space on the board, and marks the space for the current player. Then
    checks for global board updates and acts accordingly."""

    local_board.board[row][col] = GLOBALS.player  # set space to player

    # Check if this move determines the outcome of the local board (win, lose, draw)
    if local_board.has_tic_tac_toe(GLOBALS.player):
        # if local board has been won, set playable to False, then mark the global board
        local_board.playable = False
        GLOBALS.global_board.mark_global_board(local_board, GLOBALS.player)

        # Now check if this determines the outcome of the global board. If so, the game is over
        if GLOBALS.global_board.has_tic_tac_toe(GLOBALS.player):
            GLOBALS.game_over = True
        elif GLOBALS.global_board.is_full():
            GLOBALS.game_over = True
            GLOBALS.player = 0

    # if the local board is a draw
    elif local_board.is_full():
        local_board.playable = False
        GLOBALS.global_board.mark_global_board(local_board, -1)

        if GLOBALS.global_board.is_full():
            GLOBALS.game_over = True

    # update the focus of the local boards for the next turn
    GLOBALS.global_board.update_focus(row, col)

    # switch player 1 <-> 2
    if not GLOBALS.game_over:
        GLOBALS.player = (GLOBALS.player % 2) + 1

    # GLOBALS.global_board.print_board()  # Print board to standard out
    draw_board()  # Draw board in GUI
    update_text()


def main() -> None:
    """The main game loop. Initializes the global variables, then plays one game of ultimate tic tac toe"""

    while not GLOBALS.game_over:
        if GLOBALS.player == GLOBALS.bot:  # bot turn
            if GLOBALS.bot_alg == BEGINNER:
                lb, row, col = minimax.bot_turn(GLOBALS.global_board, GLOBALS.bot)  # get the bot's move
            else:
                raise Exception("Undefined bot algorithm")

            make_move(lb, row, col)  # record the move and update the GUI

        else:  # human turn (will always be the case in 2-player mode
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()

                # New Game Button
                if newgamebutton.is_button_event(event, mouse):
                    newgamebutton.draw(screen)
                    if event.type == pygame.MOUSEBUTTONUP:
                        GLOBALS.reset = True
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
                    # is_event handles drawing any affected options itself, so no need to call a draw method here
                    pass

                # Human Turn
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Get lb, and row and col coordinates from get_inputs(). Check if lb is None
                    params = get_inputs(mouse)
                    if params is not None:
                        lb, row, col = params
                        # Check if local board is in focus and if selected space has not yet been played
                        if lb.focus and lb.board[row][col] == 0:
                            make_move(lb, row, col)

                # If the mouse has been moved and is within the global board, draw a trail that displays an X or O
                # depending on the turn
                elif event.type == pygame.MOUSEMOTION and mouse[0] < GLOBALBOARDSIZE - int(1.1 * DIFF):
                    # draw an 'X' or 'O' where the mouse is pointed
                    if GLOBALS.player == 1:
                        draw_x(mouse, screen)
                    else:
                        pygame.draw.circle(screen, RED, mouse, DIFF, 4)

                    # after the display is updated, redraw the board so that the 'X' or 'O' will disappear the next
                    # time the display is updated
                    mousebox = pygame.Rect(mouse[0] - (DIFF // 2), mouse[1] - (DIFF // 2), DIFF,
                                           DIFF)
                    pygame.display.update(mousebox)
                    draw_board(False)


def keep_alive() -> None:
    """Keep the screen up after the game ends until the user quits or resets"""
    # global reset
    while not GLOBALS.reset:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()

            # New Game Button
            if newgamebutton.is_button_event(event, mouse):
                newgamebutton.draw(screen)
                if event.type == pygame.MOUSEBUTTONUP:
                    GLOBALS.reset = True
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
        # GLOBALS.global_board.print_board()  # command line
        draw_board(update=False)  # GUI
        draw_menu()  # GUI
        pygame.display.flip()

        main()
        keep_alive()
        GLOBALS = GlobalVariables()
