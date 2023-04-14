import pygame
from settings import *
from sprites import *
from game import *

if "__main__" == __name__:
    game = Game().run()
    pygame.quit()
