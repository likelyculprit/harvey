class Stats:
    '''Track stats for the game.'''

    def __init__(self, harvey):
        '''Init stats.'''
        self.settings = harvey.settings
        self.reset_stats()
        # Start game inactive until player presses button.
        self.game_active = 0

    def reset_stats(self):
        '''Reset stats to initial state.'''
        self.specks_left = self.settings.specks_left
