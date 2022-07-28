###################### TODO ################################
# bug number of bullets

# levels
# stars background new each level
# obstacles
# animate aliens
# animate hero - propulsion, shootshake
# borders
# abilities new each level
# temp pickups
# different aliens

# netherium pentanium dilithium quantium thaumite


import sys
import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
import pygame.font
from random import randint


########################################################################
#        ####  #####  #####  #####  #####  #   #   ###    ####         #
#       #      #        #      #      #    ##  #  #      #             #
#        ###   ####     #      #      #    # # #  #  ##   ###          #
#           #  #        #      #      #    #  ##  #   #      #         #
#       ####   #####    #      #    #####  #   #   ###   ####          #
########################################################################


class Settings:
    '''A class to store all game settings.'''

    def __init__(self):
        '''Init static settings.'''
        # Screen settings.
        self.screen_width = 800
        self.screen_height = 800
        self.bg_color = (20, 10, 70)

        # Bullet settings.
        self.bullet_width = 8
        self.bullet_height = 8

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        '''Init settings that can change during the game.'''
        self.ship_speed = 5

        self.bullet_speed = 6
        self.bullet_damage = 1
        self.bullets_allowed = 3

        self.speck_chance = 3  # chance per 1000 to appear each tick.
        self.specks_left = randint(15, 25)

        self.alien_chance = 5  # chance per 1000 to appear each tick.
        self.aliens_left = randint(40, 50)
        self.alien_hp = 1


########################################################################
#                   ####  #####   ###   #####   ####                   #
#                  #        #    #   #    #    #                       #
#                   ###     #    #####    #     ###                    #
#                      #    #    #   #    #        #                   #
#                  ####     #    #   #    #    ####                    #
########################################################################

class Stats:
    '''Track stats for the game.'''

    def __init__(self, harvey):
        '''Init stats.'''
        self.settings = harvey.settings
        self.reset_stats()
        # Start game inactive until player presses button.
        self.game_active = 0
        self.scene_active = 0
        self.choice_active = 0
        self.current_level = 1

    def reset_stats(self):
        '''Reset stats to initial state.'''
        self.specks_left = self.settings.specks_left


########################################################################
#              ####   #   #  #####  #####   ###   #   #                #
#              #   #  #   #    #      #    #   #  ##  #                #
#              ####   #   #    #      #    #   #  # # #                #
#              #   #  #   #    #      #    #   #  #  ##                #
#              ####    ###     #      #     ###   #   #                #
########################################################################


class Button(Sprite):
    '''Class for buttons and interface elements.'''

    def __init__(self, harvey, width, height, msg):
        '''Init button attributes.'''
        super().__init__()
        self.screen = harvey.screen
        self.screen_rect = self.screen.get_rect()

        # Set button properties.
        self.width, self.height = width, height
        self.text_color = (30, 167, 225)
        self.font = pygame.font.SysFont('segoeuiblack', 64)

        # Create button rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        pygame.draw.rect(rect, color, (x, y, width, height), thickness, radius)

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

########################################################################
#                      #   #  #####  ####    ###                       #
#                      #   #  #      #   #  #   #                      #
#                      #####  ####   ####   #   #                      #
#                      #   #  #      #   #  #   #                      #
#                      #   #  #####  #   #   ###                       #
########################################################################


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


########################################################################
#                   ###   #      #####  #####  #   #                   #
#                  #   #  #        #    #      ##  #                   #
#                  #####  #        #    ####   # # #                   #
#                  #   #  #        #    #      #  ##                   #
#                  #   #  #####  #####  #####  #   #                   #
########################################################################


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


########################################################################
#               ####   #   #  #      #      #####  #####               #
#               #   #  #   #  #      #      #        #                 #
#               ####   #   #  #      #      ####     #                 #
#               #   #  #   #  #      #      #        #                 #
#               ####    ###   #####  #####  #####    #                 #
########################################################################


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


########################################################################
#                   ####  ####   #####   ####  #   #                   #
#                  #      #   #  #      #      #  #                    #
#                   ###   ####   ####   #      ###                     #
#                      #  #      #      #      #  #                    #
#                  ####   #      #####   ####  #   #                   #
########################################################################


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
        self.position = (self.rect.x, self.rect.y)

    def blitme(self):
        '''Draw speck at its current location.'''
        self.screen.blit(self.image, self.position)


########################################################################
#               #   #   ###   ####   #   #  #####  #   #               #
#               #   #  #   #  #   #  #   #  #       # #                #
#               #####  #####  ####   #   #  ####     #                 #
#               #   #  #   #  #   #   # #   #        #                 #
#               #   #  #   #  #   #    #    #####    #                 #
########################################################################


class Harvey:
    '''Overall class to manage game assets and behavior.'''

    def __init__(self):
        '''Init the game and create resources.'''
        pygame.init()
        self.settings = Settings()
        self.pad = 0
        if pygame.joystick.get_count():
            self.pad = pygame.joystick.Joystick(0)
        if self.pad:
            self.pad.init()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.rect = self.screen.get_rect()
        pygame.display.set_caption("Harvey")
        self.hero = Hero(self)

    def run_game(self):
        '''Start the main loop for the game.'''
        while True:
            self._check_events()
            self.hero.update()
            self._update_screen()

    def _check_events(self):
        '''Respond to keypresses and mouse events.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Gamepad inputs, prioritized above keyboard.
            if self.pad:
                if self.pad.get_button(6):
                    sys.exit()
                # Left stick or d-pad horizontal axis.
                if (self.pad.get_axis(0) < -0.07 or
                        self.pad.get_hat(0)[0] == -1):
                    self.hero.moving_left = True
                    self.hero.moving_right = False
                elif (self.pad.get_axis(0) > 0.07 or
                        self.pad.get_hat(0)[0] == 1):
                    self.hero.moving_right = True
                    self.hero.moving_left = False
                elif -0.07 <= self.pad.get_axis(0) <= 0.07:
                    self.hero.moving_left = False
                    self.hero.moving_right = False

                # Left stick or d-pad vertical axis.
                if (self.pad.get_axis(1) < -0.07 or
                        self.pad.get_hat(0)[1] == 1):
                    self.hero.moving_up = True
                    self.hero.moving_down = False
                elif (self.pad.get_axis(1) > 0.07 or
                        self.pad.get_hat(0)[1] == -1):
                    self.hero.moving_down = True
                    self.hero.moving_up = False
                elif -0.07 <= self.pad.get_axis(1) <= 0.07:
                    self.hero.moving_up = False
                    self.hero.moving_down = False

                if self.pad.get_button(2):
                    self.hero.jumping = True

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        '''Respond to keypresses.'''
        if event.key == pygame.K_RIGHT:
            self.hero.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.hero.moving_left = True
        elif event.key == pygame.K_DOWN:
            self.hero.moving_down = True
        elif event.key == pygame.K_UP:
            self.hero.moving_up = True

        elif event.key == pygame.K_b:
            if self.hero.jumping == False:
                self.hero.jumping = True

        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        '''Respond to key releases.'''
        if event.key == pygame.K_RIGHT:
            self.hero.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.hero.moving_left = False
        elif event.key == pygame.K_DOWN:
            self.hero.moving_down = False
        elif event.key == pygame.K_UP:
            self.hero.moving_up = False

    def _update_screen(self):
        '''Update images on screen and flip to new screen.'''
        self.screen.fill(self.settings.bg_color)
        self.hero.blitme()
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance and run the game.
    harvey = Harvey()
    harvey.run_game()
