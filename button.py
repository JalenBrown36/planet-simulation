import pygame

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (100, 100, 100)
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont("comicsans", 20)
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        win.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) / 2,
                                self.rect.y + (self.rect.height - text_surface.get_height()) / 2))
    
    def click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.click(event.pos)