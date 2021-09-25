import math
import time
import pygame
import random
from utils.transform import Point2D
class P2AI:
    def __init__(self, player, ball):
        self.player = player
        self.ball = ball
        self.state = "stand"
        self.watch_range = 500

        self.ret_point = Point2D(player.transform.position.x, player.transform.position.y)

        # -1 : move left, 0 : don't move, 1: moveright
        self.moving = 0

    def form_vector(self, p1, p2):
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        return (dx, dy)

    def distance(self, p1, p2):
        dx = p1.x - p2.x
        dy = p1.y - p2.y
        return math.sqrt(dx**2 + dy**2)

    def run(self):
        wating = False
        while True:
            if self.ball.transform.position.y == 640 and not wating:
                time.sleep(.5)
                wating = True
            if self.distance(self.player.transform.position, self.ball.transform.position) < self.player.radius:
                self.hit()
                wating = False
            elif self.player.transform.position.x - self.ball.transform.position.x > 0 :
                self.move_left()
            elif self.player.transform.position.x - self.ball.transform.position.x < 0 :
                self.move_right()
            time.sleep(0.2)

    def move_left(self):
        if self.moving == -1:
            return
        elif self.moving == 1:
            # stop moving right
            event = pygame.event.Event(pygame.KEYUP, {
            'key':pygame.K_SEMICOLON
            })
            pygame.event.post(event)
        # moving left
        event = pygame.event.Event(pygame.KEYDOWN, {
            'key':pygame.K_k
            })
        pygame.event.post(event)
        self.moving = -1
    
    def move_right(self):
        if self.moving == 1:
            return
        elif self.moving == -1:
            # stop moving left
            event = pygame.event.Event(pygame.KEYUP, {
            'key':pygame.K_k
            })
            pygame.event.post(event)
        # moving left
        event = pygame.event.Event(pygame.KEYDOWN, {
            'key':pygame.K_SEMICOLON
            })
        pygame.event.post(event)
        self.moving = 1

    # def run1(self):
    #     while True:
    #         if self.distance(self.player.transform.position, self.ball.transform.position) < self.player.radius:
    #             self.hit()
    #             self.state = "return"

    #         elif self.state != "return" and self.distance(self.player.transform.position, self.ball.transform.position) < self.watch_range and self.ball.velocity.y > 0:
    #             self.state = "follow"
            
    #         if self.state == "follow":
    #             vec = self.form_vector(self.player.transform.position, self.ball.transform.position)
    #             allow_range = 10
    #             if vec[0] > allow_range:
    #                 mx = 1
    #             elif vec[0] < -allow_range:
    #                 mx = -1 
    #             else:
    #                 mx = 0

    #             if vec[1] > allow_range:
    #                 my = 1
    #             elif vec[1] < -allow_range:
    #                 my = -1
    #             else:
    #                 my = 0

    #             self.move((mx, my))
    #         if self.state == "return":
    #             if self.distance(self.player.transform.position, self.ret_point) < 10:
    #                 self.state = "stand"
    #             vec = self.form_vector(self.player.transform.position, self.ret_point)
    #             mx = 1 if vec[0] > 0 else -1
    #             my = 1 if vec[0] > 0 else -1

    #             self.move((mx, my))
               
    #         time.sleep(0.2)

    # def move(self, direction):
    #     movedown = pygame.event.Event(768, {
    #         'key':pygame.K_l
    #     })
    #     moveup = pygame.event.Event(768, {
    #         'key':pygame.K_o
    #     })
    #     moveleft = pygame.event.Event(768, {
    #         'key':pygame.K_k
    #     })
    #     moveright = pygame.event.Event(768, {
    #         'key':pygame.K_SEMICOLON
    #     })
        
    #     if direction[0] == -1:
    #         pygame.event.post(moveleft)
    #     elif direction[0] == 1:
    #         pygame.event.post(moveright)
        
    #     if direction[1] == -1:
    #         pygame.event.post(moveup)
    #     elif direction[1] == 1:
    #         pygame.event.post(movedown)

    def hit(self):
        pygame.event.post(pygame.event.Event(768, {
            'key' : pygame.K_j
        }))
