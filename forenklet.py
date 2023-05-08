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

# Class
class Particle:
    # Konstanter for simulasjonen (Coulombs konstant)
    k_e = 8.99e9
    
    # Scaling
    dimension = 1e-13
    SCALE_X = DISPLAY_X / dimension
    SCALE_Y = DISPLAY_Y / dimension
    # TIMESTEP = 10e-21

    # Initiation of class properties
    def __init__(self, x, y, radius, mass, charge, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.charge = charge
        self.color = color
        
        # Acceleration
        self.x_acc = 0
        self.y_acc = 0

        # Velocity
        self.x_vel = 0
        self.y_vel = 0

    # Force method
    def force(self, other):
        distance = math.sqrt(self.x ** 2 + self.y ** 2)
        force_x = self.k_e * self.charge * other.charge * self.x / distance ** 3
        force_y = self.k_e * self.charge * other.charge * self.y / distance ** 3
        return force_x, force_y
    
    # Update position method
    def update_position(self, other):
        # Force
        force_x, force_y = self.force(other)

        # Acceleration
        self.x_acc = force_x / self.mass
        self.y_acc = force_y / self.mass

        # Velocity
        self.x_vel += self.x_acc
        self.y_vel += self.y_acc

        # Position
        self.x += self.x_vel
        self.y += self.y_vel
    
    # Draw method
    def draw(self, display):
        x = self.x * self.SCALE_X + DISPLAY_X / 2
        y = self.y * self.SCALE_Y + DISPLAY_Y / 2
        pygame.draw.circle(display, self.color, (x, y), self.radius)

# Main function
def main():
    running = True
    clock = pygame.time.Clock()

    gold = Particle(0, 0, 10, 0, 1.26e-17, GOLD)
    alfa = Particle(0, 1e-13/3, 5, 6.64e-27, 3.20e-19, WHITE)
    alfa.y_vel = -1.5e7
    particles = [gold, alfa]

    while(running):
        # Updating of display
        DISPLAY.fill(BLACK)
        for particle in particles:
            particle.draw(DISPLAY)
        alfa.update_position(gold)
        pygame.display.update()
        clock.tick(1)

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False
    pygame.quit()
main()