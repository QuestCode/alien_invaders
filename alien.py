import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self,ai_settings, screen):
        """Initialize the alien and set its starting postion."""
        super(Alien,self).__init__()
        self.health = 1
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/hands_up_invader_green.png')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image,self.rect)

    def update(self):
        """Move the alien right."""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien is at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


class RedAlien(Alien):

    def __init__(self,ai_settings, screen):
        """Initialize the alien and set its starting postion."""
        super().__init__(ai_settings, screen)
        self.image = pygame.image.load('images/king_invader_red.png')
        self.health = 3

class YellowAlien(Alien):

    def __init__(self,ai_settings, screen):
        """Initialize the alien and set its starting postion."""
        super().__init__(ai_settings, screen)
        self.image = pygame.image.load('images/hands_down_invader_yellow.png')
        self.health = 2
