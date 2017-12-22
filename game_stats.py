class GameStats():
    """ Tract the game statistic info """
    
    def __init__(self, ai_settings):
        """ Initiate statistic info """
        self.ai_settings = ai_settings
        self.reset_stats()
        # Deactive the game when it starts
        self.game_active = False
        
        # Never reset highest score
        self.high_score = 0
    
        
    def reset_stats(self):
        """ Initiate statistic info that may be changed during the game running """
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        
    
