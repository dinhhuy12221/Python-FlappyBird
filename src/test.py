# To remove the background outside the text in Pygame, you can use a mask to create a transparent surface that only shows the text and not the background. Here’s an example code that demonstrates how to do this:

import pygame
import sys

pygame.init()

# Set up the display
screen = pygame.display.set_mode((640, 480))

# Load the font
font = pygame.font.SysFont(None, 48)

# Render the text
text = font.render("Hello World", True, (255, 255, 255))

# Create a mask from the text
mask = pygame.mask.from_surface(text)

# Create a new surface with a transparent background
transparent_surface = pygame.Surface((text.get_width(), text.get_height()), pygame.SRCALPHA)

# Blit the text onto the transparent surface using the mask
transparent_surface.blit(text, (0, 0), None, pygame.BLEND_RGBA_MULT)

# Blit the transparent surface onto the screen


pygame.display.flip()

while True:
    screen.fill((255,0,0))
    screen.blit(transparent_surface, (100, 100))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
# This code creates a new surface with a transparent background and blits the text onto it using a mask to create a surface that only shows the text and not the background1. I hope this helps!