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
        self.velocity = Vector2(velocity)

        # Load alien image and set its rect.
        self.image = pygame.image.load('assets/alien1.png')
        self.rect = self.image.get_rect()
        self.radius = self.image.get_width() / 2

        # Set random starting position.
        self.rect.x = randint(80, 700)
        self.rect.y = randint(80, 700)
        self.position = Vector2(float(self.rect.x), float(self.rect.y))

    def update(self):
        '''Move each alien on the screen.'''
        self.position = self.position + self.velocity
        self.blit_position = self.position - Vector2(self.radius)
        self.screen.blit(self.image, self.blit_position)

    # def blitme(self):
    #     '''Draw alien at its current location.'''
    #     print(self.position, self.radius, self.blit_position)
    #     self.blit_position = self.position - Vector2(self.radius)
    #     self.screen.blit(self.image, self.blit_position)

    def collides_with(self, other_obj):
        '''Determine if alien contacts anything.'''
        self.distance = self.position.distance_to(other_obj.position)
        return self.distance < self.radius + other_obj.radius
