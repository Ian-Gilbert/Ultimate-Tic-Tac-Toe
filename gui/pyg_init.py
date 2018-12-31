import pygame


"""Initializes PyGame dimensions and constants"""

# Board Dimensions
SQUARESIZE = 64  # size of each square
WHITESPACE = 64  # space in between local boards
BOARDERSIZE = WHITESPACE // 2  # boarder between edge of screen and local boards
LOCALBOARDSIZE = SQUARESIZE * 3  # total size of each local board
GLOBALBOARDSIZE = SQUARESIZE * 9 + WHITESPACE * 3  # width of the global board, not including the menu
MENUWIDTH = LOCALBOARDSIZE + 2 * BOARDERSIZE  # the width of the menu area
DIFF = int(SQUARESIZE * 0.4)  # determines size of the 'X's and 'O's. Must be less than half of SQUARESIZE

# Color Definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

LIGHT_GRAY = (200, 200, 200)
MEDIUM_GRAY = (150, 150, 150)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

LIGHT_RED = (255, 150, 150)
MEDIUM_RED = (225, 50, 50)
RED = (200, 0, 0)

LIGHT_GREEN = (150, 255, 150)
MEDIUM_GREEN = (50, 225, 50)
GREEN = (0, 200, 0)

LIGHT_BLUE = (150, 150, 255)
MEDIUM_BLUE = (50, 50, 225)
BLUE = (0, 0, 200)

# Color Families:
GRAY_FAMILY = [MEDIUM_GRAY, GRAY]
RED_FAMILY = [MEDIUM_RED, RED]
GREEN_FAMILY = [MEDIUM_GREEN, GREEN]
BLUE_FAMILY = [MEDIUM_BLUE, BLUE]


# Screen Dimensions
SCREENWIDTH = GLOBALBOARDSIZE + MENUWIDTH
SCREENHEIGHT = GLOBALBOARDSIZE

GLOBALBOARDAREA = pygame.Rect(0, 0, GLOBALBOARDSIZE, GLOBALBOARDSIZE)
MENUAREA = pygame.Rect(GLOBALBOARDSIZE, 0, MENUWIDTH, SCREENHEIGHT)

# Font for the game
pygame.font.init()
FONT = pygame.font.Font('freesansbold.ttf', 16)


def draw_x(center, surface):
    """Draws a blue 'X' in the GUI centered at the given point"""
    # Draws a blue 'X' given the center crossing point of the 'X'
    pygame.draw.line(surface, BLUE, center, (center[0] + DIFF, center[1] + DIFF), 5)
    pygame.draw.line(surface, BLUE, center, (center[0] - DIFF, center[1] + DIFF), 5)
    pygame.draw.line(surface, BLUE, center, (center[0] + DIFF, center[1] - DIFF), 5)
    pygame.draw.line(surface, BLUE, center, (center[0] - DIFF, center[1] - DIFF), 5)
