from Assignment2.objects import *
from Assignment2.utils.load_assets import *

class App:
    def __init__(self):
        self._running = True
        self.size = self.width, self.height = 400, 800
        self.player_speed = 200

    def on_init(self):
        pygame.init()
        self.last_frame_tick = pygame.time.get_ticks()/1000

        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self.image_surface = load_img("background\\background.png")[0]

        self.player1 = Player(self._display_surf, Transform(Point2D(100,100), 0), 10, 0.2, 0.1)
        self.player1_velocity = Point2D(0,0)
        self.player1_hit = False

        self._running = True

    def on_render(self):
        self._display_surf.blit(self.image_surface, (0,0))
        self.player1.draw()

        pygame.display.flip()

    def on_event(self, events):
        hit = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player1_velocity.x -= self.player_speed
                elif event.key == pygame.K_d:
                    self.player1_velocity.x += self.player_speed
                elif event.key == pygame.K_w:
                    self.player1_velocity.y -= self.player_speed
                elif event.key == pygame.K_s:
                    self.player1_velocity.y += self.player_speed
                elif event.key == pygame.K_f:
                    hit = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player1_velocity.x += self.player_speed
                elif event.key == pygame.K_d:
                    self.player1_velocity.x -= self.player_speed
                elif event.key == pygame.K_w:
                    self.player1_velocity.y += self.player_speed
                elif event.key == pygame.K_s:
                    self.player1_velocity.y -= self.player_speed
        if hit:
            self.player1_hit = True
        else:
            self.player1_hit = False


    def on_loop(self):
        current_time = pygame.time.get_ticks()/1000
        delta_time = current_time - self.last_frame_tick
        self.last_frame_tick = current_time
        self.player1.move(delta_time, self.player1_velocity)
        if self.player1_hit:
            self.player1.hit()
        self.player1.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            # for event in pygame.event.get():
            #     self.on_event(event)
            self.on_event(pygame.event.get())
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == '__main__':
    app = App()
    app.on_execute()

