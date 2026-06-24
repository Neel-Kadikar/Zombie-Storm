from pygame import *
from random import *
from math import *

# Initialize pygame
init()
width, height = 800, 600
screen = display.set_mode((width, height))

# Colors
RED = (255, 0, 0)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
BROWN = (150, 75, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BGGREEN = (97, 123, 62)
TILEGREEN = (88, 113, 56)
YELLOW = (255, 255, 0)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)

# Load all sprites
stashPic = image.load("Sprites/stash.png").convert_alpha()
bushPic = image.load("Sprites/bush.png").convert_alpha()
stonePic = image.load("Sprites/stone.png").convert_alpha()
shopBG = image.load("Sprites/shopBG.png").convert_alpha()
shopItem1 = image.load("Sprites/shopItem1.png").convert_alpha()
shopItem2 = image.load("Sprites/shopItem2.png").convert_alpha()
shopItem3 = image.load("Sprites/shopItem3.png").convert_alpha()
shopItem4 = image.load("Sprites/shopItem4.png").convert_alpha()
shopItem5 = image.load("Sprites/shopItem5.png").convert_alpha()
shopItem6 = image.load("Sprites/shopItem6.png").convert_alpha()
playerup = image.load("Sprites/playerup.png").convert_alpha()
playerdown = image.load("Sprites/playerdown.png").convert_alpha()
playerleft = image.load("Sprites/playerleft.png").convert_alpha()
playerright = image.load("Sprites/playerright.png").convert_alpha()
enemyIcon = image.load("Sprites/enemy.png").convert_alpha()
menuBG = image.load("Sprites/menuBG.png").convert_alpha()
howToPlay = image.load("Sprites/howToPlay.png").convert_alpha()
backstory = image.load("Sprites/backstory.png").convert_alpha()

# UI Items
UIItem1 = image.load("Sprites/UIItem1.png").convert_alpha()
UIItem2 = image.load("Sprites/UIItem2.png").convert_alpha()
UIItem3 = image.load("Sprites/UIItem3.png").convert_alpha()
UIItem4 = image.load("Sprites/UIItem4.png").convert_alpha()

# Inventory Items
inventoryBG = image.load("Sprites/inventoryBG.png").convert_alpha()
spearIcon = image.load("Sprites/spearIcon.png").convert_alpha()
bowIcon = image.load("Sprites/bowIcon.png").convert_alpha()
gunIcon = image.load("Sprites/gunIcon.png").convert_alpha()
inventoryIcons = [spearIcon, bowIcon, gunIcon]

# Structure icons
wallIcon = image.load("Sprites/wallIcon.png").convert_alpha()
spikeIcon = image.load("Sprites/spikeIcon.png").convert_alpha()
stoneWallIcon = image.load("Sprites/stoneWallIcon.png").convert_alpha()
strongSpikeIcon = image.load("Sprites/strongSpikeIcon.png").convert_alpha()

# Game setup
myClock = time.Clock()

# Map setup - creates a 50x50 grid with random tiles (0-30). Number used to determine whether blank tile, tree, or stone
mapList = [[randint(0, 30) for _ in range(50)] for _ in range(50)]
tileSize = 40
map_width = len(mapList[0]) * tileSize
map_height = len(mapList) * tileSize

# Player and stash positions
playerpos = [map_width//2, map_height//2]  # Center of map
gold_stash = Rect(map_width//2 - 25, map_height//2 - 125, 50, 50)  # Above player

# Game objects
bullets = []
shopRects = []
mats = [0, 0]  # wood, stone
enemies = []
inventory = []
enemy_colliding = [False] * 1000
score = 0
health = 100
gold_health = 100

# Player rectangles
player_world_rect = Rect(playerpos[0]-20, playerpos[1]-20, 40, 40)
playericon = Rect(width//2-20, height//2-20, 40, 40)

# Game modes
current_mode = "shoot"  # "shoot" or "mine" or "spear"

# Day/Night and Wave systems
game_time = [True, 0, 30000, 20000, time.get_ticks()]  # [day_time, darkness, day_length, night_length, timer]
wave_info = [1, 0, 10, False]  # [wave_count, zombies_killed, zombies_needed, wave_active]
zombie_stats = [20, 1]  # [size, speed]

# Mining text system
mining_text = ["", 0]  # [text, show_until_time]

# Structure systems
structure_Rects = []
structure_Types = []
structure_HP = []

# Player sprites
playerPic = 0
playerPicList = [playerup, playerdown, playerleft, playerright]  # 0=up, 1=down, 2=left, 3=right

# Shop items
shopItems = [shopItem1, shopItem2, shopItem3, shopItem4, shopItem5, shopItem6]
UIItemsRects = []
UIIcons = [UIItem1, UIItem2, UIItem3, UIItem4]
selectedItem = 0

# Set transparency for UI elements
for icon in UIIcons:
    icon.set_alpha(150)
    
for item in shopItems:
    item.set_alpha(200)

for icon in inventoryIcons:
    icon.set_alpha(150)

shopBG.set_alpha(150)
inventoryBG.set_alpha(150)

def drawScene(playerpos, bullets, enemies, gold_stash, score, health, offsetx, offsety): #Draws the entire game scene including map, objects, and UI
    
    screen.fill(BGGREEN)
    draw_map(screen, mapList, tileSize, offsetx, offsety)
   
    # Draw darkness overlay if night - Used some help for Surface, used online forums and pygame docs
    if game_time[1] > 0:
        dark = Surface((width, height))
        dark.set_alpha(game_time[1])
        dark.fill(BLACK)
        screen.blit(dark, (0, 0))
   
    # Draw structures
    for i in range(len(structure_Rects)):
        if structure_Types[i] == "wall":
            screen.blit(wallIcon, (structure_Rects[i].x + offsetx, structure_Rects[i].y + offsety))
        elif structure_Types[i] == "spike":
            screen.blit(spikeIcon, (structure_Rects[i].x + offsetx, structure_Rects[i].y + offsety))
        elif structure_Types[i] == "stoneWall":
            screen.blit(stoneWallIcon, (structure_Rects[i].x + offsetx, structure_Rects[i].y + offsety))
        elif structure_Types[i] == "strongSpike":
            screen.blit(strongSpikeIcon, (structure_Rects[i].x + offsetx, structure_Rects[i].y + offsety))
   
    # Draw bullets
    for b in bullets:
        draw.rect(screen, WHITE, Rect(b[0]+offsetx, b[1]+offsety, b[2], b[3]))
       
    # Draw enemies
    for enemy in enemies:
        draw.circle(screen, BLACK, (enemy[0] + offsetx, (enemy[1] + offsety)), zombie_stats[0])
        draw.circle(screen, RED, (enemy[0] + offsetx, (enemy[1] + offsety)), zombie_stats[0]/3 )

    # Draw UI texts
    texts = [f"Day" if game_time[0] else f"Night", 
             f"Wave: {wave_info[0]}", 
             f"Score: {score}", 
             f"Health: {health}", 
             f"Gold HP: {gold_health}", 
             f"Mode: {current_mode}", 
             f"Wood: {mats[0]} Stone: {mats[1]}"]
   
    for i in range(len(texts)):  #blitting texts
        text_surface = font.SysFont('Arial', 30).render(texts[i], True, WHITE)
        screen.blit(text_surface, (10, 10 + i * 30))
    
    # Draw player and stash
    screen.blit((playerPicList[playerPic]), playericon)
    screen.blit(stashPic, (gold_stash.x + offsetx, gold_stash.y + offsety))

    # Draw mining text if active
    if time.get_ticks() < mining_text[1]:
        text_surface = font.SysFont('Arial', 20).render(mining_text[0], True, WHITE)
        screen.blit(text_surface, (width//2 - 30, height//2 - 50))

def drawShop(): #Draws the shop interface when open
    if shopOpen:
        screen.blit(shopBG, (100, 100))
        shopRects.clear()  # Clear previous rects to avoid duplicates
        for i in range(3):  # 3 rows
            for j in range(2):  # 2 columns
                item_index = i * 2 + j
                if item_index < len(shopItems):  # Make sure we don't go out of bounds of the map (border)
                    itemRect = Rect(j*300 + 150, i*115 + 150, 200, 60)
                    shopRects.append(itemRect)
                    screen.blit(shopItems[item_index], (j*300 + 150, i*115 + 150))

def handleShopClick(clicked_index, mats, health): #Handles shop item purchases
    
    global speed, gold_health
    
    # Shop item 1: Buy health potion
    if clicked_index == 0:
        if mats[0] >= 100 and mats[1] >= 100:
            mats[0] -= 100
            mats[1] -= 100
            health += 25
            if health > 100:
                health = 100
            print("Bought small health potion (+25 HP)!")
        else:
            print("Not enough materials!")
    
    # Shop item 2: Buy shield
    elif clicked_index == 1:
        if mats[0] >= 150 and mats[1] >= 150:
            mats[0] -= 150
            mats[1] -= 150
            health += 100
            if health > 200:
                health = 200
            print("Bought shield!")
        else:
            print("Not enough materials!")
            
    # Shop item 3: Buy gold heal
    elif clicked_index == 2:
        if mats[0] >= 200 and mats[1] >= 200:
            mats[0] -= 200
            mats[1] -= 200
            gold_health = 100  # Full heal
            print("Bought gold stash heal (full health)!")
        else:
            print("Not enough materials!")
    
    # Shop item 4: Buy spear
    elif clicked_index == 3:
        if mats[0] >= 100 and mats[1] >= 120 and "spear" not in inventory: #avoiding buying more than once
            mats[0] -= 100
            mats[1] -= 120
            print("Bought spear!")
            inventory.append("spear")
        elif "spear" in inventory:
            print("already have spear!")
        else:
            print("Not enough materials!")
    
    # Shop item 5: Buy bow
    elif clicked_index == 4:
        if mats[0] >= 150 and mats[1] >= 130 and "bow" not in inventory and "gun" not in inventory: #cannot have gun and bow, gun is an upgrade of bow
            mats[0] -= 150
            mats[1] -= 130
            speed = 2  # Bow shooting speed
            print("Bought bow!")
            inventory.append("bow")
        elif "bow" in inventory:
            print("already have bow!")
        elif "gun" in inventory:
            print("already have gun (upgraded version)!")
        else:
            print("Not enough materials!")
    
    # Shop item 6: Buy gun
    elif clicked_index == 5:
        if mats[0] >= 250 and mats[1] >= 250 and "gun" not in inventory:
            mats[0] -= 250
            mats[1] -= 250
            speed = 5  # set Gun shooting speed
            print("Bought gun!")
            if "bow" in inventory:
                inventory.remove("bow")
            inventory.append("gun")
        elif "gun" in inventory:
            print("already have gun!")
        else:
            print("Not enough materials!")
    
    return mats, health

def inventorySystem(): #Draws the inventory at the bottom of the screen
    
    screen.blit(inventoryBG, (40, 500))
    # Draw inventory items
    if "spear" in inventory:
        screen.blit(spearIcon, (50, 500))
    if "bow" in inventory:
        screen.blit(bowIcon, (155, 500))
    if "gun" in inventory:
        screen.blit(gunIcon, (155, 500))

def drawItemsUI(): #Draws the UI items at the bottom of the screen
    
    UIItemsRects.clear()
    for i in range(len(UIIcons)):
        screen.blit(UIIcons[i], (275 + i * (55 + 8.57), 500))

def removeDeadStructures(): #Removes structures that have been destroyed
    
    i = len(structure_HP) - 1
    while i >= 0:
        if structure_HP[i] <= 0:
            structure_HP.pop(i)
            structure_Rects.pop(i)
            structure_Types.pop(i)
        i -= 1

def useItems(): #Places structures on current tile
    
    global mats, playerpos
    
    # Wood wall
    if selectedItem == 1 and mats[0] >= 10:
        placeStructure("wall", 10, 0, 100)
    
    # Spike
    elif selectedItem == 2 and mats[0] >= 10 and mats[1] >= 10:
        placeStructure("spike", 10, 10, 100)
    
    # Stone wall
    elif selectedItem == 3 and mats[1] >= 16:
        placeStructure("stoneWall", 0, 16, 200)
    
    # Strong spike
    elif selectedItem == 4 and mats[0] >= 20 and mats[1] >= 20:
        placeStructure("strongSpike", 20, 20, 200)

def placeStructure(structure_type, wood_cost, stone_cost, hp): #function to help place structures and avoid placing over each other
    #snaps structure rect to sit on tile, not overlap on multiple
    structure_x = playerpos[0] // tileSize * tileSize
    structure_y = playerpos[1] // tileSize * tileSize
    structure_Rect = Rect(structure_x, structure_y, tileSize, tileSize)
    
    can_place = True
    for oldrect in structure_Rects:
        if structure_Rect.colliderect(oldrect):
            can_place = False
                
    if can_place:
        structure_Rects.append(structure_Rect)
        structure_Types.append(structure_type)
        structure_HP.append(hp)
        mats[0] -= wood_cost
        mats[1] -= stone_cost
        print(f"Placed {structure_type}!")

def moveBullets(bullets): #Updates bullet positions and removes those that go off screen
    
    for b in bullets[:]:
        b[0] += b[4]  # Update x position with x velocity
        b[1] += b[5]  # Update y position with y velocity
        
        # Check if bullet is out of bounds
        if b[0] < 0 or b[0] > map_width or b[1] < 0 or b[1] > map_height:
            bullets.remove(b)
    return bullets

def checkBulletHits(bullets, enemies, current_score):
    """Checks for bullet-enemy collisions"""
    new_score = current_score
    for b in bullets[:]:
        for enemy in enemies[:]:
            # Check distance between bullet and enemy using formula
            if sqrt((b[0] - enemy[0])**2 + (b[1] - enemy[1])**2) < 25:
                enemies.remove(enemy)
                if b in bullets:
                    bullets.remove(b)
                new_score += 5
                wave_info[1] += 1
                break
    return bullets, enemies, new_score

def checkPlayerHits(enemies, playerpos, current_health):
    """Checks for enemy-player collisions"""
    new_health = current_health
    for enemy in enemies:
        if sqrt((playerpos[0] - enemy[0])**2 + (playerpos[1] - enemy[1])**2) < 40:
            new_health -= 1
            # Push enemy away
            angle = atan2(enemy[1] - playerpos[1], enemy[0] - playerpos[0])
            enemy[0] += 5 * cos(angle)
            enemy[1] += 5 * sin(angle)
    return enemies, new_health

def checkGoldHits(enemies, gold_rect, current_gold_health):
    """Checks for enemy-gold stash collisions"""
    new_gold_health = current_gold_health
    for enemy in enemies[:]:
        if gold_rect.collidepoint(enemy[0], enemy[1]):
            new_gold_health -= 1
    return enemies, new_gold_health

def spawnEnemies(enemies):
    """Spawns new enemies during nighttime waves"""
    if not game_time[0] and wave_info[3] and randint(1, 30) == 1:
        side = randint(0, 3)
        if side == 0:  # Top
            enemies.append([randint(0, width), -20])
        elif side == 1:  # Right
            enemies.append([width + 20, randint(0, height)])
        elif side == 2:  # Bottom
            enemies.append([randint(0, width), height + 20])
        else:  # Left
            enemies.append([-20, randint(0, height)])
    return enemies

def moveEnemies(enemies, gold_rect):
    """Moves enemies toward the gold stash with collision detection for structures"""
    global score
    
    alive_enemies = []
    for enemy in enemies:
        target_x, target_y = gold_rect.centerx, gold_rect.centery
        new_x, new_y = enemy[0], enemy[1]
        
        # Move toward gold stash
        if target_x > enemy[0]:
            new_x += zombie_stats[1]
        elif target_x < enemy[0]:
            new_x -= zombie_stats[1]
            
        if target_y > enemy[1]:
            new_y += zombie_stats[1]
        elif target_y < enemy[1]:
            new_y -= zombie_stats[1]
        
        # Check for collisions with structures
        test_rect = Rect(new_x - zombie_stats[0], new_y - zombie_stats[0], 
                         zombie_stats[0]*2, zombie_stats[0]*2)
        enemy_died = False
        can_move = True
        
        for j in range(len(structure_Rects)):
            if test_rect.colliderect(structure_Rects[j]):
                if structure_Types[j] in ["spike", "strongSpike"]:
                    score += 5
                    wave_info[1] += 1
                    enemy_died = True
                    structure_HP[j] -= 0.1
                    break
                elif structure_Types[j] in ["wall", "stoneWall"]:
                    structure_HP[j] -= 0.1
                    can_move = False
        
        if not enemy_died:
            if can_move:
                enemy[0], enemy[1] = new_x, new_y
            alive_enemies.append(enemy)
            
    enemies[:] = alive_enemies
    return enemies

def updateDayNight():
    """Manages day/night cycle and waves"""
    current_time = time.get_ticks()
    
    # Daytime
    if game_time[0]:
        if game_time[1] > 0:  # Gradually reduce darkness
            game_time[1] -= 0.5
        
        # Switch to night after day_length
        if current_time - game_time[4] > game_time[2]:
            game_time[0] = False
            game_time[4] = current_time
            wave_info[3] = True  # Start wave
    
    # Nighttime
    else:
        if game_time[1] < 180:  # Gradually increase darkness
            game_time[1] += 0.5
        
        # Switch to day after night_length OR all zombies defeated
        if (current_time - game_time[4] > game_time[3] or
            (wave_info[3] and len(enemies) == 0 and wave_info[1] >= wave_info[2])):
            game_time[0] = True
            game_time[4] = current_time
            wave_info[3] = False  # End wave
            wave_info[1] = 0  # Reset zombies killed
            wave_info[2] += 5  # Increase zombies needed next wave
            wave_info[0] += 1  # Increase wave count
            
            # Make zombies faster and smaller each wave
            zombie_stats[1] += 0.2
            zombie_stats[0] = max(10, zombie_stats[0] - 1)

def mineBlock(mx, my, materials, mapList, player_pos):
    """Handles mining blocks and getting resources increased"""
    tile_x = (mx - offsetx) // tileSize
    tile_y = (my - offsety) // tileSize
    
    # Check if tile is within map bounds
    if 0 <= tile_y < len(mapList) and 0 <= tile_x < len(mapList[0]):
        player_tile_x = playerpos[0] // tileSize
        player_tile_y = playerpos[1] // tileSize
        
        # Check if tile is adjacent to player
        if abs(tile_x - player_tile_x) <= 1 and abs(tile_y - player_tile_y) <= 1:
            block_type = mapList[tile_y][tile_x]
            
            if block_type == 29:  # Wood
                materials[0] += 2
                mining_text[0] = "+2 wood"
                mining_text[1] = time.get_ticks() + 2000
            elif block_type == 30:  # Stone
                materials[1] += 2
                mining_text[0] = "+2 stone"
                mining_text[1] = time.get_ticks() + 2000
    return materials, mapList

def movePlayer(playerpos):
    """Handles player movement with collision detection"""
    global playerPic, player_world_rect
    
    keys = key.get_pressed()
    goldColliding = False
    
    new_x, new_y = playerpos[0], playerpos[1]
    
    # Movement controls
    if keys[K_w]:
        new_y -= 3
        playerPic = 0  # Face up
    if keys[K_s]:
        new_y += 3
        playerPic = 1  # Face down
    if keys[K_a]:
        new_x -= 3
        playerPic = 2  # Face left
    if keys[K_d]:
        new_x += 3
        playerPic = 3  # Face right
        
    # Keep player within map boundaries
    new_x = max(20, min(new_x, map_width - 20))
    new_y = max(20, min(new_y, map_height - 20))

    # Check for collision with gold stash
    collide_test_rect = Rect(new_x - 20, new_y - 20, 40, 40)
    if collide_test_rect.colliderect(gold_stash):
        goldColliding = True
    
    # Only update position if not colliding with gold
    if not goldColliding:
        playerpos[0], playerpos[1] = new_x, new_y

def draw_map(screen, mapList, tileSize, offsetx=0, offsety=0):
    """Draws the game map with tiles"""
    for row in range(len(mapList)):
        for col in range(len(mapList[row])):
            x = col*tileSize + offsetx
            y = row*tileSize + offsety
            rectColor = BGGREEN
            
            # Determine tile type
            if mapList[row][col] == 29:  # Wood
                rectColor = BROWN
            elif mapList[row][col] == 30:  # Stone
                rectColor = GREY

            # Draw tile background
            if rectColor == BGGREEN:
                draw.rect(screen, rectColor, (x, y, tileSize, tileSize))
            else:
                draw.rect(screen, rectColor, (x+10, y+10, 20, 20))
            
            # Draw tile border
            draw.rect(screen, TILEGREEN, (x, y, tileSize, tileSize), 3)
            
            # Draw tile sprites
            if rectColor == GREY:
                screen.blit(stonePic, (x, y))
            elif rectColor == BROWN:
                screen.blit(bushPic, (x, y))

def game():
    """Main game function, keeps organized compared to putting everything at start of program"""
    #some help taken from online reccomendations and documentation to keep game function for organization rather than at start of program
    #also makes it easier to code for when replaying from the menu after dying
    
    global running, shopOpen, current_mode, selectedItem, speed
    global offsetx, offsety, playerpos, gold_stash
    global bullets, shopRects, mats, enemies, inventory, score, health, gold_health
    global game_time, wave_info, zombie_stats, mapList
    global structure_Rects, structure_Types, structure_HP  
    
    
    running = True
    shopOpen = False
    current_mode = "shoot"
    selectedItem = 0
    speed = 0
    
    # Reset map (regenerate random map)
    mapList = [[randint(0, 30) for _ in range(50)] for _ in range(50)]
    
    # Reset player position
    playerpos = [map_width//2, map_height//2]
    gold_stash = Rect(map_width//2 - 25, map_height//2 - 125, 50, 50)
    
    # Reset game objects
    bullets = []
    shopRects = []
    mats = [0, 0]
    enemies = []
    inventory = []
    score = 0
    health = 100
    gold_health = 100
    
    # Reset structures  
    structure_Rects = []
    structure_Types = []
    structure_HP = []
    
    # Reset day/night cycle
    game_time = [True, 0, 30000, 20000, time.get_ticks()]
    
    # Reset wave info
    wave_info = [1, 0, 10, False]
    
    # Reset zombie stats
    zombie_stats = [20, 1]
    
    # Game loop
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"
                
            if evt.type == MOUSEBUTTONDOWN:
                if evt.button == 1:  # Left click
                    mx, my = mouse.get_pos()
                    
                    if not shopOpen:
                        # Shooting mode
                        if current_mode == "shoot" and speed != 0:
                            world_mx = mx - offsetx
                            world_my = my - offsety
                            ang = atan2(world_my - playerpos[1], world_mx - playerpos[0])
                            vx = cos(ang) * speed
                            vy = sin(ang) * speed
                            bullets.append([playerpos[0], playerpos[1], 8, 8, vx, vy])
                        
                        # Mining mode
                        elif current_mode == "mine":
                            mats, mapList = mineBlock(mx, my, mats, mapList, playerpos)
                        
                        # Spear mode
                        elif current_mode == "spear":
                            world_mx = mx - offsetx
                            world_my = my - offsety
                            
                            for enemy in enemies[:]:
                                enemy_rect = Rect(enemy[0] - zombie_stats[0], enemy[1] - zombie_stats[0],
                                                zombie_stats[0]*2, zombie_stats[0]*2)
                                
                                # Check if clicked on enemy and in range
                                if (enemy_rect.collidepoint(world_mx, world_my) and 
                                    sqrt((playerpos[0] - enemy[0])**2 + (playerpos[1] - enemy[1])**2) < 70):
                                    enemies.remove(enemy)
                                    score += 5
                                    wave_info[1] += 1
                    
                    else:  # Shop is open
                        clicked_rect = None
                        for rect in shopRects:
                            if rect.collidepoint(mx, my):
                                clicked_rect = rect
                                break

                        if clicked_rect:
                            clicked_index = shopRects.index(clicked_rect)
                            mats, health = handleShopClick(clicked_index, mats, health)
            
            if evt.type == KEYDOWN:
                # Toggle shop
                if evt.key == K_b:
                    shopOpen = not shopOpen
                
                # Select items 1-8
                if K_1 <= evt.key <= K_8:
                    selectedItem = evt.key - K_1 + 1
                    print("Selected item:", selectedItem)
                    useItems()
                
                # Deselect item
                if evt.key == K_ESCAPE:
                    selectedItem = 0
                    print("Selected item:", selectedItem)
                
                # Cycle through modes
                if evt.key == K_SPACE:
                    if current_mode == "shoot":
                        current_mode = "mine"
                    elif current_mode == "mine":
                        current_mode = "spear"
                    else:
                        current_mode = "shoot"
        
        # Game updates
        bullets = moveBullets(bullets)
        bullets, enemies, score = checkBulletHits(bullets, enemies, score)
        enemies = moveEnemies(enemies, gold_stash)
        enemies, health = checkPlayerHits(enemies, playerpos, health)
        enemies, gold_health = checkGoldHits(enemies, gold_stash, gold_health)
        enemies = spawnEnemies(enemies)
        updateDayNight()
        
        # Game over condition
        if health <= 0 or gold_health <= 0:
            running = False
            print(f"Game Over! Final Score: {score}")
        
        removeDeadStructures()
        
        # Calculate camera offset to center on player always
        offsetx = width//2 - playerpos[0]
        offsety = height//2 - playerpos[1]
        
        # Drawing
        drawScene(playerpos, bullets, enemies, gold_stash, score, health, offsetx, offsety)
        drawShop()
        drawItemsUI()
        inventorySystem()
        movePlayer(playerpos)

        myClock.tick(60)
        display.flip()
    
    return "menu"

def instructions():
    """Shows the how to play screen"""
    running = True
    backButton = Rect(50, 50, 100, 50)
    
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"
            if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                if backButton.collidepoint(mouse.get_pos()):
                    return "menu"
        
        screen.fill(BLACK)
        screen.blit(howToPlay, (0, 0))
        
        # Draw back button
        draw.rect(screen, RED, backButton)
        text_surface = font.SysFont('Arial', 20).render("Back", True, WHITE)
        screen.blit(text_surface, (backButton.x + 25, backButton.y + 15))
        
        display.flip()
    return "menu"

def story():
    """Shows the backstory screen"""
    running = True
    backButton = Rect(50, 50, 100, 50)
    
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"
            if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                if backButton.collidepoint(mouse.get_pos()):
                    return "menu"
        
        screen.fill(BLACK)
        screen.blit(backstory, (0, 0))
        
        # Draw back button
        draw.rect(screen, RED, backButton)
        text_surface = font.SysFont('Arial', 20).render("Back", True, WHITE)
        screen.blit(text_surface, (backButton.x + 25, backButton.y + 15))
        
        display.flip()
    return "menu"

def menu():
    """Main menu screen"""
    running = True
    buttons = []
    buttonTexts = ["Zombie Storm", "How to Play", "Backstory"]
    
    # Create buttons
    for i in range(3):
        buttons.append(Rect(300, 200 + i*100, 200, 80))
    
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"
            if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                for i in range(len(buttons)):
                    if buttons[i].collidepoint(mouse.get_pos()):
                        if i == 0:
                            return "game"
                        elif i == 1:
                            return "instructions"
                        elif i == 2:
                            return "story"
        
        screen.fill(BLACK)
        screen.blit(menuBG, (0, 0))
        
        # Draw buttons
        for i in range(len(buttons)):
            draw.rect(screen, GOLD, buttons[i])
            text_surface = font.SysFont('Arial', 30).render(buttonTexts[i], True, BLACK)
            text_rect = text_surface.get_rect(center=buttons[i].center)
            screen.blit(text_surface, text_rect)
        
        display.flip()

# Main game loop
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
    elif page == "game":
        page = game()
    elif page == "instructions":
        page = instructions()
    elif page == "story":
        page = story()

quit()
