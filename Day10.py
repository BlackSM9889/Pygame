import pygame
from sys import exit
import os
import random
import tile_map

#變數
GAME_MAP = tile_map.OPTIMIZED_GAME_MAP1

ROW_COUNT = len(GAME_MAP)
COLUMN_COUNT = len(GAME_MAP[0])

TILE_SIZE = 40
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
PLAYER_DISTANCE = 5

GRAVITY = 0.3
FRICTION = 0.4
PLAYER_VELOCITY_X = 7
PLAYER_VELOCITY_Y = -9

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

BLADER_WIDTH = 45
BLADER_HEIGHT = 60
BLADER_VELOCITY_X = 4
BLADER_VELOCITY_Y = 2

#item 變數
LIFE_ENERGY_WIDTH = 20
LIFE_ENERGY_HEIGHT = 24
BIG_LIFE_ENERGY_WIDTH = 28
BIG_LIFE_ENERGY_HEIGHT = 32
ITEM_VELOCITY_Y = -7

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
wall_tile_image = load_image("wall-tile.png", (TILE_SIZE, TILE_SIZE))
beam_tile_image = load_image("beam-tile.png", (TILE_SIZE, TILE_SIZE))
rock_tile1_image = load_image("rock-tile1.png", (TILE_SIZE, TILE_SIZE))
rock_tile2_image = load_image("rock-tile2.png", (TILE_SIZE, TILE_SIZE))
rock_tile3_image = load_image("rock-tile3.png", (TILE_SIZE, TILE_SIZE))
rock_tile4_image = load_image("rock-tile4.png", (TILE_SIZE, TILE_SIZE))
door_tile_image = load_image("door-tile.png", (TILE_SIZE, TILE_SIZE))
room_tile_image = load_image("room-tile.png", (TILE_SIZE, TILE_SIZE))

metall_image_right = load_image("metall-right.png", (METALL_WIDTH, METALL_HEIGHT))
metall_image_left = load_image("metall-left.png", (METALL_WIDTH, METALL_HEIGHT))
metall_image_guard_right = load_image("metall-guard-right.png", (METALL_WIDTH, METALL_HEIGHT))
metall_image_guard_left = load_image("metall-guard-left.png", (METALL_WIDTH, METALL_HEIGHT))
metall_image_bullet = load_image("metall-bullet.png", (METALL_BULLET_WIDTH, METALL_BULLET_HEIGHT))
life_energy_image = load_image("life-energy.png", (LIFE_ENERGY_WIDTH, LIFE_ENERGY_HEIGHT))
big_life_energy_image = load_image("big-life-energy.png", (BIG_LIFE_ENERGY_WIDTH, BIG_LIFE_ENERGY_HEIGHT))
score_ball_image = load_image("score-ball.png", (TILE_SIZE/2, TILE_SIZE/2))
spike_image = load_image("spike.png", (TILE_SIZE, TILE_SIZE))
blader_image_right = load_image("blader-right.png", (BLADER_WIDTH, BLADER_HEIGHT))
blader_image_left = load_image("blader-left.png", (BLADER_WIDTH, BLADER_HEIGHT))

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
pygame.display.set_caption("Pygame")
clock = pygame.time.Clock()
pygame.font.init()
game_font = pygame.font.Font("./megaman-game-font.otf", 24)
game_over = False

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
        self.score = 0
    
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

    def set_invincible(self, milliseconds=1000):
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

class Blader(pygame.Rect):
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, BLADER_WIDTH, BLADER_HEIGHT)
        self.image = blader_image_right
        self.direction = "right"
        self.health = 3
        self.velocity_x = BLADER_VELOCITY_X
        self.velocity_y = BLADER_VELOCITY_Y
        self.start_x = x
        self.start_y = y
        self.max_range_x = TILE_SIZE*4
        self.max_range_y = TILE_SIZE
    
    def update_image(self):
        if self.direction == "right":
            self.image = blader_image_right
        elif self.direction == "left":
            self.image = blader_image_left                   

class Tile(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, TILE_SIZE, TILE_SIZE)
        self.image = image

class Spike(Tile): # 讓 Spike 繼承 Tile 的特性
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        # 定義縮小版的 hitbox，這就是你要的「縮小範圍」
        # x+8, y+16 代表從左邊縮進 8，頂部縮下 16，大小改為 24x24
        self.hitbox = pygame.Rect(x + 8, y + 16, 20, 20)

class Item(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, image.get_width(), image.get_height())
        self.image = image
        self.jumping = False
        self.velocity_y = ITEM_VELOCITY_Y 
        self.used = False        

def append_tiles(map_code, tile):
    if map_code < 0:
        background_tiles.append(tile)
    else:
        tiles.append(tile)

def create_map():
    for column in range(len(GAME_MAP[0])):
        for row in range(len(GAME_MAP)):
            map_code = GAME_MAP[row][column]
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            if map_code == 0: #empty tile
                continue
            elif abs(map_code) == 1:
                append_tiles(map_code, Tile(x, y, rock_tile1_image))
            elif abs(map_code) == 2:
                append_tiles(map_code, Tile(x, y, rock_tile2_image))
            elif abs(map_code) == 3:
                append_tiles(map_code, Tile(x, y, rock_tile3_image))
            elif abs(map_code) == 4:
                append_tiles(map_code, Tile(x, y, rock_tile4_image))
            elif abs(map_code) == 5:
                append_tiles(map_code, Tile(x, y, floor_tile_image))
            elif abs(map_code) == 6:
                append_tiles(map_code, Tile(x, y, wall_tile_image))
            elif map_code == 7:
                background_tiles.append(Tile(x, y, beam_tile_image))
            elif map_code == 8:
                spikes.append(Tile(x, y, spike_image))
            elif map_code == 9:
                background_tiles.append(Tile(x, y, door_tile_image))
            elif map_code == 10:
                background_tiles.append(Tile(x, y, room_tile_image))
            elif map_code == 11:
                metalls.append(Metall(x, y))
            elif map_code == 12:
                bladers.append(Blader(x, y))

def reset_game():
    global player, metalls, metall_bullets, tiles, background_tiles,\
    items, spikes, bladers, game_over
    player = Player()
    metalls = []
    metall_bullets = [] #used to keep bullets active when metall is destroyed
    tiles = []
    background_tiles = []
    items = []
    spikes = [] #traps, hazards
    bladers = []
    create_map()
    game_over = False

def check_tile_collision(character):
    check_range = 200 
    for tile in tiles:
        if abs(tile.x - character.x) < check_range and abs(tile.y - character.y) < check_range:
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

def drop_item(character):
    random_number = random.randint(1, 100) #inclusive of 100
    if 0 < random_number <= 20:
        items.append(Item(character.x, character.y, big_life_energy_image))
    elif 20 < random_number <= 50:
        items.append(Item(character.x, character.y, life_energy_image))
    elif 50 < random_number <= 75:
        items.append(Item(character.x, character.y, score_ball_image))    

def move_player_x(velocity_x):
    move_map_x(velocity_x)
    tile = check_tile_collision(player)
    if tile is not None:
        move_map_x(-velocity_x)

def move_map_x(velocity_x):
    for tile in background_tiles:
        tile.x += velocity_x

    for tile in tiles:
        tile.x += velocity_x
    
    for metall in metalls:
        metall.x += velocity_x
        for bullet in metall.bullets:
            bullet.x += velocity_x

    for bullet in metall_bullets:
        bullet.x += velocity_x
    
    for item in items:
        item.x += velocity_x
    
    for spike in spikes:
        spike.x += velocity_x
    
    for blader in bladers:
        blader.start_x += velocity_x
        blader.x += velocity_x
    

def move():
    global metalls, items, bladers,  metall_bullets, game_over
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

    for spike in spikes:
        if player.colliderect(spike):
            player.health = 0 #game over

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
                player.set_invincible(1000) 
                
                #  施加彈開力道
                if player.centerx < metall.centerx:
                    player.velocity_x = -12  
                else:
                    player.velocity_x = 12   
                
                player.velocity_y = -8       
                
    
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

    for bullet in metall_bullets:
        bullet.x += bullet.velocity_x
        bullet.y += bullet.velocity_y
        if not player.invincible and player.colliderect(bullet):
            player.health -= 2
            bullet.used = True
            player.set_invincible()
    
    metall_bullets = [bullet for bullet in metall_bullets if not bullet.used \
                        and bullet.x + bullet.width > 0 and bullet.x < GAME_WIDTH]            

    #bullets
    for bullet in player.bullets:
        bullet.x += bullet.velocity_x
        for metall in metalls:
            if metall.health > 0 and not bullet.used and bullet.colliderect(metall):
                bullet.used = True
                if not metall.guarding:
                    metall.health -= 1
                    if metall.health <= 0:
                        drop_item(metall)
                        metall_bullets.extend(metall.bullets)
                        player.score += 500

        for blader in bladers:
            if blader.health > 0 and not bullet.used and bullet.colliderect(blader):
                bullet.used = True
                blader.health -= 1
                if blader.health <= 0:
                    drop_item(blader)   
                    player.score += 500             
    
    player.bullets = [bullet for bullet in player.bullets if not bullet.used \
                      and bullet.x + bullet.width > 0 and bullet.x < GAME_WIDTH]
    metalls = [metall for metall in metalls if metall.health > 0]  
    bladers = [blader for blader in bladers if blader.health > 0] 

 #bladers
    for blader in bladers:
        if abs(blader.x + blader.velocity_x - blader.start_x) >= blader.max_range_x:
            blader.velocity_x *= -1
            if blader.velocity_x < 0:
                blader.direction = "left"
            elif blader.velocity_x > 0:
                blader.direction = "right"
        else:
            blader.x += blader.velocity_x

        if abs(blader.y + blader.velocity_y - blader.start_y) >= blader.max_range_y:
            blader.velocity_y *= -1
        else:
            blader.y += blader.velocity_y
        
        #bladers hitbox
        if not player.invincible and player.colliderect(blader):
            player.invincible = True  # 第一時間鎖死
            player.health -= 1
            player.set_invincible(1500)
            
            # X 軸彈開：透過移動地圖達成
            if player.centerx < blader.centerx:
                move_map_x(15) 
            else:
                move_map_x(-15)
            
            player.velocity_y = -8
    
    for item in items:
        item.velocity_y += GRAVITY
        item.y += item.velocity_y
        check_tile_collision_y(item)
        if player.colliderect(item):
            item.used = True
            if item.image == life_energy_image:
                player.health = min(player.health + 2, player.max_health)
            elif item.image == big_life_energy_image:
                player.health = min(player.health + 8, player.max_health)
    items = [item for item in items if not item.used]

    if player.health <= 0 or player.y > GAME_HEIGHT:
        game_over = True


def draw():
    window.fill("black")
    scaled_background = pygame.transform.scale(background_image, (GAME_WIDTH, GAME_HEIGHT))
    window.blit(scaled_background, (0, 0))

    for tile in background_tiles:
        if tile.x > GAME_WIDTH:
            break
        window.blit(tile.image, tile)

    for tile in tiles:
        if tile.x > GAME_WIDTH:
            break
        window.blit(tile.image, tile)

    for spike in spikes:
        if spike.x > GAME_WIDTH:
            break
        window.blit(spike.image, spike)    

    player.update_image()
    window.blit(player.image, player)

    for bullet in player.bullets:
        window.blit(bullet.image, bullet)

    for metall in metalls:
        if metall.x > GAME_WIDTH:
            break
        metall.update_image()
        window.blit(metall.image, metall)
        for bullet in metall.bullets:
            window.blit(bullet.image, bullet)

    for bullet in metall_bullets:
        window.blit(bullet.image, bullet)

    for blader in bladers:
        if blader.x > GAME_WIDTH:
            break
        blader.update_image()
        window.blit(blader.image, blader)        

    for item in items:
        if item.x > GAME_WIDTH:
            break
        window.blit(item.image, item)        

    pygame.draw.rect(window, "red", (TILE_SIZE, TILE_SIZE, 10*player.max_health, 10))  
    pygame.draw.rect(window, "green", (TILE_SIZE, TILE_SIZE, 10*player.health, 10))  

    #score
    text_score = str(player.score)
    while len(text_score) < 7: #7 digits in score
        text_score = "0" + text_score
    text_surface = game_font.render(text_score, False, "white")
    window.blit(text_surface, (GAME_WIDTH/2-80, TILE_SIZE/2))

    if game_over:
        text_surface = game_font.render("Game Over:", False, "black")
        window.blit(text_surface, (GAME_WIDTH/2, GAME_HEIGHT/2))
        text_surface = game_font.render("Press [Enter] to Restart", False, "black")
        window.blit(text_surface, (GAME_WIDTH/2, GAME_HEIGHT/2 + TILE_SIZE))

#start game
player = Player()
metalls = []
metall_bullets = []
tiles = []
background_tiles = []
items = []
spikes = []
bladers = []
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
    if (keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]) and game_over:
        reset_game()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        move_player_x(PLAYER_VELOCITY_X)
        player.direction = "left"

    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        move_player_x(-PLAYER_VELOCITY_X)
        player.direction = "right"

    else:
        player.velocity_x = 0  

    if (keys[pygame.K_UP] or keys[pygame.K_w]) and not player.jumping:
        player.velocity_y = PLAYER_VELOCITY_Y
        player.jumping = True

    if (keys[pygame.K_x] or keys[pygame.K_SPACE]) and player.shoot_cooldown == 0:
        player.set_shooting() 

    
    # 冷卻計時
    if player.shoot_cooldown > 0:
        player.shoot_cooldown -= 1    

    if not game_over:
        move()
        draw()
        pygame.display.update()
        clock.tick(60)