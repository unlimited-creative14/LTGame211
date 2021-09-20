import pygame.time

from Assignment2.utils.load_assets import load_img


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Transform:
    def __init__(self, position: Point2D, rotation=0):
        self.position = position
        self.rotation = rotation

    def translate(self, x, y):
        self.position.x += x
        self.position.y += y


class Player:
    def __init__(self, surface, transform: Transform, r, idle_animate, hit_animate):
        self._surface = surface
        self.transform = transform
        self.radius = r
        self.idle_animate = idle_animate
        self.hit_animate = hit_animate

        self.idles = []
        for i in range(0, 4):
            self.idles.append(load_img("character\\idle\\idle" + str(i + 1) + '.png'))

        self.hits = []
        for i in range(0, 8):
            self.hits.append(load_img("character\\hit\\hit" + str(i + 1) + '.png'))

        self.hit_index = 0
        self.idle_index = 0

        # bool check hitting animation
        self.is_hitting = False

        # time when hitting
        self.hit_tick = 0

    def move(self, delta_time, velocity: Point2D):
        self.transform.translate(velocity.x * delta_time, velocity.y * delta_time)

    def hit(self):
        self.hit_tick = pygame.time.get_ticks()/1000
        self.is_hitting = True

    def update(self):
        current_time = pygame.time.get_ticks()/1000

        # hit animation index
        index = int((current_time - self.hit_tick) / self.hit_animate)
        if index > 7:
            self.is_hitting = False
        else:
            self.hit_index = index

        # idle animation index
        self.idle_index = int(current_time / self.idle_animate) % 4

    def draw(self):
        if self.is_hitting:
            self._surface.blit(self.hits[self.hit_index][0], self.hits[self.hit_index][1].move(self.transform.position.x, self.transform.position.y))
        else:
            self._surface.blit(self.idles[self.idle_index][0],
                               self.idles[self.idle_index][1].move(self.transform.position.x, self.transform.position.y))
