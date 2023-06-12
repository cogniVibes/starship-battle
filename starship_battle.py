import sys
import json
from time import sleep
from random import randint

import pygame

from settings import Settings
from game_stats import GameStats
from display import Display
from button import Hard_Button, Play_Button, Easy_Button, Medium_Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from life import Lives
from star import Star
import sound_effects as se


class StarshipBattle:
    """Overall class to manage game assets and behaviour"""

    
    def __init__(self) -> None:
        """Initialize the game assets, and create game resources"""
        pygame.init()

        self.clock = pygame.time.Clock()
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode((1200, 650))

        self.stats = GameStats(self)
        self.dp = Display(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.stars = pygame.sprite.Group()
        self._create_stars()

        # Make the play button
        self.play_button = Play_Button(self,"PLAY")
        self.easy_button = Easy_Button(self,"EASY")
        self.medium_button = Medium_Button(self,"MEDIUM")
        self.hard_button = Hard_Button(self,"HARD")

        icon = pygame.image.load('assets/images/icon/starship_battle_icon.ico')
        pygame.display.set_caption("Starship Battle")
        pygame.display.set_icon(icon)
        if not self.stats.game_active:
            pygame.mixer.music.play(-1)
    
    def run_game(self) -> None:
        """Start the main loop for the game"""
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()
                self._check_fleet_edges()
                
            self._update_screen()

            self.clock.tick(60)

    
    def _check_events(self) -> None:
        # Respond to keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._close_game()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_easy_button(mouse_pos)
                self._check_medium_button(mouse_pos)
                self._check_hard_button(mouse_pos)


    def _start_game(self) -> None:        
        # Reset the game statistics``
        self.stats.reset_stats()
        self.stats.game_active = True
        
        # Get rid of any remaining aliens and bullets
        self.stats.ammo_used = 0 
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

        # Reset score and level
        self.dp.prep_score()
        self.dp.prep_level()
        self.dp.prep_lives()

        # Hide the mouse button
        pygame.mouse.set_visible(False)

    
    def _check_keydown_events(self, event) -> None:
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            # Move the ship to the right
            self.ship.moving_right = True

        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            # Move the ship to the left
            self.ship.moving_left = True
        if (self.stats.ammo - self.stats.ammo_used != 0 and
            event.key == pygame.K_SPACE):
                self._fire_bullet()

    
    def _check_keyup_events(self, event) -> None:
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

        elif event.key == pygame.K_q:
            self._close_game()

        elif event.key == pygame.K_p:
            self._start_game()


    def _check_play_button(self, mouse_pos) -> None:
        """Start a new game when player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active and self.stats.difficulty_chosen:
            se.play_sound.play()
            self._start_game()


    def _check_easy_button(self, mouse_pos) -> None:
        button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            se.click_sound.play()
            self.easy_button.button_colour = (self.settings.chosen_button_colour)
            self.easy_button.draw_button()
            self.medium_button.button_colour = (244,180,27)
            self.medium_button.draw_button()
            self.hard_button.button_colour = (244,180,27)
            self.hard_button.draw_button()
            self.settings.easy_init()
            self.settings.initialize_dynamic_settings()
            self.settings.ship_speed = 10.0
            self.settings.bullet_speed = 8.0
            self.settings.alien_speed = 1.5
            self.stats.difficulty_chosen = True
            self.settings.mode = 1

    def _check_medium_button(self, mouse_pos) -> None:
        button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            se.click_sound.play()
            self.medium_button.button_colour = (self.settings.chosen_button_colour)
            self.medium_button.draw_button()
            self.easy_button.button_colour = (244,180,27)
            self.easy_button.draw_button()
            self.hard_button.button_colour = (244,180,27)
            self.hard_button.draw_button()
            self.hard_button.draw_button()
            self.settings.medium_init()
            self.settings.initialize_dynamic_settings()
            self.stats.difficulty_chosen = True
            self.settings.mode = 2


    def _check_hard_button(self, mouse_pos) -> None:
        button_clicked = self.hard_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            se.click_sound.play()
            self.hard_button.button_colour = (self.settings.chosen_button_colour)
            self.hard_button.draw_button()
            self.easy_button.button_colour = (244,180,27)
            self.easy_button.draw_button()
            self.medium_button.button_colour = (244,180,27)
            self.medium_button.draw_button()
            self.settings.easy_init()
            self.settings.initialize_dynamic_settings()
            self.stats.difficulty_chosen = True
            self.settings.mode = 3

    
    def _fire_bullet(self) -> None:
        """Create a new bullet and add it to the bullet group"""   
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
        se.bullet_sound.play()
        self.stats.used_ammo()
        if self.stats.ammo - self.stats.ammo_used == 0:
            self._ship_hit()

    
    def _update_bullets(self) -> None:
        """Update position of bullets and get rid of old bullets"""
        # Update bullet positions
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                
        self._check_bullet_alien_collision()


    def _check_bullet_alien_collision(self) -> None:
        """Respond to bullet-alien collisions"""
        # Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.dp.prep_score()
            self.dp.check_high_score()
            se.alien_sound.play()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.ammo_used = 0

            # Increase level
            self.stats.level += 1
            self.dp.prep_level()


    def _create_fleet(self) -> None:
        """Create the fleet of aliens"""
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self)             
        alien_width, alien_height = alien.rect.size
        available_space = self.settings.screen_width - alien_width
        number_aliens_x = available_space // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                                (3 * alien_height) - ship_height)
        number_rows = (available_space_y // (2 * alien_height))

        self.stats.number_aliens = number_aliens_x * (number_rows - 1)
        self.aliens_number = number_aliens_x * (number_rows - 1)

        # Create the first row of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # Create an alien and place it in a row
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number) -> None:
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 *alien_width * alien_number
        alien.rect.x = alien.x
        if row_number == 0:
            alien.rect.y =  alien.rect.height + 2 * alien.rect.height
        else:
            alien.rect.y =  alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _update_aliens(self) -> None:
        """Update the position of all the aliens in the fleet"""
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()


    def _check_fleet_edges(self) -> None:
        """Respond appropriately if any alien has reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self) -> None:
        """Drop the entire fleet or change the direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

        
    def _ship_hit(self) -> None:
        """Respond to the ship being hit by alien"""
        # Decrement ships left, and update scoreboard
        se.ship_hit_sound.play()
        self.stats.ship_left -= 1
        self.dp.prep_lives()
        self.stats.ammo_used = 0

        if self.stats.ship_left > 0:
            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and centre the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(1.5)

        else:
            self.stats.game_active = False
            self.stats.difficulty_chosen = False
            pygame.mouse.set_visible(True)
            sleep(0.5)
            

    def _check_aliens_bottom(self) -> None:
        """Check if any alien has reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this as if the ship got hit
                self._ship_hit()
                break       

    def _create_stars(self) -> None:
        """Create a sky full of stars."""
        # Create an star and find the number of stars in a row.
        # Spacing between each star is equal to two star widths.
        star = Star(self)
        star_width, star_height = star.rect.size
        available_space_x = self.settings.screen_width - (star_width)
        number_stars_x = available_space_x // (200 * star_width)
            
        # Determine the number of rows of stars that fit on the screen.
        #   We'll just fill most of the screen with stars.
        available_space_y = (self.settings.screen_height -
                            (2 * star_height))
        number_rows = available_space_y // (4 * star_height)
            
        # Fill the sky with stars.
        for row_number in range(number_rows):
            for star_number in range(number_stars_x):
                self._create_star(star_number, row_number)

    def _create_star(self, star_number, row_number):
        """Create an star and place it in the row."""
        star = Star(self)
        star_width, star_height = star.rect.size
        star.rect.x = star_width + 2 * star_width * star_number
        star.rect.y = star.rect.height + 2 * star.rect.height * row_number

        # Randomize the positions of the stars.
        star.rect.x += randint(-1 * (self.settings.screen_width), self.settings.screen_width)
        star.rect.y += randint(-1 * (self.settings.screen_height), self.settings.screen_height)

        self.stars.add(star)  

    
    def _close_game(self) -> None:
        saved_high_score = self.stats.get_saved_high_score()
        f = 0
        if saved_high_score['easy'] < self.stats.high_score['easy']:
            f = 1
        elif saved_high_score['medium'] < self.stats.high_score['medium']:
            f = 1
        elif saved_high_score['hard'] < self.stats.high_score['hard']:
            f = 1
        if f == 1:
            with open ('assets/high_score.json', 'w') as f:
                json.dump(self.stats.high_score, f)

        sys.exit()

    
    def _update_screen(self) -> None:
        # Update images on the screen, and flip to new screen
        self.screen.fill(self.settings.bg_colour)
        self.ship.blitme()
        self.stars.draw(self.screen)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information
        self.dp.show_score()

        self.stats.initialize_ammo()

        #Draw the play button if the game is inactive
        if not self.stats.game_active and not self.stats.difficulty_chosen:
            self.easy_button.button_colour = (244,180,27)
            self.medium_button.button_colour = (244,180,27)
            self.hard_button.button_colour = (244,180,27)
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()
        elif not self.stats.game_active and self.stats.difficulty_chosen:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance and run
    ai = StarshipBattle()
    ai.run_game()

