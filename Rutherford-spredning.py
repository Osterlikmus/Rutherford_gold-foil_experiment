
# Libraries and modules
import pygame
import math

# Initiation of pygame
pygame.init()

# Definition of display
DISPLAY_X, DISPLAY_Y = 800, 800
DISPLAY = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))
CAPTION = pygame.display.set_caption("Ernest Rutherford sitt gullfolie-eksperiment")

# Colors
BLACK = (0, 0, 0)
GOLD  = (255, 215, 0)
WHITE = (255, 255, 255)

# Gunnar Colors
BROWN = (150, 75, 0)
PURPLE = (160, 32, 240)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 140, 0)
BLUE = (0, 0, 255)

# Class
class Particle:
    # Konstanter for simulasjonen (Coulombs konstant)
    COULOMBS_KONSTANT = 8.99e9
    
    # Scaling
    DIMENSION = 1.0e-12
    SCALE_X = DISPLAY_X / DIMENSION
    SCALE_Y = DISPLAY_Y / DIMENSION

    # Timestep
    TIMESTEP = 1.0e-22

    # Initiation of class properties
    def __init__(self, x_pos, y_pos, radius, mass, charge, color):
        # Position
        self.x_pos = x_pos
        self.y_pos = y_pos
        
        # Velocity
        self.x_vel = 0
        self.y_vel = 0

        # Acceleration
        self.x_acc = 0
        self.y_acc = 0

        self.radius = radius
        self.mass = mass
        self.charge = charge
        self.color = color
        self.trail = []

    # Force method
    def force(self, other):
        distance = math.sqrt(self.x_pos ** 2 + self.y_pos ** 2)
        force_x = self.COULOMBS_KONSTANT * self.charge * other.charge * self.x_pos / distance ** 3
        force_y = self.COULOMBS_KONSTANT * self.charge * other.charge * self.y_pos / distance ** 3
        return force_x, force_y
    
    # Update position method
    def update_position(self, other):
        # Force
        force_x, force_y = self.force(other)

        # Acceleration
        self.x_acc = force_x / self.mass
        self.y_acc = force_y / self.mass

        # Velocity
        self.x_vel += self.x_acc * self.TIMESTEP
        self.y_vel += self.y_acc * self.TIMESTEP

        # Position
        self.x_pos += self.x_vel * self.TIMESTEP
        self.y_pos += self.y_vel * self.TIMESTEP

        # Append position to trail
        self.trail.append((self.x_pos, self.y_pos))
    
    # Draw method
    def draw(self, display):
        x = self.x_pos * self.SCALE_X + DISPLAY_X / 2
        y = self.y_pos * self.SCALE_Y + DISPLAY_Y / 2
        pygame.draw.circle(display, self.color, (x, y), self.radius)
        
        trail = []
        if len(self.trail) >= 2:
            for point in self.trail:
                x, y = point
                x = x * self.SCALE_X + DISPLAY_X / 2
                y = y * self.SCALE_Y + DISPLAY_Y / 2
                trail.append((x, y))
            pygame.draw.lines(display, self.color, False, trail, 2)

# Helping function
def insideDisplay(alfa):
    if(alfa.x_pos < -alfa.DIMENSION / 2 or alfa.x_pos > alfa.DIMENSION / 2 or alfa.y_pos < -alfa.DIMENSION / 2 or alfa.y_pos > alfa.DIMENSION / 2):
        return False
    else:
        return True

# Main function
def main():
    running = True
    clock = pygame.time.Clock()

    gold = Particle(0, 0, 5, 0, 1.26e-17, GOLD)
    alfa_startpos = [-4e-13, -2e-13, -1e-13, -0.5e-13, -0.2e-13, -0.1e-13]
    alfa_color = [BLUE, ORANGE, GREEN, RED, PURPLE, BROWN]
    
    while(running):
        #trail_to_scale = []
        for index in range(len(alfa_startpos)):
            alfa = Particle(-5e-13, alfa_startpos[index], 1, 6.64e-27, 3.20e-19, alfa_color[index])
            alfa.x_vel = 1.5e7
            particles = [gold, alfa]
        
            while(insideDisplay(alfa)):
                # Updating of display
                DISPLAY.fill(BLACK)
                for particle in particles:
                    particle.draw(DISPLAY)
                alfa.update_position(gold)
                pygame.display.update()
                clock.tick(600)

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False
    pygame.quit()
main()