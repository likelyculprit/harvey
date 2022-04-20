import pygame
from pygame.sprite import Sprite
from random import randint


class Alien(Sprite):
    '''A class to represent a single alien.'''

    def __init__(self, harvey):
        '''Init alien and set starting position.'''
        super().__init__()
        self.screen = harvey.screen

        # Load alien image and set its rect.
        self.image = pygame.image.load('assets/alien1.bmp')
        self.rect = self.image.get_rect()

        # Set random starting position.
        self.rect.x = randint(80, 700)
        self.rect.y = randint(80, 700)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
