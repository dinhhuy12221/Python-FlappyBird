import pygame
from random import choice,randint
from settings import *

class Background(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.type = "Background"

        surf = pygame.image.load(r"img/background.png").convert_alpha()
        image = pygame.transform.scale(surf, [WINDOW_WIDTH,WINDOW_HEIGHT])
        self.image = pygame.Surface([WINDOW_WIDTH*2,WINDOW_HEIGHT])
        self.image.blit(image, (0,0))
        self.image.blit(image, (WINDOW_WIDTH,0))

        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)
    
    def update(self):
        self.rect.x = round(self.pos.x)
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.pos.x -= 2

class Ground(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.type = "Ground"

        ground_surf = pygame.image.load(r"img/floor.png").convert_alpha()

        self.image = pygame.transform.scale(ground_surf, pygame.math.Vector2((WINDOW_WIDTH * 4,ground_surf.get_height())))
        self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x = round(self.pos.x)
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.pos.x -= 4

class Bird(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.type = "Bird"

        bird_surf = pygame.image.load(r'img/bird.png').convert_alpha()
        self.image = pygame.transform.scale(bird_surf, pygame.math.Vector2(bird_surf.get_size()) * 0.5)
        self.rect = self.image.get_rect(midleft=(WINDOW_WIDTH // 5, WINDOW_HEIGHT // 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.mask = pygame.mask.from_surface(self.image)

        self.gravity = 1
        self.direction = 0

    def jump(self):
        self.direction -=  15                                                             
        
    def apply_gravity(self):                                                                  
        self.direction += self.gravity * 0.3
        self.pos.y += self.direction * 0.3
        self.rect.y = round(self.pos.y) 

    def rotate(self):
        rotated_image = pygame.transform.rotozoom(self.image,-self.direction*0.1,1)
        self.image = rotated_image
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.apply_gravity()
        # self.rotate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.type = "Obstacle"

        orientation = choice(('up', 'down'))
        surf = pygame.image.load(f'img/pipe.png').convert_alpha()
        self.image = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * 0.5)
        x = WINDOW_WIDTH + randint(40, 100)
        if orientation == 'up':
            y = WINDOW_HEIGHT + randint(0, 150)
            self.rect = self.image.get_rect(midbottom=(x, y))
        if orientation == 'down':
            y = randint(-70, 0)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop=(x, y))

        self.pos = pygame.math.Vector2(self.rect.center)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.pos.x -= 5
        self.rect.x = round(self.pos.x)
        if self.rect.right < -1:
            self.kill()