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
PLAYER_JUMP_HEIGHT = 90
PLAYER_SHOOT_WIDTH = 70
PLAYER_JUMP_SHOOT_WIDTH = 64
PLAYER_DISTANCE = 7

GRAVITY = 0.5
FRICTION = 0.4
PLAYER_VELOCITY_Y = -14

PLAYER_BULLET_WIDTH = 20
PLAYER_BULLET_HEIGHT = 25
PLAYER_BULLET_VELOCITY_X = 8

#enemy 變數
METALL_WIDTH = 56
METALL_HEIGHT = 56
METALL_BULLET_WIDTH = 18
METALL_BULLET_HEIGHT = METALL_BULLET_WIDTH
METALL_BULLET_VELOCITY_X = 2
METALL_BULLET_VELOCITY_Y = METALL_BULLET_VELOCITY_X

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
player_image_shoot_right = load_image("robot-right-shoot.png", (PLAYER_SHOOT_WIDTH, PLAYER_HEIGHT))
player_image_shoot_left = load_image("robot-left-shoot.png", (PLAYER_SHOOT_WIDTH, PLAYER_HEIGHT))
player_image_jump_shoot_right = load_image("robot-right-jump-shoot.png",
                                           (PLAYER_JUMP_SHOOT_WIDTH, PLAYER_JUMP_HEIGHT))
player_image_jump_shoot_left = load_image("robot-left-jump-shoot.png",
                                           (PLAYER_JUMP_SHOOT_WIDTH, PLAYER_JUMP_HEIGHT))
player_image_bullet = load_image("bullet.png", (PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT))
floor_tile_image = load_image("floor-tile.png", (TILE_SIZE, TILE_SIZE))
metall_image_right = load_image("metall-right.png", (METALL_WIDTH, METALL_HEIGHT))
metall_image_left = load_image("metall-left.png", (METALL_WIDTH, METALL_HEIGHT))
metall_image_guard_right = load_image("metall-guard-right.png", (METALL_WIDTH, METALL_HEIGHT))
metall_image_guard_left = load_image("metall-guard-left.png", (METALL_WIDTH, METALL_HEIGHT))
metall_image_bullet = load_image("metall-bullet.png", (METALL_BULLET_WIDTH, METALL_BULLET_HEIGHT))

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
pygame.display.set_caption("Pygame")
clock = pygame.time.Clock()

#Custom event
INVINCIBLE_END = pygame.USEREVENT + 0
SHOOTING_END = pygame.USEREVENT + 1


class Player(pygame.Rect):
    class Bullet(pygame.Rect):
        def __init__(self):
            if player.direction == "left":
                pygame.Rect.__init__(self, player.x, player.y + TILE_SIZE/2,
                                     PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)
                self.velocity_x = -PLAYER_BULLET_VELOCITY_X
            elif player.direction == "right":
                pygame.Rect.__init__(self, player.x + player.width, player.y + TILE_SIZE/2,
                                     PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)
                self.velocity_x = PLAYER_BULLET_VELOCITY_X
            self.image = player_image_bullet
            self.used = False

    def __init__(self):
        pygame.Rect.__init__(self, PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_image_right
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = "right"
        self.jumping = False
        self.invincible = False
        self.max_health = 30
        self.health =  self.max_health
        self.shooting = False
        self.shoot_cooldown = 0
        self.bullets = []
    
    def update_image(self):
        if self.jumping and self.shooting:
            if self.direction == "right":
                self.image = player_image_jump_shoot_right
            elif self.direction == "left":
                self.image = player_image_jump_shoot_left
        elif self.shooting:
            if self.direction == "right":
                self.image = player_image_shoot_right
            elif self.direction == "left":
                self.image = player_image_shoot_left
        elif self.jumping:
            if self.direction == "right":
                self.image = player_image_jump_right
            elif self.direction == "left":
                self.image = player_image_jump_left
        else:
            if self.direction == "right":
                self.image = player_image_right
            elif self.direction == "left":
                self.image = player_image_left

    def set_invincible(self, milliseconds=1500):
        self.invincible = True
        pygame.time.set_timer(INVINCIBLE_END, milliseconds, 1)            

    def set_shooting(self):
        if not self.shooting:
            self.shooting = True
            self.bullets.append(Player.Bullet())
            pygame.time.set_timer(SHOOTING_END, 250, 1)            

class Metall(pygame.Rect):
    class Bullet(pygame.Rect):
        def __init__(self, metall, velocity_y):
            if metall.direction == "left":
                pygame.Rect.__init__(self, metall.x, metall.y + TILE_SIZE/2,
                                     METALL_BULLET_WIDTH, METALL_BULLET_HEIGHT)
                self.velocity_x = -METALL_BULLET_VELOCITY_X
            elif metall.direction == "right":
                pygame.Rect.__init__(self, metall.x + metall.width, metall.y + TILE_SIZE/2,
                                     METALL_BULLET_WIDTH, METALL_BULLET_HEIGHT)
                self.velocity_x = METALL_BULLET_VELOCITY_X
            self.velocity_y = velocity_y
            self.image = metall_image_bullet
            self.used = False

    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, 56, 60)
        self.image = metall_image_left
        self.velocity_y = 0
        self.direction = "left"
        self.jumping = False
        self.health = 1
        self.bullets = []
        self.last_fired = pygame.time.get_ticks()
        self.guarding = False

    def update_image(self):
        if self.direction == "right":
            if self.guarding:
                self.image = metall_image_guard_right
            else:
                self.image = metall_image_right
        elif self.direction == "left":
            if self.guarding:
                self.image = metall_image_guard_left
            else:
                self.image = metall_image_left    

    def set_shooting(self):
        if abs(self.x - player.x) <= TILE_SIZE*4:
            self.guarding = False
            now = pygame.time.get_ticks()
            if now - self.last_fired > 1000:
                self.last_fired = now
                self.bullets.append(Metall.Bullet(self, -METALL_BULLET_VELOCITY_Y))
                self.bullets.append(Metall.Bullet(self, 0))
                self.bullets.append(Metall.Bullet(self, METALL_BULLET_VELOCITY_Y))    
        else:
            self.guarding = True           

class Tile(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, TILE_SIZE, TILE_SIZE)
        self.image = image

def create_map():
    tiles.clear()
    
    suspended_y = GAME_HEIGHT - (TILE_SIZE * 3)

    # 1. 底部懸浮長地表 (規格：range 20) 
    for i in range(20): 
        tile = Tile(i * TILE_SIZE, suspended_y, floor_tile_image)
        tiles.append(tile)
    
    # 2. 左側垂直柱子 (規格：range 3) 
    for i in range(3):
        tile = Tile(TILE_SIZE * 3, suspended_y - (i + 1) * TILE_SIZE, floor_tile_image)
        tiles.append(tile)

    for i in range(3):
        metall = Metall(player.x + TILE_SIZE*(3+i*1.5), TILE_SIZE*6)
        metalls.append(metall)

    #  3. 右側懸空平台 (規格：range 4) 
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
    global metalls
    # x
    player.x += player.velocity_x
    if player.x < 0: player.x = 0
    if player.right > GAME_WIDTH: player.right = GAME_WIDTH
    
    tile = check_tile_collision(player) 
    if tile:
        if player.velocity_x > 0: player.right = tile.left
        if player.velocity_x < 0: player.left = tile.right
        player.velocity_x = 0 

    # y  
    player.velocity_y += GRAVITY
    player.y += player.velocity_y
    
    tile = check_tile_collision(player) 
    if tile:
        if player.velocity_y > 0: 
            player.bottom = tile.top
            player.velocity_y = 0
            player.jumping = False
        elif player.velocity_y < 0:
            player.top = tile.bottom
            player.velocity_y = 0

    # 小怪碰撞檢查 位移
    for metall in metalls:
        # 小怪本身hitbox
        metall.velocity_y += GRAVITY
        metall.y += metall.velocity_y
        check_tile_collision_y(metall)

        if not player.invincible:
            if player.colliderect(metall):
                #扣血
                player.health -= 1
                #  觸發無敵
                player.set_invincible(1500) 
                
                #  施加彈開力道
                if player.centerx < metall.centerx:
                    player.velocity_x = -12  
                else:
                    player.velocity_x = 12   
                
                player.velocity_y = -8       
                
                print("撞到怪了！進入無敵狀態並彈開")
    
        if player.x < metall.x:
            metall.direction = "left"
        else:
            metall.direction = "right"       

     #enemy bullets
        metall.set_shooting()
        for bullet in metall.bullets:
            bullet.x += bullet.velocity_x
            bullet.y += bullet.velocity_y
            if not player.invincible and player.colliderect(bullet):
                player.health -= 2
                bullet.used = True
                player.set_invincible()
        
        metall.bullets = [bullet for bullet in metall.bullets if not bullet.used \
                          and bullet.x + bullet.width > 0 and bullet.x < GAME_WIDTH]            

    #bullets
    for bullet in player.bullets:
        bullet.x += bullet.velocity_x
        for metall in metalls:
            if metall.health > 0 and not bullet.used and bullet.colliderect(metall):
                bullet.used = True
                if not metall.guarding:
                    metall.health -= 1
    
    player.bullets = [bullet for bullet in player.bullets if not bullet.used \
                      and bullet.x + bullet.width > 0 and bullet.x < GAME_WIDTH]
    metalls = [metall for metall in metalls if metall.health > 0]    
    

def draw():
    window.fill("black")
    scaled_background = pygame.transform.scale(background_image, (GAME_WIDTH, GAME_HEIGHT))
    window.blit(scaled_background, (0, 0))

    for tile in tiles:
        window.blit(tile.image, tile)

    player.update_image()
    window.blit(player.image, player)

    for bullet in player.bullets:
        window.blit(bullet.image, bullet)

    for metall in metalls:
        metall.update_image()
        window.blit(metall.image, metall)
        for bullet in metall.bullets:
            window.blit(bullet.image, bullet)

    pygame.draw.rect(window, "red", (TILE_SIZE, TILE_SIZE, 10*player.max_health, 10))  
    pygame.draw.rect(window, "green", (TILE_SIZE, TILE_SIZE, 10*player.health, 10))  

#start game
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

        if event.type == INVINCIBLE_END:
            player.invincible = False
        elif event.type == SHOOTING_END:
            player.shooting = False    

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

    if (keys[pygame.K_x] or keys[pygame.K_SPACE]) and player.shoot_cooldown == 0:
        player.set_shooting() 
        print(len(player.bullets))

    
    # 冷卻計時
    if player.shoot_cooldown > 0:
        player.shoot_cooldown -= 1    

    move()
    draw()
    pygame.display.update()
    clock.tick(60)
