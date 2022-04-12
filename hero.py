import pygame


class Hero:
    '''A class to manage the ship.'''

    def __init__(self, harvey):
        '''Init the ship and set its starting position.'''
        self.screen = harvey.screen
        self.settings = harvey.settings
        self.screen_rect = harvey.screen.get_rect()

        # Load the ship image and get its rect.
        self.orig_image = pygame.image.load('assets/hero.bmp')
        self.image = self.orig_image
        self.rect = self.image.get_rect()

        # Variables for line end points.
        self.line_start = (0, 0)

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement and position flags.
        self.on_bottom = True
        self.on_top = False
        self.on_left = False
        self.on_right = False

        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False

        self.jumping = False

    def update(self):
        '''Update ship position based on movement flag.'''
        pygame.draw.line(self.screen, (255, 255, 255), (60, 80), (130, 100))
        if self.jumping:
            # self.moving_right = False
            # self.moving_left = False
            # self.moving_down = False
            # self.moving_up = False

            # Jump from bottom.
            if self.on_bottom and (
                    self.rect.centerx <= self.screen_rect.centerx):
                if self.rect.left > self.screen_rect.left:
                    self.line_end = (0,
                                     (self.rect.midleft[1] -
                                      self.rect.midleft[0])
                                     )
                    self.image = pygame.transform.rotate(self.orig_image, -45)
                    self.x -= self.settings.ship_speed
                    self.y -= self.settings.ship_speed
                elif self.rect.left <= self.screen_rect.left:
                    self.image = pygame.transform.rotate(self.orig_image, -90)
                    self.on_bottom = False
                    self.on_left = True
                    self.jumping = False

            elif self.on_bottom and (
                    self.rect.centerx > self.screen_rect.centerx):
                if self.rect.right < self.screen_rect.right:
                    self.line_end = (
                        self.settings.screen_width,
                        (sum(self.rect.midright) -
                         self.settings.screen_height))
                    self.image = pygame.transform.rotate(self.orig_image, 45)
                    self.x += self.settings.ship_speed
                    self.y -= self.settings.ship_speed
                elif self.rect.right >= self.screen_rect.right:
                    self.image = pygame.transform.rotate(self.orig_image, 90)
                    self.on_bottom = False
                    self.on_right = True
                    self.jumping = False

            # Jump from top.
            elif self.on_top and self.rect.centerx < self.screen_rect.centerx:
                if self.rect.left > self.screen_rect.left:
                    self.line_end = (0, sum(self.rect.midleft))
                    self.image = pygame.transform.rotate(self.orig_image, -135)
                    self.x -= self.settings.ship_speed
                    self.y += self.settings.ship_speed
                elif self.rect.left <= self.screen_rect.left:
                    self.line_start = self.rect.midright
                    self.image = pygame.transform.rotate(self.orig_image, -90)
                    self.on_top = False
                    self.on_left = True
                    self.jumping = False

            elif self.on_top and self.rect.centerx >= self.screen_rect.centerx:
                if self.rect.right < self.screen_rect.right:
                    self.line_end = (self.settings.screen_width,
                                     (self.settings.screen_width -
                                      (self.rect.midright[0] -
                                       self.rect.midright[1])))
                    self.image = pygame.transform.rotate(self.orig_image, -45)
                    self.x += self.settings.ship_speed
                    self.y += self.settings.ship_speed
                elif self.rect.right >= self.screen_rect.right:
                    self.image = pygame.transform.rotate(self.orig_image, 90)
                    self.on_top = False
                    self.on_right = True
                    self.jumping = False

            # Jump from left.
            elif self.on_left and self.rect.centery <= self.screen_rect.centery:
                if self.rect.top > self.screen_rect.top:
                    self.line_end = (sum(self.rect.midleft), 0)
                    self.image = pygame.transform.rotate(self.orig_image, -135)
                    self.x += self.settings.ship_speed
                    self.y -= self.settings.ship_speed
                elif self.rect.top <= self.screen_rect.top:
                    self.image = pygame.transform.rotate(self.orig_image, 180)
                    self.on_left = False
                    self.on_top = True
                    self.jumping = False

            elif self.on_left and self.rect.centery > self.screen_rect.centery:
                if self.rect.bottom < self.screen_rect.bottom:
                    self.line_end = (self.settings.screen_height -
                                     (self.rect.midbottom[1] -
                                      self.rect.midbottom[0]),
                                     self.settings.screen_height)
                    self.image = pygame.transform.rotate(self.orig_image, -45)
                    self.x += self.settings.ship_speed
                    self.y += self.settings.ship_speed
                elif self.rect.bottom >= self.screen_rect.bottom:
                    self.image = self.orig_image
                    self.on_left = False
                    self.on_bottom = True
                    self.jumping = False

            # Jump from right.
            elif self.on_right and self.rect.centery < self.screen_rect.centery:
                if self.rect.top > self.screen_rect.top:
                    self.line_end = (self.rect.midtop[0] - self.rect.midtop[1],
                                     0)
                    self.image = pygame.transform.rotate(self.orig_image, 135)
                    self.x -= self.settings.ship_speed
                    self.y -= self.settings.ship_speed
                elif self.rect.top <= self.screen_rect.top:
                    self.image = pygame.transform.rotate(self.orig_image, 180)
                    self.on_right = False
                    self.on_top = True
                    self.jumping = False

            elif self.on_right and self.rect.centery >= self.screen_rect.centery:
                if self.rect.bottom < self.screen_rect.bottom:
                    self.line_end = ((sum(self.rect.midbottom) -
                                      self.settings.screen_height),
                                     self.settings.screen_height)
                    self.image = pygame.transform.rotate(self.orig_image, 45)
                    self.x -= self.settings.ship_speed
                    self.y += self.settings.ship_speed
                elif self.rect.bottom >= self.screen_rect.bottom:
                    self.image = self.orig_image
                    self.on_right = False
                    self.on_bottom = True
                    self.jumping = False

        # Horizontal movement.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            if (self.on_top or self.on_bottom) and not self.jumping:
                self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            if (self.on_top or self.on_bottom) and not self.jumping:
                self.x -= self.settings.ship_speed

        # Vertical movement.
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            if (self.on_left or self.on_right) and not self.jumping:
                self.y += self.settings.ship_speed
        if self.moving_up and self.rect.top > self.screen_rect.top:
            if (self.on_left or self.on_right) and not self.jumping:
                self.y -= self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        '''Draw the ship at its current location.'''
        if self.jumping:
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                self.rect.center,
                self.line_end,
                width=3)
        self.screen.blit(self.image, self.rect)
