# Libraries and modules
import pygame
import math
import matplotlib.pyplot as plt

# Initiation of pygame
pygame.init()

# Definition of display
DISPLAY_X, DISPLAY_Y = 800, 800
DISPLAY = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))
CAPTION = pygame.display.set_caption("Ernest Rutherford sitt gullfolie-eksperiment")
FONT = pygame.font.SysFont("comicsans", 16)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD  = (255, 215, 0)

# Scaling
DIMENSION = 1.0e-12
SCALE_X = DISPLAY_X / DIMENSION
SCALE_Y = DISPLAY_Y / DIMENSION

# Timestep
TIMESTEP = 1.0e-22

# Coulombs konstant
COULOMBS_KONSTANT = 8.99e9

# Class
class Particle:
    # Initiation of class attributes
    def __init__(self, x_pos, y_pos, x_vel, radius, mass, charge, color):
        # Position
        self.x_pos = x_pos
        self.y_pos = y_pos
        
        # Velocity
        self.x_vel = x_vel
        self.y_vel = 0

        # Acceleration
        self.x_acc = 0
        self.y_acc = 0

        self.radius = radius
        self.mass = mass
        self.charge = charge
        self.color = color
        self.trail = []
        self.minimum_distance_from_gold = abs(x_pos)

    # Method for calculating the force
    def force(self, other):
        distance = math.sqrt(self.x_pos ** 2 + self.y_pos ** 2)
        if distance < self.minimum_distance_from_gold:
            self.minimum_distance_from_gold = distance
        force_x = COULOMBS_KONSTANT * self.charge * other.charge * self.x_pos / distance ** 3
        force_y = COULOMBS_KONSTANT * self.charge * other.charge * self.y_pos / distance ** 3
        return force_x, force_y
    
    # Method to update the position of the alfa particles
    def updatePosition(self, other):
        # Force
        force_x, force_y = self.force(other)

        # Acceleration
        self.x_acc = force_x / self.mass
        self.y_acc = force_y / self.mass

        # Velocity
        self.x_vel += self.x_acc * TIMESTEP
        self.y_vel += self.y_acc * TIMESTEP

        # Position
        self.x_pos += self.x_vel * TIMESTEP
        self.y_pos += self.y_vel * TIMESTEP

        # Append position to trail
        self.trail.append((self.x_pos, self.y_pos))
    
    # Draw method
    def draw(self, display):
        x = self.x_pos * SCALE_X + DISPLAY_X / 2
        y = self.y_pos * SCALE_Y + DISPLAY_Y / 2
        pygame.draw.circle(display, self.color, (x, y), self.radius)
        
        trail = []
        if len(self.trail) >= 2:
            for point in self.trail:
                x, y = point
                x = x * SCALE_X + DISPLAY_X / 2
                y = y * SCALE_Y + DISPLAY_Y / 2
                trail.append((x, y))
            pygame.draw.lines(display, self.color, False, trail, 2)

    # Method for checking if the alfa particle is inside of the display
    def insideDisplay(self):
        if(self.x_pos < -DIMENSION / 2 or self.x_pos > DIMENSION / 2 or self.y_pos < -250 / SCALE_X or self.y_pos > DIMENSION / 2):
            return False
        else:
            return True

    # Beregning av spredningsvinkel
    def spredningsVinkel(self):
        theta = abs(int(math.atan(self.y_vel/self.x_vel) * 180 / math.pi))
        if(self.x_vel < 0):
            theta = 180 - theta
        return theta

    # Beregning av støtparameter
    def teoretiskStøtparameter(self, other, alfa_startvelocity_x):
        velocity = math.sqrt(self.x_vel**2 + self.y_vel**2)
        cos_theta = self.x_vel / velocity
        try:
            teoretisk_støtparameter = int(COULOMBS_KONSTANT * self.charge * other.charge / (self.mass * alfa_startvelocity_x ** 2) * math.sqrt((1 + cos_theta) / (1 - cos_theta)) * 10e15)
        except:
            teoretisk_støtparameter = None
        return teoretisk_støtparameter

    # Updating the display
    def updateDisplay(self, other, alfa_startposition_y):
        DISPLAY.blit(FONT.render(f"Startavstand i y-retning fra kjernen: {abs(int(alfa_startposition_y * 10e15))} fm", 1, WHITE), (10, 10))
        DISPLAY.blit(FONT.render(f"Spredningsvinkel: {self.spredningsVinkel()}°", 1, WHITE), (10, 40))
        DISPLAY.blit(FONT.render(f"Teoretisk støtparameter: {self.teoretiskStøtparameter(other, 1.5e7)} fm", 1, WHITE), (10, 70))
        DISPLAY.blit(FONT.render(f"Minste avstand fra kjernen: {int(self.minimum_distance_from_gold * 10e15)} fm", 1, WHITE), (10, 100))

def pygame_simulation():
    running = True
    clock = pygame.time.Clock()

    # Generating the gold particle and defining startvalues
    gold_particle = Particle(0, 0, 0, 5, 0, 1.26e-17, GOLD)
    particles = [gold_particle, None]
    alfa_startposition_y = 0
     
    while(running):
        # Generating the alfaparticle
        alfa_particle = Particle(-5e-13, alfa_startposition_y, 1.5e7, 1, 6.64e-27, 3.20e-19, WHITE)
        particles[1] = alfa_particle
        
        # Startdisplay
        DISPLAY.fill(BLACK)
        for particle in particles:
            particle.draw(DISPLAY)
        alfa_particle.updateDisplay(gold_particle, alfa_startposition_y)
        pygame.display.update()
        clock.tick(60)
        
        # Code for changing the y-position to the alfa particle
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_UP]):
            if(alfa_particle.insideDisplay()):
                alfa_startposition_y -= 0.025e-13
            else:
                alfa_startposition_y += 0.025e-13
        if(keys[pygame.K_DOWN]):
            if(alfa_particle.insideDisplay()):
                alfa_startposition_y += 0.025e-13
            else:
                alfa_startposition_y -= 0.025e-13

        # Start of simulation
        if(keys[pygame.K_SPACE]):
            while(alfa_particle.insideDisplay()):
                DISPLAY.fill(BLACK)
                for particle in particles:
                    particle.draw(DISPLAY)
                alfa_particle.updateDisplay(gold_particle, alfa_startposition_y)
                alfa_particle.updatePosition(gold_particle)
                pygame.display.update()
                clock.tick(200)

                for event in pygame.event.get():
                    if(event.type == pygame.QUIT):
                        alfa_particle.insideDisplay() = False
        
            # Restarting the simulation
            running_2 = True
            while(running_2):
                DISPLAY.fill(BLACK)
                for particle in particles:
                    particle.draw(DISPLAY)
                alfa_particle.updateDisplay(gold_particle, alfa_startposition_y)
                DISPLAY.blit(FONT.render(f"Trykk på [r] for å nullstille simulasjonen", 1, WHITE), (DISPLAY_X / 4, DISPLAY_Y / 2))
                pygame.display.update()
                if(keys[pygame.K_r]):
                    running_2 = False
                for event in pygame.event.get():
                    if(event.type == pygame.QUIT):
                        running = False
            
            alfa_startposition_y = 0
        
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False         
    pygame.quit()

# Main function
def main():
    pygame_simulation()
main()
