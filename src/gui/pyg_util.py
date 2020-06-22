from typing import List  # also Tuple from src.gui.pyg_init
from gui.pyg_init import *
import sys


class Button:

    def __init__(self, pos: Tuple[int, int], text: str, width: int = LOCALBOARDSIZE, height: int = SQUARESIZE,
                 colorfamily: ColorFamily = GRAY_FAMILY, textcolor: RGBColor = BLACK) -> None:
        """
        :param pos: specifies the top left corner of the button (top, left)
        :param text: text to be displayed on the button
        :param colorfamily: specifies a light and regular color for when the button is clicked or highlighted (or not)
        :param textcolor: color of the text
        """
        # available button modes
        self.NORMAL = 0
        self.PRESSED = 1
        self.HOVER = 2

        self.rect: pygame.Rect = pygame.Rect(pos[0], pos[1], width, height)
        self.text: str = text
        self.colorfamily: ColorFamily = colorfamily
        self.textcolor: RGBColor = textcolor
        self.mode: int = self.NORMAL

        # create the surfaces for a text button
        self.normal_surface: pygame.Surface = pygame.Surface(self.rect.size)
        self.pressed_surface: pygame.Surface = pygame.Surface(self.rect.size)
        self.hover_surface: pygame.Surface = pygame.Surface(self.rect.size)
        self.update()  # draw the initial button images

    def update(self) -> None:
        w = self.rect.width  # syntactic sugar
        h = self.rect.height  # syntactic sugar

        # fill background color for all buttons
        self.normal_surface.fill(self.colorfamily[1])
        self.pressed_surface.fill(self.colorfamily[0])
        self.hover_surface.fill(self.colorfamily[0])

        # draw caption text for all buttons
        caption_surface = FONT.render(self.text, True, self.textcolor)
        caption_rect = caption_surface.get_rect()
        caption_rect.center = w // 2, h // 2
        self.normal_surface.blit(caption_surface, caption_rect)
        self.pressed_surface.blit(caption_surface, caption_rect)
        self.hover_surface.blit(caption_surface, caption_rect)

        # draw border for normal button
        pygame.draw.rect(self.normal_surface, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.line(self.normal_surface, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.normal_surface, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.normal_surface, DARK_GRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self.normal_surface, DARK_GRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self.normal_surface, GRAY, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(self.normal_surface, GRAY, (w - 2, 2), (w - 2, h - 2))

        # draw border for down button
        pygame.draw.rect(self.pressed_surface, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.line(self.pressed_surface, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.pressed_surface, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.pressed_surface, DARK_GRAY, (1, h - 2), (1, 1))
        pygame.draw.line(self.pressed_surface, DARK_GRAY, (1, 1), (w - 2, 1))
        pygame.draw.line(self.pressed_surface, GRAY, (2, h - 3), (2, 2))
        pygame.draw.line(self.pressed_surface, GRAY, (2, 2), (w - 3, 2))

        # draw border for highlight button
        pygame.draw.rect(self.hover_surface, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.line(self.hover_surface, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.hover_surface, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.hover_surface, DARK_GRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self.hover_surface, DARK_GRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self.hover_surface, GRAY, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(self.hover_surface, GRAY, (w - 2, 2), (w - 2, h - 2))

    def draw(self, surface: pygame.Surface, update: bool = True) -> None:
        if self.mode == self.NORMAL:
            surface.blit(self.normal_surface, self.rect)
        elif self.mode == self.PRESSED:
            surface.blit(self.pressed_surface, self.rect)
        elif self.mode == self.HOVER:
            surface.blit(self.hover_surface, self.rect)

        if update:
            pygame.display.update(self.rect)

    def is_button_event(self, event: pygame.event, mouse: Tuple[int, int]) -> bool:
        if self.rect.collidepoint(mouse[0], mouse[1]):
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and self.mode != self.HOVER:
                self.mode = self.HOVER
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN and self.mode != self.PRESSED:
                self.mode = self.PRESSED
                return True
        elif self.mode != self.NORMAL:
            self.mode = self.NORMAL
            return True
        return False


"""******************************************************************************************************************"""


class GameOptionButton(Button):
    """Each option in the GameOptions menu. Extends Button class"""

    def __init__(self, pos: Tuple[int, int], text: str) -> None:
        Button.__init__(self, pos, text, width=int(.45 * LOCALBOARDSIZE), height=int(.75 * SQUARESIZE))
        self.selected: bool = False

        # Add selected surface
        self.selected_surface: pygame.Surface = pygame.Surface(self.rect.size)
        self.update_surfaces()

    def update_surfaces(self) -> None:
        """Extends the update() method from the Button class"""
        # update regular surfaces
        self.update()

        # update selected_surface
        self.selected_surface.fill(MEDIUM_BLUE)

        w = self.rect.width  # syntactic sugar
        h = self.rect.height  # syntactic sugar

        # render font on selected_surface
        caption_surface = FONT.render(self.text, True, LIGHT_GRAY)
        caption_rect = caption_surface.get_rect()
        caption_rect.center = w // 2, h // 2
        self.selected_surface.blit(caption_surface, caption_rect)

        # draw border around selected_surface
        pygame.draw.rect(self.selected_surface, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.line(self.selected_surface, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.selected_surface, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.selected_surface, DARK_GRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self.selected_surface, DARK_GRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self.selected_surface, GRAY, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(self.selected_surface, GRAY, (w - 2, 2), (w - 2, h - 2))

    def draw_option(self, surface: pygame.Surface, update: bool = True) -> None:
        """Extends the draw() method from the Button class"""
        # If the button is selected, draw the blue "selected surface"
        if self.selected:
            surface.blit(self.selected_surface, self.rect)
        # Otherwise use the button draw method, which checks if the button is highlighted and stuff
        else:
            self.draw(surface, update=False)

        if update:
            pygame.display.update(self.rect)


class GameOptions:
    """Kind of like a drop down menu that's always down, cause I'm too lazy to make an actual drop down menu. User
    selects one of the options, which sets the mode. When a new game is started, the mode will determine the game setup,
    i.e. 2-player vs AI difficulty, or determining who goes first."""

    def __init__(self, pos: Tuple[int, int], default: str, *options: str) -> None:
        """
        :param pos: position of the first button
        :param default: button selected by default
        :param options: the text to be displayed on each button (also the mode that the button will dictate)
        """
        self.rect: pygame.Rect = pygame.Rect(pos, (int(.45 * LOCALBOARDSIZE), int(.75 * SQUARESIZE)))
        self.current_option: GameOptionButton
        self.options: List[GameOptionButton] = []
        for i in range(len(options)):
            left = pos[0]
            top = pos[1] + (i * .75 * SQUARESIZE)
            self.options.append(GameOptionButton((left, top), options[i]))
            if options[i] == default:
                self.current_option = self.options[i]
                self.current_option.selected = True

    def is_event(self, event: pygame.event, mouse: Tuple[int, int], surface: pygame.Surface) -> bool:
        """Kind of extends the is_button_event() method from the Button class"""
        for button in self.options:
            if button.is_button_event(event, mouse):
                if event.type == pygame.MOUSEBUTTONUP and not button.selected:
                    self.current_option.selected = False
                    self.current_option.draw_option(surface)

                    button.selected = True
                    self.current_option = button
                button.draw_option(surface)
                return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """Draws each button"""
        for button in self.options:
            button.draw_option(surface, False)

    def get_option(self) -> str:
        """Returns the text of the selected option"""
        return self.current_option.text


"""******************************************************************************************************************"""


class TextArea:
    """White area that can print two lines of text. Used for printing the turn/winner"""

    def __init__(self) -> None:
        # Overall area of the textarea
        self.rect: pygame.Rect = pygame.Rect(GLOBALBOARDSIZE + BOARDERSIZE, BOARDERSIZE + int(0.25 * SQUARESIZE),
                                             LOCALBOARDSIZE, SQUARESIZE)

        # Top half of the textarea
        self.top_rect: pygame.Rect = pygame.Rect(GLOBALBOARDSIZE + BOARDERSIZE, BOARDERSIZE + int(0.25 * SQUARESIZE),
                                                 LOCALBOARDSIZE, SQUARESIZE // 2)
        self.top_surface: pygame.Surface = pygame.Surface(self.top_rect.size)

        # Bottom half of the textarea
        self.bot_rect: pygame.Rect = pygame.Rect(GLOBALBOARDSIZE + BOARDERSIZE,
                                                 BOARDERSIZE + (SQUARESIZE // 4) + (SQUARESIZE // 2),
                                                 LOCALBOARDSIZE, SQUARESIZE // 2)
        self.bot_surface: pygame.Surface = pygame.Surface(self.bot_rect.size)

    def set_text(self, top_text: str, bot_text: str, surface: pygame.Surface, color: RGBColor = BLACK) -> None:
        self.top_surface.fill(WHITE)
        self.bot_surface.fill(WHITE)

        # Render the top text
        top_text_surface = FONT.render(top_text, True, color)
        top_text_rect = top_text_surface.get_rect()
        top_text_rect.center = self.top_rect.width // 2, self.top_rect.height // 2
        self.top_surface.blit(top_text_surface, top_text_rect)
        surface.blit(self.top_surface, self.top_rect)

        # Render the bottom text
        bot_text_surface = FONT.render(bot_text, True, color)
        bot_text_rect = bot_text_surface.get_rect()
        bot_text_rect.center = self.bot_rect.width // 2, self.bot_rect.height // 2
        self.bot_surface.blit(bot_text_surface, bot_text_rect)
        surface.blit(self.bot_surface, self.bot_rect)

        pygame.display.update(self.rect)


"""******************************************************************************************************************"""


class RulesScreen:
    """Prints the rules of the game on the screen"""

    def __init__(self) -> None:
        self.offset: Tuple[int, int] = (SQUARESIZE, SQUARESIZE)  # offset from the main screen
        self.rect: pygame.Rect = pygame.Rect(self.offset[0], self.offset[1], GLOBALBOARDSIZE - 2 * SQUARESIZE,
                                             GLOBALBOARDSIZE - 2 * SQUARESIZE)
        self.surface: pygame.Surface = pygame.Surface(self.rect.size)
        self.ok_button: Button = Button((self.rect.centerx - (LOCALBOARDSIZE // 2) - self.offset[0],
                                         GLOBALBOARDSIZE - int(2.5 * SQUARESIZE) - self.offset[1]), 'OK')

        # Get the rules from rules.txt, and save each line in a list. File must end with a newline
        with open("gui/rules.txt", 'r') as file:
            self.lines_of_text: List[str] = file.readlines()

        self.write_rules()  # draw each line on the surface
        self.ok_button.draw(self.surface, False)

    def write_rules(self) -> None:
        for i in range(len(self.lines_of_text)):
            line = self.lines_of_text[i]
            text_surface = FONT.render('> ' + line[:-1], True, GREEN)  # get rid of the newline character
            text_rect = text_surface.get_rect()
            text_rect.topleft = (8, 8 + 24 * i)  # placement of each line on the surface
            self.surface.blit(text_surface, text_rect)

    def show_rules(self, screen: pygame.display) -> None:
        # Put the rules on the main screen
        screen.blit(self.surface, self.rect)
        pygame.display.update(self.rect)

        # Wait for the user to press OK or quit the game
        while True:
            for event in pygame.event.get():
                # Subtract the offset from the mouse position
                mouse = pygame.mouse.get_pos()
                mouse = (mouse[0] - self.offset[0], mouse[1] - self.offset[1])

                # OK button
                if self.ok_button.is_button_event(event, mouse):
                    self.ok_button.draw(self.surface, False)
                    screen.blit(self.surface, self.rect)
                    pygame.display.update(self.ok_button.rect)
                    if event.type == pygame.MOUSEBUTTONUP:
                        return

                # User quits the game
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
