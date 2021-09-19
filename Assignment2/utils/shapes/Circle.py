from shape import Shape
from point import Point

class Circle(Shape):
    def __init__(self, center : Point, rad):
        self.center = center
        self.rad = rad
    def contains(self, point:Point):
        return point.get_sqr_distance(self.center) < self.rad**2
    def is_overlap(self, shape):
        return
    