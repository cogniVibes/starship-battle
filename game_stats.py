import json

class GameStats:
    """Track statistics for Alien Invasion"""


    def __init__(self, ai_game) -> None:
        """Initialize settings"""
        self.settings = ai_game.settings
        self.reset_stats()
        # Start game in an inactive state
        self.game_active = False
        self.difficulty_chosen = False
        self.number_aliens = 0
        self.ammo_used = 0

        # High score should never be reset.
        self.high_score = self.get_saved_high_score()

    def get_saved_high_score(self) -> int:
        """Gets high score from file, if it exists."""
        try:
            with open('assets/high_score.json','r') as f:
                return json.load(f)
        except FileNotFoundError:
            with open('assets/high_score.json','w') as f:
                json.dump({'easy':0, 'medium':0, 'hard':0},f)
                return {'easy':0, 'medium':0, 'hard':0}


    def reset_stats(self) -> None:
        """Initialize settings that can change during the game"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    
    def initialize_ammo(self) -> None:
        self.ammo = self.number_aliens + 25


    def used_ammo(self) -> None:
        self.ammo_used +=1  