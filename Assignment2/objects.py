import math
import pygame.time
from utils.collision import CircleCollier, BoxCollider
from utils.load_assets import load_img
from utils.transform import *


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
            image, rect = load_img("character/idle/idle" + str(i + 1) + '.png')
            image = pygame.transform.rotate(image, self.transform.rotation)
            self.idles.append((image, rect))

        self.hits = []
        for i in range(0, 8):
            image, rect = load_img("character/hit/hit" + str(i + 1) + '.png')
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
    def __init__(self, surface, transform: Transform, a=-30, scale=1, vmax=400):
        self.vmax = vmax
        self.obj_type = "ball"
        self.scale = scale
        self._surface = surface
        self.transform = transform
        self.idle, self.fly, self.fire, self.swirl, self.fire_swirl = load_img('ball/ball.png'), load_img('ball/ball_flying.png'), load_img('ball/ball_firing.png'), load_img('ball/ball_swirl.png'),load_img('ball/ball_fire_swirl.png')
        self.is_flying = False
        self.velocity = Point2D(0.0001, 0.00001)
        self.a = a

        self.collider = CircleCollier(self.transform.position, 10)
        self.hitted = False
        self.hit_time = 0

        self.dead = False
        self.last_hit = ""

        self.firing = False
        self.item_time = 15

        self.swirling = False
        self.vx_swirling = 0

        # index 0 for speed up item
        # index 1 for swirl item
        self.item_remaining_time = [0, 0]

    def update(self, delta_time):
        # update speedup status
        self.item_remaining_time[0] -= delta_time
        self.item_remaining_time[1] -= delta_time
        if self.item_remaining_time[0] < 0 and self.firing == True:
            self.normalspeed()
        if self.item_remaining_time[1] < 0 and self.swirling == True:
            self.swirling = False

        if self.hitted:
            self.hit_time += delta_time
            if self.hit_time > 0.1:
                self.hitted = False

        if abs(self.velocity.x) < 0.1 and abs(self.velocity.y) < 0.1:
            self.is_flying = False

        if self.is_flying:

            if self.swirling == True:
                if self.velocity.y > 0:
                    self.velocity.x = -self.vx_swirling * ((self.transform.position.y - 400) / 400) * self.vmax * delta_time
                else:
                    self.velocity.x = self.vx_swirling * ((self.transform.position.y - 400) / 400) * self.vmax * delta_time
                self.velocity.y += self.a/2 * delta_time
            else:
                try:
                    angle = 270 - math.atan(self.velocity.y / self.velocity.x) * 180 / 3.1416 - (
                        180 if self.velocity.x < 0 else 0)
                except:
                    angle = 270 - (180 if self.velocity.x < 0 else 0)
                a_y, a_x = self.a * math.sin(angle), self.a*math.cos(angle)
                #a_x, a_y = self.a * self.velocity.x / self.vmax, self.a * self.velocity.y / self.vmax
                self.velocity.x = self.vmax if self.velocity.x >= self.vmax else self.velocity.x + a_x * delta_time
                self.velocity.y = self.vmax if self.velocity.y >= self.vmax else self.velocity.y + a_y * delta_time

            #self.velocity.x, self.velocity.y = self.velocity.x + a_x * delta_time, self.velocity.y + a_y * delta_time
            self.transform.translate(self.velocity.x * delta_time, self.velocity.y * delta_time)

    def draw(self):
        angle = 0 if self.velocity.y <= 0 else 180
        # calculate angle to rotate image
        if self.velocity.x != 0:
            angle = 270 - math.atan(self.velocity.y / self.velocity.x) * 180 / 3.1416 - (
                180 if self.velocity.x < 0 else 0)
        # draw image
        if self.is_flying:
            if self.firing and self.swirling:
                image = pygame.transform.rotate(self.fire_swirl[0], angle)
                self._surface.blit(image, self.fire_swirl[1].move(self.transform.position.x - 20 * self.scale,
                                                       self.transform.position.y - 20 * self.scale))

            elif self.firing:
                image = pygame.transform.rotate(self.fire[0], angle)
                self._surface.blit(image, self.fire[1].move(self.transform.position.x - 20 * self.scale,
                                                       self.transform.position.y - 20 * self.scale))
            
            elif self.swirling:
                image = pygame.transform.rotate(self.swirl[0], angle)
                self._surface.blit(image, self.swirl[1].move(self.transform.position.x - 20 * self.scale,
                                                       self.transform.position.y - 20 * self.scale))

            else:
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
                y_value = math.sqrt(abs(self.vmax ** 2 - x_value ** 2))
                self.velocity.x, self.velocity.y = x_value, y_value
                self.vx_swirling = x_value
                self.is_flying = True
                self.last_hit = "player1"

        # player 2 hit a ball
        elif collider.obj_type == "player2":
            # if the ball is lower than the player 2
            if self.transform.position.y < collider.transform.position.y:
                x_value = self.vmax * (self.transform.position.x - collider.transform.position.x) / collider.radius
                y_value = -math.sqrt(abs(self.vmax ** 2 - x_value ** 2))
                self.velocity.x, self.velocity.y = x_value, y_value
                self.vx_swirling = x_value
                self.is_flying = True
                self.last_hit = "player2"

        # collision with the wall
        elif collider.obj_type == "wall":
            if abs(self.velocity.x) < 20:
                self.velocity.y = -self.velocity.y
            else:
                self.velocity.x = -self.velocity.x
            self.hitted = True
        elif collider.obj_type == "deadwall":
            self.velocity = Point2D(0,0)
            self.dead = True
            self.hitted = False

        elif collider.obj_type == "block":
            if collider.owner * self.velocity.y > 0 :
                self.velocity.y = -self.velocity.y

        elif collider.obj_type == "item":
            if collider.type == "block_item":
                # collision with block item
                if self.velocity.y < 0:
                    return 1
                else:
                    return -1
            elif collider.type == "speedup_item":
                self.speedup()
                return 2
            elif collider.type == "swirl_item":
                self.swirling = True
                self.item_remaining_time[1] = self.item_time
                return 3

    def speedup(self):
        if self.firing == False:
            self.firing = True
            self.vmax *= 1.5
            self.velocity.y *= 1.5
            self.velocity.x *= 1.5
            self.item_remaining_time[0] = self.item_time
            return 1
        return 0
    
    def normalspeed(self):
        self.firing = False
        self.vmax /= 1.5

class Wall:
    def __init__(self, transform: Transform, width, height):
        self.transform = transform
        self.width = width
        self.height = height
        self.obj_type = "wall"
        self.collider = BoxCollider(transform.position, self.width, self.height)
        self.draw_color = (0,255,0)
    def draw(self, surface):
        pygame.draw.rect(surface, self.draw_color, pygame.Rect(self.transform.position.x-self.width/2, self.transform.position.y-self.height/2, self.width, self.height))
    def on_collision(self, collider):
        pass


class DeadWall(Wall):
    def __init__(self, transform: Transform, width, height, side):
        super().__init__(transform, width, height)
        self.side = side
        self.obj_type = "deadwall"
        self.draw_color = (255,0,0)
    
    def on_collision(self, collider):
        pass
class Score:
    def __init__(self, pos, label):
        self.pos = pos
        self.count = 0
        self.label = label
    def inc(self):
        self.count += 1
    def draw(self, surface):
        font = pygame.font.SysFont("anyfont", 39)
        lb = font.render(self.label + str(self.count), True, (255,255,255))

        newpos = (self.pos[0] - lb.get_width()/2, self.pos[1] - lb.get_height()/2)
        surface.blit(lb, newpos)


class Block:
    def __init__(self, transfrom: Transform, width, height, owner, start_tick):
        self.obj_type = "block"
        self.transform = transfrom
        self.width = width
        self.height = height
        self.collider = BoxCollider(self.transform.position, self.width, self.height)
        # -1 is Player 1 (on top), 1 is player 2 (on bottom)
        self.owner = owner
        self.draw_color = (255, 255, 0)
        self.start_tick = start_tick
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.draw_color, pygame.Rect(self.transform.position.x-self.width/2, self.transform.position.y-self.height/2, self.width, self.height))


class Item:
    def __init__(self, type, transfrom: Transform):
        self.obj_type = "item"
        self.type = type
        self.transform = transfrom
        self.collider = BoxCollider(transfrom.position, 50, 50)
        self.block_img, self.block_rect = load_img("items/block.png")
        self.speedup_img, self.speedup_rect = load_img("items/lighting.png")
        self.swirl_img, self.swirl_rect = load_img("items/swirl_item.png")

    def draw(self, surface):
        if self.type == "block_item":
            surface.blit(self.block_img, self.block_rect.move(self.transform.position.x - 25, self.transform.position.y - 25))

        elif self.type == "speedup_item":
            surface.blit(self.speedup_img, self.speedup_rect.move(self.transform.position.x - 25, self.transform.position.y - 25))

        elif self.type == "swirl_item":
            surface.blit(self.swirl_img, self.swirl_rect.move(self.transform.position.x - 25, self.transform.position.y - 25))
            

