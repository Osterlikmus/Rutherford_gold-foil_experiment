
# Modules
import pygame
from partikkel import Partikkel
from pylab import array, norm

# Initiation of pygame
pygame.init()

# Definition of display
display_x = 900
display_y = 500
display = pygame.display.set_mode([display_x, display_y])
caption = pygame.display.set_caption("Ernest Rutherford sitt gullfolie-eksperiment")

# Colors
WHITE = (255, 255, 255)
GOLD  = (255, 224, 145)
BLACK = (0, 0, 0)

# Partikler
alfa_color = WHITE
alfa_radius = 5
alfapartikkel = Partikkel(alfa_color, alfa_radius)
gull_color = GOLD
gull_radius = 10
gullpartikkel = Partikkel(gull_color, gull_radius)
spritelist = pygame.sprite.Group(alfapartikkel, gullpartikkel)
#spritelist.add(alfapartikkel, gullpartikkel)

# Konstanter for simulasjonen
m = 6.64e-27    # massen av alfapartikkelen, kg
q1 = 3.20e-19   # ladningen til alfapartikkelen, C
q2 = 1.26e-17   # ladningen til gullkjernen, C
k_e = 8.99e9    # Coulombs konstant

# Startverdier for partiklene
gull_position = array([(display_x/2)-gull_radius, (display_y/5)-gull_radius])
gullpartikkel.rect.x = gull_position[0]
gullpartikkel.rect.y = gull_position[1]

alfa_position = array([(display_x/2)+2*alfa_radius, (display_y/1.2)-alfa_radius])
alfa_velocity = array([0, -1])

# Beregning av kraftsum og akselerasjon
def Alfa_akselerasjon(alfa_position):
    elektrisk_kraft_abs = (k_e*q1*q2)/(norm(alfa_position)**2)
    retningsvektor = alfa_position/norm(alfa_position)
    elektrisk_kraft = elektrisk_kraft_abs*retningsvektor
    alfa_akselerasjon = elektrisk_kraft/m
    return alfa_akselerasjon

# Simulation
clock = pygame.time.Clock()
FPS = 100

running = True
while(running):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
    
    # Movement of particles
    alfapartikkel.rect.x = alfa_position[0]
    alfapartikkel.rect.y = alfa_position[1] 
    alfa_akselerasjon = Alfa_akselerasjon(alfa_position)
    alfa_velocity = alfa_velocity + alfa_akselerasjon
    alfa_position = alfa_position + alfa_velocity

    # Updating of display
    display.fill(BLACK)
    spritelist.draw(display)
    pygame.display.flip()
    clock.tick(FPS)