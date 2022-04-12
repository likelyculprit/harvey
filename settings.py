class Settings:
    '''A class to store all game settings.'''

    def __init__(self):
        '''Init game settings.'''
        # Screen settings.
        self.screen_width = 800
        self.screen_height = 800
        self.bg_color = (20, 10, 70)

        # Ship settings.
        self.ship_speed = 0.4
