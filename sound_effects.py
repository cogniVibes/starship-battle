import pygame

pygame.mixer.init()

bullet_sound = pygame.mixer.Sound('assets/sounds/bullet.wav')
alien_sound = pygame.mixer.Sound('assets/sounds/explosion.wav')
play_sound = pygame.mixer.Sound('assets/sounds/play.wav')
click_sound = pygame.mixer.Sound('assets/sounds/click.wav')
ship_hit_sound = pygame.mixer.Sound('assets/sounds/ship_hit.wav')

pygame.mixer.music.load('assets/sounds/On My Way.wav')