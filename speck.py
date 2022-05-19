import pygame
from pygame.sprite import Sprite
from random import randint


class Speck(Sprite):
    '''A class to represent an energy speck.'''

    def __init__(self, harvey):
        '''Init speck and set starting position.'''
        super().__init__()
        self.screen = harvey.screen
        self.settings = harvey.settings

        # Load speck image and set its rect.
        self.image = pygame.image.load('assets/speck.png')
        self.rect = self.image.get_rect()
        self.radius = self.image.get_width() / 2

        # Set random starting position.
        self.rect.x = randint(80, 700)
        self.rect.y = randint(80, 700)

    def blitme(self):
        '''Draw alien at its current location.'''
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
