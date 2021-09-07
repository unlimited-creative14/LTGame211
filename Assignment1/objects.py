from utils import *
class MPipe():
    def __init__(self, size, surface, xpos, scale):
        # remember to assign self.image and self.rect
        self._surface = surface
        self._pipe_head, self._head_rect = load_img('pipe_head.png', scale)
        self._pipe_body, self._body_rect = load_img('pipe_body.png', scale)
        self._size = size
        self.rect = self._head_rect.copy()

        # combine rect
        self.rect.inflate_ip(0, self._body_rect.height * size)
        self.rect.move_ip(xpos, -self.rect.y)

        # combine image
        self.image = pygame.Surface(self.rect.size, SRCALPHA)
        self.image.blit(self._pipe_head, (0,0))
        rectself = self._head_rect.copy()
        for i in range(size):
            rectself.move_ip(0, self._body_rect.height)
            self.image.blit(self._pipe_body, rectself)

        # move to bottom
        self.rect.y = self._surface.get_rect().height - self.rect.height

    def update(self):
        pass

    def draw(self):
        self._surface.blit(self.image, self.rect)

class Zombie:
    def __init__(self, surface, fall_speed, xpos = 0, dest_pipe = None, scale = 1):
        self._surface = surface
        self.image, self.rect = load_img("zombie/Idle1.png", scale)
        self.dest_pipe = dest_pipe

        self._fallspd = fall_speed
        self.pos = (xpos, -self.rect.height)
        self.state = "falling"

    def draw(self):
        self._surface.blit(self.image, self.rect.move(self.pos))
        
    def update(self, delta_time):
        if self.state == 'falling':
            self.pos = (self.pos[0], self.pos[1] + delta_time * self._fallspd)
        elif self.state == 'die':
            pass

    def reset_pos(self):
        self.pos = (self.pos[0], -self.rect.height)

    def get_true_rect(self):
        return self.rect.move(self.pos)
    def set_fallspeed(self, spd):
        self._fallspd = spd
    def mul_fallspeed(self, factor):
        self._fallspd *= factor

class AimMark():
    def __init__(self, surface, scale):
        self._surface = surface
        self.image, self.rect = load_img("aim_mark.png", scale)
        self.rect.move_ip(-self.rect.centerx, -self.rect.centery)

        self.pos = (0,0)
    def update(self):
        pass
    def set_pos(self, pos):
        self.pos = pos

    def draw(self):
        self._surface.blit(self.image, self.rect.move(self.pos))

class PointCount:
    def __init__(self, surface, initpos):
        self.hit = 0
        self.miss = 0
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.pos = initpos
        self._surface = surface
        

    def inc_hit(self):
        self.hit += 1
    def inc_miss(self):
        self.miss += 1
    def set_pos(self, npos):
        self.pos = npos

    def draw(self):
        srfhit = self.font.render("Hit:" + str(self.hit), False, (0,0,0))
        srfmiss = self.font.render("Miss:" + str(self.miss), False, (0,0,0))

        baserect = pygame.Rect(0,0,max(srfhit.get_width(), srfmiss.get_width()), srfhit.get_height() + srfmiss.get_height())
        basesuf = pygame.Surface(baserect.size, SRCALPHA)
        
        self._surface.blit(srfhit, baserect.move(self.pos))
        self._surface.blit(srfmiss, baserect.move(self.pos).move(0, srfhit.get_height()))



        