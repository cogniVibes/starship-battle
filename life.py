import pygame
from pygame.sprite import Sprite

class Lives(Sprite):
    """Class to display lives"""

    def __init__(self, ai_game) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.stats = ai_game.stats
        self.screen_rect = ai_game.screen.get_rect()

        # Load the life image and get its rect
        self.image = pygame.image.load('assets/images/heart.bmp')
        self.rect = self.image.get_rect()
