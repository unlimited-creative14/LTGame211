from abc import ABC, abstractmethod
import pygame
from pygame import draw

white = (255,255,255)
green = (0,255,0)

class Point:
    def __init__(self, x, y, data=None):
        self.x = x
        self.y = y
        self.data = data

    def move(self, dx = 0, dy = 0):
        return Point(self.x + dx, self.y + dy)
    def get_sqr_distance(self, other_point):
        return (self.x - other_point.x)**2 + (self.y - other_point.y)**2

    def __eq__(self, o: object) -> bool:
        return o.x == self.x and o.y == self.y
    def __str__(self) -> str:
        return "x="+str(self.x)+", y="+str(self.y)
    def draw(self, surface, color = white, rad = 1):
        draw.circle(surface, color, (self.x, self.y), rad)


class Shape(ABC):
    @abstractmethod
    def contains(self, shape_object):
        """Check if this shape contains specify shape_object"""
    
    @abstractmethod
    def is_overlap(self, shape):
        """Check if this shape overlap another shape"""

    
    @abstractmethod
    def draw(self, shape):
        """Draw this shape using pygame draw engine"""


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
    def contains(self, shape_object):
        if isinstance(shape_object, Point):
            point = shape_object
            if(self.origin.x < point.x and point.x < self.origin.x + self.w):
                return self.origin.y < point.y and point.y < self.origin.y + self.h
            return False
        if isinstance(shape_object, Rect):
            rect = shape_object
            if not self.contains(rect.origin):
                return False
            p2 = rect.origin.move(rect.w, rect.h)
            if not self.contains(p2):
                return False
            return True
        raise NotImplementedError()


    def is_overlap(self, shape):
        if isinstance(shape, Rect):
            rect = shape
            if self.origin.x > rect.origin.x + rect.w or rect.origin.x > self.origin.x + self.w:
                return False
            if self.origin.y > rect.origin.y + rect.h or rect.origin.y > self.origin.y + self.h:
                return False
            return True
        if isinstance(shape, Circle):
            return shape.is_overlap(self)

    def __str__(self) -> str:
        return 'Rect(%s,w=%d,h=%d)' % (str(self.origin), self.w, self.h)

    # pygame draw
    def to_pygame_rect(self):
        return pygame.Rect(self.origin.x, self.origin.y, self.w, self.h)
    
    def draw(self, surface, color = white):
        pygame.draw.rect(surface, color, self.to_pygame_rect(), width=1)

class Circle(Shape):
    def __init__(self, center : Point, rad):
        self.center = center
        self.rad = rad
    def contains(self, shape_object):
        if isinstance(shape_object, Point):
            point = shape_object
            return point.get_sqr_distance(self.center) <= self.rad**2
        if isinstance(shape_object, Rect):
            rect = shape_object
            return self.contains(rect.origin) and self.contains(rect.origin.move(rect.w, rect.h))
        raise NotImplementedError
    def is_overlap(self, shape):
        if isinstance(shape, Circle):
            return self.center.get_sqr_distance(shape.center) <= (self.rad + shape.rad)**2
        if isinstance(shape, Rect):
            # https://www.geeksforgeeks.org/check-if-any-point-overlaps-the-given-circle-and-rectangle/
            
            p1 = shape.origin
            p2 = p1.move(shape.w, shape.h)
            # Find nearest point on the Rect to the center of circle
            pn = Point(max(p1.x, min(self.center.x, p2.x)), max(p1.y, min(self.center.y, p2.y)))
            # Check whether this point is in or outside the circle
            return self.contains(pn)
    def draw(self, surface, color = white):
        draw.circle(surface, color, (self.center.x, self.center.y), self.rad)
