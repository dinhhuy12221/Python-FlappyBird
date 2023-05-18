import pygame, sys
from settings import *
from sprites import *


class Game():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption("FLAPPY BIRD")
        self.clock = pygame.time.Clock()
        self.game_status = "Start"
        self.font = pygame.font.Font("font/BD_Cartoon_Shout.ttf", 20)
        self.score = 0
        self.score_updated = False

    def sprites_setup(self):
        self.all_sprites_list = pygame.sprite.Group()
        self.collision_sprites_list = pygame.sprite.Group()
        self.background = Background(self.all_sprites_list)
        self.ground_sprite = pygame.sprite.Group()
        self.ground = Ground([self.ground_sprite,self.collision_sprites_list])
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1600)

    def collision(self):
        if pygame.sprite.spritecollide(self.bird, self.collision_sprites_list, False, pygame.sprite.collide_mask) or self.bird.pos.y <= -10:
            for sprite in self.collision_sprites_list:
                if sprite.type == "Obstacle":
                    sprite.kill()
            self.bird.kill()
            self.game_status = "End"

    def text_display(self):
        text = "TAP TO PLAY"
        text_surf = self.font.render(text, True,(255,255,255)).convert_alpha()
        text_rect = text_surf.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 1.5))
        self.window.blit(text_surf, text_rect) 

    def title_display(self):
        tilte_img = pygame.image.load("img/title.png").convert_alpha()
        title_surf = pygame.transform.scale(tilte_img, pygame.math.Vector2(tilte_img.get_size()) * 0.08)
        title_rect = title_surf.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
        self.window.blit(title_surf,title_rect)

    def result_display(self):
        if self.score_updated:
            record_text = f"NEW RECORD: {self.score}"
            record_text_surf = self.font.render(record_text, True, (255,255,255))
            record_text_rect = record_text_surf.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
            self.window.blit(record_text_surf, record_text_rect)
        else:
            score_text = f"YOUR SCORE: {self.score}"
            score_text_surf = self.font.render(score_text, True, (255,255,255))
            score_text_rect = score_text_surf.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
            self.window.blit(score_text_surf, score_text_rect)

    def score_display(self):
        self.score_surf = self.font.render(f"{self.score}", True, (255,255,255)).convert_alpha()
        self.score_rect = self.score_surf.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 5))
        self.window.blit(self.score_surf,self.score_rect)
    
    def increase_score(self):
        for sprite in self.collision_sprites_list:
            if sprite.type == "Obstacle":
                if self.bird.pos.x > sprite.pos.x + 50:
                    sprite.remove(self.collision_sprites_list)
                    self.score += 1
    

    def run(self):
        self.sprites_setup()
        running = True

        while running:
            # try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()
                    if self.game_status == "Running" and event.type == self.obstacle_timer:
                        Obstacle([self.collision_sprites_list,self.all_sprites_list])
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if self.game_status == "Start":
                                self.bird = Bird(self.all_sprites_list)
                                self.game_status = "Running"
                                self.score = 0
                                self.score_updated = False
                            elif self.game_status == "End":
                                self.game_status = "Running"
                                self.bird.kill()
                                self.bird = Bird(self.all_sprites_list)
                                self.score = 0
                                self.score_updated = False
                            elif self.game_status == "Running":
                                self.bird.jump()

                self.all_sprites_list.update()
                self.all_sprites_list.draw(self.window)
                self.ground_sprite.update()
                self.ground_sprite.draw(self.window)

                if self.game_status == "Start":
                    self.score = 0
                    self.title_display()
                    self.text_display()
                elif self.game_status == "Running":
                    self.collision()
                    self.increase_score()
                    self.score_display() 
                elif self.game_status == "End":
                    self.text_display()
                    self.result_display()

                self.clock.tick(FRAMERATE)
                pygame.display.update()
            # except:
            #     print("error")