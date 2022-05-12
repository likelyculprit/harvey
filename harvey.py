import sys
import pygame
from random import randint

from settings import Settings
from hero import Hero
from bullet import Bullet
from alien import Alien


class Harvey:
    '''Overall class to manage game assets and behavior.'''

    def __init__(self):
        '''Init the game and create resources.'''
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.running = True
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
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

    def run_game(self):
        '''Start the main loop for the game.'''
        while self.running:
            self._check_events()
            self.hero.update()
            self._update_bullets()
            self._update_aliens()
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

                if self.pad.get_button(2):
                    self.hero.jumping = True

                if self.pad.get_button(0) or self.pad.get_axis(5) > 0:
                    if not self.hero.jumping:
                        self._fire_bullet()

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

        elif event.key == pygame.K_b:
            if self.hero.jumping == False:
                self.hero.jumping = True

        elif event.key == pygame.K_SPACE:
            if not self.hero.jumping:
                self._fire_bullet()

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

    def _add_alien(self):
        '''Add aliens to the screen.'''
        # Randomized velocity vector.
        alien = Alien(self, self.settings.get_rand_velo())
        self.aliens.add(alien)

    def _generate_alien(self):
        '''Determine if a new alien should appear.'''
        alien_rand_gen = randint(0, 1000)
        if alien_rand_gen < self.settings.alien_chance:
            self._add_alien()

    def _update_aliens(self):
        '''Update position of aliens.'''
        self._generate_alien()
        self.aliens.update()

        # Check for alien-hero collisions.
        alien_coll = pygame.sprite.spritecollideany(self.hero, self.aliens)
        if alien_coll:
            print("stunned")
            self.hero.stun()
            if self.hero.on_top or self.hero.on_bottom:
                alien_coll.velocity.y *= -1
            if self.hero.on_left or self.hero.on_right:
                alien_coll.velocity.x *= -1

    def _fire_bullet(self):
        '''Create a new bullet and add it to the bullets group.'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        '''Update position of bullets and delete old bullets.'''
        self.bullets.update()

        # Delete bullets that have left the screen.
        for bullet in self.bullets.copy():
            if (bullet.rect.bottom < 0 or
                    bullet.rect.top > self.settings.screen_height or
                    bullet.rect.left > self.settings.screen_width or
                    bullet.rect.right < 0):
                self.bullets.remove(bullet)

        # Check for bullet-alien collisions and remove both on contact.
        self.collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

    def _update_screen(self):
        '''Update images on screen and flip to new screen.'''
        self.screen.fill(self.settings.bg_color)
        self.hero.blitme()
        for bullet in self.bullets.sprites():
            bullet.blitme()
        for alien in self.aliens.sprites():
            alien.blitme()
        pygame.display.flip()
        self.clock.tick(60)


if __name__ == '__main__':
    # Make a game instance and run the game.
    harvey = Harvey()
    harvey.run_game()
