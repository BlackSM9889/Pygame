import pygame
from sys import exit
import os

#變數
TILE_SIZE = 64
GAME_WIDTH = 1280
GAME_HEIGHT = 720

PLAYER_X = GAME_WIDTH/2
PLAYER_Y = GAME_HEIGHT/2
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 96
PLAYER_JUMP_WIDTH = 76
PLAYER_JUMP_HEIGHT = 84
PLAYER_DISTANCE = 5

GRAVITY = 0.5
FRICTION = 0.4
PLAYER_VELOCITY_X = 5
PLAYER_VELOCITY_Y = -14

METALL_WIDTH = 48
METALL_HEIGHT = 40

#image
def load_image(image_name, scale=None):
    image = pygame.image.load(os.path.join("image", image_name))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image

background_image = load_image("background.png")
player_image_right = load_image("robot-right.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_left = load_image("robot-left.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_jump_right = load_image("robot-right-jump.png", (PLAYER_JUMP_WIDTH, PLAYER_JUMP_HEIGHT))
player_image_jump_left = load_image("robot-left-jump.png", (PLAYER_JUMP_WIDTH, PLAYER_JUMP_HEIGHT))
floor_tile_image = load_image("floor-tile.png", (TILE_SIZE, TILE_SIZE))
metall_image_left = load_image("metall-left.png", (METALL_WIDTH, METALL_HEIGHT))

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
pygame.display.set_caption("Pygame")
clock = pygame.time.Clock()

class Player(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_image_right
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = "right"
        self.jumping = False
    
    def update_image(self):
        if self.jumping:
            if self.direction == "right":
                self.image = player_image_jump_right
            elif self.direction == "left":
                self.image = player_image_jump_left
        else:
            if self.direction == "right":
                self.image = player_image_right
            elif self.direction == "left":
                self.image = player_image_left

class Metall(pygame.Rect):
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, METALL_WIDTH, METALL_HEIGHT)
        self.image = metall_image_left
        self.velocity_y = 0
        self.direction = "left"
        self.jumping = False

class Tile(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, TILE_SIZE, TILE_SIZE)
        self.image = image

def create_map():
    tiles.clear()
    
    # 精確計算：畫面總高度 - 3格空隙 - 1格地板本身 = 距離底部 4 格的位置
    # 這樣地板下方就會剛好剩下 3 格 TILE_SIZE 的高度是空的
    suspended_y = GAME_HEIGHT - (TILE_SIZE * 3)

    # === 1. 底部懸浮長地表 (規格：range 20) ===
    for i in range(20): 
        # 只畫這一層地表，下方不寫任何填充迴圈，達成簍空效果
        tile = Tile(i * TILE_SIZE, suspended_y, floor_tile_image)
        tiles.append(tile)
    
    # === 2. 左側垂直柱子 (規格：range 3) ===
    # 柱子長在懸浮地表上方
    for i in range(3):
        tile = Tile(TILE_SIZE * 3, suspended_y - (i + 1) * TILE_SIZE, floor_tile_image)
        tiles.append(tile)

    for i in range(3):
        metall = Metall(player.x + TILE_SIZE*(3+i*1.5), TILE_SIZE*6)
        metalls.append(metall)

    # === 3. 右側懸空平台 (規格：range 4) ===
    # 依照你的規格，再往上移 3 格
    for i in range(4):
        tile = Tile(TILE_SIZE * 11 + i * TILE_SIZE, suspended_y - TILE_SIZE * 3, floor_tile_image)
        tiles.append(tile)

def check_tile_collision(character):
    for tile in tiles:
        if character.colliderect(tile):
            return tile
    return None

def check_tile_collision_x(character):
    tile = check_tile_collision(character)
    if tile is not None:
        if character.velocity_x < 0: #going left
            character.x = tile.x + tile.width #right side of tile
        elif character.velocity_x > 0: #going right
            character.x = tile.x - character.width #left side of tile
        character.velocity_x = 0

def check_tile_collision_y(character):
    tile = check_tile_collision(character)
    if tile is not None:
        if character.velocity_y < 0: #going up
                character.y = tile.y + tile.height #bottom of tile
        elif character.velocity_y > 0: #going down
            character.y = tile.y - character.height #top of tile
            character.jumping = False
        character.velocity_y = 0

def move():
    # ... (前段處理 X 軸速度的程式碼不變) ...

    # === 2. X 軸實際位移與碰撞檢查 ===
    player.x += player.velocity_x
    
    if player.x < 0: player.x = 0
    if player.right > GAME_WIDTH: player.right = GAME_WIDTH
    
    # 【修正處 1】傳入 player 參數
    tile = check_tile_collision(player) 
    if tile:
        if player.velocity_x > 0: player.right = tile.left
        if player.velocity_x < 0: player.left = tile.right
        player.velocity_x = 0 

    # === 3. Y 軸位移與碰撞檢查（重力） ===
    player.velocity_y += GRAVITY
    player.y += player.velocity_y
    
    # 【修正處 2】傳入 player 參數
    tile = check_tile_collision(player) 
    if tile:
        if player.velocity_y > 0: # 落地
            player.bottom = tile.top
            player.velocity_y = 0
            player.jumping = False
        elif player.velocity_y < 0: # 撞頂
            player.top = tile.bottom
            player.velocity_y = 0

    for metall in metalls:
        metall.velocity_y += GRAVITY
        metall.y += metall.velocity_y
        check_tile_collision_y(metall)

        if player.colliderect(metall):
            print("COLLISION WITH METALL")


def draw():
    window.fill("black")
    scaled_background = pygame.transform.scale(background_image, (GAME_WIDTH, GAME_HEIGHT))
    window.blit(scaled_background, (0, 0))

    for tile in tiles:
        window.blit(tile.image, tile)

    player.update_image()
    window.blit(player.image, player)
    for metall in metalls:
        window.blit(metall.image, metall)

player = Player()
#metall = Metall(player.x + TILE_SIZE*3, TILE_SIZE*6)
metalls = []
tiles = []

create_map()

while True: #game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    # 左右移動控制：改為控制速度，而不是直接改座標
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.velocity_x = -PLAYER_DISTANCE
        player.direction = "left"
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.velocity_x = PLAYER_DISTANCE
        player.direction = "right"
    else:
        player.velocity_x = 0  # 若沒按鍵則速度歸零

    if (keys[pygame.K_UP] or keys[pygame.K_w]) and not player.jumping:
        player.velocity_y = PLAYER_VELOCITY_Y
        player.jumping = True

    move()
    draw()
    pygame.display.update()
    clock.tick(60)