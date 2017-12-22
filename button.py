import pygame.font

class Button():

    def __init__(self, ai_settings, screen, msg):
        """ Initiate button attributes """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Set button size and other attributes
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        # Create an object for a button and make it center
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # Button caption only needed to be created once
        self.prep_msg(msg)
    
    def prep_msg(self, msg):
        """ Render the msg to a picture and make it center on the button """
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        # Draw a button filled with color then draw the text
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
