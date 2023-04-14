import pygame
from settings import *
from sprites import *
from data import *
import datetime

pygame.init()

class Game():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption("FLAPPY BIRD")
        self.status = "start"
        self.score = 0
        self.font = pygame.font.Font(None, 40)

        self.data = Data()
        record_text = ""
        for i in self.data.selectHighestScore():
            record_text += f"{i[0]}  {i[1]}"
        self.record = self.font.render(record_text, True , (255,0,0))
        self.record_rect = self.record.get_rect()

    def setupSprites(self):
        self.all_sprites_list = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        Background(self.all_sprites_list)
        Ground([self.all_sprites_list, self.collision_sprites],1.8)
        self.bird = Bird(self.all_sprites_list)

        self.obtacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obtacle_timer, 1400)

    def collision(self):
        if pygame.sprite.spritecollide(self.bird, self.collision_sprites, True, pygame.sprite.collide_mask) or self.bird.pos.y <= -10:
            for sprite in self.collision_sprites:
                if sprite.type == "Obstacle":
                    sprite.kill()
            self.bird.kill()
            self.status = "end"
            self.data.insert(self.score, datetime=datetime.datetime.now())

    def displayTitle(self):
        image_title = pygame.image.load(r'img/title.png')
        title = pygame.transform.scale(image_title,(300,70))
        title_rect = title.get_rect(center = (WINDOW_WIDTH // 2, 80))
        self.window.blit(title,title_rect)
            
    def displayStart(self,pos_x, pos_y):
        # Start button
        image_start = pygame.image.load(r'img/start.png')
        start_button = pygame.transform.scale(image_start, (100,100))
        self.start_rect = start_button.get_rect(center = (pos_x, pos_y))
        self.window.blit(start_button,self.start_rect)

    def displayRestart(self,pos_x, pos_y):
        image_restart = pygame.image.load(r'img/restart.png').convert_alpha()
        restart_button = pygame.transform.scale(image_restart, (100,100))
        self.restart_rect = restart_button.get_rect(center = (pos_x, pos_y))
        self.window.blit(restart_button, self.restart_rect)

    def displayPause(self):
        image_pause = pygame.image.load(r'img/pause.png').convert_alpha()
        pau_button = pygame.transform.scale(image_pause,(30,30))
        self.pau_rect = pau_button.get_rect(topleft = (0,0))
        self.window.blit(pau_button, self.pau_rect)

    def displayRecord(self,pos_x, pos_y):
        # Score button
        image_score = pygame.image.load(r'img/record.png').convert_alpha()
        score_button = pygame.transform.scale(image_score, (100,100))
        self.scb_rect = score_button.get_rect(center = (pos_x, pos_y))
        self.window.blit(score_button, self.scb_rect)

    def displayRecordTable(self):
        image = pygame.image.load(r'img/record_table.png').convert_alpha()
        table = pygame.transform.scale(image,(400,500))
        table_width = table.get_width()
        table_height = table.get_height()
        self.table_rect = table.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2.5))
        self.window.blit(table,self.table_rect)
        self.record_rect.center = (table_width // 1.8,table_height // 4)
        self.window.blit(self.record,self.record_rect)
    
    def displayBack(self,pos_x,pos_y):
        image = pygame.image.load(r'img/return.png').convert_alpha()
        return_image = pygame.transform.scale(image,(100,100))
        self.return_rect = return_image.get_rect(center = (pos_x,pos_y))
        self.window.blit(return_image, self.return_rect)

    def displayHome(self,pos_x, pos_y):
        image_home = pygame.image.load(r'img/home.png').convert_alpha()
        home_button = pygame.transform.scale(image_home, (100,100))
        self.home_rect = home_button.get_rect(center = (pos_x,pos_y))
        self.window.blit(home_button,self.home_rect)

    def increaseScore(self):
        for sprite in self.collision_sprites:
            if sprite.type == "Obstacle" and self.bird.pos.x > sprite.pos.x:
                self.score += 1
    
    def displayScore(self):
        self.score_text = self.font.render(f"{self.score}", True, (255,0,0))
        self.score_text_rect = self.score_text.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 5))
        self.window.blit(self.score_text,self.score_text_rect)

    def run(self):
        self.clock.tick(FRAMERATE)
        self.setupSprites()
        running = True

        while running:
            # try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.status == "start" or self.status == "stop":
                            if self.start_rect.collidepoint(event.pos):
                                self.status = "running"
                            if self.scb_rect.collidepoint(event.pos):
                                self.status = "table"
                        elif self.status == "running":
                            if self.pau_rect.collidepoint(event.pos):
                                self.status = "stop"
                        elif self.status == "end":
                            if self.restart_rect.collidepoint(event.pos):
                                self.status = "running"
                                self.bird = Bird(self.all_sprites_list)
                                Ground([self.all_sprites_list, self.collision_sprites],1.8)
                                self.score = 0
                            if self.home_rect.collidepoint(event.pos):
                                self.status = "start"
                                Ground([self.all_sprites_list, self.collision_sprites],1.8)
                                self.bird = Bird(self.all_sprites_list)
                                self.score = 0
                        elif self.status == "table":
                            if self.return_rect.collidepoint(event.pos):
                                self.status = "start"
                    if event.type == self.obtacle_timer and self.status == "running":
                        Obstacle([self.all_sprites_list, self.collision_sprites],1.6)
                        self.increaseScore()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.bird.jump()
                
                self.all_sprites_list.draw(self.window)
                if self.status == "stop":
                    self.displayStart(WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2)
                    self.displayRecord(WINDOW_WIDTH // 2 + 60, WINDOW_HEIGHT // 2)
                else:
                    self.all_sprites_list.update()
                if self.status == "start":
                    self.displayTitle()
                    self.displayStart(WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2)
                    self.displayRecord(WINDOW_WIDTH // 2 + 60, WINDOW_HEIGHT // 2)
                elif self.status == "running":
                    self.bird.apply_gravity()
                    self.displayPause()
                    self.displayScore()
                    self.collision()
                elif self.status == "end":
                    self.displayRestart(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60)
                    self.displayHome(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60)
                elif self.status == "table":
                    self.displayRecordTable()
                    self.displayBack(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 1.2)
                self.clock.tick(FRAMERATE)
                pygame.display.update()
            # except:
            #     print("error")