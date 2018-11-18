import pygame
import sys
import boardclasses


def draw_x(center):
    # Draws a blue 'X' given the center crossing point of the 'X'
    pygame.draw.line(screen, BLUE, center, (center[0] + DIFF, center[1] + DIFF), 5)
    pygame.draw.line(screen, BLUE, center, (center[0] - DIFF, center[1] + DIFF), 5)
    pygame.draw.line(screen, BLUE, center, (center[0] + DIFF, center[1] - DIFF), 5)
    pygame.draw.line(screen, BLUE, center, (center[0] - DIFF, center[1] - DIFF), 5)


def draw_board():
    """Displays the full global and local boards in the GUI"""
    screen.fill(LIGHT_GRAY)

    # For each local board
    for outer_x in range(3):
        for outer_y in range(3):
            # Get the current local board
            index = outer_y * 3 + outer_x
            local_board = board.local_boards[index]

            # Top left coordinate of the current local board
            board_origin_x = BOARDERSIZE + ((LOCALBOARDSIZE + WHITESPACE) * outer_x)
            board_origin_y = BOARDERSIZE + ((LOCALBOARDSIZE + WHITESPACE) * outer_y)

            # Color the board accordingly if it is won by X or O, or if it is in focus
            if local_board.focus and not game_over:  # if the game is over, nothing is in focus
                pygame.draw.rect(screen, WHITE, (board_origin_x, board_origin_y, LOCALBOARDSIZE, LOCALBOARDSIZE))
            elif board.board[outer_y][outer_x] == 1:
                pygame.draw.rect(screen, LIGHT_BLUE, (board_origin_x, board_origin_y, LOCALBOARDSIZE, LOCALBOARDSIZE))
            elif board.board[outer_y][outer_x] == 2:
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
                        draw_x(center)
                    elif local_board.board[inner_y][inner_x] == 2:
                        pygame.draw.circle(screen, RED, center, DIFF, 4)


# def get_lb_name(key):
#     # Returns the physical location of the local board given lb_index as a key (for the command line)
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
#     return switcher.get(key)


def get_inputs():
    """Gets the current position of the mouse and returns the local board index and row and column coordinates of the
    square that the mouse is currently in. If the mouse is not in a square, then index will return None."""

    x_pos, y_pos = pygame.mouse.get_pos()  # current x and y coordinates of the mouse
    index = None  # default value for index

    # For each local board
    for x in range(3):
        for y in range(3):
            # Top left coordinate of the current local board
            board_origin_x = BOARDERSIZE + ((LOCALBOARDSIZE + WHITESPACE) * x)
            board_origin_y = BOARDERSIZE + ((LOCALBOARDSIZE + WHITESPACE) * y)

            # If the mouse is over one of the boards, set index accordingly
            if board_origin_x < x_pos < board_origin_x + LOCALBOARDSIZE and \
                    board_origin_y < y_pos < board_origin_y + LOCALBOARDSIZE:
                index = y * 3 + x
                break
        # How to break out of nested for loops in python:
        else:  # if the inner loop does not break, continue
            continue
        break  # if the inner loop does break, then break out of the outer loop too

    # row and col will be nonsense if the mouse is not over a board. Need to ensure index is not None before using
    row_pos = (y_pos - board_origin_y) // SQUARESIZE
    col_pos = (x_pos - board_origin_x) // SQUARESIZE

    return index, row_pos, col_pos


# def get_next_move():
#     # Request local board and row and col coordinates from the player (for the command line)
#     # DO NOT RUN WHILE USING THE GUI
#     while True:
#         next_lb_index = int(input(f"Player {player}, please select your local board (1-9): ")) - 1
#         next_lb = board.local_boards[next_lb_index]
#         if next_lb.focus:
#             print(f"The {get_lb_name(next_lb_index)} board is in focus.")
#             next_row = int(input(f"Player {player}, please enter the row (1-3): ")) - 1
#             next_col = int(input(f"Player {player}, please enter the column (1-3): ")) - 1
#
#             if next_lb.board[next_row][next_col] == 0:
#                 return next_lb_index, next_lb, next_row, next_col
#             else:
#                 print("That space has already been played.")
#         else:
#             print(f"The {get_lb_name(next_lb_index)} board is not playable.")


def update_focus(old_row, old_col):
    """Use the previous move to set the focus of the local boards for the next turn"""

    # Local board in the same position as the previous guess. May or may not be playable
    next_lb_index = (old_row * 3) + old_col
    next_lb = board.local_boards[next_lb_index]

    # if the board is playable, set focus to True, and all others to False
    if next_lb.playable:
        for local_board in board.local_boards:
            local_board.focus = False
        next_lb.focus = True
    # if the board is not playable, set all playable boards in focus, and all non-playable boards out of focus
    else:
        for local_board in board.local_boards:
            local_board.focus = local_board.playable


# Global board
board = boardclasses.GlobalBoard()
board.print_board()  # command line

player = 1  # player will always be 1 or 2. 1 -> 'X' and 2 -> 'O'
winner = 0  # record the winner so it can be displayed

game_over = False  # break out of the game loop when the game ends


"""PyGame Initialization"""
pygame.init()

# Board Dimensions
SQUARESIZE = 65  # size of each square
WHITESPACE = 65  # space in between local boards
BOARDERSIZE = 32  # boarder between edge of screen and local boards
LOCALBOARDSIZE = SQUARESIZE * 3  # total size of each local board
DIFF = 25  # determines size of the 'X's and 'O's. Must be less than half of SQUARESIZE

# Color Definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 0, 200)
LIGHT_BLUE = (150, 150, 255)
RED = (200, 0, 0)
LIGHT_RED = (255, 150, 150)

# Screen Dimensions
width = SQUARESIZE * 9 + WHITESPACE * 3
height = SQUARESIZE * 9 + WHITESPACE * 3

size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Ultimate Tic Tac Toe")

draw_board()  # GUI
pygame.display.update()
"""End PyGame Initialization"""

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:

            # get the board index, and row and col coordinates from get_inputs(). Check if lb_index is None
            lb_index, row, col = get_inputs()
            if lb_index is not None:
                lb = board.local_boards[lb_index]

                # Check if selected space has already been played
                if lb.focus and lb.board[row][col] == 0:
                    lb.board[row][col] = player  # set space to player

                    # Check if this move determines the outcome of the local board (win, lose, draw)
                    if lb.has_tic_tac_toe():
                        # if local board has been won, set playable to False, then mark the global board
                        lb.playable = False
                        board.mark_board(lb_index, player)

                        # Now check if this determines the outcome of the global board. If so, the game is over
                        if board.has_tic_tac_toe():
                            winner = player
                            game_over = True
                        elif board.is_full():
                            game_over = True

                    # if the local board is a draw
                    elif lb.is_full():
                        lb.playable = False

                    # update the focus of the local boards for the next turn
                    update_focus(row, col)

                    board.print_board()  # Command Line
                    draw_board()  # GUI
                    pygame.display.update()

                    # switch player 1 <-> 2
                    player = (player % 2) + 1

        # if the mouse has not been clicked, draw a trail that shows whose turn it is
        else:
            mouse = pygame.mouse.get_pos()

            # draw an 'X' or 'O' where the mouse is pointed
            if player == 1:
                draw_x(mouse)
            else:
                pygame.draw.circle(screen, RED, mouse, DIFF, 4)

            # after the display is updated, redraw the board so that the 'X' or 'O' will disappear the next time the
            # display is updated
            pygame.display.update()
            draw_board()

# Display the game result
if winner == 0:
    print("\nThe game is a draw.")
else:
    print(f"\nPlayer {winner} has won!")

# Keep the screen up after the game ends until the user quits
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
