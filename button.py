from pygame.sprite import Sprite
import pygame.font


class Button(Sprite):
    '''Class for buttons and interface elements.'''

    def __init__(self, harvey, image_path):
        '''Init button attributes.'''
        super().__init__()
        self.screen = harvey.screen
        self.screen_rect = self.screen.get_rect()

        # Set button properties.
        self.width, self.height = 200, 100
        self.image = pygame.image.load(image_path)

        # Create button rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

    def blitme(self):
        '''Draw blank button then draw button image.'''
        # self.screen.fill((214, 221, 231), self.rect)
        self.screen.blit(self.image, self.rect)
