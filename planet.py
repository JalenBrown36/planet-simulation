import pygame
import math
from decimal import Decimal

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    TIMESTEP = 3600 * 24  # 1 day

    # Class variables
    _planet_count = 0  # Counter for the number of planets
    _initial_scale = 100 / AU  # Initial scale

    def __init__(self, x, y, radius, color, mass, isSun):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.sun = isSun
        self.distance_to_sun = 0
        self.orbit = []
        self.x_vel = 0
        self.y_vel = 0

        # Update the scale based on the number of planets
        Planet._planet_count += 1
        Planet.SCALE = Planet._initial_scale * (1 / (Planet._planet_count ** .9))  # Adjust SCALE

    def draw(self, win):
        # Compute the screen coordinates for the planet
        x = self.x * Planet.SCALE + win.get_width() / 2
        y = self.y * Planet.SCALE + win.get_height() / 2  

        # Draw the orbit if available
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                px, py = point
                px = px * Planet.SCALE + win.get_width() / 2
                py = py * Planet.SCALE + win.get_height() / 2
                updated_points.append((px, py))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        # Draw the planet itself
        pygame.draw.circle(win, self.color, (int(x), int(y)), int(self.radius / Planet._planet_count ** 2.98))

        # Display the distance from the Sun if it's not the Sun
        if not self.sun:
            FONT = pygame.font.SysFont("comicsans", 16)  # Create font
            distance_text = FONT.render(f"{'%.2E' % Decimal(self.distance_to_sun / 1000)} km", 1, (255, 255, 255))
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

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