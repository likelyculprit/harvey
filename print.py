def run_game(self):
    while 1:

        self._check_events()
             # inputs

        self.hero.update()
             # hero movement

        self._update_bullets()
             # allow shooting for interaction

        if self.stats.game_active:
            self._update_aliens()

            self._update_specks()

        self._update_screen()
         self.screen.fill(self.settings.bg_color)

          self.hero.blitme()

           for bullet in self.bullets.sprites():
                bullet.blitme()

            for alien in self.aliens.sprites():
                alien.blitme()

            for speck in self.specks.sprites():
                speck.blitme()

            if not self.stats.game_active:
                self.play_button.blitme()

            pygame.display.flip()
            self.clock.tick(60)
