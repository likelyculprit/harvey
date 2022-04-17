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

        self.jumping = False

    def go_left(self):
        if self.on_bottom and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed
        elif self.on_top and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.on_left and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        elif self.on_right and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

    def go_right(self):
        if self.on_bottom and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.on_top and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed
        elif self.on_left and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        elif self.on_right and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed

    def jump_up(self):
        self.y -= self.settings.ship_speed

    def jump_down(self):
        self.y += self.settings.ship_speed

    def jump_left(self):
        self.x -= self.settings.ship_speed

    def jump_right(self):
        self.x += self.settings.ship_speed

    def update(self):
        '''Update ship position based on movement flag.'''
        pygame.draw.line(self.screen, (255, 255, 255), (60, 80), (130, 100))
        if self.jumping:

            # Jump from bottom.
            if self.on_bottom and (
                    self.rect.centerx <= self.screen_rect.centerx):
                if self.rect.left > self.screen_rect.left:
                    self.line_end = (0,
                                     (self.rect.midleft[1] -
                                      self.rect.midleft[0])
                                     )
                    self.image = pygame.transform.rotate(self.orig_image, -45)
                    self.jump_up()
                    self.jump_left()

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
                    self.jump_up()
                    self.jump_right()

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
                    self.jump_down()
                    self.jump_left()
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
                    self.jump_down()
                    self.jump_right()
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
                    self.jump_right()
                    self.jump_up()
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
                    self.jump_right()
                    self.jump_down()
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
                    self.jump_left()
                    self.jump_up()
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
                    self.jump_left()
                    self.jump_down()
                elif self.rect.bottom >= self.screen_rect.bottom:
                    self.image = self.orig_image
                    self.on_right = False
                    self.on_bottom = True
                    self.jumping = False

        # Surface movement.
        if self.moving_right and not self.jumping:
            self.go_right()
        if self.moving_left and not self.jumping:
            self.go_left()

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
