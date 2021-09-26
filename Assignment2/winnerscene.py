from objects import *
import pygame
from homescene import HomeScene
from game import App

class WinnerScene:
    def __init__(self, post_game):
        pygame.init()
        self._running = True
        self.size = self.width, self.height = 400, 800
        self.post_game = post_game
        self.center = (self.width/2, self.height/2)
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self.image_surface = load_img("background/background.png")[0]
        self.next_scene = None

    def on_init(self):
        self.txWinner = Text((self.center[0], self.center[1] - 120),"Winner: " + self.post_game.winner, 40)
        self.txScore = Text((self.center[0], self.center[1] - 50),"%d - %d" % (self.post_game.score1.count, self.post_game.score2.count), 36)
        btnback_pos = (self.center[0]+20, self.center[1])
        btnagain_pos = (self.center[0]-100, self.center[1])
        self.btnBack = Button(
            btnback_pos, 
            100, 50, 
            Text(btnback_pos, "Back", 25))
        self.btnAgain = Button(
            btnagain_pos, 
            100, 50, 
            Text(btnagain_pos, "Again", 25))

        # make center
        self.txWinner.pos = (self.txWinner.pos[0] - self.txWinner.get_rect().w / 2, self.txWinner.pos[1])
        self.txScore.pos = (self.txScore.pos[0] - self.txScore.get_rect().w / 2, self.txScore.pos[1])
        global p2b
        self.btnBack.set_callback(
            lambda: HomeScene()
        )
        self.btnAgain.set_callback(
            lambda: App(p2b)
        )

    def on_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                a = self.btnBack.check_click(event.pos)
                b = self.btnAgain.check_click(event.pos)
                self.next_scene = a or b
                

    def on_loop(self):
        if self.next_scene:
            self._running = False

    def on_render(self):
        self._display_surf.blit(self.image_surface, (0,0))

        
        self.txWinner.draw(self._display_surf)
        
        self.txScore.draw(self._display_surf)
        self.btnBack.draw(self._display_surf)
        self.btnAgain.draw(self._display_surf)

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
