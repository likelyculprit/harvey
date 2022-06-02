import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
from random import randint


class Alien(Sprite):
    '''A class to represent a single alien.'''

    def __init__(self, harvey, velocity):
        '''Init alien and set starting position.'''
        super().__init__()
        self.screen = harvey.screen
        self.settings = harvey.settings
        self.velocity = Vector2(velocity)
        self.hero = harvey.hero

        # Load alien image and set its rect.
        self.image = pygame.image.load('assets/alien1.png')
        self.rect = self.image.get_rect()
        self.radius = self.image.get_width() / 2

        # Set random starting position.
        self.rect.x = randint(80, 700)
        self.rect.y = randint(80, 700)
        self.position = Vector2(float(self.rect.x), float(self.rect.y))

        # Set starting HP.
        self.hp = self.settings.alien_hp

    def update(self):
        '''Move each alien on the screen.'''
        self.position = self.position + self.velocity
        self.check_edges()
        self.blit_position = self.position - Vector2(self.radius)
        self.rect.x = int(self.blit_position.x)
        self.rect.y = int(self.blit_position.y)
        self.screen.blit(self.image, self.blit_position)

    def check_edges(self):
        '''Determine if alien hits screen edges.'''
        # Top or bottom edges.
        if ((self.position.y - self.radius) <= 0 or
                (self.position.y + self.radius) >=
                self.settings.screen_height):
            self.velocity.y *= -1

        # Side edges.
        if ((self.position.x - self.radius) <= 0 or
                (self.position.x + self.radius) >=
                self.settings.screen_width):
            self.velocity.x *= -1

    def blitme(self):
        '''Draw alien at its current location.'''
        self.blit_position = self.position - Vector2(self.radius)
        self.screen.blit(self.image, self.blit_position)
