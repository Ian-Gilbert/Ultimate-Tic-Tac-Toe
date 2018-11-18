import pygame
import sys
import boardclasses


def draw_x(center):
    pygame.draw.line(screen, BLUE, center, (center[0] + DIFF, center[1] + DIFF), 5)
    pygame.draw.line(screen, BLUE, center, (center[0] - DIFF, center[1] + DIFF), 5)
    pygame.draw.line(screen, BLUE, center, (center[0] + DIFF, center[1] - DIFF), 5)
    pygame.draw.line(screen, BLUE, center, (center[0] - DIFF, center[1] - DIFF), 5)


def draw_board():
    screen.fill(LIGHT_GRAY)

    # Draw the grid lines
    for outer_x in range(3):
        for outer_y in range(3):
            index = outer_y * 3 + outer_x
            local_board = board.local_boards[index]

            board_origin_x = (WHITESPACE // 2) + ((LOCALBOARDSIZE + WHITESPACE) * outer_x)
            board_origin_y = (WHITESPACE // 2) + ((LOCALBOARDSIZE + WHITESPACE) * outer_y)

            if local_board.focus and not game_over:
                pygame.draw.rect(screen, WHITE, (board_origin_x, board_origin_y, LOCALBOARDSIZE, LOCALBOARDSIZE))
            elif board.board[outer_y][outer_x] == 1:
                pygame.draw.rect(screen, LIGHT_BLUE, (board_origin_x, board_origin_y, LOCALBOARDSIZE, LOCALBOARDSIZE))
            elif board.board[outer_y][outer_x] == 2:
                pygame.draw.rect(screen, LIGHT_RED, (board_origin_x, board_origin_y, LOCALBOARDSIZE, LOCALBOARDSIZE))

            for inner_x in range(3):
                for inner_y in range(3):
                    center_x = board_origin_x + (SQUARESIZE * inner_x) + SQUARESIZE // 2
                    center_y = board_origin_y + (SQUARESIZE * inner_y) + SQUARESIZE // 2
                    center = (center_x, center_y)

                    if local_board.board[inner_y][inner_x] == 1:
                        draw_x(center)
                    elif local_board.board[inner_y][inner_x] == 2:
                        pygame.draw.circle(screen, RED, center, DIFF, 4)

            for i in range(4):
                # Vertical Grid Lines
                start_x = board_origin_x + (SQUARESIZE * i)
                start_y = board_origin_y
                pygame.draw.line(screen, BLACK, (start_x, start_y), (start_x, start_y + LOCALBOARDSIZE))

                # Horizontal Grid Lines
                start_x = board_origin_x
                start_y = board_origin_y + (SQUARESIZE * i)
                pygame.draw.line(screen, BLACK, (start_x, start_y), (start_x + LOCALBOARDSIZE, start_y))


# def get_lb_name(key):
#     # Returns the name of the local board given lb_index as a key
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
    x_pos, y_pos = pygame.mouse.get_pos()
    index = None
    for x in range(3):
        for y in range(3):
            board_origin_x = (WHITESPACE // 2) + ((LOCALBOARDSIZE + WHITESPACE) * x)
            board_origin_y = (WHITESPACE // 2) + ((LOCALBOARDSIZE + WHITESPACE) * y)
            if board_origin_x < x_pos < board_origin_x + LOCALBOARDSIZE and \
                    board_origin_y < y_pos < board_origin_y + LOCALBOARDSIZE:
                index = y * 3 + x
                break
        else:
            continue
        break

    row_pos = (y_pos - board_origin_y) // SQUARESIZE
    col_pos = (x_pos - board_origin_x) // SQUARESIZE

    return index, row_pos, col_pos


# def get_next_move():
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
    next_lb_index = (old_row * 3) + old_col
    next_lb = board.local_boards[next_lb_index]

    if next_lb.playable:
        for local_board in board.local_boards:
            local_board.focus = False
        next_lb.focus = True
    else:
        for local_board in board.local_boards:
            local_board.focus = local_board.playable


board = boardclasses.GlobalBoard()
board.print_board()
player = 1
winner = 0

game_over = False


"""PyGame Initialization"""
pygame.init()

# Board Dimensions
SQUARESIZE = 65
WHITESPACE = 65
LOCALBOARDSIZE = SQUARESIZE * 3
DIFF = 25

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

draw_board()
pygame.display.update()
"""End PyGame Initialization"""

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            try:
                lb_index, row, col = get_inputs()
                lb = board.local_boards[lb_index]
            except TypeError:
                pass
            else:
                if lb.focus and lb.board[row][col] == 0:
                    lb.board[row][col] = player

                    if lb.has_tic_tac_toe():
                        lb.playable = False
                        board.mark_board(lb_index, player)
                        if board.has_tic_tac_toe():
                            winner = player
                            game_over = True
                        elif board.is_full():

                            game_over = True
                    elif lb.is_full():
                        lb.playable = False

                    update_focus(row, col)

                    board.print_board()  # Command Line
                    draw_board()  # GUI
                    pygame.display.update()

                    player = (player % 2) + 1
        else:
            mouse = pygame.mouse.get_pos()
            if player == 1:
                draw_x(mouse)
            else:
                pygame.draw.circle(screen, RED, mouse, DIFF, 4)

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
