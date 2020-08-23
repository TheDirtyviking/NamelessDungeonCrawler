import arcade
import game
import items
import goblin

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
    shield.left = x * SPRITE_SIZE
    shield.bottom = y * SPRITE_SIZE + 15
    shield.pickup = items.shield_get_picked_up
    room.item_list.append(shield)

def add_heal(room, x, y):
    heal = arcade.Sprite("resources/images/heal.png", .7)
    heal.left = x * SPRITE_SIZE + 15
    heal.bottom = y * SPRITE_SIZE + 15
    heal.pickup = items.heal_get_picked_up
    room.item_list.append(heal)

def add_goblin_1(room, x, y, name):
    gobbo = arcade.Sprite("resources/images/goblin_1.png", .7)
    gobbo.left = x * SPRITE_SIZE + 15
    gobbo.bottom = y * SPRITE_SIZE + 15
    gobbo.Goblin = goblin.Goblin(center_x=gobbo._get_center_x(), center_y=gobbo._get_center_y())
    gobbo.move = gobbo.Goblin.update
    gobbo.name = name
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
                room.visible_list.append(fog)
                room.fog_list.remove(fog)
    for visible in room.visible_list:
        if abs(visible.center_x - player_x) > player_sight * SPRITE_SIZE or abs(visible.center_y - player_y) > player_sight * SPRITE_SIZE:
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
        self.next_room = None
        self.previous_room = None
            

def setup_room_1():
    room = Room()
    room.wall_list = arcade.SpriteList()

    #Create walls on the top and bottom of the screen
    for y in (0, 14):
        for x in range(0, 25):
            add_wall(room, x, y)

    #Create walls on the left and right of the screen
    for x in (0, 24):
        for y in range(1, 14):
            if (y != 4 and y != 5) or x == 0:
                add_wall(room, x , y)

    #Fill the entire screen with floors
    room.floor_list = arcade.SpriteList()
    for x in range(1, 25):
        for y in range(1, 14):
            add_floor(room, x, y)

    #Bottom most wall
    for x in range(3, 24):
        if(x != 18 and x != 19 and x != 12 and x != 11):
            add_wall(room, x, 3)

    #Southern most vertical walls
    add_wall(room, 3, 2)
    add_wall(room, 3, 1)
    add_wall(room, 17, 2)
    add_wall(room, 17, 1)
    for x in (14, 15, 16):
        for y in (1, 2):
            add_darkness(room, x, y)

    #Left most vertical wall
    for y in range(4, 9):
        add_wall(room, 3, y)

    #Top left wall bottom of first opening
    for x in range(4, 9):
        add_wall(room, x, 8)

    #Top most horizontal wall
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

    room.fog_list = arcade.SpriteList()
    for x in range(0, 25):
        for y in range(0, 15):
            fog = arcade.Sprite("resources/images/darkness.png", SPRITE_SCALING)
            fog.left = x * SPRITE_SIZE
            fog.bottom = y * SPRITE_SIZE
            room.fog_list.append(fog)

    room.visible_list = arcade.SpriteList()

    room.item_list = arcade.SpriteList()
    add_torch(room, 23, 13)
    add_sword(room, 23, 1)
    add_heal(room, 4, 1)

    room.enemy_list = arcade.SpriteList()
    add_goblin_1(room, 3, 13, 'one')
    add_goblin_1(room, 5, 11, 'two')
    add_goblin_1(room, 4, 10, 'three')
    
    room.player_attack_list = arcade.SpriteList()
    room.enemy_attack_list = arcade.SpriteList()
    room.accent_list = arcade.SpriteList()

    add_enemy_engine(room.enemy_list, room.wall_list)

    def next_room(x, y):
        return x > SCREEN_WIDTH

    room.next_room = next_room
    
    return room