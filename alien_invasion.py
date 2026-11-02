import sys  # to be able to exit the game

import pygame

from time import sleep  # To be able to make delay when ship is hit

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:
    """Overall class to save game assets and behaviour"""

    def __init__(self):
        # Intialise the backgrond so that pygame can work properly
        pygame.init()

        # Make instance of Settings class
        self.settings = Settings()

        # Intialise dynamic settings at game begining
        self.settings.intialize_dynamic_settings()

        # This object is called a surface. This where all graphics can fit
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # sets an attribute that contain color of the window
        self.bg_color = self.settings.bg_color

        # Make instance of game status
        self.stats = GameStats(self)

        # Score board intialisation at top right
        self.scoreboard = ScoreBoard(self)

        # make an instance of Ship after we made the screen
        self.ship = Ship(self)
        # Instance of the sprite group for bullets
        self.bullets = pygame.sprite.Group()
        # Instance of the sprite group for aliens
        self.aliens = pygame.sprite.Group()

        # Instance of the button
        self.button = Button(self, "play")

        # Intialise the creation of alien fleet at the game begining
        self._create_fleet()

        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    # refactoring code using helper methods
    def _check_events(self):
        """Checks for any mouse or keyboard events"""
        # Note pygame.event.get() lists all the events from
        # last time the function was called
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_mouse_pos(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_mouse_pos(
        self, pos
    ):  # A point here, if player clicked the mouse, say by mistake while playing the game <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        """Starts the new game when player chicks play"""
        button_clicked = self.button.rect.collidepoint(pos)
        if button_clicked and not self.stats.game_active:
            # Intialise the game settings at the start of new game
            self.settings.intialize_dynamic_settings()

            # Reset Game Statistics
            self.stats.reset_stats()
            self.stats.game_active = True

            # reset the score board at start
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()

            # Remove any remainging alien or ship
            self.aliens.empty()
            self.bullets.empty()

            # Recner the ship and create fleet at game start
            self.ship.center_ship()
            self._create_fleet()  # Note this can be removed as its updated automatically within _update_bullets()

            # Hide cursor during game
            pygame.mouse.set_visible(False)

        else:
            self.stats.game_active = False
            # Make visible if player pressed mouse
            pygame.mouse.set_visible(True)

    def _check_keydown_events(self, event):
        """respond to keypress, made to cofactor _check_events"""
        if event.key == pygame.K_RIGHT:
            # update moving_right flag
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # update moving_left flag
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """respond to keyup, made to cofactor _check_events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Creates a new bullet and add it to bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """update positon of bullets and git rid of old bullets."""
        self.bullets.update()
        # Get rid of the old bullets so that, it doesn't consume memory
        for bullet in self.bullets.sprites():  # .copy() vs. .sprites()
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullets_aliens_collisions()

    def _check_bullets_aliens_collisions(self):
        """Respond to bullet-alien collision"""
        # Check for collosions of Aliens and Bullets groups
        # if so, it removes both
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)

        if collisions:
            for value in collisions.values():
                self.stats.score += self.settings.alien_points * len(value)
            self.scoreboard.prep_score()

        # check if there is still any aliens, create fleet again if not so
        if not self.aliens:
            self.stats.game_level += 1  # increase level when all fleet shoot down
            self.scoreboard.prep_level()
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_aliens(self):
        """Update the position of aliens on screen"""
        self._check_fleet_edges()
        self.aliens.update()

        # check ship-alien collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check if aliens has hit bottom
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond if any aliens has reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change its direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to ship being hit by alien."""
        if self.stats.ships_left > 1:
            # Decrements the ships left
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            # Get rid of the remainig aliens or bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause before reset
            sleep(1)
        else:
            # Check for the maximum score for scoreboard
            self.stats.max_score = max(self.stats.max_score, self.stats.score)
            # Game Over when player runs out of ships
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        """Check if aliens has reached the bottom of screen"""
        # check if alien reach Screen Bottom
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # creates an alien and finds the number of aliens in a row
        # spacing between aliens is equal to one alien width
        alien = Alien(self)  # This alien won't be added to the fleet
        alien_width, alien_height = alien.rect.size
        # Determine number of aliens in each row
        ship_height = self.ship.rect.height
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # Determine number of rows of aliens
        avaliable_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height
        )
        number_aliens_y = avaliable_space_y // (2 * alien_height)

        # Creates rows of aliens
        for row_number in range(0, number_aliens_y):
            # Create aliens in each row
            for alien_number in range(0, number_aliens_x):
                # create an alien and place it in the row
                alien = Alien(self)
                alien.x = alien_width + 2 * alien_width * alien_number
                alien.y = alien_height + 2 * alien_height * row_number
                alien.rect.x = alien.x
                alien.rect.y = alien.y
                self.aliens.add(alien)

    def _update_screen(self):
        """update image on screen and flip to the new scene"""
        # Redraw the screen throuhg each path through each pass through the loop
        # using fill method
        self.screen.fill(self.bg_color)

        # After displaying the screen, we draw ship by using bltime fuction
        self.ship.bltime()

        if self.stats.game_active:  # I found out that that I can still fire one bullet and it draws on screen after game is inactive, so <<<
            # updates Bullets position
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

        if not self.stats.game_active:
            # Adding button to play if game isn't acitve
            self.button.draw_button()

        # add alien to screen
        self.aliens.draw(self.screen)

        # Add score to display
        self.scoreboard.display_score()

        # Make the most recnetly drawn screens visible
        # it erases the old screen making the new scene visible
        # making the illusion of motion
        pygame.display.flip()


if __name__ == "__main__":  # if the file is called directly, not imported as module
    # as python sets the special value __name__ = '__main__' when run directly
    # Make the game instances and start the game
    ai = AlienInvasion()
    ai.run_game()
