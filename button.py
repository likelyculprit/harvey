from pygame.sprite import Sprite
import pygame.font


class Button(Sprite):
    '''Class for buttons and interface elements.'''

    def __init__(self, harvey, image_path, msg):
        '''Init button attributes.'''
        super().__init__()
        self.screen = harvey.screen
        self.screen_rect = self.screen.get_rect()

        # Set button properties.
        self.width, self.height = 200, 100
        self.text_color = (30, 167, 225)
        self.font = pygame.font.SysFont('segoeuiblack', 64)
        self.image = pygame.image.load(image_path)

        # Create button rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        '''Render msg as image and center it on the button.'''
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center  # this isnt happening

    def blitme(self):
        '''Draw blank button then draw button image.'''
        # self.screen.fill((214, 221, 231), self.rect)
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
