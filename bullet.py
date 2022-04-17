import pygame

from pygame.sprite import Sprite


class Bullet(Sprite):
    '''A class to manage bullets fired by player.'''

    def __init__(self, harvey):
        '''Create a bullet object at the ship's current position.'''
        super().__init__()
        self.screen = harvey.screen
        self.settings = harvey.settings

        # Create a bullet at (0, 0) then set correct position.
        self.image = pygame.image.load('assets/bullet1.bmp')
        self.rect = self.image.get_rect()

        if self.hero.on_bottom:
            self.rect.center = self.hero.rect.midtop
        elif self.hero.on_top:
            self.rect.center = self.hero.rect.midbottom
        elif self.hero.on_left:
            self.rect.center = self.hero.rect.midright
        elif self.hero.on_right:
            self.rect.center = self.hero.rect.midleft

        # Store the bullet's position as a decimal value.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
