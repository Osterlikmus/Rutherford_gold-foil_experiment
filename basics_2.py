# Libraries and modules
import pygame
import math

# Initiation of pygame
pygame.init()

# Definition of display
display_x, display_y = 800, 800
DISPLAY = pygame.display.set_mode((display_x, display_y))
CAPTION = pygame.display.set_caption("Ernest Rutherford sitt gullfolie-eksperiment")

# Colors
BLACK = (0, 0, 0)
GOLD  = (255, 215, 0)
WHITE = (255, 255, 255)

# Class
class Particle:
    # Konstanter for simulasjonen (Coulombs konstant)
    k_e = 8.99e9
    
    #Scaling
    dimension = 1e-13
    SCALE = min(display_x, display_y) / dimension
    TIMESTEP = 10e-21

    # Initiation of class properties
    def __init__(self, x, y, radius, mass, charge, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.charge = charge
        self.color = color
        
        self.gold = False
        self.distance_to_gold_particle = 0
        
        # Acceleration
        self.x_acc = 0
        self.y_acc = 0

        # Velocity
        self.x_vel = 0
        self.y_vel = 0

    # Force method
    def force(self, other):
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.gold:
            self.distance_to_gold_particle = distance

        if distance == 0:
            return 0, 0
        else:
            force = self.k_e * self.charge * other.charge / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    # Update position method
    def update_position(self, particles):
        # Total force
        total_force_x = total_force_y = 0
        for particle in particles:
            if particle == self:
                continue
            
            fx, fy = self.force(particle)
            total_force_x += fx
            total_force_y += fy

        # Acceleration
        self.x_acc = total_force_x / self.mass
        self.y_acc = total_force_y / self.mass

        # Velocity
        self.x_vel += self.x_acc * #self.TIMESTEP
        self.y_vel += self.y_acc * #self.TIMESTEP

        # Position
        self.x += self.x_vel * #self.TIMESTEP
        self.y += self.y_vel * #self.TIMESTEP
    
    # Draw method
    def draw(self, display):
        x = self.x * self.SCALE + display_x / 2
        y = self.y * self.SCALE + display_y / 2
        pygame.draw.circle(display, self.color, (x, y), self.radius)

# Main function
def main():
    gold = Particle(0, 0, 30, 0, 1.26e-17, GOLD)
    gold.gold = True
    alfa = Particle(0, 1e-13/5, 10, 6.64e-27, 3.20e-19, WHITE)
    #alfa.y_vel = -1.419e7
    particles = [gold, alfa]

    clock = pygame.time.Clock()
    running = True
    while(running):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False
        
        # Updating of display
        DISPLAY.fill(BLACK)
        for particle in particles:
            particle.draw(DISPLAY)
        #alfa.update_position(particles)
        pygame.display.update()
        clock.tick(60) 
    pygame.quit()
main()