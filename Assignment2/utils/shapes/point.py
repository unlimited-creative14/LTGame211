from .shape import *
from pygame import draw

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
