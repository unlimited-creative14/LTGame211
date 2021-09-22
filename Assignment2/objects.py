import math
import pygame.time
from Assignment2.utils.collision import CircleCollier, BoxCollider
from Assignment2.utils.load_assets import load_img
from Assignment2.utils.transform import *


class Player:
    def __init__(self, surface, transform: Transform, r, idle_animate, hit_animate, side, scale=1):
        self.obj_type = "player" + str(side)
        self.scale = scale
        self._surface = surface
        self.transform = transform
        self.radius = r
        self.idle_animate = idle_animate
        self.hit_animate = hit_animate
        self.collider = CircleCollier(self.transform.position, self.radius, False)

        self.idles = []
        for i in range(0, 4):
            image, rect = load_img("character\\idle\\idle" + str(i + 1) + '.png')
            image = pygame.transform.rotate(image, self.transform.rotation)
            self.idles.append((image, rect))

        self.hits = []
        for i in range(0, 8):
            image, rect = load_img("character\\hit\\hit" + str(i + 1) + '.png')
            image = pygame.transform.rotate(image, self.transform.rotation)
            self.hits.append((image, rect))

        self.hit_index = 0
        self.idle_index = 0

        # bool check hitting animation
        self.is_hitting = False

        # time when hitting
        self.hit_tick = 0

    def move(self, delta_time, velocity: Point2D):
        self.transform.translate(velocity.x * delta_time, velocity.y * delta_time)

    def hit(self):
        self.hit_tick = pygame.time.get_ticks() / 1000
        self.is_hitting = True
        self.collider.enable = True

    def update(self, current_time):
        # hit animation index
        index = int((current_time - self.hit_tick) / self.hit_animate)
        if index > 7:
            self.is_hitting = False
            self.collider.enable = False
        else:
            self.hit_index = index

        # idle animation index
        self.idle_index = int(current_time / self.idle_animate) % 4

    def draw(self):
        if self.is_hitting:
            self._surface.blit(self.hits[self.hit_index][0],
                               self.hits[self.hit_index][1].move(self.transform.position.x - 128 * self.scale,
                                                                 self.transform.position.y - 128 * self.scale))
        else:
            self._surface.blit(self.idles[self.idle_index][0],
                               self.idles[self.idle_index][1].move(self.transform.position.x - 128 * self.scale,
                                                                   self.transform.position.y - 128 * self.scale))

    def on_collision(self, collider):
        pass


class Ball:
    def __init__(self, surface, transform: Transform, a=-0.3, scale=1, vmax=1):
        self.vmax = vmax
        self.obj_type = "ball"
        self.scale = scale
        self._surface = surface
        self.transform = transform
        self.idle, self.fly = load_img('ball\\ball.png'), load_img('ball\\ball_flying.png')
        self.is_flying = False
        self.velocity = Point2D(0, 0)
        self.a = a

        self.collider = CircleCollier(self.transform.position, 10)
        self.hitted = False
        self.hit_time = 0

    def update(self, delta_time):
        if self.hitted:
            self.hit_time += delta_time
            if self.hit_time > 0.5:
                self.hitted = False

        if abs(self.velocity.x) < 0.01 and abs(self.velocity.y) < 0.01:
            self.is_flying = False
        if self.is_flying:
            a_x, a_y = self.a * self.velocity.x * 2, self.a * self.velocity.y * 2
            self.velocity.x, self.velocity.y = self.velocity.x + a_x * delta_time, self.velocity.y + a_y * delta_time
            self.transform.translate(self.velocity.x, self.velocity.y)

    def draw(self):
        angle = 0 if self.velocity.y <= 0 else 180
        # calculate angle to rotate image
        if self.velocity.x != 0:
            angle = 270 - math.atan(self.velocity.y / self.velocity.x) * 180 / 3.1416 - (
                180 if self.velocity.x < 0 else 0)
        # draw image
        if self.is_flying:
            image = pygame.transform.rotate(self.fly[0], angle)
            self._surface.blit(image, self.fly[1].move(self.transform.position.x - 20 * self.scale,
                                                       self.transform.position.y - 20 * self.scale))
        else:
            image = pygame.transform.rotate(self.idle[0], angle)
            self._surface.blit(image, self.idle[1].move(self.transform.position.x - 20 * self.scale,
                                                        self.transform.position.y - 20 * self.scale))

    def on_collision(self, collider):
        if self.hitted:
            return
        self.hitted = True
        self.hit_time = 0

        # change direction

        # player 1 hit a ball
        if collider.obj_type == "player1":
            # if the ball is lower than the player 1
            if self.transform.position.y > collider.transform.position.y:
                x_value = self.vmax * (self.transform.position.x - collider.transform.position.x) / collider.radius
                y_value = math.sqrt(self.vmax ** 2 - x_value ** 2)
                self.velocity.x, self.velocity.y = x_value, y_value
                self.is_flying = True

        # player 2 hit a ball
        elif collider.obj_type == "player2":
            # if the ball is lower than the player 2
            if self.transform.position.y < collider.transform.position.y:
                x_value = self.vmax * (self.transform.position.x - collider.transform.position.x) / collider.radius
                y_value = -math.sqrt(self.vmax ** 2 - x_value ** 2)
                self.velocity.x, self.velocity.y = x_value, y_value
                self.is_flying = True

        # collision with the wall
        elif collider.obj_type == "wall":
            print("wall")
            self.velocity.x = -self.velocity.x

class Wall:
    def __init__(self, transform: Transform, width, height):
        self.transform = transform
        self.width = width
        self.height = height
        self.obj_type = "wall"
        self.collider = BoxCollider(transform.position, self.width, self.height)

    def on_collision(self, collider):
        pass
