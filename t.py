import pygame
from sys import exit


GAME_WIDTH = 1280
GAME_HEIGHT = 720

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
pygame.display.set_caption("Pygame")
clock = pygame.time.Clock()

player = pygame.Rect(0, 670, 50, 50)

def draw():
    window.fill((20, 18, 167))
    pygame.draw.rect(window, (2, 239, 238), player)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= 5        
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y += 5
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= 5 
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += 5
        
    draw()    

    pygame.display.update()
    clock.tick(60)