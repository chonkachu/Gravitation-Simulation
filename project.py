import pygame
import math

pygame.init()

# Window and simulation constants
WIDTH = 1920      # Screen width in pixels
HEIGHT = 1080     # Screen height in pixels
G = 6.67430e-11  # Universal gravitational constant in m³/kg/s²
SCALE = 1e9      # Scale factor to convert from meters to pixels
TIME_STEP = 100000  # Time step for simulation in seconds
M_sun = 1.989e30    # Sun mass in kg

# Define colors in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)    # Sun color
BLUE = (0, 0, 255)      # Earth color
GREEN = (0, 255, 0)       # Orbit path color
RED = (255, 0, 0)         # Mercury color
PINK = (255, 192, 203)    # Venus color
ORANGE = (255, 165, 0)    # Mars color
BEIGE = (245, 222, 179)   # Jupiter color

def calculate_k(mass):
    return M_sun * mass * G

def calculate_angular_momentum(r_0, K, mass, eccentricity):
    return math.sqrt((eccentricity + 1) * (K * mass * r_0))

def calculate_mechanical_energy(r_0, r_max, K):
    return -K/(r_0+r_max)

def to_screen_coords(r, theta):
    x = r * math.cos(theta) / SCALE + WIDTH/2
    y = r * math.sin(theta) / SCALE + HEIGHT/2
    return (int(x), int(y))

class Planet:
    def __init__(self, name, mass, perihelion, aphelion, eccentricity, color):
        self.name = name
        self.mass = mass
        self.r_0 = perihelion * 1000  # Convert km to m
        self.r_max = aphelion * 1000  # Convert km to m
        self.K = calculate_k(mass)
        self.e = eccentricity
        self.L = calculate_angular_momentum(self.r_0, self.K, self.mass, self.e)
        self.theta = 0.0
        self.history = []
        self.color = color
        self.orbit_period = 2 * math.pi * math.sqrt(((self.r_0 + self.r_max)/2)**3 / (G * M_sun))
        self.angular_velocity = 2 * math.pi / self.orbit_period
        self.mech_energy = calculate_mechanical_energy(self.r_0, self.r_max, self.K)
        
    def get_position(self):
        r = (self.L**2)/(self.K*self.mass) * (1/(1 + self.e*math.cos(self.theta)))
        return r, self.theta
    
    def update(self, dt):
        dtheta = self.angular_velocity * dt
        self.theta += dtheta
        self.theta = self.theta % (2 * math.pi)
        
        r, theta = self.get_position()
        screen_pos = to_screen_coords(r, theta)
        
        self.history.append(screen_pos)
        if len(self.history) > 50:
            self.history.pop(0)
    
    def draw(self, screen):
        if len(self.history) > 1:
            pygame.draw.lines(screen, self.color, False, self.history, 1)
        
        r, theta = self.get_position()
        planet_pos = to_screen_coords(r, theta)
        pygame.draw.circle(screen, self.color, planet_pos, 10)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")
clock = pygame.time.Clock()

# Initialize planets
planets = [
    Planet("Mercurio", 0.330e24, 46e6, 69.8e6, 0.206, RED),
    Planet("Venus", 4.87e24, 107.5e6, 108.9e6, 0.007, PINK),
    Planet("Terra", 5.97e24, 147.1e6, 152.1e6, 0.017, BLUE),
    Planet("Marte", 0.642e24, 206.7e6, 249.3e6, 0.094, ORANGE),
    Planet("Jupiter", 1898e24, 740.6e6, 816.4e6, 0.049, BEIGE)
]

selected_planet = None

# Main simulation loop
running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_UP:
                TIME_STEP *= 1.1
            elif event.key == pygame.K_DOWN:
                TIME_STEP /= 1.1
            # Handle number keys 1-5
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                selected_planet = planets[event.key - pygame.K_1]
    
    if not paused:
        for planet in planets:
            planet.update(TIME_STEP)
    
    screen.fill(BLACK)
    
    pygame.draw.circle(screen, YELLOW, (WIDTH//2, HEIGHT//2), 20)
    
    for planet in planets:
        planet.draw(screen)
    
    # Draw information
    font = pygame.font.Font(None, 36)
    info_text = [
        f"Time Step: {TIME_STEP/86400:.1f} dias",
        "Espaço: Pausa  Up/Down: Aumenta Timestep",
        "Pressione 1-5 para ver dados de um planeta:",
        "1: Mercurio, 2: Venus, 3: Terra, 4: Marte, 5: Jupiter"
    ]
    
    # Add selected planet information
    if selected_planet:
        info_text.insert(1, f"{selected_planet.name} Periodo Orbital: {selected_planet.orbit_period/86400:.1f} dias")
        info_text.insert(2, f"Momentum angular: {selected_planet.L:.2e} kgm^2/s")
        info_text.insert(3, f"Energia Mecanica: {selected_planet.mech_energy:.2e} J")
    
    for i, text in enumerate(info_text):
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (10, 10 + i*40))
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
