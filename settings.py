# This file will contain all the settings of the project in one place instead of
# of searching through the entire project


class Settings:
    """A file storing all settings for alien invasion"""

    def __init__(self):
        """intialise the game settings"""
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # ship setting
        self.ship_speed = 1.5
        self.ships_limit = 3  # default 3
        # Bullet_Setting
        self.bullet_speed = 1  # default 1.5
        self.bullet_width = 400  # default 3
        self.bullet_height = 15  # default 15
        self.bullet_color = (60, 70, 90)
        self.bullets_allowed = 10
        # Alien_Settings
        self.alien_speed = 0.3  # default 0.3
        self.fleet_drop_speed = 10  # default 10
        self.fleet_direction = 1  # Right -> 1, Left -> -1
        self.alien_delay = 1
        self.alien_points = 50  # default 50
        # Rates
        self.speedup_rate = 2  # default 1.5
        self.points_rate = 2  # default 2
        

        self.intialize_dynamic_settings()

    def intialize_dynamic_settings(self):
        """Intialise the values that can change during the game"""
        # I noticed that at really high speeds, that pygame collosion funtions wasn't fast enough to detect
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 0.3
        self.fleet_direction = 1  # Right -> 1, Left -> -1
        self.alien_points = 50

    def increase_speed(self):
        """Increase the speeds settings and alien score values"""
        self.ship_speed *= self.speedup_rate
        self.bullet_speed *= self.speedup_rate
        self.alien_speed *= self.speedup_rate
        self.alien_points *= self.points_rate
