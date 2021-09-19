from utils.shapes.Rect import Rect
from utils.shapes.point import Point
import pygame
from pygame import display

from utils.quadtree.quadtree import QuadTree
from utils.quadtree.objects import *

white = (255,255,255)
green = (0,255,0)

class QuadTreeCollisionVisualize:
    def __init__(self):
        self._running = True
        self.display_size = self.w, self.h = 600, 600
        self.surface = pygame.display.set_mode(self.display_size)
        self.rect = Rect(Point(0,0), self.surface.get_rect().width, self.surface.get_rect().height)

        # setup timer
        self.delta_time = 0
        self.internal_clock = 0
        self.last_frame_tick = 0
        
        self.move_clock = 0
        self.move_rate = 60
        # visualize insert
        self.ncount = 1000

    def on_init(self):
        pygame.init()
        self.particles = []

        for i in range(self.ncount):
            pos = Point(random.uniform(0, self.w), random.uniform(0, self.h))
            self.particles.append(Particle(pos))
        self.collision_method = self.method1

        self.last_frame_tick = pygame.time.get_ticks()
        self.last_update_tick = pygame.time.get_ticks()
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN and event.unicode == '1':
            self.collision_method = self.method1
        if event.type == pygame.KEYDOWN and event.unicode == '2':
            self.collision_method = self.method2

    def on_loop(self):
        nc = pygame.time.get_ticks()
        self.delta_time = (nc - self.last_frame_tick) / 1000.0
        self.last_frame_tick = nc         
        
        if self.move_clock < (1/self.move_rate):
            self.move_clock += self.delta_time
        else:
            self.move_clock = 0
            for particle in self.particles:
                particle.move()


    def on_render(self):
        self.surface.fill((0,0,0))

        colors = {}
        for particle in self.particles:
            colors[particle] = white

        self.collision_method(colors)         
                
        for particle in colors.keys():
            particle.draw(self.surface, colors[particle])


        display.flip()

    def method1(self, colors:dict):
        for particle in self.particles:
            for other_particle in self.particles:
                if particle is not other_particle and particle.is_collision(other_particle):
                    colors[particle] = green
                    break      

    def method2(self, colors:dict):
        qtree = QuadTree(self.rect, 8)
        for particle in self.particles:
            collisions = qtree.insert_and_get_collisions(particle, particle.pos)
            if not len(collisions) == 0:
                colors[particle] = green
                for collision in collisions:
                    colors[collision] = green
            
    def method3(self, colors:dict):
        qtree = QuadTree(self.rect, 8)
        for particle in self.particles:
            qtree.insert(particle, particle.pos)

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
    theApp = QuadTreeCollisionVisualize()
    theApp.on_execute()