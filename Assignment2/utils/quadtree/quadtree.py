from utils.shapes.shape import Shape
import pygame
from utils.shapes.shape import Rect

class QuadTree:
    def __init__(self, boundary: Rect, cap):
        self.rect = boundary
        self.capacity = cap
        self.items = []
        self._divided = False

    def _sub_divide(self):
        self._tl = QuadTree(self.rect.get_tl(), self.capacity)
        self._tr = QuadTree(self.rect.get_tr(), self.capacity)
        self._bl = QuadTree(self.rect.get_bl(), self.capacity)
        self._br = QuadTree(self.rect.get_br(), self.capacity)
    
    def get_rect(self):
        return self.rect

    def insert(self, obj, pos):
        if not self.rect.contains(pos):
            return False

        if len(self.items) < self.capacity:
            self.items.append(pos)
            return True
        else:
            if not self._divided:
                self._sub_divide()
                self._divided = True
        
            return self._tl.insert(obj, pos) or self._tr.insert(obj, pos) or self._bl.insert(obj, pos) or self._br.insert(obj, pos)
    def insert_and_get_collisions(self, obj, pos):
        collisions = []
        if not self.rect.contains(pos):
            return []

        for particle in self.items:
            if obj.is_collision(particle):
                collisions.append(particle)
        if len(self.items) < self.capacity:
            self.items.append(obj)
        else:
            if not self._divided:
                self._sub_divide()
                self._divided = True
            collisions.extend(self._tl.insert_and_get_collisions(obj, pos))
            collisions.extend(self._tr.insert_and_get_collisions(obj, pos))
            collisions.extend(self._bl.insert_and_get_collisions(obj, pos))
            collisions.extend(self._br.insert_and_get_collisions(obj, pos))

        return collisions

    def remove(self, pos):
        """Not implemented yet"""
        pass

    def query(self, rect:Shape):
        """Find all points lie in this rect"""
        if not self.rect.is_overlap(rect):
            return []

        # if specify rect fully contains this self.rect
        # no need to check if specify rect contains all points inside (speed up a little bit)
        if rect.contains(self.rect):
            found = self.items.copy()
        else:
            found = list(filter(lambda p : rect.contains(p), self.items))
        if self._divided:
            found.extend(self._tl.query(rect))
            found.extend(self._tr.query(rect))
            found.extend(self._bl.query(rect))
            found.extend(self._br.query(rect))
        return found
            

    # pygame display
    def draw(self, surface):
        for point in self.items:
            point.draw(surface)
        if self._divided:
            # draw divider here
            top = (self.rect.origin.x + self.rect.w/2, self.rect.origin.y)
            bot = (self.rect.origin.x + self.rect.w/2, self.rect.origin.y + self.rect.h)
            left = (self.rect.origin.x, self.rect.origin.y + self.rect.h/2)
            right = (self.rect.origin.x + self.rect.w, self.rect.origin.y + self.rect.h/2)
            pygame.draw.line(surface, (255,255,255), top, bot, 1)
            pygame.draw.line(surface, (255,255,255), left, right, 1)

            self._tl.draw(surface)
            self._bl.draw(surface)
            self._tr.draw(surface)
            self._br.draw(surface)
            
