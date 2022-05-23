import sys
import pygame
from random import randint
from time import sleep

from settings import Settings
from hero import Hero
from bullet import Bullet
from speck import Speck
from alien import Alien
from stats import Stats


class Harvey:
    '''Overall class to manage game assets and behavior.'''

    def __init__(self):
        '''Init the game and create resources.'''
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.pad = 0
        if pygame.joystick.get_count():
            self.pad = pygame.joystick.Joystick(0)
            self.pad.init()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.rect = self.screen.get_rect()
        pygame.display.set_caption("Harvey")
        self.stats = Stats(self)
        self.hero = Hero(self)
        self.bullets = pygame.sprite.Group()
        self.specks = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

    def run_game(self):
        '''Start the main loop for the game.'''
        while 1:
            self._check_events()

            if self.stats.game_active:
                self.hero.update()
                self._update_bullets()
                self._update_aliens()
                self._update_specks()

            self._update_screen()

    def start_level(self):
        '''Prepare a new level.'''
        self.aliens.empty()
        self.bullets.empty()
        self.specks.empty()
        self.hero.start_position()

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

    def _add_speck(self):
        '''Add specks to the screen.'''
        speck_rand_gen = randint(0, 1000)
        if (speck_rand_gen < self.settings.speck_chance and
                self.settings.specks_left > 0):
            speck = Speck(self)
            self.specks.add(speck)
            self.settings.specks_left -= 1
            print("Remaining specks:", self.settings.specks_left)

    def _update_specks(self):
        '''Update status of specks.'''
        self._add_speck()
        self.specks.update()
        if self.settings.specks_left <= 0 and not self.specks:
            print("Aliens have taken all energy. We're doomed")

    def _add_alien(self):
        '''Add aliens to the screen.'''
        alien_rand_gen = randint(0, 1000)
        if (alien_rand_gen < self.settings.alien_chance and
                self.settings.aliens_left > 0):
            # Randomized velocity vector.
            alien = Alien(self, self.settings.get_rand_velo())
            self.aliens.add(alien)
            self.settings.aliens_left -= 1
            print("Aliens remaining:", self.settings.aliens_left)

    def _update_aliens(self):
        '''Update position of aliens.'''
        self._add_alien()
        self.aliens.update()
        if self.settings.aliens_left <= 0 and not self.aliens:
            print("You have eliminated the threat")

        # Check for alien-hero collisions.
        alien_coll = pygame.sprite.spritecollide(self.hero, self.aliens, True)
        if alien_coll:
            self.hero.stunned = True
            self.hero.timer = 3000
        self.hero.check_stun(self.clock.get_time())

        # Check for alien-speck collisions.
        eats = pygame.sprite.groupcollide(
            self.specks, self.aliens, True, False)

    def _fire_bullet(self):
        '''Create a new bullet and add it to the bullets group.'''
        if (len(self.bullets) < self.settings.bullets_allowed and
                not self.hero.stunned):
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        '''Update position of bullets and delete old bullets.'''
        self.bullets.update()

        # for alien in self.aliens.copy():
        #     hit_bullet = pygame.sprite.spritecollide(
        #         alien, self.bullets, True)

        # Delete bullets that have left the screen.
        for bullet in self.bullets.copy():
            if (bullet.rect.bottom < 0 or
                    bullet.rect.top > self.settings.screen_height or
                    bullet.rect.left > self.settings.screen_width or
                    bullet.rect.right < 0):
                self.bullets.remove(bullet)
            # for hit_alien in pygame.sprite.spritecollide(
            #         bullet, self.aliens, False):
            #     self._damage(hit_alien, self.settings.bullet_damage)
        # Check for bullet-alien collisions and remove both on contact.
        hits = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, False)
        for alien in hits.values():
            self._damage(alien[0], self.settings.bullet_damage)

    def _damage(self, alien, damage):
        '''Deal damage to a hit alien.'''
        alien.hp -= damage
        if alien.hp <= 0:
            self.aliens.remove(alien)

    def _update_screen(self):
        '''Update images on screen and flip to new screen.'''
        self.screen.fill(self.settings.bg_color)
        self.hero.blitme()
        for bullet in self.bullets.sprites():
            bullet.blitme()
        for alien in self.aliens.sprites():
            alien.blitme()
        for speck in self.specks.sprites():
            speck.blitme()
        pygame.display.flip()
        self.clock.tick(60)


if __name__ == '__main__':
    # Make a game instance and run the game.
    harvey = Harvey()
    harvey.run_game()
