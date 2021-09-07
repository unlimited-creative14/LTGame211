
import random
from objects import *


sizes = [1,2,3,2,1,2,4]

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 800, 600

        self.delta_time = 0
        self.internal_clock = 0
        self.last_frame_tick = 0
        self.scale = 0.4


        self.point = 0
        self.default_fallspeed = 175
        self.slowdown_factor = 0.5
        self.spawn_clock = 0
        self.spawn_rate = 1.75
        self.max_zombie = len(sizes)*2

        random.shuffle(sizes)
        self.live = 3

    def on_init(self):
        pygame.init()
        self.last_frame_tick = pygame.time.get_ticks()
        self.last_update_tick = pygame.time.get_ticks()

        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE)  
        self._img_surface = load_img("bg.bmp")[0]

        self.pos = [self.width * i / len(sizes) for i in range(len(sizes))]
        
        self.scale = 2/(len(sizes))

        self.pipes = [MPipe(sizes[i], self._display_surf, self.pos[i], self.scale) for i in range(len(sizes))]
        self.zombies = []

        self.aimmark = AimMark(self._display_surf, self.scale / 4)
        self.hitcount = PointCount(self._display_surf, (0,0))

        self.bg_sound = load_sound("bg_music.wav")
        self.boom_sound = load_sound("boom.wav")
        self.boom_sound.set_volume(0.5)

        self.bg_sound.play(loops=-1)

        self._running = True

        # init for boom
        self.kabooms = []

 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            hit = False
            for zombie in self.zombies:
                if not contains(zombie.dest_pipe.rect, event.pos) and contains(zombie.rects[zombie.index].move(zombie.pos), event.pos):
                    self.zombies.remove(zombie)
                    self.hitcount.inc_hit()
                    hit = True
                    # new kaboom
                    self.boom_sound.play(maxtime=500)
                    self.kabooms.append(Kaboom(self._display_surf, self.scale * 2, 0.1, event.pos))

                    break
            if not hit:
                self.hitcount.inc_miss()
                
        elif event.type == MOUSEMOTION:
            self.aimmark.set_pos(event.pos)

    def on_loop(self):
        nc = pygame.time.get_ticks()
        self.delta_time = (nc - self.last_frame_tick) / 1000.0
        self.last_frame_tick = nc

        # create more zombies here
        # select pipe to spawn

        if len(self.zombies) < self.max_zombie:
            if self.spawn_clock < (1/self.spawn_rate):
                self.spawn_clock += self.delta_time
            else:
                self.spawn_clock = 0
                num = random.choice(range(len(sizes)))
                selected_pipe = self.pipes[num]
                self.zombies.append(Zombie(self._display_surf, self.default_fallspeed, self.pos[num], selected_pipe, self.scale))
        
        for zombie in self.zombies:
            # remove zombie when he completely fall into pipe
            if zombie.get_true_rect().top > zombie.dest_pipe.rect.top:
                self.zombies.remove(zombie)

                print("fall out")

            # slow down zombie when he get into pipe
            if zombie.get_true_rect().bottom > zombie.dest_pipe.rect.top:
                zombie.set_fallspeed(self.slowdown_factor*self.default_fallspeed)

        for kaboom in self.kabooms:
            if kaboom.success == 1:
                self.kabooms.remove(kaboom)

        # do update them
        [x.update(self.delta_time) for x in self.zombies]
        [x.update(self.delta_time) for x in self.kabooms]


    def on_render(self):
        self._display_surf.blit(self._img_surface, (0,0))
        
        [x.draw() for x in self.zombies]
        [x.draw() for x in self.pipes]
        [x.draw() for x in self.kabooms]
        self.aimmark.draw()  
        self.hitcount.draw()  

        pygame.display.flip()

    def on_cleanup(self):
        self.bg_sound.stop()
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
    theApp = App()
    theApp.on_execute()