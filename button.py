import pygame.font


class Button:
    """Button to start playing or restart game"""

    def __init__(self, ai_game, msg):
        """intialise the button"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # set dimensions and button properties
        self.width, self.height = 200, 50
        self.button_color = (100, 255, 0)
        self.text_color = (225, 225, 225)
        self.font = pygame.font.SysFont(
            None, 48
        )  # Font Name to None to use system default

        # built the button rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message need to be prepared once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color
        )  # True for antiliasing, makeing text edges smother, button_color->sets text background color, the same as button
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.screen_rect.center

    def draw_button(self):
        """Draw the button then the text on screen surface"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
