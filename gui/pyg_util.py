from gui.pyg_init import *
import sys


class Button:
    def __init__(self, pos, text, width=LOCALBOARDSIZE, height=SQUARESIZE, colorfamily=GRAY_FAMILY, textcolor=BLACK):
        """
        :param pos: specifies the top left corner of the button (top, left)
        :param text: text to be displayed on the button
        :param colorfamily: specifies a light and regular color for when the button is clicked or highlighted (or not)
        :param textcolor: color of the text
        """
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.text = text
        self.colorfamily = colorfamily
        self.textcolor = textcolor
        self.mode = 'normal'

        # create the surfaces for a text button
        self.normal_surface = pygame.Surface(self.rect.size)
        self.down_surface = pygame.Surface(self.rect.size)
        self.highlight_surface = pygame.Surface(self.rect.size)
        self.update()  # draw the initial button images

    def update(self):
        w = self.rect.width  # syntactic sugar
        h = self.rect.height  # syntactic sugar

        # fill background color for all buttons
        self.normal_surface.fill(self.colorfamily[1])
        self.down_surface.fill(self.colorfamily[0])
        self.highlight_surface.fill(self.colorfamily[0])

        # draw caption text for all buttons
        caption_surface = FONT.render(self.text, True, self.textcolor)
        caption_rect = caption_surface.get_rect()
        caption_rect.center = w // 2, h // 2
        self.normal_surface.blit(caption_surface, caption_rect)
        self.down_surface.blit(caption_surface, caption_rect)
        self.highlight_surface.blit(caption_surface, caption_rect)

        # draw border for normal button
        pygame.draw.rect(self.normal_surface, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.line(self.normal_surface, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.normal_surface, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.normal_surface, DARK_GRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self.normal_surface, DARK_GRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self.normal_surface, GRAY, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(self.normal_surface, GRAY, (w - 2, 2), (w - 2, h - 2))

        # draw border for down button
        pygame.draw.rect(self.down_surface, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.line(self.down_surface, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.down_surface, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.down_surface, DARK_GRAY, (1, h - 2), (1, 1))
        pygame.draw.line(self.down_surface, DARK_GRAY, (1, 1), (w - 2, 1))
        pygame.draw.line(self.down_surface, GRAY, (2, h - 3), (2, 2))
        pygame.draw.line(self.down_surface, GRAY, (2, 2), (w - 3, 2))

        # draw border for highlight button
        pygame.draw.rect(self.highlight_surface, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.line(self.highlight_surface, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.highlight_surface, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.highlight_surface, DARK_GRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self.highlight_surface, DARK_GRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self.highlight_surface, GRAY, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(self.highlight_surface, GRAY, (w - 2, 2), (w - 2, h - 2))

    def draw(self, surface, update=True):
        if self.mode == 'normal':
            surface.blit(self.normal_surface, self.rect)
        elif self.mode == 'highlight':
            surface.blit(self.highlight_surface, self.rect)
        elif self.mode == 'down':
            surface.blit(self.down_surface, self.rect)

        if update:
            pygame.display.update(self.rect)

    def is_button_event(self, event, mouse):
        if self.rect.collidepoint(mouse[0], mouse[1]):
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and self.mode != 'highlight':
                self.mode = 'highlight'
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN and self.mode != 'down':
                self.mode = 'down'
                return True
        elif self.mode != 'normal':
            self.mode = 'normal'
            return True
        return False


"""******************************************************************************************************************"""


class GameOptionButton(Button):
    """Each option in the GameOptions menu"""

    def __init__(self, pos, text):
        Button.__init__(self, pos, text, width=int(.45 * LOCALBOARDSIZE), height=int(.75 * SQUARESIZE),
                        colorfamily=[LIGHT_BLUE, MEDIUM_GRAY])
        self.selected = False

        # Add selected surface
        self.selected_surface = pygame.Surface(self.rect.size)
        self.update_surfaces()

    def update_surfaces(self):
        # update regular surfaces
        self.update()

        # update selected_surface
        self.selected_surface.fill(MEDIUM_BLUE)

        w = self.rect.width  # syntactic sugar
        h = self.rect.height  # syntactic sugar

        caption_surface = FONT.render(self.text, True, LIGHT_GRAY)
        caption_rect = caption_surface.get_rect()
        caption_rect.center = w // 2, h // 2
        self.selected_surface.blit(caption_surface, caption_rect)

        pygame.draw.rect(self.selected_surface, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.line(self.selected_surface, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.selected_surface, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.selected_surface, DARK_GRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self.selected_surface, DARK_GRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self.selected_surface, GRAY, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(self.selected_surface, GRAY, (w - 2, 2), (w - 2, h - 2))

    def draw_option(self, surface, update=True):
        if self.selected:
            surface.blit(self.selected_surface, self.rect)
        else:
            self.draw(surface, update=False)

        if update:
            pygame.display.update(self.rect)


class GameOptions:
    """Kind of like a drop down menu that's always down, cause I'm too lazy to make an actual drop down menu. User
    selects one of the options, which sets the mode. When a new game is started, the mode will determine the game setup,
    i.e. 2-player vs AI difficulty, or determining who goes first."""

    def __init__(self, pos, default, *options):
        """
        :param pos: position of the first button
        :param default: button selected by default
        :param options: the text to be displayed on each button (also the mode that the button will dictate)
        """
        self.rect = pygame.Rect(pos, (int(.45 * LOCALBOARDSIZE), int(.75 * SQUARESIZE)))
        self.mode = default
        self.options = []
        for i in range(len(options)):
            left = pos[0]
            top = pos[1] + (i * .75 * SQUARESIZE)
            self.options.append(GameOptionButton((left, top), options[i]))
            if self.mode == self.options[i].text:
                self.options[i].selected = True

    def is_event(self, event, mouse, surface):
        for button in self.options:
            if button.is_button_event(event, mouse):
                if event.type == pygame.MOUSEBUTTONDOWN and not button.selected:
                    for button_again in self.options:  # button_again will always make me laugh
                        if button is button_again:
                            button_again.selected = True
                        elif button_again.selected:
                            button_again.selected = False
                            button_again.draw_option(surface)
                button.draw_option(surface)
                return True

    def draw(self, surface):
        for button in self.options:
            button.draw_option(surface, False)

    def get_option(self):
        for button in self.options:
            if button.selected:
                return button.text


"""******************************************************************************************************************"""


class TextArea:
    """White area that can print two lines of text. Used for printing the turn/winner"""

    def __init__(self):
        # Overall area of the textarea
        self.rect = pygame.Rect(GLOBALBOARDSIZE + BOARDERSIZE, BOARDERSIZE + int(0.25 * SQUARESIZE), LOCALBOARDSIZE,
                                SQUARESIZE)

        # Top half of the textarea
        self.top_rect = pygame.Rect(GLOBALBOARDSIZE + BOARDERSIZE, BOARDERSIZE + int(0.25 * SQUARESIZE), LOCALBOARDSIZE,
                                    SQUARESIZE // 2)
        self.top_surface = pygame.Surface(self.top_rect.size)

        # Bottom half of the textarea
        self.bot_rect = pygame.Rect(GLOBALBOARDSIZE + BOARDERSIZE, BOARDERSIZE + (SQUARESIZE // 4) + (SQUARESIZE // 2),
                                    LOCALBOARDSIZE, SQUARESIZE // 2)
        self.bot_surface = pygame.Surface(self.bot_rect.size)

    def set_text(self, top_text, bot_text, surface, color=BLACK):
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

    def __init__(self):
        self.offset = (SQUARESIZE, SQUARESIZE)  # offset from the main screen
        self.rect = pygame.Rect(self.offset[0], self.offset[1], GLOBALBOARDSIZE - 2 * SQUARESIZE,
                                GLOBALBOARDSIZE - 2 * SQUARESIZE)
        self.surface = pygame.Surface(self.rect.size)
        self.ok_button = Button((self.rect.centerx - (LOCALBOARDSIZE // 2) - self.offset[0],
                                 GLOBALBOARDSIZE - int(2.5 * SQUARESIZE) - self.offset[1]), 'OK')

        # Get the rules from rules.txt, and save each line in a list. File must end with a newline
        with open("gui/rules.txt", 'r') as file:
            self.linesoftext = file.readlines()

        self.write_rules()  # draw each line on the surface
        self.ok_button.draw(self.surface, False)

    def write_rules(self):
        for i in range(len(self.linesoftext)):
            line = self.linesoftext[i]
            text_surface = FONT.render('> ' + line[:-1], True, GREEN)  # get rid of the newline character
            text_rect = text_surface.get_rect()
            text_rect.topleft = (8, 8 + 24 * i)  # placement of each line on the surface
            self.surface.blit(text_surface, text_rect)

    def show_rules(self, screen):
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
