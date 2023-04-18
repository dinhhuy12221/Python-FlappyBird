import pygame
from random import choice,randint
from settings import *

class Background(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.type = "Background"

        surf = pygame.image.load(r"img/background2.png").convert_alpha()
        image1 = pygame.transform.scale(surf, [WINDOW_WIDTH,WINDOW_HEIGHT])
        self.image = pygame.Surface([WINDOW_WIDTH*2,WINDOW_HEIGHT])
        self.image.blit(image1, (0,0))
        self.image.blit(image1, (WINDOW_WIDTH,0))

        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)
    
    def update(self):
        self.rect.x = round(self.pos.x)
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.pos.x -= 5

class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_refactor):
        super().__init__(groups)
        self.type = "Ground"

        ground_surf = pygame.image.load(r"img/floor.png").convert_alpha()

        self.image = pygame.transform.scale(ground_surf, pygame.math.Vector2((WINDOW_WIDTH * 4,ground_surf.get_height() * .6)) * scale_refactor)
        self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x = round(self.pos.x)
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.pos.x -= 10

class Bird(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.type = "Bird"

        bird_surf = pygame.image.load(r'img/bird.png').convert_alpha()
        self.image = pygame.transform.scale(bird_surf, pygame.math.Vector2((50,50)))
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH // 5, WINDOW_HEIGHT // 2))
        self.pos = pygame.math.Vector2(self.rect.center)

        self.mask = pygame.mask.from_surface(self.image)

        self.direction = 0
        self.gravity = 1

    def jump(self):
        self.direction -= 25 
        self.direction *= 0.6
        
    def apply_gravity(self):
        self.direction += self.gravity * 0.6
        self.pos.y += self.direction * 0.6
        self.rect.y = round(self.pos.y)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scale_refactor):
        super().__init__(groups)
        self.type = "Obstacle"

        # orientation = choice(('up', 'down'))
        # surf = pygame.image.load(f'img/{choice((0, 1))}.png').convert_alpha()
        # self.image = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_refactor)
        # x = WINDOW_WIDTH + randint(40, 100)
        # if orientation == 'up':
        #     y = WINDOW_HEIGHT + randint(0, 150)
        #     self.rect = self.image.get_rect(midbottom=(x, y))
        # if orientation == 'down':
        #     y = randint(-150, 0)
        #     self.image = pygame.transform.flip(self.image, False, True)
        #     self.rect = self.image.get_rect(midtop=(x, y))
        x = WINDOW_WIDTH  + randint(40, 100)
        y =  WINDOW_HEIGHT // 2 + randint(-200,100)
        surf = pygame.image.load(r'img/obstacle1.png').convert_alpha()
        self.image = pygame.transform.scale(surf, pygame.math.Vector2(WINDOW_WIDTH,WINDOW_HEIGHT * 1.4))
        self.rect = self.image.get_rect(center=(x,y))

        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.pos.x -= 5
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -1:
            self.kill()