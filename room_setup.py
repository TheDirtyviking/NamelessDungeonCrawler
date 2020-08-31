import arcade
import game
import items
import goblin
import sound_manager

SPRITE_SCALING = 0.6
SPRITE_NATIVE_SIZE = 100
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)
SCREEN_WIDTH = SPRITE_SIZE * 25
SCREEN_HEIGHT = SPRITE_SIZE * 15

def add_wall(room, x, y):
    wall = arcade.Sprite("resources/images/wall.png", SPRITE_SCALING)
    wall.left = x * SPRITE_SIZE
    wall.bottom = y * SPRITE_SIZE
    room.wall_list.append(wall)

def add_darkness(room, x, y):
    darkness = arcade.Sprite("resources/images/darkness.png", SPRITE_SCALING)
    darkness.left = x * SPRITE_SIZE
    darkness.bottom = y * SPRITE_SIZE
    room.floor_list.append(darkness)

def add_floor(room, x, y):
    floor = arcade.Sprite("resources/images/floor.png", SPRITE_SCALING)
    floor.left = x * SPRITE_SIZE
    floor.bottom = y * SPRITE_SIZE
    room.floor_list.append(floor)

def add_torch(room, x, y):
    torch = arcade.Sprite("resources/images/torch.png", SPRITE_SCALING)
    torch.left = x * SPRITE_SIZE
    torch.bottom = y * SPRITE_SIZE
    torch.pickup = items.torch_get_picked_up
    room.item_list.append(torch)

def add_sword(room, x, y):
    sword = arcade.Sprite("resources/images/sword.png", .7)
    sword.left = x * SPRITE_SIZE
    sword.bottom = y * SPRITE_SIZE + 15
    sword.pickup = items.sword_get_picked_up
    room.item_list.append(sword)

def add_shield(room, x, y):
    shield = arcade.Sprite("resources/images/shield.png", .7)
    shield.left = x * SPRITE_SIZE + 15
    shield.bottom = y * SPRITE_SIZE + 15
    shield.pickup = items.shield_get_picked_up
    room.item_list.append(shield)

def add_heal(room, x, y):
    heal = arcade.Sprite("resources/images/heal.png", .7)
    heal.left = x * SPRITE_SIZE + 15
    heal.bottom = y * SPRITE_SIZE + 15
    heal.pickup = items.heal_get_picked_up
    room.item_list.append(heal)

def add_goblin_1(room, x, y):
    gobbo = arcade.Sprite("resources/images/goblin_1.png", .7)
    gobbo.left = x * SPRITE_SIZE + 15
    gobbo.bottom = y * SPRITE_SIZE + 15
    gobbo.Goblin = goblin.Goblin(center_x=gobbo._get_center_x(), center_y=gobbo._get_center_y())
    gobbo.move = gobbo.Goblin.update
    gobbo.engine = None
    room.enemy_list.append(gobbo)

def add_goblin_2(room, x, y,):
    gobbo = arcade.Sprite("resources/images/goblin_2.png", .7)
    gobbo.left = x * SPRITE_SIZE + 15
    gobbo.bottom = y * SPRITE_SIZE + 15
    gobbo.Goblin = goblin.Goblin(5, 2, 1, gobbo._get_center_x(), gobbo._get_center_y())
    gobbo.move = gobbo.Goblin.update
    gobbo.engine = None
    room.enemy_list.append(gobbo)

def add_goblin_3(room, x, y):
    gobbo = arcade.Sprite("resources/images/goblin_3.png", .9)
    gobbo.left = x * SPRITE_SIZE + 15
    gobbo.bottom = y * SPRITE_SIZE + 15
    gobbo.Goblin = goblin.Goblin(15, 5, 2, gobbo._get_center_x(), gobbo._get_center_y(), gobtype=goblin.HOBGOBLIN, attack_range=60, movespeed=2)
    gobbo.move = goblin.Goblin.update
    gobbo.engine = None
    room.enemy_list.append(gobbo)

def add_player_attack(room, x, y, angle, damage):
    attack = arcade.Sprite("resources/images/attack_swipe.png")
    attack.center_x = x
    attack.center_y = y
    attack.angle = angle
    attack.timer = 10
    attack.damage = damage
    attack.damaged_sprites = arcade.SpriteList()
    room.player_attack_list.append(attack)

def add_enemy_attack(room, x, y, angle, damage):
    attack = arcade.Sprite("resources/images/enemy_swipe.png")
    attack.center_x = x
    attack.center_y = y
    attack.angle = angle
    attack.timer = 10
    attack.damage = damage
    attack.damaged_hero = False
    room.enemy_attack_list.append(attack)

def add_fog(room):
        #Add fog
    room.fog_list = arcade.SpriteList()
    for x in range(0, 25):
        for y in range(0, 15):
            fog = arcade.Sprite("resources/images/darkness.png", SPRITE_SCALING)
            fog.left = x * SPRITE_SIZE
            fog.bottom = y * SPRITE_SIZE
            fog.is_wall = False
            room.fog_list.append(fog)
            for wall in room.wall_list:
                if wall.position == fog.position:
                    fog.is_wall = True

def update_player_attacks(room):
    for attack in room.player_attack_list:
        attack.timer -= 1
        if attack.timer <= 0:
            room.player_attack_list.remove(attack)
        else:
            hit_enemies = arcade.check_for_collision_with_list(attack, room.enemy_list)
            for enemy in hit_enemies:
                b_already_hit = False
                for damaged_enemy in attack.damaged_sprites:
                    if enemy == damaged_enemy:
                        b_already_hit = True
                if not b_already_hit:
                    enemy.Goblin.take_damage(attack.damage)
                    attack.damaged_sprites.append(enemy)

def update_enemy_attacks(room, player_sprite, slayer):
    for attack in room.enemy_attack_list:
        attack.timer -= 1
        if attack.timer <= 0:
            room.enemy_attack_list.remove(attack)
        elif not attack.damaged_hero:
            attack.damaged_hero = arcade.check_for_collision(attack, player_sprite)
            if attack.damaged_hero:
                slayer.take_damage(attack.damage)
            
def update_fog(room, player_position, player_sight):
    player_x = player_position[0]
    player_y = player_position[1]
    for fog in room.fog_list:
        if abs(fog.center_x - player_x) <= player_sight * SPRITE_SIZE:
            if abs(fog.center_y - player_y) <= player_sight * SPRITE_SIZE:
                if fog.is_wall:
                    room.visible_list.append(fog)
                    room.fog_list.remove(fog)
                elif arcade.has_line_of_sight(player_position, fog.position, room.wall_list, player_sight * SPRITE_SIZE):
                    room.visible_list.append(fog)
                    room.fog_list.remove(fog)
    for visible in room.visible_list:
        if abs(visible.center_x - player_x) > player_sight * SPRITE_SIZE or abs(visible.center_y - player_y) > player_sight * SPRITE_SIZE:
            room.fog_list.append(visible)
            room.visible_list.remove(visible)
        elif not visible.is_wall:
            if not player_position == visible.position and not arcade.has_line_of_sight(player_position, visible.position, room.wall_list, player_sight * SPRITE_SIZE):
                room.fog_list.append(visible)
                room.visible_list.remove(visible)

def update_enemies(room, player_position):
    player_x = player_position[0]
    player_y = player_position[1]
    for enemy in room.enemy_list:
        if enemy.Goblin.health <= 0:
            enemy.Goblin.die(room, enemy.left, enemy.bottom)
            room.enemy_list.remove(enemy)
            add_enemy_engine(room.enemy_list, room.wall_list)
        if abs(enemy.center_x - player_x) <= 4 * SPRITE_SIZE:
            if abs(enemy.center_y - player_y) <= 4 * SPRITE_SIZE:
                enemy.Goblin.update(player_position, room, enemy)
                enemy.engine.update()

def add_enemy_engine(enemies, walls):
    for enemy in enemies:
        collidables = arcade.SpriteList()
        for x in range(len(enemies)):
            if not enemy == enemies[x]:
                collidables.append(enemies[x])
        for wall in walls:
            collidables.append(wall)
        enemy.engine = arcade.PhysicsEngineSimple(enemy, collidables)

class Room:

    def __init__(self):
        self.player_attack_list = None
        self.enemy_attack_list = None
        self.wall_list = None
        self.enemy_list = None
        self.item_list = None
        self.floor_list = None
        self.fog_list = None
        self.visible_list = None
        self.enemy_physics_engine = None
        self.accent_list = None
        self.check_move_room = None
        self.boss_fight = None
            
def room_1_move_room(room, slayer_pos, game):
    if slayer_pos[0] > SPRITE_SIZE * 25:
        game.update_room(1)
        return (5, SPRITE_SIZE * 4.5)
    return None

def room_2_move_room(room, slayer_pos, game):
    if slayer_pos[1] < 0:
        if slayer_pos[0] > SPRITE_SIZE * 20 and slayer_pos[0] < SPRITE_SIZE * 22:
            game.update_room(3)
            return (SPRITE_SIZE * 13, SPRITE_SIZE * 14.5)
        elif slayer_pos[0] > SPRITE_SIZE * 4 and slayer_pos[0] < SPRITE_SIZE * 6:
            game.update_room(2)
            return (SPRITE_SIZE * 23, SPRITE_SIZE * 14.5)
    elif slayer_pos[0] < 0:
        game.update_room(0)
        return (SPRITE_SIZE * 24, SPRITE_SIZE * 5)

def room_3_move_room(room, slayer_pos, game):
    if slayer_pos[1] > SPRITE_SIZE * 15:
        game.update_room(1)
        return (SPRITE_SIZE * 5, 5)
    elif slayer_pos[1] < 0:
        if slayer_pos[0] < SPRITE_SIZE * 6 and slayer_pos[0] > SPRITE_SIZE * 4:
            game.update_room(4)
            return (SPRITE_SIZE * 14, SPRITE_SIZE * 14.5)
        elif slayer_pos[0] > SPRITE_SIZE * 22 and slayer_pos[0] < SPRITE_SIZE * 24:
            game.update_room(5)
            return (SPRITE_SIZE * 3, SPRITE_SIZE * 14.5)
    return None

def room_4_move_room(room, slayer_pos, game):
    if slayer_pos[1] > SPRITE_SIZE * 15:
        game.update_room(1)
        return (SPRITE_SIZE * 21, 5)
    elif slayer_pos[1] < 0:
        game.update_room(5)
        return (SPRITE_SIZE * 13, SPRITE_SIZE * 14.5)
    return None

def room_5_move_room(room, slayer_pos, game):
    if slayer_pos[1] > SPRITE_SIZE * 15:
        game.update_room(2)
        return (SPRITE_SIZE * 5, 5)
    return None

def room_6_move_room(room, slayer_pos, game):
    if len(room.enemy_list) == 0:
        game.win_game()
    elif slayer_pos[1] > SPRITE_SIZE * 15:
        if slayer_pos[0] < SPRITE_SIZE * 4 and slayer_pos[0] > SPRITE_SIZE * 2:
            game.update_room(2)
            return (SPRITE_SIZE * 23, 5)
        elif slayer_pos[0] > SPRITE_SIZE * 12 and slayer_pos[0] < SPRITE_SIZE * 14:
            game.update_room(3)
            return (SPRITE_SIZE * 7, 5)
    elif (not room.boss_fight) and slayer_pos[1] < SPRITE_SIZE * 11:
        add_wall(room, 7, 11)
        add_wall(room, 8, 11)
        for fog in room.fog_list:
            for wall in room.wall_list:
                    if wall.position == fog.position:
                        fog.is_wall = True
        sound_manager.play_sound(sound_manager.CLOSE_DOOR, .15)
        room.boss_fight = True
    return None
    
def setup_room_1():
    room = Room()

    #Add walls
    room.wall_list = arcade.SpriteList()
    for y in (0, 14):
        for x in range(0, 25):
            add_wall(room, x, y)
    for x in (0, 24):
        for y in range(1, 14):
            if (y != 4 and y != 5) or x == 0:
                add_wall(room, x , y)
    for x in range(3, 24):
        if(x != 18 and x != 19 and x != 12 and x != 11):
            add_wall(room, x, 3)
    add_wall(room, 3, 2)
    add_wall(room, 3, 1)
    add_wall(room, 17, 2)
    add_wall(room, 17, 1)
    for y in range(4, 9):
        add_wall(room, 3, y)
    for x in range(4, 9):
        add_wall(room, x, 8)
    for x in range(10, 24):
        add_wall(room, x, 12)
    for x in range(17, 24):
        add_wall(room, x, 6)
    for y in range(1, 10):
        add_wall(room, 13, y)
    add_wall(room, 14, 9)
    add_wall(room, 15, 9)
    for y in range(6, 12):
        add_wall(room, 11, y)

    #Add floors
    room.floor_list = arcade.SpriteList()
    for x in range(1, 25):
        for y in range(1, 14):
            add_floor(room, x, y)
    for x in (14, 15, 16):
        for y in (1, 2):
            add_darkness(room, x, y)

    #Add fog
    add_fog(room)
                
    #Add items
    room.item_list = arcade.SpriteList()
    add_torch(room, 23, 13)
    add_heal(room, 23, 1)
    add_heal(room, 4, 1)

    #Add enemies
    room.enemy_list = arcade.SpriteList()
    add_goblin_1(room, 3, 13)
    add_goblin_1(room, 5, 11)
    add_goblin_1(room, 4, 10)
    add_goblin_1(room, 21, 9)
    add_goblin_2(room, 19, 8)
    add_goblin_1(room, 5, 6)
    
    #Initialize other lists
    room.visible_list = arcade.SpriteList()
    room.player_attack_list = arcade.SpriteList()
    room.enemy_attack_list = arcade.SpriteList()
    room.accent_list = arcade.SpriteList()

    #Add physics engines to enemies
    add_enemy_engine(room.enemy_list, room.wall_list)

    #Add room movement logic
    room.check_move_room = room_1_move_room
    
    return room

def setup_room_2():
    room = Room()
    room.wall_list = arcade.SpriteList()

    #Add walls
    for x in range(0, 25):
        add_wall(room, x, 14)
    for y in range(0, 4):
        add_wall(room, 0, y)
    for y in range(6, 14):
        add_wall(room, 0, y)
        add_wall(room, 9, y)
        add_wall(room, 17, y)
    for y in range(0, 15):
        add_wall(room, 24, y)
    for y in range(1, 3):
        add_wall(room, 3, y)
    for x in range(0, 4):
        add_wall(room, x, 0)
    for x in range(6, 20):
        add_wall(room, x, 0)
    for x in range(22, 25):
        add_wall(room, x, 0)
        add_wall(room, x, 3)
    for x in range(1, 20):
        add_wall(room, x, 3)
    for x in range(1, 4):
        add_wall(room, x, 6)
    for x in range(6, 11):
        add_wall(room, x, 6)
    for x in range(13, 21):
        add_wall(room, x, 6)

    #Add floors
    room.floor_list = arcade.SpriteList()
    for x in range(1, 25):
        for y in range(1, 14):
            add_floor(room, x, y)
    for x in (1, 2):
        for y in (1, 2):
            add_darkness(room, x, y)
    add_floor(room, 0, 4)
    add_floor(room, 0, 5)
    add_floor(room, 4, 0)
    add_floor(room, 5, 0)
    add_floor(room, 20, 0)
    add_floor(room, 21, 0)
    
    #Add fog
    add_fog(room)

    #Add items
    room.item_list = arcade.SpriteList()
    add_shield(room, 23, 13)
    add_heal(room, 23, 2)

    #Add enemies
    room.enemy_list = arcade.SpriteList()
    add_goblin_1(room, 2, 12)
    add_goblin_1(room, 8, 2)
    add_goblin_1(room, 15, 8)
    add_goblin_1(room, 17, 4)
    add_goblin_2(room, 12, 11)

    #Initialize other lists
    room.visible_list = arcade.SpriteList()
    room.player_attack_list = arcade.SpriteList()
    room.enemy_attack_list = arcade.SpriteList()
    room.accent_list = arcade.SpriteList()

    #Add physics engines to enemies
    add_enemy_engine(room.enemy_list, room.wall_list)

    #Add logic for moving rooms
    room.check_move_room = room_2_move_room

    return room

def setup_room_3():

    room = Room()

    #Add walls
    room.wall_list = arcade.SpriteList()
    for x in range(0, 22):
        add_wall(room, x, 14)
    for x in range(0, 4):
        add_wall(room, x, 0)
    for x in range(1, 11):
        add_wall(room, x, 7)
    for x in range(13, 18):
        add_wall(room, x, 7)
    for x in range(3, 15):
        add_wall(room, x, 4)
        add_wall(room, x, 3)
    for x in range(6, 22):
        add_wall(room, x, 0)
    for x in range(17, 22):
        add_wall(room, x, 1)
        add_wall(room, x, 2)
        add_wall(room, x, 12)
    add_wall(room, 17, 13)
    add_wall(room, 21, 13)
    for y in range(1, 14):
        add_wall(room, 0, y)
    for y in range(8, 12):
        add_wall(room, 4, y)
        add_wall(room, 6, y)
    add_wall(room, 5, 11)
    for y in range(1, 3):
        add_wall(room, 3, y)
    for y in range(3, 5):
        add_wall(room, 20, y)
    for y in range(3, 10):
        add_wall(room, 21, y)
        add_wall(room, 20, y)
    for y in range(8, 14):
        add_wall(room, 17, y)
    for y in range(0, 15):
        add_wall(room, 24, y)
    for y in range(3, 5):
        add_wall(room, 17, y)

    #Add floors
    room.floor_list = arcade.SpriteList()
    for x in range(1, 25):
        for y in range(1, 14):
            add_floor(room, x, y)
    for x in range(18, 21):
        add_darkness(room, x, 13)
        add_darkness(room, x, 1)
    for y in range(8, 11):
        add_darkness(room, 5, y)
    add_floor(room, 4, 0)
    add_floor(room, 5, 0)
    add_floor(room, 22, 0)
    add_floor(room, 23, 0)
    add_floor(room, 22, 14)
    add_floor(room, 23, 14)
    
    #Add fog
    add_fog(room)

    #Add items
    room.item_list = arcade.SpriteList()
    add_torch(room, 3, 8)
    add_sword(room, 1, 8)
    add_heal(room, 2, 1)

    #Add enemies
    room.enemy_list = arcade.SpriteList()
    add_goblin_1(room, 8, 9)
    add_goblin_1(room, 15, 12)
    add_goblin_1(room, 14, 10)
    add_goblin_2(room, 10, 12)

    #Initialize other lists
    room.visible_list = arcade.SpriteList()
    room.player_attack_list = arcade.SpriteList()
    room.enemy_attack_list = arcade.SpriteList()
    room.accent_list = arcade.SpriteList()

    #Add physics engines to enemies
    add_enemy_engine(room.enemy_list, room.wall_list)

    #Add logic for moving rooms
    room.check_move_room = room_3_move_room

    return room

def setup_room_4():

    room = Room()

    #Add walls
    room.wall_list = arcade.SpriteList()
    for x in range(0, 12):
        add_wall(room, x, 14)
    for x in range(0, 6):
        add_wall(room, x, 0)
    for x in range(1, 3):
        add_wall(room, x, 7)
        add_wall(room, x, 8)
    for x in range(8, 25):
        add_wall(room, x, 0)
    for x in range(14, 25):
        add_wall(room, x, 14)
    for x in range(6, 19):
        add_wall(room, x, 7)
        add_wall(room, x, 8)
    for x in range(11, 16):
        add_wall(room, x, 11)
    for x in range(18, 21):
        add_wall(room, x, 11)
    for y in range(1, 14):
        add_wall(room, 0, y)
        add_wall(room, 24, y)
    for y in range(1, 13):
        add_wall(room, 5, y)
    for y in range(1, 4):
        add_wall(room, 12, y)
    for y in range(9, 11):
        add_wall(room, 18, y)
    for y in range(12, 14):
        add_wall(room, 11, y)

    #Add floors
    room.floor_list = arcade.SpriteList()
    for x in range(1, 25):
        for y in range(1, 14):
            add_floor(room, x, y)
    add_floor(room, 6, 0)
    add_floor(room, 7, 0)
    add_floor(room, 12, 14)
    add_floor(room, 13, 14)
    
    #Add fog
    add_fog(room)

    #Add items
    room.item_list = arcade.SpriteList()
    add_sword(room, 1, 1)
    add_heal(room, 6, 9)
    add_heal(room, 22, 1)
    add_shield(room, 23, 1)

    #Add enemies
    room.enemy_list = arcade.SpriteList()
    add_goblin_1(room, 2, 10)
    add_goblin_1(room, 9, 10)
    add_goblin_1(room, 17, 3)
    add_goblin_1(room, 19, 5)
    add_goblin_2(room, 15, 5)
    add_goblin_2(room, 22, 3)

    #Initialize other lists
    room.visible_list = arcade.SpriteList()
    room.player_attack_list = arcade.SpriteList()
    room.enemy_attack_list = arcade.SpriteList()
    room.accent_list = arcade.SpriteList()

    #Add physics engines to enemies
    add_enemy_engine(room.enemy_list, room.wall_list)

    #Add logic for moving rooms
    room.check_move_room = room_4_move_room

    return room

def setup_room_5():

    room = Room()

    #Add walls
    room.wall_list = arcade.SpriteList()
    for x in range(0, 25):
        add_wall(room, x, 0)
    for x in range(0, 13):
        add_wall(room, x, 14)
    for x in range(15, 25):
        add_wall(room, x, 14)
    for x in range(3, 13):
        add_wall(room, x, 3)
        add_wall(room, x, 4)
    for x in range(15, 20):
        add_wall(room, x, 3)
        add_wall(room, x, 4)
    for y in range(1, 14):
        add_wall(room, 0, y)
        add_wall(room, 24, y)
    for y in range(5, 14):
        add_wall(room, 11, y)
        add_wall(room, 12, y)
        add_wall(room, 15, y)
        add_wall(room, 16, y)
    for y in range(5, 12):
        add_wall(room, 6, y)
    for y in range(5, 10):
        add_wall(room, 7 , y)
    add_wall(room, 7 , 11)
    for y in range(9, 12):
        add_wall(room, 8, y)
    
    #Add floors
    room.floor_list = arcade.SpriteList()
    for x in range(1, 25):
        for y in range(1, 14):
            add_floor(room, x, y)
    add_floor(room, 13, 14)
    add_floor(room, 14, 14)
    add_darkness(room, 7, 10)
    
    #Add fog
    add_fog(room)
        
    #Add items
    room.item_list = arcade.SpriteList()
    add_heal(room, 10, 5)
    add_heal(room, 17, 13)
    add_shield(room, 8, 5)
    add_sword(room, 22, 13)

    #Add enemies
    room.enemy_list = arcade.SpriteList()
    add_goblin_1(room, 4, 7)
    add_goblin_1(room, 18, 8)
    add_goblin_1(room, 19, 10)
    add_goblin_2(room, 2, 11)
    add_goblin_2(room, 22, 6)

    #Initialize other lists
    room.visible_list = arcade.SpriteList()
    room.player_attack_list = arcade.SpriteList()
    room.enemy_attack_list = arcade.SpriteList()
    room.accent_list = arcade.SpriteList()

    #Add physics engines to enemies
    add_enemy_engine(room.enemy_list, room.wall_list)

    #Add logic for moving rooms
    room.check_move_room = room_5_move_room

    return room

def setup_room_6():

    room = Room()
    room.boss_fight = False

    #Add walls
    room.wall_list = arcade.SpriteList()
    for x in range(0, 25):
        add_wall(room, x, 0)
    for x in range(4, 12):
        add_wall(room, x, 14)
    for x in range(2, 7):
        add_wall(room, x, 11)
    for x in range(9, 15):
        add_wall(room, x, 11)
    for x in range(14, 24):
        add_wall(room, x, 14)
    for y in range(1, 15):
        add_wall(room, 0, y)
        add_wall(room, 24, y)
    for y in range(11, 15):
        add_wall(room, 1, y)
    for y in range(12, 14):
        add_wall(room, 14, y)

    #Add floors
    room.floor_list = arcade.SpriteList()
    for x in range(1, 25):
        for y in range(1, 14):
            add_floor(room, x, y)
    for x in (2, 3, 12, 13):
        add_floor(room, x, 14)
    
    #Add fog
    add_fog(room)

    #Add items
    room.item_list = arcade.SpriteList()
    add_heal(room, 1, 1)
    add_heal(room, 12, 1)
    add_heal(room, 15, 13)
    add_heal(room, 23, 13)

    #Add enemies
    room.enemy_list = arcade.SpriteList()
    add_goblin_1(room, 3, 8)
    add_goblin_1(room, 8, 6)
    add_goblin_1(room, 16, 8)
    add_goblin_1(room, 16, 4)
    add_goblin_1(room, 21, 7)
    add_goblin_2(room, 3, 4)
    add_goblin_2(room, 13, 3)
    add_goblin_2(room, 21, 11)
    add_goblin_3(room, 21, 2)

    #Initialize other lists
    room.visible_list = arcade.SpriteList()
    room.player_attack_list = arcade.SpriteList()
    room.enemy_attack_list = arcade.SpriteList()
    room.accent_list = arcade.SpriteList()

    #Add physics engines to enemies
    add_enemy_engine(room.enemy_list, room.wall_list)

    #Add logic for moving rooms
    room.check_move_room = room_6_move_room

    return room