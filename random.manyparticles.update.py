# Libraries and modules
import pygame
import math
import random
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
        self.distance = math.sqrt(self.x_pos ** 2 + self.y_pos ** 2)

    # Method for calculating the force
    def force(self, other):
        distance = math.sqrt(self.x_pos ** 2 + self.y_pos ** 2)
        if distance < self.distance:
            self.distance = distance
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
        if(self.x_pos < -DIMENSION / 2 or self.x_pos > DIMENSION / 2 or self.y_pos < -DIMENSION or self.y_pos > DIMENSION / 2):
            return False
        else:
            return True

    # Beregning av spredningsvinkel
    def spredningsVinkel(self):
        theta = abs(int(math.atan(self.y_vel/self.x_vel) * 180 / math.pi))
        if(self.x_vel < 0):
            theta = 180 - theta
        spredningsvinkel_font = FONT.render(f"Spredningsvinkel: {theta}°", 1, WHITE)
        return spredningsvinkel_font, theta

# Helping functions
def particlesInsideDisplay(particles):
    for particle in particles:
        if(particle.insideDisplay()):
            return True
        elif():
            


def pygame_simulation():
    running = True
    clock = pygame.time.Clock()

    # Startvalues
    gold_particle = Particle(0, 0, 0, 5, 0, 1.26e-17, GOLD)
    particles = [gold_particle]
    alfa_startposition_x = -5e-13
    alfa_startvelocity_x = 1.5e7
    
    # Matplotlib list setup
    alfa_antall = [0] * 181
    spredningvinkler = []
    for number in range(181):
        spredningvinkler.append(number)
    
    # The simulation
    while(running):
        # Alfa particles
        for _ in range(100):
            alfa_startposition_y = random.uniform(-3e-13, 5e-13)
            alfa_particle = Particle(alfa_startposition_x, alfa_startposition_y, alfa_startvelocity_x, 1, 6.64e-27, 3.20e-19, WHITE)
            particles.append(alfa_particle)
        
        # The simulation
        while(particlesInsideDisplay(particles)):
            DISPLAY.fill(BLACK)
            for particle in particles:
                particle.draw(DISPLAY)
                particle.updatePosition(gold_particle)
            pygame.display.update()
            clock.tick(600)
        
        for particle in particles:
            alfa_antall[particle.spredningsVinkel()[1]] += 1

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False
    pygame.quit()
    return spredningvinkler, alfa_antall

def matplotlib_graph(spredningsvinkler, alfa_antall):
    plt.plot(spredningsvinkler, alfa_antall)
    plt.title("Forholdet mellom antall utsendte alfapartikler og tilhørende spredningsvinkel", fontsize = 9)
    plt.xlabel("x: vinkel (θ)")
    plt.ylabel("y: antall")
    plt.xlim([0, 180])
    plt.ylim([0, 10])
    plt.show()

# Pygame Simulation
def main():
    spredningsvinkler, alfa_antall = pygame_simulation()
    matplotlib_graph(spredningsvinkler, alfa_antall)
main()
