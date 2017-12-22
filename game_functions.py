import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Monitor key press DOWN"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

    # Press I to double the bullet width
    elif event.key == pygame.K_i:
        ai_settings.bullet_width *= 2
    elif event.key == pygame.K_k:
        ai_settings.bullet_width /= 2

    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """Monitor key press UP"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
            
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # Monitor keyboard and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)                
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """ Start a new game when a player presses the play button """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings to default
        ai_settings.initialize_dynamic_settings()
        
        # High the mouse icon
        pygame.mouse.set_visible(False)
        
        # Reset the game statistic info
        stats.reset_stats()
        stats.game_active = True
        
        # Reset score picture
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        # Empty the alien fleet and bullets
        aliens.empty()
        bullets.empty()
        
        # Create a new alien fleet and put the ship at the center bottom of screen
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
            
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Update pictures on the screen and show the new screen"""
    # Re-draw the screen in each loop
    screen.fill(ai_settings.bg_color)
    
    # Re-draw all bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    # Show score
    sb.show_score()
    
    # If the game is deactivated, draw the play button
    if not stats.game_active :
        play_button.draw_button()
    
    # Enable the new screen visible
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update bullets position and remove disappered bullets"""
    # Update bullets position
    bullets.update()
    
    # Remove disappeared bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):    
    # Check if any bullet hits an alien
    # if yes, remove corresponding bullet and alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        # Remove current bullets and create a new alien fleet
        bullets.empty()
        ai_settings.increase_speed()
        
        # Increase level
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)
    
def fire_bullet(ai_settings, screen, ship, bullets):
    """If bullets number below limit, fir a new bullet"""
    # Create a new bullet and put it into the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        for i in range(5):
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)
            i += 1
        
def get_number_aliens_x(ai_settings, alien_width):
    """ Calculate how many aliens can be displayed on one line """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """ Calculate how many rows can be displayed on one column """
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ Create an alien and put it on the current line """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width* alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    

def create_fleet(ai_settings, screen, ship, aliens):
    """ Create the alien fleet """
    # Create an alien and calculate how many aliens can be displayed on one line
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    # Create alien fleet
    for row_number in range (number_rows):
        for alien_number in range (number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
            
def check_fleet_edges(ai_settings, aliens):
    """ Take actions when an alien reaches the screen edges """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """ Move the alien fleet down and change their direction """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
        
def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """ Respond to an alien hitting the ship """
    if stats.ships_left > 0:
        # Reduce Ships_left by 1
        stats.ships_left -= 1
        
        # Update scoreboard
        sb.prep_ships()
        
        # Empty the alien fleet and bullets
        aliens.empty()
        bullets.empty()
        
        # Create a new alien fleet and put the ship at the center bottom of screen
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
        # Suspend
        sleep(0.5)
    
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        
def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """ Check if any alien meets the screen bottom """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat it as the ship is hit
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Check if any alien is on the edge of screen and update all aliens' position in the alien fleet """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # Check if any alien hits the ship
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    
    # Check if any alien meets the screen bottom    
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
    
def check_high_score(stats, sb):
    """ Check if a new score record occurred """
    if stats.score > stats.high_score:
            stats.high_score = stats.score
            sb.prep_high_score()
    
    
    
    
    
    
    
    
