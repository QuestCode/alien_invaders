import pygame

class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen Settings
        self.game_title = 'Alien Invasion'
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0,0,0)
        self.button_color = (0,0,0)
        self.text_color = (255,255,255)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15

        # Ship Bullet Settings
        self.ship_bullet_color = 60,60,60
        self.ship_bullets_allowed = 5

        # Alien settings
        self.fleet_drop_speed = 10
        self.alien_bullet_color = 153,0,153
        self.alien_bullets_allowed = 3

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.lose_level = False

        self.ship_image = 'images/png_images/ship.png'
        self.green_alien_image = 'images/hands_up_invader_green.png'
        self.yellow_alien_image = 'images/hands_down_invader_yellow.png'
        self.red_alien_image = 'images/king_invader_red.png'

        try:
            self.winner_font = pygame.font.Font("fonts/Megadeth.ttf", 70)
        except:
            self.winner_font = pygame.font.Font(None, 70)

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the games."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3

        self.alien_speed_factor = 1
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.green_alien_points = 50
        self.yellow_alien_points = 100
        self.red_alien_points = 200

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.green_alien_points = int(self.green_alien_points * self.score_scale)
        self.yellow_alien_points = int(self.yellow_alien_points * self.score_scale)
        self.red_alien_points = int(self.red_alien_points * self.score_scale)
        # print(self.alien_points)
