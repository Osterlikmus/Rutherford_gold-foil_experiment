
import pygame

BLACK = (0, 0, 0)

class Partikkel(pygame.sprite.Sprite):
    def __init__(self, color, radius):
        super().__init__()
        self.color = color
        self.radius = radius

        self.image = pygame.Surface([2*radius, 2*radius])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = pygame.draw.circle(self.image, color, [radius, radius], radius)