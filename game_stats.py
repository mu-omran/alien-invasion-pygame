class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Intialise Statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Intial score for any new game
        self.score = 0

        # Maximum Score Container
        self.max_score = 0

        # Game level
        self.game_level = 0

        # Flag for Game Activity
        self.game_active = False

    def reset_stats(self):
        """Intialise the statistics that can vary throughout the game"""
        self.ships_left = self.settings.ships_limit
        self.score = 0
        self.game_level = 0
