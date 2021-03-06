from objects import *
import pygame
from game import App
class HomeScene:
    def __init__(self):
        self._running = True
        self.size = self.width, self.height = 400, 800
        self.center = (self.width/2, self.height/2)
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self.image_surface = load_img("background/background.png")[0]
        self.next_scene = None

    def on_init(self):
        self.title = Text((self.center[0] - 100, self.center[1] - 150),
        "Tennis", 100, color=(232,215,42)
        )

        w, h = 200, 50
        btn2player_pos = (self.center[0]-w/2, self.center[1])
        btnbotplayer_pos = (self.center[0]-w/2, self.center[1] + 100)

        self.btn2Player =  Button(
            btn2player_pos, 
            200, 50, 
            Text(btn2player_pos, "Player - Player", 32, color=(232,215,42)),
            color=(83,35,222))
        self.btnBotPlayer = Button(
            btnbotplayer_pos, 
            200, 50, 
            Text(btnbotplayer_pos, "Bot - Player", 32, color=(232,215,42)),
            color=(83,35,222))


        self.btn2Player.set_callback(
            lambda: App(False)
        ) 
        self.btnBotPlayer.set_callback(
            lambda: App(True)
        )

    def on_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                a = self.btn2Player.check_click(event.pos)
                b = self.btnBotPlayer.check_click(event.pos)
                self.next_scene = a or b

    def on_loop(self):
        if self.next_scene:
            self._running = False

    def on_render(self):
        self._display_surf.blit(self.image_surface, (0,0))

        self.title.draw(self._display_surf)
        self.btnBotPlayer.draw(self._display_surf)
        self.btn2Player.draw(self._display_surf)

        pygame.display.flip()

    def on_cleanup(self):
        if self.next_scene:
            self.next_scene.on_execute()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            self.on_event(pygame.event.get())
            self.on_loop()
            self.on_render()
                
        self.on_cleanup()