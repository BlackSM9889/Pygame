import pygame
from sys import exit
import os

GAME_WIDTH = 1280
GAME_HEIGHT = 720

PLAYER_X = GAME_WIDTH/2
PLAYER_Y = GAME_HEIGHT/2
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 96
PLAYER_DISTANCE = 5

background_image = pygame.image.load(os.path.join("image", "background.png"))
player_image_right = pygame.image.load(os.path.join("image", "robot-right.png"))
player_image_right = pygame.transform.scale(player_image_right, (PLAYER_WIDTH, PLAYER_HEIGHT))

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
pygame.display.set_caption("Pygame")
clock = pygame.time.Clock()

class Player(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_image_right

player = Player()

def draw():
    window.fill("black")
    scaled_background = pygame.transform.scale(background_image, (GAME_WIDTH, GAME_HEIGHT))
    window.blit(scaled_background, (0, 0))
    window.blit(player.image, (player.x, player.y))

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y = max(player.y - PLAYER_DISTANCE, 0)
       
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y + player.height + PLAYER_DISTANCE <= GAME_HEIGHT:
        player.y = min(player.y + PLAYER_DISTANCE, GAME_HEIGHT - player.height)

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x = max(player.x - PLAYER_DISTANCE, 0)

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x = min(player.x + PLAYER_DISTANCE, GAME_WIDTH - player.width)
        
    draw()    

    pygame.display.update()
    clock.tick(60)