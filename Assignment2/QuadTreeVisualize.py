from pygame import display, surface
from pygame.constants import MOUSEBUTTONDOWN, MOUSEMOTION
from pygame.draw import rect

from utils.quadtree.quadtree import QuadTree
from utils.shapes.Rect import Rect
from utils.shapes.point import Point

import random
import pygame

white = (255,255,255)
green = (0,255,0)

class QuadTreeVisualize:
    def __init__(self):
        self._running = True
        self.display_size = self.w, self.h = 600, 600
        self.surface = pygame.display.set_mode(self.display_size)
        self.rect = Rect(Point(0,0), self.surface.get_rect().width, self.surface.get_rect().height)

        # setup timer
        self.delta_time = 0
        self.internal_clock = 0
        self.last_frame_tick = 0
        self.point_spawn_clock = 0
        self.point_spawn_rate = 100

        # visualize insert
        self.ncount = 600
        self.i = 0


    def on_init(self):
        pygame.init()

        self.mouserect = Rect(Point(0,0), 200, 150)
        self.qtree = QuadTree(self.rect, 5)

        self.last_frame_tick = pygame.time.get_ticks()
        self.last_update_tick = pygame.time.get_ticks()
        self._running = True

        #generate n points
        while self.i < self.ncount:
            centerx, centery = self.rect.to_pygame_rect().center
            randomx = int(random.gauss(mu=centerx, sigma=75))
            randomy = int(random.gauss(mu=centery, sigma=75))

            self.qtree.insert(None, Point(randomx, randomy))
            self.i += 1

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN and event.unicode == '+':
            pt = Point(random.randint(0, self.display_size[0]), random.randint(0, self.display_size[1]))
            self.qtree.insert(None, pt)
        if event.type == pygame.KEYDOWN and event.unicode == 'q':
            print('Count=%d' % len(self.mypoints))
            for p in self.mypoints:
                print(p)
        if event.type == MOUSEBUTTONDOWN:
            pt = Point(*(event.pos))
            self.qtree.insert(None, pt)
        if event.type == MOUSEMOTION:
            self.mouserect.set_origin(Point(*(event.pos)))
        

    def on_loop(self):
        nc = pygame.time.get_ticks()
        self.delta_time = (nc - self.last_frame_tick) / 1000.0
        self.last_frame_tick = nc 

        self.mypoints = self.qtree.query(self.mouserect)

    def on_render(self):
        self.surface.fill((0,0,0))
        self.qtree.draw(self.surface)
        self.mouserect.draw(self.surface, green)
        for p in self.mypoints:
            pygame.draw.circle(self.surface, green, (p.x,p.y), 3)
        display.flip()

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
if __name__ == "__main__" :
    theApp = QuadTreeVisualize()
    theApp.on_execute()