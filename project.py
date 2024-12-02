import pygame
import numpy as np
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 1000
HEIGHT = 800
G = 6.67430e-11  # Universal gravitational constant
SCALE = 1e9      # Scale factor for visualization
TIME_STEP = 100  # Simulation time step in seconds

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.scale = width / (max_val - min_val)
        self.value = initial
        self.dragging = False
        
        # Calculate initial position of slider button
        self.button_x = x + (initial - min_val) * self.scale
        self.button_rect = pygame.Rect(self.button_x - 5, y - 5, 10, height + 10)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = event.pos[0]
            self.button_x = max(self.rect.left, min(self.rect.right, mouse_x))
            self.button_rect.centerx = self.button_x
            self.value = self.min_val + (self.button_x - self.rect.left) / self.scale
    
    def draw(self, screen):
        # Draw slider bar
        pygame.draw.rect(screen, GRAY, self.rect)
        # Draw slider button
        pygame.draw.rect(screen, RED, self.button_rect)

class TwoBodySystem:
    def __init__(self, M, m, initial_distance):
        self.M = M  # Primary mass
        self.m = m  # Secondary mass
        self.reduced_mass = (M * m)/(M + m)
        self.K = G * M * m
        
        # Initial positions
        self.r1 = np.array([-m * initial_distance / (M + m), 0.0])
        self.r2 = np.array([M * initial_distance / (M + m), 0.0])
        
        # Calculate initial velocity for circular orbit
        v = math.sqrt(G * (M + m) / initial_distance)
        self.v1 = np.array([0.0, v * m/(M + m)])
        self.v2 = np.array([0.0, -v * M/(M + m)])
        
        self.history1 = []
        self.history2 = []
    
    def calculate_force(self):
        r = self.r2 - self.r1
        r_mag = np.linalg.norm(r)
        F = self.K * r / (r_mag**3)
        return F
    
    def calculate_energy(self):
        v_rel = self.v2 - self.v1
        T = 0.5 * self.reduced_mass * np.dot(v_rel, v_rel)
        r = np.linalg.norm(self.r2 - self.r1)
        V = -self.K / r
        return T + V
    
    def update(self, dt):
        F = self.calculate_force()
        
        self.v1 += F * dt / self.M
        self.v2 -= F * dt / self.m
        
        self.r1 += self.v1 * dt
        self.r2 += self.v2 * dt
        
        screen_pos1 = (int(self.r1[0]/SCALE + WIDTH/2), 
                      int(self.r1[1]/SCALE + HEIGHT/2))
        screen_pos2 = (int(self.r2[0]/SCALE + WIDTH/2), 
                      int(self.r2[1]/SCALE + HEIGHT/2))
        
        self.history1.append(screen_pos1)
        self.history2.append(screen_pos2)
        
        if len(self.history1) > 100:
            self.history1.pop(0)
            self.history2.pop(0)
    
    def draw(self, screen):
        if len(self.history1) > 1:
            pygame.draw.lines(screen, YELLOW, False, self.history1, 1)
            pygame.draw.lines(screen, BLUE, False, self.history2, 1)
        
        pos1 = (int(self.r1[0]/SCALE + WIDTH/2), int(self.r1[1]/SCALE + HEIGHT/2))
        pos2 = (int(self.r2[0]/SCALE + WIDTH/2), int(self.r2[1]/SCALE + HEIGHT/2))
        
        radius1 = int(math.log10(self.M) * 1.5)
        radius2 = int(math.log10(self.m) * 1.5)
        
        pygame.draw.circle(screen, YELLOW, pos1, radius1)
        pygame.draw.circle(screen, BLUE, pos2, radius2)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two-Body Gravitational System")
clock = pygame.time.Clock()

# Initialize system
M_sun = 1.989e30  # Mass of Sun in kg
M_earth = 5.972e24  # Mass of Earth in kg
initial_distance = 1.496e11  # Average Sun-Earth distance in meters

# Create slider for distance
distance_slider = Slider(50, 50, 200, 20, 1e11, 3e11, initial_distance)
system = TwoBodySystem(M_sun, M_earth, distance_slider.value)

# Font for text
font = pygame.font.Font(None, 36)

running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Reset simulation
                system = TwoBodySystem(M_sun, M_earth, distance_slider.value)
            elif event.key == pygame.K_SPACE:  # Pause/unpause
                paused = not paused
        
        # Handle slider events
        distance_slider.handle_event(event)
    
    # Update system if not paused
    if not paused:
        system.update(TIME_STEP)
    
    # Clear screen
    screen.fill(BLACK)
    
    # Draw system
    system.draw(screen)
    
    # Draw slider and labels
    distance_slider.draw(screen)
    distance_text = font.render(f"Distance: {distance_slider.value:.2e} m", True, WHITE)
    screen.blit(distance_text, (270, 50))
    
    # Display total energy
    energy = system.calculate_energy()
    energy_text = font.render(f"Energy: {energy:.2e} J", True, WHITE)
    screen.blit(energy_text, (10, 10))
    
    # Display controls
    controls_text = font.render("R: Reset  Space: Pause", True, WHITE)
    screen.blit(controls_text, (10, HEIGHT - 30))
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
