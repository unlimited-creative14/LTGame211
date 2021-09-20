from utils.shapes.shape import Circle, Point
import pygame

white = (255,255,255)

class Particle:
    def  __init__(self, pos: Point):
        self.pos = pos
        self.r = 6
        self.rect = Circle(pos, self.r)
    def move(self):
        self.pos.x += random.gauss(0, 1)
        self.pos.y += random.gauss(0, 1)
    def draw(self, surface:pygame.Surface, colorc = white):
        self.pos.draw(surface, color = colorc, rad=self.r)
    def is_collision(self, other_particle):
        if self.pos.get_sqr_distance(other_particle.pos) < self.r**2:
            return True
        
    
