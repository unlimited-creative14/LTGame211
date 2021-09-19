from .shape import Shape
from .point import Point
import pygame

white = (255,255,255)
class Rect(Shape):
    def __init__(self, point: Point, w, h):
        self.origin = Point(point.x, point.y)
        self.w = w
        self.h = h
    def set_origin(self, point):
        self.origin = point
    def get_tl(self):
        return Rect(self.origin, self.w/2, self.h/2)
    def get_tr(self):
        return Rect(self.origin.move(self.w/2, 0), self.w/2, self.h/2)    
    def get_bl(self):
        return Rect(self.origin.move(0, self.h/2), self.w/2, self.h/2)  
    def get_br(self):
        return Rect(self.origin.move(self.w/2, self.h/2), self.w/2, self.h/2)  
    def contains(self, point):
        if(self.origin.x < point.x and point.x < self.origin.x + self.w):
            return self.origin.y < point.y and point.y < self.origin.y + self.h
        return False

    def is_overlap(self, rect):
        if self.origin.x > rect.origin.x + rect.w or rect.origin.x > self.origin.x + self.w:
            return False
        if self.origin.y > rect.origin.y + rect.h or rect.origin.y > self.origin.y + self.h:
            return False
        return True

    def __str__(self) -> str:
        return 'Rect(%s,w=%d,h=%d)' % (str(self.origin), self.w, self.h)

    # pygame draw
    def to_pygame_rect(self):
        return pygame.Rect(self.origin.x, self.origin.y, self.w, self.h)
    
    def draw(self, surface, color = white):
        pygame.draw.rect(surface, color, self.to_pygame_rect(), width=1)