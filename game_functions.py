import sys
import pygame
import random
from bullet import Bullet
from bullet import  AlienBullet
from alien import Alien
from alien import RedAlien
from alien import YellowAlien
from bunker import Bunker
from time import sleep
from button import Button
from alienlabel import AlienLabel
from pygame.sprite import Group


def present_game(ai_settings,screen):
    screen.fill(ai_settings.bg_color)
    font = ai_settings.winner_font
    msg = font.render(ai_settings.game_title, True, ai_settings.text_color)
    msgRect = msg.get_rect()
    msgRect.centerx = int(ai_settings.screen_width/2)
    msgRect.top = int(ai_settings.screen_height/6)
    screen.blit(msg, msgRect)
    pygame.display.update()
    display_score_card(ai_settings,screen)
    play_button = Button(ai_settings,screen,"Start the Game")
    play_button.draw_button()

def display_score_card(ai_settings,screen):
    green_alien = AlienLabel(ai_settings.screen_width/3,ai_settings.screen_height/3)
    green_alien.initialize_images(ai_settings,screen,ai_settings.green_alien_image,ai_settings.green_alien_points)


    yellow_alien = AlienLabel(ai_settings.screen_width/3,ai_settings.screen_height/3 + 50)
    yellow_alien.initialize_images(ai_settings,screen,ai_settings.yellow_alien_image,ai_settings.yellow_alien_points)

    red_alien = AlienLabel(ai_settings.screen_width/3,ai_settings.screen_height/3 + 100)
    red_alien.initialize_images(ai_settings,screen,ai_settings.red_alien_image,ai_settings.red_alien_points)
    green_alien.update()
    yellow_alien.update()
    red_alien.update()

def check_events(ai_settings,screen,stats,sb,play_button,ship,red_aliens,yellow_aliens,green_aliens,bunkers,bullets,alien_bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,red_aliens,yellow_aliens,green_aliens,bunkers,bullets,mouse_x,mouse_y)

def update_screen(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens,bunkers,bullets,alien_bullets,play_button):
    """Update images on the screen and flip to the new screen."""
    screen.fill(ai_settings.bg_color)

    #Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for bullet in alien_bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()

    bunkers.draw(screen)
    red_aliens.draw(screen)
    yellow_aliens.draw(screen)
    green_aliens.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        present_game(ai_settings,screen)

    # Make the most recently drawn sceeen visible.
    pygame.display.flip()

def check_keydown_events(event,ai_settings,screen,ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move the ship to the right
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_bullets(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens,bunkers,bullets,alien_bullets):
    """Update position of the bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    alien_bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # Get rid of bullets that have disappeared.
    screen_rect = screen.get_rect()
    for bullet in alien_bullets.copy():
        if bullet.rect.top >= screen_rect.height:
            alien_bullets.remove(bullet)

    check_bullet_bunker_collisions(ai_settings,screen,bunkers,bullets,alien_bullets)
    check_ship_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens,bullets)
    check_alien_bullet_ship_collision(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens,bullets,alien_bullets)

def update_bunkers(ai_settings,screen,bunkers):
    bunkers.update()

def check_bullet_bunker_collisions(ai_settings,screen,bunkers,bullets,alien_bullets):
    bunker_collisions(ai_settings,bunkers,bullets,alien_bullets)

def bunker_collisions(ai_settings,bunkers,bullets,alien_bullets):
    bullet_coll = pygame.sprite.groupcollide(bullets,bunkers,True,True)
    alien_bullet_coll = pygame.sprite.groupcollide(alien_bullets,bunkers,True,True)

    if bullet_coll:
        print('coll')
        # for bunkers in bullet_coll.values():


def alien_collision(sb,stats,bullets,aliens,alien_points):
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)

    if collisions:
        for aliens in collisions.values():
            stats.score += alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)

def check_ship_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens,bullets):
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.

    ai_settings.lose_level = False

    # Red Alien Collisions
    alien_collision(sb,stats,bullets,red_aliens,ai_settings.red_alien_points)
    # Yellow Alien Collisions
    alien_collision(sb,stats,bullets,yellow_aliens,ai_settings.yellow_alien_points)
    # Green Alien Collisions
    alien_collision(sb,stats,bullets,green_aliens,ai_settings.green_alien_points)

    if len(red_aliens) == 0 and len(yellow_aliens) == 0 and len(green_aliens) == 0 and ai_settings.lose_level == False:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        reset_level(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens)


def check_alien_bullet_ship_collision(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens,bullets,alien_bullets):
    """Respond to ship being hit by alien bullet."""
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    collisions = pygame.sprite.spritecollideany(ship,alien_bullets)

    if collisions:
        if stats.ships_left > 0:
            # Decrement ships_left
            stats.ships_left -= 1

            # Update scoreboard.
            sb.prep_ships()

            bullets.empty()
            alien_bullets.empty()

            # Create a new fleet and center the ship.
            ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            stats.game_active = False
            pygame.mouse.set_visible(True)

        # aliens = [red_aliens,yellow_aliens,green_aliens]
        ai_settings.lose_level = True
        if len(red_aliens) == 0 and len(yellow_aliens) == 0 and len(green_aliens) == 0:
            # Empty the list of aliens and bullets.
            aliens.empty()
            reset_level(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens)


def fire_bullet(ai_settings,screen,ship,bullets):
    """Fire a bullet if limit is not reached yet."""
    if len(bullets) < ai_settings.ship_bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def alien_fire_bullet(ai_settings,screen,red_aliens,yellow_aliens,green_aliens,alien_bullets):
    # Randomly choose an alien to fire a bullet at the ship
    row = random.randint(0,2)
    if row == 0:
        alien_fire_action(ai_settings,screen,red_aliens,alien_bullets)
    elif row == 1:
        alien_fire_action(ai_settings,screen,yellow_aliens,alien_bullets)
    else:
        alien_fire_action(ai_settings,screen,green_aliens,alien_bullets)

def alien_fire_action(ai_settings,screen,aliens,alien_bullets):
    if len(aliens) > 0:
        index = random.randint(0,len(aliens)-1)
        alien = aliens.sprites()[index]
        if len(alien_bullets) < ai_settings.alien_bullets_allowed:
            new_bullet = AlienBullet(ai_settings,screen,alien)
            alien_bullets.add(new_bullet)

def attack_ship(ai_settings,screen,red_aliens,yellow_aliens,green_aliens,alien_bullets):
    # print(len(alien_bullets))
    if not len(alien_bullets) == ai_settings.alien_bullets_allowed:
        # fire alien bullet
        alien_fire_bullet(ai_settings,screen,red_aliens,yellow_aliens,green_aliens,alien_bullets)

def create_bunkers(ai_settings,screen,bunkers):
    bunker = Bunker(ai_settings,screen)
    number_bunkers = get_number_bunkers(ai_settings,bunker.rect.width)
    for bunker_number in range(number_bunkers):
        new_bunker = Bunker(ai_settings,screen)
        bunker_width = new_bunker.rect.width
        new_bunker.x = bunker_width + 2 * bunker_width * bunker_number
        new_bunker.rect.x = new_bunker.x
        new_bunker.rect.y = ai_settings.screen_height/2 + 100
        bunkers.add(new_bunker)

def get_number_bunkers(ai_settings, bunker_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * bunker_width
    return int(available_space_x / (2 * bunker_width))

def create_fleet(ai_settings,screen,ship,red_aliens,yellow_aliens,green_aliens,level):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings,screen,0)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    create_rectangle_fleet(ai_settings,screen,red_aliens,yellow_aliens,green_aliens,number_rows,number_aliens_x)


def create_rectangle_fleet(ai_settings,screen,red_aliens,yellow_aliens,green_aliens,number_rows,number_aliens_x):
    # Create the first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Create an alien and place it in the row.
            create_alien(ai_settings,screen,red_aliens,yellow_aliens,green_aliens,alien_number,row_number)



def create_alien(ai_settings,screen,red_aliens,yellow_aliens,green_aliens,alien_number,row_number):
    """Create an alien and place it in the row."""
    alien = None
    if row_number == 0:
        alien = RedAlien(ai_settings,screen,row_number)
    elif row_number == 1:
        alien = YellowAlien(ai_settings,screen,row_number)
    else:
        alien = Alien(ai_settings,screen,row_number)

    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number

    if row_number == 0:
        red_aliens.add(alien)
    elif row_number == 1:
        yellow_aliens.add(alien)
    else:
        green_aliens.add(alien)

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    return int(available_space_x / (2 * alien_width))

def get_number_rows(ai_settings,ship_height,alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    return int(available_space_y / (2 * alien_height))


def update_aliens(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens,bullets,alien_bullets):
    """Check if the fleet is at an edge, and then update the postions of all aliens in the fleet."""
    check_fleet_edges(ai_settings,green_aliens)
    check_fleet_edges(ai_settings,yellow_aliens)
    check_fleet_edges(ai_settings,red_aliens)
    green_aliens.update()
    yellow_aliens.update()
    red_aliens.update()

    ship_collision(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens,bullets,alien_bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens,bullets,alien_bullets)

def ship_collision(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens,bullets,alien_bullets):
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship,red_aliens):
        ship_hit_by_alien_ship(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens,bullets,alien_bullets)
    elif pygame.sprite.spritecollideany(ship,yellow_aliens):
        ship_hit_by_alien_ship(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens,bullets,alien_bullets)
    elif pygame.sprite.spritecollideany(ship,green_aliens):
        ship_hit_by_alien_ship(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens,bullets,alien_bullets)

def check_fleet_edges(ai_settings,aliens):
    """Respond appropriately if any aliens have reach an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit_by_alien_ship(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens,bullets,alien_bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        green_aliens.empty()
        yellow_aliens.empty()
        red_aliens.empty()
        bullets.empty()
        alien_bullets.empty()
        # Create a new fleet and center the ship.
        ship.center_ship()

        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def add_aliens(red_aliens,yellow_aliens,green_aliens):
    aliens = Group()
    for alien in red_aliens.sprites():
        aliens.add(alien)
    for alien in yellow_aliens.sprites():
        aliens.add(alien)
    for alien in green_aliens.sprites():
        aliens.add(alien)
    return aliens

def check_aliens_bottom(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens,bullets,alien_bullets):
    """Check if any aliens have reached the bottom of the screen."""
    aliens = add_aliens(red_aliens,yellow_aliens,green_aliens)
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit_by_alien_ship(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens,bullets,alien_bullets)
            break

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,red_aliens,yellow_aliens,green_aliens,bunkers,bullets,mouse_x,mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        green_aliens.empty()
        yellow_aliens.empty()
        red_aliens.empty()
        bullets.empty()
        bunkers.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings,screen,ship,red_aliens,yellow_aliens,green_aliens,stats.level)

        # Create bunkers
        create_bunkers(ai_settings,screen,bunkers)

        ship.center_ship()

def check_high_score(stats,sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def reset_level(ai_settings,screen,stats,sb,ship,red_aliens,yellow_aliens,green_aliens):
    sb.prep_level()
    create_fleet(ai_settings,screen,ship,red_aliens,yellow_aliens,green_aliens,stats.level)
    ai_settings.lose_level = False
