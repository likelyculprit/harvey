from random import randint


class Settings:
    '''A class to store all game settings.'''

    # Screen settings.
    screen_width = 800
    screen_height = 800
    bg_color = (20, 10, 70)

    # Ship settings.
    ship_speed = 5

    # Bullet settings.
    bullet_speed = 6
    bullet_width = 8
    bullet_height = 8
    bullet_damage = 1
    bullets_allowed = 3

    # Speck settings.
    speck_chance = 6

    # Alien settings.
    # chance out of 1000 that an alien will appear each tick.
    alien_chance = 4
    alien_hp = 1

    def get_rand_velo(self):
        return (randint(-1, 1), randint(-1, 1))


###################### TODO ################################
# levels
# stars background new each level
# generate specks
# aliens eat specks
# animate aliens
# borders
# obstacles

# abilities new each level
# temp pickups
# different aliens
