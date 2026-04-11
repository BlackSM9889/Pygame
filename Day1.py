import pygame
from sys import exit


GAME_WIDTH = 1280
GAME_HEIGH = 720

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGH))
pygame.display.set_caption("Pygame")
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

            pygame.display.update()
            clock.tick(60)