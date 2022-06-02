from random import randint


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
