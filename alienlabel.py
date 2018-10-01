import pygame
from pygame.sprite import Sprite

class AlienLabel(Sprite):
    def __init__(self,x,y):

        self.x = int(x)
        self.y = int(y)


    def initialize_images(self,ai_settings,screen,alien_image,alien_points):
        self.screen = screen
        #create image
        self.image = pygame.sprite.Sprite()
        self.image.image = pygame.image.load(alien_image)
        self.image_rect = self.image.image.get_rect().move(self.x,self.y)

        #create text label
        font = pygame.font.SysFont("monospace",35)
        font_color = ai_settings.text_color
        font_background = ai_settings.bg_color
        title = ' = ' + str(alien_points) + ' points'
        self.text = font.render(title, True, font_color, font_background)
        self.text_rect = self.text.get_rect()
        self.text_rect.left, self.text_rect.top = self.image_rect.right, self.image_rect.top+5

    def update(self):
        #draw player to screen
        self.screen.blit(self.image.image, self.image_rect)
        #draw text to screen
        self.screen.blit(self.text, self.text_rect)
