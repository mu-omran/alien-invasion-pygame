from pygame.font import SysFont
from pygame.sprite import Group
from ship import Ship


class ScoreBoard:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.stats = ai_game.stats
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Score Text properties
        self.score_color = (255, 255, 255)
        self.font = SysFont(None, 48)

        self.prep_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn score text into rendered image"""
        # For the dynamic score
        score = self.stats.score
        rounded_score = round(score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(
            score_str, True, self.score_color, self.settings.bg_color
        )
        self.score_rect = self.score_image.get_rect()

        # Display score at top right of the screen
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

        # For the maximum score
        max_score = self.stats.max_score
        rounded_max = round(max_score, -1)
        max_str = f"{rounded_max:,}"
        self.max_image = self.font.render(
            max_str, True, self.score_color, self.settings.bg_color
        )
        self.max_image_rect = self.max_image.get_rect()

        # Display max score at top center of the screen
        self.max_image_rect.centerx = self.screen_rect.centerx
        self.max_image_rect.top = 20

    def prep_level(self):
        """Convert level to pygame surface object and makes its rect"""
        level = self.stats.game_level
        level_str = str(level)
        self.level_image = self.font.render(
            level_str, True, self.score_color, self.settings.bg_color
        )
        self.level_rect = self.level_image.get_rect()

        # place level on screen surface
        self.level_rect.top = self.score_rect.bottom + 10
        self.level_rect.right = self.score_rect.right

    def prep_ships(self):
        """Create the ships left for dashboard display"""
        self.ships = Group()
        for i in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.left = 20 + i * ship.rect.width
            ship.rect.top = 20
            self.ships.add(ship)
       
    def display_score(self):
        """Display scores, level, and ships on display"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.max_image, self.max_image_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
