import pygame.font
from pygame.sprite import Group

from life import Lives

class Display:
    """A class to report scoring information"""


    def __init__(self, ai_game) -> None:
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for storing information
        self.text_colour = (244,180,27)
        self.font_score = pygame.font.Font("assets/font/3D-Thirteen-Pixel-Fonts.ttf", 48)
        self.font_high_score = pygame.font.Font("assets/font/3D-Thirteen-Pixel-Fonts.ttf", 24)

        # Prepare the initial score image
        self.prep_score()
        self.prep_level() 
        self.prep_lives()
        self.prep_name()


    def prep_name(self) -> None:
        """Turn the game name into a rendered image."""
        name_str = "STARSHIP BATTLE"
        self.name_image = self.font_score.render(
            name_str, True,
            self.text_colour, self.settings.bg_colour)
        
        # Position the level at the top of the screen
        self.name_rect = self.name_image.get_rect()
        self.name_rect.centerx = self.screen_rect.centerx
        self.name_rect.top = self.score_rect.top
    
    
    def prep_score(self) -> None:
        """Turn the score into a rendered image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font_score.render(
            f"SCORE : {score_str}", True, self.text_colour,
            self.settings.bg_colour)

        # Display the score at the top-right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_high_score(self) -> None:
        """Turn the high score into a rendred image"""
        high_score = self.high_score_mode()
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font_high_score.render(
                f"HIGH SCORE : {high_score_str}", True,
                self.text_colour, self.settings.bg_colour)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.score_rect.right
        self.high_score_rect.top = self.score_rect.bottom + 10


        self.not_active_high_score_image = self.font_score.render(
                f"HIGH SCORE : {high_score_str}", True,
                self.text_colour, self.settings.bg_colour)
        self.not_active_rect = self.not_active_high_score_image.get_rect()
        
        self.not_active_rect.bottom = self.screen_rect.bottom - 125
        self.not_active_rect.centerx = self.screen_rect.centerx

    def prep_level(self) -> None:
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font_score.render(
            f"LEVEL : {level_str}", True,
            self.text_colour, self.settings.bg_colour)
        
        # Position the level at the top of the screen
        self.level_rect = self.level_image.get_rect()
        self.level_rect.centerx = self.screen_rect.centerx
        self.level_rect.top = self.score_rect.top


    def prep_lives(self) -> None:
        """Show how many lives are left"""
        self.lives = Group()
        for life_number in range(self.stats.ship_left):
            life = Lives(self.ai_game)
            life.rect.x = 20 + life_number  * 1.2 * life.rect.width
            life.rect.y = self.score_rect.y
            self.lives.add(life)


    def prep_ammo(self) -> None:
        """Turn the ammo into a rendred image"""
        self.stats.initialize_ammo()
        ammo_str = "{:,}".format(self.stats.ammo)
        self.ammo_image = self.font_high_score.render(
                f"AMMO : {self.stats.ammo - self.stats.ammo_used}/{ammo_str}", True,
                self.text_colour, self.settings.bg_colour)
        self.ammo_rect = self.ammo_image.get_rect()
        self.ammo_rect.x = 20
        self.ammo_rect.top = self.score_rect.bottom + 10


    def check_high_score(self):
        """Check to see if there's a new high score."""
        high_score = self.high_score_mode()
        if self.stats.score > high_score:
            if self.settings.mode == 1:
                self.stats.high_score['easy'] = self.stats.score
            elif self.settings.mode == 2:
                self.stats.high_score['medium'] = self.stats.score
            elif self.settings.mode == 3:
                self.stats.high_score['hard'] = self.stats.score
            self.prep_high_score()


    def show_score(self) -> None:
        """Draw scores, level and lives to the screen"""
        if not self.stats.game_active:
            self.screen.blit(self.name_image, self.name_rect)
        if self.stats.difficulty_chosen and not self.stats.game_active:
            self.prep_high_score()
            self.screen.blit(self.not_active_high_score_image, self.not_active_rect)
        if self.stats.game_active:
            self.screen.blit(self.score_image, self.score_rect)
            self.screen.blit(self.high_score_image, self.high_score_rect)
            self.screen.blit(self.level_image, self.level_rect)
            self.prep_ammo()
            self.screen.blit(self.ammo_image, self.ammo_rect)
            self.lives.draw(self.screen)

    def high_score_mode(self):
        if self.stats.difficulty_chosen:
            if self.settings.mode == 1:
                high_score = round(self.stats.high_score['easy'], -1)
            elif self.settings.mode == 2:
                high_score = round(self.stats.high_score['medium'], -1)
            elif self.settings.mode == 3:
             high_score = round(self.stats.high_score['hard'], -1)
            return high_score