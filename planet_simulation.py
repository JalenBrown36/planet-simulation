import pygame
from planet import Planet
from button import Button

# Initialize pygame instance
pygame.init()

# Set up pygame window
WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Game window
pygame.display.set_caption('Planet Simulation')  # Window title

# Define colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GRAY = (80, 78, 81)
BROWN = (139, 69, 19)  
GOLD = (255, 215, 0)  
CYAN = (0, 255, 255)  

RADIUS_SCALE = .0001  # Scale factor for planet radius
# List of planet specifications
PLANETS_ORDER = [
    # Name, x-position (AU), size (radius in km), color, mass (kg), velocity (m/s), isSun
    ('Sun', 0.0, 1398200, YELLOW, 1.989e30, 0, True),
    ('Mercury', 0.387, 4880, DARK_GRAY, 3.301e23, -47.9 * 1000, False),
    ('Venus', 0.723, 12104, YELLOW, 4.867e24, -35.0 * 1000, False),
    ('Earth', 1.0, 12742, BLUE, 5.972e24, 29.8 * 1000, False),
    ('Mars', 1.524, 6779, RED, 6.417e23, 24.1 * 1000, False),
    ('Jupiter', 5.203, 139820, BROWN, 1.898e27, 13.1 * 1000, False),
    ('Saturn', 9.537, 116460, GOLD, 5.683e26, 9.7 * 1000, False), 
    ('Uranus', 19.191, 50724, CYAN, 8.681e25, 6.8 * 1000, False),  
    ('Neptune', 30.070, 49244, BLUE, 1.024e26, 5.4 * 1000, False)
]

# Index to keep track of the next planet to add
planet_index = 0

def add_planet(planets):
    """Add the next planet in the PLANETS_ORDER list to the planets list."""
    global planet_index
    if planet_index < len(PLANETS_ORDER):
        planet_data = PLANETS_ORDER[planet_index]
        name, x, size, color, mass, velocity, isSun = planet_data
        
        # Create and append the new planet
        new_planet = Planet(x * Planet.AU, 0, size * RADIUS_SCALE, color, mass, isSun)
        new_planet.y_vel = velocity
        planets.append(new_planet)
        
        # Move to the next planet in the list
        planet_index += 1
    else:
        print("No more planets to add.")

def remove_planet(planets):
    """Remove the last planet from the planets list, ensuring the Sun remains."""
    global planet_index
    if planet_index > 1:
        planets.pop()
        planet_index -= 1

        # Decrement the planet count
        Planet._planet_count -= 1

        # Recalculate the scale based on the new planet count
        Planet.SCALE = Planet._initial_scale * (1 / (Planet._planet_count ** .9))
    else: 
        print("Cannot remove the sun.")

def main():
    """Main game loop."""
    run = True
    clock = pygame.time.Clock()  # Clock instance for frame rate control

    planets = []  # List to hold planets
    add_planet(planets)

    # Create buttons
    add_button = Button(20, 20, 160, 40, "Add Planet", lambda: add_planet(planets))
    remove_button = Button(20, 70, 160, 40, "Remove Planet", lambda: remove_planet(planets))

    while run:
        # Frame rate control
        clock.tick(60)
        
        # Fill the screen with black
        WIN.fill((0, 0, 0))

        # Draw the title
        title_font = pygame.font.SysFont("comicsans", 24)
        title = title_font.render('Planet Simulation', True, WHITE)
        WIN.blit(title, (WIDTH / 2 - title.get_width() / 2, 16))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Update button states
            add_button.update(event)
            remove_button.update(event)
        
        # Draw buttons
        add_button.draw(WIN)
        remove_button.draw(WIN)

        # Update and draw planets
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        # Update the display
        pygame.display.update()

    # Quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()