import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object at the ship's current postition."""
        super(Bullet,self).__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set correct postition.
        self.rect = pygame.Rect(0, 0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

        self.color = ai_settings.ship_bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rect postion.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen,self.color,self.rect)


class AlienBullet(Sprite):
    def __init__(self, ai_settings, screen, alien):
        """Create a bullet object at the ship's current postition."""
        super(AlienBullet,self).__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set correct postition.
        self.rect = pygame.Rect(0, 0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        self.color = ai_settings.alien_bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)



    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y += self.speed_factor
        # Update the rect postion.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen,self.color,self.rect)
