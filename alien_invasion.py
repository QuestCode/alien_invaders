import sys
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
from button import  Button
from scoreboard import Scoreboard
import game_functions as gf
import pygame
from pygame.sprite import Group

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    # gf.present_game(ai_settings,screen)

    # Make the Play Button.
    play_button = Button(ai_settings,screen,"Play")

    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)

    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings,screen)
    # Make a group to store bullets in.
    bullets = Group()
    alien_bullets = Group()
    aliens = Group()

    # Create fleet of aliens.
    gf.create_fleet(ai_settings,screen,ship,aliens,stats.level)

    # start loop for game.
    while True:
        # watch for keyboard and mouse events.
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,alien_bullets)
        if stats.game_active:
            ship.update()
            gf.attack_ship(ai_settings,screen,aliens,alien_bullets)
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets,alien_bullets)
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets,alien_bullets)
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,alien_bullets,play_button)

run_game()
