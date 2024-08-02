import pygame
import math
from enum import Enum
# Initialize pygame instance
pygame.init()

# Set pygame window
WIDTH, HEIGHT = 1000, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # PI game surface aka window
pygame.display.set_caption('Planet Simulation')  # Window title

FONT = pygame.font.SysFont("comicsans", 16)  # Create font
FONT2 = pygame.font.SysFont("comicsans", 24)  # Create font

# TODO: Add a add planet button (by order)
# TODO: Add a remove planet button (by order)
# TODO: Add a speed slider
# TODO: Add a side navigation


class Color(Enum):
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLUE = (100, 149, 237)
    RED = (188, 39, 50)
    DARK_GRAY = (80, 78, 81)


class Planet:
    # Class variables
    # Austronomical Units (AU) (Distance from sun converted to meters)
    AU = 149.6e6 * 1000
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
        x = (self.x * self.SCALE + WIDTH / 2) + 300
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) >= 2:
            updated_points = []
            for point in self.orbit:
                point_x, point_y = point
                point_x = (point_x * self.SCALE + WIDTH / 2) + 300
                point_y = point_y * self.SCALE + HEIGHT / 2
                updated_points.append((point_x, point_y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        # Draw planet on screen
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(
                # Create text object
                f'{round(self.distance_to_sun/1000, 1)}km', True, Color.WHITE.value)
            win.blit(distance_text, (x - distance_text.get_width()/2,
                     y - distance_text.get_height()/2))  # Render text on screen

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0

        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

class SideBar:
    def __init__(self, x, y, width, height, color) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
    def draw(self, win):
        x = self.x
        y = self.y + HEIGHT / 2
        
        pygame.draw.rect(win, self.color, (x, y, self.width, self.height))

# Game loop


def main():
    run = True
    clock = pygame.time.Clock()  # Create clock instance (help with synchronization)

    sidebar = SideBar(16, 0, WIDTH/3, HEIGHT * 2/3, Color.WHITE.value)
    
    sun = Planet(0, 0, 30, Color.YELLOW.value, 1.989 * 10**30, True)
    earth = Planet(-1 * Planet.AU, 0, 16,
                   Color.BLUE.value, 5.972 * 10**24, False)
    earth.y_vel = 29.8 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12,
                  Color.RED.value, 6.39 * 10**23, False)
    mars.y_vel = 24.1 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8,
                     Color.DARK_GRAY.value, 3.30 * 10**23, False)
    mercury.y_vel = -47.9 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14,
                   Color.WHITE.value, 4.8685 * 10**24, False)
    venus.y_vel = -35.0 * 1000

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)  # Set frame rate (update)
        WIN.fill((0, 0, 0))

        title = FONT2.render('Planet Simulation', True,
                             Color.WHITE.value)  # Create text object
        # Render text on screen
        WIN.blit(title, ((WIDTH - title.get_width())/2, 16))

        # Get events (e.g. keyboard, mouse, etc.)
        for event in pygame.event.get():
            # Close event
            if event.type == pygame.QUIT:
                run = False

        sidebar.draw(WIN)
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()  # Quit out application


if __name__ == "__main__":
    main()
