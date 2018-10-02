import pygame
from pygame.sprite import Sprite

class Bunker(Sprite):
    def __init__(self,ai_settings,screen):
        super(Bunker,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.hits = 4

        # Load the ship image and get its rect
        self.image = pygame.image.load(ai_settings.bunker_image)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image,self.rect)

    def update(self):
        self.hits -= 1
