import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """One class used to manage the ship's bullets"""
    
    def __init__(self, ai_settings, screen, ship):
        """Create a new bullet object at the ship's position"""
        super().__init__()
        self.screen = screen
        
        # Create a rectangle at (0, 0) then reset its right position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        # Store the float position of the bullet
        self.y = float(self.rect.y)
        
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
        
    def update(self):
        """Move the bullet up"""
        # Update the float number of the bullet's position
        self.y -= self.speed_factor
        # Update the float number of the bullet's rect position
        self.rect.y = self.y
        
    def draw_bullet(self):
        """Draw a bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
