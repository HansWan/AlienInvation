import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Initiate the ship and set its initial position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings;
        
        # Load the ship picture and get its bounding rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # Set each new ship at the center of screen bottom
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Store float number at the ship attribute center
        self.center = float(self.rect.centerx)
        
        # Moving flag
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Move the ship according to the moving flag"""
        # Update the ship's center, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        
        # Change the rect according to the self.center
        self.rect.centerx = self.center
        
    def blitme(self):
        """Draw the ship at a designated position"""
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """ Put the new ship in the cneter of the screen """
        self.center = self.screen_rect.centerx
