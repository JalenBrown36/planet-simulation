import pygame
import math
from enum import Enum
# Initialize pygame instance
pygame.init()

# Set pygame window
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # PI game surface aka window
pygame.display.set_caption('Planet Simulation')  # Window title


class Color(Enum):
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLUE = (100, 149, 237)
    RED = (188, 39, 50)
    DARK_GRAY = (80, 78, 81)


class Planet:
    # Class variables
    AU = 149.6e6 * 1000  # Austronomical Units (AU) (Distance from sun)
    G = 6.67428e-11  # Gravity constant
    SCALE = 150 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600*24  # 1 day (update time)

    def __init__(self, x: int, y: int, radius: int, color: tuple, mass: float, isSun: bool):
        # Set Planet properties relative to the sun
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []  # Store travel points (draw orbit)
        self.sun = isSun  # Check if sun
        self.distance_to_sun = 0  # Distance from sun

        # Set velocities for orbitting planet
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        # Draw planet on screen
        pygame.draw.circle(win, self.color, (x, y), self.radius)
        
    def attraction(self, other):
        other_x, other_y = other.x, other.y

# Game loop


def main():
    run = True
    clock = pygame.time.Clock()  # Create clock instance (help with synchronization)

    sun = Planet(0, 0, 30, Color.YELLOW.value, 1.989 * 10**30, True)
    earth = Planet(-1 * Planet.AU, 0, 16,
                   Color.BLUE.value, 5.972 * 10**24, False)
    mars = Planet(-1.524 * Planet.AU, 0, 12,
                  Color.RED.value, 6.39 * 10**23, False)
    mercury = Planet(0.387 * Planet.AU, 0, 8,
                     Color.DARK_GRAY.value, 3.30 * 10**23, False)
    venus = Planet(0.723 * Planet.AU, 0, 14,
                   Color.WHITE.value, 4.8685 * 10**24, False)

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)  # Set frame rate (update)

        # Get events (e.g. keyboard, mouse, etc.)
        for event in pygame.event.get():
            # Close event
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()  # Quit out application


if __name__ == "__main__":
    main()
