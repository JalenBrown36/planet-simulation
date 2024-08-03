import pygame
from button import Button

class SideBar:
    def __init__(self, x, y, width, height, color) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
    def draw(self, win, func):
        screen_width, screen_height = win.get_size() 
        x = self.x * (screen_width / self.width)
        y = self.y - self.height / 2
        
        # pygame.draw.rect(win, self.color, (x, y, screen_width / 3, screen_height * 2 / 3))
        