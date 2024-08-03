import pygame

class Button:
    def __init__(self, x, y, width, height, text, action):
        """
        Initialize a button with position, size, text, and action.
        """
        self.rect = pygame.Rect(x, y, width, height)  # Rectangle representing the button's area
        self.color = (100, 100, 100)  # Default button color (gray)
        self.text = text  # Button text
        self.action = action  # Action to be called when the button is clicked
        self.font = pygame.font.SysFont("comicsans", 20)  # Font for button text

    def draw(self, win):
        """
        Draw the button on the provided window surface.
        """
        # Draw the button's background
        pygame.draw.rect(win, self.color, self.rect)
        
        # Render and center the button's text
        text_surface = self.font.render(self.text, True, (255, 255, 255))  # Render the text in white
        text_rect = text_surface.get_rect(center=self.rect.center)  # Center text within the button
        win.blit(text_surface, text_rect.topleft)  # Draw the text on the window

    def click(self, pos):
        """
        Check if the button was clicked based on the given position.
        """
        if self.rect.collidepoint(pos):
            self.action()  # Call the button's action if the position is within the button

    def update(self, event):
        """
        Update the button based on the given event.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse button click
            self.click(event.pos)  # Process click if it occurred within the button's area