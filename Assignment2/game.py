from utils.collision import *
from utils.load_assets import *
from objects import *
import pygame
from pygame.locals import *
from computer_play import P2AI
from threading import Thread
import threading
import winnerscene
import homescene
import random
class App:
    def __init__(self, p2b):
        self.p2b = p2b
        self._running = True
        self.size = self.width, self.height = 400, 800
        self.player_speed = 200
        self.moving_pos = (Point2D(30, 40), Point2D(370, 760))
        self.ball_pos = (Point2D(200, 160), Point2D(200, self.height-160))
        self.y_center = self.height/2
        self.x_center = self.width/2
        self.start_random_item = pygame.time.get_ticks()/1000
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self.image_surface = load_img("background/background.png")[0]
        # GameEnd
        self.winner = "None"

        self.win_point = 10

    def on_init(self):
        self.last_frame_tick = pygame.time.get_ticks()/1000

        self.player1 = Player(self._display_surf, Transform(Point2D(200, 100), 180), 90, 0.2, 0.1, 1)
        self.player1_velocity = Point2D(0, 0)
        self.player1_hit = False

        self.player2 = Player(self._display_surf, Transform(Point2D(200, 700), 0), 90, 0.2, 0.1, 2, is_bot=self.p2b)
        self.player2_velocity = Point2D(0, 0)
        self.player2_hit = False

        self.ball = Ball(self._display_surf, Transform(Point2D(self.ball_pos[0].x, self.ball_pos[0].y), 0))

        wall_height = 280
        wall_y = 260 + wall_height/2
        self.left_wall = Wall(Transform(Point2D(20, wall_y), 0), 10, wall_height)
        self.right_wall = Wall(Transform(Point2D(370, wall_y), 0), 10, wall_height)

        self.items = []
        self.block = None
        self.block_index = 0
        
        # spatial hashmap collision
        self.spatial_hashmap = SpatialHashmap(self.width, self.height, 10)
        # append some object
        self.spatial_hashmap.append_obj(self.ball)
        self.spatial_hashmap.append_obj(self.player1)
        self.spatial_hashmap.append_obj(self.player2)
        self.spatial_hashmap.append_obj(self.left_wall)
        self.spatial_hashmap.append_obj(self.right_wall)

        self.score1 = Score((self.x_center, self.y_center - 30), "")
        self.score2 = Score((self.x_center, self.y_center + 30), "")

        # Init computer player
        if self.p2b:
            self.p2ai = P2AI(self.player2, self.ball)
            self.aithread = Thread(target=P2AI.run, args=(self.p2ai, ))
            self.aithread.start()

        self._running = True

    def on_render(self):
        self._display_surf.blit(self.image_surface, (0, 0))
        self.player1.draw()
        self.player2.draw()
        self.ball.draw()

        # self.left_wall.draw(self._display_surf)
        # self.right_wall.draw(self._display_surf)

        self.score1.draw(self._display_surf)
        self.score2.draw(self._display_surf)

        for item in self.items:
            item.draw(self._display_surf)

        if self.block != None:
            self.block.draw(self._display_surf)

        pygame.display.flip()

    def on_event(self, events):
        player1_hit = False
        player2_hit = False
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
                    player1_hit = True
                if event.key == pygame.K_k:
                    self.player2_velocity.x -= self.player_speed
                elif event.key == pygame.K_SEMICOLON:
                    self.player2_velocity.x += self.player_speed
                elif event.key == pygame.K_o:
                    self.player2_velocity.y -= self.player_speed
                elif event.key == pygame.K_l:
                    self.player2_velocity.y += self.player_speed
                elif event.key == pygame.K_j:
                    player2_hit = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player1_velocity.x += self.player_speed
                elif event.key == pygame.K_d:
                    self.player1_velocity.x -= self.player_speed
                elif event.key == pygame.K_w:
                    self.player1_velocity.y += self.player_speed
                elif event.key == pygame.K_s:
                    self.player1_velocity.y -= self.player_speed
                if event.key == pygame.K_k:
                    self.player2_velocity.x += self.player_speed
                elif event.key == pygame.K_SEMICOLON:
                    self.player2_velocity.x -= self.player_speed
                elif event.key == pygame.K_o:
                    self.player2_velocity.y += self.player_speed
                elif event.key == pygame.K_l:
                    self.player2_velocity.y -= self.player_speed
                
        self.player1_hit = player1_hit
        self.player2_hit = player2_hit

    def on_loop(self):
        current_time = pygame.time.get_ticks()/1000
        delta_time = current_time - self.last_frame_tick
        self.last_frame_tick = current_time
        
        # check win
        if self.score1.count >= self.win_point:
            self._running = False
            self.winner = self.player1.get_player_name()
            return
        if self.score2.count >= self.win_point:
            self._running = False
            self.winner = self.player2.get_player_name()
            return

        # check collision
        self.spatial_hashmap.calculate_collision()
        # 0 is ball
        collsion_result = self.spatial_hashmap.call_collision(0) 
        if collsion_result in [-1, 1]:
            # remove block item
            self.items.pop()
            self.spatial_hashmap.pop_obj()
            # append new block object
            # -1 if owner is player 1 (on top) , 1 if owner is player 2 (on bottom)
            if collsion_result == 1:
                self.block = Block(Transform(Point2D(150, 500), 0), 60, 20, 1, current_time)
            else:
                self.block = Block(Transform(Point2D(150, 300), 0), 60, 20, -1, current_time)
            self.spatial_hashmap.append_obj(self.block)
            # reset start random time
            self.start_random_item = current_time
            self.block_index = self.spatial_hashmap.length() - 1

        elif collsion_result in [2, 3]:
            # remove speed up item
            self.items.pop()
            self.spatial_hashmap.pop_obj()
            self.start_random_item = current_time


        #self.spatial_hashmap.call_collision_all()
        self.spatial_hashmap.clear_data()

        if self.ball.dead:
            self.ball.dead = False
            # remove block collider
            # if self.block != None:
            #     self.block = None
            #     self.spatial_hashmap.pop_index(self.block_index)

            if self.ball.last_hit == "player1":
                if self.ball.transform.position.y > self.y_center:
                    self.score1.inc()
                    self.ball.transform.position.x , self.ball.transform.position.y = self.ball_pos[1].x, self.ball_pos[1].y
                else:
                    self.score2.inc()
                    self.ball.transform.position.x , self.ball.transform.position.y = self.ball_pos[0].x, self.ball_pos[0].y
            elif self.ball.last_hit == "player2":
                if self.ball.transform.position.y < self.y_center:
                    self.score2.inc()
                    self.ball.transform.position.x , self.ball.transform.position.y = self.ball_pos[0].x, self.ball_pos[0].y
                else:
                    self.score1.inc()
                    self.ball.transform.position.x , self.ball.transform.position.y = self.ball_pos[1].x, self.ball_pos[1].y
            self.spatial_hashmap.clear_data()
            

        self.player1.move(delta_time, self.player1_velocity)
        self.player2.move(delta_time, self.player2_velocity)

        if self.player1.transform.position.x < self.moving_pos[0].x:
            self.player1.transform.position.x = self.moving_pos[0].x
        elif self.player1.transform.position.x > self.moving_pos[1].x:
            self.player1.transform.position.x = self.moving_pos[1].x
        elif self.player1.transform.position.y < self.moving_pos[0].y:
            self.player1.transform.position.y = self.moving_pos[0].y
        elif self.player1.transform.position.y > self.y_center - 100:
            self.player1.transform.position.y = self.y_center - 100

        if self.player2.transform.position.x < self.moving_pos[0].x:
            self.player2.transform.position.x = self.moving_pos[0].x
        elif self.player2.transform.position.x > self.moving_pos[1].x:
            self.player2.transform.position.x = self.moving_pos[1].x
        elif self.player2.transform.position.y < self.y_center + 100:
            self.player2.transform.position.y = self.y_center + 100
        elif self.player2.transform.position.y > self.moving_pos[1].y:
            self.player2.transform.position.y = self.moving_pos[1].y

        if self.player1_hit:
            self.player1.hit()

        if self.player2_hit:
            self.player2.hit()

        self.player1.update(current_time)
        self.player2.update(current_time)

        self.ball.update(delta_time)

        # random item
        if current_time - self.start_random_item > 10 and len(self.items) == 0:
            rand = random.randint(0, 2)
            if rand == 0 and self.block == None:
                # new block item
                self.items.append(Item("block_item", Transform(Point2D(225,400), 0)))
                self.spatial_hashmap.append_obj(self.items[0])
            elif rand == 1:
                # rand speed up
                self.items.append(Item("speedup_item", Transform(Point2D(225,400), 0)))
                self.spatial_hashmap.append_obj(self.items[len(self.items) - 1])
            elif rand == 2:
                # rand swirl item
                self.items.append(Item("swirl_item", Transform(Point2D(225,400), 0)))
                self.spatial_hashmap.append_obj(self.items[len(self.items) - 1])
            self.start_random_item = current_time
            
        # check ball dead
        if self.ball.transform.position.x < - 1 or self.ball.transform.position.x > 400 or self.ball.transform.position.y < -1 or self.ball.transform.position.y > self.height + 1 :
            # reset ball
            self.ball.dead = True
            self.ball.velocity = Point2D(0,0)
            self.ball.hitted = False
            
            # reset player status
            self.player1.is_hitting = False
            self.player1.collider.enable = False

            self.player2.is_hitting = False
            self.player2.collider.enable = False

    def on_cleanup(self):
        if self.p2b:
            self.p2ai.running = False

        # switch to winner scene
        ws = winnerscene.WinnerScene(self)
        ws.on_execute()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            self.on_event(pygame.event.get())
            self.on_loop()
            self.on_render()
                
        self.on_cleanup()



if __name__ == '__main__':
    pygame.init()
    sound = load_sound("background.mp3")
    sound.play(loops=-1)
    sound.set_volume(0.4)

    app = homescene.HomeScene()
    app.on_execute()
        

