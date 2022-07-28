import pygame

from pygame.sprite import Sprite


class Bullet(Sprite):
    '''A class to manage bullets fired by player.'''

    def __init__(self, harvey):
        '''Create a bullet object at the ship's current position.'''
        super().__init__()
        self.screen = harvey.screen
        self.settings = harvey.settings
        self.hero = harvey.hero

        # Create a bullet at (0, 0) then set correct position.
        self.image = pygame.image.load('assets/bullet1.png')
        self.rect = self.image.get_rect()

        self.goes_up = False
        self.goes_down = False
        self.goes_right = False
        self.goes_left = False

        if self.hero.on_bottom:
            self.rect.center = self.hero.rect.midtop
            self.goes_up = True
        elif self.hero.on_top:
            self.rect.center = self.hero.rect.midbottom
            self.goes_down = True
        elif self.hero.on_left:
            self.rect.center = self.hero.rect.midright
            self.goes_right = True
        elif self.hero.on_right:
            self.rect.center = self.hero.rect.midleft
            self.goes_left = True

        # Store the bullet's position as a decimal value.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        '''Move the bullet on the screen.'''
        if self.goes_up:
            self.y -= self.settings.bullet_speed
        elif self.goes_down:
            self.y += self.settings.bullet_speed
        elif self.goes_right:
            self.x += self.settings.bullet_speed
        elif self.goes_left:
            self.x -= self.settings.bullet_speed

        self.rect.x, self.rect.y = self.x, self.y

    def blitme(self):
        '''Draw bullet at its current location.'''
        self.screen.blit(self.image, self.rect)
