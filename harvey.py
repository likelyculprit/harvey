import sys
import pygame

from settings import Settings
from hero import Hero


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
