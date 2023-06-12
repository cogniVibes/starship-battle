
class Settings:
    """A class to store all the settings for Alien Invsdion"""


    def __init__(self) -> None:
        """Initialize the game's static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 650
        self.bg_colour = (0,0,0)

        self.chosen_button_colour = (191,121,88)
        
        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (225,225,225)

        # How quickly the alien point value increases
        self.score_scale = 1.5

        # Ship settings
        self.ship_limit = 3

        self.initialize_dynamic_settings()

        self.mode = 0



    def easy_init(self) -> None:        
        # Alien settings
        self.fleet_drop_speed = 7

        # How quickly the game speeds up
        self.speedup_scale = 1.1

    def medium_init(self) -> None:
        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1


    def hard_init(self) -> None:
        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.2


    def initialize_dynamic_settings(self) -> None:
        self.ship_speed = 7.5
        self.bullet_speed = 7.5
        self.alien_speed = 2.5
        self.alien_points = 50

        # fleet_direction of 1 represents right, -1 represents left
        self.fleet_direction = 1


    def increase_speed(self) -> None:
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
